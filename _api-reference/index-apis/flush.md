---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Flush
parent: Index operations
grand_parent: Index APIs
nav_order: 30
---

# Flush API

**於 1.0 版推出**
{: .label .label-purple }

Flush API 會將所有記憶體內的作業儲存到磁碟上的區段。已沖寫至索引區段的作業，在叢集重新啟動期間不再需要保留於交易記錄檔中，因為這些作業現在已儲存在 Lucene 索引內。

OpenSearch 會根據交易記錄檔大小等條件，在背景自動執行沖寫，此行為由 `index.translog.flush_threshold_size` 設定控制。請節制地使用 Flush API，例如在手動重新啟動或需要釋放記憶體時使用。

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
| `allow_no_indices` | 布林值 | 設為 `false` 時，若任何萬用字元運算式或索引別名指向任何已關閉或遺失的索引，請求將回傳錯誤。預設為 `true`。 |
| `expand_wildcards` | 字串 | 指定萬用字元運算式可展開的索引類型。支援逗號分隔值。有效值為：<br> - `all`：展開至所有開啟與關閉的索引，包括隱藏索引。<br> - `open`：展開至開啟的索引。<br> - `closed`：展開至關閉的索引。<br> - `hidden`：展開時包含隱藏索引。必須與 `open`、`closed` 或兩者一併使用。<br> - `none`：不接受萬用字元運算式。<br> 預設為 `open`。 |
| `force` | 布林值 | 設為 `true` 時，即使記憶體內沒有索引變更，也會強制執行沖寫。預設為 `true`。 |
| `ignore_unavailable` | 布林值 | 設為 `true` 時，OpenSearch 會忽略遺失或已關閉的索引。設為 `false` 時，若強制合併作業遇到遺失或已關閉的索引，OpenSearch 會回傳錯誤。預設為 `false`。 |
| `wait_if_ongoing` | 布林值 | 設為 `true` 時，若有另一個沖寫請求正在執行，Flush API 不會執行。設為 `false` 時，若有另一個沖寫請求正在執行，OpenSearch 會回傳錯誤。預設為 `true`。 |

## 範例請求：沖寫特定索引

下列範例沖寫名為 `shakespeare` 的索引：

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


## 範例請求：沖寫所有索引

下列範例沖寫叢集中的所有索引：

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

OpenSearch 會回應確認沖寫請求的分片數量、完成請求的分片數量，以及失敗的分片數量：

```
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
