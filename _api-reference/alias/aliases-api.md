---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "管理別名"
parent: Alias APIs
grand_parent: Index APIs
nav_order: 50
redirect_from:
 - /api-reference/index-apis/alias/
---

# Manage Aliases API
**於 1.0 版導入**
{: .label .label-purple }

Manage aliases API 可在單一原子交易中執行多項索引別名操作。當您需要新增或移除多個別名、將別名從一個索引切換到另一個索引，或在管理別名的同時刪除索引時，請使用此 API。此 API 接受一個動作陣列，因此非常適合必須以原子方式執行的複雜別名操作。

此 API 與 [Create or update alias API]({{site.url}}{{site.baseurl}}/api-reference/alias/create-alias/) 不同，後者一次只操作一個別名，並使用不同的請求參數。針對涉及多個別名或索引的大量操作與原子交易，請使用 Manage aliases API。

如需索引別名的概念性資訊（包括使用案例與範例），請參閱[索引別名]({{site.url}}{{site.baseurl}}/im-plugin/index-alias/)。


## 端點

```json
POST _aliases
```

## 查詢參數

下表列出可用的查詢參數。所有查詢參數皆為選用。

參數 | 資料類型 | 說明
:--- | :--- | :---
`cluster_manager_timeout` | 時間 | 等待叢集管理員節點回應的時間量。預設為 `30s`。
`timeout` | 時間 | 等待叢集回應的時間量。預設為 `30s`。

## 請求本文欄位

下表列出可用的請求本文欄位。

欄位 | 資料類型 | 說明 | 必要
:--- | :--- | :--- | :---
`actions` | 陣列 | 您要對索引執行的動作集合。有效選項為：`add`、`remove` 與 `remove_index`。陣列中必須至少有一個動作。 | 是
`add` | 不適用 | 將別名新增至指定的索引。 | 否
`remove` | 不適用 | 從指定的索引移除別名。 | 否
`remove_index` | 不適用 | 刪除索引。 | 否
`index` | 字串 | 要與別名建立關聯的索引名稱。支援萬用字元運算式。 | 若您未在本文中提供 `indices` 欄位則為必要。
`indices` | 陣列 | 要與別名建立關聯的索引名稱陣列。 | 若您未在本文中提供 `index` 欄位則為必要。
`alias` | 字串 | 別名的名稱。 | 若您未在本文中提供 `aliases` 欄位則為必要。
`aliases` | 陣列 | 別名名稱陣列。 | 若您未在本文中提供 `alias` 欄位則為必要。
`filter` | 物件 | 與別名搭配使用的篩選器，使別名指向索引中經篩選的部分。 | 否
`is_hidden` | 布林值 | 指定別名是否應在包含萬用字元運算式的結果中隱藏 | 否
`must_exist` | 布林值 | 指定要移除的別名是否必須存在。 | 否
`is_write_index` | 布林值 | 指定索引是否應為寫入索引。一個別名一次只能有一個寫入索引。若寫入請求提交至連結多個索引的別名，OpenSearch 只會在寫入索引上執行該請求。**重要**：未為索引明確設定 `is_write_index: true` 且僅參照一個索引的別名，會讓該索引在參照另一個索引之前一直作為寫入索引。一旦參照另一個索引，就不會再有寫入索引，寫入作業將被拒絕。 | 否
`routing` | 字串 | 用於在特定操作中為分片指派自訂值。 | 否
`index_routing` | 字串 | 僅在索引操作中為分片指派自訂值。 | 否
`search_routing` | 字串 | 僅在搜尋操作中為分片指派自訂值。 | 否

## 範例：新增別名

下列請求會建立名為 `logs_current` 的別名，指向 `application_logs_2024` 索引：

<!-- spec_insert_start
component: example_code
rest: POST /_aliases
body: |
{
  "actions": [
    {
      "add": {
        "index": "application_logs_2024",
        "alias": "logs_current"
      }
    }
  ]
}
-->
{% capture step1_rest %}
POST /_aliases
{
  "actions": [
    {
      "add": {
        "index": "application_logs_2024",
        "alias": "logs_current"
      }
    }
  ]
}
{% endcapture %}

{% capture step1_python %}


