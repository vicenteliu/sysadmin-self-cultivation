# Azure — Labs

Runnable, tear-down-able exercises — same shape as the [AWS labs](../../aws/labs/), so
you feel the concepts *translate* rather than re-learning from scratch.

> **Ground rules:** use a **free / sandbox subscription**, set a **Budget alert**
> first, put everything in a dedicated **resource group**, and delete the resource
> group when done (the cleanest teardown Azure gives you). Reach VMs via **Bastion**
> or `az ssh` — never open SSH/RDP to the internet.

## Planned labs (build order)

1. **`01-scoped-identity-inventory/`** — a least-privilege **Reader** assignment (or a
   scoped service principal), then a script that inventories the subscription via
   **Azure Resource Graph** (or `az resource list`) to CSV. The direct parallel to
   AWS lab 01 — see how the *same* "scoped identity → list everything" move looks in
   Azure. *(next)*
2. **`02-minimal-vnet-vm-terraform/`** — Terraform for a VNet + subnet, an **NSG with
   no inbound**, and one VM with a **managed identity** and **no public IP**, reachable
   via Bastion. Encryption on, `plan` → `apply` → `destroy`. The Azure twin of AWS
   lab 02.
3. **`03-keyvault-managed-identity/`** — a Key Vault + a VM/function that reads a
   secret via its **managed identity** — proving "no secrets in code" the Azure way.
4. **`04-budget-and-policy/`** — a Budget alert + an **Azure Policy** that *denies*
   public IPs or requires encryption — cost and guardrails as code.

Each lab folder will carry: the code (Terraform/Bicep + any script), a `README` with
goal + what to verify, and explicit teardown. Labs land as the module matures.
