---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "管理預測器"
nav_order: 8
parent: Forecasting
has_children: false
---

# 管理預測器

在[建立預測器]({{site.url}}{{site.baseurl}}/observing-your-data/forecast/getting-started/)之後，您可以使用 **Details** 頁面管理其生命週期與組態。這包括啟動或停止預測器、更新其設定，或完全刪除它。您可以使用此頁面監視預測器狀態、疑難排解問題，並隨時間微調行為。

## Forecasters 表格

**Forecasters** 表格提供您已設定之每個預測器的總覽。

| 欄位 | 說明 |
|--------|-------------|
| **Name** | 您在建立預測器時指派的名稱。 |
| **Status** | 目前的生命週期狀態，例如 `Running`、`Initializing` 或 `Test complete`。按一下 <i class="euiIcon euiIcon--xs euiIcon--expand"></i> 圖示可取得更多資訊，包括最近一次狀態變更的時間戳記以及任何失敗訊息。 |
| **Index** | 預測器讀取資料的來源索引或別名。 |
| **Last updated** | 最近一次組態變更的時間戳記。 |
| **Quick actions** | 依預測器目前狀態而定的情境感知按鈕，例如 **Start**、**Stop** 或 **Delete**。 |

## 執行狀態

預測器（也就是底層的預測工作）可能處於下列任一狀態。標記為*自動*的轉換無需使用者操作即可發生；其他狀態則需要您手動選取 **Start** 或 **Stop**。

| 狀態 | 說明 | 典型觸發方式 |
|-------|-------------|------------------|
| **Inactive** | 預測器已建立但從未啟動。 | 無。 |
| **Inactive: stopped** | 預測器在執行後被手動停止。 | 使用者選取 **Stop forecasting**。 |
| **Awaiting data to initialize forecast** | 工作嘗試啟動但歷史資料不足。 | 自動。 |
| **Awaiting data to restart forecast** | 工作在資料中斷後恢復，正在等待新資料。 | 資料中斷後自動發生。 |
| **Initializing test** | 正在為一次性回測建置模型。 | 選取 **Create and test** 或 **Start test** 後自動發生。 |
| **Test complete** | 回測已完成，工作不再執行。 | 自動。 |
| **Initializing forecast** | 正在訓練模型以進行持續的即時預測。 | 選取 **Start forecasting** 後自動發生。 |
| **Running** | 工作正在串流即時資料並產生預測。 | 初始化成功完成時自動發生。 |
| **Initializing test failed** | 測試失敗，通常是由於資料不足。 | 自動。 |
| **Initializing forecast failed** | 即時模式初始化失敗。 | 自動。 |
| **Forecast failed** | 工作已啟動但遇到執行階段錯誤，例如分片失敗。 | 自動，但需要使用者注意。 |

下圖說明各狀態之間的關係與轉換。

![Forecast state diagram]({{site.url}}{{site.baseurl}}/images/forecast/state.png){: width="1600" height="1600" }

## 尋找與篩選預測器

如果您有許多預測器，可以使用表格底部的分頁控制項在頁面之間導覽。您也可以使用搜尋列依 **name**、**status** 或 **index** 進行篩選，這在管理大量預測器時很有幫助。

## 針對預測值發出警示

由於預測結果索引不是系統索引，您可以像對任何其他使用者索引一樣，為結果索引建立[警示監視器]({{site.url}}{{site.baseurl}}/monitoring-plugins/alerting/)。

### 警示監視器範例

例如，以下是一個針對高基數預測器的監視器。您可以修改排程、查詢與彙總以符合您的使用情境：

