---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "使用查詢建立視覺化"
nav_order: 50
parent: Building data visualizations
grand_parent: OpenSearch Dashboards
has_children: true
has_toc: false
redirect_from:
  - /dashboards/visualize/visualization-editor/
---

# 使用查詢建立視覺化

_視覺化編輯器_可讓您撰寫 [Piped Processing Language (PPL)]({{site.url}}{{site.baseurl}}/sql-and-ppl/ppl/) 或 Prometheus Query Language (PromQL) 查詢來建立視覺化。編輯器會自動將查詢結果欄位對應至圖表座標軸，並根據資料的形狀建議圖表類型。若要從儀表板開啟視覺化編輯器，請選取 **Create new** > **Add visualization**。

## 先決條件

使用視覺化編輯器之前，OpenSearch Dashboards 管理員必須完成下列設定步驟。

### 步驟 1：啟用必要設定

除了[啟用工作區]({{site.url}}{{site.baseurl}}/dashboards/workspace/workspace/#enabling-workspaces)之外，請將下列設定新增至您的 `opensearch_dashboards.yml` 檔案：

```yaml
explore.enabled: true
```
{% include copy.html %}

更新組態檔案後，請重新啟動 OpenSearch Dashboards，變更才會生效。

### 步驟 2：建立工作區

視覺化編輯器需要工作區。如果已啟用已儲存物件權限，則只有儀表板管理員可以建立工作區，其他使用者必須由現有工作區的擁有者將其加入該工作區。如需詳細資訊，請參閱[設定儀表板管理員]({{site.url}}{{site.baseurl}}/dashboards/workspace/workspace-acl/#configuring-dashboard-administrators)。

若要建立工作區，請依照下列步驟操作：

1. 前往 OpenSearch Dashboards 首頁。
1. 選取 **Create workspace**。
1. 輸入工作區名稱。
1. 選取 **Analytics (all features)** 使用案例。
1. 選取 **Create workspace**。

如需詳細資訊，請參閱[建立工作區]({{site.url}}{{site.baseurl}}/dashboards/workspace/create-workspace/)。

### 步驟 3：設定資料來源

視覺化編輯器需要與您的工作區關聯的資料集：

- 若使用 PPL，請設定索引模式：
    1. 在您的工作區中，前往 **Index patterns**（位於 **Management** 中）。
    1. 選取 **Create index pattern**。
    1. 輸入索引名稱（例如 `opensearch_dashboards_sample_data_logs`）。
    1. 選取 **Next step**。
    1. 選取時間欄位（例如 `@timestamp`）。
    1. 選取 **Create index pattern**。

    如需詳細資訊，請參閱[索引模式]({{site.url}}{{site.baseurl}}/dashboards/management/index-patterns/)。

- 若使用 PromQL（Prometheus 資料來源），請為您的工作區設定 Prometheus 資料來源連線。如需詳細資訊，請參閱[將 Prometheus 連線至 OpenSearch]({{site.url}}{{site.baseurl}}/dashboards/management/connect-prometheus/)。

### 步驟 4（選用）：安裝範例資料

本文件中的範例使用 OpenSearch Dashboards 範例資料集。若要安裝範例資料集，請依照下列步驟操作：

1. 在左側導覽中，展開 **Manage workspace** 並選取 **Sample data**。
1. 在 **Sample log data** 圖格以及您想新增的其他圖格中選取 **Add data** 按鈕。本節中的範例使用範例記錄資料。

如需詳細資訊，請參閱[新增範例資料]({{site.url}}{{site.baseurl}}/dashboards/getting-started/data-setup/#add-sample-data)。

## 瀏覽視覺化編輯器使用者介面

下圖顯示視覺化編輯器的主要元件。

![附有標註的視覺化編輯器介面]({{site.url}}{{site.baseurl}}/images/dashboards/visualization-editor/visualization-editor-overview.png){: width="100%" }

- _時間篩選器_ (A) 用於選取查詢結果的時間範圍。
- _Update 按鈕_ (B) 用於執行或重新整理查詢。
- _查詢編輯器_ (C) 包含查詢文字；若使用 PromQL，則包含查詢建構器。
- _Saved queries_ 下拉式選單 (D) 用於儲存及載入可重複使用的查詢。
- _組態面板_ (E) 包含圖表類型選取器、欄位對應及樣式設定。

## 建立視覺化

若要開啟視覺化編輯器，請使用下列其中一種方法：

- 在左側導覽中，選取 **Explorer** > **Logs**，然後選取 **Visualization** 索引標籤。
- 在儀表板中，選取新增面板圖示，然後選取 **Add visualization**。

若要建立視覺化，請依照下列步驟操作：

1. 從查詢列中的資料集選取器選取資料集（例如 **opensearch_dashboards_sample_data_logs**）。
1. 在查詢編輯器中撰寫 PPL 查詢。如果您已選取資料集，請以管道字元 (`|`) 作為查詢的開頭。否則，請使用 `source =` 明確指定來源。例如，下列查詢會計算每小時的記錄事件數：

   ```sql
   source = opensearch_dashboards_sample_data_logs | stats count() by SPAN(@timestamp, 1h)
   ```
   {% include copy.html %}

   如果已選取 `opensearch_dashboards_sample_data_logs` 作為資料集，您可以省略 `source`：

   ```sql
   | stats count() by SPAN(@timestamp, 1h)
   ```
   {% include copy.html %}

1. 選取 **Update** 或按下 **Enter** 以執行查詢。
1. 編輯器會根據您的查詢結果自動選取圖表類型，並將欄位對應至座標軸。若要變更圖表類型，請使用 **Visualization type** 下拉式選單。
1. 若要自訂欄位對應，請使用 **Fields** 面板。

## 使用儀表板變數

您可以使用儀表板變數來建立動態的互動式視覺化。變數可讓您在篩選值、指標、時間間隔和彙總函式之間切換，而無須編輯查詢。請在您的 PPL 或 PromQL 查詢中使用 `$variableName` 或 `${variableName}` 語法來參照變數。

如需詳細資訊，請參閱[儀表板變數]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualization-editor/dashboard-variables/)。

## 儲存視覺化

若要儲存視覺化，請選取 **Save**（如果您是從儀表板開啟編輯器，則選取 **Save and back**）。輸入視覺化的名稱，然後選取 **Save**。

如果您是從儀表板開啟視覺化編輯器，儲存後視覺化會自動新增至該儀表板。如果您是從 **Explorer** > **Logs** 建立視覺化，請先儲存，再手動將其新增至儀表板。

## 儲存及重複使用查詢

若要儲存 PPL 查詢以便重複使用，請選取 **Saved queries** > **Save query**。在對話方塊中，設定下列選項。

| 選項 | 說明 |
| --- | --- |
| **Save as new query** | 選取時，會將查詢儲存為新項目，而不是覆寫現有項目。 |
| **Name** | 已儲存查詢的名稱。 |
| **Description** | 查詢的選用說明。 |
| **Include filters** | 啟用時，會將目前套用的篩選器與查詢一併儲存。 |
| **Include time filter** | 啟用時，會將目前的時間範圍與查詢一併儲存。 |

選取 **Save changes** 以儲存查詢。

若要載入先前儲存的查詢，請選取 **Saved queries** > **Open query**，然後從清單中選取查詢，再選取 **Open query** 按鈕。已儲存的查詢會載入至查詢編輯器。

## 視覺化類型

如需支援的圖表類型及其預期資料形狀的清單，請參閱[視覺化類型]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualization-editor/viz-types/)。

## 設定視覺化

共用組態選項（欄位、分割、座標軸、工具提示、圖例、閾值等）適用於多種視覺化類型。如需詳細資訊，請參閱[在視覺化編輯器中設定視覺化]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualization-editor/configuring-visualizations/)。

## 查詢面板

使用查詢面板可選擇查詢語言和資料集、撰寫或建構查詢，並執行查詢以產生視覺化。查詢面板支援 PPL、PromQL，以及在啟用時支援 SQL。若使用 PromQL，查詢面板還提供 **Builder** 和 **Code** 模式、多個查詢列，以及個別查詢和共用的查詢選項。

如需詳細資訊，請參閱[查詢面板]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualization-editor/query-panel/)。

## 資料轉換

資料轉換會在呈現視覺化之前修改查詢結果。使用轉換可重新塑形、篩選、排序、計算或摘要資料，而無須變更原始查詢。如需詳細資訊，請參閱[資料轉換]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualization-editor/data-transformation/)。

## 相關文件

- [PPL]({{site.url}}{{site.baseurl}}/sql-and-ppl/ppl/)
- [儀表板變數]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualization-editor/dashboard-variables/)
- [建立儀表板]({{site.url}}{{site.baseurl}}/dashboards/dashboard/)
- [索引模式]({{site.url}}{{site.baseurl}}/dashboards/management/index-patterns/)
- [將 Prometheus 連線至 OpenSearch]({{site.url}}{{site.baseurl}}/dashboards/management/connect-prometheus/)
