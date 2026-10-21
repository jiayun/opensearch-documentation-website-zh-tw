---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: API
nav_order: 50
parent: Notifications
redirect_from:
  - /notifications-plugin/api/
---

# 通知 API

使用 Notifications REST API 以程式設計方式建立、擷取、更新及刪除通知組態，並傳送測試訊息。透過 API 定義頻道，可讓您對頻道定義進行版本管理並重複使用。

通知組態是下列其中一種類型：

- 接收通知的頻道：`slack`、`chime`、`microsoft_teams`、`webhook`、`email` 或 `sns`。
- `email` 頻道用來傳送訊息的電子郵件寄件者：`smtp_account` 或 `ses_account`。
- `email` 頻道傳送訊息的目標電子郵件收件者群組：`email_group`。

---

#### 目錄
1. 目錄
{:toc}

---

## 列出支援的頻道組態

若要擷取所有支援的通知組態類型清單，請將 GET 請求傳送至 `features` 資源。

### 端點

```json
GET /_plugins/_notifications/features
```

### 範例請求

```json
GET /_plugins/_notifications/features
```
{% include copy-curl.html %}

### 範例回應

```json
{
  "allowed_config_type_list" : [
    "slack",
    "chime",
    "microsoft_teams",
    "webhook",
    "email",
    "sns",
    "ses_account",
    "smtp_account",
    "email_group"
  ],
  "plugin_features" : {
    "tooltip_support" : "true"
  }
}
```

### 回應本文欄位

下表列出所有回應本文欄位。

欄位 | 資料類型 | 說明
:--- | :--- | :---
`allowed_config_type_list` | 字串陣列 | 叢集允許的組態類型。由 `opensearch.notifications.core.allowed_config_types` 設定進行設定。
`plugin_features` | 物件 | 外掛程式功能及其值。包含 `tooltip_support`，其由 `opensearch.notifications.core.tooltip_support` 設定進行設定。

## 列出所有通知頻道

若要擷取所有通知頻道的清單，請向 `channels` 資源傳送 GET 請求。回應包含 `slack`、`chime`、`microsoft_teams`、`webhook`、`email` 與 `sns` 類型的組態。電子郵件寄件者與電子郵件收件者群組不是頻道，因此回應不會包含它們。此端點不接受查詢參數。

### 端點

```json
GET /_plugins/_notifications/channels
```

### 請求範例

```json
GET /_plugins/_notifications/channels
```
{% include copy-curl.html %}

### 範例回應

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

若要擷取所有類型的通知組態清單，請向 `configs` 資源傳送 GET 請求。

### 端點

```json
GET /_plugins/_notifications/configs
```

### 查詢參數

下表列出可用的查詢參數。所有查詢參數皆為選用。無法識別的查詢參數會被拒絕。

參數 | 資料類型 | 說明
:--- | :--- | :---
`config_id` | 字串 | 傳回具有此 ID 的組態。
`config_id_list` | 字串 | 傳回具有這些 ID 的組態。請指定以逗號分隔的組態 ID 清單。若指定 `config_id` 或 `config_id_list`，請求會忽略所有篩選參數。
`from_index` | 整數 | 結果的起始索引。預設為 `0`。
`max_items` | 整數 | 可傳回的組態數量上限。預設為 `1000`。
`sort_field` | 字串 | 排序結果所依據的欄位。有效值為下列兩張表中篩選參數的名稱，但 `email.recipient_list.recipient` 與 `email_group.recipient_list.recipient` 除外。預設為 `last_updated_time_ms`。
`sort_order` | 字串 | 排序方向。有效值為 `asc` 與 `desc`。預設為 `asc`。
`query` | 字串 | 使用查詢字串語法搜尋所有關鍵字與文字篩選欄位。
`text_query` | 字串 | 使用查詢字串語法搜尋所有文字篩選欄位。

下列篩選參數會比對欄位完全等於指定值的組態。如有註明，可指定多個以逗號分隔的值，以比對其中任一值。

