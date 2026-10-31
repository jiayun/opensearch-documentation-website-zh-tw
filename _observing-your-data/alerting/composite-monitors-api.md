---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "複合監視器 API"
parent: Alerting
nav_order: 65
---

# 複合監視器 API

使用複合監視器 API 來建立及管理[複合監視器]({{site.url}}{{site.baseurl}}/observing-your-data/alerting/composite-monitors/)及其連鎖警示。在 API 中，複合監視器稱為*工作流程*（workflow），其 ID 即為工作流程 ID。

## 建立複合監視器

建立複合監視器。

### 端點

```json
POST _plugins/_alerting/workflows
```

### 請求本文欄位

下表列出可用的請求本文欄位。

欄位 | 資料類型 | 必要 | 說明
:--- | :--- | :--- | :---
`name` | 字串 | 必要 | 複合監視器的名稱。
`workflow_type` | 字串 | 必要 | 設為 `composite`。
`schedule` | 物件 | 必要 | 複合監視器的執行頻率。請參閱[`schedule` 物件](#the-schedule-object)。
`inputs` | 陣列 | 必要 | 委派監視器及其執行順序。請參閱[`inputs` 陣列](#the-inputs-array)。
`triggers` | 陣列 | 選用 | 產生連鎖警示的觸發條件。請參閱[`triggers` 陣列](#the-triggers-array)。
`enabled` | 布林值 | 選用 | 是否啟用複合監視器。預設為 `true`。

### `schedule` 物件

`schedule` 物件包含 `period` 物件，其中含有下列欄位。

欄位 | 資料類型 | 說明
:--- | :--- | :---
`interval` | 整數 | 兩次執行之間的時間單位數。
`unit` | 字串 | 間隔的時間單位。有效值為 `MINUTES`、`HOURS` 及 `DAYS`。

### `inputs` 陣列

`inputs` 陣列包含一個含有 `composite_input.sequence.delegates` 陣列的物件。`delegates` 陣列中的每個物件含有下列欄位。

欄位 | 資料類型 | 說明
:--- | :--- | :---
`order` | 整數 | 委派監視器在序列中的位置。委派監視器依遞增順序執行。
`monitor_id` | 字串 | 委派監視器的 ID。複合監視器支援以每次查詢（per query）、每個桶（per bucket）及每份文件（per document）監視器作為委派監視器。

### `triggers` 陣列

`triggers` 陣列中的每個物件含有一個 `chained_alert_trigger` 物件，其中含有下列欄位。

欄位 | 資料類型 | 說明
:--- | :--- | :---
`id` | 字串 | 觸發條件 ID。
`name` | 字串 | 觸發條件名稱。
`severity` | 字串 | 警示嚴重性，從 `1`（最高）到 `5`（最低）。
`condition` | 物件 | 觸發條件。含有 `script` 物件，其中 `source` 是產生連鎖警示的 Painless 條件，而 `lang` 為 `painless`。請參閱[定義連鎖警示觸發條件](#defining-chained-alert-trigger-conditions)。
`actions` | 陣列 | 符合觸發條件時要執行的動作。動作欄位請參閱[動作]({{site.url}}{{site.baseurl}}/observing-your-data/alerting/actions/)。

### 定義連鎖警示觸發條件

連鎖警示觸發條件會使用 `monitor[id=<monitor-id>]` 參照委派監視器，當委派監視器在目前執行中產生警示時，其值為 `true`。您可以使用下列運算子組合這些參照：

- `&&`（AND）
- `||`（OR）
- `!`（NOT）
- `()`（優先順序）

例如：

- 當監視器 1 和監視器 2 都產生警示時，`monitor[id=1] && monitor[id=2]` 會產生連鎖警示。
- 當監視器 1 產生警示或監視器 2 未產生警示時，`monitor[id=1] || !monitor[id=2]` 會產生連鎖警示。
- 當監視器 1 產生警示，且監視器 2 或監視器 3 其中一個產生警示時，`monitor[id=1] && (monitor[id=2] || monitor[id=3])` 會產生連鎖警示。

條件中監視器 ID 的順序不會影響委派監視器的執行順序。執行順序由 `delegates` 陣列中的 `order` 欄位設定。
{: .note }

### 範例請求

下列請求會建立含有兩個委派監視器及兩個觸發條件的複合監視器。當兩個委派監視器都產生警示時，`Both monitors` 觸發條件會產生連鎖警示。當其中至少一個產生警示時，`Either monitor` 觸發條件會產生連鎖警示：

```json
POST _plugins/_alerting/workflows
{
  "name": "Traffic and errors",
  "workflow_type": "composite",
  "enabled": true,
  "schedule": {
    "period": {
      "interval": 1,
      "unit": "MINUTES"
    }
  },
  "inputs": [
    {
      "composite_input": {
        "sequence": {
          "delegates": [
            {
              "order": 1,
              "monitor_id": "grsbCIcBvEHfkjWFeCqb"
            },
            {
              "order": 2,
              "monitor_id": "agasbCIcBvEHfkjWFeCqa"
            }
          ]
        }
      }
    }
  ],
  "triggers": [
    {
      "chained_alert_trigger": {
        "id": "m1ANDm2",
        "name": "Both monitors",
        "severity": "1",
        "condition": {
          "script": {
            "source": "(monitor[id=grsbCIcBvEHfkjWFeCqb] && monitor[id=agasbCIcBvEHfkjWFeCqa])",
            "lang": "painless"
          }
        },
        "actions": []
      }
    },
    {
      "chained_alert_trigger": {
        "id": "m1ORm2",
        "name": "Either monitor",
        "severity": "2",
        "condition": {
          "script": {
            "source": "(monitor[id=grsbCIcBvEHfkjWFeCqb] || monitor[id=agasbCIcBvEHfkjWFeCqa])",
            "lang": "painless"
          }
        },
        "actions": []
      }
    }
  ]
}
```
{% include copy-curl.html %}

## 取得複合監視器

傳回複合監視器的組態。

### 端點

```json
GET _plugins/_alerting/workflows/{workflow_id}
```

### 路徑參數

下表列出可用的路徑參數。

參數 | 資料類型 | 說明
:--- | :--- | :---
`workflow_id` | 字串 | 複合監視器的工作流程 ID。必要。

### 範例請求

```json
GET _plugins/_alerting/workflows/SX9egKEBrJhc2kcbnbU_
```
{% include copy-curl.html %}

## 更新複合監視器

取代複合監視器的組態。請求本文欄位與[建立複合監視器](#create-composite-monitor)相同。

### 端點

```json
PUT _plugins/_alerting/workflows/{workflow_id}
```

### 範例請求

下列請求會將複合監視器變更為每 5 分鐘執行一次，並只保留 `Both monitors` 觸發條件：

```json
PUT _plugins/_alerting/workflows/SX9egKEBrJhc2kcbnbU_
{
  "name": "Traffic and errors",
  "workflow_type": "composite",
  "enabled": true,
  "schedule": {
    "period": {
      "interval": 5,
      "unit": "MINUTES"
    }
  },
  "inputs": [
    {
      "composite_input": {
        "sequence": {
          "delegates": [
            {
              "order": 1,
              "monitor_id": "grsbCIcBvEHfkjWFeCqb"
            },
            {
              "order": 2,
              "monitor_id": "agasbCIcBvEHfkjWFeCqa"
            }
          ]
        }
      }
    }
  ],
  "triggers": [
    {
      "chained_alert_trigger": {
        "id": "m1ANDm2",
        "name": "Both monitors",
        "severity": "1",
        "condition": {
          "script": {
            "source": "(monitor[id=grsbCIcBvEHfkjWFeCqb] && monitor[id=agasbCIcBvEHfkjWFeCqa])",
            "lang": "painless"
          }
        },
        "actions": []
      }
    }
  ]
}
```
{% include copy-curl.html %}

## 刪除複合監視器

刪除一個複合監視器。委派的監視器不會被刪除。

### 端點

```json
DELETE _plugins/_alerting/workflows/{workflow_id}
```

### 範例請求

```json
DELETE _plugins/_alerting/workflows/SX9egKEBrJhc2kcbnbU_
```
{% include copy-curl.html %}

## 執行複合監視器

立即執行一個複合監視器並回傳觸發結果。

### 端點

```json
POST _plugins/_alerting/workflows/{workflow_id}/_execute
```

### 範例請求

```json
POST _plugins/_alerting/workflows/SX9egKEBrJhc2kcbnbU_/_execute
```
{% include copy-curl.html %}

### 範例回應

```json
{
    "execution_id": "I0GXeIgBYKBG2nHoiHCL_2023-06-01T20:18:48.511884_a9c1d055-9b70-49c2-b32a-716cff1f562e",
    "workflow_name": "scale_up",
    "workflow_id": "I0GXeIgBYKBG2nHoiHCL",
    "trigger_results": {
        "m1ANDm2": {
            "name": "jnkjn",
            "triggered": true,
            "action_results": {},
            "error": null
        },
        "m1ORm2": {
            "name": "jnkjn",
            "triggered": true,
            "action_results": {},
            "error": null
        }
    },
    "monitor_run_results": [{
            "monitor_name": "test triggers",
            "period_start": 1685650668501,
            "period_end": 1685650728501,
            "error": null,
            "input_results": {
                "results": [{
                    "bhjh": [
                        "OkGceIgBYKBG2nHoyHAn|test1",
                        "O0GceIgBYKBG2nHozHCW|test1"
                    ],
                    "nkjkj": [
                        "OkGceIgBYKBG2nHoyHAn|test1",
                        "O0GceIgBYKBG2nHozHCW|test1"
                    ],
                    "jknkjn": [
                        "OkGceIgBYKBG2nHoyHAn|test1",
                        "O0GceIgBYKBG2nHozHCW|test1"
                    ]
                }],
                "error": null
            },
            "trigger_results": {
                "NC3Dd4cBCDCIfBYtViLI": {
                    "name": "njkkj",
                    "triggeredDocs": [
                        "OkGceIgBYKBG2nHoyHAn|test1",
                        "O0GceIgBYKBG2nHozHCW|test1"
                    ],
                    "action_results": {},
                    "error": null
                }
            }
        },
        {
            "monitor_name": "test triggers 2",
            "period_start": 1685650668501,
            "period_end": 1685650728501,
            "error": null,
            "input_results": {
                "results": [{
                    "bhjh": [
                        "PEGceIgBYKBG2nHo1HCw|test",
                        "PUGceIgBYKBG2nHo3HA8|test"
                    ],
                    "nkjkj": [
                        "PEGceIgBYKBG2nHo1HCw|test",
                        "PUGceIgBYKBG2nHo3HA8|test"
                    ],
                    "jknkjn": [
                        "PEGceIgBYKBG2nHo1HCw|test",
                        "PUGceIgBYKBG2nHo3HA8|test"
                    ]
                }],
                "error": null
            },
            "trigger_results": {
                "NC3Dd4cBCDCIfBYtViLI": {
                    "name": "njkkj",
                    "triggeredDocs": [
                        "PEGceIgBYKBG2nHo1HCw|test",
                        "PUGceIgBYKBG2nHo3HA8|test"
                    ],
                    "action_results": {},
                    "error": null
                }
            }
        }
    ],
    "execution_start_time": "2023-06-01T20:18:48.511874Z",
    "execution_end_time": "2023-06-01T20:18:53.682405Z",
    "error": null
}
```

## 取得連鎖警示

回傳由複合監視器產生的連鎖警示。

### 端點

```json
GET _plugins/_alerting/workflows/alerts
```

### 查詢參數

下表列出可用的查詢參數。所有查詢參數皆為選用。

參數 | 資料類型 | 說明
:--- | :--- | :---
`workflowIds` | 字串 | 以逗號分隔的工作流程 ID 清單。只回傳由這些複合監視器產生的警示。
`getAssociatedAlerts` | 布林值 | 設為 `true` 時，回應也會包含由委派監視器產生的稽核警示。預設為 `false`。

### 範例請求

```json
GET _plugins/_alerting/workflows/alerts?workflowIds=SX9egKEBrJhc2kcbnbU_&getAssociatedAlerts=true
```
{% include copy-curl.html %}

### 範例回應

```json
{
    "alerts": [
        {
            "id": "PbQoZokBfd2ci_FqMGi6",
            "version": 1,
            "monitor_id": "",
            "workflow_id": "G7QoZokBfd2ci_FqD2iZ",
            "workflow_name": "scale_up",
            "associated_alert_ids": [
                "4e8256c5-529a-484c-bf7b-d3980c03e9a4",
                "513a8cb3-44bc-4eee-8aac-131be10b399e"
            ],
            "schema_version": -1,
            "monitor_version": -1,
            "monitor_name": "",
            "execution_id": "G7QoZokBfd2ci_FqD2iZ_2023-07-17T23:20:55.244970_edd977d2-c02b-4cbe-8a79-2aa7991c4191",
            "trigger_id": "m1ANDm2",
            "trigger_name": "jnkjn",
            "finding_ids": [],
            "related_doc_ids": [],
            "state": "ACTIVE",
            "error_message": null,
            "alert_history": [],
            "severity": "1",
            "action_execution_results": [],
            "start_time": 1689636057269,
            "last_notification_time": 1689636057270,
            "end_time": null,
            "acknowledged_time": null
        },
        {
            "id": "PrQoZokBfd2ci_FqMGj8",
            "version": 1,
            "monitor_id": "",
            "workflow_id": "G7QoZokBfd2ci_FqD2iZ",
            "workflow_name": "scale_up",
            "associated_alert_ids": [
                "4e8256c5-529a-484c-bf7b-d3980c03e9a4",
                "513a8cb3-44bc-4eee-8aac-131be10b399e"
            ],
            "schema_version": -1,
            "monitor_version": -1,
            "monitor_name": "",
            "execution_id": "G7QoZokBfd2ci_FqD2iZ_2023-07-17T23:20:55.244970_edd977d2-c02b-4cbe-8a79-2aa7991c4191",
            "trigger_id": "m1ORm2",
            "trigger_name": "jnkjn",
            "finding_ids": [],
            "related_doc_ids": [],
            "state": "ACTIVE",
            "error_message": null,
            "alert_history": [],
            "severity": "1",
            "action_execution_results": [],
            "start_time": 1689636057340,
            "last_notification_time": 1689636057340,
            "end_time": null,
            "acknowledged_time": null
        }
    ],
    "associatedAlerts": [
        {
            "id": "4e8256c5-529a-484c-bf7b-d3980c03e9a4",
            "version": -1,
            "monitor_id": "DrQoZokBfd2ci_FqCWh8",
            "workflow_id": "G7QoZokBfd2ci_FqD2iZ",
            "workflow_name": "",
            "associated_alert_ids": [],
            "schema_version": 5,
            "monitor_version": 1,
            "monitor_name": "test triggers",
            "execution_id": "G7QoZokBfd2ci_FqD2iZ_2023-07-17T23:20:55.244970_edd977d2-c02b-4cbe-8a79-2aa7991c4191",
            "trigger_id": "NC3Dd4cBCDCIfBYtViLI",
            "trigger_name": "njkkj",
            "finding_ids": [
                "277afca7-d5aa-46ed-8023-5449ece65d36"
            ],
            "related_doc_ids": [
                "H7QoZokBfd2ci_FqFmii|test1"
            ],
            "state": "AUDIT",
            "error_message": null,
            "alert_history": [],
            "severity": "1",
            "action_execution_results": [],
            "start_time": 1689636056410,
            "last_notification_time": 1689636056410,
            "end_time": null,
            "acknowledged_time": null
        },
        {
            "id": "513a8cb3-44bc-4eee-8aac-131be10b399e",
            "version": -1,
            "monitor_id": "EbQoZokBfd2ci_FqCmiR",
            "workflow_id": "G7QoZokBfd2ci_FqD2iZ",
            "workflow_name": "",
            "associated_alert_ids": [],
            "schema_version": 5,
            "monitor_version": 1,
            "monitor_name": "test triggers 2",
            "execution_id": "G7QoZokBfd2ci_FqD2iZ_2023-07-17T23:20:55.244970_edd977d2-c02b-4cbe-8a79-2aa7991c4191",
            "trigger_id": "NC3Dd4cBCDCIfBYtViLI",
            "trigger_name": "njkkj",
            "finding_ids": [
                "6d185585-a077-4dde-8e43-b4c01b9f3102"
            ],
            "related_doc_ids": [
                "ILQoZokBfd2ci_FqGmhb|test"
            ],
            "state": "AUDIT",
            "error_message": null,
            "alert_history": [],
            "severity": "1",
            "action_execution_results": [],
            "start_time": 1689636056943,
            "last_notification_time": 1689636056943,
            "end_time": null,
            "acknowledged_time": null
        }
    ],
    "totalAlerts": 2
}
```

### 回應本文欄位

下表列出所有回應本文欄位。

欄位 | 資料類型 | 說明
:--- | :--- | :---
`alerts` | 陣列 | 複合監視器產生的鏈結警示。
`associatedAlerts` | 陣列 | 委派監視器產生的稽核警示。僅當 `getAssociatedAlerts` 為 `true` 時傳回。
`totalAlerts` | 整數 | 鏈結警示的總數。

## 確認鏈結警示

確認一或多個作用中的鏈結警示。已處於 `ERROR`、`COMPLETED` 或 `ACKNOWLEDGED` 狀態的警示會以 `failed` 陣列傳回。

### 端點

```json
POST _plugins/_alerting/workflows/{workflow_id}/_acknowledge/alerts
```

### 請求本文欄位

下表列出可用的請求本文欄位。

欄位 | 資料類型 | 必要 | 說明
:--- | :--- | :--- | :---
`alerts` | 字串陣列 | 必要 | 要確認的警示 ID。若要取得警示 ID，請使用[取得鏈結警示](#get-chained-alerts)。

### 範例請求

```json
POST _plugins/_alerting/workflows/SX9egKEBrJhc2kcbnbU_/_acknowledge/alerts
{
  "alerts": ["VH9egKEBrJhc2kcbnrU5"]
}
```
{% include copy-curl.html %}

### 範例回應

```json
{
  "success": ["VH9egKEBrJhc2kcbnrU5"],
  "failed": []
}
```
