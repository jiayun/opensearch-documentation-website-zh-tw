---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "偵測器 API"
parent: Security Analytics APIs
nav_order: 35
---

# 偵測器 API

下列 API 可用於多項與偵測器相關的工作，從建立偵測器到更新與搜尋偵測器。許多 API 呼叫會在請求中使用偵測器 ID，可透過 [Search detector API](#search-detector) 取得。

---
## 建立偵測器

建立新的偵測器。

```json
POST _plugins/_security_analytics/detectors
```

### 請求本文欄位

建立偵測器時，您可以指定下列欄位。

欄位 | 類型 | 說明
:--- | :--- |:--- |
`enabled` | 布林值 | 將偵測器設為啟用 (true) 或停用 (false)。建立新偵測器時預設為 `true`。必要。
`name` | 字串 | 偵測器的名稱。名稱只能由大小寫字母、數字 0--9、連字號、空格與底線組成。請使用 5--50 個字元。必要。
`detector_type` | 字串 | 定義偵測器的記錄檔類型。選項包括 `linux`、`network`、`windows`、`ad_ldap`、`apache_access`、`cloudtrail`、`dns` 與 `s3`。必要。
`schedule` | 物件 | 決定偵測器執行頻率的排程。關於在 API 中指定固定間隔的資訊，請參閱 [Cron 運算式]({{site.url}}{{site.baseurl}}/api-reference/common-parameters/#cron-expressions)。
`schedule.period` | 物件 | 排程頻率的詳細資訊。
`schedule.period.interval` | 整數 | 偵測器的執行間隔。
`schedule.period.unit` | 字串 | 間隔的時間單位。
`inputs` | 物件 | 偵測器的輸入。
`inputs.detector_input` | 陣列 | 包含用於建立偵測器的索引與定義的陣列。偵測器僅允許一個記錄資料來源。
`inputs.detector_input.description` | 字串 | 偵測器的描述。選用。
`inputs.detector_input.custom_rules` | 陣列 | 自訂規則的偵測器輸入。偵測器必須至少指定一條規則。若已指定預先封裝的規則，則為選用。
`inputs.detector_input.custom_rules.id` | 字串 | 使用者為自訂規則產生的有效規則 ID。有效規則的格式為全域唯一識別碼 (UUID)。更多資訊請參閱 [通用唯一識別碼](https://en.wikipedia.org/wiki/Universally_unique_identifier)。
`inputs.detector_input.indices` | 陣列 | 偵測器使用的記錄資料來源，可以是索引名稱或索引模式。僅支援一個項目。必要。
`inputs.detector_input.pre_packaged_rules` | 陣列 | 預先封裝規則 (相對於自訂規則) 的偵測器輸入。偵測器必須至少指定一條規則。若已指定自訂規則，則為選用。
`inputs.detector_input.pre_packaged_rules.id` | 字串 | 預先封裝規則的規則 ID。關於使用 API 搜尋規則並在結果中取得規則 ID 的資訊，請參閱 [搜尋預先封裝的規則]({{site.url}}{{site.baseurl}}/security-analytics/api-tools/rule-api/#search-pre-packaged-rules)。
`triggers` | 陣列 | 警示的觸發設定。
`triggers.ids` | 陣列 | 成為觸發條件一部分的規則 ID 清單。
`triggers.tags` | 陣列 | 標籤在安全性規則中指定。之後可選取標籤並套用至警示觸發條件，以聚焦警示的觸發條件。關於如何在 Sigma 規則中使用標籤的範例，請參閱 Sigma 的 [規則建立指南](https://github.com/SigmaHQ/sigma/wiki/Rule-Creation-Guide#tags)。
`triggers.id` | 字串 | 觸發條件的唯一 ID。
`triggers.sev_levels` | 陣列 | Sigma 規則嚴重性等級：`informational`；`low`；`medium`；`high`；`criticial`。請參閱 Sigma 規則建立指南中的 [等級](https://github.com/SigmaHQ/sigma/wiki/Rule-Creation-Guide#level)。
`triggers.name` | 字串 | 觸發條件的名稱。名稱只能由大小寫字母、數字 0--9、連字號、空格與底線組成。請使用 5--50 個字元。必要。
`triggers.severity` | 整數 | 以整數表示的觸發條件嚴重性等級：1 = 最高；2 = 高；3 = 中；4 = 低；5 = 最低。觸發條件嚴重性是警示定義的一部分。
`triggers.actions` | 物件 | 當符合觸發條件時，動作會傳送通知。選用，因為警示不一定需要通知訊息。
`triggers.actions.id` | 字串 | 動作的唯一 ID。由使用者產生。
`triggers.actions.destination_id` | 字串 | 通知目的地的唯一 ID。由使用者產生。 
`triggers.actions.subject_template` | 物件 | 包含通知訊息主旨欄位的資訊。選用。
`triggers.actions.subject_template.source` | 字串 | 通知訊息的主旨。
`triggers.actions.subject_template.lang` | 字串 | 用於定義主旨的指令碼語言。必須是 Mustache。關於範本的更多資訊，請參閱 [Mustache 手冊](https://mustache.github.io/mustache.5.html)。
`triggers.actions.name` | 字串 | 觸發警示的名稱。名稱只能由大小寫字母、數字 0--9、連字號、空格與底線組成。請使用 5--50 個字元。
`triggers.actions.message_template` | 字串 | 包含通知訊息內文的資訊。選用。
`triggers.actions.message_template.source` | 字串 | 通知訊息的內文。
`triggers.actions.message_template.lang` | 字串 | 用於定義訊息的指令碼語言。必須是 `Mustache`。
`triggers.actions.throttle_enabled` | 布林值 | 啟用警示通知的節流。選用。預設為 `false`。
`triggers.actions.throttle` | 物件 | 節流可限制您在特定時間範圍內收到的通知數量。
`triggers.actions.throttle.unit` | 字串 | 節流的時間單位。
`triggers.actions.throttle.value` | 整數 | 時間單位的值。

### 請求範例

```json
POST _plugins/_security_analytics/detectors
{
  "enabled": true,
  "schedule": {
    "period": {
      "interval": 1,
      "unit": "MINUTES"
    }
  },
  "detector_type": "WINDOWS",
  "type": "detector",
  "inputs": [
    {
      "detector_input": {
        "description": "windows detector for security analytics",
        "custom_rules": [
          {
            "id": "bc2RB4QBrbtylUb_1Pbm"
          }
        ],
        "indices": [
          "windows"
        ],
        "pre_packaged_rules": [
          {
            "id": "06724a9a-52fc-11ed-bdc3-0242ac120002"
          }
        ]
      }
    }
  ],
  "triggers": [
    {
      "ids": [
        "06724a9a-52fc-11ed-bdc3-0242ac120002"
      ],
      "types": [],
      "tags": [
        "attack.defense_evasion"
      ],
      "severity": "1",
      "actions": [{
          "id": "hVTLkZYzlA",
          "destination_id": "6r8ZBoQBKW_6dKriacQb",
          "subject_template": {
            "source": "Trigger: {{ctx.trigger.name}}",
            "lang": "mustache"
          },
          "name": "hello_world",
          "throttle_enabled": false,
          "message_template": {
            "source": "Detector {{ctx.detector.name}} just entered alert status. Please investigate the issue." +
            "- Trigger: {{ctx.trigger.name}}" +
            "- Severity: {{ctx.trigger.severity}}",
            "lang": "mustache"
          },
          "throttle": {
            "unit": "MINUTES",
            "value": 108
          }
        }
      ],
      "id": "8qhrBoQBYK1JzUUDzH-N",
      "sev_levels": [],
      "name": "test-trigger"
    }
  ],
  "name": "nbReFCjlfn"
}
```
{% include copy-curl.html %}

### 回應範例

```json
{
    "_id": "dc2VB4QBrbtylUb_Hfa3",
    "_version": 1,
    "detector": {
        "name": "nbReFCjlfn",
        "detector_type": "windows",
        "enabled": true,
        "schedule": {
            "period": {
                "interval": 1,
                "unit": "MINUTES"
            }
        },
        "inputs": [
            {
                "detector_input": {
                    "description": "windows detector for security analytics",
                    "indices": [
                        "windows"
                    ],
                    "custom_rules": [
                        {
                            "id": "bc2RB4QBrbtylUb_1Pbm"
                        }
                    ],
                    "pre_packaged_rules": [
                        {
                            "id": "06724a9a-52fc-11ed-bdc3-0242ac120002"
                        }
                    ]
                }
            }
        ],
        "triggers": [
            {
                "id": "8qhrBoQBYK1JzUUDzH-N",
                "name": "test-trigger",
                "severity": "1",
                "types": [],
                "ids": [
                    "06724a9a-52fc-11ed-bdc3-0242ac120002"
                ],
                "sev_levels": [],
                "tags": [
                    "attack.defense_evasion"
                ],
                "actions": [
                    {
                        "id": "hVTLkZYzlA",
                        "name": "hello_world",
                        "destination_id": "6r8ZBoQBKW_6dKriacQb",
                        "message_template": {
                            "source": "Trigger: {{ctx.trigger.name}}",
                            "lang": "mustache"
                        },
                        "throttle_enabled": false,
                        "subject_template": {
                            "source": "Detector {{ctx.detector.name}} just entered alert status. Please investigate the issue." +
                    "- Trigger: {{ctx.trigger.name}}" +
                    "- Severity: {{ctx.trigger.severity}}",
                            "lang": "mustache"
                        },
                        "throttle": {
                            "value": 108,
                            "unit": "MINUTES"
                        }
                    }
                ]
            }
        ],
        "last_update_time": "2022-10-24T01:22:03.738379671Z",
        "enabled_time": "2022-10-24T01:22:03.738376103Z"
    }
}
```

---
## 更新偵測器

更新偵測器定義。需要使用偵測器 ID 來指定偵測器。

```json
PUT /_plugins/_security_analytics/detectors/{detector_Id}
```

### 請求本文欄位

更新偵測器時，您可以指定下列欄位。

欄位 | 類型 | 說明
:--- | :--- |:--- |
`detector_type` | 字串 | 定義偵測器的記錄類型。選項包括 `linux`、`network`、`windows`、`ad_ldap`、`apache_access`、`cloudtrail`、`dns` 和 `s3`。
`name` | 字串 | 偵測器的名稱。名稱只能包含大小寫字母、數字 0--9、連字號、空格和底線。請使用 5--50 個字元。必要。
`enabled` | 布林值 | 將偵測器設定為啟用 (true) 或停用 (false)。
`schedule.period.interval` | 整數 | 偵測器的執行間隔。
`schedule.period.unit` | 字串 | 間隔的時間單位。
`inputs.input.description` | 字串 | 偵測器的描述。
`inputs.input.indices` | 陣列 | 偵測器使用的記錄資料來源。僅允許一個來源。
`inputs.input.rules.id` | 陣列 | 偵測器定義的安全性規則清單。
`triggers.sev_levels` | 陣列 | Sigma 規則嚴重性等級：`informational`；`low`；`medium`；`high`；`criticial`。請參閱 Sigma 規則建立指南中的 [等級](https://github.com/SigmaHQ/sigma/wiki/Rule-Creation-Guide#level)。
`triggers.tags` | 陣列 | 標籤在安全性規則中指定。之後可以選取標籤並套用至警示觸發條件，以聚焦警示的觸發條件。請參閱 Sigma 的 [規則建立指南](https://github.com/SigmaHQ/sigma/wiki/Rule-Creation-Guide#tags) 中如何在 Sigma 規則中使用標籤的範例。
`triggers.actions` | 物件 | 當符合觸發條件時，動作會傳送通知。請參閱 [建立偵測器]({{site.url}}{{site.baseurl}}/security-analytics/api-tools/detector-api/#create-detector) 的觸發動作。


### 請求範例

```json
PUT /_plugins/_security_analytics/detectors/J1RX1IMByX0LvTiGTddR
{
  "type": "detector",
  "detector_type": "windows",
  "name": "windows_detector",
  "enabled": true,
  "createdBy": "chip",
  "schedule": {
    "period": {
      "interval": 1,
      "unit": "MINUTES"
    }
  },
  "inputs": [
    {
      "input": {
        "description": "windows detector for security analytics",
        "indices": [
          "windows"
        ],
        "custom_rules": [],
        "pre_packaged_rules": [
          {
            "id": "73a883d0-0348-4be4-a8d8-51031c2564f8"
          },
          {
            "id": "1a4bd6e3-4c6e-405d-a9a3-53a116e341d4"
          }
        ]
      }
    }
  ],
  "triggers": [
    {
      "sev_levels": [],
      "tags": [],
      "actions": [],
      "types": [
        "windows"
      ],
      "name": "test-trigger",
      "id": "fyAy1IMBK2A1DZyOuW_b"
    }
  ]
}
```
{% include copy-curl.html %}

### 回應範例

```json
{
    "_id": "J1RX1IMByX0LvTiGTddR",
    "_version": 1,
    "detector": {
        "name": "windows_detector",
        "detector_type": "windows",
        "enabled": true,
        "schedule": {
            "period": {
                "interval": 1,
                "unit": "MINUTES"
            }
        },
        "inputs": [
            {
                "detector_input": {
                    "description": "windows detector for security analytics",
                    "indices": [
                        "windows"
                    ],
                    "rules": [
                        {
                            "id": "LFRY1IMByX0LvTiGZtfh"
                        }
                    ]
                }
            }
        ],
        "triggers": [],
        "last_update_time": "2022-10-14T02:36:32.909581688Z",
        "enabled_time": "2022-10-14T02:33:34.197Z"
    }
}
```

#### 回應本文欄位

欄位 | 類型 | 說明
:--- | :--- |:--- |
`_version` | 字串 | 此次更新的版本號碼。
`detector.last_update_time` | 字串 | 上次更新的日期與時間。
`detector.enabled_time` | 字串 | 偵測器上次啟用的日期與時間。

---
## 刪除偵測器

使用偵測器 ID 刪除偵測器。

### 端點

```json
DELETE /_plugins/_security_analytics/detectors/IJAXz4QBrmVplM4JYxx_
```

### 請求範例

```json
DELETE /_plugins/_security_analytics/detectors/<detector Id>
```
{% include copy-curl.html %}

### 回應範例

```json
{
  "_id" : "IJAXz4QBrmVplM4JYxx_",
  "_version" : 1
}
```

---
## 取得偵測器

使用偵測器 ID 擷取偵測器詳細資訊。

### 端點

```json
GET /_plugins/_security_analytics/detectors/x-dwFIYBT6_n8WeuQjo4
```

### 請求範例

```json
GET /_plugins/_security_analytics/detectors/<detector Id>
```
{% include copy-curl.html %}

### 範例回應

```json
{
  "_id" : "x-dwFIYBT6_n8WeuQjo4",
  "_version" : 1,
  "detector" : {
    "name" : "DetectorTest1",
    "detector_type" : "windows",
    "enabled" : true,
    "schedule" : {
      "period" : {
        "interval" : 1,
        "unit" : "MINUTES"
      }
    },
    "inputs" : [
      {
        "detector_input" : {
          "description" : "Test and delete",
          "indices" : [
            "windows1"
          ],
          "custom_rules" : [ ],
          "pre_packaged_rules" : [
            {
              "id" : "847def9e-924d-4e90-b7c4-5f581395a2b4"
            }
          ]
        }
      }
    ],
    "last_update_time" : "2023-02-02T23:22:26.454Z",
    "enabled_time" : "2023-02-02T23:22:26.454Z"
  }
}
```

---
## 搜尋偵測器

依偵測器 ID、偵測器名稱或偵測器類型搜尋偵測器相符項目。

### 請求本文欄位

欄位 | 類型 | 說明
:--- | :--- |:--- |
`_id` | 字串 | 更新的版本號碼。
`detector.name` | 字串 | 偵測器的名稱。
`detector_type` | 字串 | 偵測器的記錄類型。選項為 `linux`、`network`、`windows`、`ad_ldap`、`apache_access`、`cloudtrail`、`dns` 及 `s3`。

### 範例請求

**偵測器 ID**
```json
POST /_plugins/_security_analytics/detectors/_search
{
    "query": {
        "match": {
            "_id": "MFRg1IMByX0LvTiGHtcN"
        }
    }
}
```
{% include copy-curl.html %}

**偵測器名稱**
```json
POST /_plugins/_security_analytics/detectors/_search
{
  "size": 30,  
  "query": {
    "nested": {
      "path": "detector",
      "query": {
        "bool": {
          "must": [
            { "match": {"detector.name": "DetectorTest1"} }
          ]
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

### 範例回應

```json
{
  "took" : 0,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 1,
      "relation" : "eq"
    },
    "max_score" : 3.671739,
    "hits" : [
      {
        "_index" : ".opensearch-sap-detectors-config",
        "_id" : "x-dwFIYBT6_n8WeuQjo4",
        "_version" : 1,
        "_seq_no" : 76,
        "_primary_term" : 17,
        "_score" : 3.671739,
        "_source" : {
          "type" : "detector",
          "name" : "DetectorTest1",
          "detector_type" : "windows",
          "enabled" : true,
          "enabled_time" : 1675380146454,
          "schedule" : {
            "period" : {
              "interval" : 1,
              "unit" : "MINUTES"
            }
          },
          "inputs" : [
            {
              "detector_input" : {
                "description" : "Test and delete",
                "indices" : [
                  "windows1"
                ],
                "custom_rules" : [ ],
                "pre_packaged_rules" : [
                  {
                    "id" : "847def9e-924d-4e90-b7c4-5f581395a2b4"
                  }
                ]
              }
            }
          ],
          "triggers" : [
            {
              "id" : "w-dwFIYBT6_n8WeuQToW",
              "name" : "trigger 1",
              "severity" : "1",
              "types" : [
                "windows"
              ],
              "ids" : [
                "847def9e-924d-4e90-b7c4-5f581395a2b4"
              ],
              "sev_levels" : [
                "critical"
              ],
              "tags" : [
                "attack.t1003.002"
              ],
              "actions" : [
                {
                  "id" : "",
                  "name" : "Triggered alert condition:  - Severity: 1 (Highest) - Threat detector: DetectorTest1",
                  "destination_id" : "",
                  "message_template" : {
                    "source" : """Triggered alert condition: 
Severity: 1 (Highest)
Threat detector: DetectorTest1
Description: Test and delete
Detector data sources:
  windows1""",
                    "lang" : "mustache"
                  },
                  "throttle_enabled" : false,
                  "subject_template" : {
                    "source" : "Triggered alert condition:  - Severity: 1 (Highest) - Threat detector: DetectorTest1",
                    "lang" : "mustache"
                  },
                  "throttle" : {
                    "value" : 10,
                    "unit" : "MINUTES"
                  }
                }
              ]
            }
          ],
          "last_update_time" : 1675380146454,
          "monitor_id" : [
            "xOdwFIYBT6_n8WeuQToa"
          ],
          "bucket_monitor_id_rule_id" : {
            "-1" : "xOdwFIYBT6_n8WeuQToa"
          },
          "rule_topic_index" : ".opensearch-sap-windows-detectors-queries",
          "alert_index" : ".opensearch-sap-windows-alerts",
          "alert_history_index" : ".opensearch-sap-windows-alerts-history",
          "alert_history_index_pattern" : "<.opensearch-sap-windows-alerts-history-{now/d}-1>",
          "findings_index" : ".opensearch-sap-windows-findings",
          "findings_index_pattern" : "<.opensearch-sap-windows-findings-{now/d}-1>"
        }
      }
    ]
  }
}
```