參數 | 資料類型 | 說明
:--- | :--- | :---
`last_updated_time_ms` | 字串 | 組態最後更新的時間，以 epoch 毫秒表示。請指定確切值或 `<from>..<to>` 格式的範圍。
`created_time_ms` | 字串 | 組態建立的時間，以 epoch 毫秒表示。請指定確切值或 `<from>..<to>` 格式的範圍。
`is_enabled` | 布林值 | 組態是否已啟用。
`config_type` | 字串 | 組態類型。請指定一或多個以逗號分隔的值。有效值為 `slack`、`chime`、`microsoft_teams`、`webhook`、`email`、`sns`、`smtp_account`、`ses_account` 與 `email_group`。
`email.email_account_id` | 字串 | `email` 頻道所使用的電子郵件寄件者 ID。接受以逗號分隔的清單。
`email.email_group_id_list` | 字串 | `email` 頻道所使用的電子郵件收件者群組 ID。接受以逗號分隔的清單。
`smtp_account.method` | 字串 | SMTP 寄件者的加密方法。接受以逗號分隔的清單。
`ses_account.region` | 字串 | Amazon Simple Email Service (Amazon SES) 寄件者的 AWS 區域。接受以逗號分隔的清單。

下列篩選參數會比對欄位包含指定文字的組態。

參數 | 資料類型 | 說明
:--- | :--- | :---
`name` | 字串 | 組態名稱。
`description` | 字串 | 組態描述。
`email.recipient_list.recipient` | 字串 | `email` 頻道的收件者電子郵件地址。
`email_group.recipient_list.recipient` | 字串 | 電子郵件收件者群組的收件者電子郵件地址。
`slack.url` | 字串 | Slack 傳入 webhook URL。必須包含 `hooks.slack.com/services/` 或 `hooks.gov-slack.com/services/`。
`chime.url` | 字串 | Amazon Chime 傳入 webhook URL。必須包含 `hooks.chime.aws/incomingwebhooks/` 與 `?token=` 參數。
`microsoft_teams.url` | 字串 | Microsoft Teams webhook URL。URL 的網域必須是 `webhook.office.com`、`powerplatform.com` 或 `logic.azure.com`。
`webhook.url` | 字串 | 自訂 webhook URL。
`smtp_account.host` | 字串 | SMTP 寄件者的主機。
`smtp_account.from_address` | 字串 | SMTP 寄件者的寄件者電子郵件地址。
`sns.topic_arn` | 字串 | Amazon Simple Notification Service (Amazon SNS) 主題 ARN。
`sns.role_arn` | 字串 | 用於發布至 Amazon SNS 主題的 IAM 角色 ARN。
`ses_account.role_arn` | 字串 | Amazon SES 寄件者的 IAM 角色 ARN。
`ses_account.from_address` | 字串 | Amazon SES 寄件者的寄件者電子郵件地址。

### 範例請求

```json
GET /_plugins/_notifications/configs
```
{% include copy-curl.html %}

下列請求會傳回前 10 個按名稱排序的 Slack 與 Amazon Chime 組態：

```json
GET /_plugins/_notifications/configs?config_type=slack,chime&sort_field=name&sort_order=asc&max_items=10
```
{% include copy-curl.html %}

### 回應範例

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

### 回應本文欄位

下表列出所有回應本文欄位。

欄位 | 資料類型 | 說明
:--- | :--- | :---
`start_index` | 整數 | 傳回結果的起始索引。
`total_hits` | 整數 | 符合請求的組態總數。
`total_hit_relation` | 字串 | `total_hits` 是精確值（`eq`）或下限（`gte`）。
`config_list` | 物件陣列 | 符合的組態。

`config_list` 陣列中的每個物件都包含下列欄位。

