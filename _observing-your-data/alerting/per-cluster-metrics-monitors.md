---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "個別叢集指標監視器"
nav_order: 15
parent: Monitors
grand_parent: Alerting
has_children: false
---

# 每個叢集指標監視器 (Per cluster metrics monitors)

每個叢集指標監視器會依排程執行叢集 API 請求，並使用觸發條件評估回應。您可以使用它來產生關於叢集狀態的警示，例如，在下列情況時：

- 叢集健康狀態達到黃色或紅色。
- 叢集層級指標，例如 CPU 使用率與 JVM 記憶體使用率，達到指定的門檻。
- 節點層級指標，例如可用磁碟空間、JVM 記憶體使用率與 CPU 使用率，達到指定的門檻。
- 儲存的文件總數達到指定的門檻。

## 建立個別叢集指標監視器

下列範例會建立一個監視器，在叢集健全狀態不是綠色時產生警示。

若要建立監視器，請依照下列步驟操作：

1. 在頂端選單中，前往 **OpenSearch Plugins** > **Alerting**。
1. 選取 **Monitors** 索引標籤，然後選取 **Create monitor**。
1. 在 **Monitor details** 中，輸入 **Monitor name**，例如 `Cluster health`，並選取 **Per cluster metrics monitor**。您也可以變更 **Schedule**。依預設，監視器每分鐘執行一次。
1. 在 **Select data** 中，保持選取本機叢集。若要監控遠端叢集，請在 **Select clusters** 中選取這些叢集。如需詳細資訊，請參閱[監控遠端叢集](#monitoring-remote-clusters)。
1. 在 **Query** 的 **Request type** 中，選取 **Cluster health**。您也可以在 **Path parameters** 中輸入路徑參數，以篩選 API 回應，例如以逗號分隔的索引名稱清單。若要檢視 API 回應，請選取 **Preview query**。
1. 在 **Triggers** 中，選取 **Add trigger**，然後設定觸發條件：
   - **Trigger name**：輸入 `Cluster health is not green`。
   - **Severity level**：保留 **1 (Highest)**。
   - **Trigger condition**：保留所選請求類型的預設條件 `ctx.results[0].status != "green"`。此條件是用來評估 API 回應的 [Painless]({{site.url}}{{site.baseurl}}/scripting/painless/) 指令碼。若要測試此條件，請選取 **Preview condition response**。
1. 您也可以在 **Actions** 中新增動作，在符合觸發條件時傳送通知。如需詳細資訊，請參閱[動作]({{site.url}}{{site.baseurl}}/observing-your-data/alerting/actions/)。
1. 選取 **Create**。

如果叢集健全狀態為黃色或紅色，監視器會產生處於 **Active** 狀態的警示。例如，若單一節點叢集包含具有副本的索引，其狀態會是黃色，因為無法指派副本。

個別叢集指標監視器最多支援 10 個觸發條件。如需可用於觸發條件的變數，請參閱[觸發條件變數]({{site.url}}{{site.baseurl}}/observing-your-data/alerting/triggers/#trigger-variables)。

## 使用 API 建立每個叢集指標監視器

若要使用 API 建立前述範例中的監視器，請傳送下列請求：

```json
POST _plugins/_alerting/monitors
{
  "type": "monitor",
  "monitor_type": "cluster_metrics_monitor",
  "name": "Cluster health",
  "enabled": true,
  "schedule": {
    "period": {
      "interval": 1,
      "unit": "MINUTES"
    }
  },
  "inputs": [
    {
      "uri": {
        "api_type": "CLUSTER_HEALTH",
        "path": "_cluster/health",
        "path_params": ""
      }
    }
  ],
  "triggers": [
    {
      "query_level_trigger": {
        "name": "Cluster health is not green",
        "severity": "1",
        "condition": {
          "script": {
            "source": "ctx.results[0].status != \"green\"",
            "lang": "painless"
          }
        },
        "actions": []
      }
    }
  ]
}
```
{% include copy-curl.html %}

如需監視器 API 的更多資訊，請參閱 [Alerting API]({{site.url}}{{site.baseurl}}/observing-your-data/alerting/api/)。

## 支援的 API

每個叢集指標監視器可以呼叫下列 API。使用 API 建立監視器時，`api_type` 欄會列出要在 `inputs.uri.api_type` 欄位中使用的值。這些 API 支援路徑參數，例如以逗號分隔的索引名稱清單，但不支援查詢參數。

API | `api_type` | OpenSearch Dashboards 中的請求類型
:--- | :--- | :---
[Cluster Health]({{site.url}}{{site.baseurl}}/api-reference/cluster-api/cluster-health/) | `CLUSTER_HEALTH` | **Cluster health**
[Cluster Settings]({{site.url}}{{site.baseurl}}/api-reference/cluster-api/cluster-settings/) | `CLUSTER_SETTINGS` | **Cluster settings**
[Cluster Stats]({{site.url}}{{site.baseurl}}/api-reference/cluster-api/cluster-stats/) | `CLUSTER_STATS` | **Cluster stats**
[CAT Indices]({{site.url}}{{site.baseurl}}/api-reference/cat/cat-indices/) | `CAT_INDICES` | **List indices**
[CAT Pending Tasks]({{site.url}}{{site.baseurl}}/api-reference/cat/cat-pending-tasks/) | `CAT_PENDING_TASKS` | **List pending tasks**
[CAT Recovery]({{site.url}}{{site.baseurl}}/api-reference/cat/cat-recovery/) | `CAT_RECOVERY` | **List index and shard recoveries**
[CAT Shards]({{site.url}}{{site.baseurl}}/api-reference/cat/cat-shards/) | `CAT_SHARDS` | **List shards**
[CAT Snapshots]({{site.url}}{{site.baseurl}}/api-reference/cat/cat-snapshots/) | `CAT_SNAPSHOTS` | **List snapshots**
[CAT Tasks]({{site.url}}{{site.baseurl}}/api-reference/cat/cat-tasks/) | `CAT_TASKS` | **List tasks**
[Nodes Stats]({{site.url}}{{site.baseurl}}/api-reference/nodes-apis/nodes-stats/) | `NODES_STATS` | 無法使用。請使用 API。

## 限制 API 欄位

若要限制個別叢集指標監視器可使用的 API 與回應欄位，請修改 Alerting 外掛程式內的 [supported_json_payloads.json](https://github.com/opensearch-project/alerting/blob/main/alerting/src/main/resources/org/opensearch/alerting/settings/supported_json_payloads.json) 檔案。此檔案的作用如同允許清單。預設情況下，監視器與觸發條件可以使用所有支援的 API 及其回應欄位。

如果您修改此檔案，則只能為檔案中列出的 API 建立個別叢集指標監視器，且觸發條件只能使用檔案中列出的欄位。例如，下列項目允許為 Cluster Stats API 建立監視器，並允許觸發條件使用 `indices.shards.total` 與 `indices.shards.index.shards.min` 欄位：

```json
"/_cluster/stats": {
  "indices": [
    "shards.total",
    "shards.index.shards.min"
  ]
}
```

## 監視遠端叢集

每個叢集指標監視器可以在多個叢集上呼叫 API。在 OpenSearch Dashboards 中，於 **Select clusters** 選取叢集。使用 API 時，在 `inputs.uri.clusters` 欄位中列出叢集，例如 `"clusters": ["cluster-1", "cluster-2"]`。

當監視器在多個叢集上呼叫 API 時，`ctx.results[0]` 會包含每個叢集的回應，並以叢集名稱作為鍵值。下列觸發條件會在任一叢集的健康狀態不是綠色時產生警示：

```
for (cluster in ctx.results[0].keySet()) if (ctx.results[0][cluster].status != "green") return true
```
{% include copy.html %}

若要在 OpenSearch Dashboards 中建立跨叢集監視器，您需要下列[權限]({{site.url}}{{site.baseurl}}/security/access-control/permissions/)：`cluster:admin/opensearch/alerting/remote/indexes/get`、`indices:admin/resolve/index`、`cluster:monitor/health` 和 `indices:admin/mappings/get`。
{: .note}

下圖顯示一個在兩個叢集上呼叫 Cluster Health API 的每個叢集指標監視器。

![多個叢集的每個叢集指標監視器]({{site.url}}{{site.baseurl}}/images/alerting/cross-cluster-cluster-metrics-monitors.png){: width="700" }

## 限制

個別叢集指標監視器有以下限制：

- 叢集必須處於監視器可以執行且其動作可以被執行的狀態。
- 移除使用者的資源權限，並不會停止該使用者針對該資源既有的監視器執行。
- 具備建立監視器權限的使用者，不會被阻止為其沒有權限的資源建立監視器。不過，這些監視器不會執行。
