---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "並行分段搜尋"
parent: Improving search performance
nav_order: 20
---

# 並行分段搜尋

使用並行分段搜尋，在查詢階段以平行方式搜尋分段。並行分段搜尋可改善搜尋延遲的情況包括下列幾種：

- 傳送長時間執行的請求時，例如包含彙總或大範圍的請求
- 作為強制將分段合併為單一分段的替代方案，以改善效能

## 背景

在 OpenSearch 中，每個搜尋請求都遵循分散-聚集 (scatter-gather) 通訊協定。協調節點會接收搜尋請求，評估需要哪些分片來處理此請求，並將分片層級的搜尋請求傳送給這些分片。每個收到請求的分片會使用 Lucene 在本機執行請求並傳回結果。協調節點會合併從所有分片收到的回應，並將搜尋回應傳回給用戶端。此外，如果用戶端要求任何文件欄位或整份文件做為回應的一部分，協調節點可以選擇在將最終結果傳回給用戶端之前執行擷取階段。

## 並行搜尋分段

若未使用並行分段搜尋，Lucene 會在查詢階段依序對每個分片上的所有分段執行請求。查詢階段接著會收集搜尋請求中排名最前的命中結果。使用並行分段搜尋時，每個分片層級的請求會在查詢階段以平行方式搜尋分段。對於每個分片，分段會分割成多個_配量_ (slice)。每個配量是可在個別執行緒上平行執行的工作單位，因此配量數量會決定分片層級請求的最大平行度。一旦所有配量完成其工作，Lucene 會對配量執行縮減作業，將其合併並為此分片層級請求建立最終結果。配量會使用新的 `index_searcher` 執行緒集區執行，這與處理分片層級請求的 `search` 執行緒集區不同。

## 在索引或叢集層級啟用並行分段搜尋

從 OpenSearch 3.0 版開始，並行分段搜尋預設會在叢集層級啟用。預設的並行分段搜尋模式為 `auto`。升級後，彙總工作負載可能會遇到 CPU 使用率增加的情況。我們建議監視叢集的資源使用情形，並視需要調整基礎架構容量，以維持最佳效能。
{: .important}

若要在叢集上設定並行分段搜尋，請使用 `search.concurrent_segment_search.mode` 設定。較舊的 `search.concurrent_segment_search.enabled` 設定將在未來版本中淘汰，改用新的設定。

您可以在兩個層級啟用並行分段搜尋：

- 叢集層級
- 索引層級

索引層級設定優先於叢集層級設定。因此，如果叢集設定已啟用，但索引設定已停用，則該索引的並行分段搜尋將會停用。因此，除非明確設定索引層級設定，否則不會評估該設定，無論為該設定設定的預設值為何。您可以呼叫 [Index Settings API]({{site.url}}{{site.baseurl}}/api-reference/index-apis/get-settings/) 並省略 `?include_defaults` 查詢參數，以擷取索引層級設定的目前值。
{: .note}

叢集層級與索引層級的 `search.concurrent_segment_search.mode` 設定皆接受下列值：

