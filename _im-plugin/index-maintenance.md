---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "索引維護"
nav_order: 10
redirect_from:
  - /dashboards/im-dashboards/forcemerge/
  - /dashboards/im-dashboards/rollover/
  - /dashboards/admin-ui-index/forcemerge/
  - /dashboards/admin-ui-index/rollover/
---

# 索引維護

OpenSearch 會在背景重新整理索引、排清 translog，並合併分段，因此大多數叢集完全不需要手動執行這些操作。當您需要在特定時刻取得結果時，請自行執行這些操作：在將文件編製索引後立即讓它可供搜尋、在建立快照前從已刪除的文件回收磁碟空間，或是變更已超出原始配置的索引分片數。

每項操作都可透過 [索引操作 API]({{site.url}}{{site.baseurl}}/api-reference/index-apis/index-operations/) 執行，且除了複製之外，也可從 OpenSearch Dashboards 的 **Index Management** 頁面執行。

如需建立、開啟、關閉及刪除索引等生命週期操作，請參閱 [索引操作]({{site.url}}{{site.baseurl}}/im-plugin/index-operations/)。

本頁的範例會操作名為 `logs-2026` 且具有兩個主要分片的索引，您可以使用下列請求建立該索引：

```json
PUT /logs-2026
{
  "settings": {
    "index.number_of_shards": 2,
    "index.number_of_replicas": 0
  }
}
```
{% include copy-curl.html %}

## 重新整理索引

重新整理會將記憶體內緩衝區中的文件寫入新的分段，使其可供搜尋。OpenSearch 預設每秒重新整理每個索引，因此文件在您將其編製索引後約一秒即可搜尋。當測試或用戶端需要在寫入文件後立即搜尋該文件時，請手動重新整理索引：

```json
POST /logs-2026/_refresh
```
{% include copy-curl.html %}

每次重新整理都會建立一個分段，因此在大量載入期間頻繁重新整理會拖慢索引編製。當您載入大量資料時，請在載入期間將 `index.refresh_interval` 設為 `-1`，並在結束時重新整理一次。如需詳細資訊，請參閱 [Refresh index]({{site.url}}{{site.baseurl}}/api-reference/index-apis/refresh/)。

重新整理僅適用於開啟的索引。

## 排清索引

排清會執行 Lucene 提交，將檔案系統快取中的分段寫入磁碟，並啟動新的 translog。這正是讓已編製索引的資料在節點重新啟動後仍能持久保存的原因。OpenSearch 會根據 translog 大小與存留時間自動排清：

```json
POST /logs-2026/_flush
```
{% include copy-curl.html %}

在為了維護而關閉節點之前，請手動排清，這樣復原時就不必重播大量的 translog。如需詳細資訊，請參閱 [Flush]({{site.url}}{{site.baseurl}}/api-reference/index-apis/flush/)。

排清僅適用於開啟的索引。

## 清除索引快取

OpenSearch 會快取欄位資料、查詢結果及請求層級的彙總結果，以加速重複的搜尋。清除這些快取可釋放堆積記憶體，但在快取重新填入之前，後續搜尋會變慢：

```json
POST /logs-2026/_cache/clear
```
{% include copy-curl.html %}

若要只清除其中一個快取而非全部，請使用 `fielddata`、`query` 或 `request` 查詢參數。如需詳細資訊，請參閱 [Clear cache]({{site.url}}{{site.baseurl}}/api-reference/index-apis/clear-index-cache/)。

清除快取僅適用於開啟的索引。

## 強制合併索引

OpenSearch 會將索引儲存為一組不可變的分段，並在背景將較小的分段合併為較大的分段。已刪除的文件只會被標示為已刪除；其空間會在包含該文件的分段合併時回收。強制合併會立即執行該合併，減少分段數量並清除已刪除的文件：

```json
POST /logs-2026/_forcemerge?max_num_segments=1
```
{% include copy-curl.html %}

強制合併的 I/O 成本很高，且可能產生自動合併原則永遠不會再合併的分段。請僅對不再接收寫入的索引執行，例如已輪替的時間序列索引。如需詳細資訊，請參閱 [Force merge]({{site.url}}{{site.baseurl}}/api-reference/index-apis/force-merge/)。

## 縮小索引

縮小會將索引複製到具有較少主要分片的新索引。若索引建立時的分片數超過其最終規模所需，請縮小該索引，因為現有索引的主要分片數無法就地變更。

首先，封鎖來源索引上的寫入操作。縮小仍接受寫入的索引會失敗並出現 `illegal_state_exception`：

```json
PUT /logs-2026/_settings
{
  "index.blocks.write": true
}
```
{% include copy-curl.html %}

接著縮小索引：

```json
POST /logs-2026/_shrink/logs-2026-shrunk
{
  "settings": {
    "index.number_of_shards": 1
  }
}
```
{% include copy-curl.html %}

來源索引必須符合下列條件：

