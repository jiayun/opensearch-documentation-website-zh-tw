---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "元件範本 API"
parent: Index templates
grand_parent: Index APIs
nav_order: 60
---

# 元件範本 API
**於 1.0 版推出**
{: .label .label-purple }

您可以使用元件範本 API 來建立、擷取、更新及刪除元件範本。元件範本是可重複使用的建構區塊，可定義設定、對應與別名，並可供多個索引範本共用。 

索引範本可使用多個元件範本建構。若要將元件範本納入索引範本，您需要將其列在索引範本的 `composed_of` 區段中。元件範本僅會套用至新建立且符合索引範本所指定條件的資料串流與索引。

如果在索引範本或索引建立請求中直接定義任何設定或對應，這些設定會優先於元件範本中指定的設定或對應。

元件範本僅用於建立索引的過程。對於資料串流，這包括建立資料串流本身，以及建立支援該串流的後端索引。修改元件範本不會影響現有索引，包括資料串流的後端索引。

## 端點

```json
PUT _component_template/{component-template-name}
GET _component_template/{component-template-name}
DELETE _component_template/{component-template-name}
HEAD _component_template/{component-template-name}
```

- `PUT`：建立或更新元件範本。接受查詢參數與請求本文。
- `GET`：擷取現有元件範本的資訊。僅接受查詢參數。
- `DELETE`：刪除現有元件範本。僅接受查詢參數。
- `HEAD`：傳回元件範本是否存在。僅傳回 HTTP 狀態碼。

## 路徑參數

下表列出可用的路徑參數。

參數 | 資料類型 | 說明
:--- | :--- | :---
`component-template-name` | 字串 | 元件範本的名稱。PUT、HEAD 及 DELETE 作業的必要參數。GET 作業的選用參數。

## 查詢參數

下表列出可用的查詢參數。所有查詢參數皆為選用。

參數 | 資料類型 | 說明 | 支援的作業
:--- | :--- | :--- | :---
`create` | 布林值 | 為 true 時，API 無法取代或更新任何現有的元件範本。預設為 `false`。 | PUT
`cluster_manager_timeout` | 時間 | 等待連線至叢集管理員節點的時間。預設為 `30s`。 | PUT, GET, DELETE

## 建立或更新元件範本

使用 PUT 作業來建立新的元件範本或更新現有的元件範本。

### 端點

```json
PUT _component_template/{component-template-name}
```

### 請求本文欄位

下表列出可用的請求本文欄位。


參數 | 資料類型 | 說明
:--- | :--- | :---
`template` | 物件 | 包含索引的 `aliases`、`mappings` 或 `settings` 的範本。如需詳細資訊，請參閱 [#template]。必要。
`version` | 整數 | 用於管理索引範本的版本號碼。OpenSearch 不會自動設定版本號碼。選用。
`_meta` | 物件 | 提供索引範本詳細資訊的中繼資料。選用。
`allow_auto_create` | 布林值 | 為 `true` 時，即使停用 `actions.auto_create_index`，仍可使用此範本自動建立索引。為 `false` 時，無法自動建立符合此範本的索引與資料串流。選用。
`deprecated` | 布林值 | 為 `true` 時，元件範本已棄用。若已棄用，OpenSearch 會在每次參照此範本時輸出警告。


### 範本

您可以在請求本文中搭配 `template` 選項使用下列物件。

#### `alias`

以要與範本關聯的別名名稱作為鍵。當請求本文中存在 `template` 選項時，此項為必要。此選項支援多個別名。

物件本文包含下列選用的別名參數。

參數 | 資料類型 | 說明
:--- | :--- | :---
`filter` | Query DSL 物件 | 限制別名可存取之文件數量的查詢。
`index_routing` | 字串 | 將編製索引作業路由至特定分片的值。指定時，會覆寫編製索引作業的 `routing` 值。
`is_hidden` | 布林值 | 為 `true` 時，別名會隱藏。預設為 false。此別名的所有索引都必須具有相同的設定值。
`is_write_index` | 布林值 | 為 `true` 時，此索引是該別名的寫入索引。預設為 `false`。
`routing` | 字串 | 用於將編製索引與搜尋作業路由至特定分片的值。
`search_routing` | 字串 | 用於將搜尋作業寫入特定分片的值。指定時，此選項會覆寫搜尋作業的 `routing` 值。

#### `mappings`

索引中存在的欄位對應。如需詳細資訊，請參閱[對應與欄位類型]({{site.url}}{{site.baseurl}}/mappings/)。選用。

#### `settings`

索引的任何組態選項。如需詳細資訊，請參閱[索引設定]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/index-settings/)。

### 請求範例：建立具有索引別名的元件範本

