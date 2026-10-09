---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Monitor API
parent: Threat intelligence APIs
grand_parent: Threat intelligence
nav_order: 35
---

# Monitor API

您可以使用威脅情報 Monitor API 來建立、搜尋及更新威脅情報摘要的[監視器]({{site.url}}{{site.baseurl}}/observing-your-data/alerting/monitors/)。


---
## 建立或更新威脅情報監視器

建立或更新威脅情報監視器。

### 端點

`POST` 方法會建立新的監視器。`PUT` 方法會更新監視器。

```json
POST _plugins/_security_analytics/threat_intel/monitors
PUT _plugins/_security_analytics/threat_intel/monitors/{monitor_id}
```

### 請求本文欄位

您可以在請求本文中指定下列欄位。

| 欄位  | 類型 | 說明  |
| :--- |  :---  | :--- |
| `name`  | 字串  | 監視器的名稱。必要。 |
| `schedule`  | 物件  | 決定監視器執行頻率的排程。必要。  |
| `schedule.period` | 物件  | 排程頻率的相關資訊。必要。  |
| `schedule.period.interval`   | 整數 | 監視器執行的間隔。必要。   |
| `schedule.period.unit`   | 字串  | 間隔的時間單位。  |
| `enabled` | 物件  | 建立監視器之使用者的相關資訊。必要。    |
| `user.backend_roles`   | 陣列   | 與使用者相關聯的後端角色。選用。  |
| `user.roles`   | 陣列   | 與使用者相關聯的角色。選用。 |
| `user.custom_attribute_names`   | 陣列   | 與使用者相關聯的自訂屬性名稱。選用。   |
| `user.user_requested_tenant`   | 字串  | 使用者要求的租用戶。選用。   |
| `indices`   | 陣列   | 用於監視器的記錄資料來源。必要。  |
| `per_ioc_type_scan_input_list`  | 陣列   | 要根據入侵指標 (IOC) 類型掃描的輸入清單。必要。   |
| `per_ioc_type_scan_input_list.ioc_type`   | 字串  | IOC 類型 (例如雜湊)。必要。  |
| `per_ioc_type_scan_input_list.index_to_fields_map`  | 物件  |包含指定 IOC 類型值的索引欄位對應。必要。 |
| `per_ioc_type_scan_input_list.index_to_fields_map.<index>` | 陣列   | 指定索引中包含的欄位清單。必要。   |
| `triggers`  | 陣列   | 警示的觸發程序設定。必要。   |
| `triggers.data_sources`   | 陣列   | 與觸發程序相關聯的資料來源清單。必要。  |
| `triggers.name`  | 字串  | 觸發程序的名稱。必要。  |
| `triggers.severity`  | 字串  | 觸發程序的嚴重性層級 (例如高、中或低)。必要。  |

### 範例請求

下列小節提供 Monitor API 的範例請求。


#### 建立監視器

```json
{
    "name": "Threat intel monitor",
    "schedule": {
        "period": {
            "interval": 1,
            "unit": "MINUTES"
        }
    },
    "enabled": false,
    "user": {
        "name": "",
        "backend_roles": [],
        "roles": [],
        "custom_attribute_names": [],
        "user_requested_tenant": null
    },
    "indices": [
        "windows"
    ],
    "per_ioc_type_scan_input_list": [
        {
            "ioc_type": "hashes",
            "index_to_fields_map": {
                "windows": [
                    "file_hash"
                ]
            }
        }
    ],
  "triggers": [
        {
            "data_sources": [
                "windows",
                "random"
            ],
            "name": "regwarg",
            "severity": "high"
        }
    ]
}
```

### 更新監視器

