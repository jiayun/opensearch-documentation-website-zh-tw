---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "搭配 Reporting CLI 使用環境變數"
nav_order: 35
parent: Reporting using the CLI
grand_parent: Reporting
redirect_from:
  - /reporting/rep-cli-env-var/
  - /dashboards/reporting-cli/rep-cli-env-var/
---

# 搭配 Reporting CLI 使用環境變數

除了在命令列提供值之外，您也可以將這些值設為環境變數。如需具有對應環境變數的選項清單，請參閱 [Reporting CLI 選項]({{site.url}}{{site.baseurl}}/dashboards/reporting/rep-cli-options/)。

您可以用下列任一方式設定環境變數：

- 在您的 shell 中匯出環境變數，例如 `export OPENSEARCH_FROM=reports@example.com`。
- 將環境變數儲存在您執行 Reporting CLI 所在目錄中名為 `.env` 的檔案。Reporting CLI 只會從目前目錄讀取 `.env` 檔案。

在 `.env` 檔案中，請使用 `NAME=VALUE` 格式，每行一個變數。以 `#` 開頭的行是註解。若要在值中包含 `#`、`'` 或 `!` 等字元，請將值以雙引號括住。引號不會包含在值中。

當同一個值在多處設定時，Reporting CLI 會依下列優先順序採用：

1. 命令列選項
1. 在 shell 中匯出的環境變數
1. `.env` 檔案中的變數

例如，若 `.env` 檔案設定了 `OPENSEARCH_FILENAME=test`，而您使用 `--filename report` 選項執行命令，則報告會儲存為 `report.pdf`。

## 範例：使用 .env 檔案請求報告

下列 `.env` 檔案會指定 URL、報告檔案名稱及認證資訊：

```
OPENSEARCH_URL="<dashboards-url>"
OPENSEARCH_FILENAME=daily-traffic
OPENSEARCH_USERNAME=<username>
OPENSEARCH_PASSWORD=<password>
```

若要使用 `.env` 檔案中的值請求 PNG 報告，請在包含該檔案的目錄中執行下列命令：

```bash
opensearch-reporting-cli --format png --auth basic
```
{% include copy.html %}

報告會以 `daily-traffic.png` 為名稱儲存到目前目錄。

## 使用 SMTP 以電子郵件傳送報告

若要使用 SMTP 以電子郵件傳送報告，請在您的 `.env` 檔案中設定以下變數：

```
OPENSEARCH_TRANSPORT=smtp
OPENSEARCH_SMTP_HOST=<smtp-host>
OPENSEARCH_SMTP_PORT=<smtp-port>
OPENSEARCH_SMTP_SECURE=true
OPENSEARCH_SMTP_USERNAME=<smtp-username>
OPENSEARCH_SMTP_PASSWORD=<smtp-password>
OPENSEARCH_FROM=<sender-email>
OPENSEARCH_TO=<recipient-email>
```

然後執行下列命令：

```bash
opensearch-reporting-cli --url '<dashboards-url>'
```
{% include copy.html %}

如果您的 SMTP 伺服器不需要驗證，請省略 `OPENSEARCH_SMTP_USERNAME` 與 `OPENSEARCH_SMTP_PASSWORD`。

## 使用 Amazon SES 請求附有報告附件的電子郵件

若要使用 Amazon SES 作為電子郵件傳輸方式，必須符合下列先決條件：

- 寄件者的電子郵件地址必須經過 [Amazon SES](https://aws.amazon.com/ses/) 驗證。
- Reporting CLI 會從您的 AWS 組態讀取 AWS 認證資訊與 AWS 區域。若要使用 [AWS Command Line Interface (AWS CLI)](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-welcome.html) 設定這些項目，請參閱 AWS Command Line Interface 使用者指南中的 [Quick configuration with `aws configure`](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html#cli-configure-quickstart-config)。
- AWS 認證資訊必須授予 `ses:SendRawEmail` 權限：

  ```json
  {
    "Statement": [
      {
        "Effect": "Allow",
        "Action": "ses:SendRawEmail",
        "Resource": "*"
      }
    ]
  }
  ```

下列命令會請求附有報告的電子郵件：

```bash
opensearch-reporting-cli --url '<dashboards-url>' --transport ses --from <sender-email> --to <recipient-email>
```
{% include copy.html %}

或者，在您的 `.env` 檔案中設定 `OPENSEARCH_TRANSPORT`、`OPENSEARCH_FROM` 和 `OPENSEARCH_TO`，並只提供 URL：

```bash
opensearch-reporting-cli --url '<dashboards-url>'
```
{% include copy.html %}

## 自訂電子郵件

若要變更電子郵件的主旨與內文，請使用 `--subject` 與 `--note` 選項，或 `OPENSEARCH_EMAIL_SUBJECT` 與 `OPENSEARCH_EMAIL_NOTE` 變數。若要變更電子郵件的版面配置，請編輯 Reporting CLI 安裝目錄中的 `src/views/index.hbs` 範本。

## 疑難排解

若要解決 **MessageRejected: Email address is not verified**，請參閱 AWS Knowledge Center 中的 [為什麼我從 Amazon SES 收到 400「message rejected」錯誤，且訊息為「Email address is not verified」？](https://repost.aws/knowledge-center/ses-554-400-message-rejected-error)。
