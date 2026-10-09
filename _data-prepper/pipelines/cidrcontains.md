---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: cidrContains()
parent: Functions
grand_parent: Pipelines
nav_order: 5
---

<!-- vale off -->
# cidrContains() 函式
<!-- vale on -->

`cidrContains()` 函式用於檢查 IP 位址是否包含在指定的無類別網域間路由（CIDR）區塊或 CIDR 區塊範圍內。此函式接受兩個或更多引數：

- 第一個引數是 JSON 指標，代表包含待檢查 IP 位址的欄位所對應的鍵或路徑。它支援 IPv4 和 IPv6 位址格式。

- 後續引數是代表一個或多個 CIDR 區塊或 IP 位址範圍的字串。此函式會檢查第一個引數指定的 IP 位址是否符合或包含在這些 CIDR 區塊中的任一個內。

例如，如果您的資料包含名為 `client.ip` 的 IP 位址欄位，且您想檢查它是否屬於 CIDR 區塊 `192.168.0.0/16` 或 `10.0.0.0/8`，您可以如下使用 `cidrContains()` 函式：

```
cidrContains('/client.ip', '192.168.0.0/16', '10.0.0.0/8')
```
{% include copy.html %}

如果 IP 位址符合任一指定的 CIDR 區塊，此函式會傳回 `true`；如果不符合，則傳回 `false`。

## 範例

下列管線會捨棄不屬於指定 CIDR 區塊的所有文件：

```yaml
cidr-allowlist-pipeline:
  source:
    http:
      path: /events
      ssl: true
      sslKeyCertChainFile: certs/dp.crt
      sslKeyFile: certs/dp.key
  processor:
    - drop_events:
        # Drop events whose client IP is NOT in specific CIDR allowlist
        drop_when: 'not cidrContains(/client/ip, "10.0.0.0/8", "192.168.0.0/16", "fd00::/8")'
  sink:
    - opensearch:
        hosts: ["https://opensearch:9200"]
        insecure: true
        username: admin
        password: admin_pass
        index_type: custom
        index: logs-%{yyyy.MM.dd}
```
{% include copy.html %}

您可以使用下列命令測試此管線：

```bash
curl -ksS -X POST "https://localhost:2021/events" \
  -H "Content-Type: application/json" \
  -d '[
    {"client":{"ip":"10.23.45.6"},"msg":"allowed 10/8"},
    {"client":{"ip":"8.8.8.8"},"msg":"should be dropped"},
    {"client":{"ip":"fd00::1234"},"msg":"allowed ULA IPv6"}
  ]'
```
{% include copy.html %}

儲存在 OpenSearch 中的文件包含下列資訊：

```json
{
  ...
  "hits": {
    "total": {
      "value": 2,
      "relation": "eq"
    },
    "max_score": 1,
    "hits": [
      {
        "_index": "logs-2025.10.14",
        "_id": "Ng1i4pkBLPEKXekW48BU",
        "_score": 1,
        "_source": {
          "client": {
            "ip": "10.23.45.6"
          },
          "msg": "allowed 10/8"
        }
      },
      {
        "_index": "logs-2025.10.14",
        "_id": "Nw1i4pkBLPEKXekW48BU",
        "_score": 1,
        "_source": {
          "client": {
            "ip": "fd00::1234"
          },
          "msg": "allowed ULA IPv6"
        }
      }
    ]
  }
}
```
