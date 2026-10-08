---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "List API"
nav_order: 20
has_children: true
redirect_from:
  - /api-reference/list/
---

# List API
**於 2.18 版推出**
{: .label .label-purple }

List API 以分頁格式擷取索引和分片的統計資料。這可簡化處理包含大量索引之回應的工作。

List API 支援兩種操作：

- [列出索引]({{site.url}}{{site.baseurl}}/api-reference/list/list-indices/)
- [列出分片]({{site.url}}{{site.baseurl}}/api-reference/list/list-shards/)

## 共用查詢參數

所有 List API 操作都支援下列選用查詢參數。

參數 | 說明
:--- | :--- |
`v` |  為各欄加入標頭以提供詳細輸出。它也會加入一些格式設定，以協助對齊各欄。本節的所有範例都包含 `v` 參數。
`help` | 列出指定操作的預設標頭及其他可用標頭。
`h`  |  將輸出限制為特定標頭。
`format` |  傳回結果的格式。有效值為 `json`、`yaml`、`cbor` 和 `smile`。
`s` | 依指定欄排序輸出。

## 範例

下列範例示範如何使用選用查詢參數來自訂所有 List API 回應。


### 取得詳細輸出

若要查詢索引及其統計資料，並取得在回應中包含所有欄標題的詳細輸出，請使用 `v` 查詢參數，如下列範例所示。

#### 請求

<!-- spec_insert_start
component: example_code
rest: GET /_list/indices?v
-->
{% capture step1_rest %}
GET /_list/indices?v
{% endcapture %}

{% capture step1_python %}


response = client.list.indices(
  params = { "v": "true" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

#### 回應

```json
health status index           uuid    pri rep  docs.count  docs.deleted
green  open   .kibana_1 - - - -              
yellow open    sample-index-1 - - - -
next_token null
```


### 取得所有可用標頭

若要查看所有可用標頭，請以下列語法使用 `help` 參數：

```json
GET _list/{operation_name}?help
```
{% include copy-curl.html %}

#### 請求

下列列出索引操作範例會傳回所有可用標頭：

<!-- spec_insert_start
component: example_code
rest: GET /_list/indices?help
-->
{% capture step1_rest %}
GET /_list/indices?help
{% endcapture %}

{% capture step1_python %}


response = client.list.indices(
  params = { "help": "true" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

#### 回應

下列範例以表格顯示索引及其健康狀態：

```json
health     | h                              | current health status
status     | s                              | open/close status
index      | i,idx                          | index name
uuid       | id,uuid                        | index uuid
pri        | p,shards.primary,shardsPrimary | number of primary shards
rep        | r,shards.replica,shardsReplica | number of replica shards
docs.count | dc,docsCount                   | available docs
```

### 取得部分標頭

若要將輸出限制為部分標頭，請以下列語法使用 `h` 參數：

```json
GET _list/{operation_name}?h={header_name_1},{header_name_2}&v
```
{% include copy-curl.html %}

對於任何操作，您可以使用 `help` 參數來確認哪些標頭可用，然後使用 `h` 參數將輸出限制為僅包含部分標頭。 

#### 請求

下列範例將回應中的索引資訊限制為僅包含索引名稱和健康狀態標頭：

<!-- spec_insert_start
component: example_code
rest: GET /_list/indices?h=health,index
-->
{% capture step1_rest %}
GET /_list/indices?h=health,index
{% endcapture %}

{% capture step1_python %}


response = client.list.indices(
  params = { "h": "health,index" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

### 回應

```json
green  .kibana_1
yellow sample-index-1
next_token null
```


### 依標頭排序

若要依標頭排序單一頁面上的輸出，請以下列語法使用 `s` 參數：

```json
GET _list/{operation_name}?s={header_name_1},{header_name_2}
```
{% include copy-curl.html %}

#### 請求

下列範例請求會依索引名稱排序索引：

<!-- spec_insert_start
component: example_code
rest: GET /_list/indices?s=h,i
-->
{% capture step1_rest %}
GET /_list/indices?s=h,i
{% endcapture %}

{% capture step1_python %}


response = client.list.indices(
  params = { "s": "h,i" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

#### 回應

```json
green sample-index-2
yellow sample-index-1
next_token null
```

### 以 JSON 格式擷取資料

預設情況下，List API 會以 `text/plain` 格式傳回資料。其他支援的格式為 [YAML](https://yaml.org/)、[CBOR](https://cbor.io/) 和 [Smile](https://github.com/FasterXML/smile-format-specification)。


若要以 JSON 格式擷取資料，請以下列語法使用 `format=json` 參數。

如果您使用 Security 外掛程式，請確保您具有適當的權限。
{: .note }

#### 請求

```json
GET _list/{operation_name}?help
```
{% include copy-curl.html %}

#### 請求

<!-- spec_insert_start
component: example_code
rest: GET /_list/indices?format=json
-->
{% capture step1_rest %}
GET /_list/indices?format=json
{% endcapture %}

{% capture step1_python %}


response = client.list.indices(
  params = { "format": "json" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

### 回應

回應包含 JSON 格式的資料：

```json
{
  "next_token": null,
  "indices": [
    {
      "health": "green",
      "status": "-",
      "index": ".kibana_1",
      "uuid": "-",
      "pri": "-",
      "rep": "-",
      "docs.count": "-",
      "docs.deleted": "-",
      "store.size": "-",
      "pri.store.size": "-"
    },
    {
      "health": "yellow",
      "status": "-",
      "index": "sample-index-1",
      "uuid": "-",
      "pri": "-",
      "rep": "-",
      "docs.count": "-",
      "docs.deleted": "-",
      "store.size": "-",
      "pri.store.size": "-"
    }
  ]
}
```

