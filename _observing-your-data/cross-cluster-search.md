---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "使用可觀測性應用程式進行跨叢集搜尋"
nav_order: 180
redirect_from:
  - /observing-your-data/cross-cluster-replication/
---

# 使用可觀測性應用程式進行跨叢集搜尋

透過跨叢集搜尋，您可以從 [事件分析]({{site.url}}{{site.baseurl}}/observing-your-data/event-analytics/) 或 Observability 工作區的記錄檔頁面查詢遠端 OpenSearch 叢集的索引。您在本機叢集上執行管線處理語言（Piped Processing Language，PPL）查詢，本機叢集會將查詢轉送至遠端叢集，並傳回合併後的結果。

## 必要條件

在查詢遠端叢集之前，請確認符合下列必要條件：

- 本機叢集可以連線至遠端叢集中至少一個節點的傳輸連接埠（預設為 `9300`）。
- 如果已啟用 Security 外掛程式，使用者必須擁有本機叢集的 PPL 權限，以及遠端叢集上所查詢索引的讀取權限。如需更多資訊，請參閱 [設定權限]({{site.url}}{{site.baseurl}}/search-plugins/cross-cluster-search/#setting-permissions)。

## 連線至遠端叢集

在本機叢集上，提供名稱以及一或多個節點的位址來註冊遠端叢集：

```json
PUT _cluster/settings
{
  "persistent": {
    "cluster.remote": {
      "my-remote-cluster": {
        "seeds": ["<remote-node-address>:9300"]
      }
    }
  }
}
```
{% include copy-curl.html %}

若要驗證連線，請傳送下列請求：

```json
GET _remote/info
```
{% include copy-curl.html %}

連線成功時，回應會包含遠端叢集的 `"connected": true`。如需更多關於回應的資訊，請參閱 [遠端叢集資訊]({{site.url}}{{site.baseurl}}/api-reference/cluster-api/remote-info/)。

如需更多關於連線叢集的資訊，包括節點角色需求以及 Docker、Kubernetes 與代理伺服器設定的範例，請參閱 [跨叢集搜尋]({{site.url}}{{site.baseurl}}/search-plugins/cross-cluster-search/)。

## 查詢遠端叢集

在 PPL 查詢中，將遠端索引指定為 `<remote-cluster-name>:<index-name>`。您可以在單一查詢中查詢多個叢集，如下表所示。

| 查詢 | 搜尋範圍 |
|:---|:---|
| `source = my-remote-cluster:application-logs` | `my-remote-cluster` 中的 `application-logs` 索引 |
| `source = *:application-logs` | 每個已連線遠端叢集中的 `application-logs` 索引 |
| `source = application-logs, my-remote-cluster:application-logs` | 本機叢集與 `my-remote-cluster` 中的 `application-logs` 索引 |

### 使用 Event analytics

若要在 Event analytics 中查詢遠端叢集，請依照下列步驟操作：

1. 在頂端選單中，前往 **Observability** > **Logs**，然後選取 **Event Explorer**。
1. 在查詢列中，輸入指定遠端索引的 PPL 查詢。例如，下列查詢會從 `my-remote-cluster` 的 `application-logs` 索引傳回伺服器錯誤：

   ```sql
   source = my-remote-cluster:application-logs | where status >= 500 | fields @timestamp, service, status, message
   ```
   {% include copy.html %}

1. 選取時間範圍，然後選取 **Run**。

### 使用 Observability 工作區

在 Observability 工作區中，您可以在 [Logs]({{site.url}}{{site.baseurl}}/observing-your-data/exploring-observability-data/discover-logs/) 頁面查詢遠端叢集。資料集無法包含遠端索引，因此您必須在查詢中指定遠端索引。

若要在 Observability 工作區中查詢遠端叢集，請依照下列步驟操作：

1. 在您的 Observability 工作區中，前往 **Logs**。
1. 選取一個資料集。
1. 在查詢編輯器中，將 `source` 替換為遠端索引，例如 `source = my-remote-cluster:application-logs | where status >= 500`。
1. 選取時間範圍，然後執行查詢。

## 常見問題

本節說明常見問題及其解決方法。

### 查詢失敗並出現 `no such index` 錯誤

如果對遠端索引的 PPL 查詢失敗並出現 `no such index` 錯誤，即使該索引存在於遠端叢集上，請在本機叢集上建立一個空索引，其名稱與索引對應須和遠端索引相同。查詢會從遠端叢集傳回文件，而不是從本機索引傳回。

## 相關文件

- 如需設定範例與安全性組態，請參閱 [跨叢集搜尋]({{site.url}}{{site.baseurl}}/search-plugins/cross-cluster-search/)。
- 如需 PPL 限制與跨叢集查詢的驗證詳細資訊，請參閱 [SQL 外掛程式文件中的跨叢集搜尋](https://github.com/opensearch-project/sql/blob/main/docs/user/ppl/admin/cross_cluster_search.md)。
