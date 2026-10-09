---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "預測 API"
parent: Forecasting
nav_order: 100
---

# 預測 API

使用這些操作以程式設計方式建立及管理預測器，讓預測器對您的時間序列資料產生預測。

---

## 目錄
- TOC
{:toc}

---

## 建立預測器

**於 3.1 版推出**
{: .label .label-purple }

建立預測器以產生時間序列預測。預測器可以是單一串流（不含類別欄位），也可以是高基數（含有一或多個類別欄位）。

建立預測器時，您需定義來源索引、預測間隔與預測範圍、要預測的特徵，以及選用參數，例如類別欄位和自訂結果索引。


### 端點

```
POST _plugins/_forecast/forecasters
```

### 請求本文欄位

此 API 支援下列請求本文欄位。

| 欄位                         | 資料類型           | 必要 | 說明                                                                                                                                  |
| :---------------------------- | :------------------ | :------- | :------------------------------------------------------------------------------------------------------------------------------------------- |
| `name`                        | 字串              | 必要 | 預測器名稱。                                                                                                                         |
| `description`                 | 字串              | 選用 | 預測器的自由格式說明。                                                                                                   |
| `time_field`                  | 字串              | 必要 | 來源文件的時間戳記欄位。                                                                                                |
| `indices`                     | 字串或字串陣列 | 必要 | 一或多個來源索引或索引別名。                                                                             |
| `feature_attributes`          | 物件陣列    | 必要 | 要預測的特徵。僅支援一個特徵。每個物件必須包含 `feature_name` 和一個 `aggregation_query`。                  |
| `forecast_interval`           | 物件              | 必要 | 產生預測的間隔。                                                                                             |
| `horizon`                     | 整數             | 選用 | 要預測的未來間隔數。                                                                                                  |
| `window_delay`                | 物件              | 選用 | 為因應匯入延遲而加入的延遲。                                                                                              |
| `category_field`              | 字串          | 選用 | 用於依實體分組預測的一或兩個欄位。                                                                                         |
| `result_index`                | 字串              | 選用 | 用於儲存預測結果的自訂索引別名。必須以 `opensearch-forecast-result-` 開頭。預設為 `opensearch-forecast-results`。 |
| `suggested_seasonality`       | 整數             | 選用 | 季節性模式的長度（以間隔為單位）。預期範圍：8–256。                                                                             |
| `recency_emphasis`            | 整數             | 選用 | 控制近期資料對預測的影響程度。預設為 `2560`。                                                                      |
| `history`                     | 整數             | 選用 | 用於模型訓練的過去間隔數。                                                                                        |
| `result_index_min_size`       | 整數             | 選用 | 觸發索引輪替所需的最小主要分片大小（以 MB 為單位）。                                                                                |
| `result_index_min_age`        | 整數             | 選用 | 觸發索引輪替所需的最小索引存留時間（以天為單位）。                                                                                             |
| `result_index_ttl`            | 整數             | 選用 | 已輪替索引被刪除前的最短時間（以天為單位）。                                                                                |
| `flatten_custom_result_index` | 布林值             | 選用 | 若為 `true`，則扁平化自訂結果索引中的巢狀欄位，以便更容易彙總。                                                         |
| `shingle_size`                | 整數             | 選用 | 用於影響預測的過去間隔數。預設為 `8`。建議範圍：4–128。                                      |


### 範例請求：單一串流預測器

下列範例為 `network-requests` 索引建立單一串流預測器。此預測器每 3 分鐘預測一次 `deny` 欄位的最大值，並使用先前的 300 個間隔進行訓練。`window_delay` 設定會將預測視窗延遲 3 分鐘，以因應匯入延遲：


```json
POST _plugins/_forecast/forecasters
{
    "name": "Second-Test-Forecaster-7",
    "description": "ok rate",
    "time_field": "@timestamp",
    "indices": [
        "network-requests"
    ],
    "feature_attributes": [
        {
            "feature_id": "deny_max",
            "feature_name": "deny max",
            "feature_enabled": true,
            "importance": 1,
            "aggregation_query": {
                "deny_max": {
                    "max": {
                        "field": "deny"
                    }
                }
            }
        }
    ],
    "window_delay": {
        "period": {
            "interval": 3,
            "unit": "MINUTES"
        }
    },
    "forecast_interval": {
        "period": {
            "interval": 3,
            "unit": "MINUTES"
        }
    },
    "schema_version": 2,
    "horizon": 3,
    "history": 300
}
```
{% include copy-curl.html %}

