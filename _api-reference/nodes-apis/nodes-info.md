---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "節點資訊"
parent: Nodes APIs
nav_order: 10
---

# Nodes Info API
**於 1.0 版推出**
{: .label .label-purple }

Nodes Info API 提供叢集節點的資訊，其中大多為靜態資訊，包含下列項目：

- 主機系統資訊 
- JVM 
- 處理器類型 
- 節點設定 
- 執行緒集區設定 
- 已安裝的外掛程式


## 端點

```json
GET /_nodes
GET /_nodes/{nodeId}
GET /_nodes/{metrics}
GET /_nodes/{nodeId}/{metrics}
# or full path equivalent
GET /_nodes/{nodeId}/info/{metrics}
```

## 路徑參數

下表列出可用的路徑參數。所有路徑參數皆為選用。

參數 | 類型 | 說明
:--- |:-------| :---
`node_id` | 字串 | 以逗號分隔的節點 ID 清單，用於篩選結果。支援[節點篩選器]({{site.url}}{{site.baseurl}}/api-reference/nodes-apis/index/#node-filters)。預設為 `_all`。
`metrics` | 字串 | 以逗號分隔的指標群組清單，這些群組將包含在回應中。例如，`jvm,thread_pool`。預設包含所有指標。

下表列出所有可用的指標群組。

指標 | 說明
:--- |:----
`settings` | 節點的設定。這些設定包含預設設定、[組態檔案]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/#configuration-file)中的自訂設定，以及動態[更新的設定]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/#updating-cluster-settings-using-the-api)。
`os` | 主機作業系統的靜態資訊，包括版本、處理器架構，以及可用與已配置的處理器。
`process` | 包含處理程序 ID。
`jvm` | 執行中 JVM 的詳細靜態資訊，包括引數。
`thread_pool` | 各個執行緒集區已設定的選項。
`transport` | 傳輸層的資訊，其中大多為靜態資訊。
`http` | HTTP 層的資訊，其中大多為靜態資訊。
`plugins` | 已安裝的外掛程式與模組的資訊。
`ingest` | 資料匯入管線與可用的匯入處理器的資訊。
`search_pipelines` | 節點上已設定的搜尋管線的資訊。
`aggregations` | 可用的[彙總]({{site.url}}{{site.baseurl}}/opensearch/aggregations/)資訊。
`indices` | 在節點層級設定的靜態索引設定。

## 查詢參數

您可以在請求中加入下列查詢參數。所有查詢參數皆為選用。

參數 | 類型 | 說明
:--- |:-------| :---
`flat_settings`| 布林值 | 指定是否以扁平格式傳回回應的 `settings` 物件。預設為 `false`。
`timeout` | 時間 | 設定節點回應的時間限制。預設值為 `30s`。

## 請求範例

下列查詢向叢集管理員節點請求 `process` 與 `transport` 指標： 

<!-- spec_insert_start
component: example_code
rest: GET /_nodes/cluster_manager:true/process,transport
-->
{% capture step1_rest %}
GET /_nodes/cluster_manager:true/process,transport
{% endcapture %}

{% capture step1_python %}


response = client.nodes.info(
  metric = "process,transport",
  node_id = "cluster_manager:true"
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

若要僅取得叢集管理員節點的執行緒集區資訊，請使用下列查詢：

<!-- spec_insert_start
component: example_code
rest: GET /_nodes/master:true/thread_pool
-->
{% capture step1_rest %}
GET /_nodes/master:true/thread_pool
{% endcapture %}

{% capture step1_python %}


response = client.nodes.info(
  metric = "thread_pool",
  node_id = "master:true"
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 回應範例

回應包含 `<metrics>` 請求參數中指定的指標群組（在此範例中為 `process` 與 `transport`）：

```json
{
  "_nodes": {
    "total": 1,
    "successful": 1,
    "failed": 0
  },
  "cluster_name": "opensearch",
  "nodes": {
    "VC0d4RgbTM6kLDwuud2XZQ": {
      "name": "node-m1-23",
      "transport_address": "127.0.0.1:9300",
      "host": "127.0.0.1",
      "ip": "127.0.0.1",
      "version": "1.3.1",
      "build_type": "tar",
      "build_hash": "c4c0672877bf0f787ca857c7c37b775967f93d81",
      "roles": [
        "data",
        "ingest",
        "master",
        "remote_cluster_client"
      ],
      "attributes": {
        "shard_indexing_pressure_enabled": "true"
      },
      "process" : {
        "refresh_interval_in_millis": 1000,
        "id": 44584,
        "mlockall": false
      },
      "transport": {
        "bound_address": [
          "[::1]:9300",
          "127.0.0.1:9300"
        ],
        "publish_address": "127.0.0.1:9300",
        "profiles": { }
      }
    }
  }
}
```

## 回應本文欄位

回應包含每個符合 `<nodeId>` 請求參數的節點的基本識別資訊與建置資訊。下表列出回應欄位。

欄位 | 說明
:--- |:----
name | 節點的名稱。
`transport_address` | 節點的傳輸位址。
`host` | 節點的主機位址。
`ip` | 節點的主機 IP 位址。
`version` | 節點的 OpenSearch 版本。
`build_type` | 節點的建置類型，例如 `rpm`、`docker` 或 `tar`。
`build_hash` | 此建置的 git 提交雜湊值。
`total_indexing_buffer` | 用於存放新編製索引的文件的最大堆積大小，以位元組為單位。一旦超過此堆積大小，文件就會寫入磁碟。
`roles` | 節點的角色清單。
`attributes` | 節點的屬性。
`os` | 作業系統的資訊，包括名稱、版本、架構、重新整理間隔，以及可用與已配置的處理器數量。
`process` | 目前執行中的處理程序資訊，包括 PID、重新整理間隔，以及 `mlockall`，此欄位指定處理程序的位址空間是否已成功鎖定在記憶體中。 
`jvm` | JVM 的資訊，包括 PID、版本、記憶體資訊、記憶體回收器資訊與引數。
`thread_pool` | 執行緒集區的資訊。
`transport` | 傳輸位址的資訊，包括繫結位址、發布位址與設定檔。
`http` | HTTP 位址的資訊，包括繫結位址、發布位址，以及以位元組為單位的最大內容長度。
`plugins` | 已安裝的外掛程式資訊，包括名稱、版本、OpenSearch 版本、Java 版本、說明、類別名稱、自訂資料夾名稱、擴充的外掛程式清單，以及 `has_native_controller`，此欄位指定外掛程式是否具有原生控制器處理程序。 
`modules` | 模組的資訊，包括名稱、版本、OpenSearch 版本、Java 版本、說明、類別名稱、自訂資料夾名稱、擴充的外掛程式清單，以及 `has_native_controller`，此欄位指定外掛程式是否具有原生控制器處理程序。模組與外掛程式的差異在於，模組會自動載入 OpenSearch，而外掛程式必須手動安裝。
`ingest` | 資料匯入管線與處理器的資訊。
`search_pipelines` | 節點上已設定的搜尋管線的資訊。
`aggregations` | 可用的彙總類型的資訊。


## 必要權限

若您使用 Security 外掛程式，請確認您具有適當的權限：`cluster:monitor/nodes/info`。
