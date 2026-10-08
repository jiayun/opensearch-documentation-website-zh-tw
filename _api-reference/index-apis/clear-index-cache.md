---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "清除快取"
parent: Index operations
grand_parent: Index APIs
nav_order: 10
---

# Clear Cache API
**1.0 版新增**
{: .label .label-purple }

Clear Cache API 作業會清除一個或多個索引的快取。對於資料串流，此 API 會清除該串流後備索引的快取。


如果您使用 Security 外掛程式，則必須具備 `manage index` 權限。
{: .note}

## 端點

```json
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
| `allow_no_indices` | 布林值 | 是否忽略不符合任何索引的萬用字元、索引別名或 `_all` 目標 (`target` 路徑參數) 值。若為 `false`，當任何萬用字元運算式、索引別名或 `_all` 目標值不符合任何索引時，請求會回傳錯誤。即使請求目標包含其他開啟的索引，此行為也適用。例如，當目標為 `fig*,app*` 時，若有索引以 `fig` 開頭但沒有索引以 `app` 開頭，則請求會回傳錯誤。預設為 `true`。 |
| `expand_wildcards` | 字串 | 決定萬用字元運算式可展開至哪些索引類型。接受以逗號分隔的多個值，例如 `open,hidden`。有效值為：<br /><br /> `all` -- 展開至開啟、關閉與隱藏的索引。<br /><br />`open` -- 僅展開至開啟的索引。<br /><br />`closed` -- 僅展開至關閉的索引<br /><br />`hidden` -- 展開以包含隱藏的索引。必須與 `open`、`closed` 或 `both` 搭配使用。<br /><br />`none` -- 不接受展開。<br /><br /> 預設為 `open`。 |
| `fielddata` | 布林值 | 若為 `true`，則清除欄位快取。使用 `fields` 參數可清除特定欄位的快取。預設為 `true`。 |
| `fields` | 字串 | 與 `fielddata` 參數搭配使用。要從快取中清除的欄位名稱的逗號分隔清單。不支援物件或欄位別名。預設為所有欄位。 |
| `file` | 布林值 | 若為 `true`，則清除具有 Search 角色之節點上檔案快取中未使用的項目。預設為 `false`。 |
| `index` | 字串 | 要從快取中清除的索引名稱的逗號分隔清單。 |
| `ignore_unavailable` | 布林值 | 若為 `true`，OpenSearch 會忽略遺失或已關閉的索引。預設為 `false`。 |
| `query` | 布林值 | 若為 `true`，則清除查詢快取。預設為 `true`。 |
| `request` | 布林值 | 若為 `true`，則清除請求快取。預設為 `true`。 |

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

下列請求清除 `fielda` 與 `fieldb` 的欄位快取：

<!-- spec_insert_start
component: example_code
rest: POST /my-index/_cache/clear?fields=fielda,fieldb
-->
{% capture step1_rest %}
POST /my-index/_cache/clear?fields=fielda,fieldb
{% endcapture %}

{% capture step1_python %}


response = client.indices.clear_cache(
  index = "my-index",
  params = { "fields": "fielda,fieldb" }
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

#### 清除所有資料串流與索引的快取

下列請求清除所有資料串流與索引的快取：

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


### 清除具搜尋能力節點上快取中未使用的項目

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

`POST /books,hockey/_cache/clear` 請求會回傳下列回應欄位：

| 欄位 | 資料類型 | 說明 | 
:--- | :--- | :---
| `_shards` | 物件 | 分片資訊。 |
| `total` | 整數 | 分片總數。 |
| `successful` | 整數 | 成功清除快取的索引分片數量。 |
| `failed` | 整數 | 清除快取失敗的索引分片數量。 |

## 必要權限

如果您使用 Security 外掛程式，請確保您具備適當的權限：`indices:admin/cache/clear`。
