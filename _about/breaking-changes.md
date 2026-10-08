---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "重大變更"
nav_order: 5
permalink: /breaking-changes/
---

# 重大變更

OpenSearch 採用[語意化版本控制](https://semver.org/)，這表示重大變更只會在主要版本之間引入。以下各節依版本列出 OpenSearch 中引入的重大變更。

<!-- vale off -->
## 1.x
<!-- vale on -->

OpenSearch 1.x 引入了下列重大變更。

### 遷移至 OpenSearch 與巢狀 JSON 物件數量的限制

當叢集中有任何文件在所有欄位中包含超過 10,000 個巢狀 JSON 物件時，從 Elasticsearch OSS 6.8 版遷移至 OpenSearch 1.x 版將會失敗。Elasticsearch 7.0 版引入了 `index.mapping.nested_objects.limit` 設定以防範記憶體不足錯誤，並將此設定的預設值設為 `10000`。OpenSearch 自創立之初便採用此設定，並強制執行對巢狀 JSON 物件的限制。然而，由於 Elasticsearch 6.8 中沒有此設定，該版本也無法辨識此設定，因此當任何文件中的巢狀 JSON 物件數量超過預設限制時，遷移至 OpenSearch 1.x 可能會產生相容性問題，導致 Elasticsearch 6.8 與 OpenSearch 1.x 版之間無法重新配置分片。

因此，我們建議您在嘗試從 Elasticsearch 6.8 遷移之前，先評估您的資料是否超出這些限制。


## 2.0.0

OpenSearch 2.0.0 引入了下列重大變更。

### 移除對應類型參數

`type` 參數已從所有 OpenSearch API 端點中移除。取而代之的是，可以依文件類型將索引分類。如需詳細資訊，請參閱 issue [#1940](https://github.com/opensearch-project/opensearch/issues/1940)。

### 棄用非包容性用語

非包容性用語在 2.x 版中已棄用，並將在 OpenSearch 3.0 中永久移除。我們使用下列替代用語：

<!-- vale off -->
- 「Whitelist」現在改為「Allow list」
- 「Blacklist」現在改為「Deny list」
- 「Master」現在改為「Cluster Manager」
<!-- vale on -->

<!-- vale off -->
### 新增 OpenSearch Notifications 外掛程式
<!-- vale on -->

在 OpenSearch 2.0 中，Alerting 外掛程式現在已與新的 Notifications 外掛程式整合。如果您想繼續使用 Alerting 外掛程式中的通知動作，請安裝新的後端外掛程式 `notifications-core` 和 `notifications`。如果您想在 OpenSearch Dashboards 中管理通知，請使用新的 `notificationsDashboards` 外掛程式。如需詳細資訊，請參閱 OpenSearch 文件頁面上的[通知]({{site.url}}{{site.baseurl}}/observing-your-data/notifications/index/)。

### 停止支援 JDK 8

由於 Lucene 升級，OpenSearch 不得不停止支援 JDK 8。因此，Java 高階 REST 用戶端不再支援 JDK 8。恢復 JDK 8 支援目前是一項 `opensearch-java` 提案 [#156](https://github.com/opensearch-project/opensearch-java/issues/156)，並且需要從 Java 用戶端中移除對 OpenSearch 核心的相依性（issue [#262](https://github.com/opensearch-project/opensearch-java/issues/262)）。


## 2.5.0

OpenSearch 2.5.0 引入了下列重大變更。

### 文字欄位的萬用字元查詢行為

OpenSearch 2.5 包含一項錯誤修正，修正了 `case_insensitive` 參數在文字欄位上用於 `wildcard` 查詢時的行為。因此，在此錯誤修正之前會忽略大小寫並錯誤傳回結果的文字欄位萬用字元查詢，將不會再傳回相同的結果。如需詳細資訊，請參閱 issue [#8711](https://github.com/opensearch-project/OpenSearch/issues/8711)。

## 2.18.0

OpenSearch 2.18.0 引入了下列重大變更。

### 預設 k-NN 引擎變更

預設的 k-NN 引擎已從 NMSLIB 變更為 Faiss。如果您使用 `space_type: "cosinesimil"` 且未明確指定引擎，您的向量現在會在編製索引時自動正規化為單位長度。這是因為 Faiss 原生不支援餘弦相似度，而是對正規化後的向量使用內積。因此，儲存的向量值將與輸入值不同，這可能會影響擷取及比較向量的程式碼。如果您的向量已經正規化，請考慮將 `space_type` 設為 `innerproduct` 而非 `cosinesimil`，以在明確控制正規化的情況下取得數學上等效的結果。如需詳細資訊，請參閱 pull request [#2221](https://github.com/opensearch-project/k-NN/pull/2221)。

## 2.19.0

OpenSearch 2.19.0 引入了下列重大變更。

### 文字嵌入處理器中的巢狀值支援
`text_embedding` 處理器在評估 `title_tmp:_ingest._value.title_embedding` 之類的欄位時，不再取代 `_ingest._value` 之類的巢狀值。您必須改為直接將巢狀鍵指定為 `books.title:title_embedding`，才能取得所需的輸出。如需詳細資訊，請參閱 issue [#1243](https://github.com/opensearch-project/neural-search/issues/1243)。

## 3.0.0

OpenSearch 3.0.0 引入了下列重大變更。

### JDK 需求

支援的最低 JDK 版本為 JDK 21。

### 版本相容性設定

`compatibility.override_main_response_version` 設定已移除。此功能已在 OpenSearch 1.x 中棄用，且不再受到支援。

如需詳細資訊，請參閱 issue [#18228](https://github.com/opensearch-project/OpenSearch/issues/18228)。

如需替代做法，請參閱[代理程式與匯入工具]({{site.url}}{{site.baseurl}}/tools/#agents-and-ingestion-tools)。

### 索引版本

不支援在早於 `2.x.x` 的版本中建立的索引（包括系統索引）。這些索引必須在**升級之前**重新編製索引。如需重新編製索引的相關資訊，請參閱[重新編製資料索引]({{site.url}}{{site.baseurl}}/im-plugin/reindex-data/)。

如需詳細資訊，請參閱 issue [#18717](https://github.com/opensearch-project/OpenSearch/issues/18717)。

### 系統索引存取

不再提供透過 REST API 存取系統索引的功能。此功能自 OpenSearch 1.x 起即已棄用。如需詳細資訊，請參閱 issue [#7936](https://github.com/opensearch-project/OpenSearch/issues/7936)。

### 文件 ID 長度限制

512 位元組的文件 ID 長度限制現在會在所有 API 中一致地強制執行，包括 Bulk API。先前，Bulk API 允許超過 512 位元組的文件 ID。如需詳細資訊，請參閱 issue [#6595](https://github.com/opensearch-project/OpenSearch/issues/6595)。

### 節點角色組態

使用環境變數設定空白節點角色的組態問題已修正。現在使用環境變數設定 `node.roles=` 會正確設定僅協調節點，與 `opensearch.yml` 組態一致。如需詳細資訊，請參閱 issue [#3412](https://github.com/opensearch-project/OpenSearch/issues/3412)。

### JSON 處理限制

OpenSearch 中的 JSON 處理（使用 Jackson 程式庫）全面引入了新的預設限制：

- JSON 物件和陣列的最大巢狀深度限制為 1,000 層。
- JSON 屬性名稱的最大長度限制為 50,000 個單位（位元組或字元，取決於輸入來源）。

這些限制有助於防止潛在的記憶體問題和阻斷服務攻擊。如需詳細資訊，請參閱 issue [#11278](https://github.com/opensearch-project/OpenSearch/issues/11278)。

### 巢狀查詢深度

新增了 `index.query.max_nested_depth` 設定，其預設值為 `20`，最小值為 `1`，用於限制 `nested` 查詢的最大巢狀層級數。如需詳細資訊，請參閱問題 [#3268](https://github.com/opensearch-project/OpenSearch/issues/3268)。

### 執行緒集區設定

下列已淘汰的執行緒集區設定已移除：
- `thread_pool.test.max_queue_size`
- `thread_pool.test.min_queue_size`
如需詳細資訊，請參閱問題 [#2595](https://github.com/opensearch-project/OpenSearch/issues/2595)。

### 索引儲存設定

作為 `hybridfs` 檔案處理改進的一部分，`index.store.hybrid.mmap.extensions` 設定已移除。如需詳細資訊，請參閱提取請求 [#9392](https://github.com/opensearch-project/OpenSearch/pull/9392)。

### Transport NIO 外掛程式

`transport-nio` 外掛程式已移除。Netty 仍是節點對節點以及用戶端對伺服器通訊的標準網路框架。如需詳細資訊，請參閱問題 [#16887](https://github.com/opensearch-project/OpenSearch/issues/16887)。

### Nodes API 回應格式

Nodes API 回應中索引緩衝區值的格式已變更：

- `total_indexing_buffer_in_bytes` 現在顯示原始位元組（例如 `53687091`）。
- `total_indexing_buffer` 現在以人類可讀的格式顯示（例如 `51.1mb`）。

如需詳細資訊，請參閱提取請求 [#17070](https://github.com/opensearch-project/OpenSearch/pull/17070)。

### PathHierarchy 斷詞器

駝峰式命名的 `PathHierarchy` 斷詞器名稱已淘汰，改用蛇形命名的 `path_hierarchy`。如需詳細資訊，請參閱提取請求 [#10894](https://github.com/opensearch-project/OpenSearch/pull/10894)。

### Security 外掛程式

Blake2b 雜湊實作現在會正確使用 salt 參數，因此產生的雜湊值會與先前版本不同（但為正確值）。如需詳細資訊，請參閱提取請求 [#5089](https://github.com/opensearch-project/security/pull/5089)。

### k-NN 外掛程式

下列已淘汰的設定已從 k-NN 外掛程式中移除：

- `knn.plugin.enabled` 設定
- `index.knn.algo_param.ef_construction` 索引設定
- `index.knn.algo_param.m` 索引設定
- `index.knn.space_type` 索引設定

NMSLIB 引擎現已淘汰。建議您改用 Faiss 或 Lucene 引擎。

如需詳細資訊，請參閱提取請求 [#2564](https://github.com/opensearch-project/k-NN/pull/2564)。

### Performance Analyzer 外掛程式

`performance-analyzer-rca` 代理程式已移除。建議您改用 [Telemetry 外掛程式](https://github.com/opensearch-project/performance-analyzer/issues/585) 進行效能監控與分析。Telemetry 外掛程式採用 OpenTelemetry 框架，可與輕量級開放原始碼代理程式無縫整合，以將效能指標發布至可觀測性儲存區。如需詳細資訊，請參閱問題 [#591](https://github.com/opensearch-project/performance-analyzer-rca/issues/591)。

### SQL 外掛程式

- OpenSearch 查詢領域特定語言 (DSL) 回應格式已移除。
- `DELETE` 陳述式支援已移除。
- `plugins.sql.delete.enabled` 設定已移除。
- 舊版 Spark Connector 模組已淘汰。如需連線至 Spark 的相關資訊，請參閱 [`async-query-core`](https://github.com/opensearch-project/sql/blob/main/async-query-core/README.md)。
- 已淘汰的 OpenDistro 端點以及帶有 `opendistro` 前綴的舊版設定已移除。
- `plugins.sql.pagination.api` 已移除，Scroll API 已淘汰。分頁現在預設使用 Point in Time。

如需詳細資訊，請參閱問題 [#3248](https://github.com/opensearch-project/sql/issues/3248)。

### OpenSearch Dashboards

- Discover 體驗：

    - `discover:newExperience` 設定已移除。
    - DataGrid 表格功能已移除。

    如需詳細資訊，請參閱提取請求 [#9511](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/9511)。

- 視覺化：`dashboards-visualizations` 外掛程式（包括甘特圖視覺化）已移除。建議您改用：

    - Vega 視覺化，以滿足彈性的視覺化需求。
    - 追蹤分析，以處理與追蹤相關的使用案例。

    如需詳細資訊，請參閱問題 [#430](https://github.com/opensearch-project/dashboards-visualizations/issues/430)。

### Dashboards Observability 外掛程式

舊版筆記本功能已從 `dashboards-observability` 中移除。主要變更包括：

- 不再支援舊版筆記本（先前儲存在 `.opensearch-observability` 索引中）。
- 僅支援儲存在 `.kibana` 索引中的筆記本（於 2.17 版推出）。
- 升級至 3.0 版之前，您必須先將筆記本遷移至新的儲存系統。

如需詳細資訊，請參閱問題 [#2350](https://github.com/opensearch-project/dashboards-observability/issues/2350)。

### 可搜尋快照節點角色

使用可搜尋快照的節點必須具備 `warm` 節點角色。主要變更包括：

- `search` 角色不再支援可搜尋快照。
- 處理可搜尋快照分片的節點必須指派 warm 角色。
- 如果您的叢集使用可搜尋快照，則必須在升級至 3.0 版之前更新節點角色組態。

如需詳細資訊，請參閱提取請求 [#17573](https://github.com/opensearch-project/OpenSearch/pull/17573)。

### 查詢群組

查詢群組已重新命名為**工作負載群組**。主要變更包括：

- `wlm/query_group` 端點現在為 `wlm/workload_group` 端點。
- API 回應 `workloadGroupID`，而非 `queryGroupID`。
- 所有工作負載管理叢集設定現在都會加上 `wlm.workload_group` 前綴。

如需詳細資訊，請參閱提取請求 [#9813](https://github.com/opensearch-project/OpenSearch/pull/17901)。

### ML Commons 外掛程式

- `CatIndexTool` 已移除，改用 `ListIndexTool`。

### 羅馬尼亞文分析

`romanian` 分析器現在支援現代 Unicode 形式的羅馬尼亞文，並會將下加符 (cedilla) 字元正規化為對應的逗號形式字元。由於兩種形式目前仍在使用中，建議您為現有的羅馬尼亞文文件重新編製索引，以確保分析與搜尋行為一致。

