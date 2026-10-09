---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "搜尋 (gRPC)"
parent: gRPC APIs
nav_order: 10
---

# Search API (gRPC)
**於 3.0 版推出**
{: .label .label-purple }


這是實驗性功能，不建議在正式環境中使用。如需了解功能的最新進展，或想提供意見回饋，請參閱相關的 [GitHub 議題](https://github.com/opensearch-project/OpenSearch/issues/16787)。
{: .warning}

gRPC Search API 提供高效能的二進位介面，可透過 gRPC 上的 protocol buffers 執行[查詢]({{site.url}}{{site.baseurl}}/api-reference/search/)。它具備 HTTP Search API 的功能，同時享有 protobuf 型別合約與 gRPC 傳輸的優勢。gRPC API 非常適合低延遲、高輸送量的應用程式。

## 先決條件

若要提交 gRPC 請求，您必須在用戶端上備有一組 protobuf。如需取得 protobuf 的方法，請參閱[使用 gRPC API]({{site.url}}{{site.baseurl}}/api-reference/grpc-apis/index/#how-to-use-grpc-apis)。

## gRPC 服務與方法

gRPC Document API 位於 [`SearchService`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/services/search_service.proto#L22)。

您可以在 `SearchService` 中叫用 [`Search`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/services/search_service.proto#L23) gRPC 方法來提交搜尋請求。此方法接受 [`SearchRequest`](#searchrequest-fields) 並傳回 [`SearchResponse`](#searchresponse-fields)。

如需支援的搜尋查詢，請參閱[支援的查詢](#supported-queries)。其他查詢類型將在未來版本中支援。
{: .note}

## 請求欄位

gRPC Search API 支援下列請求欄位。

### SearchRequest 欄位

[`SearchRequest`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L20) 訊息接受下列欄位。所有欄位皆為選用。

| 欄位 | Protobuf 類型 | 說明 |
| :---- | :---- | :---- |
| `index` | `repeated string` | 要搜尋的索引清單。若未提供，預設為所有索引。 |
| `x_source` | [`SourceConfigParam`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L1251) | 控制回應中要傳回完整的 `_source`、不傳回 `_source`，或只傳回 `_source` 中的特定欄位。 |
| `x_source_excludes` | `repeated string` | 要從 `_source` 排除的欄位。若 `source` 為 `false` 則忽略。 |
| `x_source_includes` | `repeated string` | 要包含在 `_source` 中的欄位。若 `source` 為 `false` 則忽略。  |
| `allow_no_indices` | `bool` | 是否忽略未符合任何索引的萬用字元。預設為 `true`。 |
| `allow_partial_search_results` | `bool` | 發生錯誤或逾時時是否傳回部分結果。預設為 `true`。 |
| `analyze_wildcard` | `bool` | 是否分析萬用字元／前置字元查詢。預設為 `false`。  |
| `batched_reduce_size` | `int32` | 在節點上執行縮減 (reduce) 時處理的分片數。預設為 `512`。  |
| `cancel_after_time_interval` | `string` | 超過此時間後請求將被取消。預設為 `-1`。 |
| `ccs_minimize_roundtrips` | `bool` | 是否盡量減少節點與遠端叢集之間的來回傳輸。預設為 `true`。  |
| `default_operator` | [`Operator`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L3646) | 查詢字串的預設運算子。有效值為 `AND` 或 `OR`。預設為 `OR`。  |
| `df` | `string` | 沒有欄位前置字元的查詢字串所使用的預設欄位。  |
| `docvalue_fields` | `repeated string` | 要以 doc values 形式傳回的欄位。 |
| `expand_wildcards` | `repeated` [`ExpandWildcard`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L3567) | 萬用字元運算式可符合的索引類型。有效值為 `all` (符合任何索引)、`open` (符合開啟且非隱藏的索引)、`closed` (符合關閉且非隱藏的索引)、`hidden` (符合隱藏的索引)，以及 `none` (拒絕萬用字元運算式)。預設為 `open`。|
| `ignore_throttled` | `bool` | 解析別名時是否忽略凍結的索引。預設為 `true`。 |
| `ignore_unavailable` | `bool` | 是否忽略無法使用的索引或分片。預設為 `false`。 |
| `max_concurrent_shard_requests` | `int32` | 每個節點的並行分片請求數。預設為 `5`。 |
| `phase_took` | `bool` | 是否傳回階段層級的 `took` 值。預設為 `false`。 |
| `pre_filter_shard_size` | `int32` | 依分片大小觸發預先篩選的臨界值。預設為 `128`。 |
| `preference` | `string` | 查詢執行時的分片或節點偏好設定。 |
| `q` | `string` | 使用 [Lucene 語法]({{site.url}}{{site.baseurl}}/query-dsl/full-text/query-string/#query-string-syntax)的查詢字串。 |
| `request_cache` | `bool` | 是否使用請求快取。預設為索引的設定。 |
| `total_hits_as_int` | `bool` | 是否以整數傳回總命中數。預設為 `false`。 |
| `routing` | `repeated string` | 用來將請求導向特定分片的路由值。 |
| `scroll` | `string` | 為捲動搜尋保留搜尋情境的時間長度。 |
| `search_type` | [`SearchType`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L3576) | 計算相關性分數的方法。有效值為 `QUERY_THEN_FETCH` 和 `DFS_QUERY_THEN_FETCH`。預設為 `QUERY_THEN_FETCH`。 |
| `suggest_field` | `string` | 做為建議依據的欄位。 |
| `suggest_mode` | [`SuggestMode`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L3582) | 建議模式 (例如 `always`、`missing`、`popular`)。 |
| `suggest_size` | `int32` | 要傳回的建議數。 |
| `suggest_text` | `string` | 用來產生建議的輸入文字。 |
| `typed_keys` | `bool` | 是否在彙總與建議鍵中包含類型資訊。預設為 `true`。 |
| `search_request_body` | [`SearchRequestBody`](#searchrequestbody-fields) | 主要的搜尋請求承載內容，包括查詢與篩選條件。 |
| `global_params` | [`GlobalParams`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L1150) | 請求的全域參數。選用。 |

### SearchRequestBody 欄位

[`SearchRequestBody`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L123) 訊息接受下列欄位。所有欄位皆為選用。

| 欄位 | Protobuf 類型 | 說明 |
| :---- | :---- | :---- |
| `collapse` | [`FieldCollapse`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L1974) | 依欄位將結果分組。每個群組僅傳回排名最高的文件。 |
| `explain` | `bool` | 回傳相符文件的評分解釋。 |
| `ext` | [`ObjectMap`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L3890) | 外掛程式專屬的中繼資料，例如用於 RAG 等擴充功能。 |
| `from` | `int32` | 分頁結果的起始索引。預設為 `0`。 |
| `highlight` | [`Highlight`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L1728) | 在結果摘要中突顯相符的詞彙。 |
| `track_total_hits` | [`TrackHits`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L252) | 是否回傳總命中次數。 |
| `indices_boost` | `map<string, float>` | **已棄用。**請改用 `indices_boost_2`。 |
| `docvalue_fields` | `repeated` [`FieldAndFormat`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L1965) | 以 `doc_values` 形式回傳的欄位。您可以為回傳值指定格式（例如日期格式）。對於 `knn_vector` 欄位，支援的格式為 `binary`（預設，Base64 編碼）與 `array`（JSON 數值陣列）。如需更多資訊，請參閱[使用 `docvalue_fields` 擷取向量欄位]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/retrieve-specific-fields/#retrieving-vector-fields-using-docvalue_fields)。 |
| `min_score` | `float` | 文件納入結果所需的最低分數。 |
| `post_filter` | [`QueryContainer`](#querycontainer-fields) | 在套用彙總之後篩選命中結果。 |
| `profile` | `bool` | 啟用效能分析以分析查詢效能。 |
| `search_pipeline` | `string` | 要套用的搜尋管線名稱。 |
| `verbose_pipeline` | `bool` | 在搜尋管線中啟用詳細記錄。 |
| `query` | [`QueryContainer`](#querycontainer-fields) | 搜尋所用的 Query DSL。 |
| `rescore` | `repeated` [`Rescore`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L504) | 重新排序前 N 筆命中結果以提升精確度。 |
| `script_fields` | `map<string, `[`ScriptField`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L1677)`>` | 由指令碼計算值的自訂欄位。 |
| `search_after` | `repeated` [`FieldValue`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L2637) | 使用上一頁的值進行游標式分頁。 |
| `size` | `int32` | 要回傳的結果數量。預設為 `10`。 |
| `slice` | [`SlicedScroll`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L513) | 將捲動搜尋的搜尋情境分割成多個切片，以進行平行處理。 |
| `sort` | `repeated` [`SortCombinations`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L1693) | 排序規則（例如依欄位、分數或自訂順序）。 |
| `x_source` | [`SourceConfig`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L1267) | 控制回應中要回傳完整 `_source`、不回傳 `_source`，或僅回傳 `_source` 中的特定欄位。 |
| `fields` | `repeated` [`FieldAndFormat`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L1965) | 要額外回傳的欄位，並可指定格式選項。 |
| `terminate_after` | `int32` | 提前終止前要處理的相符文件（命中）數量上限。預設為 `0`。 |
| `timeout` | `string` | 等待查詢執行的最長時間。 |
| `track_scores` | `bool` | 是否在結果中回傳文件分數。 |
| `include_named_queries_score` | `bool` | 是否包含具名查詢的分數。 |
| `version` | `bool` | 是否在回應中包含文件版本。 |
| `seq_no_primary_term` | `bool` | 是否在回應中包含每筆命中結果的序號與主要分片任期。 |
| `stored_fields` | `repeated string` | 要回傳的儲存欄位（除非重新啟用，否則排除 `_source`）。 |
| `pit` | [`PointInTimeReference`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L612) | 用於搜尋固定快照的 Point in Time 參考。 |
| `stats` | `repeated string` | 要與請求建立關聯的標記或記錄欄位。 |
| `derived` | `map<string, `[`DerivedField`](#derivedfield-fields)`>` | 在回應中動態計算並回傳的欄位。 |
| `indices_boost_2` | `repeated` [`FloatMap`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L3004) | 各索引加權乘數目前的 protobuf 表示法。每個項目包含索引對加權的對應。 |
| `aggregations` | `map<string, `[`AggregationContainer`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L3026)`>` | 作為搜尋請求一部分要計算的彙總。 |

### DerivedField 欄位

[`DerivedField`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L228) 訊息用於在搜尋執行期間計算的動態欄位。它接受下列欄位。

| 欄位 | Protobuf 類型 | 說明 |
| :---- | :---- | :---- |
| `name` | `string` | 衍生欄位的名稱。必要。 |
| `type` | `string` | 衍生欄位的資料類型。必要。 |
| `script` | [`Script`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L1171) | 計算欄位值的指令碼。必要。 |
| `prefilter_field` | `string` | 用於預先篩選以最佳化指令碼執行的欄位。選用。 |
| `properties` | [`ObjectMap`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L3890) | 衍生欄位的其他屬性。選用。 |
| `ignore_malformed` | `bool` | 在欄位計算期間是否忽略格式錯誤的值。選用。 |
| `format` | `string` | 要套用至欄位值的格式（例如日期格式）。選用。 |

### QueryContainer 欄位

`QueryContainer` 是所有支援查詢類型的進入點。

每個 `QueryContainer` 訊息中必須提供下列欄位中的**恰好一個**。

請注意，目前部分查詢類型尚不支援。目前已實作的查詢類型清單請參閱[支援的查詢](#supported-queries)。
{: .note}

| 欄位 | Protobuf 類型 | 說明 |
| :---- | :---- | :---- |
| `bool` | [`BoolQuery`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L2133) | 使用 `AND`、`OR` 或 `NOT` 邏輯組合多個子句的布林查詢。必須是唯一設定的欄位。 |
| `constant_score` | [`ConstantScoreQuery`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L2171) | 包裝篩選器，並為所有符合的文件指派固定的相關性分數。必須是唯一設定的欄位。 |
| `function_score` | [`FunctionScoreQuery`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L2183) | 使用自訂函式調整結果的分數。必須是唯一設定的欄位。 |
| `exists` | [`ExistsQuery`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L1986) | 比對包含特定欄位的文件。必須是唯一設定的欄位。 |
| `fuzzy` | [`FuzzyQuery`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L2593) | 比對與搜尋詞彙相似的詞彙（模糊比對）。必須是唯一設定的欄位。 |
| `ids` | [`IdsQuery`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L2648) | 依據 `_id` 值比對文件。必須是唯一設定的欄位。 |
| `prefix` | [`PrefixQuery`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L2309) | 比對具有特定前綴的詞彙。必須是唯一設定的欄位。 |
| `range` | [`RangeQuery`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L2460) | 比對指定範圍內的詞彙。必須是唯一設定的欄位。 |
| `regexp` | [`RegexpQuery`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L2391) | 使用正規表示式比對詞彙。必須是唯一設定的欄位。 |
| `term` | [`TermQuery`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L2421) | 比對完全相符的詞彙（不進行分析）。必須是唯一設定的欄位。 |
| `terms` | [`TermsQuery`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L1587) | 比對欄位中包含一個或多個指定詞彙的任何文件。必須是唯一設定的欄位。 |
| `terms_set` | [`TermsSetQuery`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L2370) | 比對欄位中包含至少指定數量之完全相符詞彙的文件。必須是唯一設定的欄位。 |
| `wildcard` | [`WildcardQuery`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L1998) | 使用萬用字元模式比對詞彙。必須是唯一設定的欄位。 |
| `match` | [`MatchQuery`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L2082) | 對文字或精確值欄位執行全文比對。必須是唯一設定的欄位。 |
| `match_bool_prefix` | [`MatchBoolPrefixQuery`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L2668) | 在布林式查詢中比對完整單字與前綴。必須是唯一設定的欄位。 |
| `match_phrase` | [`MatchPhraseQuery`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L2746) | 依順序比對完全相符的片語。必須是唯一設定的欄位。 |
| `match_phrase_prefix` | [`MatchPhrasePrefixQuery`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L2719) | 比對片語，並將其中最後一個詞彙視為前綴。必須是唯一設定的欄位。 |
| `multi_match` | [`MultiMatchQuery`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L2770) | 使用單一查詢字串搜尋多個欄位。必須是唯一設定的欄位。 |
| `knn` | [`KnnQuery`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L2023) | 跨向量欄位執行的 k-NN 查詢。必須是唯一設定的欄位。 |
| `match_all` | [`MatchAllQuery`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L2659) | 比對索引中的所有文件。必須是唯一設定的欄位。 |
| `match_none` | [`MatchNoneQuery`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L2710) | 不比對任何文件。必須是唯一設定的欄位。 |
| `nested` | [`NestedQuery`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L1602) | 包裝以巢狀欄位為目標的查詢。必須是唯一設定的欄位。 |
| `geo_distance` | [`GeoDistanceQuery`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L1560) | 傳回包含地理座標點的文件，這些座標點位於所提供地理座標點的指定距離內。必須是唯一設定的欄位。 |
| `geo_bounding_box` | [`GeoBoundingBoxQuery`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L1483) | 傳回包含位於指定邊界框內之地理座標點的文件。必須是唯一設定的欄位。 |
| `script` | [`ScriptQuery`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L1471) | 根據以 Painless 指令碼語言撰寫的自訂條件篩選文件。必須是唯一設定的欄位。 |
| `hybrid` | [`HybridQuery`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L1453) | 將多個查詢的相關性分數合併為一個分數。必須是唯一設定的欄位。 |

## 支援的查詢

gRPC Search API 支援下列查詢類型：
* 詞彙層級：`exists`、`fuzzy`、`ids`、`prefix`、`range`、`regexp`、`term`、`terms`、`terms_set`、`wildcard`
* 全文：`match`、`match_bool_prefix`、`match_phrase`、`match_phrase_prefix`、`multi_match`
* 比對全部：`match_all`、`match_none`
* 複合查詢：`bool`、`constant_score`、`function_score`、`hybrid`
* 地理：`geo_bounding_box`、`geo_distance`
* 聯結查詢：`nested`
* 特殊查詢：`knn`、`script`

如需這些查詢類型的詳細資訊，請參閱 [Query DSL]({{site.url}}{{site.baseurl}}/query-dsl/)。

### 詞彙層級查詢欄位

下列各節說明每個詞彙層級查詢訊息的欄位。

#### ExistsQuery 欄位

[`ExistsQuery`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L1986) 訊息接受下列欄位。

| 欄位 | Protobuf 類型 | 說明 |
| :---- | :---- | :---- |
| `field` | `string` | 必要。要搜尋的欄位名稱。 |
| `boost` | `optional float` | 用於降低或提高查詢相關性分數的浮點數。預設為 `1.0`。 |
| `x_name` | `optional string` | 用於標記查詢的查詢名稱。 |

#### FuzzyQuery 欄位

[`FuzzyQuery`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L2593) 訊息接受下列欄位。

| 欄位 | Protobuf 類型 | 說明 |
| :---- | :---- | :---- |
| `field` | `string` | 必要。要對其執行搜尋查詢的欄位。 |
| `value` | [`FieldValue`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L2637) | 必要。要在指定欄位中搜尋的詞彙。 |
| `boost` | `optional float` | 用於降低或提高查詢相關性分數的浮點數。預設為 `1.0`。 |
| `x_name` | `optional string` | 用於標記查詢的查詢名稱。 |
| `max_expansions` | `optional int32` | 查詢可展開的詞彙數量上限。預設為 `50`。 |
| `prefix_length` | `optional int32` | 不納入模糊比對考量的開頭字元數。預設為 `0`。 |
| `rewrite_deprecated` | `optional` [`MultiTermQueryRewrite`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L3652) | **已棄用。** 請改用 `rewrite`。 |
| `transpositions` | `optional bool` | 指定是否允許將兩個相鄰字元的對調視為編輯操作。預設為 `true`。 |
| `fuzziness` | `optional` [`Fuzziness`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L2626) | 判斷詞彙是否符合某個值時，將一個單字變更為另一個單字所需的字元編輯次數（插入、刪除或替換）。|
| `rewrite` | `optional string` | 決定 OpenSearch 如何重寫查詢。請參閱[重寫參數值](#rewrite-parameter-values)。預設為 `constant_score`。 |

#### IdsQuery 欄位

[`IdsQuery`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L2648) 訊息接受下列欄位。

| 欄位 | Protobuf 類型 | 說明 |
| :---- | :---- | :---- |
| `boost` | `optional float` | 用於降低或提高查詢相關性分數的浮點數。預設為 `1.0`。 |
| `x_name` | `optional string` | 用於標記查詢的查詢名稱。 |
| `values` | `repeated string` | 要搜尋的文件 ID。 |

#### PrefixQuery 欄位

[`PrefixQuery`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L2309) 訊息接受下列欄位。

| 欄位 | Protobuf 類型 | 說明 |
| :---- | :---- | :---- |
| `field` | `string` | 必要。要執行搜尋查詢的欄位。 |
| `value` | `string` | 必要。要在指定欄位中搜尋的詞彙。 |
| `boost` | `optional float` | 用於降低或提高查詢相關性分數的浮點數。預設為 `1.0`。 |
| `x_name` | `optional string` | 用於標記查詢的查詢名稱。 |
| `rewrite_deprecated` | `optional` [`MultiTermQueryRewrite`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L3652) | **已棄用。** 請改用 `rewrite`。 |
| `case_insensitive` | `optional bool` | 允許不區分 ASCII 大小寫的比對。預設為 `false`。 |
| `rewrite` | `optional string` | 決定 OpenSearch 如何改寫查詢。請參閱[改寫參數值](#rewrite-parameter-values)。預設為 `constant_score`。 |

#### RangeQuery 欄位

[`RangeQuery`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L2460) 訊息屬於 `oneof` 類型，可包含 [`NumberRangeQuery`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L2469) 或 [`DateRangeQuery`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L2530)。

##### NumberRangeQuery 欄位

`NumberRangeQuery` 訊息接受下列欄位。

`NumberRangeQuery` 訊息接受下列欄位。

| 欄位 | Protobuf 類型 | 說明 |
| :---- | :---- | :---- |
| `field` | `string` | 必要。要執行搜尋查詢的欄位。 |
| `boost` | `optional float` | 用於降低或提高查詢相關性分數的浮點數。預設為 `1.0`。 |
| `x_name` | `optional string` | 用於標記查詢的查詢名稱。 |
| `relation` | `optional` [`RangeRelation`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L3589) | 指定範圍查詢如何比對範圍欄位的值。 |
| `gt` | `optional double` | 大於。 |
| `gte` | `optional double` | 大於或等於。 |
| `lt` | `optional double` | 小於。 |
| `lte` | `optional double` | 小於或等於。 |
| `from` | `optional` [`NumberRangeQueryAllOfFrom`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L2508) | 範圍的起始值。 |
| `to` | `optional` [`NumberRangeQueryAllOfTo`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L2519) | 範圍的結束值。 |
| `include_lower` | `optional bool` | 是否包含下限。 |
| `include_upper` | `optional bool` | 是否包含上限。 |

##### DateRangeQuery 欄位

 `DateRangeQuery` 訊息接受下列欄位。

`DateRangeQuery` 訊息接受下列欄位。

| 欄位 | Protobuf 類型 | 說明 |
| :---- | :---- | :---- |
| `field` | `string` | 必要。要執行搜尋查詢的欄位。 |
| `boost` | `optional float` | 用於降低或提高查詢相關性分數的浮點數。預設為 `1.0`。 |
| `x_name` | `optional string` | 用於標記查詢的查詢名稱。 |
| `relation` | `optional` [`RangeRelation`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L3589) | 指定範圍查詢如何比對範圍欄位的值。 |
| `gt` | `optional string` | 大於。 |
| `gte` | `optional string` | 大於或等於。 |
| `lt` | `optional string` | 小於。 |
| `lte` | `optional string` | 小於或等於。 |
| `from` | `optional` [`DateRangeQueryAllOfFrom`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L2575) | 範圍的起始值。 |
| `to` | `optional` [`DateRangeQueryAllOfTo`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L2584) | 範圍的結束值。 |
| `format` | `optional string` | 日期格式模式。 |
| `time_zone` | `optional string` | 時區識別碼。 |
| `include_lower` | `optional bool` | 是否包含下限。 |
| `include_upper` | `optional bool` | 是否包含上限。 |

#### RegexpQuery 欄位

[`RegexpQuery`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L2391) 訊息接受下列欄位。

| 欄位 | Protobuf 類型 | 說明 |
| :---- | :---- | :---- |
| `field` | `string` | 必要。要執行搜尋查詢的欄位。 |
| `value` | `string` | 必要。用於比對所提供欄位中要搜尋詞彙的正規表示式。 |
| `boost` | `optional float` | 用於降低或提高查詢相關性分數的浮點數。預設為 `1.0`。 |
| `x_name` | `optional string` | 用於標記查詢的查詢名稱。 |
| `case_insensitive` | `optional bool` | 允許正規表示式進行不區分大小寫的比對。預設為 `false`。 |
| `flags` | `optional string` | 啟用正規表示式的選用運算子。 |
| `max_determinized_states` | `optional int32` | 查詢所需的自動機狀態數上限。預設為 `10000`。 |
| `rewrite_deprecated` | `optional` [`MultiTermQueryRewrite`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L3652) | **已棄用。** 請改用 `rewrite`。 |
| `rewrite` | `optional string` | 決定 OpenSearch 如何改寫多詞彙查詢並評分。請參閱[改寫參數值](#rewrite-parameter-values)。預設為 `constant_score`。 |

#### TermQuery 欄位

[`TermQuery`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L2421) 訊息接受下列欄位。

| 欄位 | Protobuf 類型 | 說明 |
| :---- | :---- | :---- |
| `field` | `string` | 必要。要執行搜尋查詢的欄位。 |
| `boost` | `optional float` | 用於降低或提高查詢相關性分數的浮點數。預設為 `1.0`。 |
| `x_name` | `optional string` | 用於標記查詢的查詢名稱。 |
| `value` | [`FieldValue`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L2637) | 必要。要在所提供欄位中搜尋的詞彙。必須與欄位值完全相符。 |
| `case_insensitive` | `optional bool` | 允許不區分 ASCII 大小寫的比對。預設為 `false`。 |

#### TermsQuery 欄位

[`TermsQuery`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L1587) 訊息接受下列欄位。

| 欄位 | Protobuf 類型 | 說明 |
| :---- | :---- | :---- |
| `boost` | `optional float` | 用於降低或提高查詢相關性分數的浮點數。預設為 `1.0`。 |
| `x_name` | `optional string` | 用於查詢標記的查詢名稱。 |
| `value_type` | `optional` [`TermsQueryValueType`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L3612) | 用於篩選的值類型。有效值為 `default` 和 `bitmap`。預設為 `default`。 |
| `terms` | `map<string, `[`TermsQueryField`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L2333)`>` | 欄位名稱與詞彙值或詞彙查找項目的對應表。 |

#### TermsQueryField 欄位

[`TermsQueryField`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L2333) 訊息接受下列其中一個欄位。

| 欄位 | Protobuf 類型 | 說明 |
| :---- | :---- | :---- |
| `value` | [`FieldValueArray`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L2365) | 要比對的詞彙值明確清單。 |
| `lookup` | [`TermsLookup`](#termslookup-fields) | 從另一份文件取得詞彙值。 |

#### TermsLookup 欄位

[`TermsLookup`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L2342) 訊息接受下列欄位。請設定 `id_2` 或 `query` 其中之一，以識別查找文件。若兩者皆未設定，則會使用已棄用的 `id` 欄位。

| 欄位 | Protobuf 類型 | 說明 |
| :---- | :---- | :---- |
| `index` | `string` | 要從中取得詞彙的索引名稱。 |
| `path` | `string` | 查找文件中包含詞彙值的欄位路徑。 |
| `id_2` | `string` | 要從中取得詞彙的文件 ID。 |
| `query` | [`QueryContainer`](#querycontainer-fields) | 用來選取要從中取得詞彙之一份或多份文件的查詢。 |
| `routing` | `optional string` | 用於定位查找文件的路由值。 |
| `store` | `optional bool` | 是否從儲存欄位而非 `_source` 讀取詞彙值。 |
| `id` | `string` | **已棄用。**請改用 `id_2`。要從中取得詞彙的文件 ID。 |

#### TermsSetQuery 欄位

[`TermsSetQuery`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L2370) 訊息接受下列欄位。

| 欄位 | Protobuf 類型 | 說明 |
| :---- | :---- | :---- |
| `field` | `string` | 必要。要執行搜尋查詢的欄位。 |
| `terms` | `repeated string` | 必要。要在指定欄位中搜尋的詞彙陣列。 |
| `boost` | `optional float` | 用於降低或提高查詢相關性分數的浮點數。預設為 `1.0`。 |
| `x_name` | `optional string` | 用於查詢標記的查詢名稱。 |
| `minimum_should_match_field` | `optional string` | 指定所需相符詞彙數量的數值欄位名稱。 |
| `minimum_should_match_script` | `optional` [`Script`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L1171) | 傳回所需相符詞彙數量的指令碼。 |

#### WildcardQuery 欄位

[`WildcardQuery`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L1998) 訊息接受下列欄位。

| 欄位 | Protobuf 類型 | 說明 |
| :---- | :---- | :---- |
| `field` | `string` | 必要。要執行搜尋查詢的欄位。 |
| `boost` | `optional float` | 用於降低或提高查詢相關性分數的浮點數。預設為 `1.0`。 |
| `x_name` | `optional string` | 用於查詢標記的查詢名稱。 |
| `case_insensitive` | `optional bool` | 允許不區分大小寫的比對。預設為 `false`。 |
| `rewrite_deprecated` | `optional` [`MultiTermQueryRewrite`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L3652) | **已棄用。**請改用 `rewrite`。 |
| `value` | `optional string` | 用於比對指定欄位中詞彙的萬用字元模式。當 `wildcard` 未設定時為必要。 |
| `wildcard` | `optional string` | 用於比對指定欄位中詞彙的萬用字元模式。當 `value` 未設定時為必要。 |
| `rewrite` | `optional string` | 決定 OpenSearch 如何改寫查詢。請參閱[改寫參數值](#rewrite-parameter-values)。預設為 `constant_score`。 |

### 全文查詢欄位

下列章節說明各個全文查詢訊息的欄位。

下列章節說明各個全文查詢訊息的欄位。

#### MatchQuery 欄位

[`MatchQuery`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L2082) 訊息接受下列欄位。

| 欄位 | Protobuf 類型 | 說明 |
| :---- | :---- | :---- |
| `field` | `string` | 必要。要執行搜尋查詢的欄位。 |
| `query` | [`FieldValue`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L2637) | 必要。要用於搜尋的查詢字串。 |
| `boost` | `optional float` | 用於降低或提高查詢相關性分數的浮點數。預設為 `1.0`。 |
| `x_name` | `optional string` | 用於查詢標記的查詢名稱。 |
| `analyzer` | `optional string` | 用來對查詢字串文字進行斷詞的分析器。 |
| `auto_generate_synonyms_phrase_query` | `optional bool` | 指定是否為多詞項同義詞自動建立片語比對查詢。 |
| `fuzziness` | `optional` [`Fuzziness`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L2626) | 在判斷詞項是否與某個值相符時，將一個字轉換為另一個字所需的字元編輯次數（插入、刪除、替換或調換）。 |
| `fuzzy_rewrite_deprecated` | `optional` [`MultiTermQueryRewrite`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L3652) | **已棄用。**請改用 `fuzzy_rewrite`。 |
| `fuzzy_transpositions` | `optional bool` | 在模糊比對運算中加入相鄰字元的調換。預設為 `true`。 |
| `lenient` | `optional bool` | 忽略查詢與文件欄位之間的資料類型不符。預設為 `false`。 |
| `max_expansions` | `optional int32` | 查詢可擴展至的詞項數量上限。預設為 `50`。 |
| `minimum_should_match` | `optional` [`MinimumShouldMatch`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L2160) | 文件被視為相符所需的詞項相符數量。 |
| `operator` | `optional` [`Operator`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L3646) | 是所有詞項都必須相符（`AND`），還是只需一個詞項相符（`OR`）。預設為 `OR`。 |
| `prefix_length` | `optional int32` | 模糊比對中不予考慮的前置字元數量。預設為 `0`。 |
| `zero_terms_query` | `optional` [`ZeroTermsQuery`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L3606) | 指定當分析器移除所有詞項時，是不比對任何文件（`none`）還是比對所有文件（`all`）。預設為 `none`。 |
| `fuzzy_rewrite` | `optional string` | 決定 OpenSearch 如何改寫查詢。請參閱[改寫參數值](#rewrite-parameter-values)。預設為 `constant_score`。 |

#### MatchBoolPrefixQuery 欄位

[`MatchBoolPrefixQuery`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L2668) 訊息接受下列欄位。

| 欄位 | Protobuf 類型 | 說明 |
| :---- | :---- | :---- |
| `field` | `string` | 必要。要對其執行搜尋查詢的欄位。 |
| `query` | `string` | 必要。要在所提供欄位中搜尋的詞彙。最後一個詞彙會用於前置字元查詢。 |
| `boost` | `optional float` | 用來降低或提高查詢相關性分數的浮點數。預設為 `1.0`。 |
| `x_name` | `optional string` | 用於查詢標記的查詢名稱。 |
| `analyzer` | `optional string` | 用來將查詢字串文字斷詞的分析器。 |
| `fuzziness` | `optional` [`Fuzziness`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L2626) | 在判斷某個詞彙是否符合某個值時，將一個字變更為另一個字所需的字元編輯次數 (插入、刪除、取代或換位)。 |
| `fuzzy_rewrite_deprecated` | `optional` [`MultiTermQueryRewrite`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L3652) | **已棄用。** 請改用 `fuzzy_rewrite`。 |
| `fuzzy_transpositions` | `optional bool` | 在模糊處理作業中加入相鄰字元的互換。預設為 `true`。 |
| `max_expansions` | `optional int32` | 查詢可擴充的詞彙數上限。預設為 `50`。 |
| `minimum_should_match` | `optional` [`MinimumShouldMatch`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L2160) | 文件要被視為相符所需符合的詞彙數。 |
| `operator` | `optional` [`Operator`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L3646) | 所有詞彙都必須符合 (`AND`) 或只要有一個詞彙符合 (`OR`)。預設為 `OR`。 |
| `prefix_length` | `optional int32` | 模糊處理中不列入考量的前置字元數。預設為 `0`。 |
| `fuzzy_rewrite` | `optional string` | 決定 OpenSearch 如何重寫查詢。請參閱[改寫參數值](#rewrite-parameter-values)。預設為 `constant_score`。 |

#### MatchPhraseQuery 欄位

[`MatchPhraseQuery`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L2746) 訊息接受下列欄位。

| 欄位 | Protobuf 類型 | 說明 |
| :---- | :---- | :---- |
| `field` | `string` | 必要。要對其執行搜尋查詢的欄位。 |
| `query` | `string` | 必要。要用於搜尋的查詢字串。 |
| `boost` | `optional float` | 用來降低或提高查詢相關性分數的浮點數。預設為 `1.0`。 |
| `x_name` | `optional string` | 用於查詢標記的查詢名稱。 |
| `analyzer` | `optional string` | 用來將查詢字串文字斷詞的分析器。 |
| `slop` | `optional int32` | 查詢片語中允許字詞之間出現的其他字詞數。預設為 `0` (完全相符)。 |
| `zero_terms_query` | `optional` [`ZeroTermsQuery`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L3606) | 指定當分析器移除所有詞彙時，要不相符任何文件 (`none`) 或符合所有文件 (`all`)。預設為 `none`。 |

#### MatchPhrasePrefixQuery 欄位

[`MatchPhrasePrefixQuery`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L2719) 訊息接受下列欄位。

| 欄位 | Protobuf 類型 | 說明 |
| :---- | :---- | :---- |
| `field` | `string` | 必要。要對其執行搜尋查詢的欄位。 |
| `query` | `string` | 必要。要用於搜尋的查詢字串。 |
| `boost` | `optional float` | 用來降低或提高查詢相關性分數的浮點數。預設為 `1.0`。 |
| `x_name` | `optional string` | 用於查詢標記的查詢名稱。 |
| `analyzer` | `optional string` | 用來將查詢字串文字斷詞的分析器。 |
| `max_expansions` | `optional int32` | 查詢可擴充的詞彙數上限。預設為 `50`。 |
| `slop` | `optional int32` | 查詢片語中允許字詞之間出現的其他字詞數。預設為 `0` (完全相符)。 |
| `zero_terms_query` | `optional` [`ZeroTermsQuery`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L3606) | 指定當分析器移除所有詞彙時，要不相符任何文件 (`none`) 或符合所有文件 (`all`)。預設為 `none`。 |

#### MultiMatchQuery 欄位

[`MultiMatchQuery`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L2770) 訊息接受下列欄位。

| 欄位 | Protobuf 類型 | 說明 |
| :---- | :---- | :---- |
| `query` | `string` | 必要。要用於搜尋的查詢字串。 |
| `boost` | `optional float` | 用來降低或提高查詢相關性分數的浮點數。預設為 `1.0`。 |
| `x_name` | `optional string` | 用於查詢標記的查詢名稱。 |
| `analyzer` | `optional string` | 用來將查詢字串文字斷詞的分析器。 |
| `auto_generate_synonyms_phrase_query` | `optional bool` | 指定是否要為多詞項同義詞自動建立片語比對查詢。預設為 `true`。 |
| `fields` | `repeated string` | 要搜尋的欄位清單。 |
| `fuzzy_rewrite_deprecated` | `optional` [`MultiTermQueryRewrite`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L3652) | **已棄用。** 請改用 `fuzzy_rewrite`。 |
| `fuzziness` | `optional` [`Fuzziness`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L2626) | 在判斷某個詞彙是否符合某個值時，將一個字變更為另一個字所需的字元編輯次數 (插入、刪除、取代或換位)。 |
| `fuzzy_transpositions` | `optional bool` | 在模糊處理作業中加入相鄰字元的互換。預設為 `true`。 |
| `lenient` | `optional bool` | 忽略查詢與文件欄位之間的資料類型不符。預設為 `false`。 |
| `max_expansions` | `optional int32` | 查詢可擴充的詞彙數上限。預設為 `50`。 |
| `minimum_should_match` | `optional` [`MinimumShouldMatch`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L2160) | 文件要被視為相符所需符合的詞彙數。 |
| `operator` | `optional` [`Operator`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L3646) | 所有詞彙都必須符合 (`AND`) 或只要有一個詞彙符合 (`OR`)。預設為 `OR`。 |
| `prefix_length` | `optional int32` | 模糊處理中不列入考量的前置字元數。預設為 `0`。 |
| `slop` | `optional int32` | 查詢片語中允許字詞之間出現的其他字詞數。支援 `phrase` 與 `phrase_prefix` 查詢類型。 |
| `tie_breaker` | `optional float` | 介於 `0` 與 `1.0` 之間的因數，用來為符合多個查詢子句的文件指派更高的權重。 |
| `type` | `optional` [`TextQueryType`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L3596) | 多重比對查詢類型。有效值為 `best_fields`、`most_fields`、`cross_fields`、`phrase`、`phrase_prefix`、`bool_prefix`。預設為 `best_fields`。 |
| `zero_terms_query` | `optional` [`ZeroTermsQuery`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L3606) | 指定當分析器移除所有詞彙時，要不相符任何文件 (`none`) 或符合所有文件 (`all`)。預設為 `none`。 |
| `fuzzy_rewrite` | `optional string` | 決定 OpenSearch 如何重寫查詢。請參閱[改寫參數值](#rewrite-parameter-values)。預設為 `constant_score`。 |

#### MatchAllQuery 欄位

[`MatchAllQuery`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L2659) 訊息接受以下欄位。

| 欄位 | Protobuf 類型 | 說明 |
| :---- | :---- | :---- |
| `boost` | `optional float` | 用於降低或提高查詢相關性分數的浮點數。預設為 `1.0`。 |
| `x_name` | `optional string` | 用於查詢標記的查詢名稱。 |

#### MatchNoneQuery 欄位

[`MatchNoneQuery`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L2710) 訊息接受以下欄位。

| 欄位 | Protobuf 類型 | 說明 |
| :---- | :---- | :---- |
| `boost` | `optional float` | 用於降低或提高查詢相關性分數的浮點數。預設為 `1.0`。 |
| `x_name` | `optional string` | 用於查詢標記的查詢名稱。 |

### 複合查詢欄位

以下各節說明每個複合查詢訊息的欄位。

以下各節說明每個複合查詢訊息的欄位。

#### BoolQuery 欄位

[`BoolQuery`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L2133) 訊息接受以下欄位。

| 欄位 | Protobuf 類型 | 說明 |
| :---- | :---- | :---- |
| `boost` | `optional float` | 用於降低或提高查詢相關性分數的浮點數。預設為 `1.0`。 |
| `x_name` | `optional string` | 用於查詢標記的查詢名稱。 |
| `filter` | `repeated` [`QueryContainer`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L2142) | 必須出現在符合文件中的子句 (查詢)。查詢分數會被忽略。 |
| `minimum_should_match` | `optional` [`MinimumShouldMatch`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L2145) | 必須符合的 `should` 子句最小數量。 |
| `must` | `repeated` [`QueryContainer`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L2148) | 必須出現在符合文件中並計入分數的子句 (查詢)。 |
| `must_not` | `repeated` [`QueryContainer`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L2151) | 不得出現在符合文件中的子句 (查詢)。所有文件都會傳回 `0` 的分數。 |
| `should` | `repeated` [`QueryContainer`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L2154) | 應該出現在符合文件中的子句 (查詢)。 |
| `adjust_pure_negative` | `optional bool` | 確保查詢僅包含 `must_not` 子句時的正確行為。預設為 `true`。 |

#### ConstantScoreQuery 欄位

[`ConstantScoreQuery`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L2171) 訊息接受以下欄位。

| 欄位 | Protobuf 類型 | 說明 |
| :---- | :---- | :---- |
| `filter` | [`QueryContainer`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L1368) | 必要。文件必須符合才會出現在結果中的篩選查詢。 |
| `boost` | `optional float` | 用於降低或提高查詢相關性分數的浮點數。預設為 `1.0`。 |
| `x_name` | `optional string` | 用於查詢標記的查詢名稱。 |

#### FunctionScoreQuery 欄位

[`FunctionScoreQuery`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L2183) 訊息接受以下欄位。

| 欄位 | Protobuf 類型 | 說明 |
| :---- | :---- | :---- |
| `boost` | `optional float` | 用於降低或提高查詢相關性分數的浮點數。預設為 `1.0`。 |
| `x_name` | `optional string` | 用於查詢標記的查詢名稱。 |
| `boost_mode` | `optional` [`FunctionBoostMode`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L3626) | 決定計算出的函式分數如何與查詢分數合併。 |
| `functions` | `repeated` [`FunctionScoreContainer`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L2210) | 分數函式。每個項目可以設定 `filter`、`weight`，以及 `exp`、`gauss`、`linear`、`field_value_factor`、`random_score` 或 `script_score` 其中之一。 |
| `max_boost` | `optional float` | 函式可套用至文件分數的最大加權值。 |
| `min_score` | `optional float` | 將分數低於此門檻的文件從結果中排除。 |
| `query` | `optional` [`QueryContainer`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L1368) | 在套用分數函式之前用於選取文件的查詢。 |
| `score_mode` | `optional` [`FunctionScoreMode`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L3636) | 決定多個函式的分數如何合併為單一分數。 |

如需更多資訊，請參閱[函式分數查詢]({{site.url}}{{site.baseurl}}/query-dsl/compound/function-score/)。

### 連接查詢欄位

以下各節說明每個連接查詢訊息的欄位。

以下各節說明每個連接查詢訊息的欄位。

#### NestedQuery 欄位

[`NestedQuery`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L1602) 訊息接受以下欄位。

| 欄位 | Protobuf 類型 | 說明 |
| :---- | :---- | :---- |
| `path` | `string` | 必要。要搜尋的欄位路徑，或欄位路徑的陣列。 |
| `query` | [`QueryContainer`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L1368) | 必要。要在指定路徑內的巢狀物件上執行的查詢。 |
| `boost` | `optional float` | 用於降低或提高查詢相關性分數的浮點數。預設為 `1.0`。 |
| `x_name` | `optional string` | 用於查詢標記的查詢名稱。 |
| `ignore_unmapped` | `optional bool` | 設為 `true` 可忽略未對應的欄位，且不符合任何文件。預設為 `false`。 |
| `inner_hits` | `optional` [`InnerHits`](#innerhits-fields) | 若有提供，則傳回符合查詢的底層命中結果。 |
| `score_mode` | `optional` [`ChildScoreMode`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L3800) | 定義符合的內部文件分數如何影響父文件的分數。 |

### 地理查詢欄位

以下各節說明每個地理查詢訊息的欄位。

以下各節說明每個地理查詢訊息的欄位。

#### GeoBoundingBoxQuery 欄位

地理邊界框查詢會傳回地理點位於查詢中指定邊界框內的文件。[`GeoBoundingBoxQuery`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L1483) 訊息接受以下欄位。

| 欄位 | Protobuf 類型 | 說明 |
| :---- | :---- | :---- |
| `boost` | `optional float` | 用於降低或提高查詢相關性分數的浮點數。預設為 `1.0`。 |
| `x_name` | `optional string` | 用於查詢標記的查詢名稱。 |
| `type` | `optional` [`GeoExecution`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L3815) | 地理查詢的執行類型。 |
| `validation_method` | `optional` [`GeoValidationMethod`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L3662) | 驗證方法。有效值為 `IGNORE_MALFORMED`、`COERCE` 和 `STRICT`。預設為 `STRICT`。 |
| `ignore_unmapped` | `optional bool` | 指定是否忽略未對應的欄位。預設為 `false`。 |
| `bounding_box` | `map<string, `[`GeoBounds`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L1504)`>` | 定義邊界框的欄位名稱至地理邊界的對應。 |

#### GeoDistanceQuery 欄位

地理距離查詢會傳回包含地理座標點的文件，這些座標點位於所提供地理座標點的指定距離內。[`GeoDistanceQuery`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L1560) 訊息接受下列欄位。

| 欄位 | Protobuf 類型 | 說明 |
| :---- | :---- | :---- |
| `distance` | `string` | 必要。用於比對座標點的距離範圍。此距離是以指定座標點為圓心的圓半徑。 |
| `boost` | `optional float` | 用於降低或提高查詢相關性分數的浮點數。預設為 `1.0`。 |
| `x_name` | `optional string` | 用於標記查詢的查詢名稱。 |
| `distance_type` | `optional` [`GeoDistanceType`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L3750) | 指定如何計算距離。有效值為 `arc` 和 `plane`。預設為 `arc`。 |
| `validation_method` | `optional` [`GeoValidationMethod`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L3662) | 驗證方法。有效值為 `IGNORE_MALFORMED`、`COERCE` 和 `STRICT`。預設為 `STRICT`。 |
| `ignore_unmapped` | `optional bool` | 設為 `true` 可忽略未對應的欄位，且不比對任何文件。預設為 `false`。 |
| `unit` | `optional` [`DistanceUnit`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L3787) | 距離的測量單位。 |
| `location` | `map<string, `[`GeoLocation`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L1214)`>` | 欄位名稱與用於指定中心點的 `geolocations` 之間的對應。 |

### 特殊查詢欄位

下列各節說明每種特殊查詢訊息的欄位。

如需 `knn` 查詢欄位的相關資訊，請參閱 [k-NN (gRPC)]({{site.url}}{{site.baseurl}}/api-reference/grpc-apis/knn/)。

#### ScriptQuery 欄位

指令碼查詢會根據以 Painless 指令碼語言撰寫的自訂條件篩選文件。如需詳細資訊，請參閱 [Painless 指令碼語言]({{site.url}}{{site.baseurl}}/scripting/painless/)。[`ScriptQuery`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L1471) 訊息接受下列欄位。

| 欄位 | Protobuf 類型 | 說明 |
| :---- | :---- | :---- |
| `script` | [`Script`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L1171) | 必要。用於篩選文件而執行的指令碼。 |
| `boost` | `optional float` | 用於降低或提高查詢相關性分數的浮點數。預設為 `1.0`。 |
| `x_name` | `optional string` | 用於標記查詢的查詢名稱。 |

#### HybridQuery 欄位

混合查詢會將指定文件在多個查詢中的相關性分數合併為單一分數。[`HybridQuery`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L1453) 訊息接受下列欄位。

| 欄位 | Protobuf 類型 | 說明 |
| :---- | :---- | :---- |
| `boost` | `optional float` | 用於降低或提高查詢相關性分數的浮點數。預設為 `1.0`。 |
| `x_name` | `optional string` | 用於標記查詢的查詢名稱。 |
| `queries` | `repeated` [`QueryContainer`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L1368) | 包含一或多個查詢子句的陣列，用於比對文件。文件必須符合至少一個查詢子句，才會在結果中傳回。透過套用搜尋管線，將文件在所有查詢子句中的相關性分數合併為單一分數。查詢子句數量上限為 5。 |
| `pagination_depth` | `optional int32` | 混合查詢的分頁深度。 |
| `filter` | `optional` [`QueryContainer`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L1368) | 套用至混合查詢所有子查詢的篩選條件。 |

### AggregationContainer 欄位

`AggregationContainer` 定義要執行的彙總。在每個 `AggregationContainer` 訊息中，指定下列欄位中的一個，且只能指定一個。

 gRPC Search API 僅支援下列彙總類型：`max`、`min` 和 `terms`。
{: .note}

[`AggregationContainer`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L3026) 訊息封裝單一彙總定義，並接受下列欄位。

| 欄位 | Protobuf 類型 | 說明 |
| :---- | :---- | :---- |
| `meta` | [`ObjectMap`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L3890) | 附加至彙總的選用自訂中繼資料。 |
| `max` | [`MaxAggregation`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L3101) | [`max`]({{site.url}}{{site.baseurl}}/aggregations/metric/maximum/) 指標彙總。必須是唯一設定的彙總類型。 |
| `min` | [`MinAggregation`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L3115) | [`min`]({{site.url}}{{site.baseurl}}/aggregations/metric/minimum/) 指標彙總。必須是唯一設定的彙總類型。 |
| `terms_aggregation` | [`TermsAggregation`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L3179) | [`terms`]({{site.url}}{{site.baseurl}}/aggregations/bucket/terms/) 桶彙總，依詞項值將文件分組。必須是唯一設定的彙總類型。 |

### 通用訊息值

下列各節說明通用訊息類型使用的值。

#### Fuzziness

[`Fuzziness`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L2626) 訊息是 `oneof` 類型，接受下列值。

| 欄位 | Protobuf 類型 | 說明 |
| :---- | :---- | :---- |
| `string` | `string` | `AUTO` 根據詞項長度產生編輯距離。您可以選擇提供 `AUTO:[low],[high]`。 |
| `int32` | `int32` | `0`、`1` 或 `2`：允許的最大 [Levenshtein 距離](https://en.wikipedia.org/wiki/Levenshtein_distance)。 |

#### 改寫參數值

`wildcard`、`prefix`、`regexp`、`fuzzy` 和 `range` 等多詞項查詢會在內部展開為詞項集合。`rewrite` 和 `fuzzy_rewrite` 參數控制這些詞項展開的執行與評分方式。

rewrite 參數可讓您控制多詞項查詢的內部行為。

| 值 | 評分 | 效能 | 備註 |
| :---- | :---- | :---- | :---- |
| `constant_score` | 所有符合項目具有相同分數 | 最佳 | 預設模式，適合篩選條件。 |
| `scoring_boolean` | 以 TF/IDF 為基礎 | 中等 | 完整的相關性評分。 |
| `constant_score_boolean` | 使用布林結構且分數相同 | 中等 | 搭配 `must_not` 或 `minimum_should_match` 使用。 |
| `top_terms_<n>` | 對排名前 `<n>` 的詞項使用 TF/IDF | 高效率 | 將展開範圍截斷為分數最高的詞項。 |
| `top_terms_boost_<n>` | 靜態加權 | 快速 | 評分較不準確。 |
| `top_terms_blended_freqs_<n>` | 混合分數 | 均衡 | 評分與效率之間的最佳取捨。 |

{: .note}

#### MinimumShouldMatch

[`MinimumShouldMatch`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L2160) 訊息是一種 `oneof` 類型，可接受下列值。

| 欄位 | Protobuf 類型 | 說明 |
| :---- | :---- | :---- |
| `int32` | `int32` | 指定應符合之詞彙最小數量的整數。 |
| `string` | `string` | 指定百分比或組合的字串。請參閱[最小應符合數量]({{site.url}}{{site.baseurl}}/query-dsl/minimum-should-match/)。 |

#### FieldValue

[`FieldValue`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L2637) 訊息代表一個欄位值，可接受下列值。

| 欄位 | Protobuf 類型 | 說明 |
| :---- | :---- | :---- |
| `bool` | `optional bool` | 布林值。 |
| `general_number` | `optional` [`GeneralNumber`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L3915) | 數值。 |
| `string` | `optional string` | 字串值。 |
| `null_value` | `optional` [`NullValue`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L3925) | 空值。 |

#### InnerHits 欄位

[`InnerHits`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L1626) 訊息可接受下列欄位。

| 欄位 | Protobuf 類型 | 說明 |
| :---- | :---- | :---- |
| `name` | `optional string` | 在回應中用於該特定內部命中定義的名稱。 |
| `size` | `optional int32` | 在 `inner_hits` 中傳回的最大命中數。 |
| `from` | `optional int32` | 內部命中的起始文件偏移量。 |
| `collapse` | `optional` [`FieldCollapse`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L1974) | 依特定欄位值將搜尋結果分組。 |
| `docvalue_fields` | `repeated` [`FieldAndFormat`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L1965) | OpenSearch 應使用其 `doc_values` 傳回的欄位。 |
| `explain` | `optional bool` | 是否傳回 OpenSearch 如何計算文件分數的詳細資訊。預設為 `false`。 |
| `highlight` | `optional` [`Highlight`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L1728) | 醒目標示會強調結果中的搜尋詞彙。 |
| `ignore_unmapped` | `optional bool` | 指定如何處理未對應的欄位。預設為 `false`。 |
| `script_fields` | `map<string, `[`ScriptField`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L1677)`>` | 其值使用指令碼計算的自訂欄位。 |
| `seq_no_primary_term` | `optional bool` | 是否傳回每個命中文件最後一次操作的序號與主要分片任期。 |


以下所有範例都顯示可傳送至 `SearchService/Search` gRPC 方法的有效請求承載。

### 比對所有文件的查詢

`match_all` 查詢會傳回索引中的所有文件。例如，下列請求會從索引傳回最多 50 份文件：

```json
{
  "search_request_body": {
    "query": {
      "match_all": {}
    },
    "size": 50
  }
}
```
{% include copy.html %}

### 詞項查詢

`term` 查詢會將單一欄位與特定詞彙進行比對。例如，下列查詢會搜尋包含 `Rush` 一詞的標題：

```json
{
  "index": "my_index",
  "search_request_body": {
    "query": {
      "term": {
        "field": "title",
        "value": {
          "string_value": "Rush"
        },
        "case_insensitive": true
      }
    }
  }
}
```
{% include copy.html %}

### 多詞項查詢

`terms` 查詢會比對特定欄位包含清單中任一值的文件。例如，下列查詢會搜尋 ID 為 `61809` 與 `61810` 的行：

```json
{
  "search_request_body": {
    "query": {
      "terms": {
        "terms": {
          "line_id": {
            "value": {
              "field_value_array": [
                { "string": "61809" },
                { "string": "61810" }
              ]
            }
          }
        }
      }
    }
  }
}
```
{% include copy.html %}

### 使用詞項查閱的多詞項查詢

使用 `terms` 查閱的 `terms` 查詢是 `terms` 查詢的一種特殊形式，可讓您從叢集中的另一份文件取得用於篩選的詞項，而不必直接在查詢中指定。查閱文件由 `id_2`（文件 ID）或 `query`（選取一份或多份來源文件的查詢）識別。例如，下列請求會比對 `students` 索引中 `_id` 符合 ID 為 `class_1` 的 `classes` 文件之 `enrolled` 陣列中任一值的文件：

```json
{
  "search_request_body": {
    "query": {
      "terms": {
        "terms": {
          "_id": {
            "lookup": {
              "index": "classes",
              "id_2": "class_1",
              "path": "enrolled"
            }
          }
        }
      }
    }
  }
}
```
{% include copy.html %}

若要使用查詢而非 ID 來選取查閱文件，請使用 `query` 欄位：

```json
{
  "search_request_body": {
    "query": {
      "terms": {
        "terms": {
          "_id": {
            "lookup": {
              "index": "classes",
              "path": "enrolled",
              "query": {
                "match_all": {}
              }
            }
          }
        }
      }
    }
  }
}
```
{% include copy.html %}

已棄用的 `id` 欄位在 `id_2` 與 `query` 皆未設定時，仍會為了回溯相容性而被接受：

```json
{
  "search_request_body": {
    "query": {
      "terms": {
        "terms": {
          "_id": {
            "lookup": {
              "index": "classes",
              "id": "class_1",
              "path": "enrolled"
            }
          }
        }
      }
    }
  }
}
```
{% include copy.html %}


### 不比對任何文件的查詢

`match_none` 查詢不會比對任何文件：

```json
{
  "search_request_body": {
    "query": {
      "match_none": {}
    }
  }
}
```
{% include copy.html %}

## 回應欄位

gRPC Search API 會傳回下列回應欄位。

### SearchResponse 欄位

下表列出 [`SearchResponse`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L262) 訊息支援的欄位。

來源文件以位元組傳回。請使用 Base64 解碼來讀取 gRPC 回應中的 `_source` 欄位。
{: .note}

| 欄位 | Protobuf 類型 | 說明 |
| :---- | :---- | :---- |
| `took` | `int64` | 處理搜尋請求所花費的時間，單位為毫秒。 |
| `timed_out` | `bool` | 搜尋是否逾時。 |
| `x_shards` | [`ShardStatistics`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L1311) | 分片層級的成功/失敗/總計中繼資料。 |
| `phase_took` | [`PhaseTook`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L330) | 回應中的階段層級 `took` 時間值。 |
| `hits` | [`HitsMetadata`](#hitsmetadata-fields) | 主要文件結果與中繼資料。 |
| `processor_results` | `repeated` [`ProcessorExecutionDetail`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L306) | 處理器執行詳細資訊。 |
| `x_clusters` | [`ClusterStatistics`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L471) | 搜尋遠端叢集時，每個叢集上搜尋的相關資訊。 |
| `fields` | [`ObjectMap`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L3890) | **已棄用。** 在搜尋回應中擷取特定欄位。 |
| `num_reduce_phases` | `int32` | 協調節點彙總分片回應批次的次數。 |
| `profile` | [`Profile`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L483) | 查詢執行的分析資料（偵錯/效能洞察）。 |
| `pit_id` | `string` | Point in Time ID。 |
| `x_scroll_id` | `string` | 搜尋及其搜尋上下文的識別碼。 |
| `terminated_early` | `bool` | 查詢是否提前終止。 |
| `aggregations` | `map<string, `[`Aggregate`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L3009)`>` | 隨搜尋回應一併傳回的彙總結果。 |

### Aggregate 欄位

[`Aggregate`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L3009) 訊息代表單一彙總結果，並接受下列欄位。

| 欄位 | Protobuf 類型 | 說明 |
| :---- | :---- | :---- |
| `dterms` | [`DoubleTermsAggregate`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L3040) | 具有雙精度值桶索引鍵的 `terms` 彙總。 |
| `lterms` | [`LongTermsAggregate`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L3066) | 具有帶正負號長整數桶索引鍵的 `terms` 彙總。 |
| `max` | [`SingleMetricAggregateBase`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L3129) | `max` 彙總的結果。 |
| `min` | [`SingleMetricAggregateBase`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L3129) | `min` 彙總的結果。 |
| `sterms` | [`StringTermsAggregate`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L3155) | 具有字串桶索引鍵的 `terms` 彙總。 |
| `ulterms` | [`UnsignedLongTermsAggregate`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L3268) | 具有不帶正負號長整數桶索引鍵的 `terms` 彙總。 |
| `umterms` | [`UnmappedTermsAggregate`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L3256) | 未對應欄位的 `terms` 彙總結果。 |

### HitsMetadata 欄位

`HitsMetadata` 物件包含搜尋結果的相關資訊，包括相符文件的總數，以及個別文件相符項目的陣列。其中包含下列欄位。

| 欄位 | Protobuf 類型 | 說明 |
| :---- | :---- | :---- |
| `total` | [`HitsMetadataTotal`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L351) | 相符文件總數的相關中繼資料 (value \+ relation)。 |
| `max_score` | [`HitsMetadataMaxScore`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L360) | 所傳回命中項目的最高相關性分數 (可能為 `null`)。 |
| `hits` | `repeated` [`HitsMetadataHitsInner`](#hitsmetadatahitsinner-fields) | 實際的相符文件清單。每個命中項目都包含核心欄位，例如 `index`、`id`、`score` 和 `source`，以及額外的選用欄位。 |

### HitsMetadataHitsInner 欄位

每個 `HitsMetadataHitsInner` 代表查詢所相符的單一文件，並包含下列欄位。

| 欄位 | Protobuf 類型 | 說明 |
| :---- | :---- | :---- |
| `x_type` | `string` | 文件類型。 |
| `x_index` | `string` | 包含所傳回文件的索引名稱。 |
| `x_id` | `string` | 文件在索引內的唯一 ID。 |
| `x_score` | [`HitXScore`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L395) | 命中項目的相關性分數。 |
| `x_explanation` | [`Explanation`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L826) | 說明 `_score` 如何計算的文字解釋。 |
| `fields` | [`ObjectMap`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L3890) | 文件欄位值。 |
| `highlight` | `map<string, `[`StringArray`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L1262)`>` | 每個命中項目的醒目提示欄位與片段。 |
| `inner_hits` | `map<string, `[`InnerHitsResult`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L389)`>` | 來自不同範圍、對整體查詢結果有貢獻的相符巢狀文件。 |
| `matched_queries` | `repeated string` | **已棄用。** 與文件相符的查詢名稱清單。 |
| `x_nested` | [`NestedIdentity`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L838) | 命中項目來源的內部巢狀物件路徑。 |
| `x_ignored` | `repeated string` | 已忽略欄位的清單。 |
| `ignored_field_values` | `map<string, `[`StringArray`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L1262)`>` | 來自文件原始 JSON 的未經處理原始值。 |
| `x_shard` | `string` | 擷取命中項目的來源分片 ID。 |
| `x_node` | `string` | 擷取命中項目的來源節點 ID。 |
| `x_routing` | `string` | 用於自訂分片路由的路由值。 |
| `x_source` | `bytes` | Base64 編碼的 `_source` 文件。 |
| `x_seq_no` | `int64` | 序號 (用於索引歷史記錄與版本控制)。 |
| `x_primary_term` | `int64` | 主要分片任期編號 (用於樂觀並行控制)。 |
| `x_version` | `int64` | 文件版本編號。 |
| `sort` | `repeated` [`FieldValue`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L2637) | 用於結果排序的排序值。 |
| `meta_fields` | [`ObjectMap`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L3890) | 文件的中繼資料值。 |
| `matched_queries_2` | [`HitMatchedQueries`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L2851) | 文件相符查詢名稱目前的 protobuf 表示法。 |

`source` 經過 Base64 編碼，必須解碼才能取得 JSON 文件。
{: .note}

## 範例回應

```json
{
  "response_body": {
    "took": 64,
    "timed_out": false,
    "shards": {
      "successful": 1,
      "total": 1
    },
    "hits": {
      "total": {
        "total_hits": {
          "relation": "TOTAL_HITS_RELATION_EQ",
          "value": 1
        }
      },
      "hits": [
        {
          "index": "my_index",
          "id": "3",
          "score": {
            "float_value": 1.0
          },
          "source": "eyAidGl0bGUiOiAiUnVzaCIsICJ5ZWFyIjogMjAxM30=",
          "meta_fields": {}
        }
      ],
      "max_score": {
        "float_value": 1.0
      }
    }
  }
}
```
{% include copy.html %}

## Java gRPC 用戶端範例

下列範例顯示 Java 用戶端程式，其會提交範例搜尋字詞查詢 gRPC 請求，然後列印搜尋回應中傳回的命中項目數：

```java
import org.opensearch.protobufs.*;
import io.grpc.ManagedChannel;
import io.grpc.ManagedChannelBuilder;

public class SearchClient {
    public static void main(String[] args) {
        ManagedChannel channel = ManagedChannelBuilder.forAddress("localhost", 9400)
            .usePlaintext()
            .build();

        SearchServiceGrpc.SearchServiceBlockingStub stub = SearchServiceGrpc.newBlockingStub(channel);

        // Create a term query
        TermQuery termQuery = TermQuery.newBuilder()
            .setField("director")
            .setValue(FieldValue.newBuilder().setStringValue("Nolan").build())
            .build();

        // Create query container
        QueryContainer queryContainer = QueryContainer.newBuilder()
            .setTerm(termQuery)
            .build();

        // Create search request body
        SearchRequestBody requestBody = SearchRequestBody.newBuilder()
            .setQuery(queryContainer)
            .setSize(5)
            .build();

        // Create search request
        SearchRequest request = SearchRequest.newBuilder()
            .addIndex("movies")
            .setSearchRequestBody(requestBody)
            .build();

        try {
            SearchResponse response = stub.search(request);

            // Handle the response
            System.out.println("Search took: " + response.getTook() + " ms");
            System.out.println("Timed out: " + response.getTimedOut());

            HitsMetadata hits = response.getHits();
            if (hits.hasTotal()) {
                System.out.println("Total hits: " + hits.getTotal().getTotalHits().getValue());
            }

            // Process individual hits
            for (HitsMetadataHitsInner hit : hits.getHitsList()) {
                System.out.println("Hit ID: " + hit.getXId());
                System.out.println("Hit Index: " + hit.getXIndex());
                if (hit.hasXScore()) {
                    System.out.println("Score: " + hit.getXScore().getDouble());
                }
            }
        } catch (io.grpc.StatusRuntimeException e) {
            System.err.println("gRPC search request failed with status: " + e.getStatus());
            System.err.println("Error message: " + e.getMessage());
        }

        channel.shutdown();
    }
}
```
{% include copy.html %}

## Python gRPC 用戶端範例

下列範例示範如何使用 Python 用戶端應用程式傳送相同的請求。

首先，使用 `pip` 安裝 `opensearch-protobufs` 套件：

```bash
pip install opensearch-protobufs==1.2.0
```
{% include copy.html %}

使用下列程式碼傳送請求：

```python
import grpc

from opensearch.protobufs.schemas import *
from opensearch.protobufs.services import SearchServiceStub


channel = grpc.insecure_channel(
    target="localhost:9400",
)

search_stub = SearchServiceStub(channel)

# Create a term query
term_query = TermQuery(
    field="field",
    value=FieldValue(string="value")
)
query_container = QueryContainer(term=term_query)

# Create a search request
request = SearchRequest(
    search_request_body=SearchRequestBody(query=query_container),
    index=["my-index"]
)

# Send request and handle response
try:
    response = search_stub.Search(request=request)
    if response.hits:
        print("Found {} hits".format(response.hits.total))
        print(response.hits)
    elif response.timed_out or response.terminated_early:
        print("Request timed out or terminated early")
    elif response.x_shards.failed:
        print("Some shards failed to execute the search")
        print(response.x_shards.failures)
except grpc.RpcError as e:
    if e.code() == StatusCode.UNAVAILABLE:
        print("Failed to reach server: {}".format(e))
    elif e.code() == StatusCode.PERMISSION_DENIED:
        print("Permission denied: {}".format(e))
    elif e.code() == StatusCode.INVALID_ARGUMENT:
        print("Invalid argument: {}".format(e))
finally:
    channel.close()
```
