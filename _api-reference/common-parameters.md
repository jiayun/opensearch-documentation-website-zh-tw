---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "常見 REST 參數"
nav_order: 150
redirect_from:
  - /opensearch/common-parameters/
---

# 常見 REST 參數

OpenSearch REST API 共用下列查詢參數、請求本文慣例與標頭。

布林值參數只接受 `true` 與 `false`。OpenSearch 會拒絕其他值，例如 `yes` 或 `1`。數值參數可接受 JSON 數字或包含數字的字串，因此 `"size": 10` 與 `"size": "10"` 是等效的。關於時間、位元組大小與距離參數可接受的單位，請參閱[支援的單位]({{site.url}}{{site.baseurl}}/api-reference/units/)。

## 人類可讀的輸出

許多 API（例如 stats API）會傳回帶有單位的值，例如大小與持續時間。根據預設，OpenSearch 只會以適合程式使用的原始形式傳回這些值，例如 `size_in_bytes`。若要同時傳回每個值的人類可讀版本，請在請求 URL 中加入 `?human=true`。例如，索引的儲存大小會同時以 `"size": "4.2kb"` 與 `"size_in_bytes": 4356` 傳回。關於支援的單位清單，請參閱[支援的單位]({{site.url}}{{site.baseurl}}/api-reference/units/)。

下列請求會使用人類可讀的值傳回索引統計資料：

```json
GET /products/_stats/store?human=true
```
{% include copy-curl.html %}

## 美化結果

若要以可讀的縮排格式取得 JSON 回應，請在請求 URL 中加入 `?pretty=true`。請只在手動閱讀回應時使用此參數，因為它會增加回應大小。

下列請求會以美化的 JSON 格式傳回叢集健康狀態：

```json
GET /_cluster/health?pretty=true
```
{% include copy-curl.html %}

## YAML 輸出

若要以 YAML 格式傳回回應，請在請求 URL 中加入 `?format=yaml`。

下列請求會以 YAML 格式傳回叢集健康狀態：

```json
GET /_cluster/health?format=yaml
```
{% include copy-curl.html %}

## 內容類型

若要指定請求本文中的內容類型，請在請求標頭中使用 `Content-Type` 鍵名。大多數操作支援 JSON、YAML、CBOR 與 SMILE 格式。若您以 YAML 傳送請求本文，OpenSearch 也會以 YAML 傳回回應。[Bulk]({{site.url}}{{site.baseurl}}/api-reference/document-apis/bulk/) 與 [Multi-search]({{site.url}}{{site.baseurl}}/api-reference/search-apis/multi-search/) API 只接受以換行分隔的 JSON（`application/x-ndjson`）、JSON 與 SMILE。OpenSearch 會拒絕 `Content-Type` 不是支援格式的請求。

下列請求會為請求本文指定 JSON 格式：

```bash
curl -H "Content-Type: application/json" -XGET "localhost:9200/products/_search" -d '{"query": {"match_all": {}}}'
```
{% include copy.html %}

## 請求本文中的註解

JSON 請求本文可包含 `/* */` 或 `//` 格式的註解。註解在您儲存並重複使用的請求中很有用，例如索引範本或元件範本定義。OpenSearch 在剖析請求時會移除註解，因此註解不會被儲存，也不會由 Get Index Template API 等 API 傳回。

下列請求會建立一個本文包含註解的索引範本：

```json
PUT /_index_template/comment-test
{
  /* Applies to all daily log indexes */
  "index_patterns": ["comment-logs-*"],
  "template": {
    "settings": {
      "number_of_replicas": 0 // Single-node cluster
    }
  }
}
```
{% include copy-curl.html %}

若您使用 cURL 從檔案傳送包含 `//` 註解的請求本文，請使用 `--data-binary` 選項。`-d` 選項會移除檔案輸入中的換行，因此 `//` 註解會將本文其餘部分變成註解。
{: .tip}

## 查詢字串中的請求本文

有些 HTTP 用戶端無法在 `GET` 請求中傳送本文。在這種情況下，請將本文放入 `source` 查詢參數，並將 `source_content_type` 設為其媒體類型，例如 `application/json`。OpenSearch 會拒絕包含 `source` 但沒有 `source_content_type` 的請求。

下列請求會在 `orders-online` 索引中搜尋包含 `product` 欄位的文件：

```json
GET /orders-online/_search?source={"query":{"exists":{"field":"product"}}}&source_content_type=application/json
```

當您使用 cURL 或其他 HTTP 用戶端傳送此請求時，請對 `source` 值進行 URL 編碼。

## 堆疊追蹤

根據預設，錯誤回應不會包含例外狀況的 Java 堆疊追蹤。若要在疑難排解時包含堆疊追蹤，請在請求 URL 中加入 `error_trace=true`。回應接著會包含錯誤及其每個原因的 `stack_trace` 欄位。

下列請求會搜尋不存在的索引，並傳回附有堆疊追蹤的錯誤：

```json
GET /no-such-index/_search?error_trace=true
```
{% include copy-curl.html %}

## 篩選後的回應

若要縮小回應大小，請使用 `filter_path` 參數指定要傳回哪些欄位。傳遞給 `filter_path` 一個或多個以點分隔的欄位路徑，並以逗號分隔。例如，下列請求只會傳回搜尋時間、總命中數，以及每個命中的索引：

