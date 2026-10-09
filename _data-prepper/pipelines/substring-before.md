---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: substringBefore()
parent: Functions
grand_parent: Pipelines
nav_order: 80
---

<!-- vale off -->
# substringBefore() 函式
<!-- vale on -->

`substringBefore()` 函式用於擷取字串中第一個出現的指定分隔符號之前的部分。它接受兩個引數：

1. 第一個引數是常值字串或代表來源字串的 JSON 指標。

1. 第二個引數是要在第一個引數中搜尋的分隔符號字串。

如果找到分隔符號，函式會傳回字串中第一個出現的分隔符號之前的部分。如果找不到分隔符號，則傳回原始字串。如果來源解析為 `null`，函式會傳回 `null`。如果分隔符號為 `null` 或空字串，則傳回原始字串。

例如，若要從電子郵件地址欄位擷取使用者名稱，請使用 `substringBefore()` 函式，如下所示：

```
'substringBefore(/email, "@")'
```
{% include copy.html %}

如果 `/email` 欄位包含 `user@example.com`，函式會傳回 `user`。

或者，您可以使用常值字串作為第一個引數：

```
'substringBefore("hello-world-foo", "-")'
```
{% include copy.html %}

函式會傳回 `hello`，因為它擷取字串中第一個 `-` 字元之前的部分。

`substringBefore()` 函式會執行區分大小寫的搜尋。
{: .note}

## 範例

下列管線使用 `substringBefore()` 函式從 URL 欄位擷取 URL 通訊協定。它會將擷取出的通訊協定新增為名為 `protocol` 的新欄位：

```yaml
substring-before-demo:
  source:
    http:
      ssl: false

  processor:
    - add_entries:
        entries:
          - key: protocol
            value_expression: 'substringBefore(/url, "://")'

  sink:
    - opensearch:
        hosts: ["https://opensearch:9200"]
        insecure: true
        username: admin
        password: admin_password
        index_type: custom
        index: demo-index-%{yyyy.MM.dd}
```
{% include copy.html %}

您可以使用下列命令測試管線：

```bash
curl -sS -X POST "http://localhost:2021/log/ingest" \
  -H "Content-Type: application/json" \
  -d '[
        {"url":"https://opensearch.org/docs"},
        {"url":"http://example.com/page"}
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
        "_index": "demo-index-2026.03.13",
        "_id": "abc123",
        "_score": 1,
        "_source": {
          "url": "https://opensearch.org/docs",
          "protocol": "https"
        }
      },
      {
        "_index": "demo-index-2026.03.13",
        "_id": "def456",
        "_score": 1,
        "_source": {
          "url": "http://example.com/page",
          "protocol": "http"
        }
      }
    ]
  }
}
```
