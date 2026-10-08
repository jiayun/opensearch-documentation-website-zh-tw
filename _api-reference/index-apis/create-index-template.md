---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "建立或更新索引範本"
parent: Index templates
grand_parent: Index APIs
nav_order: 10
---

# 建立或更新索引範本 API
**於 1.0 版推出**
{: .label .label-purple }

您可以使用 Create or Update Index Template API，以預先定義的對應與設定建立索引，以及更新現有的索引範本。

## 端點

```json
PUT _index_template/{template-name}
POST _index_template/{template-name}
```

## 路徑參數

參數 | 資料類型 | 說明
:--- | :--- | :---
`template-name` | 字串 | 索引範本的名稱。

## 查詢參數

支援下列選用的查詢參數。

參數 | 資料類型 | 說明
:--- | :--- | :---
`create` | 布林值 | 設為 true 時，API 無法取代或更新任何現有的索引範本。預設為 `false`。
`cluster_manager_timeout` | 時間 | 等待連線至叢集管理員節點的時間長度。預設為 `30s`。

## 請求本文欄位

您可以在請求本文中使用下列選項來自訂索引範本。


參數 | 類型 | 說明
:--- | :--- | :---
`index_patterns` | 字串陣列 | 萬用字元運算式的陣列，用於比對範本建立期間所建立的資料串流與索引名稱。必要。
`composed_of` | 字串陣列 | 元件範本名稱的有序清單。這些範本會依指定的順序合併。如需詳細資訊，請參閱[使用多個元件範本](#using-multiple-component-templates)。選用。
`data_stream` | 物件 | 使用此選項時，請求會根據範本建立資料串流與任何後備索引。此設定需要相符的索引範本。此選項也可搭配 `hidden` 設定使用；當該設定設為 `true` 時，會隱藏資料串流的後備索引。選用。
`_meta` | 物件 | 提供索引範本詳細資訊的選用中繼資料。選用。
`priority` | 整數 | 決定建立新索引或資料串流時，哪些索引範本優先套用的數字。OpenSearch 會選擇優先順序最高的範本。未指定優先順序時，範本會被指派 `0`，表示最低優先順序。選用。
`template` | 物件 | 包含索引的 `aliases`、`mappings` 或 `settings` 的範本。如需詳細資訊，請參閱 [#template]。選用。
`version` | 整數 | 用於管理索引範本的版本號碼。OpenSearch 不會自動設定版本號碼。選用。
`context` | 物件 | （實驗性）`context` 參數提供針對特定使用案例的預先定義範本，可套用至索引。在範本宣告的所有設定與對應中，情境範本具有最高優先順序。如需詳細資訊，請參閱[索引情境]({{site.url}}{{site.baseurl}}/im-plugin/index-context/)。

### 範本

您可以在請求本文的 `template` 選項中使用下列物件。

#### `alias`

與範本建立關聯的別名名稱，作為物件的鍵。當請求本文中包含 `template` 選項時，此項為必要。此選項支援多個別名。

物件本文包含下列選用的別名參數。

參數 | 資料類型 | 說明
:--- | :--- | :---
`filter` | Query DSL 物件 | 限制別名可存取的文件數量的查詢。
`index_routing` | 字串 | 將編製索引操作路由至特定分片的值。指定時，會覆寫編製索引操作的 `routing` 值。
`is_hidden` | 布林值 | 設為 `true` 時，別名會隱藏。預設為 `false`。所有別名索引的此設定值都必須相符。
`is_write_index` | 布林值 | 設為 `true` 時，此索引是別名的寫入索引。預設為 `false`。
`routing` | 字串 | 用於將編製索引與搜尋操作路由至特定分片的值。
`search_routing` | 字串 | 用於將特定搜尋操作路由至特定分片的值。指定時，此選項會覆寫搜尋操作的 `routing` 值。

#### `mappings`

索引中現有的欄位對應。如需詳細資訊，請參閱[對應與欄位類型]({{site.url}}{{site.baseurl}}/mappings/)。選用。

#### `settings`

索引的任何組態選項。如需詳細資訊，請參閱[索引設定]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/index-settings/)。

## 請求範例

下列範例示範如何使用 Create or Update Index Template API。

### 包含索引別名的索引範本

下列請求範例在範本中包含索引別名：

<!-- spec_insert_start
component: example_code
rest: PUT /_index_template/alias-template
body: |
{
  "index_patterns" : ["sh*"],
  "template": {
    "settings" : {
        "number_of_shards" : 1
    },
    "aliases" : {
        "alias1" : {},
        "alias2" : {
            "filter" : {
                "term" : {"user.id" : "hamlet" }
            },
            "routing" : "shard-1"
        },
        "{index}-alias" : {}
    }
  }
}
-->
{% capture step1_rest %}
PUT /_index_template/alias-template
{
  "index_patterns": [
    "sh*"
  ],
  "template": {
    "settings": {
      "number_of_shards": 1
    },
    "aliases": {
      "alias1": {},
      "alias2": {
        "filter": {
          "term": {
            "user.id": "hamlet"
          }
        },
        "routing": "shard-1"
      },
      "{index}-alias": {}
    }
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.indices.put_index_template(
  name = "alias-template",
  body =   {
    "index_patterns": [
      "sh*"
    ],
    "template": {
      "settings": {
        "number_of_shards": 1
      },
      "aliases": {
        "alias1": {},
        "alias2": {
          "filter": {
            "term": {
              "user.id": "hamlet"
            }
          },
          "routing": "shard-1"
        },
        "{index}-alias": {}
      }
    }
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

### 使用多個相符的範本

當多個索引範本與新索引或資料串流的名稱相符時，會使用優先順序最高的範本。例如，下列兩個請求會建立具有不同優先順序的索引範本。

第一個請求建立優先順序為 `0` 的範本，與以 `h` 開頭的索引名稱相符：

```json
PUT /_index_template/template_one
{
  "index_patterns" : ["h*"],
  "priority" : 0,
  "template": {
    "settings" : {
      "number_of_shards" : 1,
      "number_of_replicas": 0
    },
    "mappings" : {
      "_source" : { "enabled" : false }
    }
  }
}
```
{% include copy-curl.html %}

第二個請求建立優先順序為 `1` 的範本，與範圍較小、以 `ha` 開頭的索引名稱集合相符：

```json
PUT /_index_template/template_two
{
  "index_patterns" : ["ha*"],
  "priority" : 1,
  "template": {
    "settings" : {
      "number_of_shards" : 2
    },
    "mappings" : {
      "_source" : { "enabled" : true }
    }
  }
}
```
{% include copy-curl.html %}

對於以 `ha` 開頭的索引，會啟用 `_source`。由於只會套用 `template_two`，索引將有兩個主要分片與一個副本。

不允許為重疊的索引模式指定相同的優先順序。嘗試建立與現有索引範本相符且優先順序相同的範本時，會發生錯誤。
{: .note}

### 新增範本版本控制

下列範例請求會為索引範本新增 `version` 編號，可簡化外部系統的範本管理：

<!-- spec_insert_start
component: example_code
rest: PUT /_index_template/versioned-template
body: |
{
  "index_patterns" : ["mac", "cheese"],
  "priority" : 0,
  "template": {
    "settings" : {
        "number_of_shards" : 1
    }
  },
  "version": 1
}
-->
{% capture step1_rest %}
PUT /_index_template/versioned-template
{
  "index_patterns": [
    "mac",
    "cheese"
  ],
  "priority": 0,
  "template": {
    "settings": {
      "number_of_shards": 1
    }
  },
  "version": 1
}
{% endcapture %}

{% capture step1_python %}


response = client.indices.put_index_template(
  name = "versioned-template",
  body =   {
    "index_patterns": [
      "mac",
      "cheese"
    ],
    "priority": 0,
    "template": {
      "settings": {
        "number_of_shards": 1
      }
    },
    "version": 1
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->


### 新增範本中繼資料

下列範例請求使用 `meta` 參數為索引範本新增中繼資料。所有中繼資料都會儲存在叢集狀態中：

<!-- spec_insert_start
component: example_code
rest: PUT /_index_template/metadata-template
body: |
{
  "index_patterns": ["rom", "juliet"],
  "template": {
    "settings" : {
        "number_of_shards" : 2
    }
  },
  "_meta": {
    "description": "Where art thou",
    "serialization": {
      "class": "MyIndexTemplate",
      "id": 12
    }
  }
}
-->
{% capture step1_rest %}
PUT /_index_template/metadata-template
{
  "index_patterns": [
    "rom",
    "juliet"
  ],
  "template": {
    "settings": {
      "number_of_shards": 2
    }
  },
  "_meta": {
    "description": "Where art thou",
    "serialization": {
      "class": "MyIndexTemplate",
      "id": 12
    }
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.indices.put_index_template(
  name = "metadata-template",
  body =   {
    "index_patterns": [
      "rom",
      "juliet"
    ],
    "template": {
      "settings": {
        "number_of_shards": 2
      }
    },
    "_meta": {
      "description": "Where art thou",
      "serialization": {
        "class": "MyIndexTemplate",
        "id": 12
      }
    }
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

### 資料串流定義

加入 `data_stream` 物件，即可將索引範本用於資料串流，如下列範例請求所示：

<!-- spec_insert_start
component: example_code
rest: PUT /_index_template/logs-template
body: |
{
  "index_patterns": ["logs-*"],
  "data_stream": { }
}
-->
{% capture step1_rest %}
PUT /_index_template/logs-template
{
  "index_patterns": [
    "logs-*"
  ],
  "data_stream": {}
}
{% endcapture %}

{% capture step1_python %}


response = client.indices.put_index_template(
  name = "logs-template",
  body =   {
    "index_patterns": [
      "logs-*"
    ],
    "data_stream": {}
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 使用多個元件範本

當您搭配 `composed_of` 欄位使用多個元件範本時，系統會依指定的順序合併這些元件範本。接著，會合併來自該元件父索引範本的所有對應、設定與別名。最後，會合併新增至索引請求的任何組態選項。

在下列範例中，符合 `my-index-*` 的索引會有兩個合併後的主要分片。如果 `composed_of` 陣列中的順序相反，則該索引只會有一個主要分片。

首先，建立一個將主要分片數設為一個的元件範本：

```json
PUT /_component_template/template_with_1_shard
{
  "template": {
    "settings": {
      "index.number_of_shards": 1
    }
  }
}
```
{% include copy-curl.html %}

接著，建立一個將主要分片數設為兩個的元件範本：

```json
PUT /_component_template/template_with_2_shards
{
  "template": {
    "settings": {
      "index.number_of_shards": 2
    }
  }
}
```
{% include copy-curl.html %}

最後，建立一個依序組合這兩個元件範本的索引範本：

```json
PUT /_index_template/composed-template
{
  "index_patterns": ["my-index-*"],
  "composed_of": ["template_with_1_shard", "template_with_2_shards"]
}
```
{% include copy-curl.html %}


對應定義與根層級選項（例如 `dynamic_templates` 和 `meta`）會採用遞迴合併，這表示當較早的元件包含 `meta` 區塊時，新的 `meta` 項目會新增至索引中繼資料的結尾。任何包含既有索引鍵的項目都會被覆寫。

## 必要權限

如果您使用 Security 外掛程式，請確認您具有適當的權限：`indices:admin/index_template/put`。