- `auto` (預設)：在此模式中，OpenSearch 會使用可外掛的_並行搜尋決策器_ (concurrent search decider)，根據查詢評估及請求中是否有彙總，決定搜尋請求要使用並行或循序路徑。根據預設，如果沒有任何外掛程式設定決策器，則會根據請求中是否有彙總來決定是否使用並行搜尋。如需可外掛決策器語意的詳細資訊，請參閱[可外掛的並行搜尋決策器](#pluggable-concurrent-search-deciders-concurrentsearchrequestdecider)。 

- `all`：為所有搜尋請求啟用並行分段搜尋。這相當於將 `search.concurrent_segment_search.enabled` 設為 `true`。 

- `none`：為所有搜尋請求停用並行分段搜尋，實際上會關閉此功能。這相當於將 `search.concurrent_segment_search.enabled` 設為 `false`。

若要為叢集中每個索引的所有搜尋請求啟用並行分段搜尋，請傳送下列請求：

```json
PUT _cluster/settings
{
   "persistent":{
      "search.concurrent_segment_search.mode": "all"
   }
}
```
{% include copy-curl.html %}

若要為特定索引的所有搜尋請求啟用並行分段搜尋，請在端點中指定索引名稱：

```json
PUT {index-name}/_settings
{
    "index.search.concurrent_segment_search.mode": "all"
}
```
{% include copy-curl.html %}

您可以繼續使用現有的 `search.concurrent_segment_search.enabled` 設定，為叢集中的所有索引啟用並行分段搜尋，如下所示：
```json
PUT _cluster/settings
{
   "persistent":{
      "search.concurrent_segment_search.enabled": true
   }
}
```
{% include copy-curl.html %}

若要為特定索引啟用並行分段搜尋，請在端點中指定索引名稱：

```json
PUT {index-name}/_settings
{
    "index.search.concurrent_segment_search.enabled": true
}
```
{% include copy-curl.html %}


評估叢集是否已啟用並行分段搜尋時，`search.concurrent_segment_search.mode` 設定優先於 `search.concurrent_segment_search.enabled` 設定。
如果未明確設定 `search.concurrent_segment_search.mode` 設定，則會評估 `search.concurrent_segment_search.enabled` 設定，以判斷是否啟用並行分段搜尋。

從指定較舊 `search.concurrent_segment_search.enabled` 設定的較早版本升級叢集時，此設定將繼續生效。不過，一旦設定 `search.concurrent_segment_search.mode`，它就會覆寫先前的設定，並根據指定的模式啟用或停用並行搜尋。
我們建議在您設定 `search.concurrent_segment_search.mode` 之後，將叢集上的 `search.concurrent_segment_search.enabled` 設為 `null`：

```json
PUT _cluster/settings
{
   "persistent":{
      "search.concurrent_segment_search.enabled": null
   }
}
```
{% include copy-curl.html %}

若要為特定索引停用舊設定，請在端點中指定索引名稱：
```json
PUT {index-name}/_settings
{
    "index.search.concurrent_segment_search.enabled": null
}
```
{% include copy-curl.html %}

## 配量機制

您可以選擇兩種可用的機制之一，將分段指派給配量：預設的[最大配量數機制](#the-max-slice-count-mechanism)或 [Lucene 機制](#the-lucene-mechanism)。

### 最大配量數機制

_最大配量數_機制是一種配量機制，使用可動態設定的最大配量數，並以循環方式將分段依序分配給各配量。當最上層分片請求已經太多，而您想要限制每個請求的配量數以減少配量之間的競爭時，這會很有用。

從 OpenSearch 3.0 版開始，並行分段搜尋預設使用最大配量數機制。最大配量數會在叢集啟動時使用公式 `Math.max(1, Math.min(Runtime.getRuntime().availableProcessors() / 2, 4))` 計算。您可以明確設定叢集層級或索引層級的 `max_slice_count` 參數來覆寫此值。如需更新 `max_slice_count` 的詳細資訊，請參閱[設定配量機制](#setting-the-slicing-mechanism)。若要還原為預設計算值，請將 `max_slice_count` 設為 `null`。 

### Lucene 機制

Lucene 機制是最大配量數機制的替代方案。預設情況下，Lucene 會為分片中的每個配量指派最多 250K 份文件或 5 個分段（以先達到者為準）。例如，假設有一個包含 11 個分段的分片。前 5 個分段各有 250K 份文件，接下來的 6 個分段各有 20K 份文件。前 5 個分段會各自被指派到一個配量，因為它們各自包含配量允許的最大文件數。接著，接下來的 5 個分段會全部被指派到另一個單一配量，因為達到了配量允許的最大分段數。第 11 個分段會被指派到一個獨立的配量。

### 設定配量機制

您可以透過更新 `search.concurrent.max_slice_count` 設定，在叢集層級或索引層級設定配量機制。

叢集層級與索引層級的 `search.concurrent.max_slice_count` 設定都可以接受以下有效值：

- 正整數：使用最大目標配量數機制。通常，2 到 8 之間的值應該就足夠了。
- `0`：使用 Lucene 機制。

若要為叢集中的所有索引設定配量數，請使用以下動態叢集設定：

```json
PUT _cluster/settings
{
   "persistent":{
      "search.concurrent.max_slice_count": 2
   }
}
```
{% include copy-curl.html %}

若要為特定索引設定配量數，請在端點中指定索引名稱：

```json
PUT {index-name}/_settings
{
    "index.search.concurrent.max_slice_count": 2
}
```
{% include copy-curl.html %}

## 一般準則

並行分段搜尋有助於提升搜尋請求的效能，但代價是消耗更多資源，例如 CPU 或 JVM heap。測試您的工作負載以了解叢集是否為並行分段搜尋正確調整規模，這一點非常重要。我們建議遵循以下並行分段搜尋準則：

* 從配量數 2 開始，並測量工作負載的效能。如果資源使用率超過建議值，請考慮擴充您的叢集。根據我們的測試，我們觀察到如果您的工作負載已經消耗超過 50% 的 CPU 資源，則您需要為並行分段搜尋擴充叢集。
* 如果您的配量數為 2，且叢集中仍有可用資源，則可以將配量數增加到更高的數字，例如 4 或 6，同時監控叢集中的搜尋延遲和資源使用率。
* 當許多用戶端同時並行傳送搜尋請求時，較低的配量數通常效果較好。這會反映在 CPU 使用率上，因為較多的用戶端會導致每秒更多的查詢，進而轉化為更高的資源使用量。

升級至 OpenSearch 3.0 時，請注意包含彙總的工作負載可能會遇到較高的 CPU 使用率，因為在 `auto` 模式下預設會啟用並行搜尋。如果您的 OpenSearch 2.x 叢集在執行彙總工作負載時 CPU 使用率超過 25%，請在升級前考慮以下選項：

- 規劃擴充叢集資源，以因應增加的 CPU 需求。
- 如果擴充對您的使用案例不可行，請準備停用並行搜尋。

## 限制

以下彙總不支援並行搜尋模型。如果搜尋請求包含其中一種彙總，即使已在叢集層級或索引層級啟用並行分段搜尋，該請求仍會以非並行路徑執行。
- [join]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/join/) 欄位上的父彙總。如需更多資訊，請參閱[此 GitHub issue](https://github.com/opensearch-project/OpenSearch/issues/9316)。
- `sampler` 與 `diversified_sampler` 彙總。如需更多資訊，請參閱[此 GitHub issue](https://github.com/opensearch-project/OpenSearch/issues/11075)。

## 其他注意事項

以下章節提供並行分段搜尋的其他注意事項。

### `terminate_after` 搜尋參數

[`terminate_after` 搜尋參數]({{site.url}}{{site.baseurl}}/api-reference/search/#query-parameters)用於在收集到指定數量的相符文件後終止搜尋請求。如果您在請求中包含 `terminate_after` 參數，並行分段搜尋將被停用，且該請求會以非並行方式執行。

一般而言，查詢會搭配較小的 `terminate_after` 值使用，因此能快速完成，因為搜尋是在較小的資料集上執行。因此，在這種情況下，並行搜尋可能無法進一步提升效能。此外，當 `terminate_after` 與其他搜尋請求參數（例如 `track_total_hits` 或 `size`）一起使用時，會增加複雜性並改變預期的查詢行為。對包含 `terminate_after` 的搜尋請求改用非並行路徑，可確保並行與非並行請求之間的結果一致。

### 排序

根據分段的資料布局，排序最佳化功能可以根據最小值與最大值以及先前收集的值，修剪整個分段。如果前幾個分段中存在排序最前的值，而所有其他分段都被修剪，則使用並行分段搜尋進行排序時，查詢延遲可能會增加。相反地，如果最後幾個分段包含排序最前的值，則並行分段搜尋可能會改善延遲。

### Terms 彙總

非並行搜尋會計算文件計數誤差，並在 `doc_count_error_upper_bound` 回應參數中傳回。在並行分段搜尋期間，`shard_size` 參數會套用於分段配量層級。因此，並行搜尋可能會引入額外的文件計數誤差。

如需 `shard_size` 如何影響 `doc_count_error_upper_bound` 與已收集桶的更多資訊，請參閱[此 GitHub issue](https://github.com/opensearch-project/OpenSearch/issues/11680#issuecomment-1885882985)。


## 開發人員資訊

以下章節提供開發人員的其他資訊。

### AggregatorFactory 變更

由於實作細節的限制，並非所有彙總類型都能支援並行分段搜尋。為了因應這一點，我們在 `AggregatorFactory` 類別中引入了 [`supportsConcurrentSegmentSearch()`](https://github.com/opensearch-project/OpenSearch/blob/2.x/server/src/main/java/org/opensearch/search/aggregations/AggregatorFactory.java#L123) 方法，用於指出特定彙總類型是否支援並行分段搜尋。預設情況下，此方法會傳回 `false`。任何需要支援並行分段搜尋的彙總器，都必須在其自身的工廠實作中覆寫此方法。

為確保以自訂外掛程式實作的 `Aggregator` 能與並行搜尋路徑正常運作，外掛程式開發人員可以在啟用並行搜尋的情況下驗證其實作，然後更新外掛程式以覆寫 [`supportsConcurrentSegmentSearch()`](https://github.com/opensearch-project/OpenSearch/blob/2.x/server/src/main/java/org/opensearch/search/aggregations/AggregatorFactory.java#L123) 方法並傳回 `true`。

### 可外掛的並行搜尋決策器：ConcurrentSearchRequestDecider

於 2.17 版推出
{: .label .label-purple }

外掛程式開發人員可以擴充 [`ConcurrentSearchRequestDecider`](https://github.com/opensearch-project/OpenSearch/blob/2.x/server/src/main/java/org/opensearch/search/deciders/ConcurrentSearchRequestDecider.java)，並透過 [`SearchPlugin#getConcurrentSearchRequestFactories()`](https://github.com/opensearch-project/OpenSearch/blob/2.x/server/src/main/java/org/opensearch/plugins/SearchPlugin.java#L148) 註冊其工廠，來自訂 `auto` 模式的並行搜尋決策。只有在請求不屬於[限制](#limitations)與[其他考量](#other-considerations)章節所列的任何類別時，才會評估這些決策器。如需決策器實作的詳細資訊，請參閱[對應的 GitHub 問題](https://github.com/opensearch-project/OpenSearch/issues/15259)。
搜尋請求會使用 `QueryBuilderVisitor` 進行剖析，其會針對搜尋請求中 `QueryBuilder` 樹狀結構的每個節點，呼叫所有已設定決策器的 [`ConcurrentSearchRequestDecider#evaluateForQuery()`](https://github.com/opensearch-project/OpenSearch/blob/2.x/server/src/main/java/org/opensearch/search/deciders/ConcurrentSearchRequestDecider.java#L36) 方法。最終的並行搜尋決策，是結合 [`ConcurrentSearchRequestDecider#getConcurrentSearchDecision()`](https://github.com/opensearch-project/OpenSearch/blob/2.x/server/src/main/java/org/opensearch/search/deciders/ConcurrentSearchRequestDecider.java#L44) 方法所傳回之每個決策器的決策而得。
