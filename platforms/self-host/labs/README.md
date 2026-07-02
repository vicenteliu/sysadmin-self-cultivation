# Self-Hosted / Bare Metal — Labs

Pure-local, tear-down-able exercises. Where the clouds need an account, this platform
needs a laptop with nested virtualization — the honest way to practice bare-metal
discipline without a data centre.

> **Ground rules:** run these in a **throwaway VM / nested hypervisor** (Proxmox,
> libvirt/KVM, or Workstation/Fusion). Nothing here needs real hardware — the point is
> the *pipeline and the reflexes*, which are identical at any scale.

## Why the command line

Self-hosting is the platform where there *is* no GUI for most of it — and where the
CLI's virtues are sharpest. `virsh`, `ipmitool`, `ansible`, and plain shell are
**faster** (no console you can even reach for a headless box), **exact**, **repeatable**
(the pipeline runs the same on machine #1 and machine #10,000), and **reviewable**.
More than that: bare metal has **no undo** — a command you can read, version, and
review is the only safe way to touch it ([`foundations/`](../../../foundations/)).

## The three-lab arc

### Lab 01 — Inventory the fleet (from code, not a spreadsheet)

The "list everything" move on hardware you own — Ansible ad-hoc against an inventory,
plus out-of-band reach via IPMI:

```bash
# inventory facts across the fleet — one command, every host
ansible all -i inventory.ini -m setup -a 'filter=ansible_hostname,ansible_distribution,ansible_memtotal_mb'

# a quick health sweep: uptime + free disk + load, everywhere
ansible all -i inventory.ini -a 'df -h / '
ansible all -i inventory.ini -a 'uptime'

# reach a box with NO OS via its BMC — the cloud "serial console" is a rental of this
ipmitool -I lanplus -H 10.0.0.50 -U admin -P "$BMC_PW" chassis power status
ipmitool -I lanplus -H 10.0.0.50 -U admin -P "$BMC_PW" sdr type temperature   # sensors
```

**Verify:** you inventoried the fleet without logging into a single box by hand, and
reached a powered-off machine over IPMI — out-of-band management, working.

### Lab 02 — Provision a node hands-off (the pipeline)

The signature self-host skill: network-boot a blank machine into a working one with no
hands ([`the-stack/03`](../../../the-stack/03-compute-and-images.md)). In a nested lab,
`virt-install` stands in for PXE + image + cloud-init:

```bash
# build a cloud-init seed (the personalization the pipeline injects at first boot)
cat > user-data <<'EOF'
#cloud-config
hostname: lab-node01
users: [{name: ops, sudo: 'ALL=(ALL) NOPASSWD:ALL', ssh_authorized_keys: [ssh-ed25519 AAAA...]}]
package_update: true
packages: [qemu-guest-agent]
EOF
cloud-localds seed.img user-data                 # pack it into a seed disk

# "PXE-equivalent" hands-off install from a cloud image + the seed
virt-install --name lab-node01 --memory 2048 --vcpus 2 \
  --disk /var/lib/libvirt/images/lab-node01.qcow2,size=10 \
  --disk seed.img,device=cdrom \
  --import --os-variant ubuntu22.04 --noautoconsole

virsh list --all                                 # the node came up with no console typing
```

**Verify:** the node boots already-personalized (hostname, user, packages) — no
installer clicked through. Re-run to prove it's **repeatable and idempotent**.

### Lab 03 — Failure domains + the RAID truth (the drills)

Two of the repo's most tangible lessons, on the platform they came from:

```bash
# FAILURE DOMAINS: define two "racks" (host groups), place a 2-replica service across
# them, then kill a "rack" and watch what survives (nested VMs standing in for hosts):
virsh destroy rack-a-node1     # simulate a rack/host failure (hard power off)
# ...the replica on rack-b keeps serving. That's a failure domain, in your hands.

# RAID IS NOT BACKUP: build a software RAID1, then prove it survives a DISK death
# but NOT a logical delete:
mdadm --create /dev/md0 --level=1 --raid-devices=2 /dev/vdb /dev/vdc
mkfs.ext4 /dev/md0 && mount /dev/md0 /mnt && echo "data" > /mnt/canary
mdadm /dev/md0 --fail /dev/vdb --remove /dev/vdb   # kill a disk — data SURVIVES (RAID's job)
cat /mnt/canary                                    # still there
rm /mnt/canary                                     # a logical delete — RAID replicated it away
# the canary is GONE on both disks. RAID ≠ backup — recover from the independent copy.
```

**Verify:** the service survives a "rack" loss; the RAID array survives a disk death
but not an `rm` — exactly the distinction [`the-stack/04`](../../../the-stack/04-storage.md)
draws, felt in your hands. Pair this with the runnable
[backup drill](../../../the-stack/labs/04-backup-not-snapshot/).

---

Honest note: this is the ✋ platform — the deepest root. These labs are the fleet work
written down, and they're the most reproducible in the repo because they need nothing
but a laptop.
