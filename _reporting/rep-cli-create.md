---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "建立與請求視覺化報告"
nav_order: 15
parent: Reporting using the CLI
grand_parent: Reporting
redirect_from:
  - /dashboards/reporting-cli/rep-cli-create/
---

# 建立與請求視覺化報告

首先，您需要取得要下載為圖片檔或 PDF 的視覺化 URL。

若要產生視覺化報告，您需要指定 Dashboards URL。

開啟您要產生報告的視覺化，然後依序選取 **Share >  Permalinks > Generate link as Snapshot > Short URL > Copy link**，如下圖所示。

![複製連結]({{site.url}}{{site.baseurl}}/images/dashboards/dash-url.png)

在 CLI 中請求報告時，您需要使用 `-u` 引數指定該 URL。

#### 範例：請求 PNG 檔案

下列命令會以基本驗證請求 PNG 格式的報告，並使用 Amazon SES 將報告傳送至電子郵件地址：

```
opensearch-reporting-cli -u https://localhost:5601/app/dashboards#/view/7adfa750-4c81-11e8-b3d7-01146121b73d -a basic -c admin:Test@1234 -e ses -s <email address>  -r <email address> -f png
```

#### 範例：請求 PDF 檔案

下列命令會請求 PDF 檔案並指定收件者的電子郵件地址：

```
opensearch-reporting-cli -u https://localhost:5601/app/dashboards#/view/7adfa750-4c81-11e8-b3d7-01146121b73d -a basic -c admin:Test@1234 -e ses -s <email address> -r <email address> -f pdf
```

成功後，檔案將傳送至指定的電子郵件地址。下圖顯示 PDF 報告範例。

![PDF 範例]({{site.url}}{{site.baseurl}}/images/dashboards/cli-pdf-report.png)

#### 範例：請求 CSV 檔案

下列命令會產生包含 CSV 格式所有表格內容的報告，並使用 Amazon SES 傳輸方式將報告傳送至電子郵件地址：

```
opensearch-reporting-cli -u https://localhost:5601/app/dashboards#/view/7adfa750-4c81-11e8-b3d7-01146121b73d -f csv -a basic -c admin:Test@1234 -e ses -s <email address> -r <email address>
```

成功後，電子郵件將傳送至指定的電子郵件地址，並附上 CSV 檔案。
