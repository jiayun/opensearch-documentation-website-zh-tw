---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "關聯引擎 API"
parent: Security Analytics APIs
nav_order: 55
---

# 關聯引擎 API

關聯引擎 API 可讓您建立新的關聯規則、檢視特定時間範圍內的發現項目與關聯，以及執行其他工作。

---

## 在記錄類型之間建立關聯規則

建立關聯規則，將來自兩個或多個記錄來源的發現項目建立關聯。

### 端點

```json
POST /_plugins/_security_analytics/correlation/rules
```

### 請求本文欄位

下表列出可用的請求本文欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- |:--- |
| `name` | 字串 | 關聯規則的名稱。選用。 |
| `correlate` | 陣列 | 要建立關聯的記錄來源。請提供至少兩個。必要。 |
| `correlate.index` | 字串 | 做為記錄來源的索引名稱。 |
| `correlate.query` | 字串 | 用來篩選安全性記錄以建立關聯的查詢。 |
| `correlate.category` | 字串 | 與記錄來源相關聯的記錄類型。 |
| `time_window` | Long | 發現項目必須在此時間範圍內發生才能建立關聯，以毫秒為單位。選用。若未指定，則套用 `plugins.security_analytics.correlation_time_window` 叢集設定。 |
| `trigger` | 物件 | 當規則將發現項目建立關聯時，產生關聯警示並傳送通知。選用。 |
| `trigger.name` | 字串 | 觸發程序的名稱。 |
| `trigger.severity` | 字串 | 以整數表示的觸發程序嚴重性等級：1 = 最高；2 = 高；3 = 中；4 = 低；5 = 最低。 |
| `trigger.actions` | 陣列 | 當觸發程序產生警示時要傳送的通知。 |
| `trigger.actions.name` | 字串 | 動作的名稱。每個動作皆為必要。 |
| `trigger.actions.destination_id` | 字串 | 接收訊息的通知管道 ID。 |
| `trigger.actions.subject_template.source` | 字串 | 通知訊息的主旨。可包含[關聯規則觸發程序變數](#correlation-rule-trigger-variables)。 |
| `trigger.actions.subject_template.lang` | 字串 | 用來定義主旨的指令碼語言。必須是 `mustache`。 |
| `trigger.actions.message_template.source` | 字串 | 通知訊息的本文。可包含[關聯規則觸發程序變數](#correlation-rule-trigger-variables)。 |
| `trigger.actions.message_template.lang` | 字串 | 用來定義訊息的指令碼語言。必須是 `mustache`。 |
| `trigger.actions.throttle_enabled` | 布林值 | 是否限制在一段時間內傳送的通知數量。預設為 `false`。 |
| `trigger.actions.throttle.unit` | 字串 | 用於節流的時間單位。 |
| `trigger.actions.throttle.value` | 整數 | 用於節流的時間單位數量。 |

### 範例請求

```json
POST /_plugins/_security_analytics/correlation/rules
{
  "correlate": [
    {
      "index": "vpc_flow",
      "query": "dstaddr:4.5.6.7 or dstaddr:4.5.6.6",
      "category": "network"
    },
    {
      "index": "windows",
      "query": "winlog.event_data.SubjectDomainName:NTAUTHORI*",
      "category": "windows"
    },
    {
      "index": "ad_logs",
      "query": "ResultType:50126",
      "category": "ad_ldap"
    },
    {
      "index": "app_logs",
      "query": "endpoint:/customer_records.txt",
      "category": "others_application"
    }
  ]
}
```
{% include copy-curl.html %}

### 範例回應

```json
{
  "_id": "DxKEUIkBpIjg64IK4nXg",
  "_version": 1,
  "rule": {
    "name": null,
    "correlate": [
      {
        "index": "vpc_flow",
        "query": "dstaddr:4.5.6.7 or dstaddr:4.5.6.6",
        "category": "network"
      },
      {
        "index": "windows",
        "query": "winlog.event_data.SubjectDomainName:NTAUTHORI*",
        "category": "windows"
      },
      {
        "index": "ad_logs",
        "query": "ResultType:50126",
        "category": "ad_ldap"
      },
      {
        "index": "app_logs",
        "query": "endpoint:/customer_records.txt",
        "category": "others_application"
      }
    ]
  }
}
```

### 回應本文欄位

下表列出所有回應本文欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- |:--- |
| `_id` | 字串 | 新規則的 ID。 |

### 關聯規則觸發程序

將 `trigger` 新增至關聯規則，即可在每次規則將發現項目建立關聯時產生關聯警示並傳送通知。下列請求會建立規則，並在其中包含觸發程序，當網路發現項目與 Active Directory 發現項目建立關聯時通知管道：

```json
POST /_plugins/_security_analytics/correlation/rules
{
  "name": "network-ad-correlation",
  "time_window": 300000,
  "correlate": [
    {
      "index": "vpc_flow",
      "query": "dstaddr:4.5.6.7",
      "category": "network"
    },
    {
      "index": "ad_logs",
      "query": "ResultType:50126",
      "category": "ad_ldap"
    }
  ],
  "trigger": {
    "name": "correlation-trigger",
    "severity": "1",
    "actions": [
      {
        "name": "notify-security-team",
        "destination_id": "6r8ZBoQBKW_6dKriacQb",
        "subject_template": {
          "source": {% raw %}"Correlation alert: {{ctx.correlationRuleName}}"{% endraw %},
          "lang": "mustache"
        },
        "message_template": {
          "source": {% raw %}"Rule {{ctx.correlationRuleName}} correlated finding {{ctx.sourceFinding}} with findings {{ctx.correlatedFindingIds}} within {{ctx.timeWindow}} ms."{% endraw %},
          "lang": "mustache"
        },
        "throttle_enabled": false
      }
    ]
  }
}
```
{% include copy-curl.html %}

回應包含產生的觸發程序與動作 ID：

```json
{
  "_id": "7mBjhqABedeO5z2szdu9",
  "_version": 1,
  "rule": {
    "name": "network-ad-correlation",
    "correlate": [
      {
        "index": "vpc_flow",
        "category": "network",
        "query": "dstaddr:4.5.6.7"
      },
      {
        "index": "ad_logs",
        "category": "ad_ldap",
        "query": "ResultType:50126"
      }
    ],
    "time_window": 300000,
    "trigger": {
      "id": "62BjhqABedeO5z2szdss",
      "name": "correlation-trigger",
      "severity": "1",
      "actions": [
        {
          "id": "6mBjhqABedeO5z2szdsr",
          "name": "notify-security-team",
          "destination_id": "6r8ZBoQBKW_6dKriacQb",
          "message_template": {
            "source": {% raw %}"Rule {{ctx.correlationRuleName}} correlated finding {{ctx.sourceFinding}} with findings {{ctx.correlatedFindingIds}} within {{ctx.timeWindow}} ms."{% endraw %},
            "lang": "mustache"
          },
          "throttle_enabled": false,
          "subject_template": {
            "source": {% raw %}"Correlation alert: {{ctx.correlationRuleName}}"{% endraw %},
            "lang": "mustache"
          }
        }
      ]
    }
  }
}
```

每個動作都需要 `name`。若請求省略它，會失敗並出現 `uninitialized_property_access_exception` 錯誤。
{: .note}

### 關聯規則觸發程序變數

下表列出關聯規則觸發程序動作的 `subject_template` 與 `message_template` 中可用的變數。這些變數與警示監視器中可用的變數不同，後者說明於[監視器變數]({{site.url}}{{site.baseurl}}/observing-your-data/alerting/monitors/#monitor-variables)。

| 變數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `ctx.correlationRuleName` | 字串 | 產生警示的關聯規則名稱。 |
| `ctx.sourceFinding` | 字串 | 起始關聯的發現項目 ID。 |
| `ctx.correlatedFindingIds` | 陣列 | 與來源發現項目建立關聯的發現項目 ID。 |
| `ctx.timeWindow` | Long | 關聯時間範圍，以毫秒為單位。 |

若要查看整個情境物件，請將 {% raw %}`{{ctx}}`{% endraw %} 新增至訊息本文。

---

## 列出特定時間範圍內的所有發現項目與關聯

列出特定時間範圍內的所有發現項目及其關聯。

### 端點

```json
GET /_plugins/_security_analytics/correlations
```

### 查詢參數

下表列出可用的查詢參數。兩個查詢參數皆為必要。

| 參數 | 資料類型 | 說明 |
| :--- | :--- |:--- |
| `start_timestamp` | 數字 | 時間範圍的開始時間，以毫秒為單位。 |
| `end_timestamp` | 數字 | 時間範圍的結束時間，以毫秒為單位。 |

### 範例請求

```json
GET /_plugins/_security_analytics/correlations?start_timestamp=1689289210000&end_timestamp=1689300010000
```
{% include copy-curl.html %}

### 範例回應

```json
{
  "findings": [
    {
      "finding1": "931de5f0-a276-45d5-9cdb-83e1045a3630",
      "logType1": "network",
      "finding2": "1e6f6a12-83f1-4a38-9bb8-648f196859cc",
      "logType2": "test_windows",
      "rules": [
        "nqI2TokBgL5wWFPZ6Gfu"
      ]
    }
  ]
}
```

### 回應本文欄位

下表列出所有回應本文欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- |:--- |
| `finding1` | 字串 | 關聯中第一個發現項目的 ID。 |
| `logType1` | 字串 | 與第一個發現項目相關聯的記錄類型。 |
| `finding2` | 字串 | 關聯中第二個發現項目的 ID。 |
| `logType2` | 字串 | 與第二個發現項目相關聯的記錄類型。 |
| `rules` | 陣列 | 與相關聯發現項目相關的關聯規則 ID 清單。 |

---

## 列出屬於某記錄類型之發現項目的關聯

列出與指定發現項目相關聯的發現項目。

### 端點

```json
GET /_plugins/_security_analytics/findings/correlate
```

### 查詢參數

下表列出可用的查詢參數。

| 參數 | 資料類型 | 說明 |
| :--- | :--- |:--- |
| `finding` | 字串 | 發現項目 ID。必要。 |
| `detector_type` | 字串 | 偵測器的記錄類型。必要。 |
| `nearby_findings` | 數字 | 相對於指定發現項目 ID 的鄰近發現項目數。選用。 |
| `time_window` | 字串 | 設定所有關聯必須同時發生的時間範圍。選用。 |

### 範例請求

```json
GET /_plugins/_security_analytics/findings/correlate?finding=425dce0b-f5ee-4889-b0c0-7d15669f0871&detector_type=ad_ldap&nearby_findings=20&time_window=10m
```
{% include copy-curl.html %}

### 範例回應

```json
{
  "findings": [
    {
      "finding": "5c661104-aaa9-484b-a91f-9cad4ae6d5f5",
      "detector_type": "others_application",
      "score": 0.000015182109564193524
    },
    {
      "finding": "2485b623-6573-42f4-a055-9b927e38a65f",
      "detector_type": "ad_ldap",
      "score": 0.000001615897872397909
    },
    {
      "finding": "051e00ad-5996-4c41-be20-f992451d1331",
      "detector_type": "windows",
      "score": 0.000016230604160227813
    },
    {
      "finding": "f11ca8a3-50d7-4074-a951-51439aa9e67b",
      "detector_type": "s3",
      "score": 0.000001759401811796124
    },
    {
      "finding": "9b86980e-5fb7-4c5a-bd1b-879a1e3baf12",
      "detector_type": "network",
      "score": 0.0000016306962606904563
    },
    {
      "finding": "e7dea5a1-164f-48f9-880e-4ba33e508713",
      "detector_type": "network",
      "score": 0.00001632626481296029
    }
  ]
}
```

### 回應本文欄位

下表列出所有回應本文欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- |:--- |
| `finding` | 字串 | 發現項目 ID。 |
| `detector_type` | 字串 | 與發現項目相關聯的記錄類型。 |
| `score` | 數字 | 相關聯發現項目的關聯分數。此分數依據關聯規則所定義之威脅情境中相關發現項目的鄰近程度計算。 |

---

## 列出關聯警示

列出由關聯規則觸發所產生的警示。

### 端點

```json
GET /_plugins/_security_analytics/correlationAlerts
```

### 查詢參數

下表列出可用的查詢參數。所有查詢參數皆為選用。

| 參數 | 資料類型 | 說明 |
| :--- | :--- |:--- |
| `correlation_rule_id` | 字串 | 關聯規則 ID。 |

### 範例請求

```json
GET /_plugins/_security_analytics/correlationAlerts?correlation_rule_id=VjY0MpABPzR_pcEveVRq
```
{% include copy-curl.html %}

### 範例回應

<details markdown="block">
<summary>
    回應
</summary>
{: .text-delta}

```json
{
    "correlationAlerts": [
        {
            "correlated_finding_ids": [
                "4f867df9-c9cb-4dc1-84bb-6c8b575f1a54"
            ],
            "correlation_rule_id": "VjY0MpABPzR_pcEveVRq",
            "correlation_rule_name": "rule-corr",
            "user": null,
            "id": "8532c08b-3ab5-4e95-a1c2-5884c4cd41a5",
            "version": 1,
            "schema_version": 1,
            "trigger_name": "trigger1",
            "state": "ACTIVE",
            "error_message": null,
            "severity": "1",
            "action_execution_results": [],
            "start_time": "2024-06-19T20:37:08.257Z",
            "end_time": "2024-06-19T20:42:08.257Z",
            "acknowledged_time": null
        },
        {
            "correlated_finding_ids": [
                "30d2109f-76bb-44ad-8f68-6daa905e018d"
            ],
            "correlation_rule_id": "VjY0MpABPzR_pcEveVRq",
            "correlation_rule_name": "rule-corr",
            "user": null,
            "id": "8bba85d9-a7fc-4c87-b35e-a7236b87159f",
            "version": 1,
            "schema_version": 1,
            "trigger_name": "trigger1",
            "state": "ACTIVE",
            "error_message": null,
            "severity": "1",
            "action_execution_results": [],
            "start_time": "2024-06-19T20:43:08.208Z",
            "end_time": "2024-06-19T20:48:08.208Z",
            "acknowledged_time": null
        }
    ],
    "total_alerts": 2
}
```
</details>

### 回應本文欄位

下表列出所有回應本文欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- |:--- |
| `correlationAlerts` | 陣列 | 符合請求的關聯警示。 |
| `correlationAlerts.correlated_finding_ids` | 陣列 | 由規則建立關聯之發現項目的 ID。 |
| `correlationAlerts.correlation_rule_id` | 字串 | 產生警示的關聯規則 ID。 |
| `correlationAlerts.correlation_rule_name` | 字串 | 產生警示的關聯規則名稱。 |
| `correlationAlerts.user` | 物件 | 與關聯規則相關聯的使用者。 |
| `correlationAlerts.id` | 字串 | 警示 ID。 |
| `correlationAlerts.version` | 整數 | 警示版本。 |
| `correlationAlerts.schema_version` | 整數 | 警示索引結構描述的版本。 |
| `correlationAlerts.trigger_name` | 字串 | 產生警示的觸發程序名稱。 |
| `correlationAlerts.state` | 字串 | 警示狀態。有效值為 `ACTIVE`、`ACKNOWLEDGED`、`COMPLETED`、`ERROR` 及 `DELETED`。 |
| `correlationAlerts.error_message` | 字串 | 警示的錯誤訊息（若有）。 |
| `correlationAlerts.severity` | 字串 | 產生警示之觸發程序的嚴重性層級。 |
| `correlationAlerts.action_execution_results` | 陣列 | 觸發程序執行之通知動作的結果。 |
| `correlationAlerts.start_time` | 字串 | 產生警示的時間。 |
| `correlationAlerts.end_time` | 字串 | 關聯時間範圍結束的時間。 |
| `correlationAlerts.acknowledged_time` | 字串 | 警示確認的時間。若警示尚未確認則為 `null`。 |
| `total_alerts` | 整數 | 傳回的警示總數。 |

---

## 確認關聯警示

確認一或多個關聯警示。

### 端點

```json
POST /_plugins/_security_analytics/_acknowledge/correlationAlerts
```

### 請求本文欄位

下表列出可用的請求本文欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- |:--- |
| `alertIds` | 陣列 | 要確認的關聯警示 ID。必要。 |

### 請求範例

```json
POST /_plugins/_security_analytics/_acknowledge/correlationAlerts
{
   "alertIds": ["8532c08b-3ab5-4e95-a1c2-5884c4cd41a5", "8bba85d9-a7fc-4c87-b35e-a7236b87159f"]
}
```
{% include copy-curl.html %}

### 範例回應

<details markdown="block">
<summary>
    回應
</summary>
{: .text-delta}

```json
{
    "acknowledged": [
        {
            "correlated_finding_ids": [
                "4f867df9-c9cb-4dc1-84bb-6c8b575f1a54"
            ],
            "correlation_rule_id": "VjY0MpABPzR_pcEveVRq",
            "correlation_rule_name": "rule-corr",
            "user": null,
            "id": "8532c08b-3ab5-4e95-a1c2-5884c4cd41a5",
            "version": 1,
            "schema_version": 1,
            "trigger_name": "trigger1",
            "state": "ACTIVE",
            "error_message": null,
            "severity": "1",
            "action_execution_results": [],
            "start_time": "2024-06-19T20:37:08.257Z",
            "end_time": "2024-06-19T20:42:08.257Z",
            "acknowledged_time": null
        },
        {
            "correlated_finding_ids": [
                "30d2109f-76bb-44ad-8f68-6daa905e018d"
            ],
            "correlation_rule_id": "VjY0MpABPzR_pcEveVRq",
            "correlation_rule_name": "rule-corr",
            "user": null,
            "id": "8bba85d9-a7fc-4c87-b35e-a7236b87159f",
            "version": 1,
            "schema_version": 1,
            "trigger_name": "trigger1",
            "state": "ACTIVE",
            "error_message": null,
            "severity": "1",
            "action_execution_results": [],
            "start_time": "2024-06-19T20:43:08.208Z",
            "end_time": "2024-06-19T20:48:08.208Z",
            "acknowledged_time": null
        }
    ],
    "failed": []
}
```
</details>

### 回應本文欄位

下表列出所有回應本文欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- |:--- |
| `acknowledged` | 陣列 | 已確認的關聯警示。 |
| `failed` | 陣列 | 無法確認的關聯警示。 |
