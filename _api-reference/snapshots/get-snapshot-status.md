---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "取得快照狀態"
parent: Snapshot APIs
nav_order: 8
---

# Get Snapshot Status API
**Introduced 1.0**
{: .label .label-purple }

傳回快照建立期間及建立之後的快照狀態詳細資料。

若要了解快照建立，請參閱[建立快照]({{site.url}}{{site.baseurl}}/api-reference/snapshots/create-snapshot/)。

如果您使用 Security 外掛程式，您必須具備 `monitor_snapshot`、`create_snapshot` 或 `manage cluster` 權限。
{: .note}

## 端點

```json
GET _snapshot/{repository}/{snapshot}/_status
```

## 路徑參數

路徑參數為選用。

| 參數 | 資料類型 | 說明 |
:--- | :--- | :---
| `repository` | String | 包含快照的儲存庫。 |
| `snapshot` | List | 要傳回的快照。 |
| `index` | List | 要包含在回應中的索引。 |

三種請求變體提供了彈性：

* `GET _snapshot/_status` 會傳回所有儲存庫中目前執行中所有快照的狀態。

* `GET _snapshot/<repository>/_status` 會傳回指定儲存庫中目前執行中的所有快照。這是偏好的變體。

* `GET _snapshot/<repository>/<snapshot>/_status` 會傳回指定儲存庫中特定快照的詳細狀態資訊，無論其目前是否正在執行。

* `GET /_snapshot/<repository>/<snapshot>/<index>/_status` 只會傳回指定儲存庫中特定快照之指定索引的詳細狀態資訊。請注意，此端點僅適用於屬於特定快照的索引。

只有在所請求資源 (例如快照以及從快照建立的索引) 的分片總數小於下列叢集設定所指定的限制時，快照 API 呼叫才能運作：

- `snapshot.max_shards_allowed_in_status_api`(Dynamic, integer)：可包含在 Snapshot Status API 回應中的分片數上限。預設值為 `200000`。不適用於[淺層快照 v2]({{site.url}}{{site.baseurl}}/tuning-your-cluster/availability-and-recovery/remote-store/snapshot-interoperability##shallow-snapshot-v2)，其中檔案的總數與大小會傳回為 0。


在雲端查詢資料時，使用此 API 傳回目前未執行之快照的狀態，無論在機器資源或處理時間方面都可能非常耗費成本。對於每個快照，每個請求都會造成讀取該快照所有分片的檔案。
{: .warning}

## 請求本文欄位

| 欄位 | 資料類型 | 說明 |
:--- | :--- | :---
| `ignore_unavailable` | Boolean | 如何處理對無法使用之快照與索引的請求。若為 `false`，請求會對無法使用的快照與索引傳回錯誤。若為 `true`，請求會忽略無法使用的快照與索引，例如已損毀或暫時無法傳回的項目。預設為 `false`。|

## 範例請求

下列請求會傳回 `my-opensearch-repo` 儲存庫中 `my-first-snapshot` 的狀態。無法使用的快照會被忽略。

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


## 範例回應

下列範例對應於前述的[範例請求](#example-request)。

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

| 欄位 | 資料類型 | 說明 | 
:--- | :--- | :---
| `repository` | String | 包含快照的儲存庫名稱。 |
| `snapshot` | String | 快照名稱。 |
| `uuid` | String | 快照的通用唯一識別碼 (UUID)。 |
| `state` | String | 快照的目前狀態。請參閱[快照狀態](#snapshot-states)。  |
| `include_global_state` | Boolean | 目前的叢集狀態是否包含在快照中。 |
| `shards_stats` | Object | 快照的分片計數。請參閱[分片統計](#shard-stats)。 |
| `stats` | Object | 快照中包含的檔案相關資訊。`file_count`：檔案數量。`size_in_bytes`：所有檔案的總大小。請參閱[快照檔案統計](#snapshot-file-stats)。 |
| `index` | List of Objects | 包含快照中索引相關資訊的物件清單。請參閱[索引物件](#index-objects)。|

### 快照狀態

| 狀態 | 說明 | 
:--- | :--- |
| `FAILED` | 快照因錯誤而終止，未儲存任何資料。 |
| `IN_PROGRESS` | 快照目前正在執行。 |
| `PARTIAL` | 全域叢集狀態已儲存，但至少有一個分片的資料未儲存。[Create snapshot]({{site.url}}{{site.baseurl}}/api-reference/snapshots/create-snapshot/) 回應的 `failures` 屬性包含其他詳細資訊。 |
| `SUCCESS` | 快照已完成，且所有分片皆成功儲存。 |

### 分片統計

所有屬性值皆為整數。

| 屬性 | 說明 | 
:--- | :--- |
| `initializing` | 仍在初始化中的分片數量。 |
| `started` | 已啟動但尚未完成的分片數量。 |
| `finalizing` | 正在完成但尚未完成的分片數量。 |
| `done` | 已成功初始化、啟動並完成的分片數量。 |
| `failed` | 無法納入快照的分片數量。 |
| `total` | 快照中包含的分片總數。 |

### 快照檔案統計

| 屬性 | 類型 | 說明 | 
:--- | :--- | :--- |
| `incremental` | Object | 快照建立期間仍需複製的檔案數量與大小。對於已完成的快照，`incremental` 會提供原本不在儲存庫中、並作為增量快照一部分而複製的檔案數量與大小。 |
| `processed` | Object | 已上傳至快照的檔案數量與大小。檔案上傳後，已處理的 `file_count` 與 `size_in_bytes` 會在統計中遞增。 |
| `total` | Object | 快照所參照檔案的總數量與總大小。 | 
| `start_time_in_millis` | Long | 快照開始建立的時間 (毫秒)。 |
| `time_in_millis` | Long | 快照完成所需的總時間 (毫秒)。 |

### 索引物件

| 屬性 | 類型 | 說明 | 
:--- | :--- | :--- |
| `shards_stats` | Object | 請參閱[分片統計](#shard-stats)。 |
| `stats` | Object | 請參閱[快照檔案統計](#snapshot-file-stats)。 |
| `shards` | List of objects | 包含快照中分片的相關資訊。OpenSearch 會傳回下列與分片相關的屬性：<br /><br /> **stage**：快照中分片的目前狀態。分片狀態包括：<br /><br /> * DONE：快照中已成功儲存至儲存庫的分片數量。<br /><br /> * FAILURE：快照中未成功儲存至儲存庫的分片數量。<br /><br /> * FINALIZE：快照中正在進行儲存至儲存庫之完成階段的分片數量。<br /><br />* INIT：快照中正在進行儲存至儲存庫之初始化階段的分片數量。<br /><br />* STARTED：快照中正在進行儲存至儲存庫之啟動階段的分片數量。<br /><br /> **stats**：請參閱[快照檔案統計](#snapshot-file-stats)。<br /><br /> **total**：快照所參照檔案的總數量與總大小。<br /><br /> **start_time_in_millis**：快照開始建立的時間 (毫秒)。<br /><br /> **time_in_millis**：快照完成所需的總時間 (毫秒)。  |

## 必要權限

如果您使用 Security 外掛程式，請確保您具備適當的權限：`cluster:admin/snapshot/status` 與 `cluster:admin/snapshot/status*`。
