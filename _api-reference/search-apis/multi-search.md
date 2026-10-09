---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "多重搜尋"
parent: Search APIs
nav_order: 20
redirect_from: 
 - /opensearch/rest-api/multi-search/
 - /api-reference/multi-search/
---

# 多重搜尋 API
**於 1.0 版推出**
{: .label .label-purple }

如同名稱所示，多重搜尋作業可讓您將多個搜尋請求捆綁成單一請求。OpenSearch 接著會平行執行這些搜尋，因此相較於每個搜尋各送出一個請求，您能更快收到回應。OpenSearch 會獨立執行每個搜尋，因此其中一個失敗不會影響其他搜尋。


<!-- spec_insert_start
api: msearch
component: endpoints
-->
## 端點
```json
GET  /_msearch
POST /_msearch
GET  /{index}/_msearch
POST /{index}/_msearch
```
<!-- spec_insert_end -->

在路徑中指定索引，會為中繼資料行未包含 `index` 欄位的任何搜尋設定預設目標。如果您省略路徑參數，且某個搜尋的中繼資料行也未指定 `index`，該搜尋會對所有索引執行。


## 查詢參數與中繼資料選項

所有參數都是選用。部分參數也可以依每個搜尋，作為各中繼資料行的一部分來套用。

參數 | 類型 | 說明 | 支援於中繼資料行
:--- | :--- | :--- | :---
`allow_no_indices` | 布林值 | 是否忽略未符合任何索引的萬用字元。預設為 `true`。 | 是
`cancel_after_time_interval` | 時間 | 搜尋請求將被取消的時間。支援父層與子層請求層級。優先順序為：<br> 1. 子層參數<br> 2. 父層參數<br> 3. [叢集設定]({{site.url}}{{site.baseurl}}/api-reference/cluster-settings/)。<br>預設為 -1。 | 是
`ccs_minimize_roundtrips` | 布林值 | OpenSearch 是否應盡量減少協調節點與遠端叢集之間的網路來回次數（僅適用於跨叢集搜尋請求）。預設為 `true`。 | 否
`expand_wildcards` | 列舉值 | 將萬用字元運算式展開為具體索引。以逗號合併多個值。支援的值為 `all`、`open`、`closed`、`hidden` 及 `none`。預設為 `open`。 | 是
`ignore_unavailable` | 布林值 | 若索引清單中的某個索引或分片不存在，是否予以忽略而非讓查詢失敗。預設為 `false`。 | 是
`include_named_queries_score` | 布林值 | 是否傳回具名查詢的分數。預設為 `false`。 | 否
`max_concurrent_searches` | 整數 | 並行搜尋的最大數量。預設值取決於您的節點數與搜尋執行緒集區大小。較高的值可提升效能，但可能使叢集超載。 | 否
`max_concurrent_shard_requests` | 整數 | 每個搜尋在每個節點上執行的並行分片請求最大數量。預設為 5。較高的值可提升效能，但可能使叢集超載。 | 否
`pre_filter_shard_size` | 整數 | 觸發預先篩選來回以排除無法符合查詢之分片的閾值（例如，因為日期範圍篩選落在分片的界限之外）。未指定時，若請求的目標超過 128 個分片、目標為唯讀索引，或依已編製索引的欄位排序，則會執行預先篩選階段。預設為 `128`。 | 否
`rest_total_hits_as_int` | 字串 | `hits.total` 屬性是否以整數（`true`）或物件（`false`）形式傳回。預設為 `false`。 | 否
`routing` | 字串 | 以逗號分隔的自訂路由值，用於將請求中的所有搜尋路由至特定分片。若要為個別搜尋設定路由，請改用中繼資料行中的 `routing` 選項。 | 否
`search_type` | 字串 | 影響相關性分數。有效選項為 `query_then_fetch` 與 `dfs_query_then_fetch`。`query_then_fetch` 使用分片的詞彙與文件頻率為文件評分（較快、較不準確），而 `dfs_query_then_fetch` 則使用所有分片的詞彙與文件頻率（較慢、較準確）。預設為 `query_then_fetch`。 | 是
`typed_keys` | 布林值 | 是否在回應中為彙總名稱加上其內部類型的前置字元。預設為 `false`。 | 否


## 僅限中繼資料的選項

部分選項無法作為整個請求的參數套用。您可以改為依每個搜尋，作為各中繼資料行的一部分來套用。全部都是選用。

