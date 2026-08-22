# baladengale-site — personal site + blog, deployed to local kind

Personal website and blog of Bala Dengale (previously `baladengale.is-a.dev` +
`baladengale.blogspot.com`), unified in one place.

```
┌────────────────┐   build.py    ┌─────────────┐  Dockerfile  ┌────────────────┐
│ posts/*.md     │ ───────────▶  │ site/blog/* │ ───────────▶ │ nginx image    │
│ (_TEMPLATE.md) │  (markdown)   │ (html+json) │  (multi-stage│ baladengale-   │
└────────────────┘               └─────────────┘   build)     │ site:latest    │
                                                             └───────┬────────┘
                                                                     │ kind load
                                                        ┌────────────▼─────────────┐
                                                        │ kind ns/baladengale      │
                                                        │ Deployment (2 replicas)  │
                                                        │ Service :8080            │
                                                        │ HTTPRoute ───────────────┼──▶ Gateway
                                                        └──────────────────────────┘   kind-infra
                                                                                     (agentgateway)
                                                        http://baladengale.internal ◀─ host :80
```

## Repository layout

| Path                     | What it is                                              |
|--------------------------|---------------------------------------------------------|
| `site/`                  | the new website (home, workex, blog)                    |
| `site/posts/*.md`        | blog posts in markdown (`_TEMPLATE.md` = standard template) |
| `site/build.py`          | dependency-free markdown → HTML blog builder            |
| `site/blog/`             | generated output (posts, index, `posts.json`) — committed for reuse |
| `Dockerfile`             | multi-stage: python builds blog → nginx serves it on :8080 |
| `deploy/`                | all Kubernetes + gateway artifacts (this folder)         |
| `deploy/nginx.conf`      | server config (pretty URLs, gzip, healthz)              |
| `deploy/namespace.yaml`  | namespace `baladengale`                                 |
| `deploy/deployment.yaml` | 2-replica deployment with probes/resources              |
| `deploy/service.yaml`    | ClusterIP service on 8080, carries `kind-infra.dev/host` annotations |
| `deploy/route.yaml`      | HTTPRoute `baladengale.internal` on the shared Gateway   |
| `deploy/deploy.sh`       | thin wrapper: `make -C ../kind site-deploy`              |

**Hostname routing:** `deploy/route.yaml` puts the site on the kind-infra
repo's shared AgentGateway at `baladengale.internal` (plain YAML, same object
`make sync` would generate from the Service annotations). DNS for
`*.internal` is already handled by dnsmasq — no /etc/hosts edits.

## Writing a new blog post

```bash
cp site/posts/_TEMPLATE.md site/posts/2026-09-01-my-new-post.md
$EDITOR site/posts/_TEMPLATE... # fill front-matter + markdown body
cd site && python3 build.py     # regenerates blog/ output
```

Supported markdown: headings (h2+ become a Contents box), **bold**, *italic*,
`code`, fenced code blocks, links, images, bullet/numbered lists, blockquotes,
tables, horizontal rules.

## Deploy to the local kind cluster

Prereqs: docker, kind (cluster `kind`), kubectl, and the kind-infra repo
(`../kind`) with its AgentGateway wired to host ports 80/443 and dnsmasq
serving `*.internal`.

```bash
./deploy/deploy.sh          # or directly: make -C ../kind site-deploy
```

Builds the image, side-loads it into the nodes, and applies
`namespace.yaml -> deployment.yaml -> service.yaml -> route.yaml` in order,
then rolls the pods and refreshes the Gateway cert SAN.

Open **https://baladengale.internal** (also on plain http :80).

## Teardown

```bash
kubectl delete namespace baladengale   # removes deploy + service + route
docker image rm baladengale-site:latest
```