欄位 | 資料類型 | 說明
:--- | :--- | :---
`config_id` | 字串 | 組態 ID。
`last_updated_time_ms` | Long | 組態上次更新的時間，以 epoch 毫秒為單位。
`created_time_ms` | Long | 組態建立的時間，以 epoch 毫秒為單位。
`config` | 物件 | 組態。包含與[建立請求](#request-body-fields)中 `config` 物件相同的欄位。

## 建立頻道組態

若要建立通知組態，請向 `configs` 資源傳送 POST 請求。使用此請求來建立頻道、電子郵件寄件者，以及電子郵件收件者群組。

若您省略 `config_id`，OpenSearch 會產生一個 ID。若您指定的 `config_id` 已經存在，請求會失敗並傳回 `409 Conflict` 狀態。若要修改現有的組態，請使用[更新頻道組態](#update-channel-configuration) API。
{: .note}

### 端點

```json
POST /_plugins/_notifications/configs
```

### 請求本文欄位

下表列出可用的請求本文欄位。

欄位 | 資料類型 | 說明
:--- | :--- | :---
`config_id` | 字串 | 組態 ID。有效字元為字母、數字、`+`、`/`、`_` 和 `-`。選用。若省略，OpenSearch 會產生 ID。
`config` | 物件 | 組態。必要。

`config` 物件包含下列欄位。

欄位 | 資料類型 | 說明
:--- | :--- | :---
`name` | 字串 | 組態名稱。必要。
`description` | 字串 | 組態說明。選用。預設為空字串。
`config_type` | 字串 | 組態類型。有效值為 `slack`、`chime`、`microsoft_teams`、`webhook`、`email`、`sns`、`smtp_account`、`ses_account` 和 `email_group`。必要。
`is_enabled` | 布林值 | 是否啟用此頻道。OpenSearch 不會將通知傳送至已停用的頻道。選用。預設為 `true`。
`<config_type>` | 物件 | 該組態類型的設定。欄位名稱必須與 `config_type` 值相符，例如，當 `config_type` 為 `slack` 時，欄位名稱為 `"slack": { ... }`。必要。各類型的欄位將在下列各節中說明。

#### Slack、Amazon Chime 與 Microsoft Teams

`slack`、`chime` 與 `microsoft_teams` 物件包含以下欄位。

欄位 | 資料類型 | 說明
:--- | :--- | :---
`url` | 字串 | 傳入 webhook 的 URL。必要。Slack URL 必須包含 `hooks.slack.com/services/` 或 `hooks.gov-slack.com/services/`。Amazon Chime URL 必須包含 `hooks.chime.aws/incomingwebhooks/` 與 `?token=` 參數。Microsoft Teams URL 的網域必須是 `webhook.office.com`、`powerplatform.com` 或 `logic.azure.com`。

#### 自訂 webhook

`webhook` 物件包含下列欄位。

欄位 | 資料類型 | 說明
:--- | :--- | :---
`url` | 字串 | webhook 的 URL。必須使用 `http` 或 `https` 通訊協定。必要。
`header_params` | 物件 | 隨每個請求一併傳送的 HTTP 標頭，以標頭名稱與值的成對方式指定。選用。
`method` | 字串 | HTTP 方法。有效值為 `POST`、`PUT` 與 `PATCH`。選用。預設為 `POST`。無法辨識的值會儲存為 `POST`。

#### 電子郵件頻道

`email` 物件包含下列欄位。寄件者與收件者群組必須先存在，才能建立頻道。

欄位 | 資料類型 | 說明
:--- | :--- | :---
`email_account_id` | 字串 | 傳送電子郵件的 `smtp_account` 或 `ses_account` 組態 ID。必要。
`recipient_list` | 物件陣列 | 收件者。每個物件包含一個 `recipient` 欄位，用於指定電子郵件地址。選用。
`email_group_id_list` | 字串陣列 | 要傳送電子郵件至的 `email_group` 組態 ID。選用。

#### Amazon SNS

`sns` 物件包含下列欄位。

欄位 | 資料類型 | 說明
:--- | :--- | :---
`topic_arn` | 字串 | Amazon SNS 主題的 ARN，格式為 `arn:aws:sns:<region>:<account_id>:<topic_name>`。必要。
`role_arn` | 字串 | OpenSearch 為了發佈至主題而擔任的 IAM 角色的 ARN。選用。若省略，OpenSearch 會使用叢集節點上可用的 AWS 認證資訊。如需詳細資訊，請參閱[將 Amazon SNS 作為頻道類型]({{site.url}}{{site.baseurl}}/observing-your-data/notifications/index/#amazon-sns-as-a-channel-type)。

#### SMTP 寄件者

`smtp_account` 物件包含下列欄位。

欄位 | 資料類型 | 說明
:--- | :--- | :---
`host` | 字串 | SMTP 伺服器主機。必要。
`port` | 整數 | SMTP 伺服器連接埠。必須是正整數。必要。
`method` | 字串 | 加密方式。有效值為 `none`、`ssl` 與 `start_tls`。必要。無法辨識的值會儲存為 `none`。若要使用 `ssl` 或 `start_tls`，請將寄件者帳戶的認證資訊加入 OpenSearch keystore。如需更多資訊，請參閱[驗證寄件者帳戶]({{site.url}}{{site.baseurl}}/observing-your-data/notifications/index/#authenticate-sender-account)。
`from_address` | 字串 | 寄件者電子郵件地址。必要。

#### Amazon SES 寄件者

`ses_account` 物件包含下列欄位。

欄位 | 資料類型 | 說明
:--- | :--- | :---
`region` | 字串 | Amazon SES 帳戶的 AWS 區域。必要。
`role_arn` | 字串 | OpenSearch 為傳送電子郵件而擔任的 IAM 角色 ARN。選用。
`from_address` | 字串 | 寄件者電子郵件地址。必要。

#### 電子郵件收件人群組

`email_group` 物件包含下列欄位。

欄位 | 資料類型 | 描述
:--- | :--- | :---
`recipient_list` | 物件陣列 | 收件者。每個物件包含一個指定電子郵件地址的 `recipient` 欄位。必要。

### 範例：建立 Slack 頻道

```json
POST /_plugins/_notifications/configs
{
  "config_id": "sample-id",
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
{% include copy-curl.html %}

### 範例：建立自訂 webhook 頻道

```json
POST /_plugins/_notifications/configs
{
  "config_id": "sample-webhook-id",
  "config": {
    "name": "Sample Webhook Channel",
    "config_type": "webhook",
    "webhook": {
      "url": "https://custom-webhook-test-url.com:8888/test-path?params1=value1&params2=value2",
      "header_params": {
        "Content-Type": "application/json"
      },
      "method": "POST"
    }
  }
}
```
{% include copy-curl.html %}

### 範例：建立電子郵件頻道

電子郵件頻道需要電子郵件寄件者。下列請求會建立 SMTP 寄件者：

```json
POST /_plugins/_notifications/configs
{
  "config_id": "sample-smtp-id",
  "config": {
    "name": "sample-smtp-sender",
    "config_type": "smtp_account",
    "smtp_account": {
      "host": "smtp.example.com",
      "port": 587,
      "method": "start_tls",
      "from_address": "alerts@example.com"
    }
  }
}
```
{% include copy-curl.html %}

下列請求會建立電子郵件收件者群組：

```json
POST /_plugins/_notifications/configs
{
  "config_id": "sample-email-group-id",
  "config": {
    "name": "sample-email-group",
    "config_type": "email_group",
    "email_group": {
      "recipient_list": [
        {
          "recipient": "test-email1@test.com"
        },
        {
          "recipient": "test-email2@test.com"
        }
      ]
    }
  }
}
```
{% include copy-curl.html %}

下列請求會建立一個電子郵件頻道，透過 SMTP 寄件者將訊息傳送給一位收件者以及該收件者群組：

```json
POST /_plugins/_notifications/configs
{
  "config_id": "sample-email-id",
  "config": {
    "name": "Sample Email Channel",
    "description": "Sample email description",
    "config_type": "email",
    "is_enabled": true,
    "email": {
      "email_account_id": "sample-smtp-id",
      "recipient_list": [
        {
          "recipient": "sample@email.com"
        }
      ],
      "email_group_id_list": ["sample-email-group-id"]
    }
  }
}
```
{% include copy-curl.html %}

若要使用 Amazon SES 寄件者，請建立 `ses_account` 組態，並在 `email_account_id` 中指定其 ID。下列請求會建立 Amazon SES 寄件者：

```json
POST /_plugins/_notifications/configs
{
  "config_id": "sample-ses-id",
  "config": {
    "name": "sample-ses-sender",
    "config_type": "ses_account",
    "ses_account": {
      "region": "us-east-1",
      "role_arn": "arn:aws:iam::012345678912:role/NotificationsSESRole",
      "from_address": "test@email.com"
    }
  }
}
```
{% include copy-curl.html %}

### 範例：建立 Amazon SNS 頻道

```json
POST /_plugins/_notifications/configs
{
  "config_id": "sample-sns-id",
  "config": {
    "name": "Sample SNS Channel",
    "config_type": "sns",
    "sns": {
      "topic_arn": "arn:aws:sns:us-east-1:012345678912:sample-topic",
      "role_arn": "arn:aws:iam::012345678912:role/NotificationsSNSRole"
    }
  }
}
```
{% include copy-curl.html %}

### 範例回應

回應包含組態 ID：

```json
{
  "config_id" : "sample-id"
}
```

## 取得頻道組態

若要依 ID 取得通知組態，請傳送 GET 請求，並將 `config_id` 指定為路徑參數。

### 端點

```json
GET /_plugins/_notifications/configs/{config_id}
```

### 路徑參數

下表列出可用的路徑參數。

參數 | 資料類型 | 說明
:--- | :--- | :---
`config_id` | 字串 | 組態 ID。必要。

### 範例請求

```json
GET /_plugins/_notifications/configs/sample-id
```
{% include copy-curl.html %}

### 範例回應

此回應的格式與[列出所有通知組態](#list-all-notification-configurations)回應相同：

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

## 更新頻道組態

若要更新現有的通知組態，請向 `configs` 資源傳送 PUT 請求，並將該組態的 `config_id` 指定為路徑參數。請求本文包含 `config` 物件，其欄位與[建立請求](#create-channel-configuration)中的欄位相同。更新會取代整個組態，因此請指定所有欄位，包括您未變更的欄位。您省略的欄位會重設為其預設值。

您無法變更現有組態的 `config_type`。指定不同 `config_type` 的請求會失敗，並傳回 `409 Conflict` 狀態。如果 `config_id` 不存在，請求會失敗，並傳回 `404 Not Found` 狀態。若要建立組態，請使用[建立頻道組態](#create-channel-configuration) API。
{: .note}

### 端點

```json
PUT /_plugins/_notifications/configs/{config_id}
```

### 路徑參數

下表列出可用的路徑參數。

參數 | 資料類型 | 說明
:--- | :--- | :---
`config_id` | 字串 | 要更新的組態 ID。必要。

### 範例請求

```json
PUT /_plugins/_notifications/configs/sample-id
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
{% include copy-curl.html %}

### 範例回應

```json
{
  "config_id" : "sample-id"
}
```

## 刪除頻道組態

若要刪除一或多個通知組態，請傳送 DELETE 請求至 `configs` 資源。以路徑參數指定單一 ID，或在 `config_id_list` 查詢參數中指定以逗號分隔的 ID 清單。如果任何指定的組態不存在，請求就會失敗，且 OpenSearch 不會刪除其中任何組態。

OpenSearch 不會檢查其他組態是否使用您要刪除的組態。例如，您可以刪除電子郵件頻道正在使用的電子郵件寄件者。

### 端點

```json
DELETE /_plugins/_notifications/configs/{config_id}
DELETE /_plugins/_notifications/configs?config_id_list=<config_id1>,<config_id2>
```

### 路徑參數

下表列出可用的路徑參數。

參數 | 資料類型 | 說明
:--- | :--- | :---
`config_id` | 字串 | 要刪除的組態 ID。

### 查詢參數

下表列出可用的查詢參數。

參數 | 資料類型 | 說明
:--- | :--- | :---
`config_id_list` | 字串 | 要刪除的組態 ID，以逗號分隔的清單。若指定此參數，OpenSearch 會忽略 `config_id` 路徑參數。

### 範例請求

```json
DELETE /_plugins/_notifications/configs/sample-id
```
{% include copy-curl.html %}

### 回應範例

```json
{
  "delete_response_list" : {
    "sample-id" : "OK"
  }
}
```

### 範例：刪除多個組態

```json
DELETE /_plugins/_notifications/configs?config_id_list=sample-id,sample-id2,sample-id3
```
{% include copy-curl.html %}

#### 回應範例

```json
{
  "delete_response_list" : {
    "sample-id" : "OK",
    "sample-id2" : "OK",
    "sample-id3" : "OK"
  }
}
```

## 傳送測試通知

若要將測試訊息傳送至頻道，請向 `feature/test` 資源傳送 POST 請求，並以路徑參數指定頻道的 `config_id`。頻道必須已啟用，且類型必須為 `slack`、`chime`、`microsoft_teams`、`webhook`、`email` 或 `sns`。電子郵件寄件者與電子郵件收件者群組無法接收測試訊息。

測試訊息標題為 `Test Message Title-<config_id>`，訊息本文為 `Test message content body for config id <config_id>`。

若 OpenSearch 成功傳遞訊息，請求會傳回 `200 OK` 狀態。若傳遞失敗，例如目的地無法連線或拒絕訊息，請求會傳回錯誤。錯誤內容包含目的地傳回的傳遞狀態。

### 端點

```json
POST /_plugins/_notifications/feature/test/{config_id}
```

### 路徑參數

下表列出可用的路徑參數。

參數 | 資料類型 | 說明
:--- | :--- | :---
`config_id` | 字串 | 要傳送測試訊息的頻道 ID。必要。

### 範例請求

```json
POST /_plugins/_notifications/feature/test/sample-webhook-id
```
{% include copy-curl.html %}

### 範例回應

```json
{
  "event_source" : {
    "title" : "Test Message Title-sample-webhook-id",
    "reference_id" : "sample-webhook-id",
    "severity" : "info",
    "tags" : [ ]
  },
  "status_list" : [
    {
      "config_id" : "sample-webhook-id",
      "config_type" : "webhook",
      "config_name" : "Sample Webhook Channel",
      "email_recipient_status" : [ ],
      "delivery_status" : {
        "status_code" : "200",
        "status_text" : "ok"
      }
    }
  ]
}
```

### 回應本文欄位

下表列出所有回應本文欄位。

欄位 | 資料類型 | 說明
:--- | :--- | :---
`event_source` | 物件 | 測試訊息的相關資訊。
`status_list` | 物件陣列 | 每個頻道的傳遞狀態。

`event_source` 物件包含下列欄位。

欄位 | 資料類型 | 說明
:--- | :--- | :---
`title` | 字串 | 訊息標題。
`reference_id` | 字串 | 訊息來源的 ID。若為測試訊息，則為頻道 ID。
`severity` | 字串 | 訊息嚴重性。
`tags` | 字串陣列 | 訊息標籤。

`status_list` 陣列中的每個物件都包含下列欄位。

欄位 | 資料類型 | 說明
:--- | :--- | :---
`config_id` | 字串 | 頻道 ID。
`config_type` | 字串 | 頻道類型。
`config_name` | 字串 | 頻道名稱。
`email_recipient_status` | 物件陣列 | 若為電子郵件頻道，則為每個收件者的傳遞狀態。每個物件都包含一個 `recipient` 欄位和一個 `delivery_status` 物件。若為其他頻道類型則為空。
`delivery_status` | 物件 | 傳遞狀態。

`delivery_status` 物件包含下列欄位。

欄位 | 資料類型 | 說明
:--- | :--- | :---
`status_code` | 字串 | 目的地傳回的狀態碼。
`status_text` | 字串 | 目的地傳回的回應文字。
