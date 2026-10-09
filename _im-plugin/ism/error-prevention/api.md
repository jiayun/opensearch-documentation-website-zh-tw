---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "ISM 錯誤預防 API"
parent: ISM error prevention
grand_parent: Index State Management
nav_order: 20
---

# ISM 錯誤預防 API

ISM 錯誤預防 API 可讓您啟用索引狀態管理 (ISM) 錯誤預防，並檢查驗證狀態與訊息。

## 啟用錯誤預防驗證

您可以透過設定 `plugins.index_state_management.action_validation.enabled` 參數來設定錯誤預防驗證。

#### 範例請求

```json
PUT _cluster/settings
{
   "persistent":{
      "plugins.index_state_management.action_validation.enabled": true
   }
}
```
{% include copy-curl.html %}

#### 範例回應

```json
{
  "acknowledged" : true,
  "persistent" : {
    "plugins" : {
      "index_state_management" : {
        "action_validation" : {
          "enabled" : "true"
        }
      }
    }
  },
  "transient" : { }
}
```

## 使用 Explain API 檢查驗證狀態與訊息

在 Explain API URI 中傳入 `validate_action=true` 路徑參數，即可檢視驗證狀態與訊息。

#### 範例請求

```json
GET _plugins/_ism/explain/test-000001?validate_action=true
```
{% include copy-curl.html %}

#### 範例回應

```json
{
  "test-000001" : {
    "index.plugins.index_state_management.policy_id" : "test_rollover",
    "index.opendistro.index_state_management.policy_id" : "test_rollover",
    "index" : "test-000001",
    "index_uuid" : "CgKsxFmQSIa8dWqpbSJmyA",
    "policy_id" : "test_rollover",
    "policy_seq_no" : -2,
    "policy_primary_term" : 0,
    "rolled_over" : false,
    "index_creation_date" : 1667410460649,
    "state" : {
      "name" : "rollover",
      "start_time" : 1667410766045
    },
    "action" : {
      "name" : "rollover",
      "start_time" : 1667411127803,
      "index" : 0,
      "failed" : false,
      "consumed_retries" : 0,
      "last_retry_time" : 0
    },
    "step" : {
      "name" : "attempt_rollover",
      "start_time" : 1667411127803,
      "step_status" : "starting"
    },
    "retry_info" : {
      "failed" : true,
      "consumed_retries" : 0
    },
    "info" : {
      "message" : "Previous action was not able to update IndexMetaData."
    },
    "enabled" : false,
    "validate" : {
      "validation_message" : "Missing rollover_alias index setting [index=test-000001]",
      "validation_status" : "re_validating"
    }
  },
  "total_managed_indices" : 1
}
```

只有在傳入 `validate_action=true` 時，才會傳回驗證狀態與訊息。將該參數設為 `false` 或省略該參數，則兩者都不會傳回。

#### 範例請求

```json
GET _plugins/_ism/explain/test-000001?validate_action=false
```
{% include copy-curl.html %}

省略該參數會得到相同的結果：

```json
GET _plugins/_ism/explain/test-000001
```
{% include copy-curl.html %}

#### 範例回應

```json
{
  "test-000001" : {
    "index.plugins.index_state_management.policy_id" : "test_rollover",
    "index.opendistro.index_state_management.policy_id" : "test_rollover",
    "index" : "test-000001",
    "index_uuid" : "CgKsxFmQSIa8dWqpbSJmyA",
    "policy_id" : "test_rollover",
    "policy_seq_no" : -2,
    "policy_primary_term" : 0,
    "rolled_over" : false,
    "index_creation_date" : 1667410460649,
    "state" : {
      "name" : "rollover",
      "start_time" : 1667410766045
    },
    "action" : {
      "name" : "rollover",
      "start_time" : 1667411127803,
      "index" : 0,
      "failed" : false,
      "consumed_retries" : 0,
      "last_retry_time" : 0
    },
    "step" : {
      "name" : "attempt_rollover",
      "start_time" : 1667411127803,
      "step_status" : "starting"
    },
    "retry_info" : {
      "failed" : true,
      "consumed_retries" : 0
    },
    "info" : {
      "message" : "Previous action was not able to update IndexMetaData."
    },
    "enabled" : false
  },
  "total_managed_indices" : 1
}
```