- 索引為唯讀，且已設定寫入封鎖。請參閱 [封鎖]({{site.url}}{{site.baseurl}}/api-reference/index-apis/blocks/)。
- 每個分片都必須有一份位於同一個節點上的分片複本，可以是主要分片或副本分片。請使用 [分片配置篩選]({{site.url}}{{site.baseurl}}/api-reference/index-apis/shard-allocation/) 將這些分片移至同一節點。
- 來源索引的每個分片都已配置，也就是索引健康狀態不是紅色。
- 目標索引尚未存在。
- 來源索引的主要分片數多於目標索引，且目標分片數是來源分片數的因數。例如，具有 8 個主要分片的索引可縮小為 4、2 或 1。具有質數個分片（例如 7）的索引只能縮小為 1。
- 任何單一目標分片接收的文件數不得超過 2,147,483,519，這是 Lucene 分片可容納的上限。
- 執行縮小的節點有足夠的可用磁碟空間容納索引的第二份複本。

如需詳細資訊，請參閱 [縮小索引]({{site.url}}{{site.baseurl}}/api-reference/index-apis/shrink-index/)。

## 分割索引

分割會將索引複製到具有更多主要分片的新索引，將每個來源分片分割成數個目標分片。若索引已超出其原始分片數，且需要更多容量來因應資料量或查詢負載，請分割該索引。分割同樣需要在來源索引上設定寫入封鎖：

```json
PUT /logs-2026/_settings
{
  "index.blocks.write": true
}
```
{% include copy-curl.html %}

接著分割索引：

```json
POST /logs-2026/_split/logs-2026-split
{
  "settings": {
    "index.number_of_shards": 4
  }
}
```
{% include copy-curl.html %}

來源索引必須符合下列條件：

- 索引為唯讀，且已設定寫入封鎖。請參閱 [Blocks]({{site.url}}{{site.baseurl}}/api-reference/index-apis/blocks/)。
- 來源索引的每個分片都已配置，也就是索引健康狀態不是紅色。
- 目標索引尚未存在。
- 來源索引的主要分片數少於目標索引，且目標分片數是來源分片數的倍數。例如，具有 2 個主要分片的索引可分割為 4、6 或 8。具有 1 個主要分片的索引可分割為任意數量的分片。
- 執行分割的節點有足夠的可用磁碟空間容納索引的第二份複本。

如需詳細資訊，請參閱 [Split index]({{site.url}}{{site.baseurl}}/api-reference/index-apis/split/)。

## 複製索引

複製會將索引複製到具有相同主要分片數、對應及設定的新索引。若要在不動到原始索引的情況下，以實際資料測試對應或設定變更，請複製該索引。與縮小和分割一樣，複製需要在來源索引上設定寫入封鎖：

```json
PUT /logs-2026/_settings
{
  "index.blocks.write": true
}
```
{% include copy-curl.html %}

接著複製索引：

```json
POST /logs-2026/_clone/logs-2026-copy
```
{% include copy-curl.html %}

完成後，將 `index.blocks.write` 設為 `false` 以移除寫入封鎖。

如需詳細資訊，請參閱 [Clone index]({{site.url}}{{site.baseurl}}/api-reference/index-apis/clone/)。複製僅可透過 API 使用。

## 輪替索引

輪替 (rollover) 會建立一個新索引，並將寫入別名或資料串流重新導向至該索引，讓寫入作業繼續針對全新的索引進行，而前一個索引則變為唯讀。這樣可以讓個別的時間序列索引保持在可管理的大小，並讓您能透過刪除整個索引來刪除或封存舊資料。

輪替目標必須是[資料串流]({{site.url}}{{site.baseurl}}/im-plugin/data-streams/)，或是具有指定寫入索引的[索引別名]({{site.url}}{{site.baseurl}}/im-plugin/index-alias/)。請建立一個名稱以數字結尾的索引，並將寫入別名指向它：

```json
PUT /logs-000001
{
  "aliases": {
    "logs": {
      "is_write_index": true
    }
  }
}
```
{% include copy-curl.html %}

下列請求會在 `logs` 別名的寫入索引達到 50 GB、1,000 萬份文件或 7 天的索引齡時執行輪替：

```json
POST /logs/_rollover
{
  "conditions": {
    "max_size": "50gb",
    "max_docs": 10000000,
    "max_age": "7d"
  }
}
```
{% include copy-curl.html %}

新索引不會符合任何條件，因此回應會報告 `"rolled_over": false`。如需更多資訊，請參閱 [Roll over index]({{site.url}}{{site.baseurl}}/api-reference/index-apis/rollover/)。

若要改為依照排程輪替，而不是在符合條件時呼叫 API，請定義一個包含 `rollover` 動作的 [Index State Management 政策]({{site.url}}{{site.baseurl}}/im-plugin/ism/index/)。ISM 會為您評估條件，並在條件符合時輪替索引。

## OpenSearch Dashboards 中的索引維護

