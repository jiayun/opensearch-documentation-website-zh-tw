---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "Reporting CLI 選項"
nav_order: 30
parent: Reporting using the CLI
grand_parent: Reporting
redirect_from:
  - /dashboards/reporting-cli/rep-cli-options/
---

# Reporting CLI 選項

您可以在 `opensearch-reporting-cli` 工具中使用下列任何引數。

| 引數      | 說明       | 可接受的值與用法 | 環境變數
:--------------------- | :--- | :--- |
`-u`, `--url` | 視覺化的 URL。 | 從 OpenSearch Dashboards > Visualize > Share > Permalinks > Copy link 取得。 | OPENSEARCH_URL
`-a`, `--auth` | 報告的驗證類型。 | 您可以指定 Basic `basic`、Cognito `cognito`、SAML `saml`，或不驗證 `none`。若未指定任何值，Reporting CLI 工具預設為不驗證，類型為 `none`。Basic、Cognito 和 SAML 需要使用 `-c` 旗標提供認證。 | N/A
`-c`, `--credentials` | OpenSearch 登入認證。 | 輸入以冒號分隔的使用者名稱和密碼。例如，username:password。Basic、Cognito 和 SAML 驗證類型為必要。 | OPENSEARCH_USERNAME 和 OPENSEARCH_PASSWORD
`-t`, `--tenant` | OpenSearch Dashboards 中的租用戶。 | 預設租用戶為 private。| N/A
`-f`, `--format` | 報告的檔案格式。 | 可以是 `pdf`、`png` 或 `csv`。預設為 `pdf`。| N/A
`-w`, `--width` | 報告的視窗寬度 (以像素為單位)。 | 預設為 `1680`。| N/A
`-l`, `--height` | 報告的視窗最小高度 (以像素為單位)。 | 預設為 `600`。 | N/A
`-n`, `--filename` | 報告的檔案名稱。 | 預設為 `reporting`。 | `opensearch-report-YYY-MM-DDTHH-mm-ss.sssZ`
`-e`, `--transport` | 傳送電子郵件的傳輸機制。 | 若為 Amazon SES，請指定 `ses`。Amazon SES 需要在您的系統上進行 AWS 組態以儲存認證。若為 SMTP，請使用 `smtp`，並使用 `--smtpusername` 和 `--smtppassword` 指定登入認證。 | OPENSEARCH_TRANSPORT
`-s`, `--from` | 寄件者的電子郵件地址。 | 例如，`user@amazon.com`。 | OPENSEARCH_FROM
`-r`, `--to` | 收件者的電子郵件地址。 | 例如，`user@amazon.com`。 | OPENSEARCH_TO
`--smtphost` | SMTP 伺服器的主機名稱。 | 例如，`SMTP_HOST`。 | OPENSEARCH_SMTP_HOST
`--smtpport` | SMTP 連線的連接埠。 | 例如，`SMTP_PORT`。 | OPENSEARCH_SMTP_PORT
`--smtpsecure` | 指定連線至伺服器時使用 TLS。 | 例如，`SMTP_SECURE`。 | OPENSEARCH_SMTP_SECURE
`--smtpusername` | SMTP 使用者名稱。| 例如，`SMTP_USERNAME`。 | OPENSEARCH_SMTP_USERNAME
`--smtppassword` | SMTP 密碼。| 例如，`SMTP_PASSWORD`。 | OPENSEARCH_SMTP_PASSWORD
`--subject` | 以引號括住的電子郵件主旨文字。 | 可以是任何字串。預設為 "This is an email containing your dashboard report"。 | OPENSEARCH_EMAIL_SUBJECT
`--note` | 電子郵件本文，可以是字串或文字檔的路徑。 | 預設註記為 "Hi,\\nHere is the latest report!" | OPENSEARCH_EMAIL_NOTE
`-h`, `--help` | 指定從命令列顯示選用引數的清單。 | N/A

## 取得協助

若要取得所有可用 CLI 引數的清單，請執行下列命令：

``` 
$ opensearch-reporting-cli -h
```