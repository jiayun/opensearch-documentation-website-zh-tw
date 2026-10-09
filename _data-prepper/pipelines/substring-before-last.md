---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: substringBeforeLast()
parent: Functions
grand_parent: Pipelines
nav_order: 90
---

<!-- vale off -->
# substringBeforeLast() 函式
<!-- vale on -->

`substringBeforeLast()` 函式用來擷取字串中最後一次出現指定分隔符之前的部分。它接受兩個引數：

1. 第一個引數是常值字串，或是代表來源字串的 JSON 指標。

1. 第二個引數是要在第一個引數中搜尋的分隔符字串。

如果找到分隔符，函式會傳回字串中最後一次出現分隔符之前的部分。如果找不到分隔符，則傳回原始字串。如果來源解析為 `null`，函式會傳回 `null`。如果分隔符為 `null` 或空字串，則傳回原始字串。

例如，若要從檔名欄位移除副檔名，請如下使用 `substringBeforeLast()` 函式：

```
'substringBeforeLast(/filename, ".")'
```
{% include copy.html %}

如果 `/filename` 欄位包含 `archive.tar.gz`，函式會傳回 `archive.tar`。

您也可以使用常值字串作為第一個引數：

```
'substringBeforeLast("one-two-three", "-")'
```
{% include copy.html %}

函式會傳回 `one-two`，因為它擷取了字串中最後一個 `-` 字元之前的部分。

`substringBeforeLast()` 函式執行區分大小寫的搜尋。
{: .note}

## 範例

下列管線使用 `substringBeforeLast()` 函式從完整檔案路徑中擷取目錄路徑，並將擷取到的目錄路徑新增為名為 `directory` 的新欄位：

```yaml
substring-before-last-demo:
  source:
    http:
      ssl: false

  processor:
    - add_entries:
        entries:
          - key: directory
            value_expression: 'substringBeforeLast(/filepath, "/")'

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

您可以使用下列命令測試此管線：

```bash
curl -sS -X POST "http://localhost:2021/log/ingest" \
  -H "Content-Type: application/json" \
  -d '[
        {"filepath":"/var/log/syslog"},
        {"filepath":"/home/user/docs/report.pdf"}
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
          "filepath": "/var/log/syslog",
          "directory": "/var/log"
        }
      },
      {
        "_index": "demo-index-2026.03.13",
        "_id": "def456",
        "_score": 1,
        "_source": {
          "filepath": "/home/user/docs/report.pdf",
          "directory": "/home/user/docs"
        }
      }
    ]
  }
}
```
