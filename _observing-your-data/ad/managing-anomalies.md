---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "設定異常警示"
nav_order: 60
parent: Anomaly detection
has_children: false
---

# 設定異常警示

建立[異常偵測器]({{site.url}}{{site.baseurl}}/observing-your-data/ad/)之後，您可以設定警示，以便在發生異常時收到通知。若要設定警示，請建立[警示監視器]({{site.url}}{{site.baseurl}}/monitoring-plugins/alerting/)，如下圖所示。如需建立警示監視器的操作說明，請參閱[建立警示監視器]({{site.url}}{{site.baseurl}}/observing-your-data/alerting/index/#creating-an-alert-monitor)。

![警示編輯器]({{site.url}}{{site.baseurl}}/images/anomaly-detection/alerting_editor.png){: width="800" height="800" }

在 **Monitor defining method** 中，選擇下列其中一種方法來定義您的監視器：

- **Anomaly detector**：用於監視個別偵測器的結果，並設定異常等級與信賴度的閾值。
- **Extraction query editor**：用於監視多個偵測器、撰寫複雜查詢，或建立進階觸發條件。



## 範例警示監視器

下列監視器是為高基數偵測器所設計。您可以修改排程、查詢和彙總，以符合您的特定使用情境：

{% raw %}
```json
{
   "name": "ad-monitor",
   "type": "monitor",
   "monitor_type": "query_level_monitor",
   "enabled": true,
   "schedule": {
      "period": {
         "unit": "MINUTES",
         "interval": 2
      }
   },
   "inputs": [
      {
         "search": {
            "indices": [
               ".opendistro-anomaly-results*"
            ],
            "query": {
               "size": 1,
               "sort": [
                  {
                     "anomaly_grade": "desc"
                  },
                  {
                     "confidence": "desc"
                  }
               ],
               "query": {
                  "bool": {
                     "filter": [
                        {
                           "range": {
                              "execution_end_time": {
                                 "from": "{{period_end}}||-2m",
                                 "to": "{{period_end}}",
                                 "include_lower": true,
                                 "include_upper": true
                              }
                           }
                        },
                        {
                           "term": {
                              "detector_id": {
                                 "value": "oJzeoZkB8KmRTvydzJDF"
                              }
                           }
                        }
                     ]
                  }
               },
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
         "query_level_trigger": {
            "id": "i5zuoZkB8KmRTvydn5Hg",
            "name": "ad-trigger",
            "severity": "1",
            "condition": {
               "script": {
                  "source": "return ctx.results != null && ctx.results.length > 0 && ctx.results[0].aggregations != null && ctx.results[0].aggregations.max_anomaly_grade != null && ctx.results[0].hits.total.value > 0 && ctx.results[0].hits.hits[0]._source != null && ctx.results[0].hits.hits[0]._source.confidence != null && ctx.results[0].aggregations.max_anomaly_grade.value != null && ctx.results[0].aggregations.max_anomaly_grade.value > 0.7 && ctx.results[0].hits.hits[0]._source.confidence > 0.7",
                  "lang": "painless"
               }
            },
            "actions": [
               {
                  "id": "notification606448",
                  "name": "ad-action",
                  "destination_id": "fpzsoZkB8KmRTvydkZGQ",
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
                     "value": 2,
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
            "interval": 2
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
         "cronExpression": "0 */2 * * *"
      },
      "monitor_type": "query_level_monitor",
      "search": {
         "searchType": "ad",
         "timeField": "",
         "aggregations": [],
         "groupBy": [],
         "bucketValue": 1,
         "bucketUnitOfTime": "h",
         "filters": []
      }
   }
}
```
{% endraw %}
{% include copy.html %}

請注意範例警示監視器中的下列重要組態：

- 搜尋輸入中的 **`"size": 1`**：擷取單一文件，讓您可以在通知中參照 `ctx.results.0.hits.hits.0`，以識別是哪個實體 (例如 `host` 或 `service`) 觸發了警示。

- **`execution_end_time` 範圍 `"{{period_end}}||-2m"` → `"{{period_end}}"`**：根據偵測器 `execution_end_time` 篩選結果---也就是偵測器完成執行並將結果編製索引的時間。由於 OpenSearch 以近乎即時的方式運作 (結果並非立即產生)，編製索引和重新整理作業會造成延遲，文件才會變成可搜尋。為了因應這種寫入到搜尋的延遲，本範例包含一小段重疊時間 (`-2m`)。請根據系統最壞情況的延遲來指定重疊時間。請避免使用 `data_end_time` (桶的邏輯結束時間)，因為這可能會遺漏較晚送達的結果。

- **`"indices": [".opendistro-anomaly-results*"]`**：符合預設的結果索引模式。如果您將結果路由到自訂索引 (例如 `opensearch-ad-plugin-result-abc*`)，請更新此模式。

- **`"detector_id": {"value": "oJzeoZkB8KmRTvydzJDF"}`** (選用)：使用此篩選條件來鎖定特定偵測器，並避免比對到其他偵測器不相關的異常。

- **`"max_anomaly_grade"` 彙總**：偵測時間範圍內最嚴重的異常。您可以使用異常結果索引中的任何欄位來進行彙總。如需其他欄位，請參閱[異常結果對應]({{site.url}}{{site.baseurl}}/monitoring-plugins/ad/result-mapping/)。

- **每 2 分鐘執行一次的監視器排程**：每 2 分鐘評估一次結果，以快速偵測異常。搭配 2 分鐘的警示節流，可避免同一事件產生重複通知。

- **觸發條件 `max_anomaly_grade.value > 0.7 && confidence > 0.7`**：設定適當的閾值，以可靠地指出異常。請根據您對偽陽性和偽陰性的容忍度來調整這些值。

- **含實體區塊的 Mustache 範本**：在通知中同時顯示單維度 (`host=server_3`) 和多維度 (`host=server_3`、`service=auth`) 實體值。您也可以加入預先篩選之儀表板的連結，以加快分級處理。


## 範例警示通知

下列範例顯示當異常超出定義的閾值時，監視器所產生的範例警示電子郵件。在此情況下，監視器正在追蹤高基數偵測器，並已針對特定實體 (`host = server_3`) 觸發警示：

```md
Monitor **ad-monitor** entered **ALERT** state — please investigate.

Trigger    : ad-trigger
Severity   : 1
Time range : 2025-10-01T23:42:33.699Z → 2025-10-01T23:44:33.699Z UTC

Entity
  • host = server_3
```