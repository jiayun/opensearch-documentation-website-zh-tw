---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "強制合併"
parent: Index operations
grand_parent: Index APIs
nav_order: 40
---

# 強制合併 API
**1.0 版引入**
{: .label .label-purple }

強制合併 API 操作會對一或多個索引的分片強制執行合併。對於資料串流，此 API 會對該串流的後端索引分片強制執行合併。

## 端點

```json
POST /_forcemerge
POST /{index}/_forcemerge
```

## 合併作業

在 OpenSearch 中，分片是一個 Lucene 索引，由_分段_（或分段檔案）組成。分段儲存已編製索引的資料，且不可變更。OpenSearch 會定期將較小的分段合併為一個新的較大分段，然後刪除原始分段。合併可減少每個分片上的分段總數，並釋放磁碟空間。

OpenSearch 會在背景執行分段合併，所產生的分段不會大於 `index.merge.policy.max_merged_segment`（預設為 5 GB）。

## 已刪除的文件

從 OpenSearch 索引中刪除文件時，該文件並不會從 Lucene 分段中刪除，而只是被標記為待刪除。合併分段檔案時，已刪除的文件會被移除（或稱為_清除_）。因此，合併也會釋放已標記為刪除的文件所占用的空間。

OpenSearch 會在 `index.soft_deletes.retention_lease.period` 設定所指定的期間內（預設為 `12h`），保留分片的操作歷程，包括已刪除的文件。強制合併不會清除仍在保留期間內的已刪除文件，因此強制合併後，已刪除文件的數量可能不會立即減少。如需詳細資訊，請參閱[索引設定]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/index-settings/)。

## Force Merge API

除了定期合併之外，您也可以使用 Force Merge API 強制合併分段。根據預設，合併原則會決定要合併哪些分段，因此強制合併請求不一定會改變分段數量。若要將每個分片的所有分段合併為單一分段，請將 `max_num_segments` 設定為 `1`。

請僅在傳送至索引的所有寫入請求都已完成後，才對該索引使用 Force Merge API。強制合併操作可能會產生非常大的分段。如果仍有寫入請求傳送至該索引，合併原則將不會合併這些分段，直到其主要由已刪除的文件組成為止。這可能會增加磁碟空間使用量，並導致效能降低。
{: .warning}

根據預設，Force Merge API 呼叫會在合併完成後才傳回。如果在此期間連線中斷，強制合併操作仍會在背景繼續執行。若要以非同步方式執行此操作，請將 `wait_for_completion` 設定為 `false`。

每個節點都會在其 `force_merge` 執行緒集區中執行強制合併操作。當集區中的所有執行緒都忙碌時，抵達的強制合併請求會排入佇列，直到有執行緒可用為止。

## 強制合併多個索引

若要強制合併多個索引，您可以對下列索引組合呼叫 Force Merge API：

- 多個索引
- 一或多個包含多個後端索引的資料串流
- 一或多個指向多個索引的索引別名
- 叢集中的所有資料串流和索引

當您強制合併多個索引時，每個節點會使用 `force_merge` 執行緒集區合併其分片。此集區的大小為節點所配置處理器數量的八分之一，最小值為 1，因此在大多數節點上，分片會一次合併一個。在強制合併作業進行期間，分片的儲存空間會暫時增加，以便將所有分段重新寫入一個新的分段。當 `max_num_segments` 設定為 `1` 時，分片的儲存空間可能會暫時加倍。

## 強制合併資料串流

強制合併資料串流有助於管理資料串流的後端索引，尤其是在輪替操作之後。以時間為基礎的索引只在指定的時間期間內接收編製索引的請求。一旦該時間期間過去且索引不再接收寫入請求，您就可以將所有索引分片的分段強制合併為一個分段。對單一分段分片的搜尋效率更高，因為它們使用較簡單的資料結構。


## 路徑參數

下表列出可用的路徑參數。所有路徑參數皆為選用。

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `index` | 字串 | 以逗號分隔的索引、資料串流或索引別名清單，作為此操作的套用對象。支援萬用字元運算式（`*`）。使用 `_all` 或 `*` 可指定叢集中的所有索引和資料串流。 |

## 查詢參數

