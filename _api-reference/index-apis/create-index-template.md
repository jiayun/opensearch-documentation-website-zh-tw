---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "建立或更新索引範本"
parent: Index templates
grand_parent: Index APIs
nav_order: 10
---

# 建立或更新索引範本 API
**1.0 版推出**
{: .label .label-purple }

使用 Create or Update Index Template API 建立具有預先定義之對應與設定的索引，以及更新現有的索引範本。

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

支援下列選用查詢參數。

參數 | 資料類型 | 說明
:--- | :--- | :---
`create` | 布林值 | 若為 true，API 將無法取代或更新任何現有的索引範本。預設為 `false`。
`cause` | 字串 | 建立或更新索引範本的原因。預設為 `api`。
`cluster_manager_timeout` | 時間 | 等待與叢集管理員節點建立連線的時間長度。預設為 `30s`。

## 請求本文欄位

您可以在請求本文中使用下列選項來自訂索引範本。


參數 | 類型 | 說明
:--- | :--- | :---
`index_patterns` | 字串陣列 | 萬用字元運算式陣列，用於在建立資料串流和索引時比對其名稱。必要。
`composed_of` | 字串陣列 | 元件範本名稱的有序清單。這些範本會依指定的順序合併。如需詳細資訊，請參閱[使用多個元件範本](#using-multiple-component-templates)。選用。
`data_stream` | 物件 | 指定此物件後，索引範本會成為資料串流範本，並可使用該範本建立名稱相符的資料串流。資料串流的後端索引一律為隱藏狀態。此物件可包含 `timestamp_field` 物件，其 `name` 欄位用於指定資料串流的時間戳記欄位。`name` 的預設值為 `@timestamp`。選用。
`_meta` | 物件 | 提供索引範本詳細資訊的選用中繼資料。選用。
`priority` | Long | 決定在建立新索引或資料串流時，哪些索引範本優先採用的數值。OpenSearch 會選擇優先順序最高的範本。若未指定優先順序，範本會被指派為 `0`，表示最低優先順序。必須為 `0` 或更大的值。索引模式重疊的索引範本不能具有相同的優先順序。選用。
`template` | 物件 | 包含索引之 `aliases`、`mappings` 或 `settings` 的範本。如需詳細資訊，請參閱[範本](#template)。選用。
`version` | Long | 用於管理索引範本的版本號碼。OpenSearch 不會自動設定版本號碼。選用。
`context` | 物件 | （實驗性）`context` 參數提供可套用至索引、針對特定使用案例預先定義的範本。在範本宣告的所有設定與對應中，脈絡範本具有最高優先順序。需要將 `cluster.application_templates.enabled` 設定設為 `true`。此物件包含脈絡的 `name`（字串，必要）、脈絡範本 `version`（字串，預設為 `_latest`），以及選用的 `params`（物件）。如需詳細資訊，請參閱[索引脈絡]({{site.url}}{{site.baseurl}}/im-plugin/index-context/)。選用。

### 範本

您可以在請求本文的 `template` 選項中使用下列物件。

#### `aliases`

要與範本建立關聯的別名名稱，以此作為鍵。此選項支援多個別名。別名名稱可以包含 `{index}`，建立索引時會將其取代為該索引的名稱。

物件本文包含下列選用的別名參數。

參數 | 資料類型 | 說明
:--- | :--- | :---
`filter` | Query DSL 物件 | 用來限制別名可存取之文件數量的查詢。
`index_routing` | 字串 | 將編製索引作業路由至特定分片的值。指定此值時，會覆寫編製索引作業的 `routing` 值。
`is_hidden` | 布林值 | 若為 `true`，則會隱藏別名。預設為 `false`。別名的所有索引的此設定值都必須相符。
`is_write_index` | 布林值 | 若為 `true`，則該索引為別名的寫入索引。預設為 `false`。
`routing` | 字串 | 用來將索引與搜尋作業路由至特定分片的值。
`search_routing` | 字串 | 用來將搜尋作業路由至特定分片的值。指定此值時，此選項會覆寫搜尋作業的 `routing` 值。

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

下列範例請求使用 `_meta` 參數，將中繼資料新增至索引範本。所有中繼資料都會儲存在叢集狀態中：

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

透過 `composed_of` 欄位使用多個元件範本時，元件範本會依指定的順序合併。索引範本本身 `template` 物件中的設定、對應和別名會在元件範本之後合併，並覆寫元件範本的內容。建立索引請求中指定的設定則會覆寫上述兩者。

在下列範例中，符合 `my-index-*` 的索引在合併後有兩個主要分片。如果將 `composed_of` 陣列中的順序反轉，該索引就會只有一個主要分片。

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


對應定義以及 `dynamic_templates` 和 `meta` 等根層級選項會採用遞迴合併。這表示當較早的元件包含 `meta` 區塊時，新的 `meta` 項目會新增至索引中中繼資料的末端。任何包含既有鍵的項目都會被覆寫。

## 必要權限

如果您使用 Security 外掛程式，請確認您具有適當的權限：`indices:admin/index_template/put`。
