---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "複製快照"
parent: Snapshot APIs
nav_order: 10
---

# Clone Snapshot API
**於 1.0 版導入**
{: .label .label-purple }

在與原始快照相同的儲存庫中，建立整個或部分快照的複本。


<!-- spec_insert_start
api: snapshot.clone
component: endpoints
-->
## 端點
```json
PUT /_snapshot/{repository}/{snapshot}/_clone/{target_snapshot}
```
<!-- spec_insert_end -->

<!-- spec_insert_start
api: snapshot.clone
component: path_parameters
-->
## 路徑參數

下表列出可用的路徑參數。

| 參數 | 必要 | 資料類型 | 說明 |
| :--- | :--- | :--- | :--- |
| `repository` | **必要** | String | 將包含快照複本的儲存庫名稱。 |
| `snapshot` | **必要** | String | 原始快照的名稱。 |
| `target_snapshot` | **必要** | String | 複製後快照的名稱。 |

<!-- spec_insert_end -->


<!-- spec_insert_start
api: snapshot.clone
component: query_parameters
include_deprecated: false
-->
## 查詢參數

下表列出可用的查詢參數。所有查詢參數皆為選用。

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `cluster_manager_timeout` | String | 等待叢集管理員節點回應的時間。如需支援的時間單位詳細資訊，請參閱 [Common parameters]({{site.url}}{{site.baseurl}}/api-reference/units/#time-units)。 |

<!-- spec_insert_end -->


## 範例請求

下列請求會將快照儲存庫 `my-opensearch-repo` 中名為 `my_snapshot` 的快照內的索引 `index_a` 與 `index_b`，複製到同一儲存庫中名為 `my_new_snapshot` 的新快照：

<!-- spec_insert_start
component: example_code
rest: PUT /_snapshot/my-opensearch-repo/my_snapshot/_clone/my_new_snapshot
body: |
{
	“indices” : “index_a,index_b”
}
-->
{% capture step1_rest %}
PUT /_snapshot/my-opensearch-repo/my_snapshot/_clone/my_new_snapshot
{
	“indices” : “index_a,index_b”
}
{% endcapture %}

{% capture step1_python %}


response = client.snapshot.clone(
  repository = "my-opensearch-repo",
  snapshot = "my_snapshot",
  target_snapshot = "my_new_snapshot",
  body = '''
{
	“indices” : “index_a,index_b”
}
'''
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->


## 範例回應

成功建立快照複本會傳回下列回應：

```json
{ 
    "acknowledged" : true
}
```

## 必要權限

如果您使用 Security 外掛程式，請確認您具備適當的權限：`cluster:admin/snapshot/clone`。