#### 範例回應 

```json
{
  "_id": "4WnXAYoBU2pVBal92lXD",
  "_version": 1,
  "forecaster": {
    "...": "Configuration (omitted)"
  }
}
```

### 範例請求：高基數預測器

下列範例建立高基數預測器，依 `host_nest.host2` 欄位將預測分組。與單一串流範例相同，它會使用歷史資料，以 3 分鐘的間隔預測 `deny` 欄位的最大值。此設定可跨不同主機進行依實體的預測：

```json
POST _plugins/_forecast/forecasters
{
    "name": "Second-Test-Forecaster-7",
    "description": "ok rate",
    "time_field": "@timestamp",
    "indices": [
        "network-requests"
    ],
    "feature_attributes": [
        {
            "feature_id": "deny_max",
            "feature_name": "deny max",
            "feature_enabled": true,
            "importance": 1,
            "aggregation_query": {
                "deny_max": {
                    "max": {
                        "field": "deny"
                    }
                }
            }
        }
    ],
    "window_delay": {
        "period": {
            "interval": 3,
            "unit": "MINUTES"
        }
    },
    "forecast_interval": {
        "period": {
            "interval": 3,
            "unit": "MINUTES"
        }
    },
    "schema_version": 2,
    "horizon": 3,
    "history": 300,
    "category_field": ["host_nest.host2"],
}
```
{% include copy-curl.html %}

#### 範例回應 

```json
{
  "_id": "4WnXAYoBU2pVBal92lXD",
  "_version": 1,
  "forecaster": {
    "...": "Configuration (omitted)"
  }
}
```


---


## 驗證預測器

**於 3.1 版導入**
{: .label .label-purple }

使用此 API 驗證預測器組態是否有效。您可以執行兩種類型的驗證：

- **僅組態驗證**：檢查組態在語法上是否正確，並參照現有的欄位。
- **訓練可行性驗證**：執行全面驗證，以確保預測器可以使用指定的組態進行訓練。


### 端點

下列端點可用於驗證預測器。

**僅組態驗證**：

```http
POST _plugins/_forecast/forecasters/_validate
```

**訓練可行性驗證**：

```http
POST _plugins/_forecast/forecasters/_validate/model
```

### 請求本文

請求本文與用於建立預測器的請求本文相同。它必須至少包含下列必要欄位：`name`、`time_field`、`indices`、`feature_attributes` 與 `forecast_interval`。

如果組態有效，回應會傳回空物件（`{}`）。如果組態無效，回應會包含詳細的錯誤訊息。


### 範例請求：缺少 `forecast_interval`

下列請求顯示省略 `forecast_interval` 的無效預測器組態：

```json
POST _plugins/_forecast/forecasters/_validate
{
  "name": "invalid-forecaster",
  "time_field": "@timestamp",
  "indices": ["network-requests"],
  "feature_attributes": [
    {
      "feature_id": "deny_max",
      "feature_name": "deny max",
      "feature_enabled": true,
      "aggregation_query": {
        "deny_max": {
          "max": {
            "field": "deny"
          }
        }
      }
    }
  ]
}
```
{% include copy-curl.html %}

### 範例回應

```json
{
  "forecaster": {
    "forecast_interval": {
      "message": "Forecast interval should be set"
    }
  }
}
```


---

## 建議組態

**於 3.1 版導入**
{: .label .label-purple }

根據資料的頻率與密度，為一或多個預測器參數（`forecast_interval`、`horizon`、`history`、`window_delay`）傳回適當的值。


### 端點

```
POST _plugins/_forecast/forecasters/_suggest/<comma‑separated-types>
```

`types` 必須是 `forecast_interval`、`horizon`、`history` 或 `window_delay` 中的一或多個。


### 範例請求：建議間隔

下列請求會分析來源資料，並根據平均事件頻率為預測器建議適當的 `forecast_interval` 值：