下表列出可用的查詢參數。所有查詢參數皆為選用。

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `allow_no_indices` | 布林值 | 若為 `false`，當萬用字元運算式或索引別名未符合任何開啟的索引時，請求會傳回錯誤。預設為 `true`。 |
| `expand_wildcards` | 字串 | 指定萬用字元運算式可展開的索引類型。支援以逗號分隔的值。有效值為：<br> - `all`：展開至所有開啟及關閉的索引，包括隱藏索引。<br> - `open`：展開至開啟的索引。<br> - `closed`：展開至關閉的索引。<br> - `hidden`：展開時包含隱藏索引。必須與 `open`、`closed` 或兩者合併使用。<br> - `none`：不接受萬用字元運算式。<br> 預設為 `open`。<br> 強制合併無法在關閉的索引上執行，因此將萬用字元展開至關閉索引的請求（`closed` 或 `all`）會傳回錯誤，除非 `ignore_unavailable` 為 `true`。 |
| `flush` | 布林值 | 在強制合併後對索引執行排清。排清可確保檔案已持久儲存至磁碟。預設為 `true`。 |
| `ignore_unavailable` | 布林值 | 若為 `true`，OpenSearch 會忽略遺失或關閉的索引。若為 `false`，當強制合併操作遇到遺失或關閉的索引時，OpenSearch 會傳回錯誤。預設為 `false`。 |
| `max_num_segments` | 整數 | 合併後每個分片的分段數量上限。將此參數設為 `1` 可將每個分片的所有分段合併為一個分段。根據預設，分段會依合併原則決定的方式進行合併。 |
| `only_expunge_deletes` | 布林值 | 若為 `true`，合併操作只會清除包含一定比例已刪除文件的分段。此比例預設為 10%，可在 `index.merge.policy.expunge_deletes_allowed` 設定中調整。使用 `only_expunge_deletes` 不會產生大於 `index.merge.policy.max_merged_segment`（預設為 5 GB）的分段。將 `only_expunge_deletes` 與 `max_num_segments` 合併使用的方式已淘汰。如需詳細資訊，請參閱[已刪除的文件](#deleted-documents)。預設為 `false`。 |
| `primary_only` | 布林值 | 若設為 `true`，合併操作只會在索引的主要分片上執行。當您想在合併完成後建立索引的快照時，這會很有用。快照只會複製主要分片中的分段。合併主要分片可降低資源消耗。預設為 `false`。 |
| `wait_for_completion` | 布林值 | 若為 `false`，OpenSearch 會以非同步方式執行強制合併操作，而不等待其完成。請求會立即傳回，且工作會在背景繼續執行。您可以使用 [Tasks API]({{site.url}}{{site.baseurl}}/api-reference/tasks/) 監控其進度。預設為 `true`，表示操作會以同步方式執行。 |

## 請求範例

下列範例說明如何使用 Force Merge API。

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

### 將資料串流的後端索引強制合併為單一分段

以下範例將資料串流的後端索引強制合併為單一分段：

<!-- spec_insert_start
component: example_code
rest: POST /testindex-logs/_forcemerge?max_num_segments=1
-->
{% capture step1_rest %}
POST /testindex-logs/_forcemerge?max_num_segments=1
{% endcapture %}

{% capture step1_python %}


response = client.indices.forcemerge(
  index = "testindex-logs",
  params = { "max_num_segments": "1" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

### 強制合併主要分片

下列範例會強制合併索引的主要分片：

<!-- spec_insert_start
component: example_code
rest: POST /testindex-logs/_forcemerge?primary_only=true
-->
{% capture step1_rest %}
POST /testindex-logs/_forcemerge?primary_only=true
{% endcapture %}

{% capture step1_python %}


response = client.indices.forcemerge(
  index = "testindex-logs",
  params = { "primary_only": "true" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 回應範例

`total` 計數同時包含主要分片與副本分片。在以下回應範例中，索引有一個主要分片和一個副本分片。由於副本分片尚未配置，因此該操作僅在主要分片上成功：

```json
{
  "_shards": {
    "total": 2,
    "successful": 1,
    "failed": 0
  }
}
```

若 `wait_for_completion` 為 `false`，回應會包含任務 ID，您可以使用 [Tasks API]({{site.url}}{{site.baseurl}}/api-reference/tasks/) 透過此 ID 監控該任務：

```json
{
  "task": "<node_id>:<task_number>"
}
```

## 回應本文欄位

下表列出所有回應欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `_shards` | 物件 | 包含執行請求之分片的相關資訊。當 `wait_for_completion` 為 `true` 時傳回。 |
| `task` | 字串 | 強制合併任務的 ID。當 `wait_for_completion` 為 `false` 時傳回。 |

`_shards` 物件包含下列欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `total` | 整數 | 執行此操作的分片數量。 |
| `successful` | 整數 | 此操作執行成功的分片數量。 |
| `failed` | 整數 | 此操作執行失敗的分片數量。 |

## 必要權限

如果您使用 Security 外掛程式，請確認您具備適當的權限：`indices:admin/forcemerge`。
