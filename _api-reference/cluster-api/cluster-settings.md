---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "叢集設定"
nav_order: 50
parent: Cluster APIs
redirect_from:
  - /api-reference/cluster-settings/
  - /opensearch/rest-api/cluster-settings/
---

# Cluster Settings API
**於 1.0 版引入**
{: .label .label-purple }

Cluster Settings API 可擷取或修改適用於 OpenSearch 叢集中所有節點的叢集整體設定。透過此 API 更新的設定優先於 `opensearch.yml` 組態檔案中定義的設定。

使用 Cluster Settings API 可達成下列目的：

- 擷取目前的叢集組態，無需存取個別節點的組態檔案，即可瞭解叢集的設定方式。
- 動態調整叢集行為，無需重新啟動叢集，例如修改分片配置設定或復原速度。
- 管理叢集中所有節點都必須一致的設定，確保行為一致。
- 使用重新啟動叢集後不會保留的暫時性設定，暫時變更設定以進行測試或疑難排解。

建議使用此 API 管理叢集整體設定，因為它可確保所有節點的設定一致，並允許動態更新而無需重新啟動，比手動編輯組態檔案更合適。
{: .tip}

更新叢集設定時，您可以指定變更應為持續性（重新啟動叢集後仍保留）或暫時性（重新啟動後清除）。如需持續性與暫時性設定、設定優先順序及重設設定的詳細資訊，請參閱[設定 OpenSearch]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/index/)。

## 端點

```json
GET /_cluster/settings
PUT /_cluster/settings
```

## 查詢參數

下表列出可用的查詢參數。所有查詢參數皆為選用。

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `cluster_manager_timeout` | 字串 | 等待叢集管理員節點回應的時間。如需支援的時間單位的詳細資訊，請參閱[常用參數]({{site.url}}{{site.baseurl}}/api-reference/units/#time-units)。_（預設：`30s`）_ |
| `flat_settings` | 布林值 | 是否以扁平形式傳回設定，這可提升可讀性，尤其是巢狀層級較深的設定。例如，`"cluster": { "max_shards_per_node": 500 }` 的扁平形式為 `"cluster.max_shards_per_node": "500"`。_（預設：`false`）_ |
| `include_defaults` | 布林值 | **僅適用於 `GET`。** 當值為 `true` 時，傳回本機節點的預設叢集設定。_（預設：`false`）_ |
| `timeout` | 字串 | **僅適用於 `PUT`。** 時間長度。單位可以是 `nanos`、`micros`、`ms`（毫秒）、`s`（秒）、`m`（分鐘）、`h`（小時）及 `d`（天）。也接受不帶單位的 `0`，以及表示未指定值的 `-1`。_（預設：`30s`）_ |
| `master_timeout` <br> _已棄用_ | 字串 | _（自 2.0 版起棄用：為推廣包容性用語，請改用 `cluster_manager_timeout`。）_ 時間長度。單位可以是 `nanos`、`micros`、`ms`（毫秒）、`s`（秒）、`m`（分鐘）、`h`（小時）及 `d`（天）。也接受不帶單位的 `0`，以及表示未指定值的 `-1`。 |

## 請求本文欄位

`GET` 操作沒有請求本文。下表列出 `PUT` 操作的請求本文欄位。

欄位 | 資料類型 | 說明
:--- | :--- | :---
`persistent` | 物件 | 完整重新啟動叢集後仍保留的設定。這些設定會寫入叢集狀態，並持續保留，直到明確變更為止。
`transient` | 物件 | 僅適用至下一次完整重新啟動叢集的設定。適合在測試或疑難排解期間暫時變更組態。

在 `persistent` 或 `transient` 物件中，以索引鍵值配對指定您要更新的設定。例如：

```json
{
  "persistent": {
    "cluster.max_shards_per_node": 500
  }
}
```

並非所有叢集設定都能使用 Cluster Settings API 動態更新。嘗試透過 API 設定靜態設定時，您會收到錯誤訊息 `"setting [cluster.some.setting], not dynamically updateable"`。靜態設定必須在 `opensearch.yml` 檔案中設定，且需要重新啟動節點。
{: .note }

如需所有可用叢集設定的完整清單，請參閱[設定 OpenSearch]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/index/)。


## 範例：擷取目前的叢集設定

若要檢視目前的叢集設定且不包含預設值，請傳送 GET 請求：

<!-- spec_insert_start
component: example_code
rest: GET /_cluster/settings
-->
{% capture step1_rest %}
GET /_cluster/settings
{% endcapture %}

{% capture step1_python %}

