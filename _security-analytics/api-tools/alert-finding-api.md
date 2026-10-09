---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "警示與結果 API"
parent: Security Analytics APIs
nav_order: 50
---


# 警示與結果 API

下列 API 可用於處理與警示和結果相關的工作。

---

## 取得警示

提供擷取與特定偵測器類型或偵測器 ID 相關之警示的選項。

### 參數

請求警示時，您可以指定下列參數。

參數 | 說明 
:--- | :---
`detector_id` | 用於擷取警示的偵測器 ID。指定 `detectorType` 時為選用，否則為必要。
`detectorType` | 用於擷取警示的偵測器類型。指定 `detector_Id` 時為選用，否則為必要。
`severityLevel` | 用於依警示嚴重性等級篩選。選用。
`alertState` | 用於依警示狀態篩選。可能的值為 ACTIVE、ACKNOWLEDGED、COMPLETED、ERROR 或 DELETED。選用。
`sortString` | 此欄位指定 Security Analytics 用來排序警示的字串。選用。
`sortOrder` | 用於排序結果清單的順序。可能的值為 `asc` 或 `desc`。選用。
`missing` | 沒有找到別名對應的欄位清單。選用。
`size` | 選用的限制，指定回應中傳回結果的最大數量。選用。
`startIndex` | 分頁指標。選用。
`searchString` | 您希望在搜尋中傳回的警示屬性。選用。

### 範例請求

```json
GET /_plugins/_security_analytics/alerts?detectorType=windows
```

### 範例回應

```json
{
    "alerts": [{
        "detector_id": "detector_12345",
        "id": "alert_id_1",
        "version": -3,
        "schema_version": 0,
        "trigger_id": "trigger_id_1",
        "trigger_name": "my_trigger",
        "finding_ids": ["finding_id_1"],
        "related_doc_ids": ["docId1"],
        "state": "ACTIVE",
        "error_message": null,
        "alert_history": [],
        "severity": null,
        "action_execution_results": [{
            "action_id": "action_id_1",
            "last_execution_time": 1665693544996,
            "throttled_count": 0
        }],
        "start_time": "2022-10-13T20:39:04.995023Z",
        "last_notification_time": "2022-10-13T20:39:04.995028Z",
        "end_time": "2022-10-13T20:39:04.995027Z",
        "acknowledged_time": "2022-10-13T20:39:04.995028Z"
    }],
    "total_alerts": 1,
    "detectorType": "windows"
}
```

#### 回應本文欄位

警示會持續存在，直到您解決根本原因為止，並具有下列狀態：

狀態 | 說明
:--- | :---
`ACTIVE` | 警示仍在進行中且未經確認。警示會保持此狀態，直到您確認警示、刪除與警示相關聯的觸發條件，或完全刪除監視器為止。
`ACKNOWLEDGED` | 有人已確認警示，但尚未修正根本原因。
`COMPLETED` | 警示已不再進行中。在對應的觸發條件評估為 false 之後，警示會進入此狀態。
`ERROR` | 執行觸發條件時發生錯誤。此錯誤通常是由於觸發條件或目的地設定不當所致。
`DELETED` | 在警示進行期間，有人刪除了與此警示相關聯的偵測器或觸發條件。

---

## 確認警示

在觸發警示時傳送確認。

### 範例請求

```json
POST /_plugins/_security_analytics/detectors/{detector_id}/_acknowledge/alerts

{"alerts":["4dc7f5a9-2c82-4786-81ca-433a209d5205"]}
```

### 範例回應

```json
{
  "acknowledged": [
    {
      "detector_id": "8YT5fYQBZ8IUM4axics6",
      "id": "4dc7f5a9-2c82-4786-81ca-433a209d5205",
      "version": 1,
      "schema_version": 4,
      "trigger_id": "1TP5fYQBMkkIGY6Pg-q8",
      "trigger_name": "test-trigger",
      "finding_ids": [
        "2e167f4b-8063-40ef-80f8-2afd9bf095b8"
      ],
      "related_doc_ids": [
        "1|windows"
      ],
      "state": "ACTIVE",
      "error_message": null,
      "alert_history": [],
      "severity": "1",
      "action_execution_results": [
        {
          "action_id": "BopdoIJKXd",
          "last_execution_time": 1668560817925,
          "throttled_count": 0
        }
      ],
      "start_time": "2022-11-16T01:06:57.748Z",
      "last_notification_time": "2022-11-16T01:06:57.748Z",
      "end_time": null,
      "acknowledged_time": null
    }
  ],
  "failed": [],
  "missing": []
}
```

