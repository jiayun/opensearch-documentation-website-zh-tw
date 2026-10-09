---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: substringAfter()
parent: Functions
grand_parent: Pipelines
nav_order: 60
---

<!-- vale off -->
# substringAfter() 函式
<!-- vale on -->

`substringAfter()` 函式用於擷取字串中第一個出現的指定分隔符號之後的部分。它接受兩個引數：

1. 第一個引數是常值字串，或代表來源字串的 JSON 指標。

1. 第二個引數是要在第一個引數中搜尋的分隔符號字串。

如果找到分隔符號，函式會傳回分隔符號第一次出現之後的字串部分。如果找不到分隔符號，則傳回原始字串。如果來源解析為 `null`，函式會傳回 `null`。如果分隔符號為 `null` 或空字串，則傳回原始字串。

例如，若要擷取名為 `header` 的欄位中第一個出現的 `=` 字元之後的值，請使用 `substringAfter()` 函式，如下所示：

```
'substringAfter(/header, "=")'
```
{% include copy.html %}

如果 `/header` 包含 `Content-Type=application/json`，函式會傳回 `application/json`。

或者，您可以使用常值字串作為第一個引數：

```
'substringAfter("hello-world-foo", "-")'
```
{% include copy.html %}

函式會傳回 `world-foo`，因為它擷取第一個 `-` 字元之後的字串部分。

`substringAfter()` 函式執行區分大小寫的搜尋。
{: .note}

## 範例

下列管線使用 `substringAfter()` 函式從電子郵件地址欄位擷取網域名稱。它會將擷取到的網域名稱新增為名為 `domain` 的新欄位：

```yaml
substring-after-demo:
  source:
    http:
      ssl: false

  processor:
    - add_entries:
        entries:
          - key: domain
            value_expression: 'substringAfter(/email, "@")'

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
        {"email":"user@example.com"},
        {"email":"admin@opensearch.org"}
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
          "email": "user@example.com",
          "domain": "example.com"
        }
      },
      {
        "_index": "demo-index-2026.03.13",
        "_id": "def456",
        "_score": 1,
        "_source": {
          "email": "admin@opensearch.org",
          "domain": "opensearch.org"
        }
      }
    ]
  }
}
```