response = client.indices.update_aliases(
  body =   {
    "actions": [
      {
        "add": {
          "index": "application_logs_2024",
          "alias": "logs_current"
        }
      }
    ]
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 範例：移除別名

下列請求會從 `application_logs_2024` 索引移除 `logs_current` 別名：

<!-- spec_insert_start
component: example_code
rest: POST /_aliases
body: |
{
  "actions": [
    {
      "remove": {
        "index": "application_logs_2024",
        "alias": "logs_current"
      }
    }
  ]
}
-->
{% capture step1_rest %}
POST /_aliases
{
  "actions": [
    {
      "remove": {
        "index": "application_logs_2024",
        "alias": "logs_current"
      }
    }
  ]
}
{% endcapture %}

{% capture step1_python %}


response = client.indices.update_aliases(
  body =   {
    "actions": [
      {
        "remove": {
          "index": "application_logs_2024",
          "alias": "logs_current"
        }
      }
    ]
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 範例：重新命名別名

您可以在同一請求中將別名從一個索引移除並新增至另一個索引，以原子方式重新命名別名。下列範例將 `primary_data` 別名從 `dataset_v1` 移至 `dataset_v2`：

```json
POST /_aliases
{
  "actions": [
    {
      "remove": {
        "index": "dataset_v1",
        "alias": "primary_data"
      }
    },
    {
      "add": {
        "index": "dataset_v2",
        "alias": "primary_data"
      }
    }
  ]
}
```
{% include copy-curl.html %}

別名操作是原子的，也就是說 `primary_data` 不會有任何時刻同時指向兩個索引或都不指向任何索引。
{: .important}

## 範例：將別名新增至多個索引

您可以使用多個 `add` 動作，將單一別名與多個索引建立關聯：

```json
POST /_aliases
{
  "actions": [
    {
      "add": {
        "index": "products_electronics",
        "alias": "all_products"
      }
    },
    {
      "add": {
        "index": "products_clothing",
        "alias": "all_products"
      }
    },
    {
      "add": {
        "index": "products_books",
        "alias": "all_products"
      }
    }
  ]
}
```
{% include copy-curl.html %}


<!-- vale off -->
## 範例：使用 indices 陣列
<!-- vale on -->

或者，您也可以使用 `indices` 陣列在單一動作中指定多個索引：

```json
POST /_aliases
{
  "actions": [
    {
      "add": {
        "indices": ["products_electronics", "products_clothing", "products_books"],
        "alias": "all_products"
      }
    }
  ]
}
```
{% include copy-curl.html %}

## 範例：使用萬用字元模式

您可以使用萬用字元模式來新增多個符合命名模式的索引。下列範例為所有以 `sales_2024` 開頭的索引建立別名：

```json
POST /_aliases
{
  "actions": [
    {
      "add": {
        "index": "sales_2024_*",
        "alias": "current_year_sales"
      }
    }
  ]
}
```
{% include copy-curl.html %}

這會建立一個時間點別名，其中包含建立當下所有符合該模式的索引。它不會自動包含之後建立且符合該模式的新索引。
{: .note}

除非您指定寫入索引，否則寫入指向多個索引的別名會產生錯誤。
{: .important}

## 範例：索引替換

您可以在不停機的情況下，以不可分割的方式將索引替換為新索引。這在重新編製索引作業中很實用：

```json
POST /_aliases
{
  "actions": [
    {
      "add": {
        "index": "customer_data_new",
        "alias": "customer_data"
      }
    },
    {
      "remove_index": {
        "index": "customer_data_old"
      }
    }
  ]
}
```
{% include copy-curl.html %}

此作業會在單一不可分割的作業中，將新索引加入別名並刪除舊索引。

## 範例：篩選別名

篩選別名可讓您套用查詢篩選條件，對索引內的資料進行區隔。如此一來，您就能建立聚焦的資料子集，並透過不同的別名名稱存取。首先，請確認您的索引已具備必要的欄位對應：

```json
PUT /user_activity
{
  "mappings": {
    "properties": {
      "user_type": {
        "type": "keyword"
      },
      "timestamp": {
        "type": "date"
      },
      "action": {
        "type": "keyword"
      }
    }
  }
}
```
{% include copy-curl.html %}

接著建立篩選別名以區隔您的資料：

```json
POST /_aliases
{
  "actions": [
    {
      "add": {
        "index": "user_activity",
        "alias": "premium_users",
        "filter": {
          "term": {
            "user_type": "premium"
          }
        }
      }
    },
    {
      "add": {
        "index": "user_activity",
        "alias": "recent_activity",
        "filter": {
          "range": {
            "timestamp": {
              "gte": "now-7d"
            }
          }
        }
      }
    }
  ]
}
```
{% include copy-curl.html %}

這些別名會自動將指定的篩選條件套用至所有搜尋、計數和依查詢刪除作業。

## 範例：基本路由

路由可讓您將作業導向特定分片，藉由減少需要查詢的分片數量來提升效能。

以下範例會建立具有路由值的別名：

```json
POST /_aliases
{
  "actions": [
    {
      "add": {
        "index": "customer_orders",
        "alias": "region_east_orders",
        "routing": "east"
      }
    }
  ]
}
```
{% include copy-curl.html %}

## 範例：為索引和搜尋作業分別設定路由

您可以為編製索引和搜尋指定不同的路由值：

```json
POST /_aliases
{
  "actions": [
    {
      "add": {
        "index": "user_sessions",
        "alias": "mobile_sessions",
        "index_routing": "mobile",
        "search_routing": "mobile,tablet"
      }
    }
  ]
}
```
{% include copy-curl.html %}

在此範例中，所有透過別名編製索引的文件都會送往「mobile」分片，但搜尋可以同時查詢「mobile」和「tablet」分片。

當您執行搜尋時若同時使用別名路由和 routing 參數，OpenSearch 會使用兩者值的交集。例如，若您搜尋 `GET /mobile_sessions/_search?routing=tablet,mobile`，則只會使用「mobile」路由值，因為它是別名路由（`mobile,tablet`）與搜尋參數（`tablet,mobile`）的交集。
{: .note}

## 範例：設定寫入索引

當別名指向多個索引時，您必須指定由哪個索引處理寫入作業。

```json
POST /_aliases
{
  "actions": [
    {
      "add": {
        "index": "logs_2024_01",
        "alias": "active_logs",
        "is_write_index": true
      }
    },
    {
      "add": {
        "index": "logs_2024_02",
        "alias": "active_logs",
        "is_write_index": false
      }
    }
  ]
}
```
{% include copy-curl.html %}

現在您可以寫入別名，所有寫入作業都會送往 `logs_2024_01`：

```json
POST /active_logs/_doc
{
  "timestamp": "2024-01-15T10:30:00",
  "level": "INFO",
  "message": "Application started successfully"
}
```
{% include copy-curl.html %}

## 範例：切換寫入索引

您可以以不可分割的方式切換作為寫入索引的索引：

```json
POST /_aliases
{
  "actions": [
    {
      "add": {
        "index": "logs_2024_01",
        "alias": "active_logs",
        "is_write_index": false
      }
    },
    {
      "add": {
        "index": "logs_2024_02",
        "alias": "active_logs",
        "is_write_index": true
      }
    }
  ]
}
```
{% include copy-curl.html %}

> 使用寫入索引時，請留意以下重要事項：
> - 一個別名同一時間只能有一個寫入索引。
> - 若別名指向多個索引但未指定寫入索引，寫入作業將遭到拒絕。
> - 對於指向單一索引的別名，該索引會自動作為寫入索引。
{: .important}

## 範例：使用 must_exist 參數

OpenSearch 為移除作業提供 `must_exist` 參數，用於控制移除不存在的別名時的錯誤處理方式：

```json
POST /_aliases
{
  "actions": [
    {
      "remove": {
        "index": "application_logs_2024",
        "alias": "logs_current",
        "must_exist": true
      }
    }
  ]
}
```
{% include copy-curl.html %}

- `must_exist: true` - 若別名不存在，則擲回錯誤
- `must_exist: false` - 即使別名不存在，也會無聲地成功
- `must_exist: null`（預設）- 只有在所有指定的別名都不存在時才擲回錯誤

## 範例回應

所有成功的別名作業都會傳回相同的回應格式：

```json
{
    "acknowledged": true
}
```

## 必要權限

若您使用 Security 外掛程式，請確認您具備適當的權限：`indices:admin/aliases/get`。

## 相關文件

如需有關索引別名的詳細資訊，請參閱[索引別名]({{site.url}}{{site.baseurl}}/im-plugin/index-alias/)。