```
POST _plugins/_forecast/forecasters/_suggest/forecast_interval
{
  "name": "interval‑suggest",
  "time_field": "@timestamp",
  "indices": ["network-requests"],
  ...
}
```
{% include copy-curl.html %}

#### 範例回應

```json
{
  "interval": {
    "period": { "interval": 1, "unit": "Minutes" }
  }
}
```

---

## 取得預測器

**於 3.1 版導入**
{: .label .label-purple }

擷取預測器及其最近的工作（選用）。

### 端點

```
GET _plugins/_forecast/forecasters/{forecaster_id}[?task=(true|false)]
```

### 範例請求：包含工作

下列請求會傳回預測器的中繼資料，以及（若有指定）其相關工作的詳細資訊：

```json
GET _plugins/_forecast/forecasters/d7-r1YkB_Z-sgDOKo3Z5?task=true
```
{% include copy-curl.html %}

回應包含 `forecaster`、`realtime_task` 與 `run_once_task` 區段。

---

## 更新預測器

**於 3.1 版導入**
{: .label .label-purple }

更新現有預測器的組態。您必須先停止所有進行中的預測工作，才能進行更新。

任何影響模型的變更，例如修改 `category_field`、`result_index` 或 `feature_attributes`，都會使 OpenSearch Dashboards 中顯示的先前結果失效。

### 端點

```
PUT _plugins/_forecast/forecasters/{forecaster_id}
```


### 範例請求：更新名稱、結果索引與類別欄位

下列內容顯示預測器 `forecaster-i1nwqooBLXq6T-gGbXI-` 的定義：

```json
{
    "_index": ".opensearch-forecasters",
    "_id": "forecaster-i1nwqooBLXq6T-gGbXI-",
    "_version": 1,
    "_seq_no": 0,
    "_primary_term": 1,
    "_score": 1.0,
    "_source": {
        "category_field": [
            "service"
        ],
        "description": "ok rate",
        "feature_attributes": [{
            "feature_id": "deny_max",
            "feature_enabled": true,
            "feature_name": "deny max",
            "aggregation_query": {
                "deny_max": {
                    "max": {
                        "field": "deny"
                    }
                }
            }
        }],
        "forecast_interval": {
            "period": {
                "unit": "Minutes",
                "interval": 1
            }
        },
        "schema_version": 2,
        "time_field": "@timestamp",
        "last_update_time": 1695084997949,
        "horizon": 24,
        "indices": [
            "network-requests"
        ],
        "window_delay": {
            "period": {
                "unit": "Seconds",
                "interval": 20
            }
        },
        "transform_decay": 1.0E-4,
        "name": "Second-Test-Forecaster-3",
        "filter_query": {
            "match_all": {
                "boost": 1.0
            }
        },
        "shingle_size": 8,
        "result_index": "opensearch-forecast-result-a"
    }
}
```

下列請求會更新預測器的 `name`、`result_index` 與 `category_field` 屬性：

```json
PUT localhost:9200/_plugins/_forecast/forecasters/forecast-i1nwqooBLXq6T-gGbXI-
{
    "name": "Second-Test-Forecaster-1",
    "description": "ok rate",
    "time_field": "@timestamp",
    "indices": [
        "network-requests"
    ],
    "feature_attributes": [
        {
            "feature_id": "deny_max",
            "feature_name": "deny max",
            "feature_enabled": true,
            "importance": 1,
            "aggregation_query": {
                "deny_max": {
                    "max": {
                        "field": "deny"
                    }
                }
            }
        }
    ],
    "window_delay": {
        "period": {
            "interval": 20,
            "unit": "SECONDS"
        }
    },
    "forecast_interval": {
        "period": {
            "interval": 1,
            "unit": "MINUTES"
        }
    },
    "ui_metadata": {
        "aabb": {
            "ab": "bb"
        }
    },
    "schema_version": 2,
    "horizon": 24,
    "category_field": ["service", "host"]
}
```
{% include copy-curl.html %}

---


## 刪除預測器

**於 3.1 版導入**  
{: .label .label-purple }

刪除預測器組態。您必須先停止所有相關的即時或單次執行預測工作，才能刪除。如果工作仍在執行中，API 會傳回 `400` 錯誤。

### 端點

