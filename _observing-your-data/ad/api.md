---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "異常偵測 API"
parent: Anomaly detection
nav_order: 1
redirect_from: 
  - /monitoring-plugins/ad/api/
---

# 異常偵測 API

使用這些異常偵測操作，以程式設計方式建立及管理偵測器。

---

#### 目錄
- TOC
{:toc}


---

## 建立異常偵測器
於 1.0 版推出
{: .label .label-purple }

建立異常偵測器。

此命令會建立名為 `test-detector` 的單一實體偵測器，其根據 `value` 欄位的總和來尋找異常，並將結果儲存在自訂的 `opensearch-ad-plugin-result-test` 索引中：

#### 範例請求

```json
POST _plugins/_anomaly_detection/detectors
{
  "name": "test-detector",
  "description": "Test detector",
  "time_field": "timestamp",
  "indices": [
    "server_log*"
  ],
  "feature_attributes": [
    {
      "feature_name": "test",
      "feature_enabled": true,
      "aggregation_query": {
        "test": {
          "sum": {
            "field": "value"
          }
        }
      }
    }
  ],
  "filter_query": {
    "bool": {
      "filter": [
        {
          "range": {
            "value": {
              "gt": 1
            }
          }
        }
      ],
      "adjust_pure_negative": true,
      "boost": 1
    }
  },
  "detection_interval": {
    "period": {
      "interval": 1,
      "unit": "Minutes"
    }
  },
  "window_delay": {
    "period": {
      "interval": 1,
      "unit": "Minutes"
    }
  },
  "result_index" : "opensearch-ad-plugin-result-test"
}
```

#### 範例回應

```json
{
  "_id": "VEHKTXwBwf_U8gjUXY2s",
  "_version": 1,
  "_seq_no": 5,
  "anomaly_detector": {
    "name": "test-detector",
    "description": "Test detector",
    "time_field": "timestamp",
    "indices": [
      "server_log*"
    ],
    "filter_query": {
      "bool": {
        "filter": [
          {
            "range": {
              "value": {
                "from": 1,
                "to": null,
                "include_lower": false,
                "include_upper": true,
                "boost": 1
              }
            }
          }
        ],
        "adjust_pure_negative": true,
        "boost": 1
      }
    },
    "detection_interval": {
      "period": {
        "interval": 1,
        "unit": "Minutes"
      }
    },
    "window_delay": {
      "period": {
        "interval": 1,
        "unit": "Minutes"
      }
    },
    "shingle_size": 8,
    "schema_version": 0,
    "feature_attributes": [
      {
        "feature_id": "U0HKTXwBwf_U8gjUXY2m",
        "feature_name": "test",
        "feature_enabled": true,
        "aggregation_query": {
          "test": {
            "sum": {
              "field": "value"
            }
          }
        }
      }
    ],
    "last_update_time": 1633392680364,
    "user": {
      "name": "admin",
      "backend_roles": [
        "admin"
      ],
      "roles": [
        "own_index",
        "all_access"
      ],
      "custom_attribute_names": [],
      "user_requested_tenant": "__user__"
    },
    "detector_type": "SINGLE_ENTITY"
  },
  "_primary_term": 1
}
```

若要藉由指定類別欄位來建立高基數偵測器：

#### 範例請求

```json
POST _plugins/_anomaly_detection/detectors
{
  "name": "test-hc-detector",
  "description": "Test detector",
  "time_field": "timestamp",
  "indices": [
    "server_log*"
  ],
  "feature_attributes": [
    {
      "feature_name": "test",
      "feature_enabled": true,
      "aggregation_query": {
        "test": {
          "sum": {
            "field": "value"
          }
        }
      }
    }
  ],
  "filter_query": {
    "bool": {
      "filter": [
        {
          "range": {
            "value": {
              "gt": 1
            }
          }
        }
      ],
      "adjust_pure_negative": true,
      "boost": 1
    }
  },
  "detection_interval": {
    "period": {
      "interval": 1,
      "unit": "Minutes"
    }
  },
  "window_delay": {
    "period": {
      "interval": 1,
      "unit": "Minutes"
    }
  },
  "category_field": [
    "ip"
  ]
}
```

#### 範例回應

```json
{
  "_id": "b0HRTXwBwf_U8gjUw43R",
  "_version": 1,
  "_seq_no": 6,
  "anomaly_detector": {
    "name": "test-hc-detector",
    "description": "Test detector",
    "time_field": "timestamp",
    "indices": [
      "server_log*"
    ],
    "filter_query": {
      "bool": {
        "filter": [
          {
            "range": {
              "value": {
                "from": 1,
                "to": null,
                "include_lower": false,
                "include_upper": true,
                "boost": 1
              }
            }
          }
        ],
        "adjust_pure_negative": true,
        "boost": 1
      }
    },
    "detection_interval": {
      "period": {
        "interval": 1,
        "unit": "Minutes"
      }
    },
    "window_delay": {
      "period": {
        "interval": 1,
        "unit": "Minutes"
      }
    },
    "shingle_size": 8,
    "schema_version": 0,
    "feature_attributes": [
      {
        "feature_id": "bkHRTXwBwf_U8gjUw43K",
        "feature_name": "test",
        "feature_enabled": true,
        "aggregation_query": {
          "test": {
            "sum": {
              "field": "value"
            }
          }
        }
      }
    ],
    "last_update_time": 1633393165265,
    "category_field": [
      "ip"
    ],
    "user": {
      "name": "admin",
      "backend_roles": [
        "admin"
      ],
      "roles": [
        "own_index",
        "all_access"
      ],
      "custom_attribute_names": [],
      "user_requested_tenant": "__user__"
    },
    "detector_type": "MULTI_ENTITY"
  },
  "_primary_term": 1
}
```

您最多可以指定兩個類別欄位：

```json
"category_field": [
  "ip"
]
```

```json
"category_field": [
  "ip", "error_type"
]
```

您可以指定下列選項。

選項 | 說明 | 類型 | 必要
:--- | :--- |:--- | :--- |
`name` |  偵測器的名稱。 | `string` | 是
`description` |  偵測器的說明。 | `string` | 否
`time_field` |  時間欄位的名稱。 | `string` | 是
`indices`  |  要做為資料來源使用的索引清單。 | `list` | 是
`feature_attributes` | 指定 `feature_name`、將 `enabled` 參數設為 `true`，並指定彙總查詢。 | `list` | 是
`filter_query` |  為您的特徵提供選用的篩選查詢。 | `object` | 否
`detection_interval` | 異常偵測器的時間間隔。 | `object` | 是
`window_delay` | 為資料收集新增額外的處理時間。 | `object` | 否
`category_field` | 使用維度將資料分類或切片。類似於 SQL 中的 `GROUP BY`。 | `list` | 否

---

## 驗證偵測器
於 1.2 版推出
{: .label .label-purple }

傳回偵測器組態是否有任何可能導致 OpenSearch 無法建立偵測器的問題。

您可以使用驗證偵測器 API 操作，在建立偵測器之前先找出偵測器組態中的問題。

