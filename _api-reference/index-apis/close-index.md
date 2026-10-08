---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "關閉索引"
parent: Core index APIs
grand_parent: Index APIs
nav_order: 60
redirect_from:
  - /opensearch/rest-api/index-apis/close-index/
---

# 關閉索引 API
**於 1.0 版推出**
{: .label .label-purple }

關閉索引 API 作業會關閉索引。索引一旦關閉，您就無法對其新增資料，也無法在該索引內搜尋任何資料。


## 端點

```json
POST /{index}/_close
```

## 路徑參數

參數 | 類型 | 說明
:--- | :--- | :---
&lt;index&gt; | 字串 | 要關閉的索引。可以是以逗號分隔的多個索引名稱清單。使用 `_all` 或 * 可關閉所有索引。

## 查詢參數

所有參數皆為選用。

參數 | 類型 | 說明
:--- | :--- | :---
`allow_no_indices` | 布林值 | 是否忽略未符合任何索引的萬用字元。預設為 `true`。
`expand_wildcards` | 字串 | 將萬用字元運算式展開為不同的索引。使用逗號組合多個值。可用的值為 all（符合所有索引）、open（符合開啟的索引）、closed（符合關閉的索引）、hidden（符合隱藏的索引）及 none（不接受萬用字元運算式）。預設為 `open`。
`ignore_unavailable` | 布林值 | 若為 true，OpenSearch 不會搜尋遺失或關閉的索引。預設為 `false`。
`wait_for_active_shards` | 字串 | 指定 OpenSearch 處理請求前必須可用的作用中分片數量。預設為 1（僅主要分片）。設定為 all 或正整數。大於 1 的值需要副本。例如，若您指定值為 3，索引必須有兩個副本，分散於另外兩個節點上，請求才能成功。
`cluster_manager_timeout` | 時間 | 等待連線至叢集管理員節點的時間長度。預設為 `30s`。
`timeout` | 時間 | 等待叢集回應的時間長度。預設為 `30s`。

## 請求範例

<!-- spec_insert_start
component: example_code
rest: POST /sample-index/_close
body: 
-->
{% capture step1_rest %}
POST /sample-index/_close

{% endcapture %}

{% capture step1_python %}


response = client.indices.close(
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
  "shards_acknowledged": true,
  "indices": {
    "sample-index1": {
      "closed": true
    }
  }
}
```

## 必要權限

若您使用 Security 外掛程式，請確保您具備適當的權限：`indices:admin/close` 和 `indices:admin/close*`。
