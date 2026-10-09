---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "使用 cron 公用程式排程報告"
nav_order: 20
parent: Reporting using the CLI
grand_parent: Reporting
redirect_from:
  - /dashboards/reporting-cli/rep-cli-cron/
---

# 使用 cron 公用程式排程報告

您可以使用 cron 命令列公用程式，透過 Reporting CLI 發起報告請求，並在任何日期或時間間隔定期執行。請依照 cron 運算式語法，指定您要發起之命令前面的日期與時間。

如要了解 cron 運算式語法，請參閱 [Cron 運算式]({{site.url}}{{site.baseurl}}/api-reference/common-parameters/#cron-expressions)。如要取得 cron 的說明，請執行下列命令來開啟手冊頁面：

```
man cron
```

### 先決條件

- 您需要一部已安裝 cron 的機器。
- 您需要安裝 Reporting CLI。請參閱[下載及安裝 Reporting CLI 工具]({{site.url}}{{site.baseurl}}/dashboards/reporting-cli/rep-cli-install/)

## 指定報告詳細資料

請執行下列命令來開啟 crontab 編輯器：

```
crontab -e
```
在 crontab 編輯器中，輸入報告請求。下列範例顯示每天上午 8:00 執行的 cron 報告：

```
0 8 * * * opensearch-reporting-cli -u https://playground.opensearch.org/app/dashboards#/view/084aed50-6f48-11ed-a3d5-1ddbf0afc873 -e ses -s <sender_email> -r <recipient_email>
```