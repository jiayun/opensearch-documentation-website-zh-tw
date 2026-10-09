---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: getMetadata()
parent: Functions
grand_parent: Pipelines
nav_order: 15
---

<!-- vale off -->
# getMetadata() 函式
<!-- vale on -->

`getMetadata()` 函式接受一個字面字串引數，並查閱事件中繼資料中的特定索引鍵。

如果索引鍵包含 `/`，則函式會遞迴查閱中繼資料。傳入後，運算式會傳回對應索引鍵的值。

傳回的值可以是任何類型。例如，如果中繼資料包含 `{"key1": "value2", "key2": 10}`，則函式 `getMetadata("key1")` 會傳回 `value2`。函式 `getMetadata("key2")` 會傳回 `10`。

## 範例

下列管線會將請求衍生的值寫入事件中繼資料，然後在 OpenSearch 接收端中使用 `getMetadata()`，建構各租用戶的每日索引名稱與文件 ID：

```yaml
metadata-pass-demo:
  source:
    http:
      ssl: false

  processor:
    - add_entries:
        entries:
          # write to metadata
          - metadata_key: tenant        
            value_expression: /tenant
          - metadata_key: ingest_marker
            value: batch-001
    - add_entries:
        entries:
          - key: tenant_from_meta
            value_expression: getMetadata("tenant")

  sink:
    - opensearch:
        hosts: ["https://opensearch:9200"]
        insecure: true
        username: admin
        password: admin_password
        index_type: custom
        # Use metadata inside sink format strings
        index: demo-%{yyyy.MM.dd}-${getMetadata("tenant")}
        document_id: ${/id}-${getMetadata("tenant")}
```
{% include copy.html %}

您可以使用下列命令測試管線：

```bash
curl -sS -X POST "http://localhost:2021/log/ingest" \
  -H "Content-Type: application/json" \
  -d '[{"id":"1","tenant":"eu","message":"hello"}, {"id":"2","tenant":"us","message":"hi"}]'
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
        "_index": "demo-2025.10.22-eu",
        "_id": "1-eu",
        "_score": 1,
        "_source": {
          "id": "1",
          "tenant": "eu",
          "message": "hello",
          "tenant_from_meta": "eu"
        }
      },
      {
        "_index": "demo-2025.10.22-us",
        "_id": "2-us",
        "_score": 1,
        "_source": {
          "id": "2",
          "tenant": "us",
          "message": "hi",
          "tenant_from_meta": "us"
        }
      }
    ]
  }
}
```
