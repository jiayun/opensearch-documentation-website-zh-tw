---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "建立或更新別名"
parent: Alias APIs
grand_parent: Index APIs
nav_order: 10
redirect_from:
  - /api-reference/index-apis/update-alias/
---

# 建立或更新索引別名 API
**於 1.0 版推出**
{: .label .label-purple }

建立或更新別名 API 可將一或多個索引新增至索引別名，或更新現有別名的設定。如需索引別名的詳細資訊，請參閱[索引別名]({{site.url}}{{site.baseurl}}/im-plugin/index-alias/)。

建立或更新別名 API 與[管理別名 API]({{site.url}}{{site.baseurl}}/api-reference/alias/aliases-api/) 不同，後者支援新增和移除別名，以及移除索引及其別名。相較之下，下列 API 僅支援新增或更新別名，而不會更新索引本身。這兩個 API 使用的請求本文參數也不同。
{: .note}

## 端點

```json
POST /{target}/_alias/{alias-name}
PUT /{target}/_alias/{alias-name}
POST /_alias/{alias-name}
PUT /_alias/{alias-name}
POST /{target}/_aliases/{alias-name}
PUT /{target}/_aliases/{alias-name}
POST /_aliases/{alias-name}
PUT /_aliases/{alias-name}
PUT /{target}/_alias
PUT /{target}/_aliases
PUT /_alias
```

## 路徑參數

下表列出可用的路徑參數。所有路徑參數皆為選用。

| 參數 | 類型 | 說明 |
:--- | :--- | :---
| `target` | String | 以逗號分隔的索引清單。支援萬用字元運算式（`*`）。若要以叢集中的所有索引為目標，請使用 `_all` 或 `*`。選用。 |
| `alias-name` | String | 要建立或更新的別名名稱。選用。 |

## 查詢參數

下表列出可用的查詢參數。所有查詢參數皆為選用。

參數 | 類型 | 說明
:--- | :--- | :---
`cluster_manager_timeout` | Time | 等待叢集管理員節點回應的時間長度。預設為 `30s`。
`timeout` | Time | 等待叢集回應的時間長度。預設為 `30s`。

## 請求本文

下表列出可用的請求本文欄位。

欄位 | 類型 | 說明
:--- | :--- | :--- | :---
`index` | String | 以逗號分隔、要與別名建立關聯的索引清單。若設定此欄位，將會覆寫 URL 路徑中指定的索引名稱。
`alias` | String | 別名的名稱。若設定此欄位，將會覆寫 URL 路徑中指定的別名名稱。
`is_write_index` | Boolean | 指定索引是否應為寫入索引。一個別名同一時間只能有一個寫入索引。若將寫入請求提交至連結到多個索引的別名，OpenSearch 只會在寫入索引上執行該請求。
`routing` | String | 為特定作業指派自訂值給分片。
`index_routing` | String | 僅為索引作業指派自訂值給分片。
`search_routing` | String | 僅為搜尋作業指派自訂值給分片。
`filter` | Object | 搭配別名使用的篩選條件，讓別名指向索引中經篩選的部分。

## 範例請求：新增簡單別名

下列請求會為索引建立基本別名：

<!-- spec_insert_start
component: example_code
rest: PUT /products-2024/_alias/current-products
-->
{% capture step1_rest %}
PUT /products-2024/_alias/current-products
{% endcapture %}

{% capture step1_python %}


response = client.indices.put_alias(
  name = "current-products",
  index = "products-2024",
  body = { "Insert body here" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 範例請求：新增以時間為基礎的別名

下列請求會為 `sales-q1-2024` 索引建立別名 `quarterly-2024`：

<!-- spec_insert_start
component: example_code
rest: PUT /sales-q1-2024/_alias/quarterly-2024
-->
{% capture step1_rest %}
PUT /sales-q1-2024/_alias/quarterly-2024
{% endcapture %}

{% capture step1_python %}


response = client.indices.put_alias(
  name = "quarterly-2024",
  index = "sales-q1-2024",
  body = { "Insert body here" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 範例請求：新增具有路由的篩選別名

首先，建立具有適當對應的索引：

<!-- spec_insert_start
component: example_code
rest: PUT /customer-data
body: |
{
    "mappings" : {
        "properties" : {
            "customer_id" : {"type" : "integer"},
            "region" : {"type" : "keyword"}
        }
    }
}
-->
{% capture step1_rest %}
PUT /customer-data
{
  "mappings": {
    "properties": {
      "customer_id": {
        "type": "integer"
      },
      "region": {
        "type": "keyword"
      }
    }
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.indices.create(
  index = "customer-data",
  body =   {
    "mappings": {
      "properties": {
        "customer_id": {
          "type": "integer"
        },
        "region": {
          "type": "keyword"
        }
      }
    }
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

接著，為特定客戶新增具有路由與篩選功能的索引別名：

<!-- spec_insert_start
component: example_code
rest: PUT /customer-data/_alias/customer-123
body: |
{
    "routing" : "west",
    "filter" : {
        "term" : {
            "customer_id" : 123
        }
    }
}
-->
{% capture step1_rest %}
PUT /customer-data/_alias/customer-123
{
  "routing": "west",
  "filter": {
    "term": {
      "customer_id": 123
    }
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.indices.put_alias(
  name = "customer-123",
  index = "customer-data",
  body =   {
    "routing": "west",
    "filter": {
      "term": {
        "customer_id": 123
      }
    }
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 範例請求：在建立索引時新增別名

您可以在使用建立索引 API 建立索引時新增別名：

<!-- spec_insert_start
component: example_code
rest: PUT /inventory-2024
body: |
{
    "mappings" : {
        "properties" : {
            "category" : {"type" : "keyword"}
        }
    },
    "aliases" : {
        "current-inventory" : {},
        "electronics" : {
            "filter" : {
                "term" : {"category" : "electronics" }
            }
        }
    }
}
-->
{% capture step1_rest %}
PUT /inventory-2024
{
  "mappings": {
    "properties": {
      "category": {
        "type": "keyword"
      }
    }
  },
  "aliases": {
    "current-inventory": {},
    "electronics": {
      "filter": {
        "term": {
          "category": "electronics"
        }
      }
    }
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.indices.create(
  index = "inventory-2024",
  body =   {
    "mappings": {
      "properties": {
        "category": {
          "type": "keyword"
        }
      }
    },
    "aliases": {
      "current-inventory": {},
      "electronics": {
        "filter": {
          "term": {
            "category": "electronics"
          }
        }
      }
    }
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 範例回應

```json
{
    "acknowledged": true
}
```

## 必要權限

如果您使用 Security 外掛程式，請確認您具備適當的權限：`indices:admin/aliases`。

## 相關文件

如需索引別名的詳細資訊，請參閱[索引別名]({{site.url}}{{site.baseurl}}/im-plugin/index-alias/)。
