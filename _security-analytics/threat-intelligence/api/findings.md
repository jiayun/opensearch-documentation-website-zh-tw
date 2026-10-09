---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "警示與發現 API"
parent: Threat intelligence APIs
grand_parent: Threat intelligence
nav_order: 50
---


# 警示與發現 API

威脅情報警示與發現 API 可從威脅情報饋送中擷取警示與發現的相關資訊。


---

## 取得威脅情報警示

擷取與威脅情報監視器相關的所有警示。

### 端點

```json
GET /_plugins/_security_analytics/threat_intel/alerts
```
{% include copy-curl.html %}


### 路徑參數

請求警示時，您可以指定下列參數。

參數 | 說明 
:--- | :---- 
`severityLevel` | 依嚴重性等級篩選警示。選用。        
`alertState`    | 用於依警示狀態篩選。可能的值為 `ACTIVE`、`ACKNOWLEDGED`、`COMPLETED`、`ERROR` 或 `DELETED`。選用。 
`sortString`    | Security Analytics 用來排序警示的字串。選用。                          
`sortOrder`     | 用於排序警示清單的順序。可能的值為 `asc` 或 `desc`。選用。                        
`missing`       | 未找到別名對應的欄位清單。選用。                                          
`size`          | 選用的回應中可傳回的最大結果數量。選用。                          
`startIndex`    | 分頁指示器。選用。  
`searchString`  | 您希望在搜尋中傳回的警示屬性。選用。

### 範例請求

```json
GET /_plugins/_security_analytics/threat_intel/alerts
```
{% include copy-curl.html %}

### 範例回應

```json
{
    "alerts": [{
      "id": "906669ee-56e8-4f40-a12f-ab4c274d7521",
      "version": 1,
      "schema_version": 0,
      "seq_no": 0,
      "primary_term": 1,
      "trigger_id": "regwarg",
      "trigger_name": "regwarg",
      "state": "ACTIVE",
      "error_message": null,
      "ioc_value": "example-has00001",
      "ioc_type": "hashes",
      "severity": "high",
      "finding_ids": [
        "a9c10094-6139-42b3-81a8-867dffbe381d"
      ],
      "acknowledged_time": 1722038395105,
      "last_updated_time": null,
      "start_time": 1722038395105,
      "end_time": null
    }],
    "total_alerts": 1
}
```

### 回應本文欄位

威脅情報警示可能處於下列其中一種狀態。

| 狀態  | 說明  |
| :---- | :--- |
| `ACTIVE`   | 警示正在進行中且尚未確認。警示會保持此狀態，直到被確認、與警示相關聯的觸發條件被刪除，或威脅情報監視器被完全刪除為止。 |
| `ACKNOWLEDGED` | 警示已確認，但警示的根本原因尚未處理。  |
| `COMPLETED` | 警示已不再進行中。當對應的觸發條件評估結果為 `false` 後，警示會進入此狀態。   |
| `DELETED` | 警示作用中時，其監視器或觸發條件已被刪除。  |

---

## 更新警示狀態 API 

將指定警示的狀態更新為 `ACKNOWLEDGED` 或 `COMPLETED`。只有處於 `ACTIVE` 狀態的警示才能更新。 

### 端點

```json
PUT /plugins/security_analytics/threat_intel/alerts/status
```

### 範例請求

下列範例將指定警示的狀態更新為 `ACKNOWLEDGED`：

```json
PUT /plugins/security_analytics/threat_intel/alerts/status?state=ACKNOWLEDGED&alert_ids={alert-id},{alert-id}
```

下列範例將指定警示的狀態更新為 `COMPLETED`：

```json
PUT /plugins/security_analytics/threat_intel/alerts/status?state=COMPLETED&alert_ids=alert_ids={alert-id},{alert-id}
```

### 範例回應

