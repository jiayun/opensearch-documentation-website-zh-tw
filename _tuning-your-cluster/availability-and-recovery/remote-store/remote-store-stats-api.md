---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Remote Store Stats API 
nav_order: 20
parent: Remote-backed storage
grand_parent: Availability and recovery
---

# Remote Store Stats API

於 2.8 版推出
{: .label .label-purple }

使用 Remote Store Stats API 監視分片層級的遠端儲存效能。

此 API 傳回的指標僅與儲存在以遠端儲存空間為後端的節點上的索引相關。若要在節點或叢集層級取得索引的彙總輸出，請使用 [Index Stats]({{site.url}}{{site.baseurl}}/api-reference/index-apis/stats/)、[Nodes Stats]({{site.url}}{{site.baseurl}}/api-reference/nodes-apis/nodes-stats/) 或 [Cluster Stats]({{site.url}}{{site.baseurl}}/api-reference/cluster-api/cluster-stats/) API。

## 端點

```json
GET _remotestore/stats/{index_name}
GET _remotestore/stats/{index_name}/{shard_id}
```

## 路徑參數

下表列出可用的路徑參數。所有路徑參數皆為選用。

參數 | 類型 | 說明
:--- | :--- | :---
`index_name` | 字串 | 索引名稱或索引模式。
`shard_id` | 字串 | 分片 ID。

## 索引的遠端儲存統計

使用下列 API 來取得所有索引分片的遠端儲存統計資料。

#### 範例請求

```json
GET _remotestore/stats/{index_name}
```
{% include copy-curl.html %}

#### 範例回應

<details open markdown="block">
<summary>
    回應
</summary>
{: .text-delta }

```json
{
    "_shards": {
        "total": 4,
        "successful": 4,
        "failed": 0
    },
    "indices": {
        "remote-index": {
            "shards": {
                "0": [{
                        "routing": {
                            "state": "STARTED",
                            "primary": true,
                            "node": "q1VxWZnCTICrfRc2bRW3nw"
                        },
                        "segment": {
                            "download": {},
                            "upload": {
                                "local_refresh_timestamp_in_millis": 1694171634102,
                                "remote_refresh_timestamp_in_millis": 1694171634102,
                                "refresh_time_lag_in_millis": 0,
                                "refresh_lag": 0,
                                "bytes_lag": 0,
                                "backpressure_rejection_count": 0,
                                "consecutive_failure_count": 0,
                                "total_uploads": {
                                    "started": 5,
                                    "succeeded": 5,
                                    "failed": 0
                                },
                                "total_upload_size": {
                                    "started_bytes": 15342,
                                    "succeeded_bytes": 15342,
                                    "failed_bytes": 0
                                },
                                "remote_refresh_size_in_bytes": {
                                    "last_successful": 0,
                                    "moving_avg": 3068.4
                                },
                                "upload_speed_in_bytes_per_sec": {
                                    "moving_avg": 99988.2
                                },
                                "remote_refresh_latency_in_millis": {
                                    "moving_avg": 44.0
                                }
                            }
                        },
                        "translog": {
                            "upload": {
                                "last_successful_upload_timestamp": 1694171633644,
                                "total_uploads": {
                                    "started": 6,
                                    "failed": 0,
                                    "succeeded": 6
                                },
                                "total_upload_size": {
                                    "started_bytes": 1932,
                                    "failed_bytes": 0,
                                    "succeeded_bytes": 1932
                                },
                                "total_upload_time_in_millis": 21478,
                                "upload_size_in_bytes": {
                                    "moving_avg": 322.0
                                },
                                "upload_speed_in_bytes_per_sec": {
                                    "moving_avg": 2073.8333333333335
                                },
                                "upload_time_in_millis": {
                                    "moving_avg": 3579.6666666666665
                                }
                            },
                            "download": {}
                        }
                    },
                    {
                        "routing": {
                            "state": "STARTED",
                            "primary": false,
                            "node": "EZuen5Y5Sv-eDCLwh9gv-Q"
                        },
                        "segment": {
                            "download": {
                                "last_sync_timestamp": 1694171634148,
                                "total_download_size": {
                                    "started_bytes": 15112,
                                    "succeeded_bytes": 15112,
                                    "failed_bytes": 0
                                },
                                "download_size_in_bytes": {
                                    "last_successful": 2910,
                                    "moving_avg": 1259.3333333333333
                                },
                                "download_speed_in_bytes_per_sec": {
                                    "moving_avg": 382387.3333333333
                                }
                            },
                            "upload": {}
                        },
                        "translog": {
                            "upload": {},
                            "download": {}
                        }
                    }
                ],
                "1": [{
                        "routing": {
                            "state": "STARTED",
                            "primary": false,
                            "node": "q1VxWZnCTICrfRc2bRW3nw"
                        },
                        "segment": {
                            "download": {
                                "last_sync_timestamp": 1694171633181,
                                "total_download_size": {
                                    "started_bytes": 18978,
                                    "succeeded_bytes": 18978,
                                    "failed_bytes": 0
                                },
                                "download_size_in_bytes": {
                                    "last_successful": 325,
                                    "moving_avg": 1265.2
                                },
                                "download_speed_in_bytes_per_sec": {
                                    "moving_avg": 456047.6666666667
                                }
                            },
                            "upload": {}
                        },
                        "translog": {
                            "upload": {},
                            "download": {}
                        }
                    },
                    {
                        "routing": {
                            "state": "STARTED",
                            "primary": true,
                            "node": "EZuen5Y5Sv-eDCLwh9gv-Q"
                        },
                        "segment": {
                            "download": {},
                            "upload": {
                                "local_refresh_timestamp_in_millis": 1694171633122,
                                "remote_refresh_timestamp_in_millis": 1694171633122,
                                "refresh_time_lag_in_millis": 0,
                                "refresh_lag": 0,
                                "bytes_lag": 0,
                                "backpressure_rejection_count": 0,
                                "consecutive_failure_count": 0,
                                "total_uploads": {
                                    "started": 6,
                                    "succeeded": 6,
                                    "failed": 0
                                },
                                "total_upload_size": {
                                    "started_bytes": 19208,
                                    "succeeded_bytes": 19208,
                                    "failed_bytes": 0
                                },
                                "remote_refresh_size_in_bytes": {
                                    "last_successful": 0,
                                    "moving_avg": 3201.3333333333335
                                },
                                "upload_speed_in_bytes_per_sec": {
                                    "moving_avg": 109612.0
                                },
                                "remote_refresh_latency_in_millis": {
                                    "moving_avg": 25.333333333333332
                                }
                            }
                        },
                        "translog": {
                            "upload": {
                                "last_successful_upload_timestamp": 1694171633106,
                                "total_uploads": {
                                    "started": 7,
                                    "failed": 0,
                                    "succeeded": 7
                                },
                                "total_upload_size": {
                                    "started_bytes": 2405,
                                    "failed_bytes": 0,
                                    "succeeded_bytes": 2405
                                },
                                "total_upload_time_in_millis": 27748,
                                "upload_size_in_bytes": {
                                    "moving_avg": 343.57142857142856
                                },
                                "upload_speed_in_bytes_per_sec": {
                                    "moving_avg": 1445.857142857143
                                },
                                "upload_time_in_millis": {
                                    "moving_avg": 3964.0
                                }
                            },
                            "download": {}
                        }
                    }
                ]
            }
        }
    }
}
```
</details>