---

## 取得結果

Get Findings API 會根據偵測器屬性傳回結果。

### 參數

取得結果時，您可以指定下列參數。

參數 | 說明 
:--- | :---
`detector_id` | 用於擷取警示的偵測器 ID。選用。
`detectorType` | 用於擷取警示的偵測器類型。選用。
`sortOrder` | 用於排序結果清單的順序。可能的值為 `asc` 或 `desc`。選用。
`size` | 選用的限制，指定回應中傳回結果的最大數量。選用。
`startIndex` | 分頁指標。選用。
`detectionType` |  決定結果擷取方式的偵測規則類型。當偵測類型為 `threat` 時，會擷取威脅情報資料來源。當偵測類型為 `rule` 時，會根據偵測器的規則擷取結果。選用。
`severity` |  用於擷取警示的偵測器規則嚴重性。嚴重性可以是 `critical`、`high`、`medium` 或 `low`。選用。

### 範例請求

```json
GET /_plugins/_security_analytics/findings/_search
{
  "total_findings": 2,
  "findings": [
    {
      "detectorId": "b9ZN040Bjlggkcgx1d1W",
      "id": "35efb736-c5d9-499d-b9b5-31f0a7d61251",
      "related_doc_ids": [
        "1"
      ],
      "index": "smallidx",
      "queries": [
        {
          "id": "QdZN040Bjlggkcgxdd3X",
          "name": "QdZN040Bjlggkcgxdd3X",
          "fields": [],
          "query": "field1: *value1*",
          "tags": [
            "high",
            "ad_ldap"
          ]
        }
      ],
      "timestamp": 1708647166500,
      "document_list": [
        {
          "index": "smallidx",
          "id": "1",
          "found": true,
          "document": "{\n  \"field1\": \"value1\"\n}\n"
        }
      ]
    },
    {
      "detectorId": "O9ZM040Bjlggkcgx6N1S",
      "id": "a5022930-4503-4ca8-bf0a-320a2b1fb433",
      "related_doc_ids": [
        "1"
      ],
      "index": "smallidx",
      "queries": [
        {
          "id": "KtZM040Bjlggkcgxkd04",
          "name": "KtZM040Bjlggkcgxkd04",
          "fields": [],
          "query": "field1: *value1*",
          "tags": [
            "critical",
            "ad_ldap"
          ]
        }
      ],
      "timestamp": 1708647166500,
      "document_list": [
        {
          "index": "smallidx",
          "id": "1",
          "found": true,
          "document": "{\n  \"field1\": \"value1\"\n}\n"
        }
      ]
    }
  ]
}

```

```json
GET /_plugins/_security_analytics/findings/_search?severity=high
{
    "total_findings": 1,
    "findings": [
        {
            "detectorId": "b9ZN040Bjlggkcgx1d1W",
            "id": "35efb736-c5d9-499d-b9b5-31f0a7d61251",
            "related_doc_ids": [
                "1"
            ],
            "index": "smallidx",
            "queries": [
                {
                    "id": "QdZN040Bjlggkcgxdd3X",
                    "name": "QdZN040Bjlggkcgxdd3X",
                    "fields": [],
                    "query": "field1: *value1*",
                    "tags": [
                        "high",
                        "ad_ldap"
                    ]
                }
            ],
            "timestamp": 1708647166500,
            "document_list": [
                {
                    "index": "smallidx",
                    "id": "1",
                    "found": true,
                    "document": "{\n  \"field1\": \"value1\"\n}\n"
                }
            ]
        }
    ]
}
        
```