下列請求範例會建立包含索引別名的元件範本：

<!-- spec_insert_start
component: example_code
rest: PUT /_component_template/alias_template
body: |
{
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
PUT /_component_template/alias_template
{
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


response = client.cluster.put_component_template(
  name = "alias_template",
  body =   {
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

### 請求範例：新增元件版本管理

下列範例會將 `version` 號碼新增至元件範本，以簡化外部系統的範本管理：

<!-- spec_insert_start
component: example_code
rest: PUT /_component_template/version_template
body: |
{
  "template": {
    "settings" : {
        "number_of_shards" : 1
    }
  },
  "version": 3
}
-->
{% capture step1_rest %}
PUT /_component_template/version_template
{
  "template": {
    "settings": {
      "number_of_shards": 1
    }
  },
  "version": 3
}
{% endcapture %}

{% capture step1_python %}


response = client.cluster.put_component_template(
  name = "version_template",
  body =   {
    "template": {
      "settings": {
        "number_of_shards": 1
      }
    },
    "version": 3
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

### 請求範例：新增範本中繼資料

下列請求範例使用 `_meta` 參數將中繼資料新增至元件範本。所有中繼資料都儲存在叢集狀態中。

<!-- spec_insert_start
component: example_code
rest: PUT /_component_template/meta_template
body: |
{
  "template": {
    "settings" : {
        "number_of_shards" : 1
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
PUT /_component_template/meta_template
{
  "template": {
    "settings": {
      "number_of_shards": 1
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


response = client.cluster.put_component_template(
  name = "meta_template",
  body =   {
    "template": {
      "settings": {
        "number_of_shards": 1
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

## 擷取元件範本

使用 GET 操作擷取一或多個元件範本及其資訊。

### 端點

```
GET /_component_template/{component-template-name}
GET /_component_template
```

### 路徑參數

下表列出可用的路徑參數。所有路徑參數皆為選用。

參數 | 資料類型 | 說明
:--- | :--- | :---
`component-template-name` | 字串 | 要擷取的元件範本名稱。支援萬用字元運算式（`*`）。若未指定，則傳回所有元件範本。

### 請求範例：依名稱擷取元件範本

<!-- spec_insert_start
component: example_code
rest: GET /_component_template/my_template
-->
{% capture step1_rest %}
GET /_component_template/my_template
{% endcapture %}

{% capture step1_python %}


response = client.cluster.get_component_template(
  name = "my_template"
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

### 請求範例：使用萬用字元模式擷取元件範本

<!-- spec_insert_start
component: example_code
rest: GET /_component_template/my_template*
-->
{% capture step1_rest %}
GET /_component_template/my_template*
{% endcapture %}

{% capture step1_python %}


response = client.cluster.get_component_template(
  name = "my_template*"
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

### 請求範例：擷取所有元件範本

<!-- spec_insert_start
component: example_code
rest: GET /_component_template
-->
{% capture step1_rest %}
GET /_component_template
{% endcapture %}

{% capture step1_python %}

response = client.cluster.get_component_template()
{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 刪除元件範本

使用 DELETE 操作從叢集中移除元件範本。

**重要注意事項**：
- 刪除元件範本不會影響使用該範本建立的現有索引。
- 您無法刪除目前由索引範本參照的元件範本。
- 此操作無法復原。

### 端點

```
DELETE _component_template/{component-template-name}
```

### 請求範例

<!-- spec_insert_start
component: example_code
rest: DELETE /_component_template/my_template
-->
{% capture step1_rest %}
DELETE /_component_template/my_template
{% endcapture %}

{% capture step1_python %}


response = client.cluster.delete_component_template(
  name = "my_template"
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 檢查元件範本是否存在

使用 HEAD 操作檢查元件範本是否存在，而不擷取其內容。此操作僅傳回 HTTP 狀態碼和標頭，不包含回應本文。

### 端點

```
HEAD _component_template/{component-template-name}
```

### 請求範例

<!-- spec_insert_start
component: example_code
rest: HEAD /_component_template/my_template
-->
{% capture step1_rest %}
HEAD /_component_template/my_template
{% endcapture %}

{% capture step1_python %}


response = client.cluster.exists_component_template(
  name = "my_template"
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

### 回應碼

- `200`：元件範本存在。
- `404`：元件範本不存在。

## 必要權限

如果您使用 Security 外掛程式，請確認您具備適當的權限。此 API 需要下列權限：

- `cluster:admin/component_template/get`：取得元件範本所需的權限
- `cluster:admin/component_template/put`：建立或更新元件範本所需的權限
- `cluster:admin/component_template/delete`：刪除元件範本所需的權限
