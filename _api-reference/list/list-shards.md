---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "列出分片"
parent: List APIs
nav_order: 20
---

# List Shards API
**2.18 版推出**
{: .label .label-purple }

列出分片操作會以分頁格式輸出所有主要分片與副本分片的狀態，以及其分布方式。

## 端點

```json
GET _list/shards
GET _list/shards/{index}
```

## 查詢參數

所有參數皆為選用。

參數 | 類型 | 說明
:--- | :--- | :---
`bytes` | 位元組大小 | 指定位元組大小的單位，例如 `7kb` 或 `6gb`。如需詳細資訊，請參閱[支援的單位]({{site.url}}{{site.baseurl}}/api-reference/units/)。
`local` | 布林值 | 是否僅從本機節點傳回資訊，而非從叢集管理員節點傳回。預設為 `false`。
`cluster_manager_timeout` | 時間 | 等待連線至叢集管理員節點的時間長度。預設為 `30s`。
`cancel_after_time_interval` | 時間 | 分片請求在經過此時間長度後會取消。預設為 `-1`（無逾時限制）。
`time` | 時間 | 指定時間單位，例如 `5d` 或 `7h`。如需詳細資訊，請參閱[支援的單位]({{site.url}}{{site.baseurl}}/api-reference/units/)。
`next_token` | 字串 | 擷取下一頁索引。當值為 `null` 時，僅提供第一頁索引。預設為 `null`。
`size` | 整數 | 單一頁面上顯示的索引數量上限。回應中單一頁面上的索引數量不一定等於指定的 `size`。預設值與最小值皆為 `2000`。最大值為 `20000`。
`sort` | 字串 | 索引的顯示順序。如果為 `desc`，則優先顯示最近建立的索引。如果為 `asc`，則優先顯示最早建立的索引。預設為 `asc`。

使用 `next_token` 查詢參數時，請使用回應產生的權杖來查看下一頁索引。當 API 傳回 `null` 後，表示 API 中包含的所有索引皆已傳回。
{: .tip }

## 範例請求

若要取得所有索引與分片的資訊，請傳送以下請求：

```json
GET /_list/shards?v
```

若要取得下一頁的分片，請傳遞上一個回應中的 `next_token` 值。重複此請求，直到回應傳回的 `next_token` 為 `null`：

```json
GET /_list/shards?v&next_token=<next_token>
```

若要將資訊限制在特定索引，請在查詢後加上索引名稱，如下列範例所示：

<!-- spec_insert_start
component: example_code
rest: GET /_list/shards/<index>?v
-->
{% capture step1_rest %}
GET /_list/shards/<index>?v
{% endcapture %}

{% capture step1_python %}


response = client.list.shards(
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
rest: GET /_list/shards/index1,index2,index3?v
-->
{% capture step1_rest %}
GET /_list/shards/index1,index2,index3?v
{% endcapture %}

{% capture step1_python %}


response = client.list.shards(
  index = "index1,index2,index3",
  params = { "v": "true" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 回應範例

**純文字格式**

```json
index | shard | prirep | state   | docs | store | ip |       | node
plugins | 0   |   p    | STARTED |   0  |  208b | 172.18.0.4 | odfe-node1
plugins | 0   |   r    | STARTED |   0  |  208b | 172.18.0.3 |  odfe-node2
....
....
next_token MTcyOTE5NTQ5NjM5N3wub3BlbnNlYXJjaC1zYXAtbG9nLXR5cGVzLWNvbmZpZw==   
```

**JSON 格式**

```json
{
  "next_token": "MTcyOTE5NTQ5NjM5N3wub3BlbnNlYXJjaC1zYXAtbG9nLXR5cGVzLWNvbmZpZw==",
  "shards": [
    {
      "index": "plugins",
      "shard": "0",
      "prirep": "p",
      "state": "STARTED",
      "docs": "0",
      "store": "208B",
      "ip": "172.18.0.4",
      "node": "odfe-node1"
    },
    {
      "index": "plugins",
      "shard": "0",
      "prirep": "r",
      "state": "STARTED",
      "docs": "0",
      "store": "208B",
      "ip": "172.18.0.3",
      "node": "odfe-node2"
    }
  ]
}
```
