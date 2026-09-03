# HHY Web

A small, explicit web framework for [HHY Language](https://github.com/hh696-wq/hhy-vm), inspired by Flask's approachable API and Go's operational simplicity.

HHY Web is a thin framework over HHY v1.4.3 Web Runtime. It adds application defaults, route helpers, composable blueprints, JSON problem responses, body parsing, authentication middleware, streaming helpers, examples, and a small CLI without creating a second HTTP runtime.

## Requirements

- HHY Language v1.4.3 or newer
- Python 3 only for the smoke test

## Hello world

```hhy
import "../../lib/hhyweb.hhy" as hhyweb

fn home(request) {
    return hhyweb.json({ message: "Hello, HHY Web!" })
}

hhyweb.minimal()
    |> hhyweb.get("/", home)
    |> hhyweb.serve({ host: "127.0.0.1", port: to_int(args[0]), workers: 1 })
```

Run it:

```sh
./bin/hhy-web run examples/hello/app.hhy --port 8000 --dev
curl http://127.0.0.1:8000/
```

## Batteries included

- `app(config)` enables request IDs and optionally CORS, gzip, health, metrics, and trusted proxies.
- HTTP helpers: `get`, `post`, `put`, `patch`, `delete`, `static_files`, and `serve`.
- `mount` composes blueprint functions without introducing a separate routing model.
- Responses: `json`, `created`, `accepted`, `no_content`, `problem`, `text`, `html`, and `redirect`.
- Request helpers: `request_json`, multipart uploads, bearer authentication, and required-header middleware.
- Streaming and SSE delegate directly to HHY's bounded, backpressured Runtime.

## Production

Use multiple workers, configure `max_body`, expose metrics only to your monitoring network, and terminate TLS/HTTP/2 at Caddy, Nginx, or a managed load balancer. Enable `trust_proxy` only behind trusted infrastructure.

```hhy
hhyweb.app({
        cors: { origin: "https://app.example.com" },
        gzip: true,
        health: "/healthz",
        metrics: "/metrics",
        trust_proxy: true
    })
    |> hhyweb.mount(api)
    |> hhyweb.serve({ host: "127.0.0.1", port: 8080, max_body: 1048576, workers: 4 })
```

See [`examples/api/app.hhy`](examples/api/app.hhy) for a complete API.

## Development

```sh
make check HHY=/path/to/hhy
make test HHY=/path/to/hhy
```

## Design rules

1. Reuse HHY Value, Error, Stream, cancellation, Router, and worker semantics.
2. Keep configuration explicit and bounded.
3. Prefer ordinary HHY functions and Flow composition over framework magic.
4. Return stable JSON errors at service boundaries.

Apache-2.0
