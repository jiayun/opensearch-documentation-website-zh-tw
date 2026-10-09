---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "PPL 監視器"
nav_order: 22
parent: Monitors
grand_parent: Alerting
has_children: false
---

# PPL 監視器

PPL 警示監視器使用 [Piped Processing Language (PPL)]({{site.url}}{{site.baseurl}}/sql-and-ppl/ppl/) 查詢來監視您的資料。它們是[每查詢監視器]({{site.url}}{{site.baseurl}}/observing-your-data/alerting/per-query-bucket-monitors/)，以 PPL 取代 Query DSL 作為查詢語言。

## 設定

本頁的範例使用包含網路請求記錄檔的 `application_logs` 索引。若要跟著操作，請使用下列對應建立索引：

```json
PUT /application_logs
{
  "mappings": {
    "properties": {
      "@timestamp": { "type": "date" },
      "endpoint": { "type": "keyword" },
      "service": { "type": "keyword" },
      "level": { "type": "keyword" },
      "response_time": { "type": "integer" }
    }
  }
}
```
{% include copy-curl.html %}

將範例文件編製索引：

```json
POST /application_logs/_bulk?refresh=true
{ "index": {} }
{ "@timestamp": "2026-01-15T10:00:00Z", "endpoint": "/api/orders", "service": "orders", "level": "ERROR", "response_time": 4200 }
{ "index": {} }
{ "@timestamp": "2026-01-15T10:01:00Z", "endpoint": "/api/orders", "service": "orders", "level": "ERROR", "response_time": 3600 }
{ "index": {} }
{ "@timestamp": "2026-01-15T10:02:00Z", "endpoint": "/api/checkout", "service": "checkout", "level": "ERROR", "response_time": 2500 }
```
{% include copy-curl.html %}

## 在 OpenSearch Dashboards 中建立 PPL 監視器

若要建立 PPL 監視器，請依照下列步驟操作：

