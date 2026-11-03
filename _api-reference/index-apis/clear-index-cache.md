---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "清除快取"
parent: Index operations
grand_parent: Index APIs
nav_order: 10
---

# Clear Cache API
**於 1.0 版推出**
{: .label .label-purple }

Clear Cache API 操作會清除一或多個索引的快取。對於資料串流，此 API 會清除該串流之後端索引的快取。

## 端點

```json
POST /_cache/clear
POST /{target}/_cache/clear
```

## 路徑參數

| 參數 | 資料類型 | 說明 |
:--- | :--- | :---
| `target` | 字串 | 要套用快取清除的資料串流、索引與索引別名的逗號分隔清單。支援萬用字元運算式 (`*`)。若要指定叢集中的所有資料串流與索引，請省略此參數或使用 `_all` 或 `*`。選用。 |


## 查詢參數

所有查詢參數皆為選用。

| 參數 | 資料類型 | 說明 |
:--- | :--- | :---
| `allow_no_indices` | 布林值 | 是否忽略不符合任何索引的萬用字元、索引別名或 `_all` 目標（`target` 路徑參數）值。若為 `false`，當任何萬用字元運算式、索引別名或 `_all` 目標值不符合任何索引時，請求會傳回錯誤。即使請求目標包含其他開啟的索引，此行為仍然適用。例如，若有索引以 `fig` 開頭，但沒有任何索引以 `app` 開頭，則目標為 `fig*,app*` 的請求會傳回錯誤。預設為 `true`。 |
| `expand_wildcards` | 字串 | 決定萬用字元運算式可展開的索引類型。可接受以逗號分隔的多個值，例如 `open,hidden`。有效值為：<br /><br /> `all` -- 展開為開啟、關閉及隱藏的索引。<br /><br />`open` -- 僅展開為開啟的索引。<br /><br />`closed` -- 僅展開為關閉的索引<br /><br />`hidden` -- 展開時包含隱藏的索引。必須與 `open` 或 `closed` 搭配使用。<br /><br />`none` -- 不接受展開。<br /><br /> 預設為 `open`。關閉的索引的快取無法清除，因此除非 `ignore_unavailable` 為 `true`，否則當萬用字元運算式符合關閉的索引時，使用 `closed` 或 `all` 的請求會失敗。 |
| `fielddata` | 布林值 | 若為 `true`，則清除欄位快取。使用 `fields` 參數可清除特定欄位的快取。預設為 `false`。 |
| `fields` | 字串 | 以逗號分隔的欄位名稱清單，這些欄位的 fielddata 會從快取中清除。若未搭配其他快取參數指定，則僅清除所列欄位的 fielddata。不支援物件或欄位別名。預設為所有欄位。 |
| `file` | 布林值 | 若為 `true`，則清除具有 Search 角色之節點上檔案快取中未使用的項目。除非 `query` 或 `fielddata` 也為 `true`，或已指定 `fields`，否則將 `file` 設定為 `true` 也會清除所有索引快取。預設為 `false`。 |
| `index` | 字串 | 以逗號分隔的索引清單，這些索引的快取會被清除。可替代 `POST /_cache/clear` 端點的 `target` 路徑參數。 |
| `ignore_unavailable` | 布林值 | 若為 `true`，OpenSearch 會忽略遺失或關閉的索引。預設為 `false`。 |
| `query` | 布林值 | 若為 `true`，則清除查詢快取。預設為 `false`。 |
| `request` | 布林值 | 若為 `true`，則清除請求快取。預設為 `false`。 |

若未指定 `fielddata`、`query`、`request` 或 `fields` 中的任何參數，則會清除所有快取。將 `fielddata` 或 `query` 設定為 `true` 只會清除該快取。若 `request` 是唯一設定為 `true` 的快取參數，且未指定 `fields`，則會清除所有快取。

