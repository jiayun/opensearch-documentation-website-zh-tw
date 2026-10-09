---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "使用 OpenSearch Dashboards 產生報告"
nav_order: 5
redirect_from:
  - /dashboards/reporting/
---


# 使用 OpenSearch Dashboards 產生報告

您可以使用 OpenSearch Dashboards 建立 PNG、PDF 和 CSV 報告。若要建立報告，您必須具備正確的權限。如需預先定義角色及其授予權限的摘要，請參閱 [安全性外掛程式]({{site.url}}{{site.baseurl}}/security/access-control/users-roles#predefined-roles)。

報告使用兩個概念：

- **報告定義** 是一種已儲存的組態，用於指定要擷取的儀表板、視覺化或已儲存的搜尋、檔案格式 (PDF、PNG 或 CSV)、時間範圍，以及選用的排程。您可以重複使用報告定義，依需求或依排程定期產生報告。
- **報告** 是由報告定義或一次性下載所產生的輸出檔案 (PDF、PNG 或 CSV)。

可用的檔案格式取決於報告來源。儀表板、視覺化和筆記本會以影像形式擷取，並可下載為 PDF 或 PNG。只有已儲存的搜尋可以匯出為 CSV，因為 CSV 輸出包含查詢傳回的資料列，而非轉譯後的影像。若要將視覺化背後的資料匯出為 CSV，請在 **Discover** 中將等效的查詢儲存為已儲存的搜尋，然後從該已儲存的搜尋產生報告。

此外，您也可以透過程式方式執行這些操作。如需更多資訊，請參閱 [Reporting API]({{site.url}}{{site.baseurl}}/reporting/api/)。

在 OpenSearch 2.16 及更早版本中，CSV 報告有不可設定的 10,000 列上限。從 2.17 版開始，此上限可在設定報告時進行組態。雖然報告沒有明確的大小限制 (例如 MB)，但極大的文件可能會導致報告產生失敗，並出現 V8 JavaScript 引擎的記憶體不足錯誤。
{: .tip }

## 產生報告

若要從介面產生報告：

1. 從導覽面板選擇 **Reporting**。
2. 對於儀表板、視覺化或筆記本，選擇 **Download PDF** 或 **Download PNG**。如果您是從 Discover 頁面建立報告，請選擇 **Generate CSV**。

報告會在背景以非同步方式產生，可能需要幾分鐘的時間，視報告大小而定。當您的報告可供下載時，會出現通知。
{: .note}

3. 若要建立排程型報告，請選擇 **Create report definition**。然後繼續進行 [使用定義建立報告](#creating-reports-using-a-definition)。此選項會根據您正在檢視的視覺化、儀表板或資料，預先填入許多欄位。


## 使用定義建立報告

定義可讓您依定期排程產生報告。

1. 從導覽面板選擇 **Reporting**。
1. 選擇 **Create**。
1. 在 **Report settings** 下，輸入報告的名稱和選用的描述。
1. 選擇 **Report source** (即產生報告的頁面)。您可以從 **Dashboard**、**Visualize**、**Discover** (已儲存的搜尋) 或 **Notebooks** 頁面產生報告。
1. 選取您的儀表板、視覺化、已儲存的搜尋或筆記本。然後選擇報告的時間範圍。
1. 為報告選擇適當的檔案格式。
1. (選用) 在報告中新增頁首或頁尾。頁首和頁尾僅適用於儀表板、視覺化和筆記本報告。
1. 在 **Report trigger** 下，選擇 **On demand** 或 **Schedule**。

   對於排程報告，請選擇 **Recurring** 或 **Cron based**。您可以每天或在其他時間間隔接收報告，而 Cron 運算式可提供更大的彈性。如需更多資訊，請參閱 [Cron 運算式]({{site.url}}{{site.baseurl}}/api-reference/common-parameters/#cron-expressions)。

2. 選擇 **Create**。

## 刪除報告定義

您可以從 OpenSearch Dashboards 或使用 API 刪除報告定義。刪除報告定義不會刪除先前產生的報告。

產生的報告無法個別刪除。
{: .note}

### 從 OpenSearch Dashboards 刪除

若要刪除報告定義，請依照下列步驟操作：

1. 從導覽面板選擇 **Reporting**。
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

如需完整的報告端點集合，請參閱 [Reporting API]({{site.url}}{{site.baseurl}}/reporting/api/)。

## 疑難排解

您可以使用下列主題來排解及解決報告的問題。

### Chromium 無法與 OpenSearch Dashboards 一起啟動

在為儀表板或視覺化建立報告時，您可能會看到下列錯誤：

![OpenSearch Dashboards 報告功能的彈出式錯誤訊息]({{site.url}}{{site.baseurl}}/images/reporting-error.png)

此問題可能由兩個原因造成：

- 您沒有與 OpenSearch Dashboards 執行所在作業系統相符的正確 `headless-chrome` 版本。請下載[正確版本](https://github.com/opensearch-project/reporting/releases/tag/chromium-1.12.0.0)。

- 您缺少其他相依性。請從[其他程式庫](https://github.com/opensearch-project/dashboards-reports/blob/1.x/dashboards-reports/rendering-engine/headless-chrome/README.md#additional-libaries)區段安裝作業系統所需的相依性。

### 報告中的字元無法載入

您可能會遇到 UTF-8 編碼字元在瀏覽器中顯示正常，但在產生的報告中無法載入的問題，這是因為缺少必要的字型相依性。請安裝[字型相依性](https://github.com/opensearch-project/dashboards-reports#missing-font-dependencies)，然後重新產生報告。