1. 選取 **Alerting** > **Monitors** > **Create monitor**。
2. 選取 **PPL monitor** 選項。
3. 輸入監視器名稱並設定排程（依時間間隔或自訂 cron 運算式）。如需 cron 運算式的詳細資訊，請參閱 [Cron 運算式]({{site.url}}{{site.baseurl}}/api-reference/common-parameters/#cron-expressions)。
4. 在 **Query** 區段中輸入您的 PPL 查詢，例如：

   ```sql
   source = application_logs | stats avg(response_time) as avg_response by endpoint
   ```
   {% include copy.html %}

5. 新增一或多個觸發條件。如需設定觸發條件的詳細資訊，請參閱 [PPL 觸發條件](#ppl-triggers)。
6. 新增動作以指定觸發條件啟動時的通知方式。如需詳細資訊，請參閱[動作]({{site.url}}{{site.baseurl}}/observing-your-data/alerting/actions/)。
7. 選取 **Create**。

## PPL 觸發條件

PPL 監視器使用 `ppl_trigger` 物件，與其他監視器類型所使用的 Painless 指令碼觸發條件不同。如需詳細資訊，請參閱 [Painless 指令碼語言]({{site.url}}{{site.baseurl}}/scripting/painless/)。每個 PPL 監視器最多支援 10 個觸發條件。

### 結果數量觸發條件

結果數量觸發條件會將基礎 PPL 查詢傳回的資料列總數與閾值進行比較。支援下列比較運算子。

運算子 | 說明
:--- | :---
`>` | 大於
`>=` | 大於或等於
`<` | 小於
`<=` | 小於或等於
`==` | 等於
`!=` | 不等於

例如，若要在傳回超過一筆結果時觸發警示，請使用下列觸發條件定義：

```json
{
  "ppl_trigger": {
    "name": "High result count",
    "severity": "1",
    "type": "number_of_results",
    "num_results_condition": ">",
    "num_results_value": 1,
    "actions": []
  }
}
```

### 自訂條件觸發條件

自訂條件觸發條件會在基礎 PPL 查詢後附加 `where` 子句。如果修改後的查詢傳回任何結果，觸發條件就會啟動。這可讓您根據計算欄位或彙總定義細緻的條件。自訂條件會在建立監視器時驗證為 `where` 陳述式。

例如，請考慮下列基礎查詢：

```sql
source = application_logs | stats max(response_time) as max_response by endpoint
```

若要在任何端點的最大回應時間超過 3000 毫秒時觸發警示，請使用下列觸發條件定義：

```json
{
  "ppl_trigger": {
    "name": "Slow endpoint detected",
    "severity": "2",
    "type": "custom",
    "custom_condition": "where max_response > 3000",
    "actions": []
  }
}
```

## 範本變數

PPL 監視器提供下列額外的範本變數，可在[動作]({{site.url}}{{site.baseurl}}/observing-your-data/alerting/actions/)和通知訊息中使用。

變數 | 資料類型 | 說明
:--- | :--- | :---
`ctx.ppl_query_results` | 陣列 | 一個由對應表組成的清單，其中每個元素代表一列 PPL 查詢結果。每個對應表中的鍵為查詢結構描述中的欄位名稱。對於結果數量觸發條件，此陣列包含基礎查詢的結果。對於自訂條件觸發條件，此陣列包含套用自訂條件後的查詢結果。

### Mustache 範本範例

下列範例會迭代 PPL 查詢結果，並輸出每一列中的欄位：

{% raw %}
```
PPL Query Results:
{{#ctx.ppl_query_results}}
  Endpoint: {{endpoint}}, Average Response Time: {{avg_response}}
{{/ctx.ppl_query_results}}
```
{% endraw %}

## 查詢結果格式

PPL 查詢結果包含 `schema` 和 `datarows` 欄位。例如，查詢 `source = application_logs | where level = 'ERROR' | stats count() as error_count by endpoint` 會傳回下列回應：

```json
{
  "schema": [
    {"name": "error_count", "type": "bigint"},
    {"name": "endpoint", "type": "string"}
  ],
  "datarows": [
    [1, "/api/checkout"],
    [2, "/api/orders"]
  ],
  "total": 2,
  "size": 2
}
```

這些結果會自動轉換為對應表清單以供範本使用，並可在 `ctx.ppl_query_results` 中取得：

```json
[
  {"error_count": 1, "endpoint": "/api/checkout"},
  {"error_count": 2, "endpoint": "/api/orders"}
]
```

## 使用 API 建立 PPL 監視器

下列範例建立一個同時包含兩種觸發條件類型的 PPL 監視器：

```json
POST _plugins/_alerting/monitors
{
  "name": "PPL Error Rate Monitor",
  "type": "monitor",
  "monitor_type": "ppl_monitor",
  "enabled": true,
  "schedule": {
    "period": {
      "unit": "MINUTES",
      "interval": 5
    }
  },
  "inputs": [
    {
      "ppl_input": {
        "query": "source = application_logs | where level = 'ERROR' | stats count() as error_count by service",
        "query_language": "ppl"
      }
    }
  ],
  "triggers": [
    {
      "ppl_trigger": {
        "name": "Too many errors",
        "severity": "1",
        "type": "number_of_results",
        "num_results_condition": ">",
        "num_results_value": 1,
        "actions": [
          {
            "name": "Notify ops channel",
            "destination_id": "your-destination-id",
            "message_template": {
              "source": {% raw %}"Monitor {{ctx.monitor.name}} detected {{ctx.ppl_query_results.size}} services with errors."{% endraw %}
            },
            "subject_template": {
              "source": "Alert: High Error Rate Detected"
            }
          }
        ]
      }
    },
    {
      "ppl_trigger": {
        "name": "Critical service errors",
        "severity": "1",
        "type": "custom",
        "custom_condition": "where error_count > 1",
        "actions": [
          {
            "name": "Page oncall",
            "destination_id": "your-destination-id",
            "message_template": {
              "source": {% raw %}"Critical error threshold exceeded:\n{{#ctx.ppl_query_results}}\n  Service: {{service}}, Errors: {{error_count}}\n{{/ctx.ppl_query_results}}"{% endraw %}
            },
            "subject_template": {
              "source": "CRITICAL: Service Error Threshold Exceeded"
            }
          }
        ]
      }
    }
  ]
}
```
{% include copy-curl.html %}

回應會確認監視器已建立，並傳回其 `_id`。監視器會依照其設定的排程執行，每次執行時都會根據最新的查詢結果評估觸發條件。當觸發條件的條件符合時，就會啟動並執行其動作。

## 測試 PPL 監視器

若要立即執行監視器而不等待下一次排程執行，請使用 Execute API 並提供監視器 ID。加入 `?dryrun=true` 以評估觸發條件，而不建立警示或執行動作：

```json
POST _plugins/_alerting/monitors/<monitor_id>/_execute?dryrun=true
```
{% include copy-curl.html %}

回應會報告查詢結果，以及每個觸發條件是否啟動。`triggered` 欄位指出每個觸發條件的條件是否符合。對於自訂條件觸發條件，`ppl_query_results` 包含符合條件的資料列：

```json
{
  "monitor_name": "PPL Error Rate Monitor",
  "period_start": 1787067810953,
  "period_end": 1787068110953,
  "error": null,
  "input_results": {
    "results": [],
    "ppl_query_results": [
      { "error_count": 1, "service": "checkout" },
      { "error_count": 2, "service": "orders" }
    ],
    "ppl_num_results": 2,
    "error": null
  },
  "trigger_results": {
    "too_many_errors": {
      "name": "Too many errors",
      "triggered": true,
      "action_results": {},
      "ppl_query_results": [],
      "error": null
    },
    "critical_service_errors": {
      "name": "Critical service errors",
      "triggered": true,
      "action_results": {},
      "ppl_query_results": [
        { "error_count": 2, "service": "orders" }
      ],
      "error": null
    }
  }
}
```

## 設定

OpenSearch 支援下列 PPL 監視器設定。所有設定皆為動態設定，因此您無需重新啟動叢集即可變更：

- `plugins.alerting.monitor.max_ppl_triggers`（動態，整數）：每個 PPL 監視器允許的最大觸發條件數量。這也是可接受的最大值，因此您只能調低。預設值為 `10`。

- `plugins.alerting.ppl_query_max_execution_duration`（動態，時間單位）：監視器執行期間 PPL 查詢允許的最長執行時間。預設值為 `30s`。

- `plugins.alerting.ppl_monitor_max_query_length`（動態，long）：PPL 查詢的最大字元數。預設值為 `2000`。

- `plugins.alerting.ppl_query_results_max_datarows`（動態，long）：執行 PPL 查詢時可擷取的最大資料列數。預設值為 `10000`。

- `plugins.alerting.ppl_query_results_max_size`（動態，long）：儲存在警示和通知中的查詢結果的最大估計大小（以位元組為單位）。如果結果超過此大小，警示會以一則訊息取代結果，指出 PPL 查詢結果過大。預設值為 `3000`。