請求本文由偵測器組態組成，並遵循與[建立偵測器 API]({{site.url}}{{site.baseurl}}/monitoring-plugins/ad/api#create-anomaly-detector) 的請求本文相同的格式。

您有下列驗證選項：

- 僅根據偵測器組態進行驗證，並找出任何會完全阻止建立偵測器的問題：

```
POST _plugins/_anomaly_detection/detectors/_validate
POST _plugins/_anomaly_detection/detectors/_validate/detector
```

- 根據來源資料進行驗證，以了解偵測器完成模型訓練的可能性。

```
POST _plugins/_anomaly_detection/detectors/_validate/model
```

此 API 操作的回應會傳回封鎖問題做為偵測器類型回應，或傳回指出某個欄位可修改以提升模型訓練成功完成可能性的回應。模型類型問題不需要修正，偵測器建立仍可成功，但若未處理這些問題，偵測器可能無法順利訓練。

#### 範例請求

```json
POST _plugins/_anomaly_detection/detectors/_validate
POST _plugins/_anomaly_detection/detectors/_validate/detector
{
  "name": "test-detector",
  "description": "Test detector",
  "time_field": "timestamp",
  "indices": [
    "server_log*"
  ],
  "feature_attributes": [
    {
      "feature_name": "test",
      "feature_enabled": true,
      "aggregation_query": {
        "test": {
          "sum": {
            "field": "value"
          }
        }
      }
    }
  ],
  "filter_query": {
    "bool": {
      "filter": [
        {
          "range": {
            "value": {
              "gt": 1
            }
          }
        }
      ],
      "adjust_pure_negative": true,
      "boost": 1
    }
  },
  "detection_interval": {
    "period": {
      "interval": 1,
      "unit": "Minutes"
    }
  },
  "window_delay": {
    "period": {
      "interval": 1,
      "unit": "Minutes"
    }
  }
}
```

如果 Validate Detector API 在偵測器組態中沒有發現任何問題，則會傳回空回應：

#### 範例回應

```json
{}
```

如果 Validate Detector API 發現組態問題，則會傳回一則說明該問題的訊息。在此範例中，特徵查詢對資料來源中不存在的欄位進行彙總：

#### 範例回應

```json
{
  "detector": {
    "feature_attributes": {
      "message": "Feature has invalid query returning empty aggregated data: average_total_rev",
      "sub_issues": {
        "average_total_rev": "Feature has invalid query returning empty aggregated data"
      }
    }
  }
}
```

下列請求會針對來源資料進行驗證，以確認模型訓練是否可能成功。在此範例中，資料以每 5 分鐘一次的頻率匯入，且偵測器間隔設定為 1 分鐘。

```json
POST _plugins/_anomaly_detection/detectors/_validate/model
{
  "name": "test-detector",
  "description": "Test detector",
  "time_field": "timestamp",
  "indices": [
    "server_log*"
  ],
  "feature_attributes": [
    {
      "feature_name": "test",
      "feature_enabled": true,
      "aggregation_query": {
        "test": {
          "sum": {
            "field": "value"
          }
        }
      }
    }
  ],
  "filter_query": {
    "bool": {
      "filter": [
        {
          "range": {
            "value": {
              "gt": 1
            }
          }
        }
      ],
      "adjust_pure_negative": true,
      "boost": 1
    }
  },
  "detection_interval": {
    "period": {
      "interval": 1,
      "unit": "Minutes"
    }
  },
  "window_delay": {
    "period": {
      "interval": 1,
      "unit": "Minutes"
    }
  }
}
```

如果 Validate Detector API 在您的組態中找出可改進之處，則會傳回包含建議的回應，協助您變更組態以改善模型訓練。

#### 範例回應

在此範例中，Validate Detector API 傳回的回應指出，將偵測器間隔長度變更為至少 4 分鐘，可以提高模型訓練成功的機率。

```json
{
  "model": {
    "detection_interval": {
      "message": "The selected detector interval might collect sparse data. Consider changing interval length to: 4",
      "suggested_value": {
        "period": {
          "interval": 4,
          "unit": "Minutes"
        }
      }
    }
  }
}
```

另一種回應可能指出您可以變更 `filter_query` (資料篩選)，因為目前篩選後的資料過於稀疏，導致模型無法正確訓練；這可能是因為索引也匯入了落在所選篩選範圍之外的資料。使用另一個 `filter_query` 可以讓您的資料更密集。

```json
{
  "model": {
    "filter_query": {
      "message": "Data is too sparse after data filter is applied. Consider changing the data filter"
    }
  }
}
```

---

## 取得偵測器
於 1.0 版推出
{: .label .label-purple }

根據 `detector_id` 傳回偵測器的所有資訊。

#### 範例請求

```json
GET _plugins/_anomaly_detection/detectors/{detectorId}
```

#### 範例回應

```json
{
  "_id": "VEHKTXwBwf_U8gjUXY2s",
  "_version": 1,
  "_primary_term": 1,
  "_seq_no": 5,
  "anomaly_detector": {
    "name": "test-detector",
    "description": "Test detector",
    "time_field": "timestamp",
    "indices": [
      "server_log*"
    ],
    "filter_query": {
      "bool": {
        "filter": [
          {
            "range": {
              "value": {
                "from": 1,
                "to": null,
                "include_lower": false,
                "include_upper": true,
                "boost": 1
              }
            }
          }
        ],
        "adjust_pure_negative": true,
        "boost": 1
      }
    },
    "detection_interval": {
      "period": {
        "interval": 1,
        "unit": "Minutes"
      }
    },
    "window_delay": {
      "period": {
        "interval": 1,
        "unit": "Minutes"
      }
    },
    "shingle_size": 8,
    "schema_version": 0,
    "feature_attributes": [
      {
        "feature_id": "U0HKTXwBwf_U8gjUXY2m",
        "feature_name": "test",
        "feature_enabled": true,
        "aggregation_query": {
          "test": {
            "sum": {
              "field": "value"
            }
          }
        }
      }
    ],
    "last_update_time": 1633392680364,
    "user": {
      "name": "admin",
      "backend_roles": [
        "admin"
      ],
      "roles": [
        "own_index",
        "all_access"
      ],
      "custom_attribute_names": [],
      "user_requested_tenant": "__user__"
    },
    "detector_type": "SINGLE_ENTITY"
  }
}
```

_作業（job）_ 是您排程定期執行的項目，因此僅適用於即時異常偵測，不適用於僅執行一次的歷史分析。

當您啟動即時偵測器時，Anomaly Detection 外掛程式會建立一個作業，若該作業已存在則會更新它。
當您啟動或重新啟動即時偵測器時，該外掛程式會建立一個新的即時任務（task），記錄執行階段資訊，例如偵測器組態快照、即時作業狀態（初始化中/執行中/已停止）、初始化進度等等。

單一偵測器只能有一個即時作業（作業 ID 與偵測器 ID 相同），但可以有多個即時任務，因為每次重新啟動即時作業都會建立新的即時任務。您可以使用 `plugins.anomaly_detection.max_old_ad_task_docs_per_detector` 設定來限制即時任務的數量。

歷史分析沒有相關聯的作業。當您為偵測器啟動或重新執行歷史分析時，Anomaly Detection 外掛程式會建立一個新的歷史批次任務，追蹤歷史分析的執行階段資訊，例如狀態、協調/工作節點、任務進度等等。您可以使用 `plugins.anomaly_detection.max_old_ad_task_docs_per_detector` 設定來限制歷史任務的數量。

使用 `job=true` 取得即時分析任務資訊。

#### 範例請求

```json
GET _plugins/_anomaly_detection/detectors/{detectorId}?job=true
```

#### 範例回應

```json
{
  "_id": "VEHKTXwBwf_U8gjUXY2s",
  "_version": 1,
  "_primary_term": 1,
  "_seq_no": 5,
  "anomaly_detector": {
    "name": "test-detector",
    "description": "Test detector",
    "time_field": "timestamp",
    "indices": [
      "server_log*"
    ],
    "filter_query": {
      "bool": {
        "filter": [
          {
            "range": {
              "value": {
                "from": 1,
                "to": null,
                "include_lower": false,
                "include_upper": true,
                "boost": 1
              }
            }
          }
        ],
        "adjust_pure_negative": true,
        "boost": 1
      }
    },
    "detection_interval": {
      "period": {
        "interval": 1,
        "unit": "Minutes"
      }
    },
    "window_delay": {
      "period": {
        "interval": 1,
        "unit": "Minutes"
      }
    },
    "shingle_size": 8,
    "schema_version": 0,
    "feature_attributes": [
      {
        "feature_id": "U0HKTXwBwf_U8gjUXY2m",
        "feature_name": "test",
        "feature_enabled": true,
        "aggregation_query": {
          "test": {
            "sum": {
              "field": "value"
            }
          }
        }
      }
    ],
    "last_update_time": 1633392680364,
    "user": {
      "name": "admin",
      "backend_roles": [
        "admin"
      ],
      "roles": [
        "own_index",
        "all_access"
      ],
      "custom_attribute_names": [],
      "user_requested_tenant": "__user__"
    },
    "detector_type": "SINGLE_ENTITY"
  },
  "anomaly_detector_job": {
    "name": "VEHKTXwBwf_U8gjUXY2s",
    "schedule": {
      "interval": {
        "start_time": 1633393656357,
        "period": 1,
        "unit": "Minutes"
      }
    },
    "window_delay": {
      "period": {
        "interval": 1,
        "unit": "Minutes"
      }
    },
    "enabled": true,
    "enabled_time": 1633393656357,
    "last_update_time": 1633393656357,
    "lock_duration_seconds": 60,
    "user": {
      "name": "admin",
      "backend_roles": [
        "admin"
      ],
      "roles": [
        "own_index",
        "all_access"
      ],
      "custom_attribute_names": [],
      "user_requested_tenant": "__user__"
    }
  }
}
```

使用 `task=true` 取得即時與歷史分析任務的資訊。

#### 範例請求

```json
GET _plugins/_anomaly_detection/detectors/{detectorId}?task=true
```

#### 範例回應

```json
{
  "_id": "VEHKTXwBwf_U8gjUXY2s",
  "_version": 1,
  "_primary_term": 1,
  "_seq_no": 5,
  "anomaly_detector": {
    "name": "test-detector",
    "description": "Test detector",
    "time_field": "timestamp",
    "indices": [
      "server_log*"
    ],
    "filter_query": {
      "bool": {
        "filter": [
          {
            "range": {
              "value": {
                "from": 1,
                "to": null,
                "include_lower": false,
                "include_upper": true,
                "boost": 1
              }
            }
          }
        ],
        "adjust_pure_negative": true,
        "boost": 1
      }
    },
    "detection_interval": {
      "period": {
        "interval": 1,
        "unit": "Minutes"
      }
    },
    "window_delay": {
      "period": {
        "interval": 1,
        "unit": "Minutes"
      }
    },
    "shingle_size": 8,
    "schema_version": 0,
    "feature_attributes": [
      {
        "feature_id": "U0HKTXwBwf_U8gjUXY2m",
        "feature_name": "test",
        "feature_enabled": true,
        "aggregation_query": {
          "test": {
            "sum": {
              "field": "value"
            }
          }
        }
      }
    ],
    "last_update_time": 1633392680364,
    "user": {
      "name": "admin",
      "backend_roles": [
        "admin"
      ],
      "roles": [
        "own_index",
        "all_access"
      ],
      "custom_attribute_names": [],
      "user_requested_tenant": "__user__"
    },
    "detector_type": "SINGLE_ENTITY"
  },
  "realtime_detection_task": {
    "task_id": "nkTZTXwBjd8s6RK4QlMq",
    "last_update_time": 1633393776375,
    "started_by": "admin",
    "error": "",
    "state": "RUNNING",
    "detector_id": "VEHKTXwBwf_U8gjUXY2s",
    "task_progress": 0,
    "init_progress": 1,
    "execution_start_time": 1633393656362,
    "is_latest": true,
    "task_type": "REALTIME_SINGLE_ENTITY",
    "coordinating_node": "SWD7ihu9TaaW1zKwFZNVNg",
    "detector": {
      "name": "test-detector",
      "description": "Test detector",
      "time_field": "timestamp",
      "indices": [
        "server_log*"
      ],
      "filter_query": {
        "bool": {
          "filter": [
            {
              "range": {
                "value": {
                  "from": 1,
                  "to": null,
                  "include_lower": false,
                  "include_upper": true,
                  "boost": 1
                }
              }
            }
          ],
          "adjust_pure_negative": true,
          "boost": 1
        }
      },
      "detection_interval": {
        "period": {
          "interval": 1,
          "unit": "Minutes"
        }
      },
      "window_delay": {
        "period": {
          "interval": 1,
          "unit": "Minutes"
        }
      },
      "shingle_size": 8,
      "schema_version": 0,
      "feature_attributes": [
        {
          "feature_id": "U0HKTXwBwf_U8gjUXY2m",
          "feature_name": "test",
          "feature_enabled": true,
          "aggregation_query": {
            "test": {
              "sum": {
                "field": "value"
              }
            }
          }
        }
      ],
      "last_update_time": 1633392680364,
      "user": {
        "name": "admin",
        "backend_roles": [
          "admin"
        ],
        "roles": [
          "own_index",
          "all_access"
        ],
        "custom_attribute_names": [],
        "user_requested_tenant": "__user__"
      },
      "detector_type": "SINGLE_ENTITY"
    },
    "estimated_minutes_left": 0,
    "user": {
      "name": "admin",
      "backend_roles": [
        "admin"
      ],
      "roles": [
        "own_index",
        "all_access"
      ],
      "custom_attribute_names": [],
      "user_requested_tenant": "__user__"
    }
  },
  "historical_analysis_task": {
    "task_id": "99DaTXwB6HknB84StRN1",
    "last_update_time": 1633393797040,
    "started_by": "admin",
    "state": "RUNNING",
    "detector_id": "VEHKTXwBwf_U8gjUXY2s",
    "task_progress": 0.89285713,
    "init_progress": 1,
    "current_piece": 1633328940000,
    "execution_start_time": 1633393751412,
    "is_latest": true,
    "task_type": "HISTORICAL_SINGLE_ENTITY",
    "coordinating_node": "SWD7ihu9TaaW1zKwFZNVNg",
    "worker_node": "2Z4q22BySEyzakYt_A0A2A",
    "detector": {
      "name": "test-detector",
      "description": "Test detector",
      "time_field": "timestamp",
      "indices": [
        "server_log*"
      ],
      "filter_query": {
        "bool": {
          "filter": [
            {
              "range": {
                "value": {
                  "from": 1,
                  "to": null,
                  "include_lower": false,
                  "include_upper": true,
                  "boost": 1
                }
              }
            }
          ],
          "adjust_pure_negative": true,
          "boost": 1
        }
      },
      "detection_interval": {
        "period": {
          "interval": 1,
          "unit": "Minutes"
        }
      },
      "window_delay": {
        "period": {
          "interval": 1,
          "unit": "Minutes"
        }
      },
      "shingle_size": 8,
      "schema_version": 0,
      "feature_attributes": [
        {
          "feature_id": "U0HKTXwBwf_U8gjUXY2m",
          "feature_name": "test",
          "feature_enabled": true,
          "aggregation_query": {
            "test": {
              "sum": {
                "field": "value"
              }
            }
          }
        }
      ],
      "last_update_time": 1633392680364,
      "user": {
        "name": "admin",
        "backend_roles": [
          "admin"
        ],
        "roles": [
          "own_index",
          "all_access"
        ],
        "custom_attribute_names": [],
        "user_requested_tenant": "__user__"
      },
      "detector_type": "SINGLE_ENTITY"
    },
    "detection_date_range": {
      "start_time": 1632788951329,
      "end_time": 1633393751329
    },
    "user": {
      "name": "admin",
      "backend_roles": [
        "admin"
      ],
      "roles": [
        "own_index",
        "all_access"
      ],
      "custom_attribute_names": [],
      "user_requested_tenant": "__user__"
    }
  }
}
```

---

## 更新偵測器
於 1.0 版推出
{: .label .label-purple }

更新偵測器的任何變更，包括描述或新增、移除特徵。
若要更新偵測器，您必須先停止即時偵測與歷史分析。

您無法更新類別欄位。
{: .note }

#### 範例請求

```json
PUT _plugins/_anomaly_detection/detectors/{detectorId}
{
  "name": "test-detector",
  "description": "Test update detector",
  "time_field": "timestamp",
  "indices": [
    "server_log*"
  ],
  "feature_attributes": [
    {
      "feature_name": "test",
      "feature_enabled": true,
      "aggregation_query": {
        "test": {
          "sum": {
            "field": "value"
          }
        }
      }
    }
  ],
  "filter_query": {
    "bool": {
      "filter": [
        {
          "range": {
            "value": {
              "gt": 1
            }
          }
        }
      ],
      "adjust_pure_negative": true,
      "boost": 1
    }
  },
  "detection_interval": {
    "period": {
      "interval": 1,
      "unit": "Minutes"
    }
  },
  "window_delay": {
    "period": {
      "interval": 1,
      "unit": "Minutes"
    }
  }
}
```


#### 範例回應

```json
{
  "_id": "VEHKTXwBwf_U8gjUXY2s",
  "_version": 2,
  "_seq_no": 7,
  "anomaly_detector": {
    "name": "test-detector",
    "description": "Test update detector",
    "time_field": "timestamp",
    "indices": [
      "server_log*"
    ],
    "filter_query": {
      "bool": {
        "filter": [
          {
            "range": {
              "value": {
                "from": 1,
                "to": null,
                "include_lower": false,
                "include_upper": true,
                "boost": 1
              }
            }
          }
        ],
        "adjust_pure_negative": true,
        "boost": 1
      }
    },
    "detection_interval": {
      "period": {
        "interval": 1,
        "unit": "Minutes"
      }
    },
    "window_delay": {
      "period": {
        "interval": 1,
        "unit": "Minutes"
      }
    },
    "shingle_size": 8,
    "schema_version": 0,
    "feature_attributes": [
      {
        "feature_id": "3kHiTXwBwf_U8gjUlY15",
        "feature_name": "test",
        "feature_enabled": true,
        "aggregation_query": {
          "test": {
            "sum": {
              "field": "value"
            }
          }
        }
      }
    ],
    "last_update_time": 1633394267522,
    "user": {
      "name": "admin",
      "backend_roles": [
        "admin"
      ],
      "roles": [
        "own_index",
        "all_access"
      ],
      "custom_attribute_names": [],
      "user_requested_tenant": "__user__"
    },
    "detector_type": "SINGLE_ENTITY"
  },
  "_primary_term": 1
}
```

---

## 刪除偵測器
於 1.0 版推出
{: .label .label-purple }

根據 `detector_id` 刪除偵測器。
若要刪除偵測器，您必須先停止即時偵測與歷史分析。

#### 範例請求

```json
DELETE _plugins/_anomaly_detection/detectors/{detectorId}
```

#### 範例回應

```json
{
  "_index": ".opensearch-anomaly-detectors",
  "_id": "70TxTXwBjd8s6RK4j1Pj",
  "_version": 2,
  "result": "deleted",
  "forced_refresh": true,
  "_shards": {
    "total": 2,
    "successful": 2,
    "failed": 0
  },
  "_seq_no": 9,
  "_primary_term": 1
}
```

---

## 預覽偵測器
於 1.0 版推出
{: .label .label-purple }

將日期範圍傳遞給異常偵測器，以傳回該日期範圍內的任何異常。

若要預覽單一實體偵測器：

#### 範例請求

```json
POST _plugins/_anomaly_detection/detectors/_preview
{
  "period_start": 1633048868000,
  "period_end": 1633394468000,
  "detector": {
    "name": "test-detector",
    "description": "Test update detector",
    "time_field": "timestamp",
    "indices": [
      "server_log*"
    ],
    "feature_attributes": [
      {
        "feature_name": "test",
        "feature_enabled": true,
        "aggregation_query": {
          "test": {
            "sum": {
              "field": "value"
            }
          }
        }
      }
    ],
    "filter_query": {
      "bool": {
        "filter": [
          {
            "range": {
              "value": {
                "gt": 1
              }
            }
          }
        ],
        "adjust_pure_negative": true,
        "boost": 1
      }
    },
    "detection_interval": {
      "period": {
        "interval": 1,
        "unit": "Minutes"
      }
    },
    "window_delay": {
      "period": {
        "interval": 1,
        "unit": "Minutes"
      }
    }
  }
}
```

#### 範例回應

```json
{
  "anomaly_result": [
    {
      "detector_id": null,
      "data_start_time": 1633049280000,
      "data_end_time": 1633049340000,
      "schema_version": 0,
      "feature_data": [
        {
          "feature_id": "8EHmTXwBwf_U8gjU0Y0u",
          "feature_name": "test",
          "data": 0
        }
      ],
      "anomaly_grade": 0,
      "confidence": 0
    },
    ...
  ],
  "anomaly_detector": {
    "name": "test-detector",
    "description": "Test update detector",
    "time_field": "timestamp",
    "indices": [
      "server_log*"
    ],
    "filter_query": {
      "bool": {
        "filter": [
          {
            "range": {
              "value": {
                "from": 1,
                "to": null,
                "include_lower": false,
                "include_upper": true,
                "boost": 1
              }
            }
          }
        ],
        "adjust_pure_negative": true,
        "boost": 1
      }
    },
    "detection_interval": {
      "period": {
        "interval": 1,
        "unit": "Minutes"
      }
    },
    "window_delay": {
      "period": {
        "interval": 1,
        "unit": "Minutes"
      }
    },
    "shingle_size": 8,
    "schema_version": 0,
    "feature_attributes": [
      {
        "feature_id": "8EHmTXwBwf_U8gjU0Y0u",
        "feature_name": "test",
        "feature_enabled": true,
        "aggregation_query": {
          "test": {
            "sum": {
              "field": "value"
            }
          }
        }
      }
    ],
    "detector_type": "SINGLE_ENTITY"
  }
}
```

如果您指定類別欄位，每個結果都會與某個實體相關聯：

#### 範例請求

```json
POST _plugins/_anomaly_detection/detectors/_preview
{
  "period_start": 1633048868000,
  "period_end": 1633394468000,
  "detector": {
    "name": "test-detector",
    "description": "Test update detector",
    "time_field": "timestamp",
    "indices": [
      "server_log*"
    ],
    "feature_attributes": [
      {
        "feature_name": "test",
        "feature_enabled": true,
        "aggregation_query": {
          "test": {
            "sum": {
              "field": "value"
            }
          }
        }
      }
    ],
    "filter_query": {
      "bool": {
        "filter": [
          {
            "range": {
              "value": {
                "gt": 1
              }
            }
          }
        ],
        "adjust_pure_negative": true,
        "boost": 1
      }
    },
    "detection_interval": {
      "period": {
        "interval": 1,
        "unit": "Minutes"
      }
    },
    "window_delay": {
      "period": {
        "interval": 1,
        "unit": "Minutes"
      }
    },
    "category_field": [
      "error_type"
    ]
  }
}
```

#### 範例回應

```json
{
  "anomaly_result": [
    {
      "detector_id": null,
      "data_start_time": 1633049280000,
      "data_end_time": 1633049340000,
      "schema_version": 0,
      "feature_data": [
        {
          "feature_id": "tkTpTXwBjd8s6RK4DlOZ",
          "feature_name": "test",
          "data": 0
        }
      ],
      "anomaly_grade": 0,
      "confidence": 0,
      "entity": [
        {
          "name": "error_type",
          "value": "error1"
        }
      ]
    },
    ...
  ],
  "anomaly_detector": {
    "name": "test-detector",
    "description": "Test update detector",
    "time_field": "timestamp",
    "indices": [
      "server_log*"
    ],
    "filter_query": {
      "bool": {
        "filter": [
          {
            "range": {
              "value": {
                "from": 1,
                "to": null,
                "include_lower": false,
                "include_upper": true,
                "boost": 1
              }
            }
          }
        ],
        "adjust_pure_negative": true,
        "boost": 1
      }
    },
    "detection_interval": {
      "period": {
        "interval": 1,
        "unit": "Minutes"
      }
    },
    "window_delay": {
      "period": {
        "interval": 1,
        "unit": "Minutes"
      }
    },
    "shingle_size": 8,
    "schema_version": 0,
    "feature_attributes": [
      {
        "feature_id": "tkTpTXwBjd8s6RK4DlOZ",
        "feature_name": "test",
        "feature_enabled": true,
        "aggregation_query": {
          "test": {
            "sum": {
              "field": "value"
            }
          }
        }
      }
    ],
    "category_field": [
      "error_type"
    ],
    "detector_type": "MULTI_ENTITY"
  }
}
```

您可以使用偵測器 ID 預覽偵測器：

```json
POST _plugins/_anomaly_detection/detectors/_preview
{
  "detector_id": "VEHKTXwBwf_U8gjUXY2s",
  "period_start": 1633048868000,
  "period_end": 1633394468000
}
```

或：

```json
POST _opendistro/_anomaly_detection/detectors/VEHKTXwBwf_U8gjUXY2s/_preview
{
  "period_start": 1633048868000,
  "period_end": 1633394468000
}
```

#### 範例回應

```json
{
  "anomaly_result": [
    {
      "detector_id": "VEHKTXwBwf_U8gjUXY2s",
      "data_start_time": 1633049280000,
      "data_end_time": 1633049340000,
      "schema_version": 0,
      "feature_data": [
        {
          "feature_id": "3kHiTXwBwf_U8gjUlY15",
          "feature_name": "test",
          "data": 0
        }
      ],
      "anomaly_grade": 0,
      "confidence": 0,
      "user": {
        "name": "admin",
        "backend_roles": [
          "admin"
        ],
        "roles": [
          "own_index",
          "all_access"
        ],
        "custom_attribute_names": [],
        "user_requested_tenant": "__user__"
      }
    },
    ...
  ],
  "anomaly_detector": {
    "name": "test-detector",
    "description": "Test update detector",
    "time_field": "timestamp",
    "indices": [
      "server_log*"
    ],
    "filter_query": {
      "bool": {
        "filter": [
          {
            "range": {
              "value": {
                "from": 1,
                "to": null,
                "include_lower": false,
                "include_upper": true,
                "boost": 1
              }
            }
          }
        ],
        "adjust_pure_negative": true,
        "boost": 1
      }
    },
    "detection_interval": {
      "period": {
        "interval": 1,
        "unit": "Minutes"
      }
    },
    "window_delay": {
      "period": {
        "interval": 1,
        "unit": "Minutes"
      }
    },
    "shingle_size": 8,
    "schema_version": 0,
    "feature_attributes": [
      {
        "feature_id": "3kHiTXwBwf_U8gjUlY15",
        "feature_name": "test",
        "feature_enabled": true,
        "aggregation_query": {
          "test": {
            "sum": {
              "field": "value"
            }
          }
        }
      }
    ],
    "last_update_time": 1633394267522,
    "user": {
      "name": "admin",
      "backend_roles": [
        "admin"
      ],
      "roles": [
        "own_index",
        "all_access"
      ],
      "custom_attribute_names": [],
      "user_requested_tenant": "__user__"
    },
    "detector_type": "SINGLE_ENTITY"
  }
}
```

---

## 啟動偵測器作業
於 1.0 版推出
{: .label .label-purple }

啟動即時或歷史異常偵測器作業。

若要啟動即時偵測器作業：

#### 範例請求

```json
POST _plugins/_anomaly_detection/detectors/{detectorId}/_start
```

#### 範例回應

```json
{
  "_id": "VEHKTXwBwf_U8gjUXY2s",
  "_version": 3,
  "_seq_no": 6,
  "_primary_term": 1
}
```

`_id` 代表即時工作 ID，與偵測器 ID 相同。

若要啟動歷史分析：

```json
POST _plugins/_anomaly_detection/detectors/{detectorId}/_start
{
  "start_time": 1633048868000,
  "end_time": 1633394468000
}
```

#### 範例回應

```json
{
  "_id": "f9DsTXwB6HknB84SoRTY",
  "_version": 1,
  "_seq_no": 958,
  "_primary_term": 1
}
```

`_id` 代表歷史批次工作 ID，其為隨機的通用唯一識別碼 (UUID)。

---

## 停止偵測器作業
於 1.0 版推出
{: .label .label-purple }

停止即時或歷史異常偵測器作業。

若要停止即時偵測器作業：

#### 範例請求

```json
POST _plugins/_anomaly_detection/detectors/{detectorId}/_stop
```

#### 範例回應

```json
{
  "_id": "VEHKTXwBwf_U8gjUXY2s",
  "_version": 0,
  "_seq_no": 0,
  "_primary_term": 0
}
```

若要停止歷史分析：

於 1.1 版推出
{: .label .label-purple }

```json
POST _plugins/_anomaly_detection/detectors/{detectorId}/_stop?historical=true
```

#### 範例回應

```json
{
  "_id": "f9DsTXwB6HknB84SoRTY",
  "_version": 0,
  "_seq_no": 0,
  "_primary_term": 0
}
```

---

## 搜尋偵測器
於 1.0 版推出
{: .label .label-purple }

傳回符合搜尋查詢的所有異常偵測器。

若要使用 `server_log*` 索引搜尋偵測器：

#### 範例請求

```json
GET _plugins/_anomaly_detection/detectors/_search
POST _plugins/_anomaly_detection/detectors/_search
{
  "query": {
    "wildcard": {
      "indices": {
        "value": "server_log*"
      }
    }
  }
}
```

#### 範例回應

```json
{
  "took": 2,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 4,
      "relation": "eq"
    },
    "max_score": 1,
    "hits": [
      {
        "_index": ".opensearch-anomaly-detectors",
        "_id": "Zi5zTXwBwf_U8gjUTfJG",
        "_version": 1,
        "_seq_no": 1,
        "_primary_term": 1,
        "_score": 1,
        "_source": {
          "name": "test",
          "description": "test",
          "time_field": "timestamp",
          "indices": [
            "server_log"
          ],
          "filter_query": {
            "match_all": {
              "boost": 1
            }
          },
          "detection_interval": {
            "period": {
              "interval": 5,
              "unit": "Minutes"
            }
          },
          "window_delay": {
            "period": {
              "interval": 1,
              "unit": "Minutes"
            }
          },
          "shingle_size": 8,
          "schema_version": 0,
          "feature_attributes": [
            {
              "feature_id": "ZS5zTXwBwf_U8gjUTfIn",
              "feature_name": "test_feature",
              "feature_enabled": true,
              "aggregation_query": {
                "test_feature": {
                  "sum": {
                    "field": "value"
                  }
                }
              }
            }
          ],
          "last_update_time": 1633386974533,
          "category_field": [
            "error_type"
          ],
          "user": {
            "name": "admin",
            "backend_roles": [
              "admin"
            ],
            "roles": [
              "own_index",
              "all_access"
            ],
            "custom_attribute_names": [],
            "user_requested_tenant": "__user__"
          },
          "detector_type": "MULTI_ENTITY"
        }
      },
      ...
    ]
  }
}
```

---

## 搜尋偵測器任務
於 1.1 版推出
{: .label .label-purple }

搜尋偵測器任務。

若要搜尋高基數偵測器最新的偵測器層級歷史分析任務

#### 範例請求

```json
GET _plugins/_anomaly_detection/detectors/tasks/_search
POST _plugins/_anomaly_detection/detectors/tasks/_search
{
  "query": {
    "bool": {
      "filter": [
        {
          "term": {
            "detector_id": "Zi5zTXwBwf_U8gjUTfJG"
          }
        },
        {
          "term": {
            "task_type": "HISTORICAL_HC_DETECTOR"
          }
        },
        {
          "term": {
            "is_latest": "true"
          }
        }
      ]
    }
  }
}
```

#### 範例回應

```json
{
  "took": 1,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 1,
      "relation": "eq"
    },
    "max_score": 0,
    "hits": [
      {
        "_index": ".opensearch-anomaly-detection-state",
        "_id": "fm-RTXwBYwCbWecgB753",
        "_version": 34,
        "_seq_no": 928,
        "_primary_term": 1,
        "_score": 0,
        "_source": {
          "detector_id": "Zi5zTXwBwf_U8gjUTfJG",
          "error": "",
          "detection_date_range": {
            "start_time": 1630794960000,
            "end_time": 1633386960000
          },
          "task_progress": 1,
          "last_update_time": 1633389090738,
          "execution_start_time": 1633388922742,
          "state": "FINISHED",
          "coordinating_node": "2Z4q22BySEyzakYt_A0A2A",
          "task_type": "HISTORICAL_HC_DETECTOR",
          "execution_end_time": 1633389090738,
          "started_by": "admin",
          "init_progress": 0,
          "is_latest": true,
          "detector": {
            "category_field": [
              "error_type"
            ],
            "description": "test",
            "ui_metadata": {
              "features": {
                "test_feature": {
                  "aggregationBy": "sum",
                  "aggregationOf": "value",
                  "featureType": "simple_aggs"
                }
              },
              "filters": []
            },
            "feature_attributes": [
              {
                "feature_id": "ZS5zTXwBwf_U8gjUTfIn",
                "feature_enabled": true,
                "feature_name": "test_feature",
                "aggregation_query": {
                  "test_feature": {
                    "sum": {
                      "field": "value"
                    }
                  }
                }
              }
            ],
            "schema_version": 0,
            "time_field": "timestamp",
            "last_update_time": 1633386974533,
            "indices": [
              "server_log"
            ],
            "window_delay": {
              "period": {
                "unit": "Minutes",
                "interval": 1
              }
            },
            "detection_interval": {
              "period": {
                "unit": "Minutes",
                "interval": 5
              }
            },
            "name": "testhc",
            "filter_query": {
              "match_all": {
                "boost": 1
              }
            },
            "shingle_size": 8,
            "user": {
              "backend_roles": [
                "admin"
              ],
              "custom_attribute_names": [],
              "roles": [
                "own_index",
                "all_access"
              ],
              "name": "admin",
              "user_requested_tenant": "__user__"
            },
            "detector_type": "MULTI_ENTITY"
          },
          "user": {
            "backend_roles": [
              "admin"
            ],
            "custom_attribute_names": [],
            "roles": [
              "own_index",
              "all_access"
            ],
            "name": "admin",
            "user_requested_tenant": "__user__"
          }
        }
      }
    ]
  }
}
```

若要搜尋高基數偵測器歷史分析的最新實體層級工作：

#### 請求範例

```json
GET _plugins/_anomaly_detection/detectors/tasks/_search
POST _plugins/_anomaly_detection/detectors/tasks/_search
{
  "query": {
    "bool": {
      "filter": [
        {
          "term": {
            "detector_id": "Zi5zTXwBwf_U8gjUTfJG"
          }
        },
        {
          "term": {
            "task_type": "HISTORICAL_HC_ENTITY"
          }
        },
        {
          "term": {
            "is_latest": "true"
          }
        }
      ]
    }
  },
  "sort": [
    {
      "execution_start_time": {
        "order": "desc"
      }
    }
  ],
  "size": 100
}
```

若要搜尋並彙總所有實體層級歷史任務的狀態：

`parent_task_id` 與您可以透過偵測器剖析 API 取得的任務 ID 相同：
`GET _plugins/_anomaly_detection/detectors/<detector_ID>/_profile/ad_task`。
{: .note }


#### 請求範例

```json
GET _plugins/_anomaly_detection/detectors/tasks/_search
POST _plugins/_anomaly_detection/detectors/tasks/_search
{
  "size": 0,
  "query": {
    "bool": {
      "filter": [
        {
          "term": {
            "detector_id": {
              "value": "Zi5zTXwBwf_U8gjUTfJG",
              "boost": 1
            }
          }
        },
        {
          "term": {
            "parent_task_id": {
              "value": "fm-RTXwBYwCbWecgB753",
              "boost": 1
            }
          }
        },
        {
          "terms": {
            "task_type": [
              "HISTORICAL_HC_ENTITY"
            ],
            "boost": 1
          }
        }
      ]
    }
  },
  "aggs": {
    "test": {
      "terms": {
        "field": "state",
        "size": 100
      }
    }
  }
}
```

#### 回應範例

```json
{
  "took": 2,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 32,
      "relation": "eq"
    },
    "max_score": null,
    "hits": []
  },
  "aggregations": {
    "test": {
      "doc_count_error_upper_bound": 0,
      "sum_other_doc_count": 0,
      "buckets": [
        {
          "key": "FINISHED",
          "doc_count": 32
        }
      ]
    }
  }
}
```

---

## 搜尋偵測器結果
於 1.0 版推出
{: .label .label-purple }

傳回搜尋查詢的所有結果。

您有下列搜尋選項：

- 若要只搜尋預設結果索引，只需使用搜尋 API：

  ```json
  POST _plugins/_anomaly_detection/detectors/results/_search/
  ```

- 若要同時搜尋自訂結果索引和預設結果索引，您可以將自訂結果索引加入搜尋 API：

  ```json
  POST _plugins/_anomaly_detection/detectors/results/_search/{custom_result_index}
  ```

  或者，加入自訂結果索引，並將 `only_query_custom_result_index` 參數設為 `false`：

  ```json
  POST _plugins/_anomaly_detection/detectors/results/_search/{custom_result_index}?only_query_custom_result_index=false
  ```

- 若要只搜尋自訂結果索引，請將自訂結果索引加入搜尋 API，並將 `only_query_custom_result_index` 參數設為 `true`：

  ```json
  POST _plugins/_anomaly_detection/detectors/results/_search/{custom_result_index}?only_query_custom_result_index=true
  ```

下列範例會搜尋即時分析中異常等級大於 0 的異常結果：

#### 請求範例

```json
GET _plugins/_anomaly_detection/detectors/results/_search/opensearch-ad-plugin-result-test
POST _plugins/_anomaly_detection/detectors/results/_search/opensearch-ad-plugin-result-test
{
  "query": {
    "bool": {
      "filter": [
        {
          "term": {
            "detector_id": "EWy02nwBm38sXcF2AiFJ"
          }
        },
        {
          "range": {
            "anomaly_grade": {
              "gt": 0
            }
          }
        }
      ],
      "must_not": [
        {
          "exists": {
            "field": "task_id"
          }
        }
      ]
    }
  }
}
```

如果您像此範例一樣指定自訂結果索引，搜尋結果 API 會同時搜尋預設結果索引和自訂結果索引。

如果您未指定自訂結果索引，而只使用 `_plugins/_anomaly_detection/detectors/results/_search` URL，Anomaly Detection 外掛程式就只會搜尋預設結果索引。

即時偵測不會將任務 ID 儲存於異常結果中，因此任務 ID 會是 null。

如需回應本文欄位的相關資訊，請參閱[異常結果對應]({{site.url}}{{site.baseurl}}/monitoring-plugins/ad/result-mapping/#response-body-fields)。

#### 回應範例

```json
{
  "took": 4,
  "timed_out": false,
  "_shards": {
    "total": 3,
    "successful": 3,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 90,
      "relation": "eq"
    },
    "max_score": 0,
    "hits": [
      {
        "_index": ".opensearch-anomaly-results-history-2021.10.04-1",
        "_id": "686KTXwB6HknB84SMr6G",
        "_version": 1,
        "_seq_no": 103622,
        "_primary_term": 1,
        "_score": 0,
        "_source": {
          "detector_id": "EWy02nwBm38sXcF2AiFJ",
          "confidence": 0.918886275269358,
          "model_id": "EWy02nwBm38sXcF2AiFJ_entity_error16",
          "schema_version": 4,
          "anomaly_score": 1.1093755891885446,
          "execution_start_time": 1633388475001,
          "data_end_time": 1633388414989,
          "data_start_time": 1633388114989,
          "feature_data": [
            {
              "feature_id": "ZS5zTXwBwf_U8gjUTfIn",
              "feature_name": "test_feature",
              "data": 0.532
            }
          ],
          "relevant_attribution": [
            {
              "feature_id": "ZS5zTXwBwf_U8gjUTfIn",
              "data": 1.0
            }
          ],
          "expected_values": [
            {
              "likelihood": 1,
              "value_list": [
                {
                  "feature_id": "ZS5zTXwBwf_U8gjUTfIn",
                  "data": 2
                }
              ]
            }
          ],
          "execution_end_time": 1633388475014,
          "user": {
            "backend_roles": [
              "admin"
            ],
            "custom_attribute_names": [],
            "roles": [
              "own_index",
              "all_access"
            ],
            "name": "admin",
            "user_requested_tenant": "__user__"
          },
          "anomaly_grade": 0.031023547546561225,
          "entity": [
            {
              "name": "error_type",
              "value": "error16"
            }
          ]
        }
      },
      ...
    ]
  }
}
```

您可以不限次數地執行歷史分析。因此，同一個偵測器可能有多個任務。

您可以先搜尋最新的歷史批次任務，再搜尋該歷史批次任務的結果。

若要使用 `task_id` 搜尋歷史分析中 `grade` 大於 0 的異常結果：

#### 請求範例

```json
GET _plugins/_anomaly_detection/detectors/results/_search
POST _plugins/_anomaly_detection/detectors/results/_search
{
  "query": {
    "bool": {
      "filter": [
        {
          "term": {
            "detector_id": "Zi5zTXwBwf_U8gjUTfJG"
          }
        },
        {
          "range": {
            "anomaly_grade": {
              "gt": 0
            }
          }
        },
        {
          "term": {
            "task_id": "fm-RTXwBYwCbWecgB753"
          }
        }
      ]
    }
  }
}
```

#### 回應範例

```json
{
  "took": 915,
  "timed_out": false,
  "_shards": {
    "total": 3,
    "successful": 3,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 4115,
      "relation": "eq"
    },
    "max_score": 0,
    "hits": [
      {
        "_index": ".opensearch-anomaly-results-history-2021.10.04-1",
        "_id": "VRyRTXwBDx7vzPBV8jYC",
        "_version": 1,
        "_seq_no": 149657,
        "_primary_term": 1,
        "_score": 0,
        "_source": {
          "detector_id": "Zi5zTXwBwf_U8gjUTfJG",
          "confidence": 0.9642989263957601,
          "task_id": "fm-RTXwBYwCbWecgB753",
          "model_id": "Zi5zTXwBwf_U8gjUTfJG_entity_error24",
          "schema_version": 4,
          "anomaly_score": 1.2260712437521946,
          "execution_start_time": 1633388982692,
          "data_end_time": 1631721300000,
          "data_start_time": 1631721000000,
          "feature_data": [
            {
              "feature_id": "ZS5zTXwBwf_U8gjUTfIn",
              "feature_name": "test_feature",
              "data": 10
            }
          ],
          "execution_end_time": 1633388982709,
          "user": {
            "backend_roles": [
              "admin"
            ],
            "custom_attribute_names": [],
            "roles": [
              "own_index",
              "all_access"
            ],
            "name": "admin",
            "user_requested_tenant": "__user__"
          },
          "anomaly_grade": 0.14249628345655782,
          "entity": [
            {
              "name": "error_type",
              "value": "error1"
            }
          ]
        }
      },
      ...
    ]
  }
}
```

---

## 搜尋前幾名異常
於 1.2 版推出
{: .label .label-purple }

針對高基數偵測器，依類別欄位值分桶，傳回前幾名的異常結果。

您可以傳遞 `historical` 布林值參數，指定要分析即時結果還是歷史結果。

#### 請求範例

```json
GET _plugins/_anomaly_detection/detectors/{detectorId}/results/_topAnomalies?historical=false
{
  "size": 3,
  "category_field": [
    "ip"
  ],
  "order": "severity",
  "task_id": "example-task-id",
  "start_time_ms": 123456789000,
  "end_time_ms": 987654321000
}
```

#### 範例回應

```json
{
  "buckets": [
    {
      "key": {
        "ip": "1.2.3.4"
      },
      "doc_count": 10,
      "max_anomaly_grade": 0.8
    },
    {
      "key": {
        "ip": "5.6.7.8"
      },
      "doc_count": 12,
      "max_anomaly_grade": 0.6
    },
    {
      "key": {
        "ip": "9.10.11.12"
      },
      "doc_count": 3,
      "max_anomaly_grade": 0.5
    }
  ]
}
```

您可以指定下列選項。

選項 | 說明 | 類型 | 必要
:--- | :--- |:--- |:--- |
`size` |  指定您想查看的前幾名桶數量。預設為 10，最大值為 10,000。 | `integer` | 否
`category_field` |  指定您要彙總的類別欄位集合。預設為偵測器的所有類別欄位。 | `list` | 否
`order` |  指定 `severity`（異常等級）或 `occurrence`（異常數量）。預設為 `severity`。 | `string` | 否
`task_id`  |  指定歷史任務 ID，僅查看該特定任務的結果。僅在 `historical=true` 時使用，否則 Anomaly Detection 外掛程式會忽略此參數。 | `string` | 否
`start_time_ms` | 指定開始分析結果的時間，以 Epoch 毫秒表示。 | `long` | 是
`end_time_ms` |  指定結束分析結果的時間，以 Epoch 毫秒表示。 | `long` | 是

---

## 取得偵測器統計資料
於 1.0 版推出
{: .label .label-purple }

提供外掛程式執行效能的相關資訊。

若要取得所有統計資料：

#### 請求範例

```json
GET _plugins/_anomaly_detection/stats
```

#### 回應範例

```json
{
  "anomaly_detectors_index_status": "green",
  "anomaly_detection_state_status": "green",
  "single_entity_detector_count": 2,
  "detector_count": 5,
  "multi_entity_detector_count": 3,
  "anomaly_detection_job_index_status": "green",
  "models_checkpoint_index_status": "green",
  "anomaly_results_index_status": "green",
  "nodes": {
    "2Z4q22BySEyzakYt_A0A2A": {
      "ad_execute_request_count": 95,
      "models": [
        {
          "detector_id": "WTBnTXwBjd8s6RK4b1Sz",
          "model_type": "rcf",
          "last_used_time": 1633398197185,
          "model_id": "WTBnTXwBjd8s6RK4b1Sz_model_rcf_0",
          "last_checkpoint_time": 1633396573679
        },
        ...
      ],
      "ad_canceled_batch_task_count": 0,
      "ad_hc_execute_request_count": 75,
      "ad_hc_execute_failure_count": 0,
      "model_count": 28,
      "ad_execute_failure_count": 1,
      "ad_batch_task_failure_count": 0,
      "ad_total_batch_task_execution_count": 27,
      "ad_executing_batch_task_count": 3
    },
    "SWD7ihu9TaaW1zKwFZNVNg": {
      "ad_execute_request_count": 12,
      "models": [
        {
          "detector_id": "Zi5zTXwBwf_U8gjUTfJG",
          "model_type": "entity",
          "last_used_time": 1633398375008,
          "model_id": "Zi5zTXwBwf_U8gjUTfJG_entity_error13",
          "last_checkpoint_time": 1633392973682,
          "entity": [
            {
              "name": "error_type",
              "value": "error13"
            }
          ]
        },
        ...
      ],
      "ad_canceled_batch_task_count": 1,
      "ad_hc_execute_request_count": 0,
      "ad_hc_execute_failure_count": 0,
      "model_count": 15,
      "ad_execute_failure_count": 2,
      "ad_batch_task_failure_count": 0,
      "ad_total_batch_task_execution_count": 27,
      "ad_executing_batch_task_count": 4
    },
    "TQDUXEzyTJyV0H6_T4hYUw": {
      "ad_execute_request_count": 0,
      "models": [
        {
          "detector_id": "Zi5zTXwBwf_U8gjUTfJG",
          "model_type": "entity",
          "last_used_time": 1633398375004,
          "model_id": "Zi5zTXwBwf_U8gjUTfJG_entity_error24",
          "last_checkpoint_time": 1633388177359,
          "entity": [
            {
              "name": "error_type",
              "value": "error24"
            }
          ]
        },
        ...
      ],
      "ad_canceled_batch_task_count": 0,
      "ad_hc_execute_request_count": 0,
      "ad_hc_execute_failure_count": 0,
      "model_count": 22,
      "ad_execute_failure_count": 0,
      "ad_batch_task_failure_count": 0,
      "ad_total_batch_task_execution_count": 28,
      "ad_executing_batch_task_count": 3
    }
  }
}
```

`model_count` 參數顯示每個節點記憶體中執行的模型總數。
若是歷史分析，您會看到下列欄位的值：

- `ad_total_batch_task_execution_count`
- `ad_executing_batch_task_count`
- `ad_canceled_batch_task_count`
- `ad_batch_task_failure_count`

如果您尚未執行任何歷史分析，這些值會顯示為 0。

若要取得特定節點的所有統計資料：

#### 請求範例

```json
GET _plugins/_anomaly_detection/{nodeId}/stats
```

若要取得節點的特定統計資料：

#### 請求範例

```json
GET _plugins/_anomaly_detection/{nodeId}/stats/{stat}
```

例如，若要取得節點 `SWD7ihu9TaaW1zKwFZNVNg` 的 `ad_execute_request_count` 值：

```json
GET _plugins/_anomaly_detection/SWD7ihu9TaaW1zKwFZNVNg/stats/ad_execute_request_count
```

#### 範例回應

```json
{
  "nodes": {
    "SWD7ihu9TaaW1zKwFZNVNg": {
      "ad_execute_request_count": 12
    }
  }
}
```

若要取得特定類型的統計資料：

#### 範例請求

```json
GET _plugins/_anomaly_detection/stats/{stat}
```

例如：

```json
GET _plugins/_anomaly_detection/stats/ad_executing_batch_task_count
```

#### 範例回應

```json
{
  "nodes": {
    "2Z4q22BySEyzakYt_A0A2A": {
      "ad_executing_batch_task_count": 3
    },
    "SWD7ihu9TaaW1zKwFZNVNg": {
      "ad_executing_batch_task_count": 3
    },
    "TQDUXEzyTJyV0H6_T4hYUw": {
      "ad_executing_batch_task_count": 4
    }
  }
}
```

---

## 剖析偵測器
於 1.0 版推出
{: .label .label-purple }

傳回與偵測器目前狀態及記憶體使用量相關的資訊，包括目前的錯誤與 shingle 大小，以協助對偵測器進行疑難排解。

此命令可藉由識別為每個偵測器執行異常偵測器作業的節點，協助您找出記錄檔的位置。

它也有助於追蹤初始化百分比、所需的 shingle 數量，以及預估的剩餘時間。

#### 範例請求

```json
GET _plugins/_anomaly_detection/detectors/{detectorId}/_profile/
GET _plugins/_anomaly_detection/detectors/{detectorId}/_profile?_all=true
GET _plugins/_anomaly_detection/detectors/{detectorId}/_profile/{type}
GET _plugins/_anomaly_detection/detectors/{detectorId}/_profile/{type1},{type2}
```

#### 範例回應

```json
GET _plugins/_anomaly_detection/detectors/{detectorId}/_profile

{
  "state": "DISABLED",
  "error": "Stopped detector: AD models memory usage exceeds our limit."
}

GET _plugins/_anomaly_detection/detectors/{detectorId}/_profile?_all=true&pretty

{
  "state": "RUNNING",
  "error": "",
  "models": [
    {
      "model_id": "3Dh6TXwBwf_U8gjURE0F_entity_KSLSh0Wv05RQXiBAQHTEZg",
      "entity": [
        {
          "name": "ip",
          "value": "192.168.1.1"
        },
        {
          "name": "error_type",
          "value": "error8"
        }
      ],
      "model_size_in_bytes": 403491,
      "node_id": "2Z4q22BySEyzakYt_A0A2A"
    },
    ...
  ],
  "total_size_in_bytes": 12911712,
  "init_progress": {
    "percentage": "100%"
  },
  "total_entities": 33,
  "active_entities": 32,
  "ad_task": {
    "ad_task": {
      "task_id": "D3I5TnwBYwCbWecg7lN9",
      "last_update_time": 1633399993685,
      "started_by": "admin",
      "state": "RUNNING",
      "detector_id": "3Dh6TXwBwf_U8gjURE0F",
      "task_progress": 0,
      "init_progress": 0,
      "execution_start_time": 1633399991933,
      "is_latest": true,
      "task_type": "HISTORICAL_HC_DETECTOR",
      "coordinating_node": "2Z4q22BySEyzakYt_A0A2A",
      "detector": {
        "name": "testhc-mc",
        "description": "test",
        "time_field": "timestamp",
        "indices": [
          "server_log"
        ],
        "filter_query": {
          "match_all": {
            "boost": 1
          }
        },
        "detection_interval": {
          "period": {
            "interval": 5,
            "unit": "Minutes"
          }
        },
        "window_delay": {
          "period": {
            "interval": 1,
            "unit": "Minutes"
          }
        },
        "shingle_size": 8,
        "schema_version": 0,
        "feature_attributes": [
          {
            "feature_id": "2zh6TXwBwf_U8gjUQ039",
            "feature_name": "test",
            "feature_enabled": true,
            "aggregation_query": {
              "test": {
                "sum": {
                  "field": "value"
                }
              }
            }
          }
        ],
        "ui_metadata": {
          "features": {
            "test": {
              "aggregationBy": "sum",
              "aggregationOf": "value",
              "featureType": "simple_aggs"
            }
          },
          "filters": []
        },
        "last_update_time": 1633387430916,
        "category_field": [
          "ip",
          "error_type"
        ],
        "user": {
          "name": "admin",
          "backend_roles": [
            "admin"
          ],
          "roles": [
            "own_index",
            "all_access"
          ],
          "custom_attribute_names": [],
          "user_requested_tenant": "__user__"
        },
        "detector_type": "MULTI_ENTITY"
      },
      "detection_date_range": {
        "start_time": 1632793800000,
        "end_time": 1633398600000
      },
      "user": {
        "name": "admin",
        "backend_roles": [
          "admin"
        ],
        "roles": [
          "own_index",
          "all_access"
        ],
        "custom_attribute_names": [],
        "user_requested_tenant": "__user__"
      }
    },
    "node_id": "2Z4q22BySEyzakYt_A0A2A",
    "task_id": "D3I5TnwBYwCbWecg7lN9",
    "task_type": "HISTORICAL_HC_DETECTOR",
    "detector_task_slots": 10,
    "total_entities_count": 32,
    "pending_entities_count": 22,
    "running_entities_count": 10,
    "running_entities": [      """[{"name":"ip","value":"192.168.1.1"},{"name":"error_type","value":"error9"}]""",
          ...],
    "entity_task_profiles": [
      {
        "shingle_size": 8,
        "rcf_total_updates": 1994,
        "threshold_model_trained": true,
        "threshold_model_training_data_size": 0,
        "model_size_in_bytes": 1593240,
        "node_id": "2Z4q22BySEyzakYt_A0A2A",
        "entity": [
          {
            "name": "ip",
            "value": "192.168.1.1"
          },
          {
            "name": "error_type",
            "value": "error7"
          }
        ],
        "task_id": "E3I5TnwBYwCbWecg9FMm",
        "task_type": "HISTORICAL_HC_ENTITY"
      },
      ...
    ]
  },
  "model_count": 32
}

GET _plugins/_anomaly_detection/detectors/{detectorId}/_profile/total_size_in_bytes

{
  "total_size_in_bytes": 13369344
}
```

您只能在歷史分析中看到 `ad_task` 欄位。

`model_count` 參數會顯示偵測器在每個節點記憶體上執行的模型總數。如果您在叢集上執行多個模型，並想知道數量，這項資訊會很有用。

如果您設定了類別欄位，則可以看到該欄位中唯一值的數量，以及所有在記憶體中執行模型的作用中實體。

您可以使用這些資料來估算異常偵測所需的記憶體量，以便決定如何調整叢集規模。例如，如果某個偵測器有一百萬個實體，而其中只有 10 個在記憶體中處於作用中狀態，您就需要垂直或水平擴展叢集。

針對單一實體偵測器：

#### 範例回應

```json
{
  "state": "INIT",
  "total_size_in_bytes": 0,
  "init_progress": {
    "percentage": "0%",
    "needed_shingles": 128
  },
  "ad_task": {
    "ad_task": {
      "task_id": "cfUNOXwBFLNqSEcxAlde",
      "last_update_time": 1633044731640,
      "started_by": "admin",
      "state": "RUNNING",
      "detector_id": "qL4NOXwB__6eNorTAKtJ",
      "task_progress": 0.49603173,
      "init_progress": 1,
      "current_piece": 1632739800000,
      "execution_start_time": 1633044726365,
      "is_latest": true,
      "task_type": "HISTORICAL_SINGLE_ENTITY",
      "coordinating_node": "bCtWtxWPThq0BIn5P5I4Xw",
      "worker_node": "dIyavWhmSYWGz65b4u-lpQ",
      "detector": {
        "name": "detector1",
        "description": "test",
        "time_field": "timestamp",
        "indices": [
          "server_log"
        ],
        "filter_query": {
          "match_all": {
            "boost": 1
          }
        },
        "detection_interval": {
          "period": {
            "interval": 5,
            "unit": "Minutes"
          }
        },
        "window_delay": {
          "period": {
            "interval": 1,
            "unit": "Minutes"
          }
        },
        "shingle_size": 8,
        "schema_version": 0,
        "feature_attributes": [
          {
            "feature_id": "p74NOXwB__6eNorTAKss",
            "feature_name": "test-feature",
            "feature_enabled": true,
            "aggregation_query": {
              "test_feature": {
                "sum": {
                  "field": "value"
                }
              }
            }
          }
        ],
        "ui_metadata": {
          "features": {
            "test-feature": {
              "aggregationBy": "sum",
              "aggregationOf": "value",
              "featureType": "simple_aggs"
            }
          },
          "filters": []
        },
        "last_update_time": 1633044725832,
        "user": {
          "name": "admin",
          "backend_roles": [
            "admin"
          ],
          "roles": [
            "own_index",
            "all_access"
          ],
          "custom_attribute_names": [],
          "user_requested_tenant": "__user__"
        },
        "detector_type": "SINGLE_ENTITY"
      },
      "detection_date_range": {
        "start_time": 1632439925885,
        "end_time": 1633044725885
      },
      "user": {
        "name": "admin",
        "backend_roles": [
          "admin"
        ],
        "roles": [
          "own_index",
          "all_access"
        ],
        "custom_attribute_names": [],
        "user_requested_tenant": "__user__"
      }
    },
    "shingle_size": 8,
    "rcf_total_updates": 1994,
    "threshold_model_trained": true,
    "threshold_model_training_data_size": 0,
    "model_size_in_bytes": 1593240,
    "node_id": "dIyavWhmSYWGz65b4u-lpQ",
    "detector_task_slots": 1
  }
}
```

`total_entities` 參數會顯示實體總數，包括偵測器的類別欄位數量。

對於具有多個類別欄位的偵測器，取得實體總數在即時分析中是一項耗費資源的操作。根據預設，在即時偵測設定檔中，偵測器最多會計數 10,000 個實體。在歷史分析方面，Anomaly Detection 外掛程式預設只會偵測前 1,000 個實體，並將排名前幾名的實體快取在記憶體中，因此取得歷史分析的實體總數並不會耗費太多資源。

`profile` 操作也會提供每個實體的相關資訊，例如實體的 `last_sample_timestamp` 和 `last_active_timestamp`。`last_sample_timestamp` 會顯示輸入資料來源索引中包含該實體的最後一份文件，而 `last_active_timestamp` 則會顯示該實體模型最後一次出現在模型快取中的時間戳記。

如果某個實體沒有異常結果，可能是該實體沒有任何樣本資料，或是記憶體和磁碟 I/O 等資源相對於實體數量而言受到限制。

#### 範例請求

```json
GET _plugins/_anomaly_detection/detectors/{detectorId}/_profile?_all=true
{
  "entity": [
    {
      "name": "host",
      "value": "i-00f28ec1eb8997686"
    }
  ]
}
```

#### 範例回應

```json
{
  "is_active": true,
  "last_active_timestamp": 1604026394879,
  "last_sample_timestamp": 1604026394879,
  "init_progress": {
    "percentage": "100%"
  },
  "model": {
    "model_id": "TFUdd3UBBwIAGQeRh5IS_entity_i-00f28ec1eb8997686",
    "model_size_in_bytes": 712480,
    "node_id": "MQ-bTBW3Q2uU_2zX3pyEQg"
  },
  "state": "RUNNING"
}
```

若只要取得歷史分析的設定檔資訊，請指定 `ad_task`。
對於多類別高基數偵測器，指定 `_all` 是一項成本高昂的操作。

#### 範例請求

```json
GET _plugins/_anomaly_detection/detectors/{detectorId}/_profile?_all
GET _plugins/_anomaly_detection/detectors/{detectorId}/_profile/ad_task
```

#### 範例回應

```json
{
  "ad_task": {
    "ad_task": {
      "task_id": "CHI0TnwBYwCbWecgqgRA",
      "last_update_time": 1633399648413,
      "started_by": "admin",
      "state": "RUNNING",
      "detector_id": "3Dh6TXwBwf_U8gjURE0F",
      "task_progress": 0,
      "init_progress": 0,
      "execution_start_time": 1633399646784,
      "is_latest": true,
      "task_type": "HISTORICAL_HC_DETECTOR",
      "coordinating_node": "2Z4q22BySEyzakYt_A0A2A",
      "detector": {
        "name": "testhc-mc",
        "description": "test",
        "time_field": "timestamp",
        "indices": [
          "server_log"
        ],
        "filter_query": {
          "match_all": {
            "boost": 1
          }
        },
        "detection_interval": {
          "period": {
            "interval": 5,
            "unit": "Minutes"
          }
        },
        "window_delay": {
          "period": {
            "interval": 1,
            "unit": "Minutes"
          }
        },
        "shingle_size": 8,
        "schema_version": 0,
        "feature_attributes": [
          {
            "feature_id": "2zh6TXwBwf_U8gjUQ039",
            "feature_name": "test",
            "feature_enabled": true,
            "aggregation_query": {
              "test": {
                "sum": {
                  "field": "value"
                }
              }
            }
          }
        ],
        "ui_metadata": {
          "features": {
            "test": {
              "aggregationBy": "sum",
              "aggregationOf": "value",
              "featureType": "simple_aggs"
            }
          },
          "filters": []
        },
        "last_update_time": 1633387430916,
        "category_field": [
          "ip",
          "error_type"
        ],
        "user": {
          "name": "admin",
          "backend_roles": [
            "admin"
          ],
          "roles": [
            "own_index",
            "all_access"
          ],
          "custom_attribute_names": [],
          "user_requested_tenant": "__user__"
        },
        "detector_type": "MULTI_ENTITY"
      },
      "detection_date_range": {
        "start_time": 1632793800000,
        "end_time": 1633398600000
      },
      "user": {
        "name": "admin",
        "backend_roles": [
          "admin"
        ],
        "roles": [
          "own_index",
          "all_access"
        ],
        "custom_attribute_names": [],
        "user_requested_tenant": "__user__"
      }
    },
    "node_id": "2Z4q22BySEyzakYt_A0A2A",
    "task_id": "CHI0TnwBYwCbWecgqgRA",
    "task_type": "HISTORICAL_HC_DETECTOR",
    "detector_task_slots": 10,
    "total_entities_count": 32,
    "pending_entities_count": 22,
    "running_entities_count": 10,
    "running_entities" : [
      """[{"name":"ip","value":"192.168.1.1"},{"name":"error_type","value":"error9"}]""",
      ...
    ],
    "entity_task_profiles": [
      {
        "shingle_size": 8,
        "rcf_total_updates": 994,
        "threshold_model_trained": true,
        "threshold_model_training_data_size": 0,
        "model_size_in_bytes": 1593240,
        "node_id": "2Z4q22BySEyzakYt_A0A2A",
        "entity": [
          {
            "name": "ip",
            "value": "192.168.1.1"
          },
          {
            "name": "error_type",
            "value": "error6"
          }
        ],
        "task_id": "9XI0TnwBYwCbWecgsAd6",
        "task_type": "HISTORICAL_HC_ENTITY"
      },
      ...
    ]
  }
}
```

---

## 刪除偵測器結果
於 1.1 版推出
{: .label .label-purple }

根據查詢刪除偵測器的結果。

刪除偵測器結果 API 只會刪除預設結果索引中的異常結果文件。不支援刪除儲存在任何自訂結果索引中的異常結果文件。

您需要手動刪除自訂結果索引中不需要的異常結果文件。

#### 範例請求

```json
DELETE _plugins/_anomaly_detection/detectors/results
{
  "query": {
    "bool": {
      "filter": [
        {
          "term": {
            "detector_id": {
              "value": "rlDtOHwBD5tpxlbyW7Nt"
            }
          }
        },
        {
          "term": {
            "task_id": {
              "value": "TM3tOHwBCi2h__AOXlyQ"
            }
          }
        },
        {
          "range": {
            "data_start_time": {
              "lte": 1632441600000
            }
          }
        }
      ]
    }
  }
}
```

#### 範例回應

```json
{
  "took": 48,
  "timed_out": false,
  "total": 28,
  "updated": 0,
  "created": 0,
  "deleted": 28,
  "batches": 1,
  "version_conflicts": 0,
  "noops": 0,
  "retries": {
    "bulk": 0,
    "search": 0
  },
  "throttled_millis": 0,
  "requests_per_second": -1,
  "throttled_until_millis": 0,
  "failures": []
}
```

---

## 建立監視器
於 1.0 版推出
{: .label .label-purple }

建立監視器以為偵測器設定警示。

#### 範例請求

```json
POST _plugins/_alerting/monitors
{
  "type": "monitor",
  "name": "test-monitor",
  "enabled": true,
  "schedule": {
    "period": {
      "interval": 20,
      "unit": "MINUTES"
    }
  },
  "inputs": [
    {
      "search": {
        "indices": [
          ".opensearch-anomaly-results*"
        ],
        "query": {
          "size": 1,
          "query": {
            "bool": {
              "filter": [
                {
                  "range": {
                    "data_end_time": {
                      "from": "{{period_end}}||-20m",
                      "to": "{{period_end}}",
                      "include_lower": true,
                      "include_upper": true,
                      "boost": 1
                    }
                  }
                },
                {
                  "term": {
                    "detector_id": {
                      "value": "m4ccEnIBTXsGi3mvMt9p",
                      "boost": 1
                    }
                  }
                }
              ],
              "adjust_pure_negative": true,
              "boost": 1
            }
          },
          "sort": [
            {
              "anomaly_grade": {
                "order": "desc"
              }
            },
            {
              "confidence": {
                "order": "desc"
              }
            }
          ],
          "aggregations": {
            "max_anomaly_grade": {
              "max": {
                "field": "anomaly_grade"
              }
            }
          }
        }
      }
    }
  ],
  "triggers": [
    {
      "name": "test-trigger",
      "severity": "1",
      "condition": {
        "script": {
          "source": "return ctx.results[0].aggregations.max_anomaly_grade.value != null && ctx.results[0].aggregations.max_anomaly_grade.value > 0.7 && ctx.results[0].hits.hits[0]._source.confidence > 0.7",
          "lang": "painless"
        }
      },
      "actions": [
        {
          "name": "test-action",
          "destination_id": "ld7912sBlQ5JUWWFThoW",
          "message_template": {
            "source": "This is my message body."
          },
          "throttle_enabled": false,
          "subject_template": {
            "source": "TheSubject"
          }
        }
      ]
    }
  ]
}
```

#### 範例回應

```json
{
  "_id": "OClTEnIBmSf7y6LP11Jz",
  "_version": 1,
  "_seq_no": 10,
  "_primary_term": 1,
  "monitor": {
    "type": "monitor",
    "schema_version": 1,
    "name": "test-monitor",
    "enabled": true,
    "enabled_time": 1589445384043,
    "schedule": {
      "period": {
        "interval": 20,
        "unit": "MINUTES"
      }
    },
    "inputs": [
      {
        "search": {
          "indices": [
            ".opensearch-anomaly-results*"
          ],
          "query": {
            "size": 1,
            "query": {
              "bool": {
                "filter": [
                  {
                    "range": {
                      "data_end_time": {
                        "from": "{{period_end}}||-20m",
                        "to": "{{period_end}}",
                        "include_lower": true,
                        "include_upper": true,
                        "boost": 1
                      }
                    }
                  },
                  {
                    "term": {
                      "detector_id": {
                        "value": "m4ccEnIBTXsGi3mvMt9p",
                        "boost": 1
                      }
                    }
                  }
                ],
                "adjust_pure_negative": true,
                "boost": 1
              }
            },
            "sort": [
              {
                "anomaly_grade": {
                  "order": "desc"
                }
              },
              {
                "confidence": {
                  "order": "desc"
                }
              }
            ],
            "aggregations": {
              "max_anomaly_grade": {
                "max": {
                  "field": "anomaly_grade"
                }
              }
            }
          }
        }
      }
    ],
    "triggers": [
      {
        "id": "NilTEnIBmSf7y6LP11Jr",
        "name": "test-trigger",
        "severity": "1",
        "condition": {
          "script": {
            "source": "return ctx.results[0].aggregations.max_anomaly_grade.value != null && ctx.results[0].aggregations.max_anomaly_grade.value > 0.7 && ctx.results[0].hits.hits[0]._source.confidence > 0.7",
            "lang": "painless"
          }
        },
        "actions": [
          {
            "id": "NylTEnIBmSf7y6LP11Jr",
            "name": "test-action",
            "destination_id": "ld7912sBlQ5JUWWFThoW",
            "message_template": {
              "source": "This is my message body.",
              "lang": "mustache"
            },
            "throttle_enabled": false,
            "subject_template": {
              "source": "TheSubject",
              "lang": "mustache"
            }
          }
        ]
      }
    ],
    "last_update_time": 1589445384043
  }
}
```

---
