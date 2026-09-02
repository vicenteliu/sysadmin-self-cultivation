---
kind: guided-run
axis: platforms
themes: [cloud]
platforms: [openstack]
marker: "🧭"
summary: "Three guided runs against DevStack — a single-node, all-in-one OpenStack in a VM, the honest way to meet the platform's plumbing without a data centre."
---
# OpenStack — Guided runs

> 🌐 **Languages:** English (default) · [中文](../../../docs/zh/platforms/openstack/labs/README.md)

Three guided runs against **DevStack** — a single-node, all-in-one OpenStack in a VM,
the honest way to meet the platform's plumbing without a data centre.

**These are [guided runs](../../../CONTEXT.md), not labs.** Each needs a real environment,
so nothing here can assert that you did it and CI cannot run it. That is the whole of the
distinction and it is not a demotion — a guided run reaches real latency, real error
messages and real bills, which no model does.

> **Ground rules:** run **DevStack** in a throwaway VM (it's not for production and
> re-stacks cleanly). `source` your credentials file first (`source openrc admin
> admin`). Delete resources when done.

## Why the command line

OpenStack has Horizon (a web dashboard) — and operators live in the **`openstack`
CLI**, because it's **faster**, **exact**, **repeatable** (the same commands across
every deployment), **reviewable**, and the same surface Heat/Terraform drive. Horizon
is for looking; the unified `openstack` client is for operating. One binary, every
service.

## The three-run arc

### Run 01 — Identity + inventory (Keystone, the front door)

Everything authenticates through **Keystone**; inventory a project from the CLI:

```bash
source openrc admin admin                            # load credentials into the env
openstack token issue                                # confirm auth works

# create a project (tenant) and a scoped user
openstack project create lab
openstack user create --project lab --password-prompt labuser
openstack role add --project lab --user labuser member

# inventory — the same 'list' verb across every service
openstack server list --all-projects -c Name -c Status -c Networks
openstack network list -c Name -c Subnets
openstack volume list -c Name -c Status -c Size
```

**Verify:** re-source as `labuser` (a scoped, non-admin identity) and watch
`--all-projects` stop working — Keystone scoping made visible.

### Run 02 — Network + instance (Nova over KVM, Neutron)

A tenant network, a router to the external net, and an instance — the KVM you may know,
wrapped in the cloud control plane:

```bash
# a tenant network + subnet, and a router out to the provider network
openstack network create lab-net
openstack subnet create --network lab-net --subnet-range 10.0.1.0/24 lab-subnet
openstack router create lab-router
openstack router set --external-gateway public lab-router
openstack router add subnet lab-router lab-subnet

# a security group that allows SSH, then launch an instance with a flavor
openstack security group rule create --proto tcp --dst-port 22 default
openstack server create --flavor m1.small --image ubuntu-22.04 \
  --network lab-net --security-group default --key-name mykey lab-vm

# a floating IP to reach it
openstack floating ip create public
openstack server add floating ip lab-vm <FLOATING_IP>
```

**Verify:** `openstack server show lab-vm -c status -c addresses` shows ACTIVE with the
floating IP; you can SSH in. **Teardown:** delete the server, floating IP, router
interfaces, subnet, network.

### Run 03 — The control-plane failure drill (the real lesson)

The lesson unique to "you build the cloud" — the API can die while your VMs keep
running ([`the-stack/01`](../../../the-stack/01-physical.md)):

```bash
# note: your instance is ACTIVE and reachable
openstack server list

# now WEDGE the control plane — stop a core service (on DevStack, a systemd unit)
sudo systemctl stop devstack@n-api            # Nova API down

# the API now fails...
openstack server list                          # ERROR — the control plane is down

# ...but the running instance is UNTOUCHED — ping it, SSH it: still up.
ping <FLOATING_IP>                             # still answers

# recover:
sudo systemctl start devstack@n-api
openstack server list                          # works again
```

**Verify:** the running VM survives the API outage untouched — the control-plane-as-
product reality you *feel* here, not read. **Teardown:** re-stack or delete the lab
resources.

## Beyond the arc — a pure-local drill

The three-run arc above needs DevStack in a VM. One more lab needs **nothing** — a
pure-local, stdlib-only, self-verifying drill tied to the [operations note](../operations.md):

### `the-cloud-is-down-the-vms-are-up/` — the control plane, wedged ✅ built (pure-local)

Runs the third step above as a model: a full queue stops every API call while nine
instances keep answering, the tenant-only dashboard stays green, and a compute host that
dies during the wedge cannot be evacuated until the queue drains — the moment a
control-plane outage becomes the tenants'. See **[`the-cloud-is-down-the-vms-are-up/`](the-cloud-is-down-the-vms-are-up/)**.

```bash
python3 the-cloud-is-down-the-vms-are-up/control_plane_drill.py   # exit 0 = the lessons held; runs in CI
```

---

Honest note: OpenStack is a 🧭 ramp — DevStack makes it a runnable one, and lab 03 is
the piece that turns the "control plane is now yours" warning from theory into muscle.
