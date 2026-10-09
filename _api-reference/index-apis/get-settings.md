---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "取得索引設定"
parent: Index settings and mappings
grand_parent: Index APIs
nav_order: 10
redirect_from:
  - /opensearch/rest-api/index-apis/get-settings/
---

# Get Index Settings API
**於 1.0 版推出**
{: .label .label-purple }

Get Index Settings API 會傳回一個或多個索引的組態設定。使用此 API 可擷取索引層級的設定，例如分片與副本的數量、重新整理間隔、分析組態，以及其他索引參數。


## 端點

<!-- spec_insert_start
component: endpoints
-->
```json
GET /_settings
GET /{target-index}/_settings
GET /{target-index}/_settings/{setting}
```
<!-- spec_insert_end -->

## 路徑參數

下表列出可用的路徑參數。所有路徑參數皆為選用。

參數 | 資料類型 | 說明
:--- | :--- | :---
`target-index` | 字串 | 要從中擷取設定的索引名稱。您可以指定單一索引名稱、以逗號分隔的索引名稱清單，或萬用字元運算式。使用 `_all` 或 `*` 可從叢集中的所有索引擷取設定。
`setting` | 字串 | 要擷取的特定設定名稱。指定後，回應只會包含所要求的設定，而非所有設定。

## 查詢參數

下表列出可用的查詢參數。所有查詢參數皆為選用。

參數 | 資料類型 | 說明
:--- | :--- | :---
`allow_no_indices` | 布林值 | 指定是否忽略未符合任何索引的萬用字元運算式或索引模式。當 `false` 時，若萬用字元運算式未符合任何索引，請求會傳回錯誤。當 `true` 時，請求會忽略不存在的索引，只傳回現有索引的設定。預設為 `true`。
`expand_wildcards` | 字串 | 指定萬用字元運算式可展開的索引類型。支援以逗號分隔的值。有效值為 `all` (所有索引)、`open` (開啟的索引)、`closed` (關閉的索引)、`hidden` (隱藏的索引)，以及 `none` (不接受萬用字元運算式)。預設為 `open`。
`flat_settings` | 布林值 | 指定是否以扁平格式傳回設定。當 `true` 時，設定會以扁平化格式傳回 (例如 `”index.creation_date”: “123456789”`)。當 `false` 時，設定會以巢狀格式傳回 (例如 `”index”: {“creation_date”: “123456789”}`)。預設為 `false`。
`include_defaults` | 布林值 | 指定是否在回應中包含預設設定。預設設定是 OpenSearch 在未明確設定時隱含套用的組態，包括 OpenSearch 外掛程式所使用的設定。當 `true` 時，回應會同時包含自訂與預設設定。當 `false` 時，回應只會包含自訂設定。預設為 `false`。
`ignore_unavailable` | 布林值 | 指定是否忽略不存在或已關閉的索引。當 `true` 時，若目標索引不存在或已關閉，請求不會傳回錯誤。當 `false` 時，若目標索引無法使用，請求會傳回錯誤。預設為 `false`。
`local` | 布林值 | 指定只從本機節點擷取設定，或從叢集管理員節點擷取設定。當 `true` 時，會從本機節點擷取設定。當 `false` 時，會從叢集管理員節點擷取設定。預設為 `false`。
`cluster_manager_timeout` | 時間 | 等待連線至叢集管理員節點的時間量。預設為 `30s`。

## 範例請求：擷取單一索引的設定

下列範例會擷取 `books` 索引的所有設定：

<!-- spec_insert_start
component: example_code
rest: GET /books/_settings
-->
{% capture step1_rest %}
GET /books/_settings
{% endcapture %}

{% capture step1_python %}


response = client.indices.get_settings(
  index = "books"
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 範例請求：從多個索引擷取設定

下列範例會從多個索引擷取設定：

```json
GET /books,products/_settings
```
{% include copy.html %}

## 範例請求：從所有索引擷取設定

下列範例會從叢集中的所有索引擷取設定：

```json
GET /_all/_settings
```
{% include copy.html %}

## 範例請求：使用萬用字元模式擷取設定

下列範例使用萬用字元模式，從所有符合該模式的索引擷取設定：

```json
GET /logs-*/_settings
```
{% include copy.html %}

## 範例請求：依名稱篩選設定

下列範例會篩選回應，只傳回符合指定模式的設定：

```json
GET /logs-*/_settings/index.number_*
```
{% include copy.html %}

{% capture default_response %}

## 範例回應

根據預設，設定會以巢狀格式傳回：

```json
{
  "books": {
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

{% endcapture %}
{{ default_response }}

{% capture flat_response %}

## 範例回應：扁平格式

當您指定 `flat_settings=true` 時，設定會以扁平化格式傳回：

```json
{
  "books": {
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

{% endcapture %}
{{ flat_response }}

## 回應本文欄位

下表列出所有回應本文欄位。

欄位 | 說明
:--- | :---
`settings` | 包含索引所有設定的物件。傳回的特定設定取決於索引組態。如需可用索引設定的相關資訊，請參閱[索引設定]({{site.url}}{{site.baseurl}}/im-plugin/index-settings/)。

## 必要權限

如果您使用 Security 外掛程式，請確認您具有適當的權限：`indices:monitor/settings/get`。
