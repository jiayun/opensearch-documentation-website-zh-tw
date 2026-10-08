---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "刪除任務"
parent: Tasks APIs
nav_order: 30
---

# Delete Task API
**於 3.9 版推出**
{: .label .label-purple }

使用 Delete Task API 刪除已完成任務的已儲存結果。例如，當您執行支援的操作並設定 `wait_for_completion=false` 時，OpenSearch 會儲存任務結果，讓您稍後可以使用 [Get Task API]({{site.url}}{{site.baseurl}}/api-reference/tasks/get-tasks/) 擷取結果。當您不再需要結果時，請將其刪除以釋放相關的儲存空間。

Delete Task API 不會取消或刪除執行中的任務。若要停止執行中的任務，請使用 [Cancel Tasks API]({{site.url}}{{site.baseurl}}/api-reference/tasks/cancel-tasks/)。
{: .important }

<!-- spec_insert_start
api: tasks.delete
component: endpoints
-->
## 端點
```json
DELETE /_tasks/{task_id}
```
<!-- spec_insert_end -->

<!-- spec_insert_start
api: tasks.delete
component: path_parameters
-->
## 路徑參數

下表列出可用的路徑參數。

| 參數 | 必要 | 資料類型 | 說明 |
| :--- | :--- | :--- | :--- |
| `task_id` | **必要** | 字串 | 要刪除的已儲存之已完成任務結果的 ID（`node_id:task_number`）。 |

<!-- spec_insert_end -->

## 請求範例

下列請求會刪除任務 `JzrCxdtFTCO_RaINw8ckNA:54321` 的已儲存結果：

<!-- spec_insert_start
component: example_code
rest: DELETE /_tasks/JzrCxdtFTCO_RaINw8ckNA:54321
-->
{% capture step1_rest %}
DELETE /_tasks/JzrCxdtFTCO_RaINw8ckNA:54321
{% endcapture %}

{% capture step1_python %}


response = client.tasks.delete(
  task_id = "JzrCxdtFTCO_RaINw8ckNA:54321"
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 回應範例

OpenSearch 刪除已儲存的結果後，會回傳確認回應：

```json
{
  "acknowledged": true
}
```

成功刪除後，Get Task API 會針對該任務回傳 `404 Not Found` 回應。

## 父任務與子任務

當任務仍有執行中的子任務或已儲存的子任務結果時，您無法刪除該任務的已儲存結果。在已儲存任務結果的階層中，請從葉節點朝根節點依序刪除結果。例如，先刪除孫任務的結果，再刪除其父任務的結果，最後刪除根任務的結果。

如果任務有執行中的子任務或已儲存的子任務結果，OpenSearch 會回傳 `409 Conflict` 回應。

## 回應碼

下表列出常見的回應碼。

| HTTP 狀態碼 | 說明 |
| :--- | :--- |
| `200 OK` | 已刪除已儲存的已完成任務結果。 |
| `404 Not Found` | 任務未在執行，且沒有已儲存的結果。 |
| `409 Conflict` | 任務仍在執行、尚未標記為已完成、有執行中的子任務，或有已儲存的子任務結果。 |

## 必要權限

如果您使用 Security 外掛程式，請確保您具有適當的權限：`cluster:admin/tasks/delete`。
