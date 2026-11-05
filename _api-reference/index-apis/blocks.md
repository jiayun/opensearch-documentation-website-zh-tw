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
| :--- | :--- | :--- |
| `index` | 字串 | 以逗號分隔的索引名稱清單。支援萬用字元運算式（`*`）。若要以叢集中的所有索引為目標，請使用 `_all` 或 `*`。不支援資料串流名稱，且您無法對資料串流的寫入索引新增封鎖。必要。 |
| `block` | 字串 | 要套用至索引的封鎖類型。必要。有效值為：<br> - `metadata`：同時封鎖擷取與變更索引中繼資料。例如，您無法關閉索引或取得其設定。<br> - `read`：封鎖讀取操作。<br> - `read_only`：封鎖寫入操作與中繼資料變更。<br> - `write`：封鎖寫入操作，但允許中繼資料變更。<br> - `search_only`：封鎖編製索引與寫入操作，同時允許透過搜尋副本進行唯讀存取。<br> OpenSearch 會透過 Scale API 自動管理此封鎖，這是讀寫分離機制的一部分。因此，請勿手動設定此參數。 |

## 查詢參數

下表列出可用的查詢參數。所有查詢參數皆為選用。

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `ignore_unavailable` | 布林值 | 若為 `false`，當請求的目標為不存在或已關閉的索引時，請求會傳回錯誤。預設為 `false`。 |
| `allow_no_indices` | 布林值 | 若為 `false`，當萬用字元運算式、索引別名或 `_all` 未符合任何索引時，請求會傳回錯誤。預設為 `true`。 |
| `expand_wildcards` | 字串 | 萬用字元運算式可符合的索引類型。支援以逗號分隔的值，例如 `open,hidden`。有效值為 `all`、`open`、`closed`、`hidden` 和 `none`。預設為 `open`。 |
| `cluster_manager_timeout` | 時間 | 等待與叢集管理員節點建立連線的時間長度。預設為 `30s`。 |
| `timeout` | 時間 | 等待請求傳回的時間長度。預設為 `30s`。 |

## 請求範例

下列請求範例會停用對 test 索引進行的任何 `write` 操作：

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

## 移除封鎖

Blocks API 只能新增封鎖。若要移除封鎖，請使用 Update Index Settings API 將對應的索引設定設為 `false`。設定名稱與封鎖名稱相對應：`index.blocks.read`、`index.blocks.read_only`、`index.blocks.metadata` 或 `index.blocks.write`。如需更多資訊，請參閱 [Update Index Settings API]({{site.url}}{{site.baseurl}}/api-reference/index-apis/update-settings/)。

下列範例請求會從 test 索引移除 `write` 封鎖：

```json
PUT /test-index/_settings
{
  "index.blocks.write": false
}
```
{% include copy-curl.html %}

若索引具有 `read_only`、`read_only_allow_delete` 或 `metadata` 封鎖，則移除該封鎖的請求只能包含該封鎖設定。請先以個別請求移除封鎖，再更新任何其他設定。

若索引的分片所在節點的磁碟使用量超過洪水階段水位線（flood-stage watermark），OpenSearch 會為這些索引新增 `index.blocks.read_only_allow_delete` 封鎖。當磁碟使用量降至高水位線（high watermark）以下時，OpenSearch 會移除該封鎖。如需更多資訊，請參閱[叢集層級路由與配置設定]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/cluster-settings/#cluster-level-routing-and-allocation-settings)。

OpenSearch 透過 Scale API 管理 `search_only` 封鎖，因此請勿使用 Update Index Settings API 移除該封鎖。若要停用僅搜尋模式，請參閱 [Scale API]({{site.url}}{{site.baseurl}}/api-reference/index-apis/scale/)。