若要前往 **Index Management** 頁面，請在頂端選單中前往 **Management > Index Management**。所選索引的維護作業位於 **Indexes** 頁面的 **Actions** 選單中，如下圖所示。

![Indexes 頁面上的 Actions 選單]({{site.url}}{{site.baseurl}}/images/admin-ui-index/index-actions-menu.png)

這些程序會針對已存在的索引執行。若要建立索引，請參閱[建立索引]({{site.url}}{{site.baseurl}}/im-plugin/index-operations/#creating-an-index-1)。

### 重新整理、排清或清除快取

1. 在 **Index Management** 中，選取 **Indexes**、**Data streams** 或 **Aliases**。
1. 選用：選取您要套用此作業之每個項目旁的核取方塊。如果您未選取任何項目，作業將套用至所有項目。
1. 選取 **Actions**，然後選取 **Refresh**、**Flush** 或 **Clear cache**。
1. 在確認對話方塊中選取相同的選項。

對於別名和資料串流，這些作業會套用至已開啟的後端索引。

### 強制合併索引

1. 在 **Index Management** 中，選取 **Indexes**、**Data streams** 或 **Aliases**。
1. 選取 **Actions**，然後選取 **Force merge**。
1. 在 **Configure source index** 中，選取要合併的索引、資料串流或別名。
1. 選用：展開 **Advanced settings** 並設定下列任一選項：

   - 若要合併至特定數量的分段，請在 **Index segments** 中選取 **Manually set number of segments** 並輸入數量。輸入 `1` 可將每個分片合併為單一分段。
   - 若要在合併完成後排清索引，請選取 **Flush indexes**。
   - 若要清除已標記為刪除的文件，請選取 **Remove deleted documents**。

1. 選用：在 **Notifications** 中，選取 **Has failed / timed out**、**Has completed** 或兩者，以接收結果通知。
1. 選取 **Force merge**。

### 縮減索引

1. 在 **Index Management** 中，選取 **Indexes**。
1. 選取要縮減的索引，然後選取 **Actions > Shrink**。
1. 在 **Configure target index** 中，於 **Target index name** 輸入名稱。
1. 在 **Number of primary shards** 輸入新的主要分片數量，並在 **Number of replicas** 輸入副本數量。
1. 選用：在 **Index alias** 中為目標索引選取或輸入一或多個別名。
1. 選用：展開 **Advanced settings** 以新增通知。請參閱[傳送其他通知]({{site.url}}{{site.baseurl}}/im-plugin/notifications-settings/#sending-additional-notifications)。
1. 選取 **Shrink**。

如果來源索引不符合[縮減條件](#shrinking-an-index)，介面會提示您解決這些條件，包括在索引上設定寫入封鎖。

### 分割索引

1. 在 **Index Management** 中，選取 **Indexes**。
1. 選取要分割的索引，然後選取 **Actions > Split**。
1. 在 **Configure target index** 中，於 **Target index name** 輸入名稱。
1. 在 **Number of primary shards** 輸入新的主要分片數量，並在 **Number of replicas** 輸入副本數量。
1. 選用：在 **Index alias** 中為目標索引選取或輸入一或多個別名。
1. 選用：展開 **Advanced settings** 以新增通知。請參閱[傳送其他通知]({{site.url}}{{site.baseurl}}/im-plugin/notifications-settings/#sending-additional-notifications)。
1. 選取 **Split**。

### 輪替資料串流

1. 在 **Index Management** 中，選取 **Data streams**。
1. 選取 **Actions**，然後選取 **Roll over**。
1. 在 **Configure source** 中，選取要輪替的資料串流。
1. 選取 **Roll over**。

### 輪替別名

1. 在 **Index Management** 中，選取 **Aliases**。
1. 選取 **Actions**，然後選取 **Roll over**。
1. 在 **Configure source** 中，選取要輪替的別名。如果別名沒有寫入索引，系統會提示您指定一個。
1. 在 **Define index** 中，輸入新索引的名稱，並可選擇性地為它輸入別名。
1. 在 **Index settings** 中，輸入主要分片數量、副本數量以及重新整理間隔。
1. 選取 **Roll over**。

### 檢查長時間執行作業的狀態

重新編製索引、縮小及分割作業可能需要數十秒到數小時的時間，視涉及的資料量而定。由於每個作業都是一次性的非遞迴作業，您可以追蹤它直到完成：

1. 在 **Index Management** 中，選取 **Indexes**。
1. 尋找作業所套用的索引。
1. 從 **Status** 欄讀取作業的狀態。

## 相關文件

- [索引操作 API]({{site.url}}{{site.baseurl}}/api-reference/index-apis/index-operations/)
- [索引操作]({{site.url}}{{site.baseurl}}/im-plugin/index-operations/)
- [索引狀態管理]({{site.url}}{{site.baseurl}}/im-plugin/ism/index/)
- [長時間執行作業的通知]({{site.url}}{{site.baseurl}}/im-plugin/notifications-settings/)
