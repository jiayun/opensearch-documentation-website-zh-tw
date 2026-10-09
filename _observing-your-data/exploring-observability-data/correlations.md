---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "相互關聯"
nav_order: 60
parent: Using Discover for observability
redirect_from:
  - /observability-plugin/correlations/
---

# 相互關聯
**3.5 版新增**
{: .label .label-purple }

相互關聯 (Correlations) 讓您能將追蹤資料集與記錄資料集連結，在分析分散式追蹤時檢視相關的記錄項目。透過將追蹤 span 與對應的應用程式記錄連結起來，相互關聯資料集可協助您快速找出問題的根本原因。

在對分散式系統進行疑難排解時，您經常需要跨多個來源相互關聯資料。追蹤可能顯示某個請求失敗，但詳細的錯誤資訊卻在您的應用程式記錄中。使用相互關聯，您可以：

- 將單一追蹤資料集連結至最多五個記錄資料集。
- 直接從 span 詳細資料面板檢視相關記錄。
- 在追蹤分析與記錄探索之間順暢切換。

## 必要條件

使用相互關聯之前，請確認您已符合下列必要條件：

1. **啟用功能旗標**：在您的 `opensearch_dashboards.yml` 檔案中加入下列設定：

   ```yaml
   workspace.enabled: true
   data_source.enabled: true
   explore.enabled: true
   explore.discoverTraces.enabled: true
   datasetManagement.enabled: true
   ```
   {% include copy.html %}

   更新組態檔後，請重新啟動 OpenSearch Dashboards 以讓變更生效。

1. **建立資料集**：您必須已設定至少一個追蹤資料集與一個記錄資料集。詳細說明請參閱[資料集]({{site.url}}{{site.baseurl}}/observing-your-data/exploring-observability-data/datasets/)。

1. **設定結構對應**：您的記錄資料集必須已設定結構對應。至少需要對應 **Trace ID** 欄位，才能將記錄與追蹤進行比對。

## 相互關聯需求

若要讓相互關聯正常運作，您的記錄資料必須包含下列可對應至追蹤情境的欄位。

| 欄位 | 用途 |
|:------|:--------|
| **Trace ID** | 將記錄項目連結至特定追蹤 |
| **Span ID** | 將記錄項目連結至特定 span |
| **Service name** | 依服務篩選記錄 |
| **Timestamp** | 依時間先後排序記錄項目 |

如果您的記錄未遵循 OpenTelemetry 慣例，請在記錄資料集中設定結構對應，將自訂欄位名稱對應至這些標準欄位。

## 建立追蹤與記錄之間的相互關聯

若要在追蹤資料集與記錄資料集之間建立相互關聯，請依照下列步驟操作：

1. 在左側導覽中前往 **Datasets**。

2. 選取您要與記錄相互關聯的追蹤資料集。

3. 在資料集詳細資料頁面中，選取 **Correlated datasets** 索引標籤，如下圖所示。

   ![追蹤資料集的 Correlated datasets 索引標籤]({{site.url}}{{site.baseurl}}/images/datasets/correlations-trace-dataset-tab.png)

4. 選取 **Configure correlation**。

5. 在 **Configure correlation** 對話方塊中，選取最多五個要與此追蹤資料集相互關聯的記錄資料集，如下圖所示。

   ![Configure correlation 對話方塊]({{site.url}}{{site.baseurl}}/images/datasets/correlations-configure-dialog.png)

6. 選取 **Save** 以建立相互關聯。

7. 相互關聯的記錄資料集現在會出現在 **Correlated datasets** 表格中，如下圖所示。

   ![表格中已建立的相互關聯]({{site.url}}{{site.baseurl}}/images/datasets/correlations-created-table.png)

## 在記錄資料集中檢視相互關聯

您可以從記錄資料集詳細資料中檢視與該記錄資料集相互關聯的追蹤資料集：

1. 在左側導覽中前往 **Datasets**。

2. 選取已與追蹤資料集相互關聯的記錄資料集。

3. 選取 **Correlated traces** 索引標籤，以檢視與此記錄資料集連結的追蹤資料集，如下圖所示。

   ![記錄資料集的 Correlated traces 索引標籤]({{site.url}}{{site.baseurl}}/images/datasets/correlations-logs-dataset-tab.png)

此檢視為唯讀。若要修改相互關聯，您必須從追蹤資料集進行編輯。
{: .note}

## 在 Traces 頁面中使用相互關聯

建立相互關聯後，您可以在分析追蹤時存取相關記錄。

### 在 span 詳細資料中檢視相關記錄

1. 前往 **Discover** > **Traces**。

2. 選取一個追蹤以檢視其詳細資料。

3. 在追蹤中選取一個 span 以開啟 **Span details**。

4. 在 **Span details** 中，選取 **Logs** 索引標籤以開啟 **Related logs**，如下圖所示。相關記錄是透過將 span 中的追蹤 ID 與相互關聯記錄資料集中的記錄項目進行比對來擷取。

   ![顯示相關記錄的 span 詳細資料]({{site.url}}{{site.baseurl}}/images/datasets/correlations-span-details-logs.png)

6. 選取一個記錄項目以檢視其完整詳細資料，或前往 **Logs** 頁面進一步探索。

## 管理相互關聯

您可以從追蹤資料集詳細資料頁面編輯或移除相互關聯。

### 編輯相互關聯

若要修改現有的相互關聯，請依照下列步驟操作：

1. 在左側導覽中前往 **Datasets**，並選取您要修改的追蹤資料集。
2. 選取 **Correlated datasets** 索引標籤。
3. 選取 **Configure correlation** 以修改相互關聯記錄資料集的清單。
4. 視需要新增或移除資料集。
5. 選取 **Save** 以套用變更。

### 移除相互關聯

若要移除相互關聯：

1. 在左側導覽中前往 **Datasets**，並選取您要修改的追蹤資料集。
2. 選取 **Correlated datasets** 索引標籤。
3. 使用刪除圖示刪除已設定的相互關聯。

## 相關文件

- [資料集]({{site.url}}{{site.baseurl}}/observing-your-data/exploring-observability-data/datasets/) -- 建立與管理資料集。
- [Data Prepper]({{site.url}}{{site.baseurl}}/data-prepper/) -- 將 OpenTelemetry 資料匯入 OpenSearch。
