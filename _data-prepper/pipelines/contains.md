---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: contains()
parent: Functions
grand_parent: Pipelines
nav_order: 10
---

<!-- vale off -->
# contains() 函式
<!-- vale on -->

`contains()` 函式用於檢查某個子字串是否存在於給定字串或事件中某個欄位的值內。它接受兩個引數：

- 第一個引數是常值字串，或是代表要搜尋之欄位或值的 JSON pointer。

- 第二個引數是要在第一個引數中搜尋的子字串。
如果第二個引數所指定的子字串存在於第一個引數所代表的字串或欄位值中，函式會傳回 `true`；如果不存在，則傳回 `false`。

例如，如果您想檢查字串 `"abcd"` 是否包含在名為 `message` 的欄位值中，您可以如下使用 `contains()` 函式：

```
'contains(/message, "abcd")'
```
{% include copy.html %}

如果欄位 `message` 包含子字串 `abcd`，此呼叫會傳回 `true`；如果不包含，則傳回 `false`。

或者，您也可以使用常值字串作為第一個引數：

```
'contains("This is a test message", "test")'
```
{% include copy.html %}

在此情況下，函式會傳回 `true`，因為子字串 `test` 存在於字串 `This is a test message` 中。

`contains()` 函式會執行區分大小寫的搜尋。
{: .note}

## 範例

下列管線使用 `contains()` 函式，根據 `/message` 中的子字串新增布林值旗標 `has_test`，並篩除不符合的事件，僅將包含字串 `ERROR` 的訊息轉送至 OpenSearch：

```yaml
contains-demo-pipeline:
  source:
    http:
      ssl: false

  processor:
    - add_entries:
        entries:
          - key: has_test
            value_expression: contains(/message, "test")
    - drop_events:
        drop_when: not contains(/message, "ERROR")

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
        {"message":"ok hello"},                  
        {"message":"this has test but ok"},
        {"message":"ERROR: something bad"}, 
        {"message":"ERROR: unit test failed"} 
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
        "_index": "demo-index-2025.10.21",
        "_id": "5YACB5oBqZitdAAb4n3r",
        "_score": 1,
        "_source": {
          "message": "ERROR: something bad",
          "has_test": false
        }
      },
      {
        "_index": "demo-index-2025.10.21",
        "_id": "5oACB5oBqZitdAAb4n3r",
        "_score": 1,
        "_source": {
          "message": "ERROR: unit test failed",
          "has_test": true
        }
      }
    ]
  }
}
```
