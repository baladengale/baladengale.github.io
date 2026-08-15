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
| `deploy/deploy.sh`       | one-shot: build → load → apply → register via kind-infra |

**Hostname routing:** there is no hand-rolled HTTPRoute here. The Service is
annotated with `kind-infra.dev/host=baladengale`, and the kind-infra repo's
`make sync` (or `make expose HOST=baladengale NS=baladengale SVC=baladengale-site PORT=8080`)
creates the HTTPRoute on the shared AgentGateway and refreshes the cert SAN.
DNS for `*.internal` is already handled by dnsmasq — no /etc/hosts edits.

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
./deploy/deploy.sh
```

Open **https://baladengale.internal** (also on plain http :80).

## Teardown

```bash
make -C ../kind unexpose HOST=baladengale    # remove gateway route
kubectl delete namespace baladengale         # removes deploy + service
docker image rm baladengale-site:latest
```
