---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "串流大量作業"
parent: Document APIs
nav_order: 25
redirect_from:
 - /opensearch/rest-api/document-apis/bulk/streaming/
---

# 串流大量作業 API
**2.17.0 版新增**
{: .label .label-purple }

這是一項實驗性功能，不建議在正式環境中使用。若要了解此功能的進度或提供意見回饋，請參閱相關的 [GitHub issue](https://github.com/opensearch-project/OpenSearch/issues/9065)。    
{: .warning}

串流大量作業 (streaming bulk) 讓您以串流方式傳送請求，並以串流回應取得結果，藉此新增、更新或刪除多份文件。相較於傳統的 [Bulk API]({{site.url}}{{site.baseurl}}/api-reference/document-apis/bulk/)，串流匯入 (streaming ingestion) 免去估算批次大小的需要 (批次大小會受到叢集在任何時間點的運作狀態影響)，並且能在多個用戶端與叢集之間自然地施加背壓 (backpressure)。串流可透過 HTTP/2 或 HTTP/1.1 (使用分塊傳輸編碼 (chunked transfer encoding)) 運作，視用戶端與叢集所支援的功能而定。

預設的 HTTP 傳輸方式不支援串流。您必須安裝 [`transport-reactor-netty4`]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/network-settings/#selecting-the-transport) HTTP 傳輸外掛程式，並將其用作預設的 HTTP 傳輸層。`transport-reactor-netty4` 外掛程式與串流大量作業 API 皆為實驗性功能。
{: .note}

## 端點

```json
POST _bulk/stream
POST {index}/_bulk/stream
```

如果您在路徑中指定索引，就不需要在[請求本文區塊]({{site.url}}{{site.baseurl}}/api-reference/document-apis/bulk/#request-body)中包含索引。

OpenSearch 也接受對 `_bulk/stream` 路徑的 PUT 請求，但我們強烈建議使用 POST。PUT 的公認用途 (在指定路徑上新增或取代單一資源) 對串流大量作業請求而言並不合理。
{: .note }


## 查詢參數

下表列出可用的查詢參數。所有查詢參數皆為選用。

參數 | 資料類型 | 說明
:--- | :--- | :---
`pipeline` | 字串 | 用於預先處理文件的管線 ID。
`refresh` | Enum | 執行編製索引作業後，是否重新整理受影響的分片。預設為 `false`。`true` 會使變更立即顯示在搜尋結果中，但會降低叢集效能。`wait_for` 會等待重新整理。請求需要較長時間才會傳回，但不會降低叢集效能。
`require_alias` | 布林值 | 設為 `true` 時，要求所有動作都以索引別名而非索引為目標。預設為 `false`。
`routing` | 字串 | 適用於未指定自身路由之作業的預設路由值。
`timeout` | Time | 等待請求傳回的時間長度。預設為 `1m`。
`wait_for_active_shards` | 字串 | 指定在 OpenSearch 處理大量請求之前，必須可用的作用中分片數量。預設為 `1`（僅主要分片）。可設為 `all` 或正整數。大於 1 的值需要副本。例如，若您指定的值為 3，索引必須有 2 個副本分散在另外 2 個節點上，請求才能成功。
`batch_interval` | Time | 指定在將批次傳送至資料節點之前，應將大量作業累積成批次的時間長度。必須大於 0。若未指定，則不會依時間將作業分批。
`batch_size` | 整數 | 指定在將批次傳送至資料節點之前，應將多少個大量作業累積成一個批次。必須大於 0。預設為 `1`。
{% comment %}_source | List | asdf
`_source_excludes` | List | asdf
`_source_includes` | List | asdf{% endcomment %}

## 請求本文欄位

串流大量作業 API 的請求本文與 [Bulk API 請求本文]({{site.url}}{{site.baseurl}}/api-reference/document-apis/bulk/#request-body)完全相容，其中每個大量作業 (create/index/update/delete) 會以個別區塊傳送。  

## 範例請求

```json
curl -X POST "http://localhost:9200/_bulk/stream" -H "Transfer-Encoding: chunked" -H "Content-Type: application/json" -d'
{ "delete": { "_index": "movies", "_id": "tt2229499" } }
{ "index": { "_index": "movies", "_id": "tt1979320" } }
{ "title": "Rush", "year": 2013 }
{ "create": { "_index": "movies", "_id": "tt1392214" } }
{ "title": "Prisoners", "year": 2013 }
{ "update": { "_index": "movies", "_id": "tt0816711" } }
{ "doc" : { "title": "World War Z" } }
'
```
{% include copy.html %}

## 回應範例

根據批次設定，每個串流回應區塊可能會回報一個或多個（批次）大量操作的結果。OpenSearch 會針對收到的每個 HTTP 區塊傳回結果，因此回應區塊的數量也取決於用戶端如何分割請求串流。

以下回應假設 ID 為 `tt1392214` 的文件已存在於 `movies` 索引中，因此 `create` 操作會導致版本衝突。ID 為 `tt2229499` 和 `tt0816711` 的文件不存在，因此 `delete` 操作會傳回 `not_found`，而 `update` 操作會失敗。對於前述未使用批次處理（預設）的請求，串流回應可能如下所示：

```json
{"took": 4, "errors": false, "items": [ { "delete": { "_index": "movies", "_id": "tt2229499", "_version": 1, "result": "not_found", "_shards": { "total": 2, "successful": 1, "failed": 0 }, "_seq_no": 1, "_primary_term": 1, "status": 404 } } ] }
{"took": 11, "errors": false, "items": [ { "index": { "_index": "movies", "_id": "tt1979320", "_version": 1, "result": "created", "_shards": { "total": 2, "successful": 1, "failed": 0 }, "_seq_no": 2, "_primary_term": 1, "status": 201 } } ] }
{"took": 2, "errors": true, "items": [ { "create": { "_index": "movies", "_id": "tt1392214", "status": 409, "error": { "type": "version_conflict_engine_exception", "reason": "[tt1392214]: version conflict, document already exists (current version [1])", "index": "movies", "shard": "0", "index_uuid": "yhizhusbSWmP0G7OJnmcLg" } } } ] }
{"took": 4, "errors": true, "items": [ { "update": { "_index": "movies", "_id": "tt0816711", "status": 404, "error": { "type": "document_missing_exception", "reason": "[tt0816711]: document missing", "index": "movies", "shard": "0", "index_uuid": "yhizhusbSWmP0G7OJnmcLg" } } } ] }
```
