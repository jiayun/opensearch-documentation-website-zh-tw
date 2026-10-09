---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "取得索引對應"
parent: Index settings and mappings
grand_parent: Index APIs
nav_order: 20
---

# 取得索引對應 API
**於 1.0 版推出**
{: .label .label-purple }

Get Mappings API 會傳回一或多個索引的對應定義。您可以使用此 API 檢查索引中欄位的設定方式、確認對應更新是否已套用，或在重新編製索引之前檢閱完整的結構描述。

<!-- spec_insert_start
api: indices.get_mapping
component: endpoints
-->
## 端點
```json
GET /_mapping
GET /{index}/_mapping
```
<!-- spec_insert_end -->

## 路徑參數

下表列出可用的路徑參數。所有路徑參數皆為選用。

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `index` | 字串 | 以逗號分隔的索引名稱清單，用於取得其對應。支援萬用字元運算式。若要取得所有索引的對應，請省略此參數，或使用 `_all` 或 `*`。 |

## 查詢參數

下表列出可用的查詢參數。所有查詢參數皆為選用。

| 參數 | 資料類型 | 說明 | 預設值 |
| :--- | :--- | :--- | :--- |
| `allow_no_indices` | 布林值 | 指定是否忽略未符合任何索引的萬用字元。若為 `false`，當萬用字元未符合任何索引時，請求會傳回錯誤。 | `true` |
| `cluster_manager_timeout` | 字串 | 等待連線至叢集管理員節點的時間長度。 | `30s` |
| `expand_wildcards` | 字串 | 指定萬用字元運算式可展開的索引類型。支援以逗號分隔的值。有效值為：<br> - `all`：符合所有索引，包括隱藏索引。<br> - `open`：符合開啟的索引。<br> - `closed`：符合關閉的索引。<br> - `hidden`：符合隱藏索引。必須與 `open`、`closed` 或兩者合併使用。<br> - `none`：不接受萬用字元運算式。 | `open` |
| `ignore_unavailable` | 布林值 | 指定是否忽略缺少或關閉的索引。若為 `true`，回應中不會包含缺少或關閉的索引。 | `false` |
| `local` | 布林值 | 指定是否僅從本機節點擷取資訊，而非從叢集管理員節點擷取。 | `false` |

## 範例：取得單一索引的對應

下列範例會取得 `products` 索引的對應：

<!-- spec_insert_start
component: example_code
rest: GET /products/_mapping
-->
{% capture step1_rest %}
GET /products/_mapping
{% endcapture %}

{% capture step1_python %}


response = client.indices.get_mapping(
  index = "products"
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 範例：取得多個索引的對應

您可以在單一請求中指定以逗號分隔的清單，以取得多個索引的對應：

<!-- spec_insert_start
component: example_code
rest: GET /products,products-us/_mapping
-->
{% capture step1_rest %}
GET /products,products-us/_mapping
{% endcapture %}

{% capture step1_python %}


response = client.indices.get_mapping(
  index = "products,products-us"
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 範例：取得所有對應

若要取得叢集中所有索引的對應，請省略索引名稱：

<!-- spec_insert_start
component: example_code
rest: GET /_mapping
-->
{% capture step1_rest %}
GET /_mapping
{% endcapture %}

{% capture step1_python %}

response = client.indices.get_mapping()
{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 回應範例

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
        },
        "weight" : {
          "type" : "integer"
        }
      }
    }
  }
}
```
</details>

## 回應本文欄位

回應包含一個 JSON 物件，其中每個索引鍵都是索引名稱。下表說明每個索引項目內的欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `mappings` | 物件 | 索引的對應定義。 |
| `mappings.properties` | 物件 | 欄位名稱與其對應設定的對應表，包括類型、參數及巢狀子欄位。 |

## 必要權限

如果您使用 Security 外掛程式，請確定您具有適當的權限：`indices:admin/mappings/get`。
