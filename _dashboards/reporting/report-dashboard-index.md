---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "使用 OpenSearch Dashboards 產生報告"
nav_order: 10
parent: Reporting
redirect_from:
  - /reporting/report-dashboard-index/
---

# 使用 OpenSearch Dashboards 產生報告

使用 OpenSearch Dashboards 從您正在檢視的頁面產生報告，並建立、管理及刪除報告定義。如需報告定義、各報告來源可用的檔案格式，以及所需權限的相關資訊，請參閱 [Reporting]({{site.url}}{{site.baseurl}}/dashboards/reporting/)。若要以程式設計方式執行這些操作，請參閱 [Reporting API]({{site.url}}{{site.baseurl}}/dashboards/reporting/api/)。

## 產生報告

若要從介面產生報告，請依照下列步驟操作：

1. 開啟您要產生報告的儀表板、視覺化、筆記本或已儲存的搜尋。
1. 在頂端選單中，選取 **Reporting**。
1. 選取格式：
   - 若為儀表板、視覺化及筆記本，請選取 **Download PDF** 或 **Download PNG**。
   - 若為 **Discover** 中已儲存的搜尋，請選取 **Generate CSV** 或 **Generate XLSX**。

   報告會在背景以非同步方式產生，視報告大小而定，可能需要幾分鐘。報告就緒時會顯示通知，並下載該檔案。

若要依排程產生報告，請在 **Reporting** 選單中選取 **Create report definition**，然後繼續前往[使用定義建立報告](#creating-reports-using-a-definition)。此選項會根據您當時檢視的頁面自動填入許多欄位。

若要檢視您產生的報告，請在 **Reporting** 選單中選取 **View reports**。

## 使用定義建立報告

定義可讓您依週期性排程產生報告。

1. 在頂端選單中，前往 **OpenSearch Plugins** > **Reporting**。
1. 在 **Report definitions** 區段中，選取 **Create**。
1. 在 **Report settings** 中，輸入報告的名稱及選用說明。
1. 選擇 **Report source**：**Dashboard**、**Visualization**、**Saved search** 或 **Notebook**。
1. 選取您的儀表板、視覺化、已儲存的搜尋或筆記本。然後選擇報告的時間範圍。
1. 選擇報告的檔案格式。若為已儲存的搜尋，您也可以設定 **Record limit**。
1. （選用）為報告新增頁首或頁尾。頁首與頁尾僅適用於儀表板、視覺化及筆記本報告。
1. 在 **Report trigger** 中，選擇 **On demand** 或 **Schedule**。

   若為排程報告，請選取 **Recurring** 或 **Cron based**。週期性報告會每日或依指定間隔執行。Cron 運算式可提供更大的彈性。如需詳細資訊，請參閱 [Cron expressions]({{site.url}}{{site.baseurl}}/api-reference/cron-expressions/)。

1. 選取 **Create**。

## 刪除報告定義

您可以從 OpenSearch Dashboards 或使用 API 刪除報告定義。刪除報告定義不會刪除先前產生的報告。

產生的報告無法個別刪除。
{: .note}

### 從 OpenSearch Dashboards 刪除

若要刪除報告定義，請依照下列步驟操作：

1. 在頂端選單中，前往 **OpenSearch Plugins** > **Reporting**。
1. 在 **Report definitions** 區段中，選取您要刪除的報告定義名稱。
1. 在報告定義詳細資料頁面上，選擇 **Delete**。
1. 在確認對話方塊中，選擇 **Delete**。

### 使用 API 刪除

若要刪除報告定義，請傳送下列請求：

```json
DELETE _plugins/_reports/definition/{report_definition_id}
```
{% include copy-curl.html %}

若要尋找報告定義 ID，請列出所有定義：

```json
GET _plugins/_reports/definitions
```
{% include copy-curl.html %}

如需完整的報告端點集合，請參閱[報告 API]({{site.url}}{{site.baseurl}}/dashboards/reporting/api/)。

## 疑難排解

您可以使用下列主題來排解及解決報告的問題。

### Chromium 無法在 OpenSearch Dashboards 中啟動

在為儀表板或視覺化建立報告時，您可能會看到下列錯誤：

![OpenSearch Dashboards 報告彈出錯誤訊息]({{site.url}}{{site.baseurl}}/images/reporting-error.png)

此問題可能由兩個原因造成：

- 您安裝的 `headless-chrome` 版本與 OpenSearch Dashboards 執行所在的作業系統不相符。請下載[正確的版本](https://github.com/opensearch-project/reporting/releases/tag/chromium-1.12.0.0)。

- 您缺少其他相依性。請從[其他程式庫](https://github.com/opensearch-project/dashboards-reports/blob/1.x/dashboards-reports/rendering-engine/headless-chrome/README.md#additional-libaries)章節安裝作業系統所需的相依性。

### 報告中的字元無法載入

您可能會遇到 UTF-8 編碼字元在瀏覽器中顯示正常，但在產生的報告中無法載入的問題，這是因為缺少必要的字型相依性。請安裝[字型相依性](https://github.com/opensearch-project/dashboards-reports#missing-font-dependencies)，然後重新產生報告。
