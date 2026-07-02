# Endpoint & MDM

> 🚧 **Opening written; body in progress.** The framework below is complete —
> what this module will cover is fixed; the prose is being filled in.

> One of the densest demand clusters in the whole signal, and the platform folders
> don't cover it: managing the fleet of laptops and phones that people actually
> work on. This is a first-class track because it's a first-class job — and it's
> the one written from the deepest hands-on experience in this repo.

Endpoint management is the discipline of taking thousands of heterogeneous devices
— macOS, Windows, iOS, Android — and making them consistent, secure, and
self-provisioning without a human touching each one. It's the same
*register → image → personalize → maintain* pipeline as [`the-stack/03`](../the-stack/03-compute-and-images.md),
pointed at the endpoint instead of the server, and it's **✋ hands-on depth**: a
multi-OS deployment platform built from scratch and operated at ~100k-device scale.

## Planned coverage

- **The MDM/UEM model** — enrollment, configuration profiles, policy, and
  compliance as the endpoint's version of infrastructure-as-code. Jamf (macOS) and
  VMware Workspace ONE / UEM operated hands-on; the "two industry-standard MDMs"
  bar met for real.
- **Imaging & provisioning** — PXE, custom images, and zero-touch first boot; the
  warehouse reality of imaging hundreds of machines a day; full-disk encryption
  enrolled at scale.
- **Software & patch lifecycle** — application packaging, distribution targeted by
  user/group/region, and patch compliance as daily operations.
- **Endpoint security** — EDR/XDR (Defender for Endpoint → SentinelOne, migrated
  and operated from both consoles), device security-configuration and
  network-admission compliance checks — the endpoint slice of [`the-stack/07`](../the-stack/07-security.md).
- **BYOD** — iOS/Android enrollment, the identity and separation questions, and the
  UAG/tunnel plumbing that makes personal devices safe to trust (scoped honestly:
  enrollment and lifecycle, not fleet compliance-profile mastery).
- **Where Intune is a ramp** — the Microsoft endpoint stack (Intune/Autopilot) is
  🧗, not ✋; the discipline transfers, the specific console is a lookup.

## Honest boundaries

✋ **hands-on depth — the core lane.** Designed and ran a multi-OS (Win/macOS/Linux)
PXE and image-based deployment platform adopted org-wide, cumulatively provisioning
100k+ devices; Jamf + Workspace ONE operated hands-on; packaging, patch compliance,
FDE, and EDR deploy/migration all daily work. 🧗 where marked: Intune/Autopilot
(different console, same discipline) and deep iOS/Android compliance-profile
engineering (enrollment/lifecycle is ✋; fleet-profile mastery is a ramp).
