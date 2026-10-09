---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "重新編製索引資料"
nav_order: 35
redirect_from:
  - /im-plugin/reindex-data/index/
---

# 重新編製索引資料

有些變更無法直接在索引上進行。您無法變更現有欄位的類型、從對應中移除欄位，或變更主要分片的數量，除非重建索引。重新編製索引會將文件從一個或多個來源索引複製到具有您所需組態的目的地索引，因此您可以在不匯出資料並重新載入的情況下進行這些變更。

重新編製索引也是您將多個索引合併為一個、依查詢分割單一索引、對已儲存的文件套用資料匯入管線，或在叢集之間移動資料的方式。

重新編製索引會從來源索引的 `_source` 欄位讀取每份文件，並使用目的地的對應與設定將其編製索引至目的地索引。這會產生兩個結果：

- 來源索引必須啟用 `_source`。任何 `stored_fields` 組態都會被忽略。
- 目的地索引不會繼承來源索引的對應與設定。如果目的地索引不存在，OpenSearch 會根據複製的第一批文件推斷動態對應來建立它，這通常不是您想要的結果。請在開始之前，使用您所需的對應與設定建立它。

重新編製大型索引的 I/O 成本很高，且可能拖慢叢集上的搜尋。請在複製執行期間將目的地索引的 `number_of_replicas` 設為 `0`，並在之後還原，同時考慮對作業進行節流。如需更多資訊，請參閱[效能最佳化]({{site.url}}{{site.baseurl}}/api-reference/document-apis/reindex/#performance-optimization)。
{: .note}

## 重新編製索引

在最簡單的形式中，重新編製索引請求會指定來源與目的地。建立來源索引並在其中新增一份文件：

```json
POST my-source-index/_doc?refresh=true
{
  "title": "Spirited Away"
}
```
{% include copy-curl.html %}

然後將其複製到目的地索引：

```json
POST _reindex
{
  "source": {
    "index": "my-source-index"
  },
  "dest": {
    "index": "my-destination-index"
  }
}
```
{% include copy-curl.html %}

根據預設，請求會執行至完成，並傳回已複製文件的摘要。若要在背景執行，請將 `wait_for_completion` 設為 `false`；回應會包含一個任務 ID，您可以將其傳遞至 [Tasks API]({{site.url}}{{site.baseurl}}/api-reference/tasks/) 以查看進度，或用於[設定通知]({{site.url}}{{site.baseurl}}/im-plugin/notifications-settings/)。

[Reindex Documents API]({{site.url}}{{site.baseurl}}/api-reference/document-apis/reindex/) 記載了重新編製索引請求可執行的其他操作，包括下列各項：

- 複製由查詢選取的文件子集
- 將多個來源索引合併為一個目的地
- 從遠端叢集重新編製索引
- 略過目的地中已存在的文件
- 在複製期間使用指令碼或資料匯入管線轉換文件
- 將作業切片以平行執行

## 在 OpenSearch Dashboards 中重新編製索引資料

若要導覽至 **Index Management** 頁面，請前往頂端功能表的 **Management > Index Management**。

下圖顯示重新編製索引表單。

![重新編製索引表單]({{site.url}}{{site.baseurl}}/images/admin-ui-index/reindex-form.png)

若要重新編製索引，請依照下列步驟操作：

1. 您可以選擇先[建立目的地索引]({{site.url}}{{site.baseurl}}/im-plugin/index-operations/#creating-an-index-1)。您也可以在下列步驟中建立它，並從來源索引匯入設定與對應。
1. 在 **Index Management** 中，選取 **Indexes**。
1. 選取 **Actions**，然後選取 **Reindex**。
1. 在 **Configure source index** 中，選取要從中複製的索引、別名或資料串流。
1. 在 **Specify a reindex option** 中，選取 **Reindex all documents** 或 **Reindex a subset of documents**。
1. 如果您要重新編製文件子集的索引，請在 **Query expression** 中輸入[查詢]({{site.url}}{{site.baseurl}}/query-dsl/)以選取要複製的文件。例如，下列查詢會選取 `timestamp` 在 2024 年 1 月 1 日或之後的文件：

   ```json
   {
     "bool": {
       "filter": [
         { "range": { "timestamp": { "gte": "2024-01-01" }}}
       ]
     }
   }
   ```
   {% include copy.html %}

1. 在 **Configure destination index** 中，選取目的地。若要在此處建立它，請選取 **Create index**，輸入名稱，選擇性地選取別名，然後選取 **Import settings and mappings** 並選取來源索引以複製其組態。您可以在 **Index mapping** 中將欄位新增至目的地。
1. 您可以選擇展開 **Advanced settings** 並設定下列任何選項：

   - 若要略過 ID 已存在於目的地中的文件，請選取 **Reindex only unique documents**。
   - 若要避免版本衝突導致作業停止，請在 **Version conflicts** 中選取 **Ignore conflicts during reindexing**。
   - 若要將作業分割為平行子任務，請選取 **Slice this reindexing operation**。
   - 若要在每份文件寫入前套用[資料匯入管線]({{site.url}}{{site.baseurl}}/ingest-pipelines/)，請在 **Transform with ingest pipeline** 中選取該管線。
   - 若要收到結果通知，請選取 **Send additional notifications**。如需更多資訊，請參閱[傳送其他通知]({{site.url}}{{site.baseurl}}/im-plugin/notifications-settings/#sending-additional-notifications)。

1. 選取 **Reindex**。

重新編製索引可能需要很長的時間。若要追蹤其進度，請參閱[檢查長時間執行作業的狀態]({{site.url}}{{site.baseurl}}/im-plugin/index-maintenance/#checking-the-status-of-long-running-operations)。

來源與目的地必須不同。將索引重新編製索引至其本身會被拒絕；若要在原地更新文件，請使用 [Update By Query]({{site.url}}{{site.baseurl}}/api-reference/document-apis/update-by-query/)。
{: .note}

## 相關文件

- [Reindex Documents API]({{site.url}}{{site.baseurl}}/api-reference/document-apis/reindex/)
- [Update By Query]({{site.url}}{{site.baseurl}}/api-reference/document-apis/update-by-query/)
- [索引編解碼器]({{site.url}}{{site.baseurl}}/im-plugin/index-codecs/#reindexing)
- [長時間執行作業通知]({{site.url}}{{site.baseurl}}/im-plugin/notifications-settings/)
