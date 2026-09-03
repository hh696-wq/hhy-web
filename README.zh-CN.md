# HHY Web

HHY Web 是基于 [HHY Language](https://github.com/hh696-wq/hhy-vm) v1.4.3 Web Runtime 的轻量框架。API 借鉴 Flask 的易用性，运行与部署方式借鉴 Go：显式配置、单进程入口、多 Worker、少魔法。

## 快速开始

```sh
./bin/hhy-web run examples/hello/app.hhy --port 8000 --dev
curl http://127.0.0.1:8000/
```

```hhy
import "../../lib/hhyweb.hhy" as hhyweb

fn home(request) {
    return hhyweb.json({ message: "你好，HHY Web！" })
}

hhyweb.minimal()
    |> hhyweb.get("/", home)
    |> hhyweb.serve({ host: "127.0.0.1", port: to_int(args[0]), workers: 1 })
```

## 已提供能力

- 应用工厂与生产默认值：Request ID、CORS、gzip、健康检查、指标、可信代理。
- GET、POST、PUT、PATCH、DELETE、静态文件与启动服务助手。
- 使用普通 `WebApp -> WebApp` 函数组合 Blueprint，不引入第二套路由语义。
- JSON、文本、HTML、重定向、201、202、204 和统一 Problem JSON 响应。
- JSON 请求解析、Bearer Token、必需 Header、上传、流式响应和 SSE。
- `hhy-web run/check/version` 小型命令行工具。

完整示例见 [`examples/api/app.hhy`](examples/api/app.hhy)。

## 可视化界面

```sh
./bin/hhy-web run examples/dashboard/app.hhy --port 8080
```

启动后打开 <http://127.0.0.1:8080/>。页面会调用 `/api/status` 和
`/api/hello`，并展示 Runtime、Bytecode 引擎、Worker 与 Request ID 状态。

## 验证

```sh
make check HHY=/path/to/hhy
make test HHY=/path/to/hhy
```

生产环境建议在 Caddy、Nginx 或云负载均衡后运行，TLS 与 HTTP/2 交给代理层，并明确限制请求体大小与 Worker 数量。

Apache-2.0
