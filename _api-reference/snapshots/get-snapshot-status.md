---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "取得快照狀態"
parent: Snapshot APIs
nav_order: 80
---

# 取得快照狀態 API
**於 1.0 版推出**
{: .label .label-purple }

傳回快照在建立期間及建立之後的狀態詳細資訊。

若要了解如何建立快照，請參閱[建立快照]({{site.url}}{{site.baseurl}}/api-reference/snapshots/create-snapshot/)。

若您使用 Security 外掛程式，必須具備 `monitor_snapshot`、`create_snapshot` 或 `manage cluster` 權限。
{: .note}

## 端點

```json
GET _snapshot/{repository}/{snapshot}/_status
```

## 路徑參數

下表列出可用的路徑參數。所有路徑參數皆為選用。

| 參數 | 資料類型 | 說明 | 
:--- | :--- | :---
| `repository` | 字串 | 包含該快照的儲存庫。 |
| `snapshot` | 清單 | 要傳回的快照。 |
| `index` | 清單 | 要包含在回應中的索引。 |

三種請求變體提供了彈性：

* `GET _snapshot/_status` 傳回所有儲存庫中目前正在執行的所有快照狀態。

* `GET _snapshot/<repository>/_status` 傳回指定儲存庫中目前正在執行的所有快照。這是建議使用的變體。

* `GET _snapshot/<repository>/<snapshot>/_status` 傳回指定儲存庫中特定快照的詳細狀態資訊，無論該快照目前是否正在執行。 

* `GET /_snapshot/<repository>/<snapshot>/<index>/_status` 僅傳回指定儲存庫中特定快照內指定索引的詳細狀態資訊。請注意，此端點僅適用於屬於特定快照的索引。

只有在所請求資源（例如快照及從快照建立的索引）的分片總數小於下列叢集設定所指定的上限時，Snapshot API 呼叫才能正常運作：

