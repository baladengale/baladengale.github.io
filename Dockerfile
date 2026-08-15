# ---------------------------------------------------------------------------
# bala.dengale — personal site + blog
# Multi-stage: (1) render markdown posts, (2) serve static output with nginx
# ---------------------------------------------------------------------------
FROM python:3.12-alpine AS build
WORKDIR /src
COPY site/ ./
RUN python3 build.py

FROM nginx:1.27-alpine
LABEL org.opencontainers.image.title="baladengale-site" \
      org.opencontainers.image.description="Personal site + blog of Bala Dengale"
COPY --from=build /src/ /usr/share/nginx/html/
COPY deploy/nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 8080
HEALTHCHECK --interval=15s --timeout=2s CMD wget -q -O /dev/null http://127.0.0.1:8080/healthz || exit 1
