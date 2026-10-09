---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "索引操作"
nav_order: 5
redirect_from:
  - /dashboards/im-dashboards/index-management/
  - /dashboards/admin-ui-index/index-management/
---

# 索引操作

索引是 OpenSearch 中資料儲存的基本單位。在索引的生命週期中，您會建立索引、檢視其設定與統計資料、在變更靜態設定時關閉索引、重新開啟索引，最後刪除索引。您可以透過[核心索引 API]({{site.url}}{{site.baseurl}}/api-reference/index-apis/core-index-apis/) 或 OpenSearch Dashboards 的 **Index Management** 頁面執行這些操作。

有關重新整理、排清、強制合併、縮減與分割等維護操作的資訊，請參閱[索引維護]({{site.url}}{{site.baseurl}}/im-plugin/index-maintenance/)。

## 建立索引

您可以讓 OpenSearch 在將第一份文件編製索引時隱含地建立索引，也可以明確地建立索引，以便從一開始就控制其對應與設定。當您需要特定數量的分片、自訂的重新整理間隔，或與動態推斷結果不同的欄位對應時，請明確地建立索引。

下列請求會建立一個具有兩個主要分片、一個副本，並為 `timestamp` 欄位設定 `date` 對應的索引：

```json
PUT /logs-2026
{
  "settings": {
    "index": {
      "number_of_shards": 2,
      "number_of_replicas": 1
    }
  },
  "mappings": {
    "properties": {
      "timestamp": { "type": "date" },
      "message": { "type": "text" }
    }
  }
}
```
{% include copy-curl.html %}

所有可用的設定與對應，請參閱 [Create Index]({{site.url}}{{site.baseurl}}/api-reference/index-apis/create-index/)。若要將相同的設定與對應套用至名稱符合某個模式的所有索引，請使用[索引範本]({{site.url}}{{site.baseurl}}/im-plugin/index-templates/)。

索引名稱必須遵循[索引命名限制]({{site.url}}{{site.baseurl}}/im-plugin/#naming-restrictions-for-indexes)。

## 檢視索引資訊

若要擷取索引的設定、對應與別名，請使用 [Get Index API]({{site.url}}{{site.baseurl}}/api-reference/index-apis/get-index/)：

```json
GET /logs-2026
```
{% include copy-curl.html %}

若要檢查索引是否存在而不擷取它，請使用 [Index Exists]({{site.url}}{{site.baseurl}}/api-reference/index-apis/exists/)。若要將別名、資料串流或萬用字元運算式解析為其涵蓋的具體索引，請使用 [Resolve Index]({{site.url}}{{site.baseurl}}/api-reference/index-apis/resolve-index/)。若要取得文件數量、儲存大小與各項操作的指標，請使用 [Index Stats]({{site.url}}{{site.baseurl}}/api-reference/index-apis/stats/)。

## 關閉與開啟索引

已關閉的索引會拒絕讀取與寫入請求，並釋放其分片所使用的記憶體，但資料仍保留在磁碟上。當您需要變更只能在已關閉索引上更新的靜態設定時，或當您想保留不再被查詢的索引而不付出其記憶體成本時，請關閉索引。

若要關閉索引，請使用 [Close Index API]({{site.url}}{{site.baseurl}}/api-reference/index-apis/close-index/)：

```json
POST /logs-2026/_close
```
{% include copy-curl.html %}

若要讓索引再次可用，請使用 [Open Index API]({{site.url}}{{site.baseurl}}/api-reference/index-apis/open-index/)：

```json
POST /logs-2026/_open
```
{% include copy-curl.html %}

需要已關閉索引的設定清單，請參閱[索引設定]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/index-settings/)。

## 刪除索引

刪除索引會移除其文件、分片與中繼資料。請使用 [Delete Index API]({{site.url}}{{site.baseurl}}/api-reference/index-apis/delete-index/)：

```json
DELETE /logs-2026
```
{% include copy-curl.html %}

已刪除的索引無法復原，除非您從[快照]({{site.url}}{{site.baseurl}}/tuning-your-cluster/availability-and-recovery/snapshots/index/)還原它。
{: .warning}

若要依排程而非手動刪除索引，請定義一個包含 `delete` 動作的 [Index State Management 政策]({{site.url}}{{site.baseurl}}/im-plugin/ism/index/)。

## OpenSearch Dashboards 中的索引操作

若要前往 **Index Management** 頁面，請在頂端選單中前往 **Management > Index Management**。**Indexes** 頁面會列出叢集中的索引，並提供每個索引的下列資訊。

| 欄位 | 說明 |
| :--- | :--- |
| **Index** | 索引的名稱。 |
| **Health** | 索引的複寫狀態：綠色（所有主要與副本分片皆已指派）、黃色（至少一個副本分片未指派），或紅色（至少一個主要分片未指派）。 |
| **Managed by policy** | 是否有 Index State Management 政策直接或透過別名套用於該索引。 |
| **Status** | 索引是開啟還是關閉。 |
| **Total size** | 索引在所有主要與副本分片上使用的儲存空間。 |
| **Size of primaries** | 索引在所有主要分片上使用的儲存空間。 |
| **Total documents** | 索引中的文件數量。 |
| **Deleted documents** | 從索引中刪除的文件數量。 |
| **Primaries** | 主要分片的數量。 |
| **Replicas** | 每個主要分片的副本分片數量。 |

由於清單可能跨越多頁，請使用搜尋方塊依名稱尋找索引。

下圖顯示 **Indexes** 頁面。

![Indexes 頁面]({{site.url}}{{site.baseurl}}/images/admin-ui-index/indexes-list.png)

