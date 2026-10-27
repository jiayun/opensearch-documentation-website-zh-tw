---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "報告"
nav_order: 75
has_children: true
has_toc: false
redirect_from:
  - /dashboards/reporting/
  - /reporting/
  - /reporting/index/
---

# 報告

您可以使用報告功能，從儀表板、視覺化、已儲存的搜尋和筆記本產生 PDF、PNG、CSV 和 XLSX 報告，可依需求產生或依排程產生。所有報告皆由 OpenSearch Dashboards 轉譯，因此即使您使用 API 或 CLI 產生報告，報告功能仍需要執行中的 OpenSearch Dashboards 執行個體。

若要在不建立報告的情況下下載搜尋結果或已儲存的物件，請參閱[匯出資料]({{site.url}}{{site.baseurl}}/dashboards/exporting-data/)。

## 報表定義與報表

報表功能使用兩個概念：

- **報表定義**是已儲存的組態，指定要擷取的儀表板、視覺化、已儲存的搜尋或筆記本，以及檔案格式、時間範圍和選用的排程。您可以重複使用報表定義，隨需或依週期性排程產生報表。
- **報表**是根據報表定義或透過單次下載所產生的檔案。

刪除報表定義不會刪除根據該定義產生的報表。

## 報表來源與檔案格式

可用的檔案格式取決於報表來源。儀表板、視覺化與筆記本會擷取為轉譯後的圖片。儲存的搜尋則匯出為查詢傳回的資料列。

| 報表來源 | 檔案格式 |
| :--- | :--- |
| 儀表板 | PDF、PNG |
| 視覺化 | PDF、PNG |
| 筆記本 | PDF、PNG |
| 儲存的搜尋 | CSV、XLSX |

若要下載視覺化背後的資料，請參閱[匯出視覺化資料]({{site.url}}{{site.baseurl}}/dashboards/exporting-data/#exporting-visualization-data)。

CSV 與 XLSX 報表預設最多包含 10,000 列。若要變更此限制，請在建立報表定義時設定記錄上限。報表沒有明確的大小限制，但極大的文件可能會導致報表產生失敗，並出現 V8 JavaScript 引擎的記憶體不足錯誤。
{: .tip }

## 選擇方法

下表列出產生報告的方式。

| 方法 | 用途 | 是否需要 Reporting 外掛程式 |
| :--- | :--- | :--- |
| [OpenSearch Dashboards]({{site.url}}{{site.baseurl}}/dashboards/reporting/report-dashboard-index/) | 從您目前檢視的頁面產生報告，並建立及管理報告定義。 | 是 |
| [Reporting CLI]({{site.url}}{{site.baseurl}}/dashboards/reporting/rep-cli-index/) | 從指令碼、cron 工作或 AWS Lambda 函式產生報告，並使用 Amazon SES 或 SMTP 以電子郵件寄送。 | 僅限 CSV 報告 |
| [Reporting API]({{site.url}}{{site.baseurl}}/dashboards/reporting/api/) | 以程式設計方式建立報告定義並產生報告。 | 是 |

## 存取控制

若要建立報告，您必須具備正確的權限。如需預先定義角色及其授予權限的摘要，請參閱[預先定義角色]({{site.url}}{{site.baseurl}}/security/access-control/users-roles/#predefined-roles)。

當報告功能啟用資源共用時，報告定義與報告的擁有者，以及具備共用權限的使用者，可以將存取權授予特定使用者、角色及後端角色。如需詳細資訊，請參閱[報告定義存取控制]({{site.url}}{{site.baseurl}}/dashboards/reporting/report-definition-access-control/)與[報告執行個體存取控制]({{site.url}}{{site.baseurl}}/dashboards/reporting/report-instance-access-control/)。
