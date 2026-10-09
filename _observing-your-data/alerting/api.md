---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: API
parent: Alerting
nav_order: 15
redirect_from:
  - /monitoring-plugins/alerting/api/
---

# 警示 API

使用警示 API，以程式設計方式建立、更新及管理監視器和警示。如需專門支援複合監視器的 API，請參閱[使用 API 管理複合監視器]({{site.url}}{{site.baseurl}}/observing-your-data/alerting/composite-monitors/#managing-composite-monitors-with-the-api)。

## 建立查詢層級監視器

查詢層級監視器會執行查詢，並判斷結果是否應觸發警示。查詢層級監視器一次只能觸發一個警示。如需查詢層級與桶 (bucket) 層級監視器的詳細資訊，請參閱[建立監視器]({{site.url}}{{site.baseurl}}/monitoring-plugins/alerting/monitors/)。

#### 請求範例
```json
POST _plugins/_alerting/monitors
{
  "type": "monitor",
  "name": "test-monitor",
  "monitor_type": "query_level_monitor",
  "enabled": true,
  "schedule": {
    "period": {
      "interval": 1,
      "unit": "MINUTES"
    }
  },
  "inputs": [{
    "search": {
      "indices": ["movies"],
      "query": {
        "size": 0,
        "aggregations": {},
        "query": {
          "bool": {
            "filter": {
              "range": {
                "@timestamp": {
                  "gte": {% raw %}"{{period_end}}||-1h"{% endraw %},
                  "lte": {% raw %}"{{period_end}}"{% endraw %},
                  "format": "epoch_millis"
                }
              }
            }
          }
        }
      }
    }
  }],
  "triggers": [{
    "name": "test-trigger",
    "severity": "1",
    "condition": {
      "script": {
        "source": "ctx.results[0].hits.total.value > 0",
        "lang": "painless"
      }
    },
    "actions": [{
      "name": "test-action",
      "destination_id": "ld7912sBlQ5JUWWFThoW",
      "message_template": {
        "source": "This is my message body."
      },
      "throttle_enabled": true,
      "throttle": {
        "value": 27,
        "unit": "MINUTES"
      },
      "subject_template": {
        "source": "TheSubject"
      }
    }]
  }]
}
```
{% include copy-curl.html %}


如果您的目的地使用自訂 webhook，且需要在訊息本文中嵌入 JSON，請務必將引號逸出：

```json
{
  "message_template": {
    {% raw %}"source": "{ \"text\": \"Monitor {{ctx.monitor.name}} just entered alert status. Please investigate the issue. - Trigger: {{ctx.trigger.name}} - Severity: {{ctx.trigger.severity}} - Period start: {{ctx.periodStart}} - Period end: {{ctx.periodEnd}}\" }"{% endraw %}
  }
}
```
{% include copy-curl.html %}


若要指定後端角色，您可以選擇在建立監視器請求的底部加入 `rbac_roles` 參數及後端角色名稱。

下列請求會建立查詢層級監視器，並提供兩個後端角色：`role1` 和 `role2`。請求底部的區段顯示以此語法指定角色的那一行：`"rbac_roles": ["role1", "role2"]`。如需了解如何使用後端角色限制存取，請參閱[（進階）依後端角色限制存取]({{site.url}}{{site.baseurl}}/monitoring-plugins/alerting/security/#advanced-limit-access-by-backend-role)。

#### 請求範例
```json
POST _plugins/_alerting/monitors
{
  "type": "monitor",
  "name": "test-monitor",
  "monitor_type": "query_level_monitor",
  "enabled": true,
  "schedule": {
    "period": {
      "interval": 1,
      "unit": "MINUTES"
    }
  },
  "inputs": [{
    "search": {
      "indices": ["movies"],
      "query": {
        "size": 0,
        "aggregations": {},
        "query": {
          "bool": {
            "filter": {
              "range": {
                "@timestamp": {
                  "gte": "{{period_end}}||-1h",
                  "lte": "{{period_end}}",
                  "format": "epoch_millis"
                }
              }
            }
          }
        }
      }
    }
  }],
  "triggers": [{
    "name": "test-trigger",
    "severity": "1",
    "condition": {
      "script": {
        "source": "ctx.results[0].hits.total.value > 0",
        "lang": "painless"
      }
    },
    "actions": [{
      "name": "test-action",
      "destination_id": "ld7912sBlQ5JUWWFThoW",
      "message_template": {
        "source": "This is my message body."
      },
      "throttle_enabled": true,
      "throttle": {
        "value": 27,
        "unit": "MINUTES"
      },
      "subject_template": {
        "source": "TheSubject"
      }
    }]
  }],
  "rbac_roles": ["role1", "role2"]
}
```
{% include copy-curl.html %}


<details markdown="block">
  <summary>
    選取以展開回應範例
  </summary>
  {: .text-delta}

#### 回應範例
```json
{
  "_id": "vd5k2GsBlQ5JUWWFxhsP",
  "_version": 1,
  "_seq_no": 7,
  "_primary_term": 1,
  "monitor": {
    "type": "monitor",
    "schema_version": 1,
    "name": "test-monitor",
    "enabled": true,
    "enabled_time": 1562703611363,
    "schedule": {
      "period": {
        "interval": 1,
        "unit": "MINUTES"
      }
    },
    "inputs": [{
      "search": {
        "indices": [
          "movies"
        ],
        "query": {
          "size": 0,
          "query": {
            "bool": {
              "filter": [{
                "range": {
                  "@timestamp": {
                    "from": {% raw %}"{{period_end}}||-1h"{% endraw %},
                    "to": {% raw %}"{{period_end}}"{% endraw %},
                    "include_lower": true,
                    "include_upper": true,
                    "format": "epoch_millis",
                    "boost": 1
                  }
                }
              }],
              "adjust_pure_negative": true,
              "boost": 1
            }
          },
          "aggregations": {}
        }
      }
    }],
    "triggers": [{
      "id": "ud5k2GsBlQ5JUWWFxRvi",
      "name": "test-trigger",
      "severity": "1",
      "condition": {
        "script": {
          "source": "ctx.results[0].hits.total.value > 0",
          "lang": "painless"
        }
      },
      "actions": [{
        "id": "ut5k2GsBlQ5JUWWFxRvj",
        "name": "test-action",
        "destination_id": "ld7912sBlQ5JUWWFThoW",
        "message_template": {
          "source": "This is my message body.",
          "lang": "mustache"
        },
        "throttle_enabled": false,
        "subject_template": {
          "source": "Subject",
          "lang": "mustache"
        }
      }]
    }],
    "last_update_time": 1562703611363
  }
}
```
{% include copy-curl.html %}

</details>


若要指定時區，您可以在請求的 `schedule` 區段中加入含有時區名稱的 [cron 運算式]({{site.url}}{{site.baseurl}}/api-reference/common-parameters/#cron-expressions)。下列範例會建立一個監視器，於每月第一天太平洋時間下午 12:10 執行。

#### 請求範例
```json
{
  "type": "monitor",
  "name": "test-monitor",
  "monitor_type": "query_level_monitor",
  "enabled": true,
  "schedule": {
    "cron" : {
        "expression": "10 12 1 * *",
        "timezone": "America/Los_Angeles"
    }
  },
  "inputs": [{
    "search": {
      "indices": ["movies"],
      "query": {
        "size": 0,
        "aggregations": {},
        "query": {
          "bool": {
            "filter": {
              "range": {
                "@timestamp": {
                  "gte": {% raw %}"{{period_end}}||-1h"{% endraw %},
                  "lte": {% raw %}"{{period_end}}"{% endraw %},
                  "format": "epoch_millis"
                }
              }
            }
          }
        }
      }
    }
  }],
  "triggers": [{
    "name": "test-trigger",
    "severity": "1",
    "condition": {
      "script": {
        "source": "ctx.results[0].hits.total.value > 0",
        "lang": "painless"
      }
    },
    "actions": [{
      "name": "test-action",
      "destination_id": "ld7912sBlQ5JUWWFThoW",
      "message_template": {
        "source": "This is a message body."
      },
      "throttle_enabled": true,
      "throttle": {
        "value": 27,
        "unit": "MINUTES"
      },
      "subject_template": {
        "source": "Subject"
      }
    }]
  }]
}
```
{% include copy-curl.html %}


如需完整的時區名稱清單，請參閱 [`tz` 資料庫時區清單](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)。Alerting 外掛程式使用 Java [`TimeZone`](https://docs.oracle.com/en/java/javase/11/docs/api/java.base/java/util/TimeZone.html) 類別，將 [`ZoneId`](https://docs.oracle.com/en/java/javase/11/docs/api/java.base/java/time/ZoneId.html) 轉換為有效的時區。

---

## 桶層級監視器

桶層級監視器會將結果依欄位分類至不同的桶。接著，監視器會以每個桶的結果執行指令碼，並評估是否觸發警示。如需桶層級與查詢層級監視器的詳細資訊，請參閱[建立監視器]({{site.url}}{{site.baseurl}}/monitoring-plugins/alerting/monitors/)。

#### 範例請求
```json
POST _plugins/_alerting/monitors
{
  "type": "monitor",
  "name": "Demo bucket-level monitor",
  "monitor_type": "bucket_level_monitor",
  "enabled": true,
  "schedule": {
    "period": {
      "interval": 1,
      "unit": "MINUTES"
    }
  },
  "inputs": [
    {
      "search": {
        "indices": [
          "movies"
        ],
        "query": {
          "size": 0,
          "query": {
            "bool": {
              "filter": [
                {
                  "range": {
                    "order_date": {
                      "from": {% raw %}"{{period_end}}||-1h"{% endraw %},
                      "to": {% raw %}"{{period_end}}"{% endraw %},
                      "include_lower": true,
                      "include_upper": true,
                      "format": "epoch_millis"
                    }
                  }
                }
              ]
            }
          },
          "aggregations": {
            "composite_agg": {
              "composite": {
                "sources": [
                  {
                    "user": {
                      "terms": {
                        "field": "user"
                      }
                    }
                  }
                ]
              },
              "aggregations": {
                "avg_products_base_price": {
                  "avg": {
                    "field": "products.base_price"
                  }
                }
              }
            }
          }
        }
      }
    }
  ],
  "triggers": [
    {
      "bucket_level_trigger": {
        "name": "test-trigger",
        "severity": "1",
        "condition": {
          "buckets_path": {
            "_count": "_count",
            "avg_products_base_price": "avg_products_base_price"
          },
          "parent_bucket_path": "composite_agg",
          "script": {
            "source": "params._count > 50 || params.avg_products_base_price < 35",
            "lang": "painless"
          }
        },
        "actions": [
          {
            "name": "test-action",
            "destination_id": "E4o5hnsB6KjPKmHtpfCA",
            "message_template": {
              "source": {% raw %}"""Monitor {{ctx.monitor.name}} just entered alert status. Please investigate the issue.   - Trigger: {{ctx.trigger.name}}   - Severity: {{ctx.trigger.severity}}   - Period start: {{ctx.periodStart}}   - Period end: {{ctx.periodEnd}}    - Deduped Alerts:   {{ctx.dedupedAlerts}}     * {{id}} : {{bucket_keys}}   {{ctx.dedupedAlerts}}    - New Alerts:   {{ctx.newAlerts}}     * {{id}} : {{bucket_keys}}   {{ctx.newAlerts}}    - Completed Alerts:   {{ctx.completedAlerts}}     * {{id}} : {{bucket_keys}}   {{ctx.completedAlerts}}"""{% endraw %},
              "lang": "mustache"
            },
            "throttle_enabled": false,
            "throttle": {
              "value": 10,
              "unit": "MINUTES"
            },
            "action_execution_policy": {
              "action_execution_scope": {
                "per_alert": {
                  "actionable_alerts": [
                    "DEDUPED",
                    "NEW"
                  ]
                }
              }
            },
            "subject_template": {
              "source": "The Subject",
              "lang": "mustache"
            }
          }
        ]
      }
    }
  ]
}
```
{% include copy-curl.html %}


<details markdown="block">
  <summary>
    選取以展開範例回應
  </summary>
  {: .text-delta}
 
#### 範例回應
```json
{
  "_id" : "Dfxr63sBwex6DxEhHV5N",
  "_version" : 1,
  "_seq_no" : 3,
  "_primary_term" : 1,
  "monitor" : {
    "type" : "monitor",
    "schema_version" : 4,
    "name" : "Demo a bucket-level monitor",
    "monitor_type" : "bucket_level_monitor",
    "user" : {
      "name" : "",
      "backend_roles" : [ ],
      "roles" : [ ],
      "custom_attribute_names" : [ ],
      "user_requested_tenant" : null
    },
    "enabled" : true,
    "enabled_time" : 1631742270785,
    "schedule" : {
      "period" : {
        "interval" : 1,
        "unit" : "MINUTES"
      }
    },
    "inputs" : [
      {
        "search" : {
          "indices" : [
            "opensearch_dashboards_sample_data_flights"
          ],
          "query" : {
            "size" : 0,
            "query" : {
              "bool" : {
                "filter" : [
                  {
                    "range" : {
                      "order_date" : {
                        "from" : {% raw %}"{{period_end}}||-1h"{% endraw %},
                        "to" : {% raw %}"{{period_end}}"{% endraw %},
                        "include_lower" : true,
                        "include_upper" : true,
                        "format" : "epoch_millis",
                        "boost" : 1.0
                      }
                    }
                  }
                ],
                "adjust_pure_negative" : true,
                "boost" : 1.0
              }
            },
            "aggregations" : {
              "composite_agg" : {
                "composite" : {
                  "size" : 10,
                  "sources" : [
                    {
                      "user" : {
                        "terms" : {
                          "field" : "user",
                          "missing_bucket" : false,
                          "order" : "asc"
                        }
                      }
                    }
                  ]
                },
                "aggregations" : {
                  "avg_products_base_price" : {
                    "avg" : {
                      "field" : "products.base_price"
                    }
                  }
                }
              }
            }
          }
        }
      }
    ],
    "triggers" : [
      {
        "bucket_level_trigger" : {
          "id" : "C_xr63sBwex6DxEhHV5B",
          "name" : "test-trigger",
          "severity" : "1",
          "condition" : {
            "buckets_path" : {
              "_count" : "_count",
              "avg_products_base_price" : "avg_products_base_price"
            },
            "parent_bucket_path" : "composite_agg",
            "script" : {
              "source" : "params._count > 50 || params.avg_products_base_price < 35",
              "lang" : "painless"
            },
            "gap_policy" : "skip"
          },
          "actions" : [
            {
              "id" : "DPxr63sBwex6DxEhHV5B",
              "name" : "test-action",
              "destination_id" : "E4o5hnsB6KjPKmHtpfCA",
              "message_template" : {
                "source" : {% raw %}"Monitor {{ctx.monitor.name}} just entered alert status. Please investigate the issue.   - Trigger: {{ctx.trigger.name}}   - Severity: {{ctx.trigger.severity}}   - Period start: {{ctx.periodStart}}   - Period end: {{ctx.periodEnd}}    - Deduped Alerts:   {{ctx.dedupedAlerts}}     * {{id}} : {{bucket_keys}}   {{ctx.dedupedAlerts}}    - New Alerts:   {{ctx.newAlerts}}     * {{id}} : {{bucket_keys}}   {{ctx.newAlerts}}    - Completed Alerts:   {{ctx.completedAlerts}}     * {{id}} : {{bucket_keys}}   {{ctx.completedAlerts}}"{% endraw %},
                "lang" : "mustache"
              },
              "throttle_enabled" : false,
              "subject_template" : {
                "source" : "The Subject",
                "lang" : "mustache"
              },
              "throttle" : {
                "value" : 10,
                "unit" : "MINUTES"
              },
              "action_execution_policy" : {
                "action_execution_scope" : {
                  "per_alert" : {
                    "actionable_alerts" : [
                      "DEDUPED",
                      "NEW"
                    ]
                  }
                }
              }
            }
          ]
        }
      }
    ],
    "last_update_time" : 1631742270785
  }
}
```
{% include copy-curl.html %}

</details>

---

## 文件層級監視器
於 2.0 版推出
{: .label .label-purple }

文件層級監視器會檢查索引中的個別文件是否符合觸發條件。若符合，監視器會產生警示通知。當您使用文件層級監視器執行查詢時，會針對每個符合觸發條件的文件回傳結果。您可以根據查詢名稱、查詢 ID 或結合多個查詢的標籤來建立觸發條件。

若要進一步瞭解功能類似文件層級監視器 API 的每文件監視器，請參閱[監視器]({{site.url}}{{site.baseurl}}/observing-your-data/alerting/monitors/)。

### 搜尋發現結果索引

您可以使用警示搜尋 API 操作，透過 GET 請求搜尋發現結果索引 `.opensearch-alerting-finding*` 以取得可用的文件發現結果。預設情況下，不含路徑參數的 GET 請求會回傳所有可用的發現結果。

若要擷取所有可用的發現結果，請依照下列方式傳送不含任何路徑參數的 GET 請求：

```json
GET /_plugins/_alerting/findings/_search?
```
{% include copy-curl.html %}

若要擷取單一文件發現項目的中繼資料，您可以依照下列方式以 `findingId` 搜尋該發現結果：

```json
GET /_plugins/_alerting/findings/_search?findingId=gKQhj8WJit3BxjGfiOXC
```
{% include copy-curl.html %}

回應會在 `total_findings` 欄位中回傳個別發現項目的數量。

若要在發現結果搜尋中取得更精確的結果，您可以使用下表定義的任何選用路徑參數。

路徑參數 | 說明 | 用法
:--- | :--- | :---
`findingId` | 發現項目的識別碼。 | 發現 ID 會在初始查詢回應中回傳。
`sortString` | 此欄位指定 Alerting 外掛程式用來排序發現結果的字串。 | 預設值為 `id`。
`sortOrder` | 發現結果清單的排序方式，可為遞增或遞減。 | 使用 `sortOrder=asc` 表示遞增，或 `sortOrder=desc` 表示遞減排序。
`size` | 選用的限制，指定回應中回傳結果的最大數量。 | 沒有最小值或最大值限制。
`startIndex` | 分頁指示器。 | 預設為 `0`。
`searchString` | 您希望在搜尋中回傳的發現結果屬性。 | 若要在特定索引中搜尋，請在請求路徑中指定索引名稱。例如，若要搜尋 `indexABC` 索引中的發現結果，請使用 `searchString=indexABC'。

### 建立文件層級監視器

您可以透過 POST 請求建立文件層級監視器，並在請求本文中提供監視器詳細資訊。至少需要提供以下詳細資訊：使用 `inputs` 欄位指定查詢或依標籤組合的查詢、有效的觸發條件，並在 `action` 欄位中提供通知訊息。

下表提供每個觸發選項的語法。

觸發選項 | 定義 | 語法
:--- | :--- | :---
標籤 | 為套用此標籤之多個查詢所比對到的文件建立警示。如果您依單一標籤將多個查詢分組，則可設定當此標籤名稱回傳結果時觸發警示。| `query[tag=<tag-name>]`
依名稱查詢 | 為具名查詢所比對到或回傳的文件建立警示。 | `query[name=<query-name>]`
依 ID 查詢 | 為指定查詢所回傳的文件建立警示。 | `query[id=<query-id>]`


#### 範例請求
```json
POST _plugins/_alerting/monitors
{
  "type": "monitor",
  "monitor_type": "doc_level_monitor",
  "name": "Example document-level monitor",
  "enabled": true,
  "schedule": {
    "period": {
      "interval": 1,
      "unit": "MINUTES"
    }
  },
  "inputs": [
    {
      "doc_level_input": {
        "description": "Example document-level monitor for audit logs",
        "indices": [
          "audit-logs"
        ],
        "queries": [
        {
            "id": "nKQnFYABit3BxjGfiOXC",
            "name": "sigma-123",
            "query": "region:\"us-west-2\"",
            "tags": [
                "tag1"
            ]
        },
        {
            "id": "gKQnABEJit3BxjGfiOXC",
            "name": "sigma-456",
            "query": "region:\"us-east-1\"",
            "tags": [
                "tag2"
            ]
        },
        {
            "id": "h4J2ABEFNW3vxjGfiOXC",
            "name": "sigma-789",
            "query": "message:\"This is a SEPARATE error from IAD region\"",
            "tags": [
                "tag3"
            ]
        }
    ]
      }
    }
  ],
    "triggers": [ { "document_level_trigger": {
      "name": "test-trigger",
      "severity": "1",
      "condition": {
        "script": {
          "source": "(query[name=sigma-123] || query[tag=tag3]) && query[name=sigma-789]",
          "lang": "painless"
        }
      },
      "actions": [
        {
            "name": "test-action",
            "destination_id": "E4o5hnsB6KjPKmHtpfCA",
            "message_template": {
                "source": {% raw %}"""Monitor  just entered alert status. Please investigate the issue. Related Finding Ids: {{ctx.alerts.0.finding_ids}}, Related Document Ids: {{ctx.alerts.0.related_doc_ids}}"""{% endraw %},
                "lang": "mustache"
            },
            "action_execution_policy": {
                "action_execution_scope": {
                    "per_alert": {
                        "actionable_alerts": []
                    }
                }
            },
            "subject_template": {
                "source": "The Subject",
                "lang": "mustache"
            }
         }
      ]
  }}]
}

```
{% include copy-curl.html %}


### 限制

如果您在索引正在重建索引時執行文件層級查詢，API 回應將不會回傳重建索引後的結果。若要取得更新，請等待重建索引程序完成後，再重新執行查詢。

---

## 更新監視器

更新監視器時，您可以選擇性地包含 `if_seq_no` 和 `if_primary_term` 查詢參數，例如 `?if_seq_no=3&if_primary_term=1`。如果這些數字與現有監視器不符，或該監視器不存在，Alerting 外掛程式會擲回錯誤。OpenSearch 會自動遞增版本號碼和序號（請參閱範例回應）。

#### 範例請求
```json
PUT _plugins/_alerting/monitors/{monitor_id}
{
  "type": "monitor",
  "name": "test-monitor",
  "enabled": true,
  "enabled_time": 1551466220455,
  "schedule": {
    "period": {
      "interval": 1,
      "unit": "MINUTES"
    }
  },
  "inputs": [{
    "search": {
      "indices": [
        "*"
      ],
      "query": {
        "query": {
          "match_all": {
            "boost": 1
          }
        }
      }
    }
  }],
  "triggers": [{
    "id": "StaeOmkBC25HCRGmL_y-",
    "name": "test-trigger",
    "severity": "1",
    "condition": {
      "script": {
        "source": "return true",
        "lang": "painless"
      }
    },
    "actions": [{
      "name": "test-action",
      "destination_id": "RtaaOmkBC25HCRGm0fxi",
      "subject_template": {
        "source": "My Message Subject",
        "lang": "mustache"
      },
      "message_template": {
        "source": "This is my message body.",
        "lang": "mustache"
      }
    }]
  }],
  "last_update_time": 1551466639295
}
```
{% include copy-curl.html %}


<details markdown="block">
  <summary>
    選取以展開範例回應
  </summary>
  {: .text-delta}

#### 回應範例
```json
{
  "_id": "Q9aXOmkBC25HCRGmzfw-",
  "_version": 4,
  "_seq_no": 4,
  "_primary_term": 1,
  "monitor": {
    "type": "monitor",
    "name": "test-monitor",
    "enabled": true,
    "enabled_time": 1551466220455,
    "schedule": {
      "period": {
        "interval": 1,
        "unit": "MINUTES"
      }
    },
    "inputs": [{
      "search": {
        "indices": [
          "*"
        ],
        "query": {
          "query": {
            "match_all": {
              "boost": 1
            }
          }
        }
      }
    }],
    "triggers": [{
      "id": "StaeOmkBC25HCRGmL_y-",
      "name": "test-trigger",
      "severity": "1",
      "condition": {
        "script": {
          "source": "return true",
          "lang": "painless"
        }
      },
      "actions": [{
        "name": "test-action",
        "destination_id": "RtaaOmkBC25HCRGm0fxi",
        "subject_template": {
          "source": "My Message Subject",
          "lang": "mustache"
        },
        "message_template": {
          "source": "This is my message body.",
          "lang": "mustache"
        }
      }]
    }],
    "last_update_time": 1551466761596
  }
}
```
{% include copy-curl.html %}

</details>

---

## 取得監視器

使用下列請求擷取特定監視器的詳細資訊。

#### 請求範例
```
GET _plugins/_alerting/monitors/{monitor_id}
```
{% include copy-curl.html %}


<details markdown="block">
  <summary>
    選取以展開回應範例
  </summary>
  {: .text-delta}

#### 回應範例
```json
{
  "_id": "Q9aXOmkBC25HCRGmzfw-",
  "_version": 3,
  "_seq_no": 3,
  "_primary_term": 1,
  "monitor": {
    "type": "monitor",
    "name": "test-monitor",
    "enabled": true,
    "enabled_time": 1551466220455,
    "schedule": {
      "period": {
        "interval": 1,
        "unit": "MINUTES"
      }
    },
    "inputs": [{
      "search": {
        "indices": [
          "*"
        ],
        "query": {
          "query": {
            "match_all": {
              "boost": 1
            }
          }
        }
      }
    }],
    "triggers": [{
      "id": "StaeOmkBC25HCRGmL_y-",
      "name": "test-trigger",
      "severity": "1",
      "condition": {
        "script": {
          "source": "return true",
          "lang": "painless"
        }
      },
      "actions": [{
        "name": "test-action",
        "destination_id": "RtaaOmkBC25HCRGm0fxi",
        "subject_template": {
          "source": "My Message Subject",
          "lang": "mustache"
        },
        "message_template": {
          "source": "This is my message body.",
          "lang": "mustache"
        }
      }]
    }],
    "last_update_time": 1551466639295
  }
}
```
{% include copy-curl.html %}

</details>

---

## 監視器統計資料

傳回警示功能的統計資料。使用 `_plugins/_alerting/stats` 來尋找節點 ID 與指標，然後即可使用這些值進一步深入查詢。

#### 請求範例
```json
GET _plugins/_alerting/stats
GET _plugins/_alerting/stats/{metric}
GET _plugins/_alerting/{node-id}/stats
GET _plugins/_alerting/{node-id}/stats/{metric}
```


<details markdown="block">
  <summary>
    選取以展開回應範例
  </summary>
  {: .text-delta}

#### 回應範例
```json
{
  "_nodes": {
    "total": 9,
    "successful": 9,
    "failed": 0
  },
  "cluster_name": "475300751431:alerting65-dont-delete",
  "plugins.scheduled_jobs.enabled": true,
  "scheduled_job_index_exists": true,
  "scheduled_job_index_status": "green",
  "nodes_on_schedule": 9,
  "nodes_not_on_schedule": 0,
  "nodes": {
    "qWcbKbb-TVyyI-Q7VSeOqA": {
      "name": "qWcbKbb",
      "schedule_status": "green",
      "roles": [
        "MASTER"
      ],
      "job_scheduling_metrics": {
        "last_full_sweep_time_millis": 207017,
        "full_sweep_on_time": true
      },
      "jobs_info": {}
    },
    "Do-DX9ZcS06Y9w1XbSJo1A": {
      "name": "Do-DX9Z",
      "schedule_status": "green",
      "roles": [
        "DATA",
        "INGEST"
      ],
      "job_scheduling_metrics": {
        "last_full_sweep_time_millis": 230516,
        "full_sweep_on_time": true
      },
      "jobs_info": {}
    },
    "n5phkBiYQfS5I0FDzcqjZQ": {
      "name": "n5phkBi",
      "schedule_status": "green",
      "roles": [
        "MASTER"
      ],
      "job_scheduling_metrics": {
        "last_full_sweep_time_millis": 228406,
        "full_sweep_on_time": true
      },
      "jobs_info": {}
    },
    "Tazzo8cQSY-g3vOjgYYLzA": {
      "name": "Tazzo8c",
      "schedule_status": "green",
      "roles": [
        "DATA",
        "INGEST"
      ],
      "job_scheduling_metrics": {
        "last_full_sweep_time_millis": 211722,
        "full_sweep_on_time": true
      },
      "jobs_info": {
        "i-wsFmkB8NzS6aXjQSk0": {
          "last_execution_time": 1550864912882,
          "running_on_time": true
        }
      }
    },
    "Nyf7F8brTOSJuFPXw6CnpA": {
      "name": "Nyf7F8b",
      "schedule_status": "green",
      "roles": [
        "DATA",
        "INGEST"
      ],
      "job_scheduling_metrics": {
        "last_full_sweep_time_millis": 223300,
        "full_sweep_on_time": true
      },
      "jobs_info": {
        "NbpoFmkBeSe-hD59AKgE": {
          "last_execution_time": 1550864928354,
          "running_on_time": true
        },
        "-LlLFmkBeSe-hD59Ydtb": {
          "last_execution_time": 1550864732727,
          "running_on_time": true
        },
        "pBFxFmkBNXkgNmTBaFj1": {
          "last_execution_time": 1550863325024,
          "running_on_time": true
        },
        "hfasEmkBNXkgNmTBrvIW": {
          "last_execution_time": 1550862000001,
          "running_on_time": true
        }
      }
    },
    "oOdJDIBVT5qbbO3d8VLeEw": {
      "name": "oOdJDIB",
      "schedule_status": "green",
      "roles": [
        "DATA",
        "INGEST"
      ],
      "job_scheduling_metrics": {
        "last_full_sweep_time_millis": 227570,
        "full_sweep_on_time": true
      },
      "jobs_info": {
        "4hKRFmkBNXkgNmTBKjYX": {
          "last_execution_time": 1550864806101,
          "running_on_time": true
        }
      }
    },
    "NRDG6JYgR8m0GOZYQ9QGjQ": {
      "name": "NRDG6JY",
      "schedule_status": "green",
      "roles": [
        "MASTER"
      ],
      "job_scheduling_metrics": {
        "last_full_sweep_time_millis": 227652,
        "full_sweep_on_time": true
      },
      "jobs_info": {}
    },
    "URMrXRz3Tm-CB72hlsl93Q": {
      "name": "URMrXRz",
      "schedule_status": "green",
      "roles": [
        "DATA",
        "INGEST"
      ],
      "job_scheduling_metrics": {
        "last_full_sweep_time_millis": 231048,
        "full_sweep_on_time": true
      },
      "jobs_info": {
        "m7uKFmkBeSe-hD59jplP": {
          "running_on_time": true
        }
      }
    },
    "eXgt1k9oTRCLmx2HBGElUw": {
      "name": "eXgt1k9",
      "schedule_status": "green",
      "roles": [
        "DATA",
        "INGEST"
      ],
      "job_scheduling_metrics": {
        "last_full_sweep_time_millis": 229234,
        "full_sweep_on_time": true
      },
      "jobs_info": {
        "wWkFFmkBc2NG-PeLntxk": {
          "running_on_time": true
        },
        "3usNFmkB8NzS6aXjO1Gs": {
          "last_execution_time": 1550863959848,
          "running_on_time": true
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

</details>

---

## 刪除監視器

使用下列請求刪除監視器。

#### 範例請求
```
DELETE _plugins/_alerting/monitors/{monitor_id}
```
{% include copy-curl.html %}


<details markdown="block">
  <summary>
    選取以展開範例回應
  </summary>
  {: .text-delta}
  
#### 範例回應
```json
{
  "_index": ".opensearch-scheduled-jobs",
  "_id": "OYAHOmgBl3cmwnqZl_yH",
  "_version": 2,
  "result": "deleted",
  "forced_refresh": true,
  "_shards": {
    "total": 2,
    "successful": 2,
    "failed": 0
  },
  "_seq_no": 11,
  "_primary_term": 1
}
```
{% include copy-curl.html %}

</details>

---

## 搜尋監視器

使用下列請求，根據特定條件 (例如監視器名稱) 查詢並擷取現有監視器的資訊。

#### 範例請求
```json
GET _plugins/_alerting/monitors/_search
{
  "query": {
    "match" : {
      "monitor.name": "my-monitor-name"
    }
  }
}
```
{% include copy-curl.html %}


<details markdown="block">
  <summary>
    選取以展開範例回應
  </summary>
  {: .text-delta}
  
#### 範例回應
```json
{
  "took": 17,
  "timed_out": false,
  "_shards": {
    "total": 5,
    "successful": 5,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": 1,
    "max_score": 0.6931472,
    "hits": [{
      "_index": ".opensearch-scheduled-jobs",
      "_type": "_doc",
      "_id": "eGQi7GcBRS7-AJEqfAnr",
      "_score": 0.6931472,
      "_source": {
        "type": "monitor",
        "name": "my-monitor-name",
        "enabled": true,
        "enabled_time": 1545854942426,
        "schedule": {
          "period": {
            "interval": 1,
            "unit": "MINUTES"
          }
        },
        "inputs": [{
          "search": {
            "indices": [
              "*"
            ],
            "query": {
              "size": 0,
              "query": {
                "bool": {
                  "filter": [{
                    "range": {
                      "@timestamp": {
                        "from": {% raw %}"{{period_end}}||-1h"{% endraw %},
                        "to": {% raw %}"{{period_end}}"{% endraw %},
                        "include_lower": true,
                        "include_upper": true,
                        "format": "epoch_millis",
                        "boost": 1
                      }
                    }
                  }],
                  "adjust_pure_negative": true,
                  "boost": 1
                }
              },
              "aggregations": {}
            }
          }
        }],
        "triggers": [{
          "id": "Sooi7GcB53a0ewuj_6MH",
          "name": "Over",
          "severity": "1",
          "condition": {
            "script": {
              "source": "_ctx.results[0].hits.total > 400000",
              "lang": "painless"
            }
          },
          "actions": []
        }],
        "last_update_time": 1545854975758
      }
    }]
  }
}
```
{% include copy-curl.html %}

</details>

---

## 執行監視器

您可以在 URL 中加入選用的 `?dryrun=true` 參數，以顯示執行結果，而不會有任何動作傳送訊息。

#### 範例請求
```json
POST _plugins/_alerting/monitors/{monitor_id}/_execute
```
{% include copy-curl.html %}


<details markdown="block">
  <summary>
    選取以展開範例回應
  </summary>
  {: .text-delta}

#### 範例回應
```json
{
  "monitor_name": "logs",
  "period_start": 1547161872322,
  "period_end": 1547161932322,
  "error": null,
  "trigger_results": {
    "Sooi7GcB53a0ewuj_6MH": {
      "name": "Over",
      "triggered": true,
      "error": null,
      "action_results": {}
    }
  }
}
```
{% include copy-curl.html %}

</details>

---

## 取得警示

傳回包含所有警示的陣列。

#### 路徑參數

下表列出可用的路徑參數。所有路徑參數皆為選用。

| 參數 | 資料類型 | 說明
| :--- | :--- | :---
| `sortString` | 字串 | 定義結果的排序方式。預設為 `monitor_name.keyword`。
| `sortOrder` | 字串 | 定義結果的順序。選項為 `asc` 或 `desc`。預設為 `asc`。
| `missing` | 字串 | 指定是否在回應中包含遺漏的資料。
| `size` | 字串 | 定義要傳回的結果數量。預設為 `20`。
| `startIndex` | 字串 | 定義結果的起始位置，用於分頁。預設為 `0`。
| `searchString` | 字串 | 定義用於搜尋特定警示的搜尋字串。預設為空字串。
| `severityLevel` | 字串 | 定義要篩選的嚴重性層級。預設為 `ALL`。
| `alertState` | 字串 | 定義要篩選的警示狀態。預設為 `ALL`。
| `monitorId` | 字串 | 依監視器 ID 篩選。
| `workflowIds` | 字串 | 允許在單一儀表板中監視來自多個工作流程的鏈結警示狀態。適用於 OpenSearch 2.9 或更新版本。

#### 範例請求
```json
GET _plugins/_alerting/monitors/alerts
```
{% include copy-curl.html %}


<details markdown="block">
  <summary>
    選取以展開範例回應
  </summary>
  {: .text-delta}

#### 範例回應
```json
{
  "alerts": [
    {
      "id": "eQURa3gBKo1jAh6qUo49",
      "version": 300,
      "monitor_id": "awUMa3gBKo1jAh6qu47E",
      "schema_version": 2,
      "monitor_version": 2,
      "monitor_name": "Example_monitor_name",
      "monitor_user": {
        "name": "admin",
        "backend_roles": [
          "admin"
        ],
        "roles": [
          "all_access",
          "own_index"
        ],
        "custom_attribute_names": [],
        "user_requested_tenant": null
      },
      "trigger_id": "bQUQa3gBKo1jAh6qnY6G",
      "trigger_name": "Example_trigger_name",
      "state": "ACTIVE",
      "error_message": null,
      "alert_history": [
        {
          "timestamp": 1617314504873,
          "message": "Example error message"
        },
        {
          "timestamp": 1617312543925,
          "message": "Example error message"
        }
      ],
      "severity": "1",
      "action_execution_results": [
        {
          "action_id": "bgUQa3gBKo1jAh6qnY6G",
          "last_execution_time": 1617317979908,
          "throttled_count": 0
        }
      ],
      "start_time": 1616704000492,
      "last_notification_time": 1617317979908,
      "end_time": null,
      "acknowledged_time": null
    }
  ],
  "totalAlerts": 1
}
```
{% include copy-curl.html %}

</details>

---

## 確認警示

[取得警示之後](#get-alerts)，您可以在一次呼叫中確認任意數量的作用中警示。如果警示已處於 `ERROR`、`COMPLETED` 或 `ACKNOWLEDGED` 狀態，則會出現在 `failed` 陣列中。

#### 範例請求
```json
POST _plugins/_alerting/monitors/{monitor-id}/_acknowledge/alerts
{
  "alerts": ["eQURa3gBKo1jAh6qUo49"]
}
```
{% include copy-curl.html %}


<details markdown="block">
  <summary>
    選取以展開範例回應
  </summary>
  {: .text-delta}


#### 範例回應
```json
{
  "success": [
  "eQURa3gBKo1jAh6qUo49"
  ],
  "failed": []
}
```
{% include copy-curl.html %}

</details>

---

## 目的地

目的地已在 OpenSearch 2.0 中被棄用，並由通知通道取代。建立、更新及刪除目的地的作業已在同一版本中移除，現有的目的地也已自動遷移至通知通道。若要設定警示的傳送目的地，請使用 [Notifications API]({{site.url}}{{site.baseurl}}/observing-your-data/notifications/api/)。下列讀取作業仍可用於擷取尚未遷移的目的地。
{: .warning}

### 取得目的地

使用下列請求擷取單一目的地。

#### 範例請求
```json
GET _plugins/_alerting/destinations/{destination-id}
```
{% include copy-curl.html %}


<details markdown="block">
  <summary>
    選取以展開範例回應
  </summary>
  {: .text-delta}

#### 範例回應
```json
{
  "totalDestinations": 1,
  "destinations": [{
      "id": "1a2a3a4a5a6a7a",
      "type": "slack",
      "name": "sample-destination",
      "user": {
        "name": "psantos",
        "backend_roles": [
          "human-resources"
        ],
        "roles": [
          "alerting_full_access",
          "hr-role"
        ],
        "custom_attribute_names": []
      },
      "schema_version": 3,
      "seq_no": 0,
      "primary_term": 6,
      "last_update_time": 1603943261722,
      "slack": {
        "url": "https://example.com"
      }
    }
  ]
}
```
{% include copy-curl.html %}

</details>

### 取得目的地

使用下列請求擷取所有目的地。

#### 範例請求
```json
GET _plugins/_alerting/destinations
```
{% include copy-curl.html %}


<details markdown="block">
  <summary>
    選取以展開範例回應
  </summary>
  {: .text-delta}

#### 範例回應
```json
{
  "totalDestinations": 1,
  "destinations": [{
      "id": "1a2a3a4a5a6a7a",
      "type": "slack",
      "name": "sample-destination",
      "user": {
        "name": "psantos",
        "backend_roles": [
          "human-resources"
        ],
        "roles": [
          "alerting_full_access",
          "hr-role"
        ],
        "custom_attribute_names": []
      },
      "schema_version": 3,
      "seq_no": 0,
      "primary_term": 6,
      "last_update_time": 1603943261722,
      "slack": {
        "url": "https://example.com"
      }
    }
  ]
}
```
{% include copy-curl.html %}

</details>

### 取得電子郵件帳戶

使用下列請求擷取為警示用途所設定的特定電子郵件帳戶詳細資料。

#### 範例請求
```json
GET _plugins/_alerting/destinations/email_accounts/{email_account_id}
{
  "name": "example_account",
  "email": "example@email.com",
  "host": "smtp.email.com",
  "port": 465,
  "method": "ssl"
}
```
{% include copy-curl.html %}


<details markdown="block">
  <summary>
    選取以展開範例回應
  </summary>
  {: .text-delta}

#### 範例回應
```json
{
  "_id" : "email_account_id",
  "_version" : 2,
  "_seq_no" : 8,
  "_primary_term" : 2,
  "email_account" : {
    "schema_version" : 2,
    "name" : "test_account",
    "email" : "test@email.com",
    "host" : "smtp.test.com",
    "port" : 465,
    "method" : "ssl"
  }
}
```
{% include copy-curl.html %}

</details>

### 搜尋電子郵件帳戶

使用下列請求擷取用於電子郵件警示的已設定電子郵件帳戶相關資訊。

#### 範例請求
```json
POST _plugins/_alerting/destinations/email_accounts/_search
{
  "from": 0,
  "size": 20,
  "sort": { "email_account.name.keyword": "desc" },
  "query": {
    "bool": {
      "must": {
        "match_all": {}
      }
    }
  }
}
```
{% include copy-curl.html %}


<details markdown="block">
  <summary>
    選取以展開範例回應
  </summary>
  {: .text-delta}

#### 範例回應
```json
{
  "took" : 8,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 2,
      "relation" : "eq"
    },
    "max_score" : null,
    "hits" : [
      {
        "_index" : ".opendistro-alerting-config",
        "_type" : "_doc",
        "_id" : "email_account_id",
        "_seq_no" : 8,
        "_primary_term" : 2,
        "_score" : null,
        "_source" : {
          "schema_version" : 2,
          "name" : "example_account",
          "email" : "example@email.com",
          "host" : "smtp.email.com",
          "port" : 465,
          "method" : "ssl"
        },
        "sort" : [
          "example_account"
        ]
      },
      ...
    ]
  }
}
```
{% include copy-curl.html %}

</details>

### 取得電子郵件群組

使用下列請求擷取特定電子郵件群組目的地的詳細資料，並傳入您要擷取的電子郵件群組 ID。

#### 範例請求
```json
GET _plugins/_alerting/destinations/email_groups/{email_group_id}
{
  "name": "example_email_group",
  "emails": [{
    "email": "example@email.com"
  }]
}
```
{% include copy-curl.html %}


<details markdown="block">
  <summary>
    選取以展開範例回應
  </summary>
  {: .text-delta}
  
#### 範例回應
```json
{
  "_id" : "email_group_id",
  "_version" : 4,
  "_seq_no" : 17,
  "_primary_term" : 2,
  "email_group" : {
    "schema_version" : 2,
    "name" : "example_email_group",
    "emails" : [
      {
        "email" : "example@email.com"
      }
    ]
  }
}
```
{% include copy-curl.html %}

</details>

### 搜尋電子郵件群組

查詢並擷取用於警示的現有電子郵件群組相關資訊，讓您能依據各種條件篩選及排序結果。下列請求顯示一個範例。

#### 範例請求
```json
POST _plugins/_alerting/destinations/email_groups/_search
{
  "from": 0,
  "size": 20,
  "sort": { "email_group.name.keyword": "desc" },
  "query": {
    "bool": {
      "must": {
        "match_all": {}
      }
    }
  }
}
```
{% include copy-curl.html %}


<details markdown="block">
  <summary>
    選取以展開範例回應
  </summary>
  {: .text-delta}
  
#### 範例回應
```json
{
  "took" : 7,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 5,
      "relation" : "eq"
    },
    "max_score" : null,
    "hits" : [
      {
        "_index" : ".opendistro-alerting-config",
        "_type" : "_doc",
        "_id" : "email_group_id",
        "_seq_no" : 10,
        "_primary_term" : 2,
        "_score" : null,
        "_source" : {
          "schema_version" : 2,
          "name" : "example_email_group",
          "emails" : [
            {
              "email" : "example@email.com"
            }
          ]
        },
        "sort" : [
          "example_email_group"
        ]
      },
      ...
    ]
  }
}
```
{% include copy-curl.html %}

</details>

## 建立註解

使用下列請求為特定警示新增註解，提供與該警示相關的額外背景資訊或備註。

#### 範例請求
```json
POST _plugins/_alerting/comments/{alert-id}
{
  "content": "sample comment"
}
```
{% include copy-curl.html %}


<details markdown="block">
  <summary>
    選取以展開範例回應
  </summary>
  {: .text-delta}
  
#### 範例回應
```json
{
  "_id": "0U6aBJABVWc3FrmWer9s",
  "_seq_no": 7,
  "_primary_term": 2,
  "comment": {
    "entity_id": "vCZkA5ABWTh3kzuBEL_9",
    "entity_type": "alert",
    "content": "sample comment",
    "created_time": 1718064151148,
    "last_updated_time": null,
    "user": "admin"
  }
}
```
{% include copy-curl.html %}

</details>

## 更新註解

使用下列請求修改先前新增且與警示相關的註解內容。

#### 請求範例

```json
PUT _plugins/_alerting/comments/{comment-id}
{
  "content": "sample updated comment"
}
```
{% include copy-curl.html %}


<details markdown="block">
  <summary>
    選取以展開回應範例
  </summary>
  {: .text-delta}
  
#### 回應範例
```json
{
  "_id": "0U6aBJABVWc3FrmWer9s",
  "_seq_no": 8,
  "_primary_term": 3,
  "comment": {
    "entity_id": "vCZkA5ABWTh3kzuBEL_9",
    "entity_type": "alert",
    "content": "sample updated comment",
    "created_time": 1718064151148,
    "last_updated_time": 1718064745485,
    "user": "admin"
  }
}
```
{% include copy-curl.html %}

</details>

## 搜尋評論

使用下列請求來查詢並擷取與警示相關聯的現有評論。

#### 請求範例
```json
GET _plugins/_alerting/comments/_search
{
  "query": {
    "match_all" : {}
  }
}
```
{% include copy-curl.html %}


<details markdown="block">
  <summary>
    選取以展開回應範例
  </summary>
  {: .text-delta}
  
#### 回應範例
```json
{
  "took": 14,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 2,
      "relation": "eq"
    },
    "max_score": 1,
    "hits": [
      {
        "_index": ".opensearch-alerting-comments-history-2024.06.10-1",
        "_id": "xE5tBJABVWc3FrmWRL5i",
        "_version": 1,
        "_seq_no": 3,
        "_primary_term": 2,
        "_score": 1,
        "_source": {
          "entity_id": "vCZkA5ABWTh3kzuBEL_9",
          "entity_type": "alert",
          "content": "a different sample comment",
          "created_time": 1718061188191,
          "last_updated_time": null,
          "user": "admin"
        }
      },
      {
        "_index": ".opensearch-alerting-comments-history-2024.06.10-1",
        "_id": "0U6aBJABVWc3FrmWer9s",
        "_version": 3,
        "_seq_no": 9,
        "_primary_term": 3,
        "_score": 1,
        "_source": {
          "entity_id": "vCZkA5ABWTh3kzuBEL_9",
          "entity_type": "alert",
          "content": "sample updated comment",
          "created_time": 1718064151148,
          "last_updated_time": 1718064745485,
          "user": "admin"
        }
      }
    ]
  }
}
```
{% include copy-curl.html %}

</details>

## 刪除評論

使用下列請求來移除與警示相關聯的特定評論。

#### 請求範例
```json
DELETE _plugins/_alerting/comments/{comment-id}
```
{% include copy-curl.html %}


<details markdown="block">
  <summary>
    選取以展開回應範例
  </summary>
  {: .text-delta}

#### 回應範例
```json
{
  "_id": "0U6aBJABVWc3FrmWer9s"
}
```
{% include copy-curl.html %}

</details>