```http
DELETE _plugins/_forecast/forecasters/{forecaster_id}
```

### 範例請求：刪除預測器

下列請求會使用預測器的唯一 ID 刪除其組態：

```http
DELETE _plugins/_forecast/forecasters/forecast-i1nwqooBLXq6T-gGbXI-
```
{% include copy-curl.html %}

---

## 啟動預測器工作

**3.1 版推出**  
{: .label .label-purple }

開始為預測器進行即時預測。

### 端點

```http
POST _plugins/_forecast/forecasters/{forecaster_id}/_start
```

### 範例請求：啟動預測器工作

下列請求會為指定的預測器啟動即時預測：

```bash
POST _plugins/_forecast/forecasters/4WnXAYoBU2pVBal92lXD/_start
```
{% include copy-curl.html %}

#### 範例回應

```json
{ "_id": "4WnXAYoBU2pVBal92lXD" }
```

---

## 停止預測器工作

**3.1 版推出**  
{: .label .label-purple }

停止預測器的即時預測。

### 端點
```http
POST _plugins/_forecast/forecasters/{forecaster_id}/_stop
```

### 範例請求：停止預測器工作

下列請求會停止指定預測器的即時預測工作：

```bash
POST _plugins/_forecast/forecasters/4WnXAYoBU2pVBal92lXD/_stop
```
{% include copy-curl.html %}


---

## 執行單次分析

**3.1 版推出**
{: .label .label-purple }

執行回溯測試 (歷史) 預測。即時工作執行期間無法執行此作業。

### 端點
```http
POST _plugins/_forecast/forecasters/{forecaster_id}/_run_once
```

### 範例請求：執行回溯測試預測

下列請求會為指定的預測器啟動單次執行預測分析：

```bash
POST _plugins/_forecast/forecasters/{forecaster_id}/_run_once
```
{% include copy-curl.html %}

#### 範例回應

回應會傳回指派給單次執行工作的任務 ID：

```json
{ "taskId": "vXZG85UBAlM4LplcKI0f" }
```

### 範例請求：依任務 ID 搜尋預測結果

使用傳回的 `taskId` 查詢 `opensearch-forecast-results*` 索引，以取得歷史預測輸出：

```json
GET opensearch-forecast-results*/_search?pretty
{
  "sort": {
    "data_end_time": "desc"
  },
  "size": 10,
  "query": {
    "bool": {
      "filter": [
        { "term": { "task_id": "vXZG85UBAlM4LplcKI0f" } },
        {
          "range": {
            "data_end_time": {
              "format": "epoch_millis",
              "gte": 1742585746033
            }
          }
        }
      ]
    }
  },
  "track_total_hits": true
}
```
{% include copy-curl.html %}

此查詢會傳回符合指定任務 ID 的 10 筆最新預測結果。


---

## 搜尋預測器

**3.1 版推出**  
{: .label .label-purple }

在 `.opensearch-forecasters` 系統索引上提供標準的 `_search` 功能，該索引會儲存預測器組態。您必須使用此 API 直接查詢 `.opensearch-forecasters`，因為該索引是系統索引，無法透過一般 OpenSearch 查詢存取。

### 端點

```http
GET _plugins/_forecast/forecasters/_search
```

### 範例請求：依索引進行萬用字元搜尋

下列請求會使用前置錨定的萬用字元，搜尋來源索引名稱開頭為 `network` 的預測器：

```json
GET _plugins/_forecast/forecasters/_search
{
  "query": {
    "wildcard": {
      "indices": {
        "value": "network*"
      }
    }
  }
}
```
{% include copy-curl.html %}

`network*` 會符合 `network`、`network-metrics`、`network_2025-06` 及類似的索引名稱。

#### 範例回應

