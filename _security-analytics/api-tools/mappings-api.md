---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "對應 API"
parent: Security Analytics APIs
nav_order: 45
---

# 對應 API

下列 API 可用於多項與對應相關的工作，包括建立、取得及更新對應。

---
## 取得對應檢視

回傳作為記錄來源之索引所包含欄位的檢視。

### 請求本文欄位

下列欄位用於取得欄位對應。

Field | Type | Description
:--- | :--- |:--- 
`index_name` | String | 用於記錄匯入的索引名稱。
`rule_topic` | String | 索引的記錄類型。

#### 請求範例

```json
GET /_plugins/_security_analytics/mappings/view

{
   "index_name": "windows",
   "rule_topic": "windows"
}
```

#### 回應範例

```json
{
    "properties": {
        "windows-event_data-CommandLine": {
            "path": "CommandLine",
            "type": "alias"
        },
        "event_uid": {
            "path": "EventID",
            "type": "alias"
        }
    },
    "unmapped_index_fields": [
        "windows-event_data-CommandLine",
        "unmapped_HiveName",
        "src_ip",
        "sha1",
        "processPath",
        "CallerProcessName",
        "CallTrace",
        "AuthenticationPackageName",
        "AuditSourceName",
        "AuditPolicyChanges",
        "AttributeValue",
        "AttributeLDAPDisplayName",
        "ApplicationPath",
        "Application",
        "AllowedToDelegateTo",
        "Address",
        "Action",
        "AccountType",
        "AccountName",
        "Accesses",
        "AccessMask",
        "AccessList"
    ]
}
```

---
## 建立對應

為指定的索引建立欄位別名對應。

#### 請求範例

```json
POST /_plugins/_security_analytics/mappings

{
   "index_name": "windows",
   "rule_topic": "windows",
   "partial": true,
   "alias_mappings": {
        "properties": {
            "event_uid": {
            "type": "alias",
            "path": "EventID"
          }
       }
   }
}
```

#### 回應範例

```json
{
    "acknowledged": true
}
```

---
## 取得對應

擷取指定索引的欄位別名對應。

### 路徑參數

Field | Type | Description
:--- | :--- |:--- 
`index_name` | String | 用於記錄匯入的索引名稱。必要。

#### 請求範例

```json
GET /_plugins/_security_analytics/mappings?index_name=windows
```

#### 回應範例

```json
{
    "windows": {
        "mappings": {
            "properties": {
                "windows-event_data-CommandLine": {
                    "type": "alias",
                    "path": "CommandLine"
                },
                "event_uid": {
                    "type": "alias",
                    "path": "EventID"
                }
            }
        }
    }
}
```

---
## 更新對應

更新指定索引的欄位別名對應。

#### 請求範例

```json
PUT /_plugins/_security_analytics/mappings

{
   "index_name": "windows",
   "field": "CommandLine",
   "alias": "windows-event_data-CommandLine"
}
```

#### 回應範例

```json
{
    "acknowledged": true
}
```

