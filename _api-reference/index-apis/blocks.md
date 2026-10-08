---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "封鎖"
parent: Index blocks and allocation
grand_parent: Index APIs
nav_order: 10
---

# Blocks API
**於 1.0 版推出**
{: .label .label-purple }

使用 Blocks API 可限制指定索引上的特定作業。不同類型的封鎖可讓您限制索引的寫入、讀取或中繼資料作業。 
例如，透過 API 新增 `write` 封鎖，可確保所有索引分片都已妥善處理該封鎖後，才傳回成功回應。對索引進行的任何尚未完成的寫入作業，都必須在 `write` 封鎖生效前完成。

## 端點

```json
PUT /{index}/_block/{block}
```

## 路徑參數

| 參數 | 資料類型 | 說明 |
:--- | :--- | :---
| `index` | 字串 | 以逗號分隔的索引名稱清單。支援萬用字元運算式（`*`）。若要以叢集中的所有資料串流和索引為目標，請使用 `_all` 或 `*`。選用。 |
| `<block>` | 字串 | 指定要套用至索引的封鎖類型。有效值為：<br> - `metadata`：封鎖中繼資料變更，例如關閉索引。<br> - `read`：封鎖讀取作業。<br> - `read_only`：封鎖寫入作業和中繼資料變更。<br> - `write`：封鎖寫入作業，但允許中繼資料變更。<br> - `search_only`：封鎖編製索引和寫入作業，同時允許透過搜尋副本進行唯讀存取。<br> OpenSearch 會透過 Scale API 自動管理此封鎖，作為讀寫分離機制的一部分。因此，請勿手動設定此參數。 |

## 查詢參數

下表列出可用的查詢參數。所有查詢參數皆為選用。

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `ignore_unavailable` | 布林值 | 當值為 `false` 時，若請求以不存在或已關閉的索引為目標，便會傳回錯誤。預設為 `false`。
| `allow_no_indices` | 布林值 | 當值為 `false` 時，若萬用字元運算式、索引別名或 `_all` 僅以已關閉或不存在的索引為目標，即使請求是針對開啟的索引發出，Refresh Index API 也會傳回錯誤。預設為 `true`。 |
| `expand_wildcards` | 字串 | 萬用字元模式可比對的索引類型。如果請求以資料串流為目標，此引數會決定萬用字元運算式是否比對任何隱藏的資料串流。支援以逗號分隔的值，例如 `open,hidden`。有效值為 `all`、`open`、`closed`、`hidden` 和 `none`。 |
`cluster_manager_timeout` | `Time` | 等待連線至叢集管理員節點的時間。預設為 `30s`。
`timeout` | `Time` | 等待請求傳回的時間。預設為 `30s`。 |

## 請求範例
<!-- spec_insert_start
component: example_code
rest: PUT /test-index/_block/write
-->
{% capture step1_rest %}
PUT /test-index/_block/write
{% endcapture %}

{% capture step1_python %}


response = client.indices.add_block(
  block = "write",
  index = "test-index"
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

以下請求範例會停用對測試索引執行的任何 `write` 作業：

<!-- spec_insert_start
component: example_code
rest: PUT /test-index/_block/write
-->
{% capture step1_rest %}
PUT /test-index/_block/write
{% endcapture %}

{% capture step1_python %}


response = client.indices.add_block(
  block = "write",
  index = "test-index"
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 回應範例

```json
{
  "acknowledged" : true,
  "shards_acknowledged" : true,
  "indices" : [ {
    "name" : "test-index",
    "blocked" : true
  } ]
}
```