```json
{
  "took": 5,
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
    "max_score": 1.0,
    "hits": [{
      "_index": ".opensearch-forecasters",
      "_id": "forecast-i1nwqooBLXq6T-gGbXI-",
      "_version": 1,
      "_seq_no": 0,
      "_primary_term": 1,
      "_score": 1.0,
      "_source": {
        "category_field": ["server"],
        "description": "ok rate",
        "feature_attributes": [{
          "feature_id": "deny_max",
          "feature_enabled": true,
          "feature_name": "deny max",
          "aggregation_query": {
            "deny_max": {
              "max": {
                "field": "deny"
              }
            }
          }
        }],
        "forecast_interval": {
          "period": {
            "unit": "Minutes",
            "interval": 1
          }
        },
        "schema_version": 2,
        "time_field": "@timestamp",
        "last_update_time": 1695084997949,
        "horizon": 24,
        "indices": ["network-requests"],
        "window_delay": {
          "period": {
            "unit": "Seconds",
            "interval": 20
          }
        },
        "transform_decay": 1.0E-4,
        "name": "Second-Test-Forecaster-3",
        "filter_query": {
          "match_all": {
            "boost": 1.0
          }
        },
        "shingle_size": 8
      }
    }]
  }
}
```

---

## 搜尋任務

**3.1 版推出**
{: .label .label-purple }

查詢 `.opensearch-forecast-state` 索引中的任務。

### 端點

```http
GET _plugins/_forecast/forecasters/tasks/_search
```

### 範例請求：搜尋先前的單次執行任務

下列請求會擷取特定預測器先前的單次執行任務 (不含最近一次)，並依 `execution_start_time` 遞減排序：

```json
GET _plugins/_forecast/forecasters/tasks/_search
{
  "from": 0,
  "size": 1000,
  "query": {
    "bool": {
      "filter": [
        { "term": { "forecaster_id": { "value": "m5apnooBHh7Wss2wewfW", "boost": 1.0 }}},
        { "term": { "is_latest": { "value": false, "boost": 1.0 }}},
        { "terms": {
            "task_type": [
              "RUN_ONCE_FORECAST_SINGLE_STREAM",
              "RUN_ONCE_FORECAST_HC_FORECASTER"
            ],
            "boost": 1.0
        }}
      ],
      "adjust_pure_negative": true,
      "boost": 1.0
    }
  },
  "sort": [
    { "execution_start_time": { "order": "desc" }}
  ]
}
```
{% include copy-curl.html %}

#### 範例回應

```json
{
  "took": 3,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": { "value": 1, "relation": "eq" },
    "max_score": null,
    "hits": [
      {
        "_index": ".opensearch-forecast-state",
        "_id": "4JaunooBHh7Wss2wOwcw",
        "_version": 3,
        "_seq_no": 5,
        "_primary_term": 1,
        "_score": null,
        "_source": {
          "last_update_time": 1694879344264,
          "execution_start_time": 1694879333168,
          "forecaster_id": "m5apnooBHh7Wss2wewfW",
          "state": "TEST_COMPLETE",
          "task_type": "RUN_ONCE_FORECAST_SINGLE_STREAM",
          "is_latest": false,
          "forecaster": {
            "description": "ok rate",
            "ui_metadata": { "aabb": { "ab": "bb" }},
            "feature_attributes": [
              {
                "feature_id": "deny_max",
                "feature_enabled": true,
                "feature_name": "deny max",
                "aggregation_query": {
                  "deny_max": {
                    "max": { "field": "deny" }
                  }
                }
              }
            ],
            "forecast_interval": {
              "period": {
                "unit": "Minutes",
                "interval": 1
              }
            },
            "schema_version": 2,
            "time_field": "@timestamp",
            "last_update_time": 1694879022036,
            "horizon": 24,
            "indices": [ "network-requests" ],
            "window_delay": {
              "period": {
                "unit": "Seconds",
                "interval": 20
              }
            },
            "transform_decay": 1.0E-4,
            "name": "Second-Test-Forecaster-5",
            "filter_query": { "match_all": { "boost": 1.0 }},
            "shingle_size": 8
          }
        },
        "sort": [ 1694879333168 ]
      }
    ]
  }
}
```

---

## 頂尖預測器
**於 3.1 版推出**
{: .label .label-purple }

根據內建或自訂指標，傳回指定時間戳記範圍內的 *top‑k* 實體。

### 端點

```http
POST _plugins/_forecast/forecasters/{forecaster_id}/results/_topForecasts
```

### 查詢參數

支援下列查詢參數。

