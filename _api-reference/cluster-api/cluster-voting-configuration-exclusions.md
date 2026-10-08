---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "投票組態排除項目"
parent: Cluster APIs
nav_order: 75
---

# 投票組態排除項目 API
**於 1.0 版推出**
{: .label .label-purple }

`_cluster/voting_config_exclusions` API 可讓您從投票組態中排除一或多個節點。當您想要安全地從叢集中移除具備叢集管理員資格的節點，或變更目前的叢集管理員時，這項功能很有用。

## 新增投票組態排除項目

使用 POST 方法新增投票組態排除項目。

### 端點
```json
POST /_cluster/voting_config_exclusions
```

### 查詢參數

下表列出可用的查詢參數。所有查詢參數皆為選用。

| 參數    | 資料類型      | 說明                                                                                                                                                                                                                                                                 |
|:-------------|:---------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `node_ids` | 清單或字串 | 要從投票組態中排除的節點 ID 清單，以逗號分隔。使用此設定時，您不能同時指定 `node_names`。必須提供 `node_ids` 或 `node_names`，才能收到有效的回應。                                                     |
| `node_names` | 清單或字串 | 要從投票組態中排除的節點名稱清單，以逗號分隔。使用此設定時，您不能同時指定 `node_ids`。必須提供 `node_ids` 或 `node_names`，才能收到有效的回應。                                                     |
| `timeout` | 字串 | 新增投票組態排除項目時，API 會等待指定的節點從投票組態中排除後，才傳回回應。如果在符合適當條件之前超過逾時期限，請求便會失敗並傳回錯誤。 |

### 範例

從投票組態中排除名為 `opensearch-node1` 的節點：

<!-- spec_insert_start
component: example_code
rest: POST /_cluster/voting_config_exclusions?node_names=opensearch-node1
body: 
-->
{% capture step1_rest %}
POST /_cluster/voting_config_exclusions?node_names=opensearch-node1

{% endcapture %}

{% capture step1_python %}


response = client.cluster.post_voting_config_exclusions(
  params = { "node_names": "opensearch-node1" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

或者，您可以使用以逗號分隔的清單指定節點 ID：

<!-- spec_insert_start
component: example_code
rest: POST /_cluster/voting_config_exclusions?node_ids=6ITS4DmNR7OJT1G5lyW8Lw,PEEW2S7-Su2XCA4zUE9_2Q
body: 
-->
{% capture step1_rest %}
POST /_cluster/voting_config_exclusions?node_ids=6ITS4DmNR7OJT1G5lyW8Lw,PEEW2S7-Su2XCA4zUE9_2Q

{% endcapture %}

{% capture step1_python %}


response = client.cluster.post_voting_config_exclusions(
  params = { "node_ids": "6ITS4DmNR7OJT1G5lyW8Lw,PEEW2S7-Su2XCA4zUE9_2Q" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 移除投票組態排除項目

使用 DELETE 方法清除先前從投票組態中排除的節點清單。這通常用於已安全移除或取代遭排除節點之後。您可以選擇等待節點從叢集中移除後，再清除排除項目。

### 端點

```json
DELETE /_cluster/voting_config_exclusions
```

### 查詢參數

下表列出可用的查詢參數。所有查詢參數皆為選用。

| 參數          | 資料類型 | 說明                                                                                                                                                                                                                                                                                                                                                                          |
|:-------------------|:----------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `wait_for_removal` | 布林值 | 指定是否等待所有遭排除的節點從叢集中移除後，再清除投票組態排除項目清單。當 `true` 時，所有遭排除的節點都會在此 API 採取任何動作之前從叢集中移除。當 `false` 時，即使部分遭排除的節點仍存在於叢集中，也會清除投票組態排除項目清單。_（預設：`true`）_ |

### 範例

使用下列請求移除所有投票組態排除項目，無須等待節點移除：

<!-- spec_insert_start
component: example_code
rest: DELETE /_cluster/voting_config_exclusions?wait_for_removal=false
body: 
-->
{% capture step1_rest %}
DELETE /_cluster/voting_config_exclusions?wait_for_removal=false

{% endcapture %}

{% capture step1_python %}


response = client.cluster.delete_voting_config_exclusions(
  params = { "wait_for_removal": "false" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

