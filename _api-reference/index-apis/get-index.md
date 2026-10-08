---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "取得索引"
parent: Core index APIs
grand_parent: Index APIs
nav_order: 30
redirect_from:
  - /opensearch/rest-api/index-apis/get-index/
---

# 取得索引 API
**於 1.0 版推出**
{: .label .label-purple }

取得索引 API 操作會傳回一或多個索引的資訊，包括其設定、對應和別名。

<!-- spec_insert_start
api: indices.get
component: endpoints
-->
## 端點
```json
GET /{index}
```
<!-- spec_insert_end -->

## 路徑參數

下表列出可用的路徑參數。

| 參數 | 必要 | 資料類型 | 說明 |
| :--- | :--- | :--- | :--- |
| `index` | **必要** | 字串 | 要擷取的索引名稱。您可以指定單一索引、以逗號分隔的索引清單，或萬用字元運算式。使用 `_all` 或 `*` 可擷取叢集中所有索引的資訊。 |

## 查詢參數

下表列出可用的查詢參數。所有查詢參數皆為選用。

| 參數 | 資料類型 | 說明 | 預設值 |
| :--- | :--- | :--- | :--- |
| `allow_no_indices` | 布林值 | 指定是否忽略未符合任何索引的萬用字元。若為 `false`，當萬用字元未符合任何索引時，請求會傳回錯誤。 | `true` |
| `expand_wildcards` | 字串 | 指定萬用字元運算式可展開為哪些類型的索引。支援以逗號分隔的值。有效值為：<br> - `all`：符合所有索引，包括隱藏索引。<br> - `open`：符合開啟的索引。<br> - `closed`：符合關閉的索引。<br> - `hidden`：符合隱藏索引。必須與 `open`、`closed` 或兩者搭配使用。<br> - `none`：不接受萬用字元運算式。 | `open` |
| `flat_settings` | 布林值 | 指定是否以平面格式傳回設定。當值為 `true` 時，設定會以扁平化格式傳回（例如，`"index.creation_date": "123456789"`）。當值為 `false` 時，設定會以巢狀格式傳回（例如，`"index": {"creation_date": "123456789"}`）。 | `false` |
| `include_defaults` | 布林值 | 指定是否在回應中包含預設設定。當值為 `true` 時，回應會包含所有設定的預設值，可協助您識別要更新的設定名稱和值。 | `false` |
| `ignore_unavailable` | 布林值 | 指定是否忽略無法使用（不存在或已關閉）的索引。若為 `true`，回應中不會包含不存在或已關閉的索引。 | `false` |
| `local` | 布林值 | 指定是否僅從本機節點擷取資訊，而非從叢集管理員節點擷取。 | `false` |
| `cluster_manager_timeout` | 字串 | 等待連線至叢集管理員節點的時間。 | `30s` |

## 請求範例

下列請求範例會擷取 `books` 索引的資訊：

<!-- spec_insert_start
component: example_code
rest: GET /books
-->
{% capture step1_rest %}
GET /books
{% endcapture %}

{% capture step1_python %}


response = client.indices.get(
  index = "books"
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 回應範例

OpenSearch 會傳回所請求的一或多個索引的資訊：

```json
{
  "books": {
    "aliases": {},
    "mappings": {},
    "settings": {
      "index": {
        "replication": {
          "type": "DOCUMENT"
        },
        "number_of_shards": "2",
        "provided_name": "books",
        "creation_date": "1778255937147",
        "number_of_replicas": "1",
        "uuid": "Onnd4TKBQMODrfvAvNXjAg",
        "version": {
          "created": "137277827"
        }
      }
    }
  }
}
```

當您使用 `flat_settings=true` 查詢參數時，設定會以扁平化格式傳回：

```json
{
  "books": {
    "aliases": {},
    "mappings": {},
    "settings": {
      "index.creation_date": "1778255937147",
      "index.number_of_replicas": "1",
      "index.number_of_shards": "2",
      "index.provided_name": "books",
      "index.replication.type": "DOCUMENT",
      "index.uuid": "Onnd4TKBQMODrfvAvNXjAg",
      "index.version.created": "137277827"
    }
  }
}
```

## 回應本文欄位

回應會為每個索引包含一個獨立物件，其索引鍵為索引名稱。每個索引物件包含下列欄位。

欄位 | 資料類型 | 說明
:--- | :--- | :---
`aliases` | 物件 | 與索引相關聯的索引別名。每個索引鍵都是別名名稱，每個值都是別名組態物件。如需詳細資訊，請參閱[索引別名]({{site.url}}{{site.baseurl}}/im-plugin/index-alias/)。
`mappings` | 物件 | 索引中文件的欄位對應。定義每個欄位的資料類型和屬性。如需詳細資訊，請參閱[對應]({{site.url}}{{site.baseurl}}/field-types/)。
`settings` | 物件 | 控制索引行為的索引設定，例如分片和副本的數量。如需詳細資訊，請參閱[索引設定]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/index-settings/)。

## 必要權限

如果您使用 Security 外掛程式，請確認您具有適當的權限：`indices:admin/get`。
