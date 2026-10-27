---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "匯出資料"
nav_order: 72
---

# 匯出資料

OpenSearch Dashboards 提供多種下載內容的方式。使用哪種方法取決於您要匯出的內容：文件本身、視覺化背後的資料、儀表板的呈現副本，或是您所建立物件的定義。

下表列出各種匯出方法。

| 您要匯出的內容 | 方法 | 格式 |
| :--- | :--- | :--- |
| 搜尋傳回的文件 | [從 Discover 下載搜尋結果](#exporting-search-results) | CSV |
| 單一文件 | [從 Discover 複製文件](#exporting-search-results) | JSON |
| 視覺化顯示的資料 | [從 Inspect 面板下載資料](#exporting-visualization-data) | CSV |
| 以檔案形式分享的儀表板、視覺化、儲存的搜尋或筆記本，可依需求或依排程產生 | [產生報表](#generating-reports) | PDF、PNG、CSV 或 XLSX |
| 儀表板、視覺化、索引模式及其他已儲存物件，用於備份或複製到另一個執行個體 | [匯出已儲存物件](#exporting-saved-objects) | NDJSON |

## 匯出搜尋結果

在 **Discover** 中，篩選文件並選擇您要匯出的欄位，然後選取 **Download as CSV**。您可以下載頁面上顯示的文件，或所有符合條件的文件，最多 10,000 筆。若要改為複製單一文件，請展開該文件並複製其 JSON 表示法。

如需更多資訊，請參閱 [在 Discover 中匯出資料]({{site.url}}{{site.baseurl}}/dashboards/discover/index-discover/#exporting-data)。

## 匯出視覺化資料

若要下載視覺化顯示的資料，請依照下列步驟操作：

1. 開啟視覺化：
   - 在 **Visualize** 應用程式中，開啟視覺化並在頂端選單選取 **Inspect**。
   - 在儀表板上，開啟視覺化的面板選單並選取 **Inspect**。
1. 選取 **Download CSV**。
1. 選取下列其中一個選項：
   - **Formatted CSV**：依照索引模式的欄位格式，以資料在表格中呈現的方式下載資料。
   - **Raw CSV**：以資料儲存時的原始形式下載資料。例如，日期會以時間戳記下載。

## 產生報表

報表可將儀表板、視覺化或筆記本擷取為 PDF 或 PNG 檔案，或將儲存的搜尋結果擷取為 CSV 或 XLSX 檔案。您可以單次產生報表，或建立報表定義以依排程產生報表。若要依排程或從指令碼匯出搜尋結果，請在 **Discover** 中儲存搜尋，並從該儲存的搜尋產生 CSV 或 XLSX 報表。

如需更多資訊，請參閱 [Reporting]({{site.url}}{{site.baseurl}}/dashboards/reporting/)。

## 匯出已儲存物件

已儲存物件是您在 OpenSearch Dashboards 中建立的儀表板、視覺化、儲存的搜尋、索引模式及其他資源的定義。匯出已儲存物件會下載這些定義，而非它們顯示的資料。請使用此方法備份您的物件，或將它們匯入另一個 OpenSearch Dashboards 執行個體。

如需更多資訊，請參閱 [Saved objects]({{site.url}}{{site.baseurl}}/dashboards/management/saved-objects/)。