{% raw %}
```json
{
   "name": "test",
   "type": "monitor",
   "monitor_type": "query_level_monitor",
   "enabled": true,
   "schedule": {
      "period": {
         "unit": "MINUTES",
         "interval": 1
      }
   },
   "inputs": [
      {
         "search": {
            "indices": [
               "opensearch-forecast-results*"
            ],
            "query": {
               "size": 1,
               "query": {
                  "bool": {
                     "filter": [
                        {
                           "range": {
                              "execution_end_time": {
                                 "from": "{{period_end}}||-15m",
                                 "to": "{{period_end}}",
                                 "include_lower": true,
                                 "include_upper": true,
                                 "format": "epoch_millis",
                                 "boost": 1
                              }
                           }
                        }
                     ],
                     "adjust_pure_negative": true,
                     "boost": 1
                  }
               },
               "aggregations": {
                  "metric": {
                     "max": {
                        "field": "forecast_upper_bound"
                     }
                  }
               }
            }
         }
      }
   ],
   "triggers": [
      {
         "query_level_trigger": {
            "id": "29oAl5cB5QuI4WJQ3hnx",
            "name": "breach",
            "severity": "1",
            "condition": {
               "script": {
                  "source": "return ctx.results[0].aggregations.metric.value == null ? false : ctx.results[0].aggregations.metric.value > 10000",
                  "lang": "painless"
               }
            },
            "actions": [
               {
                  "id": "notification378084",
                  "name": "email",
                  "destination_id": "2uzIlpcBMf-0-aT5HOtn",
                  "message_template": {
                     "source": "Monitor **{{ctx.monitor.name}}** entered **ALERT** state — please investigate.\n\nTrigger    : {{ctx.trigger.name}}\nSeverity   : {{ctx.trigger.severity}}\nTime range : {{ctx.periodStart}} → {{ctx.periodEnd}} UTC\n\nEntity\n{{#ctx.results.0.hits.hits.0._source.entity}}\n  • {{name}} = {{value}}\n{{/ctx.results.0.hits.hits.0._source.entity}}\n",
                     "lang": "mustache"
                  },
                  "throttle_enabled": true,
                  "subject_template": {
                     "source": "Alerting Notification action",
                     "lang": "mustache"
                  },
                  "throttle": {
                     "value": 15,
                     "unit": "MINUTES"
                  }
               }
            ]
         }
      }
   ],
   "ui_metadata": {
      "schedule": {
         "timezone": null,
         "frequency": "interval",
         "period": {
            "unit": "MINUTES",
            "interval": 1
         },
         "daily": 0,
         "weekly": {
            "tue": false,
            "wed": false,
            "thur": false,
            "sat": false,
            "fri": false,
            "mon": false,
            "sun": false
         },
         "monthly": {
            "type": "day",
            "day": 1
         },
         "cronExpression": "0 */1 * * *"
      },
      "monitor_type": "query_level_monitor",
      "search": {
         "searchType": "query",
         "timeField": "execution_end_time",
         "aggregations": [
            {
               "aggregationType": "max",
               "fieldName": "forecast_upper_bound"
            }
         ],
         "groupBy": [],
         "bucketValue": 15,
         "bucketUnitOfTime": "m",
         "filters": []
      }
   }
}
```
{% endraw %}
{% include copy-curl.html %}

### 監視器設計

下表說明範例警示監視器中使用的每個設計選擇及其重要性。

| 設計選擇 | 理由 |
|---------------|-----------|
| 搜尋輸入中的 `size: 1` | 擷取單一文件，讓您可以在通知中參照 `ctx.results.0.hits.hits.0`，以識別是哪個實體（例如 `host` 或 `service`）觸發了警示。 |
| `execution_end_time` 範圍 `"now-15m"` → `now` | 依結果建立時間戳記篩選，該時間戳記反映預測產生的時間。這可避免匯入延遲造成的延誤。如果您的索引包含延遲抵達的資料（例如回填的記錄檔），請避免依 `data_end_time` 篩選。 |
| 以 `max(forecast_upper_bound)` 作為指標 | 偵測上限飆升。其他選項包括：<br> `min(forecast_lower_bound)` 用於偵測突然下降。<br> `avg(forecast_value)` 用於偵測趨勢變化。<br> 如需其他欄位，請參閱[預測結果結構描述](https://github.com/opensearch-project/anomaly-detection/blob/main/src/main/resources/mappings/forecast-results.json)。 |
| 索引模式 `opensearch-forecast-results*` | 符合預設的結果索引模式。如果您將結果路由至自訂索引（例如 `opensearch-forecast-result-abc*`），請更新此模式。 |
| `forecaster_id` 上的選用詞彙篩選 | 使用此篩選器以鎖定特定預測器，避免比對到不相關的預測。 |
| 監視器每 1 分鐘執行一次，查詢視窗 15 分鐘 | 每分鐘評估一次預測，以快速偵測異常。15 分鐘的回溯視窗可提高對時間延遲的容錯能力。結合 15 分鐘的警示節流，可避免同一事件產生重複通知。 |
| Mustache 區塊印出所有實體維度 | 顯示單維度（`host=server_3`）與多維度（`host=server_3`、`service=auth`）的實體值。您也可以加入連結至預先篩選的儀表板，以加快分類速度。 |
| 門檻值 | 使用 OpenSearch Dashboards 視覺化編輯器分析最近的預測值，並決定能可靠指出異常的適當門檻值。 |


### 警示範例

以下範例顯示由監視器產生的警示電子郵件樣本，該監視器會在預測值超出定義的門檻值時進行偵測。在此案例中，監視器正在追蹤一個高基數預測器，並已針對特定實體（`host = server_3`）觸發警示：

```
Monitor **test** entered **ALERT** state — please investigate.

Trigger    : breach
Severity   : 1
Time range : 2025-06-22T09:56:14.490Z → 2025-06-22T09:57:14.490Z UTC

Entity
  • host = server_3
```

## 後續步驟

在設定並管理您的預測器之後，您可能會想控制誰可以存取與修改它們。若要了解如何管理權限、保護結果索引以及套用細微存取控制，請參閱[安全性頁面]({{site.url}}{{site.baseurl}}/observing-your-data/forecast/security/)。


