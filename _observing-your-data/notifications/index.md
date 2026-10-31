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

「通知」提供一個集中位置，用於設定 OpenSearch 外掛程式（例如 Alerting 與 Index State Management (ISM)）用來傳送通知的頻道。支援的頻道類型包括 Amazon Chime、Amazon Simple Notification Service (Amazon SNS)、透過 SMTP 或 Amazon Simple Email Service (Amazon SES) 傳送的電子郵件、Slack、Microsoft Teams，以及自訂 webhook。

## 設定通知

使用 OpenSearch Dashboards 或 REST API 來設定通知。Dashboards 會引導您選取頻道類型並輸入其設定。REST API 則讓您以程式化方式定義頻道，方便進行版本管理與重複使用。如需 API 的詳細資訊，請參閱 [Notifications API]({{site.url}}{{site.baseurl}}/observing-your-data/notifications/api/)。

## 建立頻道

若要在 OpenSearch Dashboards 中建立頻道，請依照下列步驟操作：

1. 在頂端功能表中，前往 **Management** > **Notifications**。
1. 選取 **Channels**，然後選取 **Create channel**。
1. 在 **Name and description** 區段中，輸入頻道的名稱與選用說明。
1. 在 **Configurations** 區段中，選取 **Channel type** 並輸入該類型的設定。建立頻道後即無法變更頻道類型。若為 Slack、Amazon Chime 與 Microsoft Teams，請輸入 webhook URL。如需取得 webhook URL 的詳細資訊，請參閱 [Slack](https://docs.slack.dev/messaging/sending-messages-using-incoming-webhooks/)、[Microsoft Teams](https://learn.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/what-are-webhooks-and-connectors) 或 [Amazon Chime](https://docs.aws.amazon.com/chime/latest/ug/webhooks.html) 的文件。若為其他頻道類型，請參閱下列各節。
1. （選用）若要驗證組態，請選取 **Send test message**。
1. 選取 **Create**。

### 自訂 Webhook

若要使用自訂 Webhook，請在 **Define endpoints by** 中選取 **Webhook URL** 以輸入完整 URL，或選取 **Custom attributes URL** 以分別輸入類型、主機、連接埠和路徑。接著選取 HTTP **Method**，並新增您的端點所需的任何 **Query parameters** 和 **Webhook headers**。例如，若您的端點需要基本驗證，請新增值為 `Basic <Base64-encoded-credential-string>` 的 `Authorization` 標頭。您可能還需要將 `Content-Type` 設定為 Webhook 所需的值，例如 `application/json`、`application/xml` 或 `text/plain`。

Webhook 設定（包括標頭）會以純文字形式儲存在 OpenSearch 叢集中。標頭中經過編碼的認證資訊既未加密也未雜湊處理，其他 OpenSearch 使用者可能看得到這些資訊。
{: .warning}

### 以 Amazon SNS 作為頻道類型

通知可以將訊息發布至 Amazon SNS 主題。透過 SNS 主題訂閱，您可以將通知以電子郵件訊息或簡訊形式傳送，或用來叫用 AWS Lambda 函式。如需 Amazon SNS 的詳細資訊，請參閱 [Amazon Simple Notification Service 開發人員指南](https://docs.aws.amazon.com/sns/latest/dg/welcome.html)。

若要建立 Amazon SNS 頻道，請輸入 **SNS topic ARN**，並可選擇性輸入 **IAM role ARN**。OpenSearch 會透過預設 AWS 認證提供者鏈，使用每個節點上可用的 AWS 認證資訊，例如環境變數或 Amazon EC2 執行個體設定檔。若未指定 IAM role ARN，這些認證資訊必須具備發布至該主題的權限。若指定 IAM role ARN，OpenSearch 會使用這些認證資訊來擔任該角色，然後以該角色的權限發布至該主題。

#### 使用節點認證資訊發佈

若要使用節點認證資訊發佈至主題，請授予節點所用認證資訊所屬的 IAM 使用者或角色下列權限：

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "sns:Publish",
      "Resource": "arn:aws:sns:<region>:<account_id>:<topic_name>"
    }
  ]
}
```

#### 透過擔任 IAM 角色來發佈

若要在不授予節點認證資訊直接存取 Amazon SNS 的情況下發佈至主題，請建立具有上一節所示 `sns:Publish` 權限的 IAM 角色，並在 **IAM role ARN** 中輸入其 ARN。

節點所用認證資訊所屬的 IAM 使用者或角色，必須具有擔任該角色的權限：

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "sts:AssumeRole",
      "Resource": "arn:aws:iam::<account_id>:role/<role_name>"
    }
  ]
}
```

該角色的信任政策必須允許該使用者或角色擔任它。在 `Principal` 中，指定節點所用認證資訊所屬之 IAM 使用者（`arn:aws:iam::<account_id>:user/<user_name>`）或角色（`arn:aws:iam::<account_id>:role/<role_name>`）的 ARN：

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "<node_principal_arn>"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

## 電子郵件作為通道類型

若要透過電子郵件傳送通知，請選取 **Email** 作為通道類型。接著選取一個 **Sender type**、傳送者，以及至少一名預設收件者。一個通道會使用一名傳送者，可以是 **SMTP sender**，或是透過 Amazon SES 傳送電子郵件的 **SES sender**。在 **Default recipients** 中輸入電子郵件地址，或選取收件人群組，以傳送通知給多位人士。如果該傳送者或收件人群組尚不存在，請選取 **Create SMTP sender**、**Create SES sender** 或 **Create recipient group** 來建立一個。

