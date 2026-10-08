---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "懸空索引"
parent: Index APIs
nav_order: 90
---

# 懸空索引 API
**於 1.0 版導入**
{: .label .label-purple }

當節點加入叢集後，如果節點的本機目錄中存在叢集中尚未存在的分片，就會產生懸空索引。懸空索引可以列出、刪除或匯入。

## 端點

列出懸空索引：

```json
GET /_dangling
```

匯入懸空索引：

```json
POST /_dangling/{index-uuid}
```

刪除懸空索引：

```json
DELETE /_dangling/{index-uuid}
```

## 路徑參數

路徑參數為必要。

路徑參數 | 說明
:--- | :---
`index-uuid` | 索引的 UUID。

## 查詢參數

查詢參數為選用。

查詢參數 | 資料類型 | 說明
:--- | :--- | :---
`accept_data_loss` | 布林值 | 對於 `import` 或 `delete` 必須設定為 `true`，因為 OpenSearch 無法得知懸空索引資料的來源。
`timeout` | 時間單位 | 等待回應的時間長度。如果在設定的時間內未收到回應，則會傳回錯誤。預設為 `30` 秒。
`cluster_manager_timeout` | 時間單位 | 等待連線至叢集管理員節點的時間長度。如果在設定的時間內未收到回應，則會傳回錯誤。預設為 `30` 秒。

## 範例請求：列出懸空索引

<!-- spec_insert_start
component: example_code
rest: GET /_dangling
-->
{% capture step1_rest %}
GET /_dangling
{% endcapture %}

{% capture step1_python %}

response = client.dangling_indices.list_dangling_indices()
{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 範例請求：匯入懸空索引

<!-- spec_insert_start
component: example_code
rest: POST /_dangling/msdjernajxAT23RT-BupMB?accept_data_loss=true
-->
{% capture step1_rest %}
POST /_dangling/msdjernajxAT23RT-BupMB?accept_data_loss=true
{% endcapture %}

{% capture step1_python %}


response = client.dangling_indices.import_dangling_index(
  index_uuid = "msdjernajxAT23RT-BupMB",
  params = { "accept_data_loss": "true" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

 
## 範例請求：刪除懸空索引

<!-- spec_insert_start
component: example_code
rest: DELETE /_dangling/msdjernajxAT23RT-BupMB?accept_data_loss=true
-->
{% capture step1_rest %}
DELETE /_dangling/msdjernajxAT23RT-BupMB?accept_data_loss=true
{% endcapture %}

{% capture step1_python %}


response = client.dangling_indices.delete_dangling_index(
  index_uuid = "msdjernajxAT23RT-BupMB",
  params = { "accept_data_loss": "true" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 範例回應 

````json
{
    "_nodes": {
        "total": 1,
        "successful": 1,
        "failed": 0
    },
    "cluster_name": "opensearch-cluster",
    "dangling_indices": [msdjernajxAT23RT-BupMB]
}
````