```json
GET /sales-*/_search?q=region:west&filter_path=took,hits.total.value,hits.hits._index
```
{% include copy-curl.html %}

回應只包含所要求的欄位：

```json
{
  "took": 13,
  "hits": {
    "total": {
      "value": 2
    },
    "hits": [
      {
        "_index": "sales-2026-10"
      },
      {
        "_index": "sales-2026-09"
      }
    ]
  }
}
```

篩選器支援下列語法：

- `*` 會比對任何欄位名稱或欄位名稱的一部分。例如，`metadata.indices.sales-*.state` 會傳回名稱開頭為 `sales-` 的每個索引狀態。
- `**` 會比對任意層數的路徑，因此您可以在不知道完整路徑的情況下選取欄位。例如，在 Nodes Stats API 回應中，`nodes.**.heap_used_percent` 會傳回每個節點的堆積使用量，而該值巢狀於節點 ID、`jvm` 與 `mem` 物件之下。
- 以 `-` 開頭的篩選器會排除相符的欄位。

當您合併包含性與排除性篩選器時，OpenSearch 會先套用排除性篩選器，再套用包含性篩選器。下列請求會傳回命中，但從每個命中中移除 `_index` 與 `_score` 欄位：

```json
GET /sales-*/_search?q=region:west&filter_path=hits.hits,-hits.hits._index,-hits.hits._score
```
{% include copy-curl.html %}

回應包含每個命中的 ID 與來源：

```json
{
  "hits": {
    "hits": [
      {
        "_id": "4xWKNqEBmqWRVflA9hH6",
        "_source": {
          "region": "west",
          "amount": 950
        }
      },
      {
        "_id": "4hWKNqEBmqWRVflA9hGr",
        "_source": {
          "region": "west",
          "amount": 1200
        }
      }
    ]
  }
}
```

`filter_path` 參數會將 `_source` 整體傳回，無法在其中選取欄位。若只要傳回部分文件欄位，請將 `filter_path` 與[來源篩選]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/retrieve-specific-fields/#using-source-filtering)合併使用。下列請求只會傳回每個命中的 ID 與 `amount` 欄位：

```json
GET /sales-*/_search?q=region:west&filter_path=hits.hits._id,hits.hits._source&_source_includes=amount
```
{% include copy-curl.html %}

回應包含每份文件來源中的 `amount` 欄位：

```json
{
  "hits": {
    "hits": [
      {
        "_id": "4xWKNqEBmqWRVflA9hH6",
        "_source": {
          "amount": 950
        }
      },
      {
        "_id": "4hWKNqEBmqWRVflA9hGr",
        "_source": {
          "amount": 1200
        }
      }
    ]
  }
}
```

## 扁平化設定

會傳回設定的 API（例如 Get Settings API）預設會以巢狀物件傳回設定。若要將每個設定以點標記法傳回為單一鍵，例如 `index.number_of_shards`，請在請求 URL 中加入 `flat_settings=true`。扁平化設定較容易搜尋，也較容易複製到其他請求中。

下列請求會以扁平格式傳回 `orders-online` 索引的設定：

```json
GET /orders-online/_settings?flat_settings=true
```
{% include copy-curl.html %}

回應會為每個設定包含一個鍵：

```json
{
  "orders-online": {
    "settings": {
      "index.creation_date": "1791912174739",
      "index.number_of_replicas": "0",
      "index.number_of_shards": "1",
      "index.provided_name": "orders-online",
      "index.replication.type": "DOCUMENT",
      "index.uuid": "-m06DdVxT72bWledrDZ8sA",
      "index.version.created": "137307827"
    }
  }
}
```

<!-- vale off -->
## X-Opaque-Id 標頭
<!-- vale on -->

您可以使用 `X-Opaque-Id` 標頭為任何請求指定不透明的識別碼。OpenSearch 會使用此識別碼來追蹤工作、在伺服器端記錄檔中去除重複的棄用警告，以及區分對您的叢集傳送請求的呼叫方。請勿為每個請求指定唯一值。

下列請求會為請求加入不透明的 ID：

```bash
curl -H "X-Opaque-Id: my-curl-client-1" -XGET localhost:9200/_tasks
```
{% include copy.html %}

<!-- vale off -->
## X-Request-Id 標頭
<!-- vale on -->

您可以使用 `X-Request-Id` 標頭為搜尋請求指定唯一識別碼。此識別碼用於追蹤個別搜尋請求，並可在記錄檔（例如慢速記錄檔）中參照，以供疑難排解與分析。此值必須是 32 個字元的十六進位字串。

下列請求會為搜尋請求加入請求 ID：

```bash
curl -X GET "http://localhost:9200/_search" \
  -H "Content-Type: application/json" \
  -H "X-Request-Id: 19d538d7c42d09240be001d1e4ff6201" \
  -d '{"query": {"match_all": {}}}'
```
{% include copy.html %}

## 相關文件

- [索引名稱語法]({{site.url}}{{site.baseurl}}/api-reference/index-name-syntax/)
- [支援的單位]({{site.url}}{{site.baseurl}}/api-reference/units/)
- [Cron 運算式]({{site.url}}{{site.baseurl}}/api-reference/cron-expressions/)
- [範圍查詢中的日期運算]({{site.url}}{{site.baseurl}}/query-dsl/term/range/)
- [模糊度]({{site.url}}{{site.baseurl}}/query-dsl/fuzziness/)