欄位資料（field data）項目會在下一次快取清理時移除，清理作業會依 `indices.cache.cleanup_interval` 設定所指定的間隔執行（預設為 `1m`）。在此之前，fielddata 統計資料可能仍會顯示快取清除前的大小。
{: .note}

## 範例請求

下列範例請求展示 Clear Cache API 的多種用法。

### 清除特定快取

下列請求僅清除欄位快取：

<!-- spec_insert_start
component: example_code
rest: POST /my-index/_cache/clear?fielddata=true
-->
{% capture step1_rest %}
POST /my-index/_cache/clear?fielddata=true
{% endcapture %}

{% capture step1_python %}


response = client.indices.clear_cache(
  index = "my-index",
  params = { "fielddata": "true" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

<hr />

下列請求僅清除查詢快取：

<!-- spec_insert_start
component: example_code
rest: POST /my-index/_cache/clear?query=true
-->
{% capture step1_rest %}
POST /my-index/_cache/clear?query=true
{% endcapture %}

{% capture step1_python %}


response = client.indices.clear_cache(
  index = "my-index",
  params = { "query": "true" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

<hr />

下列請求僅清除請求快取：

<!-- spec_insert_start
component: example_code
rest: POST /my-index/_cache/clear?request=true
-->
{% capture step1_rest %}
POST /my-index/_cache/clear?request=true
{% endcapture %}

{% capture step1_python %}


response = client.indices.clear_cache(
  index = "my-index",
  params = { "request": "true" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

### 清除特定欄位的快取

下列請求會清除 `product_name` 和 `category` 的欄位快取：

<!-- spec_insert_start
component: example_code
rest: POST /my-index/_cache/clear?fields=product_name,category
-->
{% capture step1_rest %}
POST /my-index/_cache/clear?fields=product_name,category
{% endcapture %}

{% capture step1_python %}


response = client.indices.clear_cache(
  index = "my-index",
  params = { "fields": "product_name,category" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

### 清除特定資料串流或索引的快取

下列請求清除兩個特定索引的快取：

<!-- spec_insert_start
component: example_code
rest: POST /my-index,my-index2/_cache/clear
-->
{% capture step1_rest %}
POST /my-index,my-index2/_cache/clear
{% endcapture %}

{% capture step1_python %}


response = client.indices.clear_cache(
  index = "my-index,my-index2"
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

### 清除所有資料串流和索引的快取

下列請求會清除所有資料串流和索引的快取：

<!-- spec_insert_start
component: example_code
rest: POST /_cache/clear
-->
{% capture step1_rest %}
POST /_cache/clear
{% endcapture %}

{% capture step1_python %}

response = client.indices.clear_cache()
{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->


### 清除具備搜尋功能之節點上快取中未使用的項目

下列請求會清除具有 Search 角色之節點上檔案快取中未使用的項目：

<!-- spec_insert_start
component: example_code
rest: POST /*/_cache/clear?file=true
-->
{% capture step1_rest %}
POST /*/_cache/clear?file=true
{% endcapture %}

{% capture step1_python %}


response = client.indices.clear_cache(
  index = "*",
  params = { "file": "true" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 範例回應

`POST /books,hockey/_cache/clear` 請求會回傳下列欄位：

```json
{
  "_shards" : {
    "total" : 4,
    "successful" : 2,
    "failed" : 0
  }
}
```

## 回應本文欄位

`POST /books,hockey/_cache/clear` 請求會傳回下列回應欄位：

| 欄位 | 資料類型 | 說明 | 
:--- | :--- | :---
| `_shards` | 物件 | 分片資訊。 |

`_shards` 物件包含下列欄位。

| 欄位 | 資料類型 | 說明 |
:--- | :--- | :---
| `total` | 整數 | 分片總數。 |
| `successful` | 整數 | 已成功清除快取的索引分片數量。 |
| `failed` | 整數 | 清除快取失敗的索引分片數量。 |

## 必要權限

如果您使用 Security 外掛程式，請確保您具備適當的權限：`indices:admin/cache/clear`。