response = client.cluster.get_settings()
{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

#### 回應範例

回應會顯示所有已明確設定的持續性與暫時性設定。空物件表示尚未設定該類型的任何設定：

```json
{
  "persistent": {
    "cluster": {
      "routing": {
        "allocation": {
          "load_awareness": {
            "flat_skew": "2"
          }
        }
      },
      "max_voting_config_exclusions": "10",
      "metadata": {
        "key": "10s"
      },
      "auto_shrink_voting_configuration": "true",
      "blocks": {
        "create_index": "false",
        "create_index.auto_release": "true"
      },
      "thread_pool": {
        "generic": {
          "max": "5"
        }
      },
      "max_shards_per_node": "500",
      "remote": {
        "my_remote_cluster": {
          "seeds": [
            "127.0.0.1:9300"
          ]
        },
        "opensearch-cluster": {
          "mode": "proxy"
        }
      },
      "no_cluster_manager_block": "write"
    },
    "indices": {
      "mapping": {
        "max_in_flight_updates": "10"
      }
    },
    "plugins": {
      "ml_commons": {
        "only_run_on_ml_node": "false",
        "mcp_server_enabled": "true",
        "native_memory_threshold": "99"
      }
    },
    "search_backpressure": {
      "mode": "monitor_only"
    },
    "action": {
      "auto_create_index": "true"
    },
    "wlm": {
      "workload_group": {
        "mode": "disabled",
        "duress_streak": "10"
      }
    },
    "admission_control": {
      "cluster": {
        "admin": {
          "cpu_usage": {
            "limit": "4"
          }
        }
      }
    },
    "script": {
      "context": {
        "field": {
          "max_compilations_rate": "75/5m",
          "cache_expire": "0ms",
          "cache_max_size": "100"
        },
        "search": {
          "max_compilations_rate": "75/5m",
          "cache_expire": "0ms",
          "cache_max_size": "100"
        },
        "ingest": {
          "max_compilations_rate": "75/5m",
          "cache_expire": "0ms",
          "cache_max_size": "100"
        }
      }
    }
  },
  "transient": {
    "cluster": {
      "max_shards_per_node": "1000"
    }
  }
}
```

## 範例：包含預設設定

若要擷取所有叢集設定（包括預設值），請使用 `include_defaults` 參數：

<!-- spec_insert_start
component: example_code
rest: GET /_cluster/settings?include_defaults=true
-->
{% capture step1_rest %}
GET /_cluster/settings?include_defaults=true
{% endcapture %}

{% capture step1_python %}


response = client.cluster.get_settings(
  params = { "include_defaults": "true" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

#### 範例回應

回應包含一個 `defaults` 物件，內含所有預設叢集設定（為精簡起見已截斷）。這在變更設定之前，可用於辨識設定名稱及其預設值：

```json
{
  "persistent" : { },
  "transient" : { },
  "defaults" : {
    "task_resource_tracking" : {
      "enabled" : "true"
    },
    "cluster" : {
      "metadata" : {
        "perf_analyzer" : {
          "collectors" : {
            "mode" : "0"
          },
          "state" : "0",
          "config" : {
            "overrides" : ""
          },
          "pa_node_stats_setting" : "1"
        }
      },
      "no_master_block" : "metadata_write",
      "persistent_tasks" : {
        "allocation" : {
          "enable" : "all",
          "recheck_interval" : "30s"
        }
      },
      "initial_cluster_manager_nodes" : [
        "opensearch-node1"
      ]
    }
  }
}
```

## 範例：使用扁平設定格式

若要以扁平格式傳回設定（可提升巢狀設定的可讀性），請使用 `flat_settings` 參數：

<!-- spec_insert_start
component: example_code
rest: GET /_cluster/settings?flat_settings=true
-->
{% capture step1_rest %}
GET /_cluster/settings?flat_settings=true
{% endcapture %}

{% capture step1_python %}


response = client.cluster.get_settings(
  params = { "flat_settings": "true" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

#### 範例回應

```json
{
  "persistent": {
    "action.auto_create_index": "true",
    "admission_control.cluster.admin.cpu_usage.limit": "4",
    "cluster.auto_shrink_voting_configuration": "true",
    "cluster.blocks.create_index": "false",
    "cluster.blocks.create_index.auto_release": "true",
    "cluster.max_shards_per_node": "500",
    "cluster.max_voting_config_exclusions": "10",
    "cluster.metadata.key": "10s",
    "cluster.no_cluster_manager_block": "write",
    "cluster.remote.my_remote_cluster.seeds": [
      "127.0.0.1:9300"
    ],
    "cluster.remote.opensearch-cluster.mode": "proxy",
    "cluster.routing.allocation.load_awareness.flat_skew": "2",
    "cluster.thread_pool.generic.max": "5",
    "indices.mapping.max_in_flight_updates": "10",
    "plugins.ml_commons.mcp_server_enabled": "true",
    "plugins.ml_commons.native_memory_threshold": "99",
    "plugins.ml_commons.only_run_on_ml_node": "false",
    "script.context.field.cache_expire": "0ms",
    "script.context.field.cache_max_size": "100",
    "script.context.field.max_compilations_rate": "75/5m",
    "script.context.ingest.cache_expire": "0ms",
    "script.context.ingest.cache_max_size": "100",
    "script.context.ingest.max_compilations_rate": "75/5m",
    "script.context.search.cache_expire": "0ms",
    "script.context.search.cache_max_size": "100",
    "script.context.search.max_compilations_rate": "75/5m",
    "search_backpressure.mode": "monitor_only",
    "wlm.workload_group.duress_streak": "10",
    "wlm.workload_group.mode": "disabled"
  },
  "transient": {
    "cluster.max_shards_per_node": "1000"
  }
}
```

## 範例：更新持續性設定

若要更新在叢集重新啟動後仍會保留的設定，請將其包含在 `persistent` 物件中：

<!-- spec_insert_start
component: example_code
rest: PUT /_cluster/settings
body: |
{
  "persistent": {
    "cluster.max_shards_per_node": 500
  }
}
-->
{% capture step1_rest %}
PUT /_cluster/settings
{
  "persistent": {
    "cluster.max_shards_per_node": 500
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.cluster.put_settings(
  body =   {
    "persistent": {
      "cluster.max_shards_per_node": 500
    }
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

#### 範例回應

`acknowledged` 欄位表示該設定已成功更新。回應會包含更新後的設定：

```json
{
  "acknowledged" : true,
  "persistent" : {
    "cluster" : {
      "max_shards_per_node" : "500"
    }
  },
  "transient" : { }
}
```

## 範例：更新暫時性設定

若要暫時更新設定（直到下一次完整叢集重新啟動為止），請將其包含在 `transient` 物件中：

<!-- spec_insert_start
component: example_code
rest: PUT /_cluster/settings
body: |
{
  "transient": {
    "indices.recovery.max_bytes_per_sec": "20mb"
  }
}
-->
{% capture step1_rest %}
PUT /_cluster/settings
{
  "transient": {
    "indices.recovery.max_bytes_per_sec": "20mb"
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.cluster.put_settings(
  body =   {
    "transient": {
      "indices.recovery.max_bytes_per_sec": "20mb"
    }
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

#### 範例回應

`acknowledged` 欄位表示該設定已成功更新。回應會包含更新後的設定：

```json
{
  "acknowledged" : true,
  "persistent" : { },
  "transient" : {
    "indices" : {
      "recovery" : {
        "max_bytes_per_sec" : "20mb"
      }
    }
  }
}
```

## 範例：重設設定

若要將設定重設為其預設值，請將其指派為 `null`：

<!-- spec_insert_start
component: example_code
rest: PUT /_cluster/settings
body: |
{
  "transient": {
    "indices.recovery.max_bytes_per_sec": null
  }
}
-->
{% capture step1_rest %}
PUT /_cluster/settings
{
  "transient": {
    "indices.recovery.max_bytes_per_sec": null
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.cluster.put_settings(
  body =   {
    "transient": {
      "indices.recovery.max_bytes_per_sec": null
    }
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 範例：使用萬用字元重設多個設定

若要一次重設多個相關設定，請使用萬用字元模式：

<!-- spec_insert_start
component: example_code
rest: PUT /_cluster/settings
body: |
{
  "persistent": {
    "indices.recovery.*": null
  }
}
-->
{% capture step1_rest %}
PUT /_cluster/settings
{
  "persistent": {
    "indices.recovery.*": null
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.cluster.put_settings(
  body =   {
    "persistent": {
      "indices.recovery.*": null
    }
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->


#### 範例回應

設定重設後，就不會再出現在回應中。該設定現在會使用優先順序中的下一個值：

```json
{
  "acknowledged" : true,
  "persistent" : { },
  "transient" : { }
}
```


## 回應欄位

下表列出回應欄位。

欄位 | 資料類型 | 說明
:--- | :--- | :---
`acknowledged` | 布林值 | 表示設定更新是否已成功套用至叢集。僅存在於 PUT 回應中。
`persistent` | 物件 | 包含所有已明確設定的持續性叢集設定。此物件中的設定在完整叢集重新啟動後仍會保留。
`transient` | 物件 | 包含所有已明確設定的暫時性叢集設定。此物件中的設定會在完整叢集重新啟動後被清除。
`defaults` | 物件 | 包含所有預設叢集設定及其預設值。僅當在 `GET` 請求中將 `include_defaults` 參數設為 `true` 時才會出現。

## 必要權限

如果您使用 Security 外掛程式，請確認您具有適當的權限：`cluster:admin/settings/update`。

## 相關文件

- 如需更多關於暫時性設定、持續性設定及設定優先順序的資訊，請參閱[設定 OpenSearch]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/)。
