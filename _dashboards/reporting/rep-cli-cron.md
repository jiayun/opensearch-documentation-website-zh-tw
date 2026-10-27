---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "使用 cron 公用程式排程報告"
nav_order: 20
parent: Reporting using the CLI
grand_parent: Reporting
redirect_from:
  - /reporting/rep-cli-cron/
  - /dashboards/reporting-cli/rep-cli-cron/
---

# 使用 cron 公用程式排程報表

使用 cron 命令列公用程式依排程執行 Reporting CLI。每個 cron 項目由一個指定執行時間的 cron 運算式，以及要執行的命令組成。

若要了解 cron 運算式的語法，請參閱 [Cron expressions]({{site.url}}{{site.baseurl}}/api-reference/cron-expressions/)。若要取得 cron 的說明，請執行下列命令以開啟 man 頁面：

```bash
man crontab
```
{% include copy.html %}

## 必要條件

- 已安裝 cron 的機器。
- Reporting CLI。如需指示，請參閱[下載並安裝 Reporting CLI 工具]({{site.url}}{{site.baseurl}}/dashboards/reporting/rep-cli-install/)。

## 指定排程

Cron 執行命令時使用的 `PATH` 非常精簡，通常只包含 `/usr/bin` 和 `/bin`，因此除非您在 crontab 中設定 `PATH`，否則 cron 找不到 `node` 和 `opensearch-reporting-cli` 命令。若要找出包含這些命令的目錄，請執行下列命令：

```bash
dirname "$(command -v node)" "$(command -v opensearch-reporting-cli)"
```
{% include copy.html %}

執行下列命令以開啟 crontab 編輯器：

```bash
crontab -e
```
{% include copy.html %}

在 crontab 編輯器中，將 `PATH` 設定為包含前一個命令傳回的目錄，然後新增報告請求。下列範例會在每天上午 8:00 產生報告，並使用 Amazon SES 以電子郵件傳送：

```
PATH=/usr/local/bin:/usr/bin:/bin
0 8 * * * opensearch-reporting-cli -u '<dashboards-url>' -e ses -s <sender-email> -r <recipient-email>
```

Cron 會將命令中的每個 `%` 字元轉換為換行，而 OpenSearch Dashboards 的 URL 通常包含 `%` 字元。請以單引號括住 URL，並將 URL 中的每個 `%` 字元逸出為 `\%`。或者，您也可以依照下一節的說明，將 URL 儲存在 `.env` 檔案中。
{: .important}

如果您使用 `-n` 選項指定檔案名稱，Reporting CLI 會在第二次執行時失敗，因為已存在同名的檔案。請省略檔案名稱，讓每份報告以加上時間戳記的檔案名稱儲存，或在下次執行前刪除先前的報告。
{: .note}

## 將報表設定儲存在 .env 檔案中

您可以將 URL 和其他選項儲存在 `.env` 檔案中，取代在 cron 命令中提供這些資訊。`.env` 檔案中的值不需要跳脫。Cron 會從您的家目錄執行命令，因此請在執行 Reporting CLI 之前，先切換至包含 `.env` 檔案的目錄。

例如，建立包含下列變數的 `/home/<user>/reports/.env` 檔案：

```
OPENSEARCH_URL="<dashboards-url>"
OPENSEARCH_TRANSPORT=smtp
OPENSEARCH_SMTP_HOST=<smtp-host>
OPENSEARCH_SMTP_PORT=<smtp-port>
OPENSEARCH_FROM=<sender-email>
OPENSEARCH_TO=<recipient-email>
```

接著將下列項目新增至 crontab：

```
PATH=/usr/local/bin:/usr/bin:/bin
0 8 * * * cd /home/<user>/reports && opensearch-reporting-cli
```

如需詳細資訊，請參閱[搭配 Reporting CLI 使用環境變數]({{site.url}}{{site.baseurl}}/dashboards/reporting/rep-cli-env-var/)。
