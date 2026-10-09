---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "通知"
nav_order: 140
has_children: true
redirect_from:
  - /notifications-plugin/
  - /notifications-plugin/index/
  - /observing-your-data/notifications/
---

# 通知

Notifications 外掛程式提供一個集中位置，管理來自 OpenSearch 外掛程式的所有通知。透過此外掛程式，您可以設定要使用的通訊服務，並檢視相關的統計資料與疑難排解資訊。目前，Alerting 與 ISM 外掛程式已與 Notifications 外掛程式整合。

## 安裝

Notifications 外掛程式已內建於所有標準 OpenSearch 發行版中，不需要另外安裝。如果您使用的是 OpenSearch 的精簡發行版，可以手動安裝此外掛程式。如需管理外掛程式的更多資訊，請參閱[管理 OpenSearch 外掛程式]({{site.url}}{{site.baseurl}}/install-and-configure/plugins/)。

## 設定通知

您可以使用 OpenSearch Dashboards 或 REST API 來設定通知。Dashboards 提供更有條理的方式來選取頻道類型，以及選擇要使用的 OpenSearch 外掛程式來源；而 REST API 則讓您以程式化方式定義通知頻道，便於版本管理與日後重複使用。

1. 使用 Dashboards UI 先建立一個頻道，以接收來自其他外掛程式的通知。支援的通訊頻道包括 Amazon Chime、Amazon Simple Notification Service (Amazon SNS)、Amazon Simple Email Service (Amazon SES)、透過 SMTP 傳送的電子郵件、Slack、Microsoft Teams，以及自訂 webhook。設定好頻道與外掛程式來源後，即可傳送訊息，並從 Notifications 外掛程式的儀表板開始追蹤您的通知。

2. 使用 Notifications REST API 來設定頻道的所有設定。若要使用此 API，您必須準備通知的名稱、描述、頻道類型、要作為來源的 OpenSearch 外掛程式，以及其他相關的 URL 或群組。

## 建立頻道

在 OpenSearch Dashboards 中，依序選擇 **Notifications**、**Channels** 與 **Create channel**。

1. 在 **Name and description** 區段中，為您的頻道指定名稱與選用的描述。
2. 在 **Configurations** 區段中，選取頻道類型，並輸入每種類型所需的資訊。如需設定使用 Amazon SNS 或電子郵件的頻道的更多資訊，請參閱下列章節。若要使用 Amazon Chime 或 Slack，您需要指定 webhook URL。如需使用 webhook 的更多資訊，請參閱 [Slack](https://docs.slack.dev/messaging/sending-messages-using-incoming-webhooks/)、[Microsoft Teams](https://learn.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/what-are-webhooks-and-connectors) 或 [Amazon Chime](https://docs.aws.amazon.com/chime/latest/ug/webhooks.html) 的文件。

若要使用自訂 webhook，您必須指定更多資訊：參數與標頭。例如，如果您的端點需要基本驗證，可能需要新增一個標頭，其授權金鑰的值為 `Basic <Base64-encoded-credential-string>`。您可能也需要將 `Content-Type` 變更為您的 webhook 所需的值。常見的值有 `application/json`、`application/xml` 與 `text/plain`。

這些資訊會以純文字形式儲存在 OpenSearch 叢集中。我們未來會改善此設計，但目前編碼後的憑證（未加密也未雜湊）可能會被其他 OpenSearch 使用者看到。

1. 在 **Availability** 區段中，選取您要與通知頻道搭配使用的 OpenSearch 外掛程式。
2. 選擇 **Create**。

### Amazon SNS 作為頻道類型

OpenSearch 支援使用 Amazon SNS 傳送通知。與 Amazon SNS 的這項整合意味著，除了其他頻道類型之外，Notifications 外掛程式還可以透過 SNS 主題傳送電子郵件訊息、簡訊，甚至執行 AWS Lambda 函式。如需 Amazon SNS 的更多資訊，請參閱 [Amazon Simple Notification Service 開發人員指南](https://docs.aws.amazon.com/sns/latest/dg/welcome.html)。

Notifications 外掛程式支援兩種驗證使用者的方式：

1. 給予使用者完整的 Amazon SNS 存取權限。
2. 讓使用者擔任具有 Amazon SNS 存取權限的 AWS Identity and Access Management (IAM) 角色。設定通知頻道使用正確的 Amazon SNS 權限後，選取可以觸發通知的 OpenSearch 外掛程式。

### 提供完整的 Amazon SNS 存取權限

若要提供 IAM 使用者完整的 Amazon SNS 存取權限，請確保該使用者具有下列權限：

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "sns:*"
      ],
      "Effect": "Allow",
      "Resource": "*"
    }
  ]
}
```

### 擔任具有 Amazon SNS 權限的 IAM 角色

若要讓使用者不必直接擁有完整的 Amazon SNS 權限即可傳送通知，可以讓使用者擔任具有必要權限的角色。

IAM 使用者必須具有下列權限才能擔任角色：

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ec2:Describe*",
        "iam:ListRoles",
        "sts:AssumeRole"
      ],
      "Resource": "*"
    }
  ]
}
```

