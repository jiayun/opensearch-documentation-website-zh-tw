---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "文件 API"
has_children: true
has_toc: false
nav_order: 50
redirect_from:
  - /opensearch/rest-api/document-apis/index/
  - /api-reference/document-apis/
---

# 文件 API
**於 1.0 版導入**
{: .label .label-purple }

文件 API 讓您能對儲存在索引中的文件執行建立、讀取、更新與刪除 (CRUD) 操作。您可以使用這些 API 管理個別文件，或在批次操作中有效率地處理多個文件。

## 操作類型

OpenSearch 文件 API 依其處理的文件數量分為下列幾類。

### 單一文件操作

單一文件操作一次處理一份文件。當您需要對特定文件執行目標式操作，或處理個別記錄時，請使用這些 API：

- 使用 Index Document API 新增文件，或以相同 ID 取代現有文件。
- 使用 Get Document API 依唯一 ID 取得文件。
- 使用 Update Document API 變更現有文件中的特定欄位，而無需重新編製整份文件的索引。
- 使用 Delete Document API 從索引中移除文件。

### 多文件操作

多文件操作在單一 API 請求中處理多個文件，相較於提交個別請求具有顯著的效能優勢。處理大型資料集或批次操作時，請一律優先使用多文件 API，因為它們：

- 將多個操作合併為一個請求，降低網路負擔。
- 讓 OpenSearch 能夠最佳化批次處理，提升輸送量。
- 減少應用程式與叢集之間的往返次數。

請在資料匯入管線、大量更新、批次刪除，以及任何需要有效率處理多個文件的情境中使用多文件操作。

### 詞向量操作

詞向量操作會擷取特定文件欄位中詞彙的資訊，包括詞頻、位置與位移。請將這些操作用於文字分析、相關性評分與自訂相似度計算。

## 重要注意事項

**單一索引限制**：所有文件 API 一次只能操作一個索引。`index` 參數只接受一個索引名稱，或指向單一索引的別名。您無法在單一文件 API 請求中指定多個索引。若要跨多個索引操作，您必須為每個索引分別提交請求。

**文件路由**：OpenSearch 使用路由演算法決定每份文件儲存在哪個分片。預設情況下，文件會依其 ID 進行路由，但您可以指定自訂路由值來控制分片放置。當您擷取、更新或刪除以自訂路由編製索引的文件時，必須提供相同的路由值。

## 資料複寫模型

OpenSearch 會在多個分片間維護資料的多份複本，以確保容錯能力與高可用性。此複寫模型以主要-備援模式為基礎，其中一份分片複本作為主要分片，其他複本則作為副本分片。

### 寫入操作

當您對文件編製索引、更新或刪除文件時，OpenSearch 會遵循以下流程：

1. **路由**：操作會依據文件 ID 或自訂路由值被路由到適當的主要分片。
2. **主要分片處理**：主要分片在本機驗證並執行該操作。
3. **複寫**：主要分片將操作平行轉送給所有作用中的副本分片。
4. **確認**：在所有同步中的副本分片確認操作後，主要分片才向用戶端回報成功。

此流程確保所有分片複本保持同步，並確保已確認的寫入在多個節點上具有持久性。

### 讀取操作

讀取操作可由任何分片複本（主要分片或副本分片）提供服務，這帶來幾項好處：

- **負載分散**：讀取請求會分散到多個分片複本，提升輸送量與回應時間。
- **高可用性**：若某個分片複本無法使用，OpenSearch 會自動將請求路由到其他複本。
- **一致性**：所有分片複本都包含相同的資料（進行中的操作除外），確保讀取結果一致。

預設情況下，OpenSearch 使用輪流分配方式選擇由哪個分片複本處理每個讀取請求。您可以透過許多文件 API 提供的 `preference` 參數影響此選擇。

## 重新整理行為

Index、Update、Delete 與 Bulk API 支援 `refresh` 參數，用於控制變更何時對搜尋操作可見。了解重新整理行為對於在資料新鮮度與系統效能之間取得平衡非常重要。

### 重新整理參數值

`refresh` 參數接受下列值：

