---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "搜尋設定"
parent: Configuring OpenSearch
nav_order: 80
---

# 搜尋設定

OpenSearch 提供多項設定，用於控制搜尋請求在叢集中的執行方式，包括請求限制、逾時與取消、scroll 與 Point in Time (PIT) 內容的存留時間，以及查詢與彙總的最佳化。

若要了解如何套用這些設定，請參閱[設定 OpenSearch]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/index/)。

OpenSearch 支援下列搜尋設定：

- `search.max_buckets`（動態，整數）：單一回應中允許的彙總桶 (bucket) 數量上限。預設為 `65535`。

- `search.phase_took_enabled`（動態，布林值）：啟用在搜尋回應中傳回階段層級的 `took` 時間值。預設為 `false`。

- `search.allow_expensive_queries`（動態，布林值）：允許或禁止高成本查詢。如需詳細資訊，請參閱[高成本查詢]({{site.url}}{{site.baseurl}}/query-dsl/index/#expensive-queries)。

- `search.query_rewriting.enabled`（動態，布林值）：啟用查詢改寫最佳化，可將查詢轉換為更有效率的形式，以提升搜尋效能。啟用後，OpenSearch 可以自動最佳化特定查詢模式，例如將針對同一欄位的多個 `term` 查詢合併為單一 `terms` 查詢。預設為 `false`。

- `search.query_rewriting.terms_threshold`（動態，整數）：控制觸發 `terms` 合併改寫器的門檻值，即針對同一欄位的 `term` 查詢數量達到此值時，會將其合併為單一 `terms` 查詢。例如，若設為 `16`（預設值），當布林子句中有 16 個以上的 term 查詢針對同一欄位時，這些查詢會合併為單一 `terms` 查詢，以獲得更佳的效能。最小值為 `2`。預設為 `16`。

- `search.query.max_query_string_length`（動態，整數）：query string 查詢允許的最大長度。此設定會拒絕超過指定限制的查詢字串，有助於避免效能問題。預設為 `32000`。

- `search.default_allow_partial_results`（動態，布林值）：叢集層級設定，允許在請求逾時或分片失敗時傳回部分搜尋結果。若搜尋請求包含 `allow_partial_search_results` 參數，則該參數的優先順序高於此設定。預設為 `true`。

- `search.node_level_query_fanout.enabled`（動態，布林值）：啟用節點層級的查詢扇出 (fan-out)。啟用後，協調節點會依目標資料節點將分片層級的 `query_then_fetch` 查詢與 `can_match` 請求分組，而不是針對每個分片各傳送一個傳輸請求。若搜尋請求包含 `node_level_query_fanout` 參數，則該參數的優先順序高於此設定。預設為 `false`。

<p id="index-pruning-settings"></p>

- `search.index_pruning.enabled`（動態，布林值）：啟用索引層級搜尋修剪，此修剪會在任何分片層級請求之前於協調節點上執行。如需詳細資訊，請參閱[索引層級搜尋修剪]({{site.url}}{{site.baseurl}}/search-plugins/index-level-search-pruning/)。預設為 `false`。

- `search.index_pruning.min_shards`（動態，整數）：OpenSearch 嘗試執行索引層級搜尋修剪前所需的作用中分片群組數量下限（一個主要分片及其副本計為一個群組）。預設為 `128`。

- `search.index_pruning.fields`（動態，清單）：可進行索引層級搜尋修剪的查詢欄位。OpenSearch 只會針對這些欄位擷取範圍限制條件。預設為 `[]`。

- `search.cancel_after_time_interval`（動態，時間單位）：叢集層級設定，用於在協調節點層級為所有搜尋請求設定預設逾時。達到指定時間後，請求會停止，且所有相關工作都會取消。預設為 `-1`（不逾時）。

- `search.default_search_timeout`（動態，時間單位）：叢集層級設定，指定搜尋請求在分片層級遭到取消前可執行的最長時間。若搜尋請求中指定了 `timeout` 間隔，則該間隔的優先順序高於已設定的設定值。預設為 `-1`。

- `search.default_keep_alive`（動態，時間單位）：指定 scroll 與 Point in Time (PIT) 搜尋的預設 keep alive 值。由於一個請求可能會多次到達同一分片（例如在查詢與擷取階段期間），OpenSearch 會開啟一個在請求整個期間都存在的_請求內容_，以確保每個個別分片請求的分片狀態一致。在標準搜尋中，擷取階段完成後，請求內容即會關閉。對於 scroll 或 PIT 搜尋，OpenSearch 會讓請求內容保持開啟，直到明確關閉為止（或直到達到 keep alive 時間）。背景執行緒會定期檢查所有開啟中的 scroll 與 PIT 內容，並刪除已超過 keep alive 逾時的內容。`search.keep_alive_interval` 設定指定檢查內容是否到期的頻率。`search.default_keep_alive` 設定為預設的到期期限。scroll 或 PIT 請求可以明確指定 keep alive，其優先順序高於此設定。預設為 `5m`。

- `search.keep_alive_interval`（靜態，時間單位）：決定 OpenSearch 檢查已超過 keep alive 限制之請求內容的間隔。預設為 `1m`。

- `search.max_keep_alive`（動態，時間單位）：指定 keep alive 值的上限。`max_keep_alive` 設定可作為安全檢查，用來檢查其他 `keep_alive` 設定（例如 `default_keep_alive`）以及請求層級的 keep alive 設定（適用於 scroll 與 PIT 內容）。無論哪種情況，若請求超過 `max_keep_alive` 值，作業都會失敗。預設為 `24h`。

- `search.low_level_cancellation`（動態，布林值）：啟用低層級請求取消。Lucene 的傳統逾時機制只會在收集搜尋結果時檢查時間。然而，高成本查詢（例如 wildcard 或 prefix）在開始收集結果之前，可能需要很長的時間進行展開。在此情況下，查詢的執行時間可能會超過逾時值。低層級取消機制可處理此情境，不僅在收集搜尋結果時會逾時，在查詢展開階段或執行任何 Lucene 作業之前也會逾時。預設為 `true`。

- `search.max_open_scroll_context`（動態，整數）：節點層級設定，指定節點開啟中的 scroll 內容數量上限。預設為 `500`。

- `search.request_stats_enabled`（動態，布林值）：從協調節點的角度開啟節點層級的階段計時統計資料收集。請求層級統計資料會追蹤搜尋請求在各個不同搜尋階段中（總共）花費的時間。您可以使用 [Nodes Stats API]({{site.url}}{{site.baseurl}}/api-reference/nodes-apis/nodes-stats/) 擷取這些計數器。預設為 `false`。

- `search.highlight.term_vector_multi_value`（靜態，布林值）：指定跨多值欄位的各個值來醒目提示片段。預設為 `true`。

- `search.max_aggregation_rewrite_filters`（動態，整數）：決定彙總期間允許的改寫篩選條件數量上限。將此值設為 `0` 可停用彙總的篩選條件改寫最佳化。這是實驗性功能，未來版本中可能會變更或移除。

- `search.dynamic_pruning.cardinality_aggregation.max_allowed_cardinality`（動態，整數）：決定在 cardinality 彙總中套用動態修剪的門檻值。若欄位的基數超過此門檻值，彙總會改回使用預設方法。這是實驗性功能，未來版本中可能會變更或移除。

- `search.aggregation.bucket_selection_strategy_factor`（動態，整數）：控制在 terms 彙總中用於選取前幾名桶的演算法。此係數決定何時使用優先佇列（較適合小型結果集），以及何時使用快速選擇（較適合大型結果集）。策略會依據條件 `size * factor < bucketsInOrd` 選擇。係數為 `0` 時一律使用優先佇列，而較高的值則會在較大的結果集中偏向使用快速選擇。有效值為 `0` 到 `10`（含）。預設為 `5`。

- `search.keyword_index_or_doc_values_enabled`（動態，布林值）：決定在 `keyword` 欄位上執行 `multi_term` 查詢時，要使用索引還是 doc values。預設值為 `false`。

## 指令碼設定

搜尋中使用的指令碼受指令碼大小、編譯與快取設定所管控。如需詳細資訊，請參閱[指令碼與資源設定]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/script-and-resource-settings/)。

## Point in Time 設定

如需 PIT 設定的相關資訊，請參閱 [PIT 設定]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/point-in-time/#pit-settings)。
