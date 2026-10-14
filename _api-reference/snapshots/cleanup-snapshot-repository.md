---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "清理快照儲存庫"
parent: Snapshot APIs
nav_order: 45
---

# 清理快照儲存庫 API
**於 1.0 版推出**
{: .label .label-purple }

清理快照儲存庫 API 會清除快照儲存庫中已不再被任何現有快照參照的資料。

## 端點

```json
POST /_snapshot/{repository}/_cleanup
```


## 路徑參數

下表列出可用的路徑參數。

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `repository` | 字串 | 快照儲存庫的名稱。 |

## 查詢參數

下表列出可用的查詢參數。所有查詢參數皆為選用。

| 參數 |  資料類型 | 說明 |
| :--- | :--- | :--- |
| `cluster_manager_timeout` | Time | 等待叢集管理員節點回應的時間長度。舊稱為 `master_timeout`。選用。預設為 30 秒。 |
| `timeout` | Time | 等待操作完成的時間長度。選用。|

## 範例請求

下列請求會從儲存庫 `my_backup` 移除所有過期資料：

<!-- spec_insert_start
component: example_code
rest: POST /_snapshot/my_backup/_cleanup
-->
{% capture step1_rest %}
POST /_snapshot/my_backup/_cleanup
{% endcapture %}

{% capture step1_python %}


response = client.snapshot.cleanup_repository(
  repository = "my_backup"
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->


## 範例回應

```json
{
	"results":{
		"deleted_bytes":40,
		"deleted_blobs":8
	}
}
```

## 回應本文欄位

下表列出所有回應本文欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `deleted_bytes` | 整數 | 刪除資料後，快照中釋出的位元組數。 |
| `deleted_blobs` | 整數 | 此請求從儲存庫清除的二進位大型物件 (BLOB) 數量。 |