- `false`（預設）：不執行任何與重新整理相關的動作。變更會在索引依據 `index.refresh_interval` 設定自動重新整理時變為可見（預設為 1 秒）。
- `true`：在操作完成後立即重新整理相關的主要分片與副本分片，讓變更立即對搜尋可見。請謹慎使用此選項，因為它可能對效能造成顯著影響。
- `wait_for`：在回應用戶端之前，等待變更透過重新整理變為可見。此選項不會強制立即重新整理，而是等待下一次排定的重新整理，或等待其他操作觸發重新整理。

### 選擇合適的重新整理設定

對大多數使用情境而言，請使用預設的 `refresh=false` 以獲得最佳效能。請參考下列準則：

- **使用 `false`（預設）**：適用於高輸送量索引作業，且可接受近即時可見性（1 秒內）的情況。
- **使用 `wait_for`**：當您需要確認變更已可搜尋，但不希望強制立即重新整理時。對批次操作而言，此選項比 `refresh=true` 更有效率。
- **謹慎使用 `true`**：僅在您確實需要立即可見性，並了解其效能影響時使用。頻繁的重新整理會產生效率不佳的索引區段，需要更多資源才能搜尋與合併。

過度使用 `refresh=true` 會產生大量小型區段並增加合併負擔，進而顯著降低叢集效能。

## 樂觀並行控制

OpenSearch 使用樂觀並行控制，確保文件更新不會以較舊的資料覆寫較新的變更。在多個操作可能同時發生的分散式系統中，此機制至關重要。

每個變更文件的操作都會由負責的主要分片指派一個序號 (`_seq_no`) 與一個主要任期 (`_primary_term`)：

- **序號**：指派給每個操作的嚴格遞增數字。較新的操作的序號一律高於較舊的操作。
- **主要任期**：識別目前的主要分片指派。當故障後選出新主要分片時，此值會改變。

`_seq_no` 與 `_primary_term` 共同唯一識別文件的每次變更，讓 OpenSearch 能夠偵測並防止順序錯亂的更新。

### 使用序號進行條件式更新

您可以將 `if_seq_no` 與 `if_primary_term` 參數搭配 Index、Update 與 Delete API 使用，確保只有在文件自您擷取後未曾變更時，操作才會成功。OpenSearch 會在 Get API 回應與搜尋結果中（若有要求）傳回目前的 `_seq_no` 與 `_primary_term` 值。

此做法可防止多個用戶端或程序同時修改同一份文件時發生更新遺失。若序號或主要任期與目前值不符，OpenSearch 會回傳版本衝突錯誤，讓您的應用程式能以最新的文件版本重試該操作。

## 單一文件操作

- [編製文件索引]({{site.url}}{{site.baseurl}}/api-reference/document-apis/index-document/)
- [取得文件]({{site.url}}{{site.baseurl}}/api-reference/document-apis/get-documents/)
- [更新文件]({{site.url}}{{site.baseurl}}/api-reference/document-apis/update-document/)
- [刪除文件]({{site.url}}{{site.baseurl}}/api-reference/document-apis/delete-document/)

## 多文件操作

- [大量操作 (Bulk)]({{site.url}}{{site.baseurl}}/api-reference/document-apis/bulk/)
- [串流大量操作 (Streaming bulk)]({{site.url}}{{site.baseurl}}/api-reference/document-apis/bulk-streaming/)
- [多重取得文件]({{site.url}}{{site.baseurl}}/api-reference/document-apis/multi-get/)
- [依查詢更新]({{site.url}}{{site.baseurl}}/api-reference/document-apis/update-by-query/)
- [依查詢刪除]({{site.url}}{{site.baseurl}}/api-reference/document-apis/delete-by-query/)
- [重新編製文件索引]({{site.url}}{{site.baseurl}}/api-reference/document-apis/reindex/)

## 詞向量操作

- [詞向量]({{site.url}}{{site.baseurl}}/api-reference/document-apis/termvector/)
- [多重詞向量]({{site.url}}{{site.baseurl}}/api-reference/document-apis/mtermvectors/)

## 提取式資料匯入

- [提取式資料匯入]({{site.url}}{{site.baseurl}}/api-reference/document-apis/pull-based-ingestion/)
