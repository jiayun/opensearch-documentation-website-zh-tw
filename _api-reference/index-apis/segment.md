---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "索引區段"
parent: Index operations
grand_parent: Index APIs
nav_order: 90
---

# Index Segments API
**Introduced 1.0**
{: .label .label-purple }

Segment API 提供索引分片內 Lucene 區段的詳細資訊，以及資料串流所屬索引的相關資訊。


## 端點

```json
GET /{index}/_segments
GET /_segments
```

## 路徑參數

下表列出可用的路徑參數。所有路徑參數皆為選用。

Parameter | Data type | Description 
:--- | :--- | :--- 
`index` | String | 以逗號分隔的索引、資料串流或索引別名清單，用於指定要套用此操作的目標。支援萬用字元運算式 (`*`)。使用 `_all` 或 `*` 可指定叢集中的所有索引與資料串流。 |

## 查詢參數

所有查詢參數皆為選用。

Parameter | Data type | Description
:--- | :--- | :---
`allow_no_indices` | Boolean | 是否忽略未符合任何索引的萬用字元。預設為 `true`。
`expand_wildcards` | String | 指定萬用字元運算式可符合的索引類型。支援以逗號分隔的值。有效值為 `all` (符合任何索引)、`open` (符合開啟且非隱藏的索引)、`closed` (符合關閉且非隱藏的索引)、`hidden` (符合隱藏的索引)，以及 `none` (拒絕萬用字元運算式)。預設為 `open`。
`ignore_unavailable` | Boolean | 當設為 `true` 時，OpenSearch 會忽略遺失或關閉的索引。若設為 `false`，當強制合併操作遇到遺失或關閉的索引時，OpenSearch 會傳回錯誤。預設為 `false`。
`verbose` | Boolean | 當設為 `true` 時，提供 Lucene 記憶體使用量的相關資訊。預設為 `false`。


## 範例請求

以下範例請求示範如何使用 Segment API。

### 特定資料串流或索引

<!-- spec_insert_start
component: example_code
rest: GET /index1/_segments
-->
{% capture step1_rest %}
GET /index1/_segments
{% endcapture %}

{% capture step1_python %}


response = client.indices.segments(
  index = "index1"
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

### 多個資料串流與索引

<!-- spec_insert_start
component: example_code
rest: GET /index1,index2/_segments
-->
{% capture step1_rest %}
GET /index1,index2/_segments
{% endcapture %}

{% capture step1_python %}


response = client.indices.segments(
  index = "index1,index2"
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

### 叢集中的所有資料串流與索引

<!-- spec_insert_start
component: example_code
rest: GET /_segments
-->
{% capture step1_rest %}
GET /_segments
{% endcapture %}

{% capture step1_python %}

response = client.indices.segments()
{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 範例回應

```json
{
  "_shards": ...
  "indices": {
    "test": {
      "shards": {
        "0": [
          {
            "routing": {
              "state": "STARTED",
              "primary": true,
              "node": "zDC_RorJQCao9xf9pg3Fvw"
            },
            "num_committed_segments": 0,
            "num_search_segments": 1,
            "segments": {
              "_0": {
                "generation": 0,
                "num_docs": 1,
                "deleted_docs": 0,
                "size_in_bytes": 3800,
                "memory_in_bytes": 1410,
                "committed": false,
                "search": true,
                "version": "7.0.0",
                "compound": true,
                "attributes": {
                }
              }
            }
          }
        ]
      }
    }
  }
}
```

## 回應本文欄位

Parameter | Data type | Description 
 :--- | :--- | :--- 
`segment` | String | 用於在分片目錄中建立內部檔案名稱的區段名稱。 
`generation` | Integer | 世代編號，例如 `0`，每寫入一個區段即遞增，並用於命名該區段。 
`num_docs` | Integer | 文件數量，取自 Lucene。巢狀文件會與其父文件分開計算。已刪除的文件，以及最近編製索引但尚未指派至區段的文件，皆不列入計算。
`deleted_docs` | Integer | 已刪除的文件數量，取自 Lucene，可能與實際執行的刪除操作次數不符。最近刪除但尚未指派至區段的文件不列入計算。已刪除的文件會在適當時機自動合併。OpenSearch 有時會額外刪除文件，以追蹤最近的分片操作。
`size_in_bytes` | Integer | 該區段使用的磁碟空間量，例如 `50kb`。 
`memory_in_bytes` | Integer | 保留在記憶體中的區段資料量 (以位元組為單位)，用以協助有效率地執行搜尋操作，例如 `1264`。值為 `-1` 表示 OpenSearch 無法計算此數字。 
`committed` | Boolean | 當設為 `true` 時，區段會同步至磁碟。同步至磁碟的區段可在強制重新開機後留存。若設為 `false`，則未提交的區段資料也會儲存在交易記錄中，以便在下次啟動時重播變更。 
`search` | Boolean | 當設為 `true` 時，會啟用區段搜尋。當設為 `false` 時，該區段可能已寫入磁碟，需要重新整理才能搜尋。
`version` | String | 用於寫入該區段的 Lucene 版本。 
`compound` | Boolean | 當設為 `true` 時，表示 Lucene 已將所有區段檔案合併為單一檔案，以節省檔案描述項。
`attributes` | Object | 顯示是否已啟用高壓縮。

## 必要權限

如果您使用 Security 外掛程式，請確認您具有適當的權限：`indices:monitor/segments`。
