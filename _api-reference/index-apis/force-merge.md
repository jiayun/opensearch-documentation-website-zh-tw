---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "強制合併"
parent: Index operations
grand_parent: Index APIs
nav_order: 40
---

# Force Merge API
**於 1.0 版導入**
{: .label .label-purple }

Force Merge API 操作會對一或多個索引的分片強制執行合併。對於資料串流，此 API 會對該串流後端索引的分片強制執行合併。

## 端點

```json
POST /_forcemerge
POST /{index}/_forcemerge/
```

## 合併操作

在 OpenSearch 中，分片是一個 Lucene 索引，由 _分段_（或分段檔案）組成。分段儲存已編製索引的資料。系統會定期將較小的分段合併為較大的分段，而較大的分段會變成不可變。合併可減少每個分片的分段總數，並釋放磁碟空間。

OpenSearch 會在背景執行分段合併，所產生的分段不會大於 `index.merge.policy.max_merged_segment`（預設為 5 GB）。

## 已刪除的文件

當文件從 OpenSearch 索引中刪除時，它並不會從 Lucene 分段中刪除，而只是被標記為待刪除。當分段檔案合併時，已刪除的文件會被移除（或 _清除_）。因此，合併也能釋放被標記為刪除的文件所佔用的空間。

## Force Merge API

除了定期合併之外，您也可以使用 Force Merge API 強制執行分段合併。

請只在所有傳送至索引的寫入請求都完成之後，才對該索引使用 Force Merge API。強制合併操作可能會產生非常大的分段。如果仍有寫入請求傳送至索引，合併原則在這些分段主要由已刪除文件組成之前，不會合併它們。這可能會增加磁碟空間使用量，並導致效能下降。
{: .warning}

當您呼叫 Force Merge API 時，呼叫會被阻擋直到合併完成。如果在此期間連線中斷，強制合併操作會繼續在背景執行。傳送至同一索引的新強制合併請求會被阻擋，直到目前執行中的合併操作完成為止。

## 強制合併多個索引

若要強制合併多個索引，您可以對下列索引組合呼叫 Force Merge API：

- 多個索引
- 包含多個後端索引的一或多個資料串流
- 指向多個索引的一或多個索引別名
- 叢集中的所有資料串流與索引

當您強制合併多個索引時，合併操作會在節點的每個分片上依序執行。當強制合併操作進行中時，分片的儲存空間會暫時增加，以便將所有分段重寫為一個新分段。當 `max_num_segments` 設定為 `1` 時，分片的儲存空間會暫時加倍。

## 強制合併資料串流

強制合併資料串流有助於管理資料串流的後端索引，尤其是在輪替操作之後。以時間為基礎的索引只在指定的時間期間內接收編製索引的請求。一旦該時間期間過去且索引不再接收寫入請求，您就可以將所有索引分片的分段強制合併為一個分段。對單一分段分片的搜尋效率更高，因為它們使用較簡單的資料結構。


## 路徑參數

下表列出可用的路徑參數。所有路徑參數皆為選用。

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `<index>` | 字串 | 以逗號分隔的索引、資料串流或索引別名清單，操作會套用至這些對象。支援萬用字元運算式（`*`）。使用 `_all` 或 `*` 可指定叢集中的所有索引與資料串流。 |

## 查詢參數