### 回應本文欄位

Remote Store Stats API 的回應本文分為三個類別：

* `routing` ：包含與分片路由相關的資訊
* `segment` ：包含與從遠端後端儲存空間傳輸分段相關的統計資料
* `translog` ：包含與從遠端後端儲存空間傳輸 translog 相關的統計資料

<!-- vale off -->
#### routing
<!-- vale on -->

`routing` 物件包含下列欄位。

|欄位	|說明	|
|:---	|:---	|
| `primary` | 表示該分片複本是否為主要分片。 |
| `node` | 分片所指派節點的名稱。 |

<!-- vale off -->
#### segment
<!-- vale on -->

`segment.upload` 物件包含下列欄位。

|欄位	|說明	|
|:---	|:---	|
| `local_refresh_timestamp_in_millis` | 最後一次成功本機重新整理的時間戳記，以毫秒為單位。  |
| `remote_refresh_timestamp_in_millis` | 最後一次成功遠端重新整理的時間戳記，以毫秒為單位。 |
| `refresh_time_lag_in_millis` | 遠端重新整理落後本機重新整理的時間量，以毫秒為單位。 |
| `refresh_lag` | 遠端儲存空間落後本機儲存空間的重新整理次數。   |
| `bytes_lag` | 遠端與本機儲存空間之間的落差，以位元組為單位。  |
| `backpressure_rejection_count` | 因遠端儲存空間的背壓而發出的寫入拒絕總數。    |
| `consecutive_failure_count` | 自上次成功重新整理以來連續發生的遠端重新整理失敗次數。  |
| `total_remote_refresh` | 遠端重新整理的總次數。  |
| `total_uploads_in_bytes` | 上傳至遠端儲存空間的所有資料總位元組數。  |
| `remote_refresh_size_in_bytes.last_successful` | 最後一次成功重新整理期間所上傳的資料大小。  |
| `remote_refresh_size_in_bytes.moving_avg` | 最近 *N* 次重新整理所上傳資料的平均大小，以位元組為單位。*N* 定義於 `remote_store.moving_average_window_size` 設定中。如需更多資訊，請參閱[遠端分段背壓]({{site.url}}{{site.baseurl}}/tuning-your-cluster/availability-and-recovery/remote-store/remote-segment-backpressure/)。 |
| `upload_latency_in_bytes_per_sec.moving_avg` | 最近 *N* 次上傳的遠端分段上傳平均速度，以位元組每秒為單位。*N* 定義於 `remote_store.moving_average_window_size` 設定中。如需更多資訊，請參閱[遠端分段背壓]({{site.url}}{{site.baseurl}}/tuning-your-cluster/availability-and-recovery/remote-store/remote-segment-backpressure/)。    |
| `remote_refresh_latency_in_millis.moving_avg` | 最近 *N* 次遠端重新整理期間，單次遠端重新整理所花費的平均時間，以毫秒為單位。*N* 定義於 `remote_store.moving_average_window_size` 設定中。如需更多資訊，請參閱[遠端分段背壓]({{site.url}}{{site.baseurl}}/tuning-your-cluster/availability-and-recovery/remote-store/remote-segment-backpressure/)。    |