選項 | 類型 | 說明
:--- | :--- | :---
`index` | 字串、字串陣列 | 如果您未在 URL 中指定一個或多個索引（或想為個別搜尋覆寫 URL 值），可以在此加入。範例包括 `"logs-*"` 與 `["my-store", "sample_data_ecommerce"]`。
`preference` | 字串 | 您想執行搜尋的節點或分片。此設定有助於測試，但在大多數情況下，預設行為可提供最佳的搜尋延遲。選項包括 `_local`、`_only_local`、`_prefer_nodes`、`_only_nodes` 及 `_shards`。最後三個選項接受節點或分片清單。範例包括 `"_only_nodes:data-node1,data-node2"` 與 `"_shards:0,1`。
`request_cache` | 布林值 | 是否快取結果，可改善重複搜尋的延遲。預設為使用索引的 `index.requests.cache.enable` 設定（新索引預設為 `true`）。
`routing` | 字串 | 以逗號分隔的自訂路由值，例如 `"routing": "value1,value2,value3"`。與查詢參數層級套用於請求中所有搜尋的 `routing` 不同，此選項僅針對個別搜尋的路由。

## 請求本文

多重搜尋請求本文使用以換行符號分隔的 JSON（NDJSON）格式，在中繼資料行與查詢行之間交替：

```
Metadata\n
Query\n
Metadata\n
Query\n

```

- 中繼資料行包含選項，例如要搜尋哪些索引以及搜尋類型。若不需要依搜尋覆寫，中繼資料行可以是空的（`{}`）。
- 查詢行使用 [Query DSL]({{site.url}}{{site.baseurl}}/opensearch/query-dsl/)。

如同[大量]({{site.url}}{{site.baseurl}}/api-reference/document-apis/bulk/)作業，JSON 不需要壓縮---可以有空格---但必須位於單一行。OpenSearch 使用換行字元來剖析多重搜尋請求，並要求請求本文以換行字元結尾。

將請求傳送至此端點時，請將 `Content-Type` 標頭設為 `application/x-ndjson`。
{: .note}

### 查詢本文欄位

每個查詢行接受與[搜尋 API]({{site.url}}{{site.baseurl}}/api-reference/search/) 請求本文相同的參數。下表列出最常用的欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `query` | 物件 | 要執行的 Query DSL 運算式。請參閱 [Query DSL]({{site.url}}{{site.baseurl}}/opensearch/query-dsl/)。 |
| `aggregations` | 物件 | 與搜尋一併執行的彙總。請參閱[彙總]({{site.url}}{{site.baseurl}}/aggregations/)。 |
| `from` | 整數 | 傳回命中結果的起始位移。預設為 `0`。 |
| `size` | 整數 | 要傳回的命中結果數量。預設為 `10`。 |
| `sort` | 陣列或物件 | 排序結果所依據的欄位與順序。 |
| `_source` | 布林值、字串或物件 | 控制每個命中結果的 `_source` 中包含哪些欄位。 |
| `highlight` | 物件 | 符合欄位的醒目提示組態。 |


## 範例：搜尋多個索引

下列範例對多個索引執行查詢，並在每個中繼資料行中指定目標索引：


<!-- spec_insert_start
component: example_code
rest: GET /_msearch
body: |
{ "index": "opensearch_dashboards_sample_data_logs"}
{ "query": { "match_all": {} }, "from": 0, "size": 10}
{ "index": "opensearch_dashboards_sample_data_ecommerce", "search_type": "dfs_query_then_fetch"}
{ "query": { "match_all": {} } }
-->
{% capture step1_rest %}
GET /_msearch
{ "index": "opensearch_dashboards_sample_data_logs"}
{ "query": { "match_all": {} }, "from": 0, "size": 10}
{ "index": "opensearch_dashboards_sample_data_ecommerce", "search_type": "dfs_query_then_fetch"}
{ "query": { "match_all": {} } }
{% endcapture %}

{% capture step1_python %}


