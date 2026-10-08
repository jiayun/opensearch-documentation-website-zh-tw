---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "列出索引"
parent: List APIs
nav_order: 25
has_children: false
---

# List Indices API
**於 2.18 版推出**
{: .label .label-purple }

list indices 作業會以分頁格式提供下列索引資訊：

- 索引所使用的磁碟空間量。
- 索引中包含的分片數。
- 索引的健康狀態。

## 端點

```json
GET _list/indices
GET _list/indices/{index}
```

## 查詢參數

參數 | 類型 | 說明
:--- | :--- | :---
`bytes` | 位元組大小 | 指定位元組大小的單位，例如 `7kb` 或 `6gb`。如需詳細資訊，請參閱[支援的單位]({{site.url}}{{site.baseurl}}/api-reference/units/)。
`health` | 字串 | 根據索引的健康狀態加以限制。支援的值為 `green`、`yellow` 及 `red`。
`include_unloaded_segments` | 布林值 | 是否包含未載入記憶體之區段的資訊。預設為 `false`。
`cluster_manager_timeout` | 時間 | 等待連線至叢集管理員節點的時間量。預設為 `30s`。
`pri` | 布林值 | 是否僅傳回主要分片的資訊。預設為 `false`。
`time` | 時間 | 指定時間單位，例如 `5d` 或 `7h`。如需詳細資訊，請參閱[支援的單位]({{site.url}}{{site.baseurl}}/api-reference/units/)。
`expand_wildcards` | 列舉值 | 將萬用字元運算式展開為具體索引。以逗號合併多個值。支援的值為 `all`、`open`、`closed`、`hidden` 及 `none`。預設為 `open`。
`next_token` | 字串 | 擷取下一頁索引。當 `null` 時，僅提供第一頁索引。預設為 `null`。
`size` | 整數 | 單一頁面中要顯示的索引數上限。回應中單一頁面的索引數不一定等於指定的 `size`。預設為 `500`。最小值為 `1`，最大值為 `5000`。
`sort` | 字串 | 索引的顯示順序。若為 `desc`，則先顯示最近建立的索引。若為 `asc`，則先顯示最舊的索引。預設為 `asc`。

使用 `next_token` 路徑參數時，請使用回應所產生的權杖來查看下一頁索引。在 API 傳回 `null` 之後，即表示已傳回 API 中包含的所有索引。
{: .tip }


## 範例請求

若要取得所有索引的資訊，請使用下列查詢，並持續指定從回應收到的 `next_token`，直到其 `null`：

```json
GET _list/indices/{index}?v&next_token=token
```


若要將資訊限制為特定索引，請在查詢後新增索引名稱，如下列範例所示：

<!-- spec_insert_start
component: example_code
rest: GET /_list/indices/<index>?v
-->
{% capture step1_rest %}
GET /_list/indices/<index>?v
{% endcapture %}

{% capture step1_python %}


response = client.list.indices(
  index = "<index>",
  params = { "v": "true" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

若要取得多個索引的資訊，請以逗號分隔索引，如下列範例所示：

<!-- spec_insert_start
component: example_code
rest: GET /_list/indices/index1,index2,index3?v&next_token=token
-->
{% capture step1_rest %}
GET /_list/indices/index1,index2,index3?v&next_token=token
{% endcapture %}

{% capture step1_python %}


response = client.list.indices(
  index = "index1,index2,index3",
  params = { "v": "true", "next_token": "token" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->


## 範例回應

**純文字格式**

```json
health | status | index | uuid | pri | rep | docs.count | docs.deleted | store.size | pri.store.size
green  | open | movies | UZbpfERBQ1-3GSH2bnM3sg | 1 | 1 | 1 | 0 | 7.7kb | 3.8kb
next_token MTcyOTE5NTQ5NjM5N3wub3BlbnNlYXJjaC1zYXAtbG9nLXR5cGVzLWNvbmZpZw==
```

**JSON 格式**

```json
{
  "next_token": "MTcyOTE5NTQ5NjM5N3wub3BlbnNlYXJjaC1zYXAtbG9nLXR5cGVzLWNvbmZpZw==",
  "indices": [
    {
      "health": "green",
      "status": "open",
      "index": "movies",
      "uuid": "UZbpfERBQ1-3GSH2bnM3sg",
      "pri": "1",
      "rep": "1",
      "docs.count": "1",
      "docs.deleted": "0",
      "store.size": "7.7kb",
      "pri.store.size": "3.8kb"
    }
  ]
}
```
