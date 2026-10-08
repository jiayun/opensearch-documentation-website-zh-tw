---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "建立索引"
parent: Core index APIs
grand_parent: Index APIs
nav_order: 10
redirect_from:
  - /opensearch/rest-api/index-apis/create-index/
  - /opensearch/rest-api/create-index/
---

# Create Index API
**於 1.0 版推出**
{: .label .label-purple }

Create Index API 會在 OpenSearch 叢集中建立新的索引。

您可以使用 Create Index API 指定下列索引組態：

- 控制索引行為的索引設定，例如分片和副本的數量。
- 定義索引中所儲存文件之欄位資料類型和屬性的欄位對應。
- 提供查詢索引時所用替代名稱的索引別名。

<!-- spec_insert_start
api: indices.create
component: endpoints
-->
## 端點
```json
PUT /{index}
```
<!-- spec_insert_end -->

## 索引命名限制

OpenSearch 索引有下列命名限制：

- 所有字母都必須是小寫。
- 索引名稱不能以底線（`_`）或連字號（`-`）開頭。
- 索引名稱不能包含空格、逗號或下列字元：

  `:`、`"`、`*`、`+`、`/`、`\`、`|`、`?`、`#`、`>` 或 `<`

<!-- spec_insert_start
api: indices.create
component: path_parameters
-->
## 路徑參數

下表列出可用的路徑參數。

| 參數 | 必要 | 資料類型 | 說明 |
| :--- | :--- | :--- | :--- |
| `index` | **必要** | 字串 | 您要建立的索引名稱。 |

<!-- spec_insert_end -->

## 查詢參數

下表列出可用的查詢參數。所有查詢參數皆為選用。

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `cluster_manager_timeout` | 字串 | 等待連線至叢集管理員節點的時間長度。 |
| `timeout` | 字串 | 等待回應的時間長度。如果在逾時之前未收到回應，請求就會失敗並傳回錯誤。 |
| `wait_for_active_shards` | 整數、字串、NULL 或字串 | 繼續執行作業之前必須處於作用中狀態的分片複本數量。可設為 `all`，或不超過索引中分片總數（`number_of_replicas+1`）的任何正整數。<br> 有效值為：<br> - `all`：等待所有分片都處於作用中狀態。 |

## 請求本文欄位

您可以加入下列請求本文欄位來設定新索引。所有請求本文欄位皆為選用。

欄位 | 資料類型 | 說明
:--- | :--- | :---
`settings` | 物件 | 索引的索引層級設定。如需索引設定清單，請參閱[索引設定]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/index-settings/)。選用。
`settings.index.number_of_shards` | 整數 | 索引中的主要分片數量。預設為 `1`。選用。
`settings.index.number_of_replicas` | 整數 | 每個主要分片的副本分片數量。預設為 `1`。選用。
`settings.number_of_shards` | 整數 | 不使用 `index` 前綴來指定主要分片數量的簡化語法。選用。
`settings.number_of_replicas` | 整數 | 不使用 `index` 前綴來指定副本分片數量的簡化語法。選用。
`mappings` | 物件 | 索引中文件的欄位對應。定義每個欄位的資料類型和屬性。如需詳細資訊，請參閱[對應]({{site.url}}{{site.baseurl}}/field-types/)。選用。
`mappings.properties` | 物件 | 定義文件中的欄位及其資料類型。每個鍵都是欄位名稱，每個值都是欄位定義物件。選用。
`aliases` | 物件 | 索引的索引別名。每個鍵都是別名名稱，每個值都是別名定義物件。如需詳細資訊，請參閱[索引別名]({{site.url}}{{site.baseurl}}/im-plugin/index-alias/)。選用。

**注意**：您不必在 `settings` 區段內明確指定 `index` 區段，可以改用簡化語法。
{: .note}

## 範例：建立基本索引

您通常不需要明確建立空白索引。當您將文件編製索引至不存在的索引時，OpenSearch 會自動建立該索引。不過，如果您想在將資料編製索引之前設定特定的設定、對應或別名，明確建立索引就很有用。

下列範例請求會建立名為 `sample-index` 的索引，不含任何設定、對應或別名：

<!-- spec_insert_start
component: example_code
rest: PUT /sample-index
body: {}
-->
{% capture step1_rest %}
PUT /sample-index
{}
{% endcapture %}

{% capture step1_python %}


