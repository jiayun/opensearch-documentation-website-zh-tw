---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: CAT plugins
parent: CAT APIs
nav_order: 50
has_children: false
redirect_from:
- /opensearch/rest-api/cat/cat-plugins/
---

# CAT Plugins API
**於 1.0 版導入**
{: .label .label-purple }

CAT plugins 操作會列出已安裝外掛程式的名稱、元件與版本。

<!-- spec_insert_start
api: cat.plugins
component: endpoints
-->
## 端點
```json
GET /_cat/plugins
```
<!-- spec_insert_end -->


<!-- spec_insert_start
api: cat.plugins
component: query_parameters
columns: Parameter, Data type, Description, Default
include_deprecated: false
-->
## 查詢參數

下表列出可用的查詢參數。所有查詢參數皆為選用。

| 參數 | 資料類型 | 說明 | 預設 |
| :--- | :--- | :--- | :--- |
| `cluster_manager_timeout` | 字串 | 建立與叢集管理員節點連線所允許的時間。 | N/A |
| `format` | 字串 | `Accept` 標頭的簡短版本，例如 `json` 或 `yaml`。 | N/A |
| `h` | 清單 | 以逗號分隔、要顯示的欄位名稱清單。 | N/A |
| `help` | 布林值 | 傳回說明資訊。 | `false` |
| `local` | 布林值 | 傳回本機資訊，但不從叢集管理員節點擷取狀態。 | `false` |
| `s` | 清單 | 以逗號分隔、用於排序的欄位名稱或欄位別名清單。 | N/A |
| `v` | 布林值 | 啟用詳細模式，顯示欄位標題。 | `false` |

<!-- spec_insert_end -->

## 範例請求

下列範例請求會列出所有已安裝的外掛程式：

<!-- spec_insert_start
component: example_code
rest: GET /_cat/plugins?v
-->
{% capture step1_rest %}
GET /_cat/plugins?v
{% endcapture %}

{% capture step1_python %}


response = client.cat.plugins(
  params = { "v": "true" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 範例回應

```json
name             component                            version
opensearch-node1 analysis-icu                         3.3.2
opensearch-node1 opensearch-alerting                  3.3.2.0
opensearch-node1 opensearch-anomaly-detection         3.3.2.0
opensearch-node1 opensearch-asynchronous-search       3.3.2.0
opensearch-node1 opensearch-cross-cluster-replication 3.3.2.0
opensearch-node1 opensearch-custom-codecs             3.3.2.0
opensearch-node1 opensearch-flow-framework            3.3.2.0
opensearch-node1 opensearch-geospatial                3.3.2.0
opensearch-node1 opensearch-index-management          3.3.2.0
opensearch-node1 opensearch-job-scheduler             3.3.2.0
opensearch-node1 opensearch-knn                       3.3.2.0
opensearch-node1 opensearch-ml                        3.3.2.0
opensearch-node1 opensearch-neural-search             3.3.2.0
opensearch-node1 opensearch-notifications             3.3.2.0
opensearch-node1 opensearch-observability             3.3.2.0
opensearch-node1 opensearch-security                  3.3.2.0
opensearch-node1 opensearch-sql                       3.3.2.0
```

## 回應欄位

下表列出所有回應欄位。在 `h` 與 `s` 查詢參數中，可指定欄位名稱或其別名。若要從您的叢集傳回此清單，請傳送 `GET /_cat/plugins?help`。

欄位 | 別名 | 說明
:--- | :--- | :---
`id` | - | 節點的唯一識別碼。
`name` | `n` | 節點名稱。
`component` | `c` | 外掛程式元件名稱。
`version` | `v` | 外掛程式版本。
`description` | `d` | 外掛程式的說明與詳細資訊。

若要顯示特定欄位，請使用 `h` 查詢參數。下列範例請求只會傳回節點名稱、元件與版本欄位：

```json
GET /_cat/plugins?v&h=name,component,version
```
{% include copy-curl.html %}

回應只包含所請求的欄位：

```json
name             component                            version
opensearch-node1 opensearch-alerting                  3.8.0.0
opensearch-node1 opensearch-anomaly-detection         3.8.0.0
opensearch-node1 opensearch-asynchronous-search       3.8.0.0
...
```

下列範例請求使用欄位別名來傳回節點 ID、元件與外掛程式說明：

```json
GET /_cat/plugins?v&h=id,c,d
```
{% include copy-curl.html %}

回應包含所請求的欄位：

```json
id                     c                                    d
6It0uQ1AR06IDC4nMstPQw opensearch-alerting                  Amazon OpenSearch alerting plugin
6It0uQ1AR06IDC4nMstPQw opensearch-anomaly-detection         OpenSearch anomaly detector plugin
6It0uQ1AR06IDC4nMstPQw opensearch-asynchronous-search       Provides support for asynchronous search
...
```

## 必要權限

如果您使用 Security 外掛程式，請確認您具備適當的權限：`cluster:monitor/nodes/info`。
