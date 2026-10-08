---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "取得別名"
parent: Alias APIs
grand_parent: Index APIs
nav_order: 20
---

# 取得索引別名 API
**於 1.0 版推出**
{: .label .label-purple }

傳回一個或多個別名的相關資訊。

## 端點

```json
GET /_alias
GET /_alias/{alias}
GET /{index}/_alias/{alias}
```

## 路徑參數

下表列出可用的路徑參數。所有路徑參數皆為選用。

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `<alias>` | String | 以逗號分隔的別名清單或萬用字元運算式，用於指定要擷取的別名。如要擷取所有索引別名的資訊，請使用 `_all` 或 `*`。 |
| `<index>` | String | 以逗號分隔的索引名稱清單或萬用字元運算式，用於限制請求範圍。 |

## 查詢參數

下表列出可用的查詢參數。所有查詢參數皆為選用。

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `allow_no_indices` | Boolean | 是否忽略不符合任何索引的萬用字元。預設為 `true`。 |
| `expand_wildcards` | String | 萬用字元運算式可符合的索引類型。支援以逗號分隔的值。有效值為 `all`、`open`、`closed`、`hidden` 及 `none`。預設為 `all`。 |
| `ignore_unavailable` | Boolean | 是否忽略無法使用的索引。預設為 `false`。 |
| `local` | Boolean | 是否僅從本機節點傳回資訊，而非從叢集管理員節點傳回。預設為 `false`。 |

## 範例請求：取得索引的所有別名

您可以在建立索引時，使用建立索引 API 請求來新增索引別名。

下列建立索引 API 請求會建立 `logs_20302801` 索引，並包含兩個別名：

- `current_day`
- `2030`，僅傳回 `logs_20302801` 索引中 `year` 欄位值為 `2030` 的文件

<!-- spec_insert_start
component: example_code
rest: PUT /logs_20302801
body: |
{
  "aliases" : {
    "current_day" : {},
    "2030" : {
      "filter" : {
          "term" : {"year" : 2030 }
      }
    }
  }
}
-->
{% capture step1_rest %}
PUT /logs_20302801
{
  "aliases": {
    "current_day": {},
    "2030": {
      "filter": {
        "term": {
          "year": 2030
        }
      }
    }
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.indices.create(
  index = "logs_20302801",
  body =   {
    "aliases": {
      "current_day": {},
      "2030": {
        "filter": {
          "term": {
            "year": 2030
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

下列取得索引別名 API 請求會傳回索引 `logs_20302801` 的所有別名：

<!-- spec_insert_start
component: example_code
rest: GET /logs_20302801/_alias/*
-->
{% capture step1_rest %}
GET /logs_20302801/_alias/*
{% endcapture %}

{% capture step1_python %}


response = client.indices.get_alias(
  name = "*",
  index = "logs_20302801"
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 範例請求：取得特定別名

下列索引別名 API 請求會傳回 `2030` 別名：

<!-- spec_insert_start
component: example_code
rest: GET /_alias/2030
-->
{% capture step1_rest %}
GET /_alias/2030
{% endcapture %}

{% capture step1_python %}


response = client.indices.get_alias(
  name = "2030"
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 範例請求：根據萬用字元取得別名

下列索引別名 API 請求會傳回任何以 `20` 開頭的別名：

<!-- spec_insert_start
component: example_code
rest: GET /_alias/20*
-->
{% capture step1_rest %}
GET /_alias/20*
{% endcapture %}

{% capture step1_python %}


response = client.indices.get_alias(
  name = "20*"
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 範例回應

```json
{
 "logs_20302801" : {
   "aliases" : {
    "current_day" : {
    },
     "2030" : {
       "filter" : {
         "term" : {
           "year" : 2030
         }
       }
     }
   }
 }
}
```

## 回應本文欄位

下表列出所有回應本文欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `<index>` | Object | 包含索引的別名。 |
| `<index>.aliases` | Object | 包含索引的別名資訊。 |
| `<index>.aliases.<alias>` | Object | 包含別名的組態。 |
| `<index>.aliases.<alias>.filter` | Object | 用於限制別名可存取之文件的查詢。 |
| `<index>.aliases.<alias>.index_routing` | String | 用於編製索引作業的路由值。 |
| `<index>.aliases.<alias>.search_routing` | String | 用於搜尋作業的路由值。 |
| `<index>.aliases.<alias>.is_write_index` | Boolean | 索引是否為別名的寫入索引。 |

## 必要權限

如果您使用 Security 外掛程式，請確認您具有適當的權限：`indices:admin/aliases/get`。

## 相關文件

如需索引別名的更多資訊，請參閱[索引別名]({{site.url}}{{site.baseurl}}/im-plugin/index-alias/)。