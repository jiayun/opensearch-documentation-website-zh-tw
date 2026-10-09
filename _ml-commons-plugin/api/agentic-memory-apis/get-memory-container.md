---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "取得記憶容器"
parent: Agentic memory APIs
grand_parent: ML Commons APIs
nav_order: 20
---

# Get Memory Container API
**於 3.3 版推出**
{: .label .label-purple }


使用此 API 依 ID 擷取記憶容器。

## 端點

```json
GET /_plugins/_ml/memory_containers/{memory_container_id}
```

## 範例請求

```json
GET /_plugins/_ml/memory_containers/SdjmmpgBOh0h20Y9kWuN
```
{% include copy-curl.html %}

## 範例回應

```json
{
    "name": "Raw memory container",
    "description": "Store static conversations with semantic search",
    "owner": {
        "name": "admin",
        "backend_roles": [
            "admin"
        ],
        "roles": [
            "own_index",
            "all_access"
        ],
        "custom_attribute_names": [],
        "user_requested_tenant": "null",
        "user_requested_tenant_access": "WRITE"
    },
    "created_time": 1754943902286,
    "last_updated_time": 1754943902286,
    "memory_storage_config": {
        "memory_index_name": "ml-static-memory-sdjmmpgboh0h20y9kwun-admin",
        "semantic_storage_enabled": false
    }
}
```

## 回應本文欄位

如需回應欄位的說明，請參閱 [Create Memory Container API 請求欄位]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/agentic-memory-apis/create-memory-container#request-body-fields)。