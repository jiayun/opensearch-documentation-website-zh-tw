---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "排清"
parent: Index operations
grand_parent: Index APIs
nav_order: 30
---

# Flush API

**於 1.0 版推出**
{: .label .label-purple }

Flush API 會將所有記憶體內的操作儲存到磁碟上的分段。重新啟動叢集時，已排清至索引分段的操作不再需要保留在交易記錄中，因為這些操作現在已儲存在 Lucene 索引中。

OpenSearch 會根據交易記錄大小等條件自動在背景執行排清，該條件由 `index.translog.flush_threshold_size` 設定控制。請謹慎使用 Flush API，例如用於手動重新啟動或釋放記憶體。

如需排清與交易記錄、重新整理及合併作業之間關係的詳細資訊，請參閱 OpenSearch 概念中的[排清]({{site.url}}{{site.baseurl}}/getting-started/concepts/#flush)。

## 端點

Flush API 支援下列路徑：

```json
GET /_flush
POST /_flush
GET /{index}/_flush
POST /{index}/_flush
```

## 路徑參數

下表列出可用的路徑參數。所有路徑參數皆為選用。

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `<index>` | 字串 | 要套用此作業的索引、資料串流或索引別名的逗號分隔清單。支援萬用字元運算式 (`*`)。使用 `_all` 或 `*` 可指定叢集中的所有索引與資料串流。 |

## 查詢參數

所有參數皆為選用。

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `allow_no_indices` | 布林值 | 若為 `false`，當任何萬用字元運算式或索引別名指向任何已關閉或不存在的索引時，請求會傳回錯誤。預設為 `true`。 |
| `expand_wildcards` | 字串 | 指定萬用字元運算式可展開的索引類型。支援以逗號分隔的值。有效值如下：<br> - `all`：展開至所有已開啟和已關閉的索引，包括隱藏索引。<br> - `open`：展開至已開啟的索引。<br> - `closed`：展開至已關閉的索引。<br> - `hidden`：展開時包含隱藏索引。必須與 `open`、`closed` 或兩者合併使用。<br> - `none`：不接受萬用字元運算式。<br> 預設為 `open`。<br> Flush API 無法排清已關閉的索引。若萬用字元運算式展開至已關閉的索引，除非 `ignore_unavailable` 為 `true`，否則請求會失敗；在此情況下會略過已關閉的索引。 |
| `force` | 布林值 | 若為 `true`，即使記憶體中沒有任何索引變更，也會強制執行排清。若為 `true`，則 `wait_if_ongoing` 也必須為 `true`，否則請求會遭到拒絕。預設為 `false`。 |
| `ignore_unavailable` | 布林值 | 若為 `true`，OpenSearch 會忽略不存在或已關閉的索引。若為 `false`，當排清作業遇到不存在或已關閉的索引時，OpenSearch 會傳回錯誤。預設為 `false`。 |
| `wait_if_ongoing` | 布林值 | 若為 `true`，當另一個排清作業正在進行時，OpenSearch 會等待該作業完成後再執行排清。若為 `false`，當某個分片上已有另一個排清作業正在執行時，該分片會略過排清，且不會傳回錯誤。預設為 `true`。 |

## 範例請求：排清特定索引

下列範例會排清名為 `shakespeare` 的索引：

<!-- spec_insert_start
component: example_code
rest: POST /shakespeare/_flush
body: 
-->
{% capture step1_rest %}
POST /shakespeare/_flush

{% endcapture %}

{% capture step1_python %}


response = client.indices.flush(
  index = "shakespeare"
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->


## 範例請求：排清所有索引

下列範例會排清叢集中的所有索引：

<!-- spec_insert_start
component: example_code
rest: POST /_flush
body: 
-->
{% capture step1_rest %}
POST /_flush

{% endcapture %}

{% capture step1_python %}

response = client.indices.flush()
{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 範例回應

OpenSearch 的回應會包含排清請求所針對的分片複本數量（包括未指派的副本）、已完成請求的分片複本數量，以及失敗的分片複本數量：

```json
{
  "_shards": {
    "total": 10,
    "successful": 10,
    "failed": 0
  }
}
```

## 必要權限

若您使用 Security 外掛程式，請確認您具備適當的權限：`indices:admin/flush` 與 `indices:admin/flush*`。