- `snapshot.max_shards_allowed_in_status_api`（動態，整數）：Snapshot Status API 回應中可包含的分片數量上限。預設值為 `200000`。不適用於[淺層快照 v2]({{site.url}}{{site.baseurl}}/tuning-your-cluster/availability-and-recovery/remote-store/snapshot-interoperability##shallow-snapshot-v2)，此類快照傳回的檔案總數與大小皆為 0。 


在查詢雲端資料時，使用此 API 傳回目前未在執行之快照的狀態，可能會耗費大量機器資源與處理時間。對於每個快照，每個請求都會讀取該快照所有分片的檔案。 
{: .warning}

## 請求本文欄位

下表列出可用的請求本文欄位。所有請求本文欄位皆為選用。

| 欄位 | 資料類型 | 說明 | 
:--- | :--- | :---
| `ignore_unavailable` | 布林值 | 如何處理針對無法使用之快照與索引的請求。若為 `false`，請求會針對無法使用的快照與索引傳回錯誤。若為 `true`，請求會忽略無法使用的快照與索引，例如已損毀或暫時無法傳回的快照與索引。預設為 `false`。|

## 請求範例

下列請求會傳回 `my-opensearch-repo` 儲存庫中 `my-first-snapshot` 的狀態，並忽略無法使用的快照。

<!-- spec_insert_start
component: example_code
rest: GET /_snapshot/my-opensearch-repo/my-first-snapshot/_status
body: |
{
   "ignore_unavailable": true
}
-->
{% capture step1_rest %}
GET /_snapshot/my-opensearch-repo/my-first-snapshot/_status
{
  "ignore_unavailable": true
}
{% endcapture %}

{% capture step1_python %}


response = client.snapshot.status(
  repository = "my-opensearch-repo",
  snapshot = "my-first-snapshot"
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->


## 回應範例

下列範例對應前述的[請求範例](#example-request)。

`GET _snapshot/my-opensearch-repo/my-first-snapshot/_status` 請求會傳回下列欄位：

````json
{
  "snapshots" : [
    {
      "snapshot" : "my-first-snapshot",
      "repository" : "my-opensearch-repo",
      "uuid" : "dCK4Qth-TymRQ7Tu7Iga0g",
      "state" : "SUCCESS",
      "include_global_state" : true,
      "shards_stats" : {
        "initializing" : 0,
        "started" : 0,
        "finalizing" : 0,
        "done" : 7,
        "failed" : 0,
        "total" : 7
      },
      "stats" : {
        "incremental" : {
          "file_count" : 31,
          "size_in_bytes" : 24488927
        },
        "total" : {
          "file_count" : 31,
          "size_in_bytes" : 24488927
        },
        "start_time_in_millis" : 1660666841667,
        "time_in_millis" : 14054
      },
      "indices" : {
        ".opensearch-observability" : {
          "shards_stats" : {
            "initializing" : 0,
            "started" : 0,
            "finalizing" : 0,
            "done" : 1,
            "failed" : 0,
            "total" : 1
          },
          "stats" : {
            "incremental" : {
              "file_count" : 1,
              "size_in_bytes" : 208
            },
            "total" : {
              "file_count" : 1,
              "size_in_bytes" : 208
            },
            "start_time_in_millis" : 1660666841868,
            "time_in_millis" : 201
          },
          "shards" : {
            "0" : {
              "stage" : "DONE",
              "stats" : {
                "incremental" : {
                  "file_count" : 1,
                  "size_in_bytes" : 208
                },
                "total" : {
                  "file_count" : 1,
                  "size_in_bytes" : 208
                },
                "start_time_in_millis" : 1660666841868,
                "time_in_millis" : 201
              }
            }
          }
        },
        "shakespeare" : {
          "shards_stats" : {
            "initializing" : 0,
            "started" : 0,
            "finalizing" : 0,
            "done" : 1,
            "failed" : 0,
            "total" : 1
          },
          "stats" : {
            "incremental" : {
              "file_count" : 4,
              "size_in_bytes" : 18310117
            },
            "total" : {
              "file_count" : 4,
              "size_in_bytes" : 18310117
            },
            "start_time_in_millis" : 1660666842470,
            "time_in_millis" : 13050
          },
          "shards" : {
            "0" : {
              "stage" : "DONE",
              "stats" : {
                "incremental" : {
                  "file_count" : 4,
                  "size_in_bytes" : 18310117
                },
                "total" : {
                  "file_count" : 4,
                  "size_in_bytes" : 18310117
                },
                "start_time_in_millis" : 1660666842470,
                "time_in_millis" : 13050
              }
            }
          }
        },
        "opensearch_dashboards_sample_data_flights" : {
          "shards_stats" : {
            "initializing" : 0,
            "started" : 0,
            "finalizing" : 0,
            "done" : 1,
            "failed" : 0,
            "total" : 1
          },
          "stats" : {
            "incremental" : {
              "file_count" : 10,
              "size_in_bytes" : 6132245
            },
            "total" : {
              "file_count" : 10,
              "size_in_bytes" : 6132245
            },
            "start_time_in_millis" : 1660666843476,
            "time_in_millis" : 6221
          },
          "shards" : {
            "0" : {
              "stage" : "DONE",
              "stats" : {
                "incremental" : {
                  "file_count" : 10,
                  "size_in_bytes" : 6132245
                },
                "total" : {
                  "file_count" : 10,
                  "size_in_bytes" : 6132245
                },
                "start_time_in_millis" : 1660666843476,
                "time_in_millis" : 6221
              }
            }
          }
        },
        ".opendistro-reports-definitions" : {
          "shards_stats" : {
            "initializing" : 0,
            "started" : 0,
            "finalizing" : 0,
            "done" : 1,
            "failed" : 0,
            "total" : 1
          },
          "stats" : {
            "incremental" : {
              "file_count" : 1,
              "size_in_bytes" : 208
            },
            "total" : {
              "file_count" : 1,
              "size_in_bytes" : 208
            },
            "start_time_in_millis" : 1660666843076,
            "time_in_millis" : 200
          },
          "shards" : {
            "0" : {
              "stage" : "DONE",
              "stats" : {
                "incremental" : {
                  "file_count" : 1,
                  "size_in_bytes" : 208
                },
                "total" : {
                  "file_count" : 1,
                  "size_in_bytes" : 208
                },
                "start_time_in_millis" : 1660666843076,
                "time_in_millis" : 200
              }
            }
          }
        },
        ".opendistro-reports-instances" : {
          "shards_stats" : {
            "initializing" : 0,
            "started" : 0,
            "finalizing" : 0,
            "done" : 1,
            "failed" : 0,
            "total" : 1
          },
          "stats" : {
            "incremental" : {
              "file_count" : 1,
              "size_in_bytes" : 208
            },
            "total" : {
              "file_count" : 1,
              "size_in_bytes" : 208
            },
            "start_time_in_millis" : 1660666841667,
            "time_in_millis" : 201
          },
          "shards" : {
            "0" : {
              "stage" : "DONE",
              "stats" : {
                "incremental" : {
                  "file_count" : 1,
                  "size_in_bytes" : 208
                },
                "total" : {
                  "file_count" : 1,
                  "size_in_bytes" : 208
                },
                "start_time_in_millis" : 1660666841667,
                "time_in_millis" : 201
              }
            }
          }
        },
        ".kibana_1" : {
          "shards_stats" : {
            "initializing" : 0,
            "started" : 0,
            "finalizing" : 0,
            "done" : 1,
            "failed" : 0,
            "total" : 1
          },
          "stats" : {
            "incremental" : {
              "file_count" : 13,
              "size_in_bytes" : 45733
            },
            "total" : {
              "file_count" : 13,
              "size_in_bytes" : 45733
            },
            "start_time_in_millis" : 1660666842673,
            "time_in_millis" : 2007
          },
          "shards" : {
            "0" : {
              "stage" : "DONE",
              "stats" : {
                "incremental" : {
                  "file_count" : 13,
                  "size_in_bytes" : 45733
                },
                "total" : {
                  "file_count" : 13,
                  "size_in_bytes" : 45733
                },
                "start_time_in_millis" : 1660666842673,
                "time_in_millis" : 2007
              }
            }
          }
        },
        ".opensearch-notifications-config" : {
          "shards_stats" : {
            "initializing" : 0,
            "started" : 0,
            "finalizing" : 0,
            "done" : 1,
            "failed" : 0,
            "total" : 1
          },
          "stats" : {
            "incremental" : {
              "file_count" : 1,
              "size_in_bytes" : 208
            },
            "total" : {
              "file_count" : 1,
              "size_in_bytes" : 208
            },
            "start_time_in_millis" : 1660666842270,
            "time_in_millis" : 200
          },
          "shards" : {
            "0" : {
              "stage" : "DONE",
              "stats" : {
                "incremental" : {
                  "file_count" : 1,
                  "size_in_bytes" : 208
                },
                "total" : {
                  "file_count" : 1,
                  "size_in_bytes" : 208
                },
                "start_time_in_millis" : 1660666842270,
                "time_in_millis" : 200
              }
            }
          }
        }
      }
    }
  ]
}
````

## 回應本文欄位

下表列出所有回應本文欄位。

| 欄位 | 資料類型 | 說明 | 
:--- | :--- | :---
| `repository` | 字串 | 包含快照的儲存庫名稱。 |
| `snapshot` | 字串 | 快照名稱。 |
| `uuid` | 字串 | 快照的通用唯一識別碼（UUID）。 |
| `state` | 字串 | 快照的目前狀態。請參閱[快照狀態](#snapshot-states)。  |
| `include_global_state` | 布林值 | 目前叢集狀態是否包含在快照中。 |
| `shards_stats` | 物件 | 快照的分片計數。請參閱[分片統計資料](#shard-stats)。 |
| `stats` | 物件 | 快照中所包含檔案的相關資訊。`file_count`：檔案數目。`size_in_bytes`：所有檔案的總大小。請參閱[快照檔案統計資料](#snapshot-file-stats)。 |
| `index` | 物件清單 | 包含快照中索引相關資訊的物件清單。請參閱[索引物件](#index-objects)。|

### 快照狀態

下表列出快照狀態。

| 狀態 | 說明 | 
:--- | :--- |
| `FAILED` | 快照因錯誤而終止，且未儲存任何資料。 |
| `IN_PROGRESS` | 快照目前正在執行中。 |
| `PARTIAL` | 已儲存全域叢集狀態，但至少有一個分片的資料未儲存。[建立快照]({{site.url}}{{site.baseurl}}/api-reference/snapshots/create-snapshot/)回應的 `failures` 屬性包含其他詳細資料。 |
| `SUCCESS` | 快照已完成，且所有分片皆已成功儲存。 |

### 分片統計資料

下表列出分片統計資料屬性。所有屬性值皆為整數。

| 屬性 | 說明 | 
:--- | :--- |
| `initializing` | 仍在初始化中的分片數目。 |
| `started` | 已啟動但尚未完成最終處理的分片數目。 |
| `finalizing` | 正在進行最終處理但尚未完成的分片數目。 |
| `done` | 已成功初始化、啟動並完成最終處理的分片數目。 |
| `failed` | 未能納入快照的分片數目。 |
| `total` | 快照中包含的分片總數。 |

### 快照檔案統計資料

下表列出快照檔案統計資料屬性。

| 屬性 | 類型 | 說明 | 
:--- | :--- | :--- |
| `incremental` | 物件 | 建立快照期間仍需複製的檔案數目與大小。對於已完成的快照，`incremental` 會提供增量快照中尚未存在於儲存庫且已複製的檔案數目與大小。 |
| `processed` | 物件 | 已上傳至快照的檔案數目與大小。檔案上傳後，統計資料中的已處理 `file_count` 與 `size_in_bytes` 會遞增。 |
| `total` | 物件 | 快照所參照的檔案總數與總大小。 | 
| `start_time_in_millis` | 長整數 | 快照建立開始的時間（毫秒）。 |
| `time_in_millis` | 長整數 | 快照完成所花費的總時間（毫秒）。 |

### 索引物件

下表列出索引物件屬性。

| 屬性 | 類型 | 說明 | 
:--- | :--- | :--- |
| `shards_stats` | 物件 | 請參閱[分片統計資料](#shard-stats)。 |
| `stats` | 物件 | 請參閱[快照檔案統計資料](#snapshot-file-stats)。 |
| `shards` | 物件清單 | 包含快照中所含分片的相關資訊。OpenSearch 會傳回下列分片相關屬性：<br /><br /> **stage**：快照中分片的目前狀態。分片狀態包括：<br /><br /> * DONE：快照中已成功儲存至儲存庫的分片數目。<br /><br /> * FAILURE：快照中未成功儲存至儲存庫的分片數目。<br /><br /> * FINALIZE：快照中處於儲存至儲存庫最終處理階段的分片數目。<br /><br />* INIT：快照中處於儲存至儲存庫初始化階段的分片數目。<br /><br />* STARTED：快照中處於儲存至儲存庫已啟動階段的分片數目。<br /><br /> **stats**：請參閱[快照檔案統計資料](#snapshot-file-stats)。 <br /><br /> **total**：快照所參照的檔案總數與總大小。 <br /><br /> **start_time_in_millis**：快照建立開始的時間（毫秒）。 <br /><br /> **time_in_millis**：快照完成所花費的總時間（毫秒）。  |

## 必要權限

如果您使用 Security 外掛程式，請確認您具有適當的權限：`cluster:admin/snapshot/status` 與 `cluster:admin/snapshot/status*`。