然後將此政策加入 IAM 使用者的信任關係中，以實際擔任該角色：

```json
{
  "Version": "2012-10-17",
  "Statement": [
  {
    "Effect": "Allow",
    "Principal": {
    "AWS": "arn:aws:iam::<arn_number>:user/<iam_username>",
    },
    "Action": "sts:AssumeRole"
  }
  ]
}
```

### 主機拒絕清單

定義 OpenSearch 節點不應對其發起請求的 IP 範圍或主機名稱。

## 電子郵件作為頻道類型

若要透過電子郵件傳送或接收通知，請選擇 **Email** 作為頻道類型。接著，至少選取一個寄件者與預設收件者。若要一次傳送通知給多人，請指定多個電子郵件地址，或選取收件者群組。如果 Notifications 外掛程式目前沒有必要的寄件者或群組，您可以先選取 **SMTP sender**，然後選擇 **Create SMTP sender** 或 **Create recipient group** 來新增。若要使用 Amazon Simple Email Service (Amazon SES)，請選擇 **SES sender**。

### 建立電子郵件寄件者

1. 指定要與寄件者關聯的唯一名稱。
2. 輸入電子郵件地址，以及（若適用）其主機（例如 smtp.gmail.com）與連接埠。如果您使用 Amazon SES，請輸入用於傳送通知的 AWS 帳戶的 IAM 角色 Amazon Resource Name (ARN)，以及 AWS Region。
3. 選擇加密方法。大多數電子郵件供應商要求 Secure Sockets Layer (SSL) 或 Transport Layer Security (TLS)，這需要在 OpenSearch keystore 中提供使用者名稱與密碼。請參閱[驗證寄件者帳戶](#authenticate-sender-account)以了解更多。只有建立 SMTP 寄件者時才需要選擇加密方法。
4. 選擇 **Create** 以儲存組態並建立寄件者。您可以在將憑證加入 OpenSearch keystore 之前先建立寄件者；但在頻道組態中使用該寄件者之前，必須先[驗證每個寄件者帳戶](#authenticate-sender-account)。

### 建立電子郵件收件者群組

1. 選擇 **Create recipient group** 後，輸入要與電子郵件群組關聯的唯一名稱，以及選用的描述。
2. 選取或輸入要加入收件者群組的電子郵件地址。
3. 選擇 **Create**。

### 驗證寄件者帳戶

如果您的電子郵件供應商要求 SSL 或 TLS，您必須先驗證每個寄件者帳戶，才能傳送電子郵件。請使用命令列介面 (CLI) 在 OpenSearch keystore 中輸入寄件者帳戶的憑證。執行下列命令（在您的 OpenSearch 目錄中）以輸入使用者名稱與密碼。&lt;sender_name&gt; 是您先前在 **Sender** 中輸入的名稱。

```json
/usr/share/opensearch/bin/opensearch-keystore add opensearch.notifications.core.email.<sender_name>.username
/usr/share/opensearch/bin/opensearch-keystore add opensearch.notifications.core.email.<sender_name>.password
```

若要變更或更新您的憑證（在您已將憑證加入每個節點的 keystore 之後），請呼叫 reload API，即可自動更新這些憑證，而不需重新啟動 OpenSearch。

```json
POST _nodes/reload_secure_settings
{
  "secure_settings_password": "1234"
}
```