### 檢視索引詳細資訊

1. 在 **Index Management** 中，選取 **Indexes**。
1. 在 **Index** 欄位中選取索引名稱。

索引頁面會顯示包含索引指標的 **Overview** 面板，以及可編輯的 **Settings**、**Mappings** 與 **Alias** 索引標籤。若要返回清單，請在階層連結軌跡中選取 **Indexes**。

### 建立索引

1. 在 **Index Management** 中，選取 **Indexes**，然後選取 **Create Index**。
1. 在 **Define index** 中，輸入索引名稱。您也可以選擇為索引選取現有別名，或輸入要建立的新別名名稱。
1. 在 **Index settings** 中，輸入主要分片數量、副本數量與重新整理間隔。預設的重新整理間隔為 `1s`。若要以扁平 JSON 物件提供其他設定，請展開 **Advanced settings**。可用的選項請參閱[索引設定]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/index-settings/)。
1. 在 **Index mapping** 中，定義文件中的欄位。選取 **Visual editor** 逐一新增欄位，或選取 **JSON editor** 貼上現有對應。在視覺化編輯器中，選取 **Add new field** 或 **Add new object**，輸入欄位名稱，並選取欄位類型。對於物件欄位，選取 {::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/icons/plus-icon.png" class="inline-icon" alt="plus icon"/>{:/}（加號）圖示以新增巢狀欄位。此面板為選用；若留空，OpenSearch 會從您編製索引的前幾份文件推斷對應。
1. 選取 **Create**。您指定的任何新別名都會與索引一併建立。

若要建立[僅附加索引]({{site.url}}{{site.baseurl}}/im-plugin/append-only-index/)，請在建立索引前於 **Advanced settings** 中新增下列設定：

```json
"index.append_only.enabled": "true"
```
{% include copy.html %}

索引建立後無法轉換為或轉換自僅附加索引。
{: .warning}

### 編輯索引

1. 在 **Index Management** 中，選取 **Indexes**。
1. 在 **Index** 欄位中選取索引名稱。
1. 選取對應您要變更項目的索引標籤：

   - 若要變更副本數量或重新整理間隔，請選取 **Settings**。若要以扁平 JSON 物件提供其他設定，請展開 **Advanced settings**。您無法變更現有索引的主要分片數量；若要變更，請改為[縮減]({{site.url}}{{site.baseurl}}/im-plugin/index-maintenance/#shrinking-an-index-1)或[分割]({{site.url}}{{site.baseurl}}/im-plugin/index-maintenance/#splitting-an-index-1)索引。
   - 若要新增欄位或物件，請選取 **Mappings**。您無法變更現有欄位的名稱或類型。
   - 若要新增別名、選取現有別名或移除別名，請選取 **Alias**。若要移除別名，請選取其名稱旁的 {::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/icons/cross-icon.png" class="inline-icon" alt="cross icon"/>{:/}（叉號）圖示。

1. 選取 **Save**。

### 關閉索引

1. 在 **Index Management** 中，選取 **Indexes**。
1. 選取您要關閉之每個索引旁的核取方塊。
1. 選取 **Actions**，然後選取 **Close**。
1. 在確認對話方塊中輸入 `close`，然後選取 **Close**。

### 開啟索引

1. 在 **Index Management** 中，選取 **Indexes**。
1. 選取您要開啟之每個已關閉索引旁的核取方塊。
1. 選取 **Actions**，然後選取 **Open**。
1. 在確認對話方塊中選取 **Open**。

### 刪除索引

1. 在 **Index Management** 中，選取 **Indexes**。
1. 選取您要刪除之每個索引旁的核取方塊。
1. 選取 **Actions**，然後選取 **Delete**。
1. 在確認對話方塊中輸入 `delete`，然後選取 **Delete**。

### 套用政策

若要從索引清單將 Index State Management 政策附加至索引：

1. 在 **Index Management** 中，選取 **Indexes**。
1. 選取您要由政策管理之每個索引旁的核取方塊。
1. 選取 **Actions**，然後選取 **Apply policy**。
1. 從 **Policy ID** 選取一項政策。系統會顯示政策的預覽。
1. 若政策包含 `rollover` 動作，請在 **Rollover alias** 中輸入現有別名。
1. 選取 **Apply**。

如需更多資訊，請參閱[受管理的索引]({{site.url}}{{site.baseurl}}/im-plugin/ism/managedindexes/)。

### 權限與錯誤報告

權限是在 API 層級透過[權限]({{site.url}}{{site.baseurl}}/security/access-control/permissions/)與動作群組強制執行。OpenSearch Dashboards 不會新增額外的權限控制層：只要您有權存取 **Index Management** 頁面即可檢視它們，只要您有權呼叫對應的 API 即可完成操作。

立即失敗的操作會在介面中報告錯誤。執行時間較長的操作，則會在失敗發生時報告。您也可以在索引清單的 **Status** 欄位中檢查操作的狀態。如需更多資訊，請參閱[檢查長時間執行操作的狀態]({{site.url}}{{site.baseurl}}/im-plugin/index-maintenance/#checking-the-status-of-long-running-operations)。

## 相關文件

- [新增與管理您的資料]({{site.url}}{{site.baseurl}}/getting-started/manage-data/)
- [核心索引 API]({{site.url}}{{site.baseurl}}/api-reference/index-apis/core-index-apis/)
- [索引維護]({{site.url}}{{site.baseurl}}/im-plugin/index-maintenance/)
- [Index State Management]({{site.url}}{{site.baseurl}}/im-plugin/ism/index/)