| 名稱                    | 類型        | 必要 | 說明 |
| :--- | :--- | :--- | :--- |
| `split_by` | 字串 | 必要 | 用於分組的欄位 (例如 `service`)。 |
| `forecast_from` | Epoch‑ms | 必要 | 評估時間範圍內第一個預測的 `data_end_time`。 |
| `size` | 整數 | 選用 | 要傳回的桶 (bucket) 數量。預設為 `5`。 |
| `filter_by` | 列舉 | 必要 | 指定要使用內建查詢或自訂查詢。必須為 `BUILD_IN_QUERY` 或 `CUSTOM_QUERY`。 |
| `build_in_query` | 列舉 | 選用 | 必須為下列其中一種內建排名條件：<br> `MIN_CONFIDENCE_INTERVAL_WIDTH` -- 依最窄的預測信賴區間排序 (最精確)。<br> `MAX_CONFIDENCE_INTERVAL_WIDTH` -- 依最寬的預測信賴區間排序 (最不精確)。<br> `MIN_VALUE_WITHIN_THE_HORIZON` -- 依預測時間範圍內觀察到的最低預測值排序。<br> `MAX_VALUE_WITHIN_THE_HORIZON` -- 依預測時間範圍內觀察到的最高預測值排序。<br> `DISTANCE_TO_THRESHOLD_VALUE` -- 依預測值與使用者定義閾值之間的差距排序。 |
| `threshold`, `relation_to_threshold` | 混合 | 視條件而定 | 僅在 `build_in_query` 為 `DISTANCE_TO_THRESHOLD_VALUE` 時為必要。 |
| `filter_query` | Query DSL | 選用 | 在 `filter_by=CUSTOM_QUERY` 時使用的自訂查詢。 |
| `subaggregations` | 陣列 | 選用 | 巢狀彙總與排序選項的清單，用於在每個桶內計算其他指標。 |

### 範例請求：以內建查詢取得窄信賴區間

下列請求會傳回依最窄信賴區間排名的頂尖預測實體：

```json
POST _plugins/_forecast/forecasters/AG_3t4kBkYqqimCe86bP/results/_topForecasts
{
  "split_by": "service",
  "filter_by": "BUILD_IN_QUERY",
  "build_in_query": "MIN_CONFIDENCE_INTERVAL_WIDTH",
  "forecast_from": 1691008679297
}
```
{% include copy-curl.html %}

#### 範例回應

```json
{
  "buckets": [
    {
      "key": { "service": "service_6" },
      "doc_count": 1,
      "bucket_index": 0,
      "MIN_CONFIDENCE_INTERVAL_WIDTH": 27.655361
    },
    ...
  ]
}
```

### 範例請求：以內建查詢取得最窄信賴區間

下列請求會傳回經排序的實體清單，其預測值具有最窄的信賴區間。結果會依據 `MIN_CONFIDENCE_INTERVAL_WIDTH` 指標以遞增順序排名：

```json
POST _plugins/_forecast/forecasters/AG_3t4kBkYqqimCe86bP/results/_topForecasts
{
  "split_by": "service",
  "filter_by": "BUILD_IN_QUERY",
  "build_in_query": "MIN_CONFIDENCE_INTERVAL_WIDTH",
  "forecast_from": 1691008679297
}
```
{% include copy-curl.html %}

#### 範例回應

```json
{
    "buckets": [
        {
            "key": {
                "service": "service_6"
            },
            "doc_count": 1,
            "bucket_index": 0,
            "MIN_CONFIDENCE_INTERVAL_WIDTH": 27.655361
        },
        {
            "key": {
                "service": "service_4"
            },
            "doc_count": 1,
            "bucket_index": 1,
            "MIN_CONFIDENCE_INTERVAL_WIDTH": 1324.7734
        },
        {
            "key": {
                "service": "service_0"
            },
            "doc_count": 1,
            "bucket_index": 2,
            "MIN_CONFIDENCE_INTERVAL_WIDTH": 2211.0781
        },
        {
            "key": {
                "service": "service_2"
            },
            "doc_count": 1,
            "bucket_index": 3,
            "MIN_CONFIDENCE_INTERVAL_WIDTH": 3372.0469
        },
        {
            "key": {
                "service": "service_3"
            },
            "doc_count": 1,
            "bucket_index": 4,
            "MIN_CONFIDENCE_INTERVAL_WIDTH": 3980.2812
        }
    ]
}
```

