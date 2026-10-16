---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "搜尋"
parent: Search APIs
nav_order: 10
redirect_from:
  - /opensearch/rest-api/search/
  - /api-reference/search/
---

# 搜尋 API
**1.0 版新增**
{: .label .label-purple }

搜尋 API 操作可讓您在叢集中搜尋資料。

## 端點

```json
GET /{index}/_search
GET /_search

POST /{index}/_search
POST /_search
```

## 查詢參數

許多參數僅在您使用 URL `q=` 參數或 `query_string` 查詢時適用。如需更多資訊，請參閱[查詢字串查詢]({{site.url}}{{site.baseurl}}/query-dsl/full-text/query-string/)。
{: .note}

下表列出可用的查詢參數。所有查詢參數皆為選用。

參數 | 類型 | 說明
:--- | :--- | :---
`allow_no_indices` | 布林值 | 是否忽略不符合任何索引的萬用字元。預設為 `true`。範例：`GET test-index-*/_search?allow_no_indices=true`。如需詳細資訊，請參閱[指定多個索引]({{site.url}}{{site.baseurl}}/api-reference/index-name-syntax/#targeting-multiple-indexes)。 |
`allow_partial_search_results` | 布林值 | 若請求發生錯誤或逾時，是否傳回部分結果。預設為 `true`。範例：`GET test-index/_search?allow_partial_search_results=false`。 |
`analyzer` | 字串 | 查詢字串中要使用的分析器。需要 `q=` 或 `query_string` 本文。範例：`GET test-index/_search?q=title:test&analyzer=standard`。如需詳細資訊，請參閱[文字分析]({{site.url}}{{site.baseurl}}/analyzers/)。 |
`analyze_wildcard` | 布林值 | 是否分析查詢字串中的萬用字元查詢和前綴查詢。預設為 `false`。需要 `q=` 或 `query_string`。範例：`GET test-index/_search?q=title:te*&analyze_wildcard=true`。 |
`batched_reduce_size` | 整數 | 在傳回最終搜尋結果之前，於協調節點上合併為一個批次的分片結果數量。此參數會限制一起處理的分片結果數量，有助於在搜尋請求涵蓋許多分片時降低記憶體使用量。預設為 `512`。範例：`GET test-index/_search?batched_reduce_size=2`。 |
`cancel_after_time_interval` | 時間 | 搜尋請求被取消前的時間。請求層級參數的優先順序高於 `cancel_after_time_interval` [叢集設定]({{site.url}}{{site.baseurl}}/api-reference/cluster-api/cluster-settings/)。預設為 `-1`。範例：`GET test-index/_search?cancel_after_time_interval=10ms`。 |
`ccs_minimize_roundtrips` | 布林值 | 是否盡量減少節點與遠端叢集之間的往返次數。預設為 `true`。範例：`GET test-index/_search?ccs_minimize_roundtrips=true`。 |
`default_operator` | 字串 | 字串查詢的預設運算子。有效值為 `AND` 和 `OR`。預設為 `OR`。需要 `q=` 或 `query_string`。範例：`GET test-index/_search?q=title:test one&default_operator=AND`。 |
`df` | 字串 | 查詢字串中未提供欄位前綴時使用的預設欄位。需要 `q=` 或 `query_string`。範例：`GET test-index/_search?q=test&df=title`。 |
`docvalue_fields` | 字串 | 以逗號分隔的欄位清單，這些欄位的值應從其 doc values 表示法傳回。Doc values 是一種經過最佳化的單欄式格式，可提升彙總、排序和指令碼的效能。範例：`GET test-index/_search?docvalue_fields=ts,views`。如需詳細資訊，請參閱[使用 doc value 欄位進行搜尋]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/retrieve-specific-fields/#searching-with-doc-value-fields)。 |
`expand_wildcards` | 字串 | 指定萬用字元運算式可比對的索引類型。支援以逗號分隔的值。<br> 有效值為：<br> - `all`：比對任何索引，包括隱藏索引。<br> - `closed`：比對已關閉的非隱藏索引。<br> - `hidden`：比對隱藏索引。必須與 `open`、`closed` 或兩者合併使用。<br> - `none`：不接受萬用字元運算式。<br> - `open`：比對開啟的非隱藏索引。<br> 預設為 `open`。範例：`GET test-index-*/_search?expand_wildcards=open`。如需詳細資訊，請參閱[指定多個索引]({{site.url}}{{site.baseurl}}/api-reference/index-name-syntax/#targeting-multiple-indexes)。 |
`explain` | 布林值 | 若為 `true`，則傳回 OpenSearch 如何計算每份文件相關性分數的詳細資訊。預設為 `false`。僅在搜尋回應中包含 `hits` 時適用。範例：`GET test-index/_search?explain=true&size=1&q=title:test`。如需詳細資訊，請參閱 [Explain API]({{site.url}}{{site.baseurl}}/api-reference/search-apis/explain/)。 |
`from` | 整數 | 傳回結果前要略過的命中數。與 `size` 搭配使用以將結果分頁。預設為 `0`。範例：`GET test-index/_search?from=5&size=5`。如需詳細資訊，請參閱[from 和 size 參數]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/paginate/#the-from-and-size-parameters)。 |
`ignore_throttled` | 布林值 | 是否忽略已凍結的具體索引、展開的索引或具有別名的索引。預設為 `true`。範例：`GET test-index/_search?ignore_throttled=true`。 |
`ignore_unavailable` | 布林值 | 若為 `true`，OpenSearch 會在搜尋期間忽略遺失或已關閉的索引以及無法使用的分片。若為 `false`，則指定遺失或已關閉的索引時，請求會傳回錯誤。預設為 `false`。範例：`GET test-index-*/_search?ignore_unavailable=true`。如需詳細資訊，請參閱[指定多個索引]({{site.url}}{{site.baseurl}}/api-reference/index-name-syntax/#targeting-multiple-indexes)。 |
`include_named_queries_score` | 布林值 | 是否針對每個命中傳回具名查詢（具有 `_name` 的查詢）的分數貢獻。預設為 `false`。需要使用 `_name` 命名的查詢。範例：`POST test-index/_search?include_named_queries_score=true {"size":1,"query":{"match":{"title":{"query":"test","_name":"q1"}}}}`。如需詳細資訊，請參閱[具名查詢]({{site.url}}{{site.baseurl}}/query-dsl/named-queries/)。 |
`lenient` | 布林值 | 當查詢有格式錯誤時（例如，使用文字查詢數值欄位），OpenSearch 是否應接受請求，而不傳回錯誤。預設為 `false`。需要 `q=` 或 `query_string`。範例：`GET test-index/_search?q=views:abc&lenient=true`。 |
`max_concurrent_shard_requests` | 整數 | 此請求在每個節點上應執行的並行分片請求數上限。預設為 `5`。範例：`GET test-index/_search?max_concurrent_shard_requests=2`。 |
`node_level_query_fanout` | 布林值 | 是否對此搜尋請求使用節點層級查詢扇出；若有提供，會覆寫 `search.node_level_query_fanout.enabled` 叢集設定。節點層級查詢扇出會依目標資料節點，將分片層級的 `query_then_fetch` 查詢和 `can_match` 請求分組。預設為 `false`。範例：`POST index1/_search?node_level_query_fanout=true`。 |
`phase_took` | 布林值 | 是否在回應中傳回階段層級的 `took` 時間值。預設為 `false`。範例：`GET test-index/_search?phase_took=true`。 |
`pre_filter_shard_size` | 整數 | 在搜尋分片上觸發預先篩選作業的預先篩選大小閾值。若搜尋請求展開後的分片數超過此值，OpenSearch 會執行預先篩選作業，根據查詢重寫排除無法比對到文件的分片。預設為 `128`。範例：`GET test-index/_search?pre_filter_shard_size=1`。 |
`preference` | 字串 | 指定 OpenSearch 應在哪些分片或節點上執行搜尋。範例：`GET test-index/_search?preference=_local`。如需有效值，請參閱[preference 查詢參數]({{site.url}}{{site.baseurl}}/api-reference/search-apis/search/#the-preference-query-parameter)。 |
`q` | 字串 | Lucene 查詢字串查詢。啟用查詢字串輔助參數。優先順序高於請求本文中的 `query` 參數。若兩者皆有指定，則只會傳回符合此參數的文件；請求本文中的查詢會被忽略。範例：`GET test-index/_search?q=title:test&size=5`。如需詳細資訊，請參閱[查詢字串查詢]({{site.url}}{{site.baseurl}}/query-dsl/full-text/query-string/)。 |
`request_cache` | 布林值 | 若指定 `size=0`，OpenSearch 是否應對請求使用搜尋結果快取。預設為索引層級的 `request_cache` 設定。範例：`GET test-index/_search?request_cache=true`。如需詳細資訊，請參閱[索引請求快取]({{site.url}}{{site.baseurl}}/search-plugins/caching/request-cache/)。 |
`rest_total_hits_as_int` | 布林值 | 是否以整數傳回 `hits.total`。否則會傳回物件。預設為 `false`。與設為 `true` 的 `track_total_hits` 搭配使用。範例：`GET test-index/_search?track_total_hits=true&rest_total_hits_as_int=true`。 |
`routing` | 字串 | 用於將搜尋路由至特定分片的自訂值。範例：`GET test-index/_search?routing=user-42`。如需詳細資訊，請參閱[路由]({{site.url}}{{site.baseurl}}/mappings/metadata-fields/routing/)。 |
`scroll` | 時間 | 保持搜尋內容開啟的時間長度。需要大於 `0` 的 `size` 以及後續的 `_search/scroll`。範例：`GET test-index/_search?scroll=1m&size=2`。如需詳細資訊，請參閱[捲動搜尋]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/paginate/#scroll-search)。 |
`search_type` | 字串 | 計算相關性分數時，OpenSearch 是否應使用全域詞彙頻率和文件頻率。有效值為 `query_then_fetch` 和 `dfs_query_then_fetch`。`query_then_fetch` 會使用分片的本機詞彙頻率和文件頻率為文件評分。這通常速度較快，但較不精確。`dfs_query_then_fetch` 會使用所有分片的全域詞彙頻率和文件頻率為文件評分。這通常速度較慢，但較精確。預設為 `query_then_fetch`。範例：`GET test-index/_search?search_type=dfs_query_then_fetch`。 |
`seq_no_primary_term` | 布林值 | 是否傳回每個文件命中最後一次操作的序號和主要分片任期。範例：`GET test-index/_search?seq_no_primary_term=true&size=1&q=title:test`。 |
`size` | 整數 | 要傳回的結果數上限。與 `from` 搭配使用以將結果分頁。預設為 `10`。範例：`GET test-index/_search?size=3`。如需詳細資訊，請參閱[from 和 size 參數]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/paginate/#the-from-and-size-parameters)。 |
`sort` | 清單 | 用於排序的 `<field>:<direction>` 配對清單，以逗號分隔。若依非分數欄位排序時仍需要分數，請使用 `track_scores=true`。範例：`GET test-index/_search?sort=views:desc&track_scores=true&size=3`。如需詳細資訊，請參閱[排序結果]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/sort/)。 |
`_source` | 字串或布林值 | 控制回應中提供的 `_source` 欄位。有效值為 `true`（傳回文件來源）、`false`（不傳回文件來源）和 `<string>`（要傳回的來源中的一或多個欄位，以清單或萬用字元模式提供）。範例：`GET test-index/_search?_source=false&size=1`、`GET test-index/_search?_source=titl*&size=1`、`GET test-index/_search?_source=title,description&size=1`。如需詳細資訊，請參閱[來源篩選](#source-filtering)。 |
`_source_excludes` | 清單 | 要從回應中排除的來源欄位清單，以逗號分隔。若 `_source` 參數為 `false`，則會忽略此參數。範例：`GET test-index/_search?_source_excludes=title&size=1`。如需詳細資訊，請參閱[來源篩選](#source-filtering)。 |
`_source_includes` | 清單 | 要包含在回應中的來源欄位清單，以逗號分隔。若 `_source` 參數為 `false`，則會忽略此參數。範例：`GET test-index/_search?_source_includes=title&size=1`。如需詳細資訊，請參閱[來源篩選](#source-filtering)。 |
`stats` | 字串 | 要與請求建立關聯的[搜尋統計資料群組](#search-stats-groups)清單，以逗號分隔。範例：`GET test-index/_search?stats=group1`。 |
`stored_fields` | 清單 | 要為每個命中傳回的已儲存欄位清單，以逗號分隔。範例：`GET test-index-stored/_search?stored_fields=note&size=1`。如需詳細資訊，請參閱[使用已儲存欄位進行搜尋]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/retrieve-specific-fields/#searching-with-stored-fields)。 |
`suggest_field` | 字串 | 用於詞彙建議的欄位。需要 `suggest_mode`，以及 `suggest_text` 或 `q` 其中之一。若要在請求本文中設定建議，請使用 `suggest` 欄位。如需詳細資訊，請參閱[您是不是要找]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/did-you-mean/)。
`suggest_mode` | 字串 | 搜尋時要使用的模式。有效值為 `always`（根據 `suggest_text` 中的詞彙提供建議）、`popular`（提供在分片上出現文件數多於搜尋詞彙的建議），以及 `missing`（為分片上沒有的詞彙提供建議）。使用 `suggest_field` 時為必要。
`suggest_size` | 整數 | 要傳回的建議數量。需要 `suggest_field` 和 `suggest_mode`。
`suggest_text` | 字串 | OpenSearch 應為其傳回建議的輸入文字。需要 `suggest_field` 和 `suggest_mode`。若省略，OpenSearch 會使用 `q` 的值。
`terminate_after` | 整數 | OpenSearch 在終止請求之前應處理的相符文件（命中）數量上限。預設為 `0`（無上限）。範例：`GET test-index/_search?terminate_after=1&size=10`。 |
`timeout` | 時間 | 作業應等待作用中分片回應的時間長度。預設為 `1m`（1 分鐘）。範例：`GET test-index/_search?timeout=10ms`。 |
`track_scores` | 布林值 | 是否傳回文件分數。預設為 `false`。搭配 `sort` 使用。範例：`GET test-index/_search?sort=views:desc&track_scores=true&size=3`。如需詳細資訊，請參閱[追蹤分數]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/sort/#tracking-scores)。 |
`track_total_hits` | 布林值或整數 | 要計數的相符文件數量。預設為 `10000`。範例：`GET test-index/_search?track_total_hits=2`。如需詳細資訊，請參閱[追蹤總命中數](#track-total-hits)。 |
`typed_keys` | 布林值 | 傳回的彙總和建議詞彙是否應在回應中包含其類型。預設為 `false`。僅適用於彙總或建議器。範例：`POST test-index/_search?typed_keys=true {"size":0,"aggs":{"a":{"terms":{"field":"views"}}}}`。如需詳細資訊，請參閱[在回應中包含建議器類型]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/did-you-mean/#including-suggester-types-in-the-response)。 |
`version` | 布林值 | 是否將文件版本納入為相符項。範例：`GET test-index/_search?version=true&size=1&q=title:test`。 |

### `preference` 查詢參數

`preference` 查詢參數會指定 OpenSearch 應在哪個分片或節點上執行搜尋。以下是有效的值：

- `_primary`：只在主要分片上執行搜尋。
- `_replica`：只在副本分片上執行搜尋。
- `_primary_first`：在主要分片上執行搜尋，但若主要分片無法使用，則容錯移轉至其他可用的分片。
- `_replica_first`：在副本分片上執行搜尋，但若副本分片無法使用，則容錯移轉至其他可用的分片。
- `_local`：若可能，在本機節點的分片上執行搜尋。
- `_prefer_nodes:<node-id-1>,<node-id-2>`：若可能，在指定的節點上執行搜尋。使用以逗號分隔的清單來指定多個節點。
- `_shards:<shard-id-1>,<shard-id-2>`：只在指定的分片上執行搜尋。使用以逗號分隔的清單來指定多個分片。與其他偏好設定合併使用時，`_shards` 偏好設定必須列在最前面。例如，`_shards:1,2|_replica`。
- `_only_nodes:<node-id-1>,<node-id-2>`：只在指定的節點上執行搜尋。使用以逗號分隔的清單來指定多個節點。
- `<string>`：指定要用於搜尋的自訂字串。該字串不能以底線字元 (`_`) 開頭。使用相同自訂字串的搜尋會路由至相同的分片。

## 請求本文

下表列出可用的請求本文欄位。所有請求本文欄位皆為選用。

欄位 | 類型 | 說明
:--- | :--- | :---
`aggregations`, `aggs` | 物件 | 在選用的 `aggregations` 參數（或其簡寫 `aggs`）中，您可以定義任意數量的彙總。每個彙總由其名稱以及 OpenSearch 支援的其中一種彙總類型所定義。如需更多資訊，請參閱[彙總]({{site.url}}{{site.baseurl}}/aggregations/)。
`collapse` | 物件 | 摺疊搜尋結果，使指定欄位的每個值只傳回最上層的文件。如需更多資訊，請參閱[摺疊搜尋結果]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/collapse-search/)。
`derived` | 物件 | 定義衍生欄位，這些欄位在搜尋時由指令碼計算，可像已編製索引的欄位一樣被查詢、彙總及傳回。如需更多資訊，請參閱[衍生欄位]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/derived/)。
`docvalue_fields` | 物件陣列 | 以 `doc_values` 形式傳回的欄位。您可以為傳回的值指定格式（例如日期格式）。對於 `knn_vector` 欄位，支援的格式為 `binary`（預設，Base64 編碼）與 `array`（JSON 數值陣列）。如需更多資訊，請參閱[使用 `docvalue_fields` 擷取向量欄位]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/retrieve-specific-fields/#retrieving-vector-fields-using-docvalue_fields)。
`explain` | 布林值 | 是否傳回 OpenSearch 如何計算文件分數的詳細資訊。預設為 `false`。
`ext` | 物件 | 外掛程式使用的設定，例如搜尋管線處理器。如需更多資訊，請參閱[ext 物件](#the-ext-object)。
`fields` | 陣列 | 每個命中結果的 `fields` 物件中要傳回的欄位。您可以使用萬用字元模式，並為日期欄位指定格式。如需更多資訊，請參閱[擷取特定欄位]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/retrieve-specific-fields/)。
`from` | 整數 | 在傳回結果之前要略過的結果數量。與 `size` 搭配使用以對結果進行分頁。預設為 `0`。如需更多資訊，請參閱[from 和 size 參數]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/paginate/#the-from-and-size-parameters)。
`highlight` | 物件 | 傳回以搜尋詞彙醒目提示的相符文字片段。如需更多資訊，請參閱[醒目提示查詢相符項目]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/highlight/)。
`include_named_queries_score` | 布林值 | 是否傳回具名查詢的分數。
`indices_boost` | 物件陣列 | 提升來自特定索引之文件的 `_score`。每個項目以 `<index>: <boost-multiplier>` 格式指定一個索引與一個提升係數。大於 `1.0` 的提升會增加分數，而介於 `0` 與 `1.0` 之間的提升則會降低分數。
`min_score` | 浮點數 | 文件必須達到才能包含在結果中的最低分數。
`pit` | 物件 | 要搜尋的時間點 (Point in Time, PIT)。搜尋 PIT 時，請勿在請求路徑中指定索引。如需更多資訊，請參閱[時間點 (Point in Time)]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/point-in-time/)。
`post_filter` | 物件 | 在彙總計算完成後篩選結果的查詢。彙總包含所有符合 `query` 的文件，而結果只包含同時符合 `post_filter` 的文件。如需更多資訊，請參閱[篩選搜尋結果]({{site.url}}{{site.baseurl}}/search-plugins/filter-search/#narrowing-results-using-post-filter-while-preserving-aggregation-visibility)。
`profile` | 布林值 | 是否傳回查詢各部分執行情況的詳細計時資訊。預設為 `false`。如需更多資訊，請參閱 [Profile API]({{site.url}}{{site.baseurl}}/api-reference/search-apis/profile/)。
`query` | 物件 | 請求中要使用的 [DSL 查詢]({{site.url}}{{site.baseurl}}/query-dsl/)。
`rescore` | 物件或物件陣列 | 使用第二個通常成本較高的查詢，重新排序 `query` 傳回的最上層結果。如需更多資訊，請參閱[重新評分]({{site.url}}{{site.baseurl}}/query-dsl/rescore/)。
`script_fields` | 物件 | 由指令碼為每個命中結果計算值並在 `fields` 物件中傳回的欄位。如需更多資訊，請參閱[使用指令碼欄位]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/retrieve-specific-fields/#using-scripted-fields)。
`search_after` | 陣列 | 上一頁最後一個命中結果的排序值。傳回排序順序中接在其後的結果。需要 `sort`。如需更多資訊，請參閱[search_after 參數]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/paginate/#the-search_after-parameter)。
`search_pipeline` | 物件 | 僅適用於此請求的暫時性搜尋管線。如需更多資訊，請參閱[搜尋管線]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/index/)。
`seq_no_primary_term` | 布林值 | 是否傳回每個文件命中結果最後一次操作的序號與主要分片任期。
`size` | 整數 | 要傳回的最大結果數量。與 `from` 搭配使用以對結果進行分頁。預設為 `10`。如需更多資訊，請參閱[from 和 size 參數]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/paginate/#the-from-and-size-parameters)。
`slice` | 物件 | 將捲動或 PIT 搜尋分割成可獨立處理的切片。如需更多資訊，請參閱[捲動搜尋]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/paginate/#scroll-search)。
`sort` | 物件或字串陣列 | 指定結果的排序方式。可以是欄位名稱、包含欄位與排序選項的物件，或這些項目的陣列。請參閱[排序結果]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/sort/)。
`_source` | 布林值、字串、字串陣列或物件 | 每個命中結果中要傳回的文件來源欄位。預設為 `true`（傳回完整文件）。如需更多資訊，請參閱[來源篩選](#source-filtering)。
`stats` | 字串陣列 | 要與此請求建立關聯的[搜尋統計資料群組](#search-stats-groups)清單。
`stored_fields` | 字串陣列 | 每個命中結果要傳回的已儲存欄位。如果您指定 `stored_fields`，除非您主動要求，否則不會傳回 `_source`。如需更多資訊，請參閱[使用已儲存欄位進行搜尋]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/retrieve-specific-fields/#searching-with-stored-fields)。
`suggest` | 物件 | 傳回與所提供文字相似的建議詞彙或片語。如需更多資訊，請參閱[您是不是要找]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/did-you-mean/)。
`terminate_after` | 整數 | OpenSearch 在終止請求前應處理的最大相符文件（命中結果）數量。預設為 0。
`timeout` | 時間 | 等待回應的時間長度。預設為無逾時。
`track_scores` | 布林值 | 當依 `_score` 以外的欄位排序時，是否計算並傳回文件分數。預設為 `false`，此時排序結果中的 `_score` 為 `null`。
`track_total_hits` | 布林值或整數 | 要精確計數的相符文件數量。預設為 `10000`。如需更多資訊，請參閱[追蹤總命中數](#track-total-hits)。
`verbose_pipeline` | 布林值 | 是否傳回此請求所執行之每個搜尋管線處理器的資訊。預設為 `false`。如需更多資訊，請參閱[為搜尋管線除錯]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/debugging-search-pipeline/)。
`version` | 布林值 | 是否在回應中包含文件版本。

### 搜尋統計資料群組

您可以在請求本文的 `stats` 欄位中指定群組名稱，或以查詢參數的形式，將搜尋請求與一或多個統計資料群組建立關聯。OpenSearch 會維護各群組的搜尋統計資料，您可以使用 [Index Stats API]({{site.url}}{{site.baseurl}}/api-reference/index-apis/stats/#specific-search-groups) 來擷取。

下列範例會將搜尋請求與兩個群組建立關聯：

```json
POST /my-index/_search
{
  "query": {
    "match_all": {}
  },
  "stats": ["group1", "group2"]
}
```
{% include copy-curl.html %}

若要擷取特定群組的搜尋統計資料，請使用 Index Stats API 的 `groups` 查詢參數：

```json
GET /my-index/_stats/search?groups=group1,group2
```
{% include copy-curl.html %}

若要傳回所有群組的統計資料，請使用 `_all`：

```json
GET /my-index/_stats/search?groups=_all
```
{% include copy-curl.html %}

## 範例請求

<!-- spec_insert_start
component: example_code
rest: GET /movies/_search
body: |
{
  "query": {
    "match": {
      "director": "Christopher Nolan"
    }
  }
}
-->
{% capture step1_rest %}
GET /movies/_search
{
  "query": {
    "match": {
      "director": "Christopher Nolan"
    }
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.search(
  index = "movies",
  body =   {
    "query": {
      "match": {
        "director": "Christopher Nolan"
      }
    }
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->


## 範例回應

下列範例回應顯示搜尋回應的結構：

```json
{
  "took": 14,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 2,
      "relation": "eq"
    },
    "max_score": 0.42727602,
    "hits": [
      {
        "_index": "movies",
        "_id": "1",
        "_score": 0.42727602,
        "_source": {
          "title": "The Dark Knight",
          "director": "Christopher Nolan",
          "year": 2008,
          "genre": "Action"
        }
      },
      {
        "_index": "movies",
        "_id": "2",
        "_score": 0.42727602,
        "_source": {
          "title": "Inception",
          "director": "Christopher Nolan",
          "year": 2010,
          "genre": "Science Fiction"
        }
      }
    ]
  }
}
```

## 回應本文欄位

下表列出回應本文的最上層欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `took` | 整數 | OpenSearch 執行搜尋所花費的時間，以毫秒為單位。從協調節點收到請求的時刻起，到準備好傳送回應為止，因此包含協調節點與資料節點之間的通訊、在 `search` 執行緒集區中排隊的時間，以及搜尋本身所花費的時間。不包含透過網路傳輸請求或回應所花費的時間。 |
| `phase_took` | 物件 | 各搜尋階段（`can_match`、`dfs_pre_query`、`query`、`dfs_query`、`fetch` 和 `expand`）所花費的時間，以毫秒為單位。僅在 `phase_took` 查詢參數為 `true` 時傳回。 |
| `timed_out` | 布林值 | 搜尋是否在完成前逾時。如果為 `true`，傳回的結果可能不完整或為空。 |
| `terminated_early` | 布林值 | OpenSearch 是否因為已收集到 `terminate_after` 指定的文件數量而提早停止搜尋。僅在設定 `terminate_after` 時傳回。 |
| `_shards` | 物件 | 執行搜尋的分片數量，以及各組分片的結果。 |
| `hits` | 物件 | 符合條件的文件及其中繼資料。 |
| `aggregations` | 物件 | 彙總結果，以彙總名稱作為鍵。僅在請求本文包含 `aggs` 物件時傳回。 |
| `suggest` | 物件 | 建議結果，以建議器名稱作為鍵。僅在請求本文包含 `suggest` 物件時傳回。 |
| `profile` | 物件 | 各分片在查詢與擷取階段的計時詳細資訊。僅在請求本文將 `profile` 設為 `true` 時傳回。如需詳細資訊，請參閱 [Profile API]({{site.url}}{{site.baseurl}}/api-reference/search-apis/profile/)。 |
| `_scroll_id` | 字串 | 識別搜尋內容的 scroll ID。將此值傳遞給 [Scroll API]({{site.url}}{{site.baseurl}}/api-reference/search-apis/scroll/)，以擷取下一批結果。僅在請求包含 `scroll` 查詢參數時傳回。 |
| `pit_id` | 字串 | 識別搜尋內容的時間點（PIT）ID。僅在請求搜尋 PIT 時傳回。如需詳細資訊，請參閱 [Point in Time API]({{site.url}}{{site.baseurl}}/api-reference/search-apis/point-in-time-api/)。 |
| `_clusters` | 物件 | 執行跨叢集搜尋的叢集數量，以及各組叢集的結果。僅在跨叢集搜尋時傳回。 |
| `num_reduce_phases` | 整數 | OpenSearch 為將分片的部分結果合併為最終結果集而執行的歸約階段數量。僅在搜尋使用多個歸約階段時傳回。 |

下表列出 `_shards` 物件中的欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `total` | 整數 | 搜尋需要查詢的分片數量，包含未配置的分片。 |
| `successful` | 整數 | 成功執行搜尋的分片數量。 |
| `skipped` | 整數 | 因初步檢查判定分片上沒有任何文件可能符合條件而略過搜尋的分片數量。這通常發生在搜尋包含範圍篩選器，且分片上的所有值都落在該範圍之外時。 |
| `failed` | 整數 | 未能執行搜尋的分片數量。未配置的分片既不計入成功，也不計入失敗，因此若 `successful` 和 `failed` 的總和小於 `total`，表示有部分分片未配置。 |

下表列出 `hits` 物件中的欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `total` | 物件 | 符合條件的文件數量。包含儲存計數的 `value` 欄位，以及 `relation` 欄位；當計數為精確值時，後者為 `eq`，當計數為下限時，則為 `gte`。當 `track_total_hits` 為 `false` 時省略。 |
| `max_score` | 浮點數 | 符合條件的文件中最高的 `_score`。當搜尋未依 `_score` 排序時，值為 `null`。 |
| `hits` | 物件陣列 | 符合條件的文件，依相關性或指定的排序方式排列。 |

下表列出 `hits.hits` 陣列中各物件的欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `_index` | 字串 | 包含該文件的索引名稱。 |
| `_id` | 字串 | 文件 ID。此 ID 僅在傳回的索引中具有唯一性。 |
| `_score` | 浮點數 | 文件的相關性分數。當搜尋未依 `_score` 排序時，值為 `null`。 |
| `_source` | 物件 | 編製索引時提供的原始 JSON 文件。若要省略此欄位或僅傳回特定欄位，請參閱[來源篩選](#source-filtering)。 |
| `fields` | 物件 | 由 `docvalue_fields` 或 `stored_fields` 擷取的欄位值。僅在請求指定其中任一參數時傳回。 |
| `sort` | 陣列 | 文件的排序值。僅在請求本文包含 `sort` 陣列時傳回。將最後一筆命中結果的值作為 `search_after` 傳遞，以擷取下一頁結果。 |
| `highlight` | 物件 | 醒目提示的片段，以欄位名稱作為鍵。僅在請求本文包含 `highlight` 物件時傳回。 |
| `matched_queries` | 字串陣列 | 文件符合的具名查詢名稱。僅在搜尋使用 `_name` 參數時傳回。 |
| `inner_hits` | 物件 | 符合條件的巢狀文件、子文件或父文件。僅在請求本文包含 `inner_hits` 物件時傳回。 |
| `_explanation` | 物件 | OpenSearch 計算文件相關性分數的詳細說明。僅在 `explain` 為 `true` 時傳回。 |
| `_shard` | 字串 | 傳回文件的分片。僅在 `explain` 為 `true` 時傳回。 |
| `_node` | 字串 | 傳回文件的節點。僅在 `explain` 為 `true` 時傳回。 |

## 來源篩選

回應中的每筆命中結果都包含一個 `_source` 物件，其中儲存原始 JSON 文件。為每筆命中結果傳回完整文件，會傳輸超過大多數應用程式所需的資料量。來源篩選可限制 OpenSearch 在 `_source` 中傳回的欄位。

下表列出 `_source` 請求本文參數接受的值。

| 值 | 說明 |
| :--- | :--- |
| `true` | 傳回完整文件。這是預設值。 |
| `false` | 從每筆命中結果中省略 `_source` 物件。 |
| 字串 | 欄位名稱或萬用字元模式，例如 `details.*`。OpenSearch 僅傳回符合條件的欄位。 |
| 字串陣列 | 欄位名稱或萬用字元模式的清單，例如 `["name", "details.*"]`。 |
| 物件 | 包含 `includes` 和 `excludes` 清單的物件。若欄位同時符合兩份清單中的模式，則不會傳回，因為 `excludes` 具有優先權。 |

若要在請求 URL 中篩選來源，請使用 `_source`、`_source_includes` 和 `_source_excludes` 查詢參數，而非在請求本文中設定。

如需範例與限制，請參閱[使用來源篩選]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/retrieve-specific-fields/#using-source-filtering)。

## 追蹤總命中數

要精確計算相符的文件數量，必須走訪每一個相符項目，對於相符文件眾多的查詢而言，這麼做的成本很高。`track_total_hits` 參數會限制 OpenSearch 計算的相符項目數量。您可以將其指定為查詢參數，或是在請求本文中指定。

根據預設，OpenSearch 會精確計算相符項目，最多到 `10000`。當有更多文件相符時，`hits.total.value` 會回報 `10000`，且 `hits.total.relation` 為 `gte`，表示查詢至少符合這麼多份文件。

下表列出 `track_total_hits` 可接受的值。

| 值 | 說明 |
| :--- | :--- |
| `true` | 計算每一份相符的文件。`hits.total.relation` 一律為 `eq`。 |
| `false` | 停用命中數計算。回應中不含 `hits.total` 物件。 |
| 整數 | 精確計算相符文件，最多到指定的數量。當有更多文件相符時，`hits.total.value` 會回報該閾值，且 `hits.total.relation` 為 `gte`。 |

計算每一個相符項目會拖慢相符文件眾多的搜尋。一旦計數達到閾值，OpenSearch 就能略過無法進入前幾名結果的文件，讓依相關性排序的搜尋更快。只有在應用程式需要精確計數時才提高閾值，而當您完全不顯示計數時，請將 `track_total_hits` 設為 `false`。

`rest_total_hits_as_int` 查詢參數需要精確計數。若請求將 `rest_total_hits_as_int` 設為 `true`，並將 `track_total_hits` 設為整數，OpenSearch 會拒絕該請求。

### 範例：預設命中計數

下列範例搜尋一個包含 10,500 份文件的 `logs` 索引，且未指定 `track_total_hits`：

```json
GET /logs/_search
{
  "size": 0,
  "query": {
    "match_all": {}
  }
}
```
{% include copy-curl.html %}

因為 `relation` 為 `gte`，所以索引中至少有 10,000 份符合的文件：

```json
{
  "hits": {
    "total": {
      "value": 10000,
      "relation": "gte"
    },
    "max_score": null,
    "hits": []
  }
}
```

### 範例：計算每份符合的文件

若要計算所有符合的結果，請將 `track_total_hits` 設定為 `true`：

```json
GET /logs/_search
{
  "size": 0,
  "track_total_hits": true,
  "query": {
    "match_all": {}
  }
}
```
{% include copy-curl.html %}

因為 `relation` 為 `eq`，所以 `value` 是符合文件的確切數量：

```json
{
  "hits": {
    "total": {
      "value": 10500,
      "relation": "eq"
    },
    "max_score": null,
    "hits": []
  }
}
```

### 範例：計數至自訂閾值

整數閾值會在相符文件數少於閾值時傳回確切計數，否則傳回下限。在 `logs` 索引中，35 份文件的 `level` 值為 `error`，其餘文件的值為 `info`。下列請求會計算 `error` 文件的數量，計數閾值為 50：

```json
GET /logs/_search
{
  "size": 0,
  "track_total_hits": 50,
  "query": {
    "term": {
      "level": "error"
    }
  }
}
```
{% include copy-curl.html %}

相符文件少於 50 份，因此計數是確切的：

```json
{
  "hits": {
    "total": {
      "value": 35,
      "relation": "eq"
    },
    "max_score": null,
    "hits": []
  }
}
```

如果您使用 `"level": "info"` 執行相同的請求，相符文件會超過 50 份。OpenSearch 會在達到閾值時停止計數，並傳回下限：

```json
{
  "hits": {
    "total": {
      "value": 50,
      "relation": "gte"
    },
    "max_score": null,
    "hits": []
  }
}
```

### 範例：停用命中計數

如果您的應用程式不顯示相符項目的數量，請將 `track_total_hits` 設為 `false`：

```json
GET /logs/_search
{
  "size": 2,
  "_source": false,
  "track_total_hits": false,
  "query": {
    "term": {
      "level": "error"
    }
  }
}
```
{% include copy-curl.html %}

`hits` 物件包含相符的文件，但不含 `total` 物件：

```json
{
  "hits": {
    "max_score": 1.0,
    "hits": [
      {
        "_index": "logs",
        "_id": "1",
        "_score": 1.0
      },
      {
        "_index": "logs",
        "_id": "301",
        "_score": 1.0
      }
    ]
  }
}
```

## `ext` 物件
**2.10 版新增**
{: .label .label-purple }

外掛程式作者可以在搜尋請求與搜尋回應中加入 `ext` 物件。`ext` 物件包含外掛程式專屬的欄位，讓外掛程式能在請求中傳遞額外參數，或在回應中傳回額外資訊。

### 在搜尋回應中使用 `ext`

外掛程式可以在搜尋回應中加入 `ext` 物件，以包含外掛程式專屬的回應欄位。例如，在對話式搜尋中，檢索增強生成 (RAG) 的結果是單一「命中」(答案)。外掛程式作者可以將此答案納入搜尋回應中，作為 `ext` 物件的一部分，使其與搜尋命中結果分開。在下列範例回應中，RAG 結果位於 `ext.retrieval_augmented_generation.answer` 欄位：

```json
{
  "took": 3,
  "timed_out": false,
  "_shards": {
    "total": 3,
    "successful": 3,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 110,
      "relation": "eq"
    },
    "max_score": 0.55129033,
    "hits": [
      {
       "_index": "...",
        "_id": "...",
        "_score": 0.55129033,
        "_source": {
          "text": "...",
          "title": "..."
        }
      },
      {
      ...
      }
      ...
      {
      ...
      }
    ],
  }, // end of hits
  "ext": {
    "retrieval_augmented_generation": { // a search response processor
      "answer": "RAG answer"
    }
  }
}
```

### 在搜尋請求中使用 `ext`

外掛程式也可以在搜尋請求中接受 `ext` 物件，以提供外掛程式專屬的參數。請求中 `ext` 物件的結構與內容取決於外掛程式的實作方式。請查閱您外掛程式的文件，了解請求 `ext` 物件中支援的特定欄位。

下列範例顯示包含 `ext` 物件的搜尋請求。`ext` 中的確切欄位取決於已安裝的外掛程式及其接受的參數：

```json
POST /my-index/_search
{
  "query": {
    "match": {
      "field": "value"
    }
  },
  "ext": {
    "my_plugin": {
      "custom_parameter": "value"
    }
  }
}
```

## 必要權限

如果您使用 Security 外掛程式，請確認您具備適當的權限：`indices:data/read/search`。
