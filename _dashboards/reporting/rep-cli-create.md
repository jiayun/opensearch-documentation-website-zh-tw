---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "建立與請求視覺化報告"
nav_order: 15
parent: Reporting using the CLI
grand_parent: Reporting
redirect_from:
  - /reporting/rep-cli-create/
  - /dashboards/reporting-cli/rep-cli-create/
---

# 建立與請求視覺化報告

若要產生報告，請將您想擷取的儀表板、視覺化、筆記本或已儲存搜尋的 OpenSearch Dashboards URL 提供給 Reporting CLI。

## 取得 URL

若要取得 URL，請依照下列步驟操作：

1. 在 OpenSearch Dashboards 中，開啟儀表板、視覺化、筆記本或已儲存的搜尋。
1. 在頂端功能表中，選取 **Share** > **Permalinks**。
1. 在 **Generate the link as** 中，選取 **Saved object**。
1. 選取 **Copy link**。

   ![Copy link]({{site.url}}{{site.baseurl}}/images/dashboards/dash-url.png)

**Saved object** 連結會經過百分比編碼，並包含頁面的時間範圍。**Snapshot** 連結也會包含目前的篩選條件與查詢，但可能含有 shell 會解讀的字元，例如 `'` 和 `!`。將 URL 傳遞給 `-u` 選項時，請以單引號括住 URL。若要使用含有單引號的 Snapshot 連結，請將 URL 儲存在 `.env` 檔案的 `OPENSEARCH_URL` 變數中。如需詳細資訊，請參閱[搭配 Reporting CLI 使用環境變數]({{site.url}}{{site.baseurl}}/dashboards/reporting/rep-cli-env-var/)。

請勿使用以 **Short URL** 選項產生的連結。Reporting CLI 會使用 URL 路徑判斷報告來源，因此對於短 URL，報告會包含 OpenSearch Dashboards 標頭與按鈕。
{: .note}

如果 URL 未包含時間範圍，報告會使用 OpenSearch Dashboards 的預設時間範圍。

## 範例：下載 PDF 報告

下列命令會將儀表板的 PDF 報告下載到目前目錄：

```bash
opensearch-reporting-cli -u '<dashboards-url>'
```
{% include copy.html %}

PDF 是預設格式。若您未指定檔案名稱，報告會儲存為 `opensearch-report-<timestamp>.pdf`。下圖顯示 PDF 報告的範例。

![PDF example]({{site.url}}{{site.baseurl}}/images/dashboards/cli-pdf-report.png)

## 範例：下載長儀表板的 PNG 報告

OpenSearch Dashboards 只有在面板顯示於瀏覽器視窗中時才會載入這些面板。根據預設，視窗高度為 600 像素，因此長儀表板下半部的面板在報告中可能會顯示為空白。若要擷取所有面板，請將 `-l` 選項設為足以容納整個儀表板的高度：

```bash
opensearch-reporting-cli -u '<dashboards-url>' -f png -l 2200 -n web-traffic
```
{% include copy.html %}

報告會儲存為 `web-traffic.png`。如果目前目錄中已存在同名檔案，Reporting CLI 不會覆寫該檔案，且命令會執行失敗。

## 範例：下載已儲存搜尋的 CSV 報告

僅已儲存的搜尋支援 CSV 報告。若要下載 CSV 報告，請提供已儲存搜尋的 URL，並將視窗寬度設定為 `800`：

```bash
opensearch-reporting-cli -u '<saved-search-url>' -f csv -w 800 -n orders
```
{% include copy.html %}

Reporting CLI 會在 **Discover** 中選取 **Reporting** > **Generate CSV** 來產生 CSV 報告。若在頁面載入後將視窗調整為其他任何寬度，**Reporting** 選單將不會顯示，且命令會失敗並出現錯誤 `No element found for selector: button[id="downloadReport"]`。
{: .note}

## 範例：使用基本驗證請求報告

如果已啟用 Security 外掛程式，請提供驗證類型與認證資訊。下列命令使用基本驗證來請求 PDF 報告：

```bash
opensearch-reporting-cli -u '<dashboards-url>' -a basic -c '<username>:<password>'
```
{% include copy.html %}

若要避免在命令列上傳遞密碼，請改用 `OPENSEARCH_USERNAME` 與 `OPENSEARCH_PASSWORD` 環境變數，而不是 `-c` 選項。

## 範例：使用 SMTP 透過電子郵件傳送報表

下列命令會產生 PDF 報表，並使用 SMTP 伺服器將報表以附件形式傳送給指定的收件者：

```bash
opensearch-reporting-cli -u '<dashboards-url>' -e smtp --smtphost <smtp-host> --smtpport <smtp-port> --smtpusername <smtp-username> --smtppassword <smtp-password> -s <sender-email> -r <recipient-email>
```
{% include copy.html %}

電子郵件包含頁面的影像、OpenSearch Dashboards 中該頁面的連結，以及作為附件的報表。報表也會儲存至目前的目錄。若要將電子郵件傳送給多位收件者，請以逗號分隔電子郵件地址。若要變更電子郵件的主旨和本文，請使用 `--subject` 和 `--note` 選項。`--note` 選項接受字串或文字檔案的路徑。

## 範例：使用 Amazon SES 以電子郵件傳送報告

下列命令會產生 PNG 報告，並使用 Amazon SES 傳送：

```bash
opensearch-reporting-cli -u '<dashboards-url>' -f png -e ses -s <sender-email> -r <recipient-email>
```
{% include copy.html %}

Amazon SES 需要 AWS 認證資訊與已驗證的寄件者地址。如需更多資訊，請參閱 [使用 Amazon SES 請求附有報告附件的電子郵件]({{site.url}}{{site.baseurl}}/dashboards/reporting/rep-cli-env-var/#using-amazon-ses-to-request-an-email-with-a-report-attachment)。

如需所有可用選項，請參閱 [Reporting CLI 選項]({{site.url}}{{site.baseurl}}/dashboards/reporting/rep-cli-options/)。