### 範例請求：以內建查詢找出預測值低於閾值的實體

下列請求會根據 `DISTANCE_TO_THRESHOLD_VALUE` 指標，傳回預測值與指定閾值相距最遠的頂尖實體：

```http
POST _plugins/_forecast/AG_3t4kBkYqqimCe86bP/results/_topForecasts
{
  "split_by": "service",                      // group forecasts by the "service" entity field
  "filter_by": "BUILD_IN_QUERY",              // use a built-in ranking metric
  "build_in_query": "DISTANCE_TO_THRESHOLD_VALUE",
  "forecast_from": 1691008679297,             // data_end_time of the first forecast in scope
  "threshold": -82561.8,                      // user-supplied threshold
  "relation_to_threshold": "LESS_THAN"        // keep only forecasts below the threshold
}
```

#### 範例回應

`DISTANCE_TO_THRESHOLD_VALUE` 指標會計算 `forecast_value – threshold`。由於 `relation_to_threshold` 為 `LESS_THAN`，API 只會傳回負距離，並以遞增順序排序 (最負的值優先)。每個桶包含下列值：

- `doc_count`：符合的預測點數量。
- `DISTANCE_TO_THRESHOLD_VALUE`：預測範圍內與閾值之間的最大距離。

下列回應會傳回 `DISTANCE_TO_THRESHOLD_VALUE`：

```json
{
  "buckets": [
    {
      "key": { "service": "service_5" },
      "doc_count": 18,
      "bucket_index": 0,
      "DISTANCE_TO_THRESHOLD_VALUE": -330387.12
    },
    ...
    {
      "key": { "service": "service_0" },
      "doc_count": 1,
      "bucket_index": 4,
      "DISTANCE_TO_THRESHOLD_VALUE": -83561.8
    }
  ]
}
```

### 範例請求：自訂查詢與巢狀彙總

下列請求會使用自訂查詢依名稱比對服務，並依最高預測值進行排名：

```json
POST _plugins/_forecast/AG_3t4kBkYqqimCe86bP/results/_topForecasts
{
  "split_by": "service",
  "forecast_from": 1691018993776,
  "filter_by": "CUSTOM_QUERY",
  "filter_query": {
    "nested": {
      "path": "entity",
      "query": {
        "bool": {
          "must": [
            { "term": { "entity.name": "service" } },
            { "wildcard": { "entity.value": "User*" } }
          ]
        }
      }
    }
  },
  "subaggregations": [
    {
      "aggregation_query": {
        "forecast_value_max": {
          "max": { "field": "forecast_value" }
        }
      },
      "order": "DESC"
    }
  ]
}
```
{% include copy-curl.html %}

#### 範例回應

```json
{
  "buckets": [
    {
      "key": { "service": "UserAuthService" },
      "doc_count": 24,
      "bucket_index": 0,
      "forecast_value_max": 269190.38
    },
    ...
  ]
}
```
---

## 剖析預測器

**於 3.1 版推出**  
{: .label .label-purple }

傳回執行階段狀態，例如初始化進度、各實體的模型中繼資料與錯誤。此 API 適用於在執行期間檢查預測器的間隔。

### 端點

```http
GET _plugins/_forecast/forecasters/{forecaster_id}/_profile[/{type1},{type2}][?_all=true]
```

您可以擷取特定剖析類型，或使用 `_all` 查詢參數請求所有可用類型。

支援下列剖析類型：

- `state`
- `error`
- `coordinating_node`
- `total_size_in_bytes`
- `init_progress`
- `models`
- `total_entities`
- `active_entities`
- `forecast_task`

如果您在請求本文中加入 `entity` 陣列，剖析範圍將僅限於該實體。

### 範例請求：使用實體篩選條件取得預設剖析資料

下列請求會傳回指定實體的預設剖析類型（`state` 與 `error`）：

```http
GET _plugins/_forecast/forecasters/tLch1okBCBjX5EchixQ8/_profile
{
  "entity": [
    {
      "name": "service",
      "value": "app_1"
    },
    {
      "name": "host",
      "value": "server_2"
    }
  ]
}
```
{% include copy-curl.html %}

#### 範例回應

```json
{
  "state": "RUNNING"
}
```

