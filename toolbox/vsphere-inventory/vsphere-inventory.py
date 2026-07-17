#!/usr/bin/env python3
"""Read-only vSphere inventory over the SOAP API — pure stdlib, no SDK.

Talks vim25 directly (XML over HTTPS via urllib) so the only requirement is
Python 3.9+. Collects VMs (with disks, NICs, firmware, snapshots), hosts,
datastores, and networks into one JSON document — the shared schema
pve-inventory emits, so the two sides of a migration can be compared.
See README.md for the schema and the honest scope.
"""

import argparse
import csv
import datetime
import json
import os
import ssl
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET

VIM = "urn:vim25"
ENVELOPE = """<?xml version="1.0" encoding="UTF-8"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
 xmlns:xsd="http://www.w3.org/2001/XMLSchema">
<soapenv:Body>{body}</soapenv:Body></soapenv:Envelope>"""

VM_PROPS = [
    "name", "runtime.powerState", "config.guestFullName", "config.firmware",
    "config.version", "config.hardware.numCPU", "config.hardware.memoryMB",
    "config.hardware.device", "snapshot.rootSnapshotList",
]
HOST_PROPS = ["name", "summary.hardware.numCpuCores", "summary.hardware.memorySize",
              "summary.config.product.fullName"]
DS_PROPS = ["summary.name", "summary.capacity", "summary.freeSpace", "summary.type"]
NET_PROPS = ["name"]

NIC_MODELS = {  # vim25 device class → common name
    "VirtualVmxnet3": "vmxnet3", "VirtualVmxnet2": "vmxnet2", "VirtualVmxnet": "vmxnet",
    "VirtualE1000": "e1000", "VirtualE1000e": "e1000e", "VirtualPCNet32": "pcnet32",
    "VirtualSriovEthernetCard": "sriov",
}


def die(msg, code):
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(code)


class Soap:
    """A minimal vim25 SOAP client: one endpoint, one session cookie."""

    def __init__(self, server, insecure):
        self.url = f"https://{server}/sdk"
        ctx = ssl.create_default_context()
        if insecure:
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
        self.opener = urllib.request.build_opener(
            urllib.request.HTTPSHandler(context=ctx))
        self.cookie = None

    def call(self, body):
        req = urllib.request.Request(
            self.url, data=ENVELOPE.format(body=body).encode(),
            headers={"Content-Type": "text/xml; charset=utf-8",
                     "SOAPAction": "urn:vim25/8.0.0.0"})
        if self.cookie:
            req.add_header("Cookie", self.cookie)
        try:
            with self.opener.open(req, timeout=60) as resp:
                cookie = resp.headers.get("Set-Cookie")
                if cookie and "vmware_soap_session" in cookie:
                    self.cookie = cookie.split(";")[0]
                return ET.fromstring(resp.read())
        except urllib.error.HTTPError as e:
            detail = e.read().decode(errors="replace")
            fault = ET.fromstring(detail).find(".//{*}faultstring") if detail else None
            die(f"vCenter fault: {fault.text if fault is not None else e}", 1)
        except (urllib.error.URLError, OSError) as e:
            die(f"cannot reach {self.url}: {e}", 1)


def text(root, tag):
    el = root.find(f".//{{{VIM}}}{tag}")
    return el.text if el is not None else None


def xsi_type(el):
    t = el.get("{http://www.w3.org/2001/XMLSchema-instance}type") or ""
    return t.split(":")[-1]


def prop_map(obj_el):
    """One ObjectContent element → {property path: <val> element}."""
    props = {}
    for ps in obj_el.findall(f"{{{VIM}}}propSet"):
        props[ps.find(f"{{{VIM}}}name").text] = ps.find(f"{{{VIM}}}val")
    return props