`segment.download` 物件包含下列欄位。

|欄位	|說明	|
|:---	|:---	|
| `last_sync_timestamp`| 自上次成功從遠端後端儲存空間下載分段檔案以來的時間戳記，以毫秒為單位。 |
| `total_download_size.started_bytes` | 正在從遠端後端儲存空間下載的分段檔案總位元組數。   |
| `total_download_size.succeeded_bytes` | 成功從遠端後端儲存空間下載的分段檔案總位元組數。 |
| `total_download_size.failed_bytes` | 從遠端後端儲存空間下載失敗的分段檔案總位元組數。 |
| `download_size_in_bytes.last_successful` | 最後一次成功從遠端後端儲存空間下載的分段檔案大小，以位元組為單位。 |
| `download_size_in_bytes.moving_avg`  | 最近 20 次下載所下載分段資料的平均大小，以位元組為單位。 |
| `download_speed_in_bytes_per_sec.moving_avg` | 最近 20 次下載的平均下載速度，以位元組每秒為單位。 |

#### translog

`translog.upload` 物件包含下列欄位。

|欄位	|說明	|
|:---	|:---	|
| `last_successful_upload_timestamp`| 自上次成功將 translog 檔案上傳至遠端後端儲存空間以來的時間戳記，以毫秒為單位。 |
| `total_uploads.started` | 嘗試將 translog 上傳同步至遠端後端儲存空間的總次數。 |
| `total_uploads.failed` | 將 translog 上傳同步至遠端後端儲存空間失敗的總次數。   |
| `total_uploads.succeeded` | 成功將 translog 上傳同步至遠端後端儲存空間的總次數。  |
| `total_upload_size.started_bytes` | 正在從遠端後端儲存空間下載的 translog 檔案總位元組數。 |
| `total_upload_size.succeeded_bytes` | 成功上傳至遠端後端儲存空間的 translog 檔案總位元組數。 |
|`total_upload_size.failed_bytes` | 上傳至遠端後端儲存空間失敗的 translog 檔案總位元組數。 |
| `total_upload_time_in_millis` | 將 translog 檔案上傳至遠端後端儲存空間所花費的總時間，以毫秒為單位。 |
| `upload_size_in_bytes.moving_avg` | 最近 *N* 次下載所上傳 translog 資料的平均大小，以位元組為單位。*N* 定義於 `remote_store.moving_average_window_size` 設定中。 |
| `upload_speed_in_bytes_per_sec.moving_avg` | 最近 *N* 次上傳的 translog 上傳平均速度，以位元組每秒為單位。*N* 定義於 `remote_store.moving_average_window_size` 設定中。    |
| `upload_time_in_millis.moving_avg` | 自最近 *N* 次上傳以來，單次 translog 上傳所花費的平均時間，以毫秒為單位。*N* 定義於 `remote_store.moving_average_window_size` 設定中。    |

`translog.download` 物件包含下列欄位。

