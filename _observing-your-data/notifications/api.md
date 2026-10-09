---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: API
nav_order: 50
parent: Notifications
redirect_from:
  - /notifications-plugin/api/
---

# Notifications API

如果您想以程式方式定義通知管道與來源，以便進行版本管理與重複使用，可以使用 Notifications REST API 定義、設定及刪除通知管道，並傳送測試訊息。

---

#### 目錄
1. 目錄
{:toc}

---

## 列出支援的管道組態

若要擷取所有支援的通知組態類型清單，請將 GET 請求傳送至 `features` 資源。

#### 請求範例

```json
GET /_plugins/_notifications/features
```

#### 回應範例

```json
{
  "allowed_config_type_list" : [
    "slack",
    "chime",
    "webhook",
    "email",
    "sns",
    "ses_account",
    "smtp_account",
    "email_group",
    "microsoft_teams"
  ],
  "plugin_features" : {
    "tooltip_support" : "true"
  }
}
```

## 列出所有通知管道

若要擷取所有通知管道的清單，請將 GET 請求傳送至 `channels` 資源。

#### 請求範例

```json
GET /_plugins/_notifications/channels
```

#### 回應範例

```json
{
  "start_index" : 0,
  "total_hits" : 2,
  "total_hit_relation" : "eq",
  "channel_list" : [
    {
      "config_id" : "sample-id",
      "name" : "Sample Slack Channel",
      "description" : "This is a Slack channel",
      "config_type" : "slack",
      "is_enabled" : true
    },
    {
      "config_id" : "sample-id2",
      "name" : "Test chime channel",
      "description" : "A test chime channel",
      "config_type" : "chime",
      "is_enabled" : true
    }
  ]
}
```

## 列出所有通知組態

若要擷取所有通知組態的清單，請將 GET 請求傳送至 `configs` 資源。

#### 請求範例

```json
GET _plugins/_notifications/configs
```

#### 回應範例

```json
{
  "start_index" : 0,
  "total_hits" : 2,
  "total_hit_relation" : "eq",
  "config_list" : [
    {
      "config_id" : "sample-id",
      "last_updated_time_ms" : 1652760532774,
      "created_time_ms" : 1652760532774,
      "config" : {
        "name" : "Sample Slack Channel",
        "description" : "This is a Slack channel",
        "config_type" : "slack",
        "is_enabled" : true,
        "slack" : {
          "url" : "https://hooks.slack.com/services/<webhook-path>"
        }
      }
    },
    {
      "config_id" : "sample-id2",
      "last_updated_time_ms" : 1652760735380,
      "created_time_ms" : 1652760735380,
      "config" : {
        "name" : "Test chime channel",
        "description" : "A test chime channel",
        "config_type" : "chime",
        "is_enabled" : true,
        "chime" : {
          "url" : "https://hooks.chime.aws/incomingwebhooks/<webhook-id>?token=<token>"
        }
      }
    }
  ]
}
```

若要篩選此請求傳回的通知組態類型，您可以使用下列選用的路徑參數來縮小查詢範圍。

參數	| 說明
:--- | :---
`config_id` | 指定管道識別碼。
`config_id_list` | 指定以逗號分隔的管道 ID 清單。
`from_index` | 搜尋的起始索引。
`max_items` | 請求中要傳回的項目數量上限。
`sort_order` | 指定結果的排序方向。有效選項為 `asc` 和 `desc`。
`sort_field` | 用於排序結果的欄位。
`last_updated_time_ms` | 管道上次更新時的 Unix 時間，以毫秒為單位。
`created_time_ms` | 管道建立時的 Unix 時間，以毫秒為單位。
`is_enabled` | 表示管道是否已啟用。
`config_type` | 管道類型。有效值為 `sns`、`slack`、`chime`、`webhook`、`smtp_account`、`ses_account`、`email_group`、`email` 和 `microsoft_teams`。
name | 管道名稱。
description	| 管道說明。
`email.email_account_id` | 管道使用的寄件者電子郵件地址。
`email.email_group_id_list` | 管道使用的電子郵件群組。
`email.recipient_list` | 管道的收件者清單。
`email_group.recipient_list` | 管道的電子郵件收件者群組清單。
`smtp_account.method` | 電子郵件加密方法。
`slack.url`	| Slack 傳入 webhook URL。必須包含 `hooks.slack.com/services/` 或 `hooks.gov-slack.com/services/`。
`chime.url`	| Amazon Chime 傳入 webhook URL。必須包含 `hooks.chime.aws/incomingwebhooks/` 和 `?token=` 參數。
`webhook.url`	| webhook URL。
`smtp_account.host`	| SMTP 帳戶的網域。
`smtp_account.from_address`	| 電子郵件帳戶的寄件者地址。
`smtp_account.method` | SMTP 帳戶的加密方法。
`sns.topic_arn`	| Amazon Simple Notification Service（SNS）主題的 ARN。
`sns.role_arn` | Amazon SNS 主題的角色 ARN。
`ses_account.region` | Amazon Simple Email Service（SES）帳戶的 AWS 區域。
`ses_account.role_arn` | Amazon SES 帳戶的角色 ARN。
`ses_account.from_address` | Amazon SES 帳戶的寄件者電子郵件地址。
`microsoft_teams.url` | Microsoft Teams webhook URL。URL 的網域必須為 `webhook.office.com`、`powerplatform.com` 或 `logic.azure.com`。