```json
GET /_plugins/_security_analytics/findings/_search?detectionType=rule
{
    "total_findings": 2,
    "findings": [
        {
            "detectorId": "b9ZN040Bjlggkcgx1d1W",
            "id": "35efb736-c5d9-499d-b9b5-31f0a7d61251",
            "related_doc_ids": [
                "1"
            ],
            "index": "smallidx",
            "queries": [
                {
                    "id": "QdZN040Bjlggkcgxdd3X",
                    "name": "QdZN040Bjlggkcgxdd3X",
                    "fields": [],
                    "query": "field1: *value1*",
                    "tags": [
                        "high",
                        "ad_ldap"
                    ]
                }
            ],
            "timestamp": 1708647166500,
            "document_list": [
                {
                    "index": "smallidx",
                    "id": "1",
                    "found": true,
                    "document": "{\n  \"field1\": \"value1\"\n}\n"
                }
            ]
        },
        {
            "detectorId": "O9ZM040Bjlggkcgx6N1S",
            "id": "a5022930-4503-4ca8-bf0a-320a2b1fb433",
            "related_doc_ids": [
                "1"
            ],
            "index": "smallidx",
            "queries": [
                {
                    "id": "KtZM040Bjlggkcgxkd04",
                    "name": "KtZM040Bjlggkcgxkd04",
                    "fields": [],
                    "query": "field1: *value1*",
                    "tags": [
                        "critical",
                        "ad_ldap"
                    ]
                }
            ],
            "timestamp": 1708647166500,
            "document_list": [
                {
                    "index": "smallidx",
                    "id": "1",
                    "found": true,
                    "document": "{\n  \"field1\": \"value1\"\n}\n"
                }
            ]
        }
    ]
}


```
```json
GET /_plugins/_security_analytics/findings/_search?detectionType=rule&severity=high
{
    "total_findings": 1,
    "findings": [
        {
            "detectorId": "b9ZN040Bjlggkcgx1d1W",
            "id": "35efb736-c5d9-499d-b9b5-31f0a7d61251",
            "related_doc_ids": [
                "1"
            ],
            "index": "smallidx",
            "queries": [
                {
                    "id": "QdZN040Bjlggkcgxdd3X",
                    "name": "QdZN040Bjlggkcgxdd3X",
                    "fields": [],
                    "query": "field1: *value1*",
                    "tags": [
                        "high",
                        "ad_ldap"
                    ]
                }
            ],
            "timestamp": 1708647166500,
            "document_list": [
                {
                    "index": "smallidx",
                    "id": "1",
                    "found": true,
                    "document": "{\n  \"field1\": \"value1\"\n}\n"
                }
            ]
        }
    ]
}
        
```

```json
GET /_plugins/_security_analytics/findings/_search?*detectorType*=
{
    "total_findings":2,
    "findings":[
       {
            "detectorId":"12345",
            "id":"2b9663f4-ae77-4df8-b84f-688a0195723b",
            "related_doc_ids":[
                "5"
            ],
            "index":"sbwhrzgdlg",
            "queries":[
                {
                    "id":"f1bff160-587b-4500-b60c-ab22c7abc652",
                    "name":"3",
                    "query":"test_field:\"us-west-2\"",
                    "tags":[
                        
                    ]
                }
            ],
            "timestamp":1664401088804,
            "document_list":[
                {
                    "index":"sbwhrzgdlg",
                    "id":"5",
                    "found":true,
                    "document":"{\n            \"message\" : \"This is an error from IAD region\",\n            \"test_strict_date_time\" : \"2022-09-28T21:38:02.888Z\",\n            \"test_field\" : \"us-west-2\"\n        }"
                }
            ]
        },
        {
            "detectorId":"12345",
            "id":"f43a2701-0ef5-4931-8254-bdf510f73952",
            "related_doc_ids":[
                "1"
            ],
            "index":"sbwhrzgdlg",
            "queries":[
                {
                    "id":"f1bff160-587b-4500-b60c-ab22c7abc652",
                    "name":"3",
                    "query":"test_field:\"us-west-2\"",
                    "tags":[
                        
                    ]
                }
            ],
            "timestamp":1664401088746,
            "document_list":[
                {
                    "index":"sbwhrzgdlg",
                    "id":"1",
                    "found":true,
                    "document":"{\n            \"message\" : \"This is an error from IAD region\",\n            \"test_strict_date_time\" : \"2022-09-28T21:38:02.888Z\",\n            \"test_field\" : \"us-west-2\"\n        }"
                }
            ]
        }
    ]
}
```