```json
{
  "updated_alerts": [
    {
      "id": "906669ee-56e8-4f40-a12f-ab4c274d7521",
      "version": 1,
      "schema_version": 0,
      "seq_no": 2,
      "primary_term": 1,
      "trigger_id": "regwarg",
      "trigger_name": "regwarg",
      "state": "ACKNOWLEDGED",
      "error_message": null,
      "ioc_value": "example-has00001",
      "ioc_type": "hashes",
      "severity": "high",
      "finding_ids": [
        "a9c10094-6139-42b3-81a8-867dffbe381d"
      ],
      "acknowledged_time": 1722039091209,
      "last_updated_time": 1722039091209,
      "start_time": 1722038395105,
      "end_time": null
    },
    {
      "id": "56e8-4f40-a12f-ab4c274d7521-906669ee",
      "version": 1,
      "schema_version": 0,
      "seq_no": 2,
      "primary_term": 1,
      "trigger_id": "regwarg",
      "trigger_name": "regwarg",
      "state": "ACKNOWLEDGED",
      "error_message": null,
      "ioc_value": "example-has00001",
      "ioc_type": "hashes",
      "severity": "high",
      "finding_ids": [
        "a9c10094-6139-42b3-81a8-867dffbe381d"
      ],
      "acknowledged_time": 1722039091209,
      "last_updated_time": 1722039091209,
      "start_time": 1722038395105,
      "end_time": null
    }
  ],
  "failure_messages": []
}
```



---

## 取得發現

傳回威脅情報入侵指標 (IOC) 的發現。當威脅情報監視器在資料掃描期間發現惡意的 IOC 時，系統會自動產生一筆發現。

### 端點

```json
GET /_plugins/_security_analytics/threat_intel/findings/
```

### 路徑參數 

| 參數      | 說明                                                                                 |
|:---------------|:--------------------------------------------------------------------------------------------|
| `sortString`   | 指定 Security Analytics 用來排序警示的字串。選用。     |
| `sortOrder`    | 用於排序發現清單的順序。可能的值為 `asc` 或 `desc`。選用。 |
| `missing`      | 未找到別名對應的欄位清單。選用。                     |
| `size`         | 回應中要傳回的最大結果數量。選用。     |
| `startIndex`   | 分頁指示器。選用。                                                         |
| `searchString` | 您希望在搜尋中傳回的警示屬性。選用。                              |

### 範例請求

```json
GET /_plugins/_security_analytics/threat_intel/findings/_search?size=3
```

```json
{
  "total_findings": 10,
  "ioc_findings": [
    {
      "id": "a9c10094-6139-42b3-81a8-867dffbe381d",
      "related_doc_ids": [
        "Ccp88ZAB1vBjq44wmTEu:windows"
      ],
      "ioc_feed_ids": [
        {
          "ioc_id": "2",
          "feed_id": "Bsp88ZAB1vBjq44wiDGo",
          "feed_name": "my_custom_feed",
          "index": ""
        }
      ],
      "monitor_id": "B8p88ZAB1vBjq44wkjEy",
      "monitor_name": "Threat intelligence monitor",
      "ioc_value": "example-has00001",
      "ioc_type": "hashes",
      "timestamp": 1722038394501,
      "execution_id": "01cae635-93dc-4f07-9e39-31076b9535d1"
    },
    {
      "id": "8d87aee0-aaa4-4c12-b4e2-b4b1f4ec80f9",
      "related_doc_ids": [
        "GsqI8ZAB1vBjq44wXTHa:windows"
      ],
      "ioc_feed_ids": [
        {
          "ioc_id": "2",
          "feed_id": "Bsp88ZAB1vBjq44wiDGo",
          "feed_name": "my_custom_feed",
          "index": ""
        }
      ],
      "monitor_id": "B8p88ZAB1vBjq44wkjEy",
      "monitor_name": "Threat intelligence monitor",
      "ioc_value": "example-has00001",
      "ioc_type": "hashes",
      "timestamp": 1722039165824,
      "execution_id": "54899e32-aeeb-401e-a031-b1728772f0aa"
    },
    {
      "id": "2419f624-ba1a-4873-978c-760183b449b7",
      "related_doc_ids": [
        "H8qI8ZAB1vBjq44woDHU:windows"
      ],
      "ioc_feed_ids": [
        {
          "ioc_id": "2",
          "feed_id": "Bsp88ZAB1vBjq44wiDGo",
          "feed_name": "my_custom_feed",
          "index": ""
        }
      ],
      "monitor_id": "B8p88ZAB1vBjq44wkjEy",
      "monitor_name": "Threat intelligence monitor",
      "ioc_value": "example-has00001",
      "ioc_type": "hashes",
      "timestamp": 1722039182616,
      "execution_id": "32ad2544-4b8b-4c9b-b2b4-2ba6d31ece12"
    }
  ]
}

```