```json
{
    "name": "Threat intel monitor",
    "schedule": {
        "period": {
            "interval": 1,
            "unit": "MINUTES"
        }
    },
    "enabled": false,
    "user": {
        "name": "",
        "backend_roles": [],
        "roles": [],
        "custom_attribute_names": [],
        "user_requested_tenant": null
    },
    "indices": [
        "windows"
    ],
    "per_ioc_type_scan_input_list": [
        {
            "ioc_type": "hashes",
            "index_to_fields_map": {
                "windows": [
                    "file_hash"
                ]
            }
        }
    ],
  "triggers": [
        {
            "data_sources": [
                "windows",
                "random"
            ],
            "name": "regwarg",
            "severity": "high"
        }
    ]
}
```


### 範例回應

```json
{
    "id": "B8p88ZAB1vBjq44wkjEy",
    "name": 1,
    "seq_no": 0,
    "primary_term": 1,
    "monitor": {
        "id": "B8p88ZAB1vBjq44wkjEy",
        "name": "Threat intel monitor",
        "per_ioc_type_scan_input_list": [
            {
                "ioc_type": "hashes",
                "index_to_fields_map": {
                    "windows": [
                        "file_hash"
                    ]
                }
            }
        ],
        "schedule": {
            "period": {
                "interval": 1,
                "unit": "MINUTES"
            }
        },
        "enabled": false,
        "user": {
            "name": "",
            "backend_roles": [],
            "roles": [],
            "custom_attribute_names": [],
            "user_requested_tenant": null
        },
        "indices": [
            "windows"
        ],
        "triggers": [
            {
                "data_sources": [
                    "windows",
                    "random"
                ],
                "ioc_types": [],
                "actions": [],
                "id": "afdd80cc-a669-4487-98a0-d84bea8e1e39",
                "name": "regwarg",
                "severity": "high"
            }
        ]
    }
}
```
---

## 刪除監視器

刪除現有的威脅情報監視器。

### 端點

```json
DELETE /_plugins/_security_analytics/threat_intel/monitors/{monitor_id}
```

### 範例請求

```json
DELETE /_plugins/_security_analytics/threat_intel/monitors/B8p88ZAB1vBjq44wkjEy
```
{% include copy-curl.html %}

### 範例回應

```json
{
  "_id" : "B8p88ZAB1vBjq44wkjEy",
  "_version" : 1
}
```

## 搜尋監視器

使用查詢搜尋現有的監視器。請求本文需要搜尋查詢。如需查詢選項，請參閱 [Query DSL]({{site.url}}{{site.baseurl}}/query-dsl/)。
 
### 範例請求

下列範例請求使用符合監視器 ID 的 match 查詢來搜尋監視器：

```json
POST /_plugins/_security_analytics/detectors/_search
{
    "query": {
        "match": {
            "_id": "HMqq_5AB1vBjq44wpTIN"
        }
    }
}
```
{% include copy-curl.html %}

### 範例回應

```json
{
  "took": 11,
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
    "max_score": 2.0,
    "hits": [
      {
        "_index": ".opendistro-alerting-config",
        "_id": "HMqq_5AB1vBjq44wpTIN",
        "_version": 1,
        "_seq_no": 8,
        "_primary_term": 1,
        "_score": 2.0,
        "_source": {
          "id": "HMqq_5AB1vBjq44wpTIN",
          "name": "Threat intel monitor",
          "per_ioc_type_scan_input_list": [
            {
              "ioc_type": "hashes",
              "index_to_fields_map": {
                "windows": [
                  "file_hash"
                ]
              }
            }
          ],
          "schedule": {
            "period": {
              "interval": 1,
              "unit": "MINUTES"
            }
          },
          "enabled": false,
          "user": {
            "name": "",
            "backend_roles": [],
            "roles": [],
            "custom_attribute_names": [],
            "user_requested_tenant": null
          },
          "indices": [
            "windows"
          ],
          "triggers": [
            {
              "data_sources": [
                "windows",
                "random"
              ],
              "ioc_types": [],
              "actions": [],
              "id": "63426758-c82d-4c87-a52c-f86ee6a8a06d",
              "name": "regwarg",
              "severity": "high"
            }
          ]
        }
      }
    ]
  }
}
```