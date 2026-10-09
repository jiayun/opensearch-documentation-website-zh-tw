---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: substringAfterLast()
parent: Functions
grand_parent: Pipelines
nav_order: 70
---

<!-- vale off -->
# substringAfterLast() 函式
<!-- vale on -->

`substringAfterLast()` 函式用於擷取字串中最後一次出現指定分隔符之後的部分。它接受兩個引數：

1. 第一個引數是常值字串，或是代表來源字串的 JSON pointer。

1. 第二個引數是要在第一個引數中搜尋的分隔符字串。

如果找到分隔符，函式會傳回字串中最後一次出現分隔符之後的部分。如果找不到分隔符，則傳回原始字串。如果來源解析為 `null`，函式會傳回 `null`。如果分隔符為 `null` 或空字串，則傳回原始字串。

例如，若要從包含檔案路徑的 `/filepath` 欄位中擷取副檔名，請如下使用 `substringAfterLast()` 函式：

```
'substringAfterLast(/filepath, ".")'
```
{% include copy.html %}

如果 `/filepath` 欄位包含 `archive.tar.gz`，函式會傳回 `gz`。

您也可以使用常值字串作為第一個引數：

```
'substringAfterLast("one-two-three", "-")'
```
{% include copy.html %}

函式會傳回 `three`，因為它擷取了最後一個 `-` 字元之後的字串部分。

`substringAfterLast()` 函式執行區分大小寫的搜尋。
{: .note}

## 範例

下列管線使用 `substringAfterLast()` 函式從完整檔案路徑中擷取檔案名稱，並將擷取到的檔案名稱新增為名為 `filename` 的新欄位：

```yaml
substring-after-last-demo:
  source:
    http:
      ssl: false

  processor:
    - add_entries:
        entries:
          - key: filename
            value_expression: 'substringAfterLast(/filepath, "/")'

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
          "filename": "syslog"
        }
      },
      {
        "_index": "demo-index-2026.03.13",
        "_id": "def456",
        "_score": 1,
        "_source": {
          "filepath": "/home/user/docs/report.pdf",
          "filename": "report.pdf"
        }
      }
    ]
  }
}
```
