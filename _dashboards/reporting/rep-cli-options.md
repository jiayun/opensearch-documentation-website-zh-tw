---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "Reporting CLI 選項"
nav_order: 30
parent: Reporting using the CLI
grand_parent: Reporting
redirect_from:
  - /reporting/rep-cli-options/
  - /dashboards/reporting-cli/rep-cli-options/
---

# Reporting CLI 選項

`opensearch-reporting-cli` 工具支援下列選項。選項值區分大小寫，且必須使用小寫。在命令列提供的選項優先於環境變數。如需更多資訊，請參閱[搭配 Reporting CLI 使用環境變數]({{site.url}}{{site.baseurl}}/dashboards/reporting/rep-cli-env-var/)。

| 選項 | 說明 | 環境變數 |
| :--- | :--- | :--- |
| `-u`, `--url` | 儀表板、視覺化、筆記本或已儲存搜尋的 OpenSearch Dashboards URL。若要取得 URL，請選取 **Share** > **Permalinks** > **Copy link**。必要。 | `OPENSEARCH_URL` |
| `-a`, `--auth` | 驗證類型。有效值為 `basic`、`cognito` 和 `saml`。需要認證資訊。若要在不進行驗證的情況下連線，請省略此選項。 | N/A |
| `-c`, `--credentials` | 以 `<username>:<password>` 格式提供的 OpenSearch Dashboards 登入認證資訊。 | `OPENSEARCH_USERNAME` 和 `OPENSEARCH_PASSWORD` |
| `-t`, `--tenant` | 啟用多租用戶功能時，登入後要選取的租用戶。有效值為 `private`、`global` 或自訂租用戶的名稱。URL 中指定的租用戶優先於此選項。預設為 `private`。 | N/A |
| `--multitenancy` | 是否在登入後選取租用戶。有效值為 `true` 和 `false`。預設為 `true`。 | N/A |
| `-f`, `--format` | 報表的檔案格式。有效值為 `pdf`、`png` 和 `csv`。`csv` 格式僅支援已儲存的搜尋。預設為 `pdf`。 | N/A |
| `-w`, `--width` | 瀏覽器視窗寬度，以像素為單位。預設為 `1680`。 | N/A |
| `-l`, `--height` | 瀏覽器視窗的最小高度，以像素為單位。預設為 `600`。 | N/A |
| `-n`, `--filename` | 報表的檔案名稱，不含副檔名。預設為 `opensearch-report-<timestamp>`。 | `OPENSEARCH_FILENAME` |
| `-e`, `--transport` | 電子郵件傳輸方式。有效值為 `ses`（Amazon SES）和 `smtp`。若未指定，則不會透過電子郵件傳送報表。 | `OPENSEARCH_TRANSPORT` |
| `-s`, `--from` | 寄件者的電子郵件地址。 | `OPENSEARCH_FROM` |
| `-r`, `--to` | 收件者的電子郵件地址。若要指定多位收件者，請以逗號分隔地址。 | `OPENSEARCH_TO` |
| `--smtphost` | SMTP 伺服器的主機名稱。 | `OPENSEARCH_SMTP_HOST` |
| `--smtpport` | SMTP 伺服器的連接埠。 | `OPENSEARCH_SMTP_PORT` |
| `--smtpsecure` | 指定 `true`，以在連線至 SMTP 伺服器時使用 TLS。任何值都會啟用 TLS，包括 `false`，因此若要在不使用 TLS 的情況下連線，請省略此選項。 | `OPENSEARCH_SMTP_SECURE` |
| `--smtpusername` | SMTP 使用者名稱。 | `OPENSEARCH_SMTP_USERNAME` |
| `--smtppassword` | SMTP 密碼。 | `OPENSEARCH_SMTP_PASSWORD` |
| `--selfsignedcerts` | 是否接受 SMTP 伺服器的自我簽署憑證。有效值為 `true` 和 `false`。預設為 `false`。 | N/A |
| `--subject` | 電子郵件主旨。預設為 `This is an email containing your opensearch dashboard report`。 | `OPENSEARCH_EMAIL_SUBJECT` |
| `--note` | 電子郵件本文，可以是字串或文字檔案的路徑。預設為 `Hi,\nHere is the latest report!`。 | `OPENSEARCH_EMAIL_NOTE` |
| `--timeout` | 等待頁面載入的最長時間，以毫秒為單位。預設為 `300000`（5 分鐘）。 | `OPENSEARCH_TIMEOUT` |
| `-h`, `--help` | 顯示選項清單。 | N/A |

## 取得說明

若要取得所有可用選項的清單，請執行下列命令：

```bash
opensearch-reporting-cli -h
```
{% include copy.html %}
