---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "開啟索引"
parent: Core index APIs
grand_parent: Index APIs
nav_order: 50
redirect_from:
  - /opensearch/rest-api/index-apis/open-index/
---

# Open Index API
**於 1.0 版推出**
{: .label .label-purple }

開啟索引 API 操作會開啟已關閉的索引，讓您可以在索引中新增或搜尋資料。


## 端點

```json
POST /{index}/_open
```

## 路徑參數

參數 | 類型 | 說明
:--- | :--- | :---
&lt;index&gt; | 字串 | 要開啟的索引。可以是以逗號分隔的多個索引名稱清單。使用 `_all` 或 * 可開啟所有索引。

## 查詢參數

所有參數皆為選用。

參數 | 類型 | 說明
:--- | :--- | :---
`allow_no_indices` | 布林值 | 是否忽略未符合任何索引的萬用字元。預設為 `true`。
`expand_wildcards` | 字串 | 將萬用字元運算式展開為不同的索引。使用逗號組合多個值。可用值為 all（符合所有索引）、open（符合已開啟的索引）、closed（符合已關閉的索引）、hidden（符合隱藏的索引）及 none（不接受萬用字元運算式）。預設為 `open`。
`ignore_unavailable` | 布林值 | 若為 true，OpenSearch 不會搜尋不存在或已關閉的索引。預設為 `false`。
`wait_for_active_shards` | 字串 | 指定 OpenSearch 處理請求前必須可用的作用中分片數量。預設為 1（僅主要分片）。設定為 all 或正整數。大於 1 的值需要副本。例如，若您指定的值為 3，索引必須有兩個副本，分散在另外兩個節點上，請求才能成功。
`cluster_manager_timeout` | 時間 | 等待連線至叢集管理員節點的時間。預設為 `30s`。
`timeout` | 時間 | 等待叢集回應的時間。預設為 `30s`。
`wait_for_completion` | 布林值 | 設定為 `false` 時，請求會立即傳回，而不會等到操作完成。若要監視操作狀態，請使用 [Tasks API]({{site.url}}{{site.baseurl}}/api-reference/tasks/)，並提供請求傳回的任務 ID。預設為 `true`。
`task_execution_timeout` | 時間 | 明確指定的任務執行逾時時間。僅在 wait_for_completion 設定為 `false` 時有用。預設為 `1h`。

## 請求範例

<!-- spec_insert_start
component: example_code
rest: POST /sample-index/_open
-->
{% capture step1_rest %}
POST /sample-index/_open
{% endcapture %}

{% capture step1_python %}


response = client.indices.open(
  index = "sample-index"
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->


## 回應範例
```json
{
  "acknowledged": true,
  "shards_acknowledged": true
}
```

## 必要權限

若您使用 Security 外掛程式，請確認您具備適當的權限：`indices:admin/open`。
