---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "記錄類型 API"
parent: Security Analytics APIs
nav_order: 56
---

# 記錄類型 API

記錄類型 API 可讓您建立自訂記錄類型、搜尋自訂記錄類型、更新自訂記錄類型，以及刪除自訂記錄類型。


## 建立記錄類型

建立新的自訂記錄類型時，需要輸入名稱與描述，並將來源指定為 `Custom`。


### 範例請求

```json
POST /_plugins/_security_analytics/logtype
{
  "description": "custom-log-type-desc",
  "name": "custom-log-type4",
  "source": "Custom"
}
```
{% include copy-curl.html %}


### 範例回應

```json
{
    "_id": "m98uk4kBlb9cbROIpEj2",
    "_version": 1,
    "logType": {
        "name": "custom-log-type4",
        "description": "custom-log-type-desc",
        "source": "Custom",
        "tags": {
            "correlation_id": 27
        }
    }
}
```


## 搜尋自訂記錄類型

此 API 可讓您搜尋系統中的記錄類型。


### 範例請求

```json
POST /_plugins/_security_analytics/logtype/_search
{
    "query": {
        "match_all": {}
    }
}
```
{% include copy-curl.html %}


### 範例回應

```json
{
    "took": 3,
    "timed_out": false,
    "_shards": {
        "total": 1,
        "successful": 1,
        "skipped": 0,
        "failed": 0
    },
    "hits": {
        "total": {
            "value": 26,
            "relation": "eq"
        },
        "max_score": 2.0,
        "hits": [
            {
                "_index": ".opensearch-sap-log-types-config",
                "_id": "s3",
                "_score": 2.0,
                "_source": {
                    "name": "s3",
                    "description": "Windows logs",
                    "source": "Sigma",
                    "tags": {
                        "correlation_id": 21
                    }
                }
            },
            {
                "_index": ".opensearch-sap-log-types-config",
                "_id": "others_compliance",
                "_score": 2.0,
                "_source": {
                    "name": "others_compliance",
                    "description": "Compliance logs",
                    "source": "Sigma",
                    "tags": {
                        "correlation_id": 4
                    }
                }
            },
            {
                "_index": ".opensearch-sap-log-types-config",
                "_id": "github",
                "_score": 2.0,
                "_source": {
                    "name": "github",
                    "description": "Sys logs",
                    "source": "Sigma",
                    "tags": {
                        "correlation_id": 16
                    }
                }
            },
            {
                "_index": ".opensearch-sap-log-types-config",
                "_id": "others_application",
                "_score": 2.0,
                "_source": {
                    "name": "others_application",
                    "description": "Application logs",
                    "source": "Sigma",
                    "tags": {
                        "correlation_id": 0
                    }
                }
            },
            {
                "_index": ".opensearch-sap-log-types-config",
                "_id": "dns",
                "_score": 2.0,
                "_source": {
                    "name": "dns",
                    "description": "Compliance logs",
                    "source": "Sigma",
                    "tags": {
                        "correlation_id": 15
                    }
                }
            },
            {
                "_index": ".opensearch-sap-log-types-config",
                "_id": "m98uk4kBlb9cbROIpEj2",
                "_score": 2.0,
                "_source": {
                    "name": "custom-log-type-updated4",
                    "description": "custom-log-type-updated-desc",
                    "source": "Custom",
                    "tags": null
                }
            }
        ]
    }
}
```


## 更新自訂記錄類型

此 API 可讓您更新現有的自訂記錄類型。請在路由中使用記錄類型的 ID 來指定記錄類型，如下列範例所示：

```json
PUT /_plugins/_security_analytics/logtype/{log_type_id}
```


### 範例請求

```json
PUT /_plugins/_security_analytics/logtype/m98uk4kBlb9cbROIpEj2
{
  "name": "custom-log-type4",
  "description": "custom-log-type-updated-desc",
  "source": "Custom"
}
```
{% include copy-curl.html %}


### 範例回應

```json
{
    "_id": "m98uk4kBlb9cbROIpEj2",
    "_version": 1,
    "logType": {
        "name": "custom-log-type4",
        "description": "custom-log-type-updated-desc",
        "source": "Custom",
        "tags": {
            "correlation_id": 27
        }
    }
}
```


## 刪除自訂記錄類型

此 API 用於刪除自訂記錄類型。請在路由中指定記錄類型的 ID 以執行此操作：

```json
DELETE /_plugins/_security_analytics/logtype/{log_type_id}
```


### 範例請求

```json
DELETE /_plugins/_security_analytics/logtype/m98uk4kBlb9cbROIpEj2
```
{% include copy-curl.html %}


### 範例回應

```json
200 OK
{
    "_id": "m98uk4kBlb9cbROIpEj2",
    "_version": 1
}
```

只有自訂記錄類型可以刪除。嘗試刪除 OpenSearch 定義的標準記錄類型會導致錯誤。
{: .note }