## 建立管道組態

若要建立通知管道組態，請將 POST 請求傳送至 `configs` 資源。

**注意：** 如果您指定已存在的 `config_id`，請求將失敗並傳回 409 Conflict 錯誤。在此情況下，請選擇不同的 `config_id`，或使用 [更新管道組態](#update-channel-configuration) API 搭配 PUT 請求來修改現有管道。如果您省略 `config_id`，OpenSearch 會自動產生一個。
{: .note}

#### 請求範例

```json
POST /_plugins/_notifications/configs/
{
  "config_id": "sample-id",
  "name": "sample-name",
  "config": {
    "name": "Sample Slack Channel",
    "description": "This is a Slack channel",
    "config_type": "slack",
    "is_enabled": true,
    "slack": {
      "url": "https://hooks.slack.com/services/<webhook-path>"
    }
  }
}
```

建立管道的 API 操作在請求本文中接受下列欄位：

欄位 |	資料類型 |	說明 |	必要
:--- | :--- | :--- | :---
`config_id` | 字串 | 組態的自訂 ID。 | 否
`config` | 物件 |	包含所有相關資訊，例如管道名稱、組態類型及外掛程式來源。 |	是
name | 字串 |	管道名稱。 | 是
description |	字串 | 管道的說明。 | 否
`config_type` |	字串 | 您的通知目的地。有效選項為 `sns`、`slack`、`chime`、`webhook`、`smtp_account`、`ses_account`、`email_group`、`email` 和 `microsoft_teams`。 | 是
`is_enabled` | 布林值 | 表示管道是否已啟用以傳送及接收通知。預設為 `true`。	| 否

建立管道操作接受多種 `config_types` 作為可能的通知目的地，因此請遵循您偏好的 `config_type` 格式。

```json
"sns": {
  "topic_arn": "<arn>",
  "role_arn": "<arn>" //optional
}
"slack": {
  "url": "https://hooks.slack.com/services/<webhook-path>"
}
"chime": {
  "url": "https://hooks.chime.aws/incomingwebhooks/<webhook-id>?token=<token>"
}
"webhook": {
  "url": "https://custom-webhook-test-url.com:8888/test-path?params1=value1&params2=value2"
}
"microsoft_teams": {
  "url": "https://example.webhook.office.com/<webhook-path>"
}
"smtp_account": {
  "host": "test-host.com",
  "port": 123,
  "method": "start_tls",
  "from_address": "test@email.com"
}
"ses_account": {
  "region": "us-east-1",
  "role_arn": "arn:aws:iam::012345678912:role/NotificationsSESRole",
  "from_address": "test@email.com"
}
"email_group": { //Email recipient group
  "recipient_list": [
    {
      "recipient": "test-email1@test.com"
    },
    {
      "recipient": "test-email2@test.com"
    }
  ]
}
"email": { //The channel that sends emails
  "email_account_id": "<smtp or ses account config id>",
  "recipient_list": [
    {
      "recipient": "custom.email@test.com"
    }
  ],
  "email_group_id_list": []
}
```

下列範例示範如何使用電子郵件作為 `config_type` 來建立管道：

```json
POST /_plugins/_notifications/configs/
{
  "config_id": "sample-email-id",
  "name": "sample-name",
  "config": {
    "name": "Sample Email Channel",
    "description": "Sample email description",
    "config_type": "email",
    "is_enabled": true,
    "email": {
      "email_account_id": "<email_account_id>",
      "recipient_list": [
        {
          "recipient": "sample@email.com"
        }
      ]
    }
  }
}
```

#### 回應範例

```json
{
  "config_id" : "<config_id>"
}
```


## 取得管道組態

若要依 `config_id` 取得管道組態，請傳送 GET 請求，並將 `config_id` 指定為路徑參數。

#### 請求範例

```json
GET _plugins/_notifications/configs/{config_id}
```

#### 回應範例

```json
{
  "start_index" : 0,
  "total_hits" : 1,
  "total_hit_relation" : "eq",
  "config_list" : [
    {
      "config_id" : "sample-id",
      "last_updated_time_ms" : 1652760532774,
      "created_time_ms" : 1652760532774,
      "config" : {
        "name" : "Sample Slack Channel",
        "description" : "This is a Slack channel",
        "config_type" : "slack",
        "is_enabled" : true,
        "slack" : {
          "url" : "https://hooks.slack.com/services/<webhook-path>"
        }
      }
    }
  ]
}
```


## 更新管道組態

若要更新現有管道組態，請將 PUT 請求傳送至 `configs` 資源，並將管道的 `config_id` 指定為路徑參數。在請求本文中指定新的組態詳細資訊。

**注意**：PUT 方法僅更新現有組態。若要建立新管道，請使用 [建立管道組態](#create-channel-configuration) API 搭配 POST 請求。如果您嘗試對不存在的 `config_id` 使用 PUT，請求將失敗。
{: .note}

#### 請求範例

```json
PUT _plugins/_notifications/configs/{config_id}
{
  "config": {
    "name": "Slack Channel",
    "description": "This is an updated channel configuration",
    "config_type": "slack",
    "is_enabled": true,
    "slack": {
      "url": "https://hooks.slack.com/services/<webhook-path>"
    }
  }
}
```

#### 回應範例

```json
{
  "config_id" : "<config_id>"
}
```


## 刪除管道組態

若要刪除管道組態，請將 DELETE 請求傳送至 `configs` 資源，並將 `config_id` 指定為路徑參數。

#### 請求範例

```json
DELETE /_plugins/_notifications/configs/{config_id}
```

#### 回應範例

```json
{
  "delete_response_list" : {
  "<config_id>" : "OK"
  }
}
```

您也可以提交以逗號分隔的管道 ID 清單，列出您要刪除的管道，OpenSearch 會刪除所有指定的通知管道。

#### 請求範例

```json
DELETE /_plugins/_notifications/configs/?config_id_list={config_id1},{config_id2},{config_id3}...
```

#### 回應範例

```json
{
  "delete_response_list" : {
  "<config_id1>" : "OK",
  "<config_id2>" : "OK",
  "<config_id3>" : "OK"
  }
}
```


## 傳送測試通知

若要傳送測試通知，請將 POST 請求傳送至 `/feature/test/`，並將管道組態的 `config_id` 指定為路徑參數。

#### 請求範例

```json
POST _plugins/_notifications/feature/test/{config_id}
```

#### 回應範例

```json
{
  "event_source" : {
    "title" : "Test Message Title-0Jnlh4ABa4TCWn5C5H2G",
    "reference_id" : "0Jnlh4ABa4TCWn5C5H2G",
    "severity" : "info",
    "tags" : [ ]
  },
  "status_list" : [
    {
      "config_id" : "0Jnlh4ABa4TCWn5C5H2G",
      "config_type" : "slack",
      "config_name" : "sample-id",
      "email_recipient_status" : [ ],
      "delivery_status" : {
        "status_code" : "200",
        "status_text" : """<!doctype html>
<html>
<head>
</head>
<body>
<div>
    <h1>Example Domain</h1>
    <p>Sample paragraph.</p>
    <p><a href="sample.example.com">TO BE OR NOT TO BE, THAT IS THE QUESTION</a></p>
</div>
</body>
</html>
"""
      }
    }
  ]
}

```
