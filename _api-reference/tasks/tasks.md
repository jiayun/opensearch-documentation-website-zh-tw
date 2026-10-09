---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Tasks APIs
has_children: yes
nav_order: 130
redirect_from:
 - /opensearch/rest-api/tasks/
 - /api-reference/tasks/
---

# Tasks APIs
**1.0 版新增**
{: .label .label-purple }

_任務_是您在叢集中執行的任何作業。例如，在您的書籍資料集合中依書名或作者名稱進行搜尋，就是一項任務。當您執行 OpenSearch 時，系統會自動建立一個任務來監控叢集的健康狀態與效能。若要取得叢集中目前正在執行之所有任務的更多資訊，您可以使用 `tasks` API 作業。

## 將標頭附加至任務

若要將請求與任務建立關聯以方便追蹤，您可以在 `curl` 命令的 HTTPS 請求讀取器中提供 `X-Opaque-Id:<ID_number>` 標頭。API 會在傳回的結果中附加指定的標頭。

下列請求會傳回 `X-Opaque-Id` 為 `111111` 的任務：

```bash
curl -i -H "X-Opaque-Id: 111111" "https://localhost:9200/_tasks" -u 'admin:<custom-admin-password>' --insecure
```
{% include copy.html %}

`_tasks` 作業會傳回下列結果：

```json
HTTP/1.1 200 OK
X-Opaque-Id: 111111
content-type: application/json; charset=UTF-8
content-length: 768

{
  "nodes": {
    "Mgqdm0r9SEGClWxp_RbnaQ": {
      "name": "opensearch-node1",
      "transport_address": "172.18.0.4:9300",
      "host": "172.18.0.4",
      "ip": "172.18.0.4:9300",
      "roles": [
        "data",
        "ingest",
        "master",
        "remote_cluster_client"
      ],
      "tasks": {
        "Mgqdm0r9SEGClWxp_RbnaQ:30072": {
          "node": "Mgqdm0r9SEGClWxp_RbnaQ",
          "id": 30072,
          "type": "direct",
          "action": "cluster:monitor/tasks/lists[n]",
          "start_time_in_millis": 1613166701725,
          "running_time_in_nanos": 245400,
          "cancellable": false,
          "parent_task_id": "Mgqdm0r9SEGClWxp_RbnaQ:30071",
          "headers": {
            "X-Opaque-Id": "111111"
          }
        },
        "Mgqdm0r9SEGClWxp_RbnaQ:30071": {
          "node": "Mgqdm0r9SEGClWxp_RbnaQ",
          "id": 30071,
          "type": "transport",
          "action": "cluster:monitor/tasks/lists",
          "start_time_in_millis": 1613166701725,
          "running_time_in_nanos": 658200,
          "cancellable": false,
          "headers": {
            "X-Opaque-Id": "111111"
          }
        }
      }
    }
  }
}
```
此作業支援與 `tasks` 作業相同的參數。下列範例說明如何將 `X-Opaque-Id` 與特定任務建立關聯：

```bash
curl -i -H "X-Opaque-Id: 123456" "https://localhost:9200/_tasks?nodes=opensearch-node1" -u 'admin:<custom-admin-password>' --insecure
```
{% include copy.html %}
