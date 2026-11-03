---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "取得索引範本"
parent: Index templates
grand_parent: Index APIs
nav_order: 30
---

# Get Index Template API
**於 1.0 版推出**
{: .label .label-purple }

Get Index Template API 會傳回一或多個索引範本的資訊。

## 端點

```json
GET /_index_template
GET /_index_template/{template-name}
HEAD /_index_template/{template-name}
```

## 路徑參數

下表列出可用的路徑參數。所有路徑參數皆為選用。

參數 | 資料類型 | 說明
:--- | :--- | :---
`template-name` | 字串 | 要傳回的索引範本名稱。支援萬用字元運算式（`*`）。不支援以逗號分隔的名稱清單。若省略，則會傳回所有索引範本。

## 查詢參數

支援下列選用查詢參數。

參數 | 類型 | 說明
:--- | :--- | :---
`cluster_manager_timeout` | 時間 | 等待與叢集管理員節點建立連線的時間長度。預設為 `30s`。
`local` | 布林值 | 是否僅從本機節點傳回資訊，而不從叢集管理員節點傳回。預設為 `false`。

## 範例請求

下列請求會為名稱以 `hotels-` 開頭的索引建立名為 `hotels-template` 的索引範本：

```json
PUT /_index_template/hotels-template
{
  "index_patterns": ["hotels-*"],
  "priority": 50,
  "version": 1,
  "template": {
    "settings": {
      "number_of_shards": 1,
      "number_of_replicas": 1
    },
    "mappings": {
      "properties": {
        "name": { "type": "text" },
        "city": { "type": "keyword" },
        "rating": { "type": "float" }
      }
    },
    "aliases": {
      "hotels": {}
    }
  },
  "_meta": {
    "description": "Template for hotel listing indexes"
  }
}
```
{% include copy-curl.html %}

下列範例請求使用萬用字元運算式取得索引範本的資訊。如果沒有任何索引範本符合指定的名稱，API 會傳回 `404` 狀態碼：

<!-- spec_insert_start
component: example_code
rest: GET /_index_template/h*
-->
{% capture step1_rest %}
GET /_index_template/h*
{% endcapture %}

{% capture step1_python %}


response = client.indices.get_index_template(
  name = "h*"
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

下列範例請求會取得所有索引範本的資訊：

<!-- spec_insert_start
component: example_code
rest: GET /_index_template
-->
{% capture step1_rest %}
GET /_index_template
{% endcapture %}

{% capture step1_python %}

response = client.indices.get_index_template()
{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 回應範例

`GET /_index_template/h*` 請求會傳回下列回應：

```json
{
  "index_templates": [
    {
      "name": "hotels-template",
      "index_template": {
        "index_patterns": [
          "hotels-*"
        ],
        "template": {
          "settings": {
            "index": {
              "number_of_shards": "1",
              "number_of_replicas": "1"
            }
          },
          "mappings": {
            "properties": {
              "city": {
                "type": "keyword"
              },
              "name": {
                "type": "text"
              },
              "rating": {
                "type": "float"
              }
            }
          },
          "aliases": {
            "hotels": {}
          }
        },
        "composed_of": [],
        "priority": 50,
        "version": 1,
        "_meta": {
          "description": "Template for hotel listing indexes"
        }
      }
    }
  ]
}
```

## 回應本文欄位

下表列出所有回應本文欄位。

欄位 | 資料類型 | 說明
:--- | :--- | :---
`index_templates` | 物件陣列 | 符合請求的索引範本。陣列中的每個物件都包含 `name` 和 `index_template` 欄位。

`index_templates` 陣列中的每個物件都包含下列欄位。

欄位 | 資料類型 | 說明
:--- | :--- | :---
`name` | 字串 | 索引範本的名稱。
`index_template` | 物件 | 索引範本定義。

`index_template` 物件包含下列欄位。

欄位 | 資料類型 | 說明
:--- | :--- | :---
`index_patterns` | 字串陣列 | 範本所套用的索引名稱模式。
`template` | 物件 | 套用至符合索引的設定、對應和別名。包含 `settings`、`mappings` 和 `aliases` 物件。僅傳回範本中已定義的物件。僅在已設定時傳回。
`composed_of` | 字串陣列 | 用於組成此索引範本的元件範本名稱。在已設定或索引範本包含 `template` 物件時傳回。在後者的情況下，此值可能是空陣列。
`priority` | Long | 範本的優先順序。當多個範本符合同一個索引時，會套用優先順序最高的範本。僅在已設定時傳回。
`version` | Long | 範本的版本號碼。僅在已設定時傳回。
`_meta` | 物件 | 與範本一起儲存的自訂中繼資料。僅在已設定時傳回。
`data_stream` | 物件 | 資料串流組態，例如 `timestamp_field`。僅在範本會建立資料串流時傳回。
`context` | 物件 | 用於將額外設定套用至符合索引的情境。僅在已設定時傳回。

## 必要權限

如果您使用 Security 外掛程式，請確認您具備適當的權限：`indices:admin/index_template/get`。
