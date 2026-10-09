---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "建立或更新索引對應"
parent: Index settings and mappings
grand_parent: Index APIs
nav_order: 30
redirect_from:
  - /opensearch/rest-api/index-apis/put-mapping/
  - /opensearch/rest-api/index-apis/update-mapping/
  - /opensearch/rest-api/update-mapping/
---

# 建立或更新索引對應 API
**推出於 1.0**
{: .label .label-purple }

使用此 API 將新欄位加入現有索引，或修改現有欄位的搜尋設定。此操作可讓您在不從頭重新建立索引的情況下演進索引結構描述。

您無法使用此操作來變更已包含索引資料之欄位的對應或欄位類型。修改現有欄位的類型可能會使先前已編製索引的資料與新對應不相容。如果您需要變更現有欄位的類型，請建立具有所需對應的新索引，然後使用 [Reindex]({{site.url}}{{site.baseurl}}/api-reference/document-apis/reindex/) 操作將文件從原始索引複製過來。若要在重新編製索引期間避免停機，您可以使用[別名]({{site.url}}{{site.baseurl}}/opensearch/index-alias/)。如需更多資訊，請參閱[變更現有欄位的類型](#example-changing-the-type-of-an-existing-field)。

<!-- spec_insert_start
api: indices.put_mapping
component: endpoints
-->
## 端點
```json
POST /{index}/_mapping
PUT  /{index}/_mapping
```
<!-- spec_insert_end -->

## 路徑參數

下表列出可用的路徑參數。

| 參數 | 必要 | 資料類型 | 說明 |
| :--- | :--- | :--- | :--- |
| `index` | **必要** | String | 要更新的索引名稱。您可以指定單一索引名稱、以逗號分隔的索引名稱清單，或萬用字元運算式。若要更新所有索引的對應，請使用 `_all` 或 `*`。 |

## 查詢參數

下表列出可用的查詢參數。所有查詢參數皆為選用。

| 參數 | 資料類型 | 說明 | 預設 |
| :--- | :--- | :--- | :--- |
| `allow_no_indices` | Boolean | 指定是否忽略未符合任何索引的萬用字元。若為 `false`，當萬用字元未符合任何索引時，請求會傳回錯誤。 | `true` |
| `cluster_manager_timeout` | String | 等待與叢集管理員節點連線的時間長度。 | `30s` |
| `expand_wildcards` | String | 指定萬用字元運算式可展開的索引類型。支援以逗號分隔的值。有效值為：<br> - `all`：符合所有索引，包括隱藏索引。<br> - `open`：符合開啟的索引。<br> - `closed`：符合關閉的索引。<br> - `hidden`：符合隱藏索引。必須與 `open`、`closed` 或兩者合併使用。<br> - `none`：不接受萬用字元運算式。 | `open` |
| `ignore_unavailable` | Boolean | 指定是否忽略遺失或關閉的索引。若為 `true`，遺失或關閉的索引不會包含在回應中。 | `false` |
| `timeout` | String | 等待回應的時間長度。若在逾時前未收到回應，請求會失敗並傳回錯誤。 | `30s` |
| `write_index_only` | Boolean | 若為 `true`，對應只會套用至目標目前的寫入索引。 | `false` |

## 請求本文欄位

下表列出可用的請求本文欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `properties` | Object | 必要。定義索引對應的欄位及其類型。每個欄位可包含名稱、[欄位資料類型]({{site.url}}{{site.baseurl}}/field-types/index/) 及[對應參數]({{site.url}}{{site.baseurl}}/field-types/mapping-parameters/)。 |
| `dynamic` | String | 控制是否動態新增欄位。有效值為 `true` (自動新增欄位)、`false` (忽略新欄位) 及 `strict` (拒絕包含未對應欄位的請求)。預設為 `true`。 |

## 範例：將欄位新增至索引

建立或更新對應 API 需要現有的索引。下列範例將 `description` 和 `price` 欄位新增至 `products` 索引：

<!-- spec_insert_start
component: example_code
rest: PUT /products/_mapping
body: |
{
  "properties": {
    "description": {
      "type": "text"
    },
    "price": {
      "type": "float"
    }
  }
}
-->
{% capture step1_rest %}
PUT /products/_mapping
{
  "properties": {
    "description": {
      "type": "text"
    },
    "price": {
      "type": "float"
    }
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.indices.put_mapping(
  index = "products",
  body =   {
    "properties": {
      "description": {
        "type": "text"
      },
      "price": {
        "type": "float"
      }
    }
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

您可以使用 [Get Mappings API]({{site.url}}{{site.baseurl}}/api-reference/index-apis/get-mapping/) 來確認對應已套用：

```json
GET /products/_mapping
```

## 範例：更新多個索引

您可以藉由指定以逗號分隔的索引名稱清單，在單一請求中將對應更新套用至多個索引。下列範例將 `currency` 和 `tax_rate` 欄位新增至美國和歐盟地區目錄：

<!-- spec_insert_start
component: example_code
rest: PUT /products-us,products-eu/_mapping
body: |
{
  "properties": {
    "currency": {
      "type": "keyword"
    },
    "tax_rate": {
      "type": "float"
    }
  }
}
-->
{% capture step1_rest %}
PUT /products-us,products-eu/_mapping
{
  "properties": {
    "currency": {
      "type": "keyword"
    },
    "tax_rate": {
      "type": "float"
    }
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.indices.put_mapping(
  index = "products-us,products-eu",
  body =   {
    "properties": {
      "currency": {
        "type": "keyword"
      },
      "tax_rate": {
        "type": "float"
      }
    }
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 範例：將屬性新增至現有的物件欄位

您可以將新的內部欄位新增至現有的 [object]({{site.url}}{{site.baseurl}}/field-types/supported-field-types/object/) 欄位。假設 `products` 索引已有具備 `name` 欄位的 `manufacturer` 物件。下列範例將 `country` 關鍵字欄位新增至 `manufacturer` 物件：

<!-- spec_insert_start
component: example_code
rest: PUT /products/_mapping
body: |
{
  "properties": {
    "manufacturer": {
      "properties": {
        "country": {
          "type": "keyword"
        }
      }
    }
  }
}
-->
{% capture step1_rest %}
PUT /products/_mapping
{
  "properties": {
    "manufacturer": {
      "properties": {
        "country": {
          "type": "keyword"
        }
      }
    }
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.indices.put_mapping(
  index = "products",
  body =   {
    "properties": {
      "manufacturer": {
        "properties": {
          "country": {
            "type": "keyword"
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

您可以藉由擷取對應來確認巢狀結構：

```json
GET /products/_mapping
```

<details markdown="block">
  <summary>
    回應
  </summary>
  {: .text-delta}

```json
{
  "products" : {
    "mappings" : {
      "properties" : {
        "description" : {
          "type" : "text"
        },
        "manufacturer" : {
          "properties" : {
            "country" : {
              "type" : "keyword"
            },
            "name" : {
              "type" : "text"
            }
          }
        },
        "price" : {
          "type" : "float"
        },
        "product_name" : {
          "type" : "text"
        }
      }
    }
  }
}
```
</details>

## 範例：為現有欄位新增多欄位

[多欄位]({{site.url}}{{site.baseurl}}/mappings/mapping-parameters/fields/)可讓您以不同方式為同一個欄位編製索引。例如，用於全文搜尋的 `text` 欄位也可以有一個用於排序或彙總的 `keyword` 子欄位。下列範例新增一個 `product_name.keyword` 子欄位並將 `ignore_above` 設為 `256`，以便對產品名稱進行精確比對篩選與排序：

<!-- spec_insert_start
component: example_code
rest: PUT /products/_mapping
body: |
{
  "properties": {
    "product_name": {
      "type": "text",
      "fields": {
        "keyword": {
          "type": "keyword",
          "ignore_above": 256
        }
      }
    }
  }
}
-->
{% capture step1_rest %}
PUT /products/_mapping
{
  "properties": {
    "product_name": {
      "type": "text",
      "fields": {
        "keyword": {
          "type": "keyword",
          "ignore_above": 256
        }
      }
    }
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.indices.put_mapping(
  index = "products",
  body =   {
    "properties": {
      "product_name": {
        "type": "text",
        "fields": {
          "keyword": {
            "type": "keyword",
            "ignore_above": 256
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

您可以驗證多欄位組態：

```json
GET /products/_mapping
```

<details markdown="block">
  <summary>
    回應
  </summary>
  {: .text-delta}

```json
{
  "products" : {
    "mappings" : {
      "properties" : {
        "description" : {
          "type" : "text"
        },
        "manufacturer" : {
          "properties" : {
            "country" : {
              "type" : "keyword"
            },
            "name" : {
              "type" : "text"
            }
          }
        },
        "price" : {
          "type" : "float"
        },
        "product_name" : {
          "type" : "text",
          "fields" : {
            "keyword" : {
              "type" : "keyword",
              "ignore_above" : 256
            }
          }
        }
      }
    }
  }
}
```
</details>

## 範例：變更支援的對應參數

某些[對應參數]({{site.url}}{{site.baseurl}}/field-types/mapping-parameters/)可以使用 Create or Update Mappings API 為現有欄位更新。例如，您可以變更 keyword 欄位的 [`ignore_above`]({{site.url}}{{site.baseurl}}/field-types/mapping-parameters/ignore-above/) 值。下列範例將 `sku` 欄位的 `ignore_above` 從 `20` 提高到 `50`，以便為較長的產品代號編製索引：

<!-- spec_insert_start
component: example_code
rest: PUT /products/_mapping
body: |
{
  "properties": {
    "sku": {
      "type": "keyword",
      "ignore_above": 50
    }
  }
}
-->
{% capture step1_rest %}
PUT /products/_mapping
{
  "properties": {
    "sku": {
      "type": "keyword",
      "ignore_above": 50
    }
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.indices.put_mapping(
  index = "products",
  body =   {
    "properties": {
      "sku": {
        "type": "keyword",
        "ignore_above": 50
      }
    }
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

您可以確認更新後的參數值：

```json
GET /products/_mapping
```

<details markdown="block">
  <summary>
    回應
  </summary>
  {: .text-delta}

```json
{
  "products" : {
    "mappings" : {
      "properties" : {
        "description" : {
          "type" : "text"
        },
        "manufacturer" : {
          "properties" : {
            "country" : {
              "type" : "keyword"
            },
            "name" : {
              "type" : "text"
            }
          }
        },
        "price" : {
          "type" : "float"
        },
        "product_name" : {
          "type" : "text",
          "fields" : {
            "keyword" : {
              "type" : "keyword",
              "ignore_above" : 256
            }
          }
        },
        "sku" : {
          "type" : "keyword",
          "ignore_above" : 50
        }
      }
    }
  }
}
```
</details>

## 範例：使用別名重新命名欄位

由於重新命名欄位會導致先前儲存的資料無法以新名稱存取，請使用 [`alias`]({{site.url}}{{site.baseurl}}/field-types/supported-field-types/alias/) 欄位類型提供參照該欄位的替代方式。下列範例建立一個指向現有 `product_id` 欄位的 `item_id` 別名，讓查詢可以使用任一名稱：

<!-- spec_insert_start
component: example_code
rest: PUT /products/_mapping
body: |
{
  "properties": {
    "item_id": {
      "type": "alias",
      "path": "product_id"
    }
  }
}
-->
{% capture step1_rest %}
PUT /products/_mapping
{
  "properties": {
    "item_id": {
      "type": "alias",
      "path": "product_id"
    }
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.indices.put_mapping(
  index = "products",
  body =   {
    "properties": {
      "item_id": {
        "type": "alias",
        "path": "product_id"
      }
    }
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

您可以驗證別名是否已建立：

```json
GET /products/_mapping
```

<details markdown="block">
  <summary>
    回應
  </summary>
  {: .text-delta}

```json
{
  "products" : {
    "mappings" : {
      "properties" : {
        "description" : {
          "type" : "text"
        },
        "item_id" : {
          "type" : "alias",
          "path" : "product_id"
        },
        "manufacturer" : {
          "properties" : {
            "country" : {
              "type" : "keyword"
            },
            "name" : {
              "type" : "text"
            }
          }
        },
        "price" : {
          "type" : "float"
        },
        "product_id" : {
          "type" : "keyword"
        },
        "product_name" : {
          "type" : "text",
          "fields" : {
            "keyword" : {
              "type" : "keyword",
              "ignore_above" : 256
            }
          }
        },
        "sku" : {
          "type" : "keyword",
          "ignore_above" : 50
        }
      }
    }
  }
}
```
</details>

## 範例：變更現有欄位的類型

您無法直接變更已包含索引資料之欄位的欄位類型。請改為建立一個具有正確對應的新索引，並使用 [Reindex]({{site.url}}{{site.baseurl}}/api-reference/document-apis/reindex/) API 從原始索引複製文件。

下列範例將 `weight` 欄位從 `integer` 變更為 `float`，以便準確儲存小數值（例如 `0.75` kg）。

首先，以更新後的欄位類型建立新索引：

<!-- spec_insert_start
component: example_code
rest: PUT /products-v2
body: |
{
  "mappings": {
    "properties": {
      "product_name": {
        "type": "text",
        "fields": {
          "keyword": {
            "type": "keyword",
            "ignore_above": 256
          }
        }
      },
      "price": {
        "type": "float"
      },
      "weight": {
        "type": "float"
      }
    }
  }
}
-->
{% capture step1_rest %}
PUT /products-v2
{
  "mappings": {
    "properties": {
      "product_name": {
        "type": "text",
        "fields": {
          "keyword": {
            "type": "keyword",
            "ignore_above": 256
          }
        }
      },
      "price": {
        "type": "float"
      },
      "weight": {
        "type": "float"
      }
    }
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.indices.create(
  index = "products-v2",
  body =   {
    "mappings": {
      "properties": {
        "product_name": {
          "type": "text",
          "fields": {
            "keyword": {
              "type": "keyword",
              "ignore_above": 256
            }
          }
        },
        "price": {
          "type": "float"
        },
        "weight": {
          "type": "float"
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

接著將資料從原始索引重新編製索引到新索引：

<!-- spec_insert_start
component: example_code
rest: POST /_reindex
body: |
{
  "source": {
    "index": "products"
  },
  "dest": {
    "index": "products-v2"
  }
}
-->
{% capture step1_rest %}
POST /_reindex
{
  "source": {
    "index": "products"
  },
  "dest": {
    "index": "products-v2"
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.reindex(
  body =   {
    "source": {
      "index": "products"
    },
    "dest": {
      "index": "products-v2"
    }
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

<details markdown="block">
  <summary>
    回應
  </summary>
  {: .text-delta}

```json
{
  "took" : 8,
  "timed_out" : false,
  "total" : 2,
  "updated" : 0,
  "created" : 2,
  "deleted" : 0,
  "batches" : 1,
  "version_conflicts" : 0,
  "noops" : 0,
  "retries" : {
    "bulk" : 0,
    "search" : 0
  },
  "throttled_millis" : 0,
  "requests_per_second" : -1.0,
  "throttled_until_millis" : 0,
  "failures" : [ ]
}
```
</details>

## 範例回應

成功的對應更新會傳回下列回應：

```json
{
  "acknowledged": true
}
```

## 回應本文欄位

下表列出所有回應本文欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `acknowledged` | Boolean | 指出請求是否已由叢集中所有相關節點確認。 |

## 必要權限

如果您使用 Security 外掛程式，請確認您具有適當的權限：`indices:admin/mapping/put`。