def retrieve(soap, pc, view, obj_type, paths):
    """All objects of obj_type in the container view, with the given props."""
    pathset = "".join(f"<pathSet>{p}</pathSet>" for p in paths)
    body = f"""<RetrievePropertiesEx xmlns="urn:vim25">
      <_this type="PropertyCollector">{pc}</_this>
      <specSet>
        <propSet><type>{obj_type}</type>{pathset}</propSet>
        <objectSet>
          <obj type="ContainerView">{view}</obj><skip>true</skip>
          <selectSet xsi:type="TraversalSpec">
            <name>view</name><type>ContainerView</type><path>view</path><skip>false</skip>
          </selectSet>
        </objectSet>
      </specSet><options/>
    </RetrievePropertiesEx>"""
    out = []
    resp = soap.call(body)
    while True:
        out += [prop_map(o) for o in resp.iter(f"{{{VIM}}}objects")]
        token = text(resp, "token")
        if not token:
            return out
        resp = soap.call(
            f'<ContinueRetrievePropertiesEx xmlns="urn:vim25">'
            f'<_this type="PropertyCollector">{pc}</_this>'
            f'<token>{token}</token></ContinueRetrievePropertiesEx>')


def parse_devices(val):
    """config.hardware.device <val> → (disks, nics)."""
    disks, nics = [], []
    if val is None:
        return disks, nics
    for dev in val:
        kind = xsi_type(dev)
        backing = dev.find(f"{{{VIM}}}backing")
        if kind == "VirtualDisk":
            cap = dev.find(f"{{{VIM}}}capacityInKB")
            label = dev.find(f"{{{VIM}}}deviceInfo/{{{VIM}}}label")
            bkind = xsi_type(backing) if backing is not None else ""
            thin = backing.find(f"{{{VIM}}}thinProvisioned") if backing is not None else None
            disks.append({
                "label": label.text if label is not None else "disk",
                "capacity_gb": round(int(cap.text) / 1048576, 1) if cap is not None else None,
                "thin": thin is not None and thin.text == "true",
                "backing": "rdm" if "RawDiskMapping" in bkind else "vmdk",
            })
        elif kind in NIC_MODELS:
            mac = dev.find(f"{{{VIM}}}macAddress")
            net = None
            if backing is not None:
                dn = backing.find(f"{{{VIM}}}deviceName")
                port = backing.find(f"{{{VIM}}}port/{{{VIM}}}portgroupKey")
                net = dn.text if dn is not None else (port.text if port is not None else None)
            nics.append({"model": NIC_MODELS[kind], "network": net,
                         "mac": mac.text if mac is not None else None})
    return disks, nics


def parse_snapshots(val):
    """snapshot.rootSnapshotList <val> → [{name, created, depth}, ...]."""
    out = []

    def walk(node, depth):
        name = node.find(f"{{{VIM}}}name")
        created = node.find(f"{{{VIM}}}createTime")
        out.append({"name": name.text if name is not None else None,
                    "created": created.text if created is not None else None,
                    "depth": depth})
        for child in node.findall(f"{{{VIM}}}childSnapshotList"):
            walk(child, depth + 1)

    if val is not None:
        for root in val.findall(f"{{{VIM}}}VirtualMachineSnapshotTree"):
            walk(root, 1)
    return out


