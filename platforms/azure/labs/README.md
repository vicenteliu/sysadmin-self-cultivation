# Azure — Labs

Runnable, tear-down-able exercises — same shape as the [AWS labs](../../aws/labs/), so
you feel the concepts *translate* rather than re-learning from scratch.

> **Ground rules:** use a **free / sandbox subscription**, set a **Budget alert**
> first, put everything in a dedicated **resource group**, and delete the resource
> group when done (the cleanest teardown Azure gives you). Reach VMs via **Bastion**
> or `az ssh` — never open SSH/RDP to the internet.

## Why the command line

Every lab here is **CLI-first** (`az`, with PowerShell `Az` as the equal alternative),
and that's a teaching choice. The portal is for *looking*; the CLI is for *doing*. An
`az` command is **faster** than a blade-hunt, **exact** (no wrong dropdown), **repeatable**
(paste into a runbook), and **reviewable** (a diff, not a screen recording) — the same
surface your automation uses. Anything you can click, you can command; the command is
what you hand to the next person or machine.

## The three-lab arc

### Lab 01 — Scoped identity + inventory

A least-privilege **Reader**, then inventory the subscription — the Azure twin of AWS
lab 01. Note **Azure Resource Graph** answers org-wide questions in one query instead
of looping (an Azure strength):

```bash
az login
az account show --query '{sub:name, id:id}' -o table     # confirm the right subscription

# the whole subscription, one query — Resource Graph (beats per-resource looping)
az graph query -q "Resources | project name, type, location, resourceGroup | order by type asc" -o table

# or the classic per-service list
az vm list -d --query '[].{name:name, rg:resourceGroup, size:hardwareProfile.vmSize, power:powerState}' -o table
az storage account list --query '[].{name:name, rg:resourceGroup, kind:kind}' -o table
```

**Verify:** narrow the Reader scope to one resource group, re-run, and watch the rest
vanish from results — the scoping made visible.

### Lab 02 — Minimal VNet + VM from code

A VNet + subnet, an **NSG with no inbound**, one VM with a **managed identity** and
**no public IP**, reachable via Bastion. From the CLI (Terraform/Bicep is the
persistent form; here's the imperative walkthrough):

```bash
az group create -n lab-rg -l eastus
az network vnet create -g lab-rg -n lab-vnet --address-prefix 10.0.0.0/16 \
  --subnet-name app --subnet-prefix 10.0.1.0/24
az network nsg create -g lab-rg -n lab-nsg          # default = no inbound allow. Good.
az vm create -g lab-rg -n lab-vm --image Ubuntu2204 \
  --vnet-name lab-vnet --subnet app --nsg lab-nsg \
  --public-ip-address "" --assign-identity \
  --admin-username azureuser --generate-ssh-keys
# reach it with NO public IP — Bastion tunnel:
az network bastion ssh -n lab-bastion -g lab-rg --target-resource-id "$(az vm show -g lab-rg -n lab-vm --query id -o tsv)" --auth-type ssh-key --username azureuser --ssh-key ~/.ssh/id_rsa
```

**Verify:** `az vm show -d -g lab-rg -n lab-vm --query publicIps -o tsv` returns empty
— no public exposure. **Teardown:** `az group delete -n lab-rg --yes --no-wait`.

### Lab 03 — Secure storage + a policy guardrail

Secure defaults and a *preventive* guardrail (Azure Policy that makes the wrong thing
impossible, not just alerted):

```bash
# a storage account that refuses public blob access + enforces HTTPS
az storage account create -g lab-rg -n labstor$RANDOM -l eastus --sku Standard_LRS \
  --allow-blob-public-access false --https-only true --min-tls-version TLS1_2

# a Budget alert (set this FIRST in real life)
az consumption budget create --budget-name lab-budget --amount 20 --time-grain Monthly \
  --category Cost --start-date 2026-07-01 --end-date 2027-07-01

# a preventive guardrail: DENY any storage account that allows public blob access
az policy assignment create --name deny-public-blob \
  --policy "$(az policy definition list --query "[?displayName=='Storage accounts should prevent shared key access'].name | [0]" -o tsv)" \
  --resource-group lab-rg
```

**Verify:** try to flip `--allow-blob-public-access true` and watch the policy deny it.
**Teardown:** folded into `az group delete -n lab-rg`.

---

Each lab lands with the code (Terraform/Bicep + any script), a `README`, and explicit
teardown. The **Entra/identity** slice (lab 01's scoped role) is the one written from
hands-on ground; the rest is the honest ramp.