您也可以在 Notifications 的 **Email senders** 與 **Email recipient groups** 頁面管理傳送者與收件人群組。

### 建立電子郵件寄件者

若要建立電子郵件寄件者，請依照下列步驟操作：

1. 輸入 **Sender name**。名稱必須包含 2 到 50 個字元。有效字元為小寫字母、數字、連字號（`-`）及底線（`_`）。對於 SMTP 寄件者，此名稱也是 [驗證寄件者帳戶](#authenticate-sender-account) 中所述金鑰儲存庫設定名稱的一部分。
1. 輸入寄件者的 **Email address**。
1. 對於 SMTP 寄件者，請輸入 **Host**（例如 `smtp.gmail.com`）與 **Port**，然後選取 **Encryption method**：**SSL/TLS**、**STARTTLS** 或 **None**。大多數電子郵件供應商需要 SSL/TLS 或 STARTTLS。若要使用其中任一種，您必須將寄件者的使用者名稱與密碼新增至 OpenSearch 金鑰儲存庫。如需詳細資訊，請參閱 [驗證寄件者帳戶](#authenticate-sender-account)。
1. 對於 SES 寄件者，請輸入 OpenSearch 用來傳送電子郵件之角色的 **IAM Role ARN** 以及 **AWS region**。
1. 選取 **Create**。

您可以在將 SMTP 寄件者的認證資訊新增至 OpenSearch 金鑰儲存庫之前，先建立該寄件者。不過，您必須先[驗證寄件者帳戶](#authenticate-sender-account)，頻道才能透過該寄件者傳送電子郵件。

SES 寄件者的電子郵件地址必須是寄件者 AWS 區域中 Amazon SES 的已驗證身分。如果您的帳戶位於 Amazon SES 沙箱中，收件者地址也必須經過驗證。OpenSearch 會使用 `ses:SendRawEmail` 動作來傳送電子郵件。您在 **IAM Role ARN** 中指定的 IAM 角色必須具備下列權限，且其信任政策必須允許節點認證資訊擔任該角色，如 [透過擔任 IAM 角色來發佈](#publishing-by-assuming-an-iam-role) 所述：

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "ses:SendRawEmail",
      "Resource": "arn:aws:ses:<region>:<account_id>:identity/<sender_email_address>"
    }
  ]
}
```

### 建立電子郵件收件者群組

若要建立電子郵件收件者群組，請依照下列步驟操作：

1. 選取 **Create recipient group**。
1. 為群組輸入唯一的 **Name**，並可選擇性輸入描述。
1. 在 **Emails** 中，選取或輸入您要新增至群組的電子郵件地址。
1. 選取 **Create**。

### 驗證寄件者帳戶

如果 SMTP 寄件者使用 SSL/TLS 或 STARTTLS 加密方法，您必須先將寄件者帳戶的認證資訊新增至 OpenSearch keystore，寄件者才能傳送電子郵件。對於加密方法為 None 的寄件者，OpenSearch 不會使用 keystore 中的認證資訊。

在每個節點上，從 OpenSearch 主目錄執行下列命令，並將 `<sender_name>` 替換為您在建立寄件者時輸入的寄件者名稱。每個命令都會提示您輸入值：

```bash
./bin/opensearch-keystore add opensearch.notifications.core.email.<sender_name>.username
./bin/opensearch-keystore add opensearch.notifications.core.email.<sender_name>.password
```

若要在不重新啟動 OpenSearch 的情況下套用新的或更新的認證資訊，請在每個節點上更新 keystore 之後，呼叫 Nodes Reload Secure Settings API：

```json
POST _nodes/reload_secure_settings
```
{% include copy-curl.html %}

如果您的 keystore 受密碼保護，請在請求本文中提供密碼：

```json
POST _nodes/reload_secure_settings
{
  "secure_settings_password": "<keystore_password>"
}
```

如需詳細資訊，請參閱 [Nodes Reload Secure Settings API]({{site.url}}{{site.baseurl}}/api-reference/nodes-apis/nodes-reload-secure/)。

## 主機拒絕清單

若要防止 OpenSearch 節點將通知傳送至特定主機，請將這些主機加入 `opensearch.notifications.core.http.host_deny_list` 設定。拒絕清單適用於會傳送 HTTP 請求的頻道：Slack、Amazon Chime、Microsoft Teams 以及自訂 webhook。每個項目可以是主機名稱、IP 位址，或以 CIDR 表示法表示的 IP 位址範圍。如果目的地主機名稱符合某個項目，或該主機名稱解析出的任何 IP 位址落在某個項目範圍內，OpenSearch 就會拒絕該訊息。此設定為動態設定，預設為空。

以下請求會將一個 IP 位址範圍和一個主機名稱加入拒絕清單：

```json
PUT _cluster/settings
{
  "persistent": {
    "opensearch.notifications.core.http.host_deny_list": ["10.0.0.0/8", "internal.example.com"]
  }
}
```
{% include copy-curl.html %}

如需 Notifications 外掛程式設定的詳細資訊，請參閱 [Notifications 外掛程式設定]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/plugin-settings/#notifications-plugin-settings)。
