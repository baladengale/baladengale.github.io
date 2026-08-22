#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# Deploy baladengale-site into the local kind cluster.
#   ./deploy/deploy.sh
#
# Thin wrapper: the whole flow (build image -> kind load -> apply
# namespace/deployment/service/route in order -> cert SAN refresh) lives in
# the kind-infra repo as `make site-deploy` (scripts/90-site.sh).
# Assumes: docker + kind + kubectl + the kind-infra repo (../kind).
# ---------------------------------------------------------------------------
set -euo pipefail

KIND_INFRA_DIR="${KIND_INFRA_DIR:-$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)/kind}"

if [ ! -f "${KIND_INFRA_DIR}/Makefile" ]; then
  echo "kind-infra repo not found at ${KIND_INFRA_DIR} — set KIND_INFRA_DIR" >&2
  exit 1
fi

make -C "${KIND_INFRA_DIR}" site-deploy
