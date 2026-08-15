#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# End-to-end deploy of baladengale-site into the local kind cluster.
#   ./deploy/deploy.sh
# Steps: build image -> load into kind -> apply manifests -> register hostname
# Hostname registration goes through the kind-infra repo (AgentGateway):
# the Service carries kind-infra.dev/host annotations, and `make sync`
# creates the baladengale.internal HTTPRoute + refreshes the cert SAN.
# Assumes: docker + kind + kubectl + the kind-infra repo (../kind).
# ---------------------------------------------------------------------------
set -euo pipefail

CLUSTER="${KIND_CLUSTER:-kind}"
IMAGE="baladengale-site:latest"
KIND_INFRA_DIR="${KIND_INFRA_DIR:-$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)/kind}"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "==> Building image ${IMAGE}"
docker build -t "${IMAGE}" "${REPO_ROOT}"

echo "==> Loading image into kind cluster '${CLUSTER}'"
kind load docker-image "${IMAGE}" --name "${CLUSTER}"

echo "==> Applying Kubernetes manifests"
kubectl apply -f "${REPO_ROOT}/deploy/namespace.yaml"
kubectl apply -f "${REPO_ROOT}/deploy/deployment.yaml"
kubectl apply -f "${REPO_ROOT}/deploy/service.yaml"

echo "==> Waiting for rollout"
kubectl -n baladengale rollout status deploy/baladengale-site --timeout=120s

echo "==> Registering baladengale.internal via kind-infra gateway"
if [ -f "${KIND_INFRA_DIR}/Makefile" ]; then
  make -C "${KIND_INFRA_DIR}" sync
else
  echo "kind-infra repo not found at ${KIND_INFRA_DIR} — set KIND_INFRA_DIR" >&2
  exit 1
fi

echo
echo "==> Done. Open: https://baladengale.internal  (DNS: *.${INTERNAL_DOMAIN:-internal} via dnsmasq)"