|欄位	|說明	|
|:---	|:---	|
| `last_successful_download_timestamp` | 自上次成功將 translog 檔案上傳至遠端後端儲存空間以來的時間戳記，以毫秒為單位。 |
| `total_downloads.succeeded` | 成功從遠端後端儲存空間下載同步 translog 的總次數。 |
| `total_download_size.succeeded_bytes` | 成功從遠端後端儲存空間上傳的 translog 檔案總位元組數。  |
| `total_download_time_in_millis` | 從遠端後端儲存空間下載 translog 檔案所花費的總時間，以毫秒為單位。  |
| `download_size_in_bytes.moving_avg`  | 最近 *N* 次下載所下載 translog 資料的平均大小，以位元組為單位。*N* 定義於 `remote_store.moving_average_window_size` 設定中。    |
| `download_speed_in_bytes_per_sec.moving_avg` | 最近 *N* 次上傳的 translog 下載平均速度，以位元組每秒為單位。*N* 定義於 `remote_store.moving_average_window_size` 設定中。   |
| `download_time_in_millis.moving_avg` |  自最近 *N* 次上傳以來，單次 translog 下載所花費的平均時間，以毫秒為單位。*N* 定義於 `remote_store.moving_average_window_size` 設定中。  |

## 單一分片的遠端儲存空間統計資料

使用下列 API 取得單一分片的遠端儲存空間統計資料。

#### 請求範例

```json
GET _remotestore/stats/{index_name}/{shard_id}
```
{% include copy-curl.html %}

#### 回應範例

<details open markdown="block">
  <summary>
    回應
  </summary>
  {: .text-delta }

```json
{
    "_shards": {
        "total": 2,
        "successful": 2,
        "failed": 0
    },
    "indices": {
        "remote-index": {
            "shards": {
                "0": [
                    {
                        "routing": {
                            "state": "STARTED",
                            "primary": true,
                            "node": "q1VxWZnCTICrfRc2bRW3nw"
                        },
                        "segment": {
                            "download": {},
                            "upload": {
                                "local_refresh_timestamp_in_millis": 1694171634102,
                                "remote_refresh_timestamp_in_millis": 1694171634102,
                                "refresh_time_lag_in_millis": 0,
                                "refresh_lag": 0,
                                "bytes_lag": 0,
                                "backpressure_rejection_count": 0,
                                "consecutive_failure_count": 0,
                                "total_uploads": {
                                    "started": 5,
                                    "succeeded": 5,
                                    "failed": 0
                                },
                                "total_upload_size": {
                                    "started_bytes": 15342,
                                    "succeeded_bytes": 15342,
                                    "failed_bytes": 0
                                },
                                "remote_refresh_size_in_bytes": {
                                    "last_successful": 0,
                                    "moving_avg": 3068.4
                                },
                                "upload_speed_in_bytes_per_sec": {
                                    "moving_avg": 99988.2
                                },
                                "remote_refresh_latency_in_millis": {
                                    "moving_avg": 44.0
                                }
                            }
                        },
                        "translog": {
                            "upload": {
                                "last_successful_upload_timestamp": 1694171633644,
                                "total_uploads": {
                                    "started": 6,
                                    "failed": 0,
                                    "succeeded": 6
                                },
                                "total_upload_size": {
                                    "started_bytes": 1932,
                                    "failed_bytes": 0,
                                    "succeeded_bytes": 1932
                                },
                                "total_upload_time_in_millis": 21478,
                                "upload_size_in_bytes": {
                                    "moving_avg": 322.0
                                },
                                "upload_speed_in_bytes_per_sec": {
                                    "moving_avg": 2073.8333333333335
                                },
                                "upload_time_in_millis": {
                                    "moving_avg": 3579.6666666666665
                                }
                            },
                            "download": {}
                        }
                    },
                    {
                        "routing": {
                            "state": "STARTED",
                            "primary": false,
                            "node": "EZuen5Y5Sv-eDCLwh9gv-Q"
                        },
                        "segment": {
                            "download": {
                                "last_sync_timestamp": 1694171634148,
                                "total_download_size": {
                                    "started_bytes": 15112,
                                    "succeeded_bytes": 15112,
                                    "failed_bytes": 0
                                },
                                "download_size_in_bytes": {
                                    "last_successful": 2910,
                                    "moving_avg": 1259.3333333333333
                                },
                                "download_speed_in_bytes_per_sec": {
                                    "moving_avg": 382387.3333333333
                                }
                            },
                            "upload": {}
                        },
                        "translog": {
                            "upload": {},
                            "download": {}
                        }
                    }
                ]
            }
        }
    }
}
```
</details>

### 本機分片的遠端儲存統計資料

若您只想擷取處理 Remote Store Stats API 請求的節點上存在的分片，請將 `local` 查詢參數設為 `true`，如下列請求範例所示：


```json
GET _remotestore/stats/{index_name}?local=true
```
{% include copy-curl.html %}