def collect(server, user, password, insecure):
    soap = Soap(server, insecure)
    sc = soap.call('<RetrieveServiceContent xmlns="urn:vim25">'
                   '<_this type="ServiceInstance">ServiceInstance</_this>'
                   '</RetrieveServiceContent>')
    session_mgr = text(sc, "sessionManager")
    root_folder = text(sc, "rootFolder")
    pc = text(sc, "propertyCollector")
    view_mgr = text(sc, "viewManager")
    api = text(sc, "fullName") or "vSphere"

    soap.call(f'<Login xmlns="urn:vim25"><_this type="SessionManager">{session_mgr}</_this>'
              f'<userName>{user}</userName><password>{password}</password></Login>')

    def view_of(kind):
        r = soap.call(
            f'<CreateContainerView xmlns="urn:vim25">'
            f'<_this type="ViewManager">{view_mgr}</_this>'
            f'<container type="Folder">{root_folder}</container>'
            f'<type>{kind}</type><recursive>true</recursive></CreateContainerView>')
        return text(r, "returnval")

    vms = []
    for p in retrieve(soap, pc, view_of("VirtualMachine"), "VirtualMachine", VM_PROPS):
        disks, nics = parse_devices(p.get("config.hardware.device"))
        snaps = parse_snapshots(p.get("snapshot.rootSnapshotList"))
        power = (p.get("runtime.powerState").text or "").replace("powered", "") \
            if p.get("runtime.powerState") is not None else None
        vms.append({
            "name": p["name"].text,
            "power": power.lower() if power else None,
            "vcpus": int(p["config.hardware.numCPU"].text) if p.get("config.hardware.numCPU") is not None else None,
            "memory_mb": int(p["config.hardware.memoryMB"].text) if p.get("config.hardware.memoryMB") is not None else None,
            "guest_os": p["config.guestFullName"].text if p.get("config.guestFullName") is not None else None,
            "firmware": p["config.firmware"].text if p.get("config.firmware") is not None else None,
            "hw_version": p["config.version"].text if p.get("config.version") is not None else None,
            "disks": disks, "nics": nics,
            "snapshots": len(snaps), "snapshot_detail": snaps,
        })

    hosts = [{
        "name": p["name"].text,
        "cpu_cores": int(p["summary.hardware.numCpuCores"].text) if p.get("summary.hardware.numCpuCores") is not None else None,
        "memory_mb": round(int(p["summary.hardware.memorySize"].text) / 1048576) if p.get("summary.hardware.memorySize") is not None else None,
        "product": p["summary.config.product.fullName"].text if p.get("summary.config.product.fullName") is not None else None,
    } for p in retrieve(soap, pc, view_of("HostSystem"), "HostSystem", HOST_PROPS)]

    datastores = [{
        "name": p["summary.name"].text,
        "capacity_gb": round(int(p["summary.capacity"].text) / 1073741824, 1) if p.get("summary.capacity") is not None else None,
        "free_gb": round(int(p["summary.freeSpace"].text) / 1073741824, 1) if p.get("summary.freeSpace") is not None else None,
        "type": p["summary.type"].text if p.get("summary.type") is not None else None,
    } for p in retrieve(soap, pc, view_of("Datastore"), "Datastore", DS_PROPS)]

    networks = [{"name": p["name"].text}
                for p in retrieve(soap, pc, view_of("Network"), "Network", NET_PROPS)]

    soap.call(f'<Logout xmlns="urn:vim25"><_this type="SessionManager">{session_mgr}</_this></Logout>')

    return {
        "source": {"kind": "vsphere", "endpoint": server, "product": api,
                   "collected_at": datetime.datetime.now(datetime.timezone.utc)
                       .strftime("%Y-%m-%dT%H:%M:%SZ")},
        "vms": vms, "hosts": hosts, "datastores": datastores, "networks": networks,
    }


def write_csv(inv, path):
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["name", "power", "vcpus", "memory_mb", "guest_os", "firmware",
                    "disks", "disk_gb_total", "nic_models", "snapshots"])
        for vm in inv["vms"]:
            w.writerow([
                vm["name"], vm["power"], vm["vcpus"], vm["memory_mb"], vm["guest_os"],
                vm["firmware"], len(vm["disks"]),
                round(sum(d["capacity_gb"] or 0 for d in vm["disks"]), 1),
                " ".join(sorted({n["model"] for n in vm["nics"]})), vm["snapshots"],
            ])


def main():
    ap = argparse.ArgumentParser(description="Read-only vSphere inventory (stdlib SOAP).")
    ap.add_argument("--server", required=True, help="vCenter/ESXi host[:port]")
    ap.add_argument("--user", required=True)
    ap.add_argument("--password", help="prefer VSPHERE_PASSWORD env over this flag")
    ap.add_argument("--insecure", action="store_true",
                    help="skip TLS verification (self-signed lab vCenter)")
    ap.add_argument("--out", metavar="FILE", help="write JSON here instead of stdout")
    ap.add_argument("--csv", metavar="FILE", help="also write a per-VM summary CSV")
    args = ap.parse_args()

    password = args.password or os.environ.get("VSPHERE_PASSWORD")
    if not password:
        die("no password: set VSPHERE_PASSWORD or pass --password", 2)

    inv = collect(args.server, args.user, password, args.insecure)

    doc = json.dumps(inv, indent=2)
    if args.out:
        with open(args.out, "w") as f:
            f.write(doc + "\n")
    else:
        print(doc)
    if args.csv:
        write_csv(inv, args.csv)
    print(f"inventory: {len(inv['vms'])} VM(s), {len(inv['hosts'])} host(s), "
          f"{len(inv['datastores'])} datastore(s), {len(inv['networks'])} network(s)",
          file=sys.stderr)


if __name__ == "__main__":
    main()
