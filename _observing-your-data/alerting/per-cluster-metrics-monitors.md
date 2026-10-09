---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "個別叢集指標監視器"
nav_order: 15
parent: Monitors
grand_parent: Alerting
has_children: false
---

# 個別叢集指標監視器

_個別叢集指標監視器_ 是一種警示監視器，可收集並分析單一叢集的指標，提供叢集效能與健全狀態的相關資訊。您可以設定警示來監視特定條件，例如：

- 叢集健全狀態變為黃色或紅色。
- 叢集層級指標（例如 CPU 使用率與 JVM 記憶體使用量）達到指定閾值。
- 節點層級指標（例如可用磁碟空間、JVM 記憶體使用量與 CPU 使用率）達到指定閾值。
- 儲存的文件總數達到指定閾值。

## 建立叢集指標監視器

若要建立叢集指標監視器，請依照下列步驟操作：

1. 選取 **Alerting** > **Monitors** > **Create monitor**。
2. 選取 **Per cluster metrics monitor** 選項。
3. 在 Query 區段中，從下拉式清單選擇 **Request type**。
4. （選用）如果您想篩選 API 回應，僅使用特定路徑參數，請在 **Path parameters** 下輸入這些參數。大多數可用於監視叢集狀態的 API 都支援其文件中所述的路徑參數（例如以逗號分隔的索引名稱清單）。
5. 在[觸發條件]({{site.url}}{{site.baseurl}}/observing-your-data/alerting/triggers/)區段中，指定哪些條件會觸發警示。觸發條件會自動填入 `painless ctx` 變數。例如，監視 Cluster Stats 的叢集監視器使用觸發條件 `ctx.results[0].indices.count <= 0`，根據查詢傳回的索引數量觸發警示。若要進一步細化條件，請新增 API 支援的任何其他 Painless 條件。若要查看條件回應的範例，請選取 **Preview condition response**。
6. 在 Actions 區段中，指定觸發條件滿足時，您希望如何通知使用者。
7. 選取 **Create**。您的新監視器會出現在 **Monitors** 清單中。

下列範例顯示叢集指標監視器的組態。

![叢集指標監視器]({{site.url}}{{site.baseurl}}/images/cluster-metrics.png){: width="700" }

## 支援的 API

觸發條件使用下列 API 端點的回應。大多數可用於監視叢集狀態的 API 都支援路徑參數（例如以逗號分隔的索引名稱清單）。這些 API 不支援查詢參數。

- [`_cluster/health`]({{site.url}}{{site.baseurl}}/api-reference/cluster-health/)
- [`_cluster/stats`]({{site.url}}{{site.baseurl}}/api-reference/cluster-stats/)
- [`_cluster/settings`]({{site.url}}{{site.baseurl}}/api-reference/cluster-settings/)
- [`_nodes/stats`]({{site.url}}{{site.baseurl}}/opensearch/popular-api/#get-node-statistics)
- [`_cat/indices`]({{site.url}}{{site.baseurl}}/api-reference/cat/cat-indices/)
- [`_cat/pending_tasks`]({{site.url}}{{site.baseurl}}/api-reference/cat/cat-pending-tasks/)
- [`_cat/recovery`]({{site.url}}{{site.baseurl}}/api-reference/cat/cat-recovery/)
- [`_cat/shards`]({{site.url}}{{site.baseurl}}/api-reference/cat/cat-shards/)
- [`_cat/snapshots`]({{site.url}}{{site.baseurl}}/api-reference/cat/cat-snapshots/)
- [`_cat/tasks`]({{site.url}}{{site.baseurl}}/api-reference/cat/cat-tasks/)

## 限制 API 欄位

如果您想隱藏 API 回應中的欄位，避免將其提供給警示使用，請重新設定 Alerting 外掛程式內的 [supported_json_payloads.json](https://github.com/opensearch-project/alerting/blob/main/alerting/src/main/resources/org/opensearch/alerting/settings/supported_json_payloads.json) 檔案。此檔案可作為您想在警示中使用的 API 欄位允許清單。預設情況下，所有 API 及其參數都可用於監視器與觸發條件。

不過，您可以修改此檔案，讓叢集指標監視器只能針對檔案中參照的 API 建立。此外，只有支援檔案中參照的欄位才能用來建立觸發條件。此 `supported_json_payloads.json` 允許為 `_cluster/stats` API 建立叢集指標監視器，並為 `indices.shards.total` 與 `indices.shards.index.shards.min` 欄位設定觸發條件。

```json
"/_cluster/stats": {
  "indices": [
    "shards.total",
    "shards.index.shards.min"
  ]
}
```

## Painless 觸發條件

Painless 指令碼可定義叢集指標監視器的觸發條件，類似於使用擷取查詢定義選項所定義的個別查詢或個別桶監視器。Painless 指令碼由至少一個陳述式，以及您希望執行的任何其他函式組成。如需詳細資訊，請參閱 [Painless 指令碼語言]({{site.url}}{{site.baseurl}}/scripting/painless/)。

叢集指標監視器最多支援 **十個** 觸發條件。

在下列範例中，監視器設定為對兩個叢集 `cluster-1` 和 `cluster-2` 呼叫 Cluster Health API。當任一叢集的 `status` 不是 `green` 時，觸發條件就會建立警示。

`script` 參數將 `source` 指向 Painless 指令碼 `for (cluster in ctx.results[0].keySet()) if (ctx.results[0][cluster].status != \"green\") return true`。如需更多 `painless ctx` 變數選項，請參閱[觸發條件變數]({{site.url}}{{site.baseurl}}/observing-your-data/alerting/triggers/#trigger-variables)。

```json
{
  "name": "Cluster Health Monitor",
  "type": "monitor",
  "monitor_type": "query_level_monitor",
  "enabled": true,
  "schedule": {
    "period": {
      "unit": "MINUTES",
      "interval": 1
    }
  },
  "inputs": [
    {
      "uri": {
        "path": "_cluster/health/",
        "path_params": "",
        "url": "http://localhost:9200/_cluster/health/",
        "clusters": ["cluster-1", "cluster-2"]
      }
    }
  ],
  "triggers": [
    {
      "query_level_trigger": {
        "id": "Tf_L_nwBti6R6Bm-18qC",
        "name": "Yellow status trigger",
        "severity": "1",
        "condition": {
          "script": {
            "source": "for (cluster in ctx.results[0].keySet()) if (ctx.results[0][cluster].status != \"green\") return true",
            "lang": "painless"
          }
        },
        "actions": []
      }
    }
  ]
}
```
儀表板介面支援選取要監視的叢集及所需的 API。下圖顯示此介面。

若要透過儀表板 UI 建立跨叢集監視器，需要下列[權限]({{site.url}}{{site.baseurl}}/security/access-control/permissions/)：`cluster:admin/opensearch/alerting/remote/indexes/get`、`indices:admin/resolve/index`、`cluster:monitor/health` 和 `indices:admin/mappings/get`。
{: .note}

![叢集指標監視器]({{site.url}}{{site.baseurl}}/images/alerting/cross-cluster-cluster-metrics-monitors.png){: width="700" }

### 限制

個別叢集指標監視器有下列限制：

- OpenSearch 叢集必須處於可監視索引條件，並可對該索引執行動作的狀態。
- 移除使用者對某個資源的權限，不會阻止該使用者先前為該資源建立的監視器執行。
- 具有建立監視器權限的使用者，可以為自己沒有權限的資源建立監視器；不過，這些監視器不會執行。
