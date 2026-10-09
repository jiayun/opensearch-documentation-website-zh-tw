---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "多重搜尋範本"
parent: Search templates
grand_parent: Search APIs
nav_order: 20
redirect_from:
  - /api-reference/msearch-template/
  - /api-reference/search-apis/msearch-template/
---

# 多重搜尋範本 API

**於 1.0 版推出**
{: .label .label-purple }

多重搜尋範本 API 會在單一 API 請求中執行多個搜尋範本請求。

## 端點

多重搜尋範本 API 使用下列路徑：

```json
GET /_msearch/template
POST /_msearch/template
GET /{index}/_msearch/template
POST /{index}/_msearch/template
```


## 查詢參數與中繼資料選項

所有參數皆為選用。部分參數也可依每次搜尋套用，作為各中繼資料行的一部分。

參數 | 類型 | 說明 | 支援於中繼資料
:--- | :--- | :---  | :---
`allow_no_indices` | Boolean | 指定是否忽略未符合任何索引的萬用字元。預設為 `true`。 | 是
`cancel_after_time_interval` | Time | 搜尋請求將被取消的時間間隔。支援於父層與子層請求。優先順序為子層參數、父層參數，以及[叢集設定]({{site.url}}{{site.baseurl}}/api-reference/cluster-settings/)。預設為 `-1`。 | 是
`css_minimize_roundtrips` | Boolean | 指定 OpenSearch 是否應盡量減少協調節點與遠端叢集之間的網路來回次數（僅適用於跨叢集搜尋請求）。預設為 `true`。 | 否
`expand_wildcards` | Enum | 將萬用字元運算式展開為具體索引。以逗號合併多個值。支援的值為 `all`、`open`、`closed`、`hidden` 及 `none`。預設為 `open`。 | 是
`ignore_unavailable` | Boolean | 若索引清單中的某個索引或分片不存在，此設定會指定是否忽略缺少的索引或分片，而非讓查詢失敗。預設為 `false`。 | 是
`max_concurrent_searches` | Integer | 並行搜尋的最大數量。預設值取決於您的節點數與搜尋執行緒集區大小。較高的值可提升效能，但可能會有使叢集超載的風險。 | 否
`max_concurrent_shard_requests` | Integer | 每個搜尋在每個節點上執行的並行分片請求最大數量。預設為 `5`。較高的值可提升效能，但可能會有使叢集超載的風險。 | 否
`pre_filter_shard_size` | Integer | 預設為 `128`。 | 否
`rest_total_hits_as_int` | String | 指定 `hits.total` 屬性要以整數（`true`）或物件（`false`）形式傳回。預設為 `false`。 | 否
`search_type` | String | 會影響相關性分數。有效選項為 `query_then_fetch` 與 `dfs_query_then_fetch`。`query_then_fetch` 會使用單一分片的詞彙與文件頻率為文件評分（較快、較不精確），而 `dfs_query_then_fetch` 則使用所有分片的詞彙與文件頻率（較慢、較精確）。預設為 `query_then_fetch`。 | 是
`typed_keys` | Boolean | 指定是否在回應中為彙總名稱加上其內部類型的前置字元。預設為 `false`。 | 否

### 僅限中繼資料的選項

部分選項無法作為整個請求的參數套用。您可改為依每次搜尋套用，作為各中繼資料行的一部分。所有選項皆為選用。

選項 | 類型 | 說明
:--- | :--- | :---
`index` | String, string array | 若您未在 URL 中指定一個或多個索引（或想為個別搜尋覆寫 URL 值），可將其納入此選項。範例包括 `"logs-*"` 與 `["my-store", "sample_data_ecommerce"]`。
`preference` | String | 指定您要在哪些節點或分片上執行搜尋。此設定對測試很有用，但在大多數情況下，預設行為可提供最佳的搜尋延遲。選項包括 `_local`、`_only_local`、`_prefer_nodes`、`_only_nodes` 及 `_shards`。最後三個選項接受節點或分片清單。範例包括 `"_only_nodes:data-node1,data-node2"` 與 `"_shards:0,1`。
`request_cache` | Boolean | 指定是否快取結果，可改善重複搜尋的延遲。預設為使用索引的 `index.requests.cache.enable` 設定（新索引的預設值為 `true`）。
`routing` | String | 以逗號分隔的自訂路由值，例如 `"routing": "value1,value2,value3"`。

## 請求本文

多重搜尋範本請求本文遵循下列模式，類似於[多重搜尋 API]({{site.url}}{{site.baseurl}}/api-reference/multi-search/) 的模式：

```
Metadata\n
Query\n
Metadata\n
Query\n

```

- 中繼資料行包含選項，例如要搜尋哪些索引以及搜尋類型。
- 查詢行使用[查詢 DSL]({{site.url}}{{site.baseurl}}/opensearch/query-dsl/)。

如同 [bulk]({{site.url}}{{site.baseurl}}/api-reference/document-apis/bulk/) 操作，JSON 不必壓縮---可以保留空格---但必須寫在單一行。OpenSearch 使用換行字元來解析多重搜尋請求，並要求請求本文以換行字元結尾。

## 範例請求

下列範例 `msearch/template` API 請求會使用名為 `line_search_template` 與 `play_search_template` 的多個範本，對單一索引執行查詢：

<!-- spec_insert_start
component: example_code
rest: GET /_msearch/template
body: |
{"index":"shakespeare"}
{"id":"line_search_template","params":{"text_entry":"All the world's a stage","limit":false,"size":2}}
{"index":"shakespeare"}
{"id":"play_search_template","params":{"play_name":"Henry IV"}}
-->
{% capture step1_rest %}
GET /_msearch/template
{"index":"shakespeare"}
{"id":"line_search_template","params":{"text_entry":"All the world's a stage","limit":false,"size":2}}
{"index":"shakespeare"}
{"id":"play_search_template","params":{"play_name":"Henry IV"}}
{% endcapture %}

{% capture step1_python %}


response = client.msearch_template(
  body = '''
{"index":"shakespeare"}
{"id":"line_search_template","params":{"text_entry":"All the world's a stage","limit":false,"size":2}}
{"index":"shakespeare"}
{"id":"play_search_template","params":{"play_name":"Henry IV"}}
'''
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 範例回應

OpenSearch 會傳回一個陣列，其中包含每次搜尋的結果，順序與多重搜尋範本請求中的順序相同：

```json
{
  "took": 5,
  "responses": [
    {
      "took": 5,
      "timed_out": false,
      "_shards": {
        "total": 1,
        "successful": 1,
        "skipped": 0,
        "failed": 0
      },
      "hits": {
        "total": {
          "value": 0,
          "relation": "eq"
        },
        "max_score": null,
        "hits": []
      },
      "status": 200
    },
    {
      "took": 3,
      "timed_out": false,
      "_shards": {
        "total": 1,
        "successful": 1,
        "skipped": 0,
        "failed": 0
      },
      "hits": {
        "total": {
          "value": 0,
          "relation": "eq"
        },
        "max_score": null,
        "hits": []
      },
      "status": 200
    }
  ]
}
```
