# Kubernetes & Containers

> 🚧 **Opening written; body in progress.** The framework below is complete —
> what this module will cover is fixed; the prose is being filled in.

> [`the-stack/05`](../the-stack/05-platform-services.md) placed Kubernetes on the
> build-vs-rent spectrum; this note goes a layer deeper into the thing itself —
> because "managed Kubernetes" still requires you to understand Kubernetes the
> moment it misbehaves. The abstraction leaks, and this is what's underneath.

Kubernetes is the most portable platform in the whole repo — an EKS cluster, an AKS
cluster, and a self-run cluster are the same API with different control-plane
owners — which is exactly why it's worth learning once, properly. This note covers
the object model and the operator's-eye view: not "how to write a microservice,"
but "how to run the thing, and debug it when a pod won't start."

## Planned coverage

- **The object model** — pods, deployments, services, ingress, configmaps/secrets,
  namespaces: the nouns, and how a request actually reaches a container.
- **The control plane** — API server, etcd, scheduler, controller-manager, kubelet;
  what the managed offerings run for you (and what they don't).
- **Managed vs. self-run** — EKS/AKS/GKE/OKE remove the etcd-and-upgrades toil but
  not the understanding; GKE as the reference. When self-running is a platform-team
  commitment (the recurring control-plane-as-product theme).
- **Networking & storage plumbing** — CNI and CSI: the leak points where
  [`the-stack/02`](../the-stack/02-network.md) and [`the-stack/04`](../the-stack/04-storage.md)
  resurface inside the cluster.
- **The debugging reflex** — `kubectl describe`/`logs`/`events`, why a pod is
  `Pending` vs. `CrashLoopBackOff`, and reading the cluster the way you read a Linux
  box.
- **The AI-assisted ramp** — AI writes YAML fluently and hallucinates fields and API
  versions just as fluently; every manifest gets validated against the cluster, not
  trusted from the chat.

## Honest boundaries

🧗 **honest ramp — clearly labeled.** Docker and image building are ✋
([`the-stack/03`](../the-stack/03-compute-and-images.md)), but Kubernetes here is
**test-environment scope, not production platform ownership** — the object model and
operator mechanics are understood and mapped via the method above, not claimed as
years running production clusters or on-call for a fleet. Where the repo needs a
production-K8s claim, it doesn't make one; this note is the honest ramp onto it.