response = client.msearch(
  body = '''
{ "index": "opensearch_dashboards_sample_data_logs"}
{ "query": { "match_all": {} }, "from": 0, "size": 10}
{ "index": "opensearch_dashboards_sample_data_ecommerce", "search_type": "dfs_query_then_fetch"}
{ "query": { "match_all": {} } }
'''
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->


## 範例：使用預設索引

當您在 URL 路徑中指定索引時，對於中繼資料行未包含 `index` 欄位的任何搜尋，該索引會作為預設索引。下列範例會對 `products` 索引執行兩個查詢，而無需在每個中繼資料行中重複索引名稱：

<!-- spec_insert_start
component: example_code
rest: GET /products/_msearch
body: |
{}
{"query": {"match": {"product_name": "headphones"}}, "size": 1}
{}
{"query": {"range": {"price": {"gte": 30, "lte": 50}}}}
-->
{% capture step1_rest %}
GET /products/_msearch
{}
{"query": {"match": {"product_name": "headphones"}}, "size": 1}
{}
{"query": {"range": {"price": {"gte": 30, "lte": 50}}}}
{% endcapture %}

{% capture step1_python %}


response = client.msearch(
  index = "products",
  body = '''
{}
{"query": {"match": {"product_name": "headphones"}}, "size": 1}
{}
{"query": {"range": {"price": {"gte": 30, "lte": 50}}}}
'''
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 使用搜尋範本

Multi-search API 透過 `_msearch/template` 端點支援[搜尋範本]({{site.url}}{{site.baseurl}}/search-plugins/search-template/)。這可讓您執行參數化搜尋，將查詢結構與搜尋時傳入的值分開。

### 範例：內嵌範本

下列請求使用內嵌範本，在單一呼叫中執行兩個參數化搜尋：

```json
GET _msearch/template
{"index": "products"}
{"source": {"query": {"match": {"product_name": "{{search_term}}"}}}, "params": {"search_term": "wireless"}}
{"index": "products"}
{"source": {"query": {"range": {"price": {"lte": "{{max_price}}"}}}}, "params": {"max_price": "75"}}

```

### 範例：已儲存的範本

您也可以依 ID 參考預先註冊的範本。首先，建立已儲存的範本：

```json
POST _scripts/product_search_template
{
  "script": {
    "lang": "mustache",
    "source": {
      "query": {
        "multi_match": {
          "query": "{{query_text}}",
          "fields": ["product_name", "description"]
        }
      },
      "size": "{{result_count}}"
    }
  }
}
```
{% include copy-curl.html %}

```json
POST _scripts/price_range_template
{
  "script": {
    "lang": "mustache",
    "source": {
      "query": {
        "range": {
          "price": {
            "gte": "{{min_price}}",
            "lte": "{{max_price}}"
          }
        }
      },
      "size": "{{result_count}}"
    }
  }
}
```
{% include copy-curl.html %}

接著在多重搜尋請求中使用已儲存的範本：

```json
GET _msearch/template
{"index": "products"}
{"id": "product_search_template", "params": {"query_text": "bluetooth speaker", "result_count": "5"}}
{"index": "products"}
{"id": "price_range_template", "params": {"min_price": "20", "max_price": "100", "result_count": "3"}}

```

## 回應範例

OpenSearch 會傳回一個陣列，其中包含每個搜尋的結果，順序與多重搜尋請求中的順序相同。

```json
{
  "took" : 2150,
  "responses" : [
    {
      "took" : 2149,
      "timed_out" : false,
      "_shards" : {
        "total" : 1,
        "successful" : 1,
        "skipped" : 0,
        "failed" : 0
      },
      "hits" : {
        "total" : {
          "value" : 10000,
          "relation" : "gte"
        },
        "max_score" : 1.0,
        "hits" : [
          {
            "_index" : "opensearch_dashboards_sample_data_logs",
            "_id" : "_fnhBXsBgv2Zxgu9dZ8Y",
            "_score" : 1.0,
            "_source" : {
              "agent" : "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322)",
              "bytes" : 4657,
              "clientip" : "213.116.129.196",
              "extension" : "zip",
              "geo" : {
                "srcdest" : "CN:US",
                "src" : "CN",
                "dest" : "US",
                "coordinates" : {
                  "lat" : 42.35083333,
                  "lon" : -86.25613889
                }
              },
              "host" : "artifacts.opensearch.org",
              "index" : "opensearch_dashboards_sample_data_logs",
              "ip" : "213.116.129.196",
              "machine" : {
                "ram" : 16106127360,
                "os" : "ios"
              },
              "memory" : null,
              "message" : "213.116.129.196 - - [2018-07-30T14:12:11.387Z] \"GET /opensearch_dashboards/opensearch_dashboards-1.0.0-windows-x86_64.zip HTTP/1.1\" 200 4657 \"-\" \"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322)\"",
              "phpmemory" : null,
              "referer" : "http://twitter.com/success/ellison-onizuka",
              "request" : "/opensearch_dashboards/opensearch_dashboards-1.0.0-windows-x86_64.zip",
              "response" : 200,
              "tags" : [
                "success",
                "info"
              ],
              "timestamp" : "2021-08-02T14:12:11.387Z",
              "url" : "https://artifacts.opensearch.org/downloads/opensearch_dashboards/opensearch_dashboards-1.0.0-windows-x86_64.zip",
              "utc_time" : "2021-08-02T14:12:11.387Z",
              "event" : {
                "dataset" : "sample_web_logs"
              }
            }
          },
          ...
        ]
      },
      "status" : 200
    },
    {
      "took" : 1473,
      "timed_out" : false,
      "_shards" : {
        "total" : 1,
        "successful" : 1,
        "skipped" : 0,
        "failed" : 0
      },
      "hits" : {
        "total" : {
          "value" : 4675,
          "relation" : "eq"
        },
        "max_score" : 1.0,
        "hits" : [
          {
            "_index" : "opensearch_dashboards_sample_data_ecommerce",
            "_id" : "efnhBXsBgv2Zxgu9ap7e",
            "_score" : 1.0,
            "_source" : {
              "category" : [
                "Women's Clothing"
              ],
              "currency" : "EUR",
              "customer_first_name" : "Gwen",
              "customer_full_name" : "Gwen Dennis",
              "customer_gender" : "FEMALE",
              "customer_id" : 26,
              "customer_last_name" : "Dennis",
              "customer_phone" : "",
              "day_of_week" : "Tuesday",
              "day_of_week_i" : 1,
              "email" : "gwen@dennis-family.zzz",
              "manufacturer" : [
                "Tigress Enterprises",
                "Gnomehouse mom"
              ],
              "order_date" : "2021-08-10T16:24:58+00:00",
              "order_id" : 576942,
              "products" : [
                {
                  "base_price" : 32.99,
                  "discount_percentage" : 0,
                  "quantity" : 1,
                  "manufacturer" : "Tigress Enterprises",
                  "tax_amount" : 0,
                  "product_id" : 22182,
                  "category" : "Women's Clothing",
                  "sku" : "ZO0036600366",
                  "taxless_price" : 32.99,
                  "unit_discount_amount" : 0,
                  "min_price" : 14.85,
                  "_id" : "sold_product_576942_22182",
                  "discount_amount" : 0,
                  "created_on" : "2016-12-20T16:24:58+00:00",
                  "product_name" : "Jersey dress - black/red",
                  "price" : 32.99,
                  "taxful_price" : 32.99,
                  "base_unit_price" : 32.99
                },
                {
                  "base_price" : 28.99,
                  "discount_percentage" : 0,
                  "quantity" : 1,
                  "manufacturer" : "Gnomehouse mom",
                  "tax_amount" : 0,
                  "product_id" : 14230,
                  "category" : "Women's Clothing",
                  "sku" : "ZO0234902349",
                  "taxless_price" : 28.99,
                  "unit_discount_amount" : 0,
                  "min_price" : 13.05,
                  "_id" : "sold_product_576942_14230",
                  "discount_amount" : 0,
                  "created_on" : "2016-12-20T16:24:58+00:00",
                  "product_name" : "Blouse - june bug",
                  "price" : 28.99,
                  "taxful_price" : 28.99,
                  "base_unit_price" : 28.99
                }
              ],
              "sku" : [
                "ZO0036600366",
                "ZO0234902349"
              ],
              "taxful_total_price" : 61.98,
              "taxless_total_price" : 61.98,
              "total_quantity" : 2,
              "total_unique_products" : 2,
              "type" : "order",
              "user" : "gwen",
              "geoip" : {
                "country_iso_code" : "US",
                "location" : {
                  "lon" : -118.2,
                  "lat" : 34.1
                },
                "region_name" : "California",
                "continent_name" : "North America",
                "city_name" : "Los Angeles"
              },
              "event" : {
                "dataset" : "sample_ecommerce"
              }
            }
          },
         ...
        ]
      },
      "status" : 200
    }
  ]
}
```

## 回應本文欄位

下表列出最上層的回應本文欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `took` | 整數 | OpenSearch 處理請求中所有搜尋的總時間，以毫秒為單位。 |
| `responses` | 陣列 | 搜尋回應物件的陣列，傳回順序與請求中對應的搜尋相同。如果某個特定搜尋完全失敗，該搜尋的陣列項目會包含 `error` 物件和 `status` 狀態碼，而非正常的搜尋回應。 |

下表列出 `responses` 陣列中每個項目的欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `took` | 整數 | OpenSearch 處理個別搜尋的時間，以毫秒為單位。 |
| `timed_out` | 布林值 | 搜尋是否在完成前逾時。 |
| `_shards` | 物件 | 搜尋涉及的分片數量相關資訊，包括 `total`、`successful`、`skipped` 和 `failed` 計數。 |
| `hits` | 物件 | 搜尋結果，包括 `total` 命中數、`max_score`，以及相符 `hits` 的陣列。 |
| `status` | 整數 | 個別搜尋結果的 HTTP 狀態碼。值為 `200` 表示成功。 |

## 部分回應

如果執行期間有一或多個分片失敗，多搜尋 API 仍會傳回成功分片的結果。`responses` 陣列中的每個個別搜尋回應都包含 `_shards` 物件，回報有多少分片成功、多少分片失敗，讓您判斷結果是否完整。

## 必要權限

如果您使用 Security 外掛程式，請確定您具有適當的權限：`indices:data/read/msearch`。