下表列出可用的查詢參數。所有查詢參數皆為選用。

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `allow_no_indices` | 布林值 | 若為 `false`，當任何萬用字元運算式或索引別名指向任何已關閉或遺失的索引時，請求會傳回錯誤。預設為 `true`。 |
| `expand_wildcards` | 字串 | 指定萬用字元運算式可展開至哪些索引類型。支援以逗號分隔的值。有效值為：<br> - `all`：展開至所有開啟與已關閉的索引，包括隱藏索引。<br> - `open`：展開至開啟的索引。<br> - `closed`：展開至已關閉的索引。<br> - `hidden`：展開時包含隱藏索引。必須與 `open`、`closed` 或兩者合併使用。<br> - `none`：不接受萬用字元運算式。<br> 預設為 `open`。 |
| `flush` | 布林值 | 在強制合併之後對索引執行排清。排清可確保檔案持續保存至磁碟。預設為 `true`。 |
| `ignore_unavailable` | 布林值 | 若為 `true`，OpenSearch 會忽略遺失或已關閉的索引。若為 `false`，當強制合併操作遇到遺失或已關閉的索引時，OpenSearch 會傳回錯誤。預設為 `false`。 |
| `max_num_segments` | 整數 | 較小分段要合併成的較大分段數量。將此參數設為 `1` 可將所有分段合併為一個分段。預設行為是視需要執行合併。 |
| `only_expunge_deletes` | 布林值 | 若為 `true`，合併操作只會針對已刪除文件比例達到特定百分比的分段，清除其中的已刪除文件。該百分比預設為 10%，並可透過 `index.merge.policy.expunge_deletes_allowed` 設定進行調整。在 OpenSearch 2.12 之前，`only_expunge_deletes` 會忽略 `index.merge.policy.max_merged_segment` 設定。從 OpenSearch 2.12 開始，使用 `only_expunge_deletes` 不會產生大於 `index.merge.policy.max_merged_segment` 的分段（預設為 5 GB）。如需更多資訊，請參閱[已刪除的文件](#deleted-documents)。預設為 `false`。 |
| `primary_only` | 布林值 | 若設為 `true`，合併操作只會在索引的主要分片上執行。當您想在合併完成後為索引建立快照時，這會很有用。快照只會從主要分片複製分段。合併主要分片可以減少資源消耗。預設為 `false`。 |
| `wait_for_completion` | 布林值 | 若為 `false`，OpenSearch 會以非同步方式執行強制合併操作，而不等待其完成。請求會立即傳回，工作會在背景繼續執行。您可以使用 [Tasks API]({{site.url}}{{site.baseurl}}/api-reference/tasks/) 監視其進度。預設為 `true`，表示操作以同步方式執行。 |

## 範例請求
<!-- spec_insert_start
component: example_code
rest: POST /.testindex-logs/_forcemerge?primary_only=true
body: 
-->
{% capture step1_rest %}
POST /.testindex-logs/_forcemerge?primary_only=true

{% endcapture %}

{% capture step1_python %}


response = client.indices.forcemerge(
  index = ".testindex-logs",
  params = { "primary_only": "true" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

下列範例示範如何使用 Force Merge API。

### 強制合併特定索引

下列範例強制合併特定索引：

<!-- spec_insert_start
component: example_code
rest: POST /testindex1/_forcemerge
-->
{% capture step1_rest %}
POST /testindex1/_forcemerge
{% endcapture %}

{% capture step1_python %}


response = client.indices.forcemerge(
  index = "testindex1"
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

### 強制合併多個索引

下列範例強制合併多個索引：

<!-- spec_insert_start
component: example_code
rest: POST /testindex1,testindex2/_forcemerge
body: 
-->
{% capture step1_rest %}
POST /testindex1,testindex2/_forcemerge

{% endcapture %}

{% capture step1_python %}


response = client.indices.forcemerge(
  index = "testindex1,testindex2"
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

### 強制合併所有索引

下列範例強制合併所有索引：

<!-- spec_insert_start
component: example_code
rest: POST /_forcemerge
body: 
-->
{% capture step1_rest %}
POST /_forcemerge

{% endcapture %}

{% capture step1_python %}

response = client.indices.forcemerge()
{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

### 將資料串流的後端索引強制合併為一個分段

下列範例將資料串流的後端索引強制合併為一個分段：

<!-- spec_insert_start
component: example_code
rest: POST /.testindex-logs/_forcemerge?max_num_segments=1
-->
{% capture step1_rest %}
POST /.testindex-logs/_forcemerge?max_num_segments=1
{% endcapture %}

{% capture step1_python %}


response = client.indices.forcemerge(
  index = ".testindex-logs",
  params = { "max_num_segments": "1" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

### 強制合併主要分片

下列範例強制合併索引的主要分片：

<!-- spec_insert_start
component: example_code
rest: POST /.testindex-logs/_forcemerge?primary_only=true
-->
{% capture step1_rest %}
POST /.testindex-logs/_forcemerge?primary_only=true
{% endcapture %}

{% capture step1_python %}


response = client.indices.forcemerge(
  index = ".testindex-logs",
  params = { "primary_only": "true" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 範例回應

```json
{
  "_shards": {
    "total": 2,
    "successful": 1,
    "failed": 0
  }
}
```

## 回應本文欄位

下表列出所有回應欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `shards` | 物件 | 包含執行請求所在分片的相關資訊。 |
| `shards.total` | 整數 | 執行操作所在的分片數量。 |
| `shards.successful` | 整數 | 操作成功執行的分片數量。 |
| `shards.failed` | 整數 | 操作執行失敗的分片數量。 |

## 必要權限

如果您使用 Security 外掛程式，請確認您具備適當的權限：`indices:admin/forcemerge`。