### 範例請求：多個剖析類型

下列請求會擷取 `init_progress`、`error`、`total_entities` 與 `state` 剖析類型：

```http
GET _plugins/_forecast/forecasters/mZ6P0okBTUNS6IWgvpwo/_profile/init_progress,error,total_entities,state
```
{% include copy-curl.html %}

### 範例請求：所有剖析類型

下列請求會傳回所有可用的剖析類型：

```http
GET _plugins/_forecast/forecasters/d7-r1YkB_Z-sgDOKo3Z5/_profile?_all=true&pretty
```
{% include copy-curl.html %}


---

## 預測器統計
**於 3.1 版導入**  
{: .label .label-purple }

傳回叢集層級或節點層級的統計資料，包括預測器數量、模型計數、請求計數器，以及內部預測索引的健康狀態。

### 端點

```http
GET _plugins/_forecast/stats
GET _plugins/_forecast/{node_id}/stats
GET _plugins/_forecast/stats/{stat_name}
```

### 範例請求：擷取所有統計資料

下列請求會擷取所有預測器的叢集層級統計資料，包括計數、模型資訊與索引狀態：

```http
GET _plugins/_forecast/stats
```
{% include copy-curl.html %}

#### 範例回應

```json
{
  "hc_forecaster_count": 1,
  "forecast_results_index_status": "yellow",
  "forecast_models_checkpoint_index_status": "yellow",
  "single_stream_forecaster_count": 1,
  "forecastn_state_status": "yellow",
  "forecaster_count": 2,
  "job_index_status": "yellow",
  "config_index_status": "yellow",
  "nodes": {
    "8B2S4ClnRFK3GTjO45bwrw": {
      "models": [
        {
          "model_type": "rcf_caster",
          "last_used_time": 1692245336895,
          "model_id": "Doj0AIoBEU5Xd2ccoe_9_entity_SO2kPi_PAMsvThWyE-zYHg",
          "last_checkpoint_time": 1692233157256,
          "entity": [
            { "name": "host_nest.host2", "value": "server_2" }
          ]
        }
      ],
      "forecast_hc_execute_request_count": 204,
      "forecast_model_corruption_count": 0,
      "forecast_execute_failure_count": 0,
      "model_count": 4,
      "forecast_execute_request_count": 409,
      "forecast_hc_execute_failure_count": 0
    }
  }
}
```

### 範例請求：擷取特定節點的統計資料

下列請求會依節點 ID 擷取特定節點的預測器統計資料：

```http
GET _plugins/_forecast/8B2S4ClnRFK3GTjO45bwrw/stats
```
{% include copy-curl.html %}

### 範例請求：擷取高基數請求的總數

下列請求會擷取所有節點的高基數預測器請求總數：

```http
GET _plugins/_forecast/stats/forecast_hc_execute_request_count
```
{% include copy-curl.html %}

### 範例請求：擷取特定節點的高基數請求計數

下列請求會擷取特定節點所執行的高基數預測器請求數量：

```http
GET _plugins/_forecast/0ZpL8WEYShy-qx7hLJQREQ/stats/forecast_hc_execute_request_count/
```
{% include copy-curl.html %}


---

## 預測器資訊
**於 3.1 版導入**
{: .label .label-purple }

傳回一個整數，代表叢集中預測器組態的總數，或檢查是否存在符合指定搜尋條件的預測器。


### 端點
```http
GET _plugins/_forecast/forecasters/count
GET _plugins/_forecast/forecasters/match?name={forecaster_name}
```

### 範例請求：計算預測器數量

下列請求會傳回叢集中目前儲存的預測器組態數量：

```http
GET _plugins/_forecast/forecasters/count
```
{% include copy-curl.html %}

### 範例回應

```json
{
  "count": 2,
  "match": false
}
```

### 範例請求：比對預測器名稱

下列請求會尋找名為 `Second-Test-Forecaster-3` 的預測器：

```http
GET _plugins/_forecast/forecasters/match?name=Second-Test-Forecaster-3
```
{% include copy-curl.html %}

### 範例回應：找到符合項目

```json
{
  "count": 0,
  "match": true
}
```

### 範例回應：找不到符合項目

```json
{
  "count": 0,
  "match": false
}
```