response = client.indices.create(
  index = "sample-index",
  body =   {}
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 範例：建立含設定的索引

下列範例請求會建立名為 `books` 的索引，並針對分片和副本數量指定特定設定：

<!-- spec_insert_start
component: example_code
rest: PUT /books
body: |
{
  "settings": {
    "index": {
      "number_of_shards": 2,
      "number_of_replicas": 1
    }
  }
}
-->
{% capture step1_rest %}
PUT /books
{
  "settings": {
    "index": {
      "number_of_shards": 2,
      "number_of_replicas": 1
    }
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.indices.create(
  index = "books",
  body =   {
    "settings": {
      "index": {
        "number_of_shards": 2,
        "number_of_replicas": 1
      }
    }
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 範例：建立含簡化設定的索引

下列範例請求會使用不含 `index` 前綴的簡化設定語法，建立名為 `books-simplified` 的索引：

<!-- spec_insert_start
component: example_code
rest: PUT /books-simplified
body: |
{
  "settings": {
    "number_of_shards": 2,
    "number_of_replicas": 1
  }
}
-->
{% capture step1_rest %}
PUT /books-simplified
{
  "settings": {
    "number_of_shards": 2,
    "number_of_replicas": 1
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.indices.create(
  index = "books-simplified",
  body =   {
    "settings": {
      "number_of_shards": 2,
      "number_of_replicas": 1
    }
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 範例：建立含對應的索引

下列範例請求會建立名為 `employees` 且含欄位對應的索引：

<!-- spec_insert_start
component: example_code
rest: PUT /employees
body: |
{
  "mappings": {
    "properties": {
      "name": {
        "type": "text"
      },
      "age": {
        "type": "integer"
      },
      "department": {
        "type": "keyword"
      }
    }
  }
}
-->
{% capture step1_rest %}
PUT /employees
{
  "mappings": {
    "properties": {
      "name": {
        "type": "text"
      },
      "age": {
        "type": "integer"
      },
      "department": {
        "type": "keyword"
      }
    }
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.indices.create(
  index = "employees",
  body =   {
    "mappings": {
      "properties": {
        "name": {
          "type": "text"
        },
        "age": {
          "type": "integer"
        },
        "department": {
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

## 範例：建立含有別名的索引

下列範例請求會建立名為 `orders` 的索引，並設定兩個別名，其中包含一個篩選別名：

<!-- spec_insert_start
component: example_code
rest: PUT /orders
body: |
{
  "aliases": {
    "current-orders": {},
    "recent-orders": {
      "filter": {
        "range": {
          "timestamp": {
            "gte": "now-7d"
          }
        }
      }
    }
  }
}
-->
{% capture step1_rest %}
PUT /orders
{
  "aliases": {
    "current-orders": {},
    "recent-orders": {
      "filter": {
        "range": {
          "timestamp": {
            "gte": "now-7d"
          }
        }
      }
    }
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.indices.create(
  index = "orders",
  body =   {
    "aliases": {
      "current-orders": {},
      "recent-orders": {
        "filter": {
          "range": {
            "timestamp": {
              "gte": "now-7d"
            }
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

建立索引請求成功時，OpenSearch 會傳回下列回應：

```json
{
  "acknowledged": true,
  "shards_acknowledged": true,
  "index": "books"
}
```

## 回應本文欄位

下表列出所有回應本文欄位。

欄位 | 資料類型 | 說明
:--- | :--- | :---
`acknowledged` | 布林值 | 表示是否已在叢集中成功建立索引。值為 `true` 表示已成功以新索引更新叢集狀態。值為 `false` 表示請求在叢集狀態更新前逾時，但索引很可能仍會建立。
`shards_acknowledged` | 布林值 | 表示 `wait_for_active_shards` 設定所指定數量的分片副本是否在作業逾時前變為作用中。值為 `true` 表示目標數量的分片副本已變為作用中。值為 `false` 表示作業在目標數量的分片副本變為作用中之前逾時，無論叢集狀態是否已成功更新（亦即 `acknowledged` 為 `true`）。
`index` | 字串 | 新建立索引的名稱。

## 等待作用中的分片

根據預設，建立索引作業只會在每個分片的主要副本皆已啟動，或請求逾時後，才將回應傳回給用戶端。您可以使用回應欄位來瞭解作業結果。

`acknowledged` 欄位表示是否已在叢集狀態中成功建立索引。`shards_acknowledged` 欄位表示目標數量的分片副本是否在逾時前變為作用中。若作業逾時，這兩個欄位都可能為 `false`，但索引仍可能建立成功。

若 `acknowledged` 為 `false`，表示叢集狀態更新已逾時，但索引很可能很快就會建立。若 `shards_acknowledged` 為 `false`，表示目標數量的分片副本未在逾時前變為作用中，無論叢集狀態是否已成功更新。

您可以使用下列其中一種方法，變更僅等待主要分片啟動的預設行為：

- 在建立索引時設定 `index.write.wait_for_active_shards` 索引設定。此設定也會影響後續寫入作業的 `wait_for_active_shards` 行為。
- 在建立索引請求中使用 `wait_for_active_shards` 查詢參數。

### 範例：使用 index.write.wait_for_active_shards 設定

下列範例請求會建立含有 `index.write.wait_for_active_shards` 設定的索引，此設定會等待兩個分片副本變為作用中後才傳回。此設定也會影響該索引後續的寫入作業：

<!-- spec_insert_start
component: example_code
rest: PUT /inventory
body: |
{
  "settings": {
    "index.write.wait_for_active_shards": "2",
    "number_of_shards": 1,
    "number_of_replicas": 1
  }
}
-->
{% capture step1_rest %}
PUT /inventory
{
  "settings": {
    "index.write.wait_for_active_shards": "2",
    "number_of_shards": 1,
    "number_of_replicas": 1
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.indices.create(
  index = "inventory",
  body =   {
    "settings": {
      "index.write.wait_for_active_shards": "2",
      "number_of_shards": 1,
      "number_of_replicas": 1
    }
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

### 範例：使用 wait_for_active_shards 查詢參數

下列範例請求會建立索引，並使用 `wait_for_active_shards` 查詢參數，等待兩個分片副本（主要分片與一個副本）變為作用中後才傳回：

<!-- spec_insert_start
component: example_code
rest: PUT /catalog?wait_for_active_shards=2
body: |
{
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 1
  }
}
-->
{% capture step1_rest %}
PUT /catalog?wait_for_active_shards=2
{
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 1
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.indices.create(
  index = "catalog",
  params = { "wait_for_active_shards": "2" },
  body =   {
    "settings": {
      "number_of_shards": 1,
      "number_of_replicas": 1
    }
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 必要權限

若您使用 Security 外掛程式，請確認您擁有適當的權限：`indices:admin/create`。
