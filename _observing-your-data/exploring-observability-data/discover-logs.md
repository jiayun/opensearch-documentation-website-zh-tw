---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "在 Discover 中分析記錄檔"
nav_order: 30
parent: Using Discover for observability
redirect_from:
  - /observability-plugin/discover-logs/
---

# 在 Discover 中分析記錄檔
**3.5 版推出**
{: .label .label-purple }

OpenSearch Dashboards 的 **Logs** 頁面是一套記錄分析工具，可讓您使用 Piped Processing Language (PPL) 探索與分析應用程式記錄檔。在此頁面上，您可以查詢記錄資料、從彙總結果建立視覺化，並將這些視覺化加入儀表板。

**Logs** 頁面提供下列功能：

- **以 PPL 為基礎的查詢**：使用 PPL 語法來篩選、彙總與轉換記錄資料。
- **自動視覺化**：當您使用 `stats` 等彙總命令時，介面會自動切換至視覺化檢視。
- **多種視覺化類型**：可從各種視覺化類型中選擇。
- **儀表板整合**：直接將視覺化儲存至新的或現有儀表板。
- **查詢管理**：儲存查詢以供重複使用，並存取最近的查詢。

## 必要條件

使用 **Logs** 頁面之前，請確認您已符合下列必要條件：

1. **啟用功能旗標**：在您的 `opensearch_dashboards.yml` 檔案中加入下列設定：

   ```yaml
   workspace.enabled: true
   data_source.enabled: true
   explore.enabled: true
   ```
   {% include copy.html %}

   更新組態檔後，請重新啟動 OpenSearch Dashboards 以讓變更生效。

2. **建立可觀測性工作區**：您必須在可觀測性工作區中操作。**Logs** 頁面僅在此工作區類型中提供。

   注意：工作區與多租戶功能不相容。若要啟用工作區，您必須先透過設定 `opensearch_security.multitenancy.enabled: false` 停用多租戶功能。
   {: .note}

3. **設定記錄資料集**：您必須至少設定一個記錄資料集。詳細說明請參閱[資料集]({{site.url}}{{site.baseurl}}/observing-your-data/exploring-observability-data/datasets/)。

## 存取 **Logs** 頁面

若要存取 **Logs** 頁面：

1. 在 OpenSearch Dashboards 中前往可觀測性工作區。
2. 在左側導覽中展開 **Discover**，然後選取 **Logs**。

## 探索記錄資料

**Logs** 頁面如下圖所示。

![Discover 記錄檔介面]({{site.url}}{{site.baseurl}}/images/discover-logs/discover-logs-interface.png)

它由下列元件組成：

- **PPL 編輯器**：頂部的查詢列，您可在此撰寫 PPL 查詢。
- **資料集選擇器**：從頁面頂端的下拉式清單中選取要探索的記錄資料集。
- **最近的查詢**：在頁面頂端存取先前執行過的查詢。
- **已儲存的查詢**：在頁面頂端存取您已儲存以供重複使用的查詢。
- **欄位**：位於左側的 **Fields** 面板，將可用欄位整理為 **Selected** 欄位與 **Query** 欄位兩個區段。
- **記錄計數**：**Log count** 直方圖顯示記錄項目隨時間的分布。使用 **Interval** 選擇器調整時間桶的大小。
- **結果區域**：以兩個分頁顯示查詢結果：
  - **Logs**：以表格格式顯示個別記錄項目。
  - **Visualization**：使用 `stats` 命令時，以圖表顯示彙總資料。
- **時間範圍選擇器**：位於右上角，可讓您設定查詢的時間範圍。

## 使用 PPL 查詢記錄檔

您可以使用 PPL 查詢記錄資料。PPL 允許您使用管線字元 (`|`) 串接命令，以篩選、轉換與彙總資料。

### 基本查詢

若要擷取資料集中的所有記錄檔，請輸入查詢並選取 **Refresh**，執行不含任何篩選條件的查詢。結果會顯示在 **Logs** 分頁中，呈現個別記錄項目。

### 使用 WHERE 子句篩選

使用 `WHERE` 子句根據欄位值篩選記錄檔：

```sql
| WHERE `resource.attributes.service.name` = 'frontend-proxy'
```
{% include copy.html %}

您可以提供多個 `WHERE` 子句來組合多個條件：

```sql
| WHERE `resource.attributes.service.name` = 'frontend-proxy'
| WHERE `attributes.url.path` in ("/api/cart","/api/checkout")
```
{% include copy.html %}

### 管理查詢

**Logs** 頁面提供工具，協助您有效率地整理與重複使用 PPL 查詢。

- **最近的查詢**：選取 **Recent queries** 以檢視並重新執行先前執行過的查詢。
- **已儲存的查詢**：選取 **Saved queries** 以存取您已儲存的查詢。若要儲存目前的查詢，請選取 **Actions** > **Save query**。

## 從記錄檔建立視覺化

當您使用 `stats` 命令彙總資料時，**Logs** 頁面會自動切換至 **Visualization** 分頁，以圖表顯示結果。

### 使用 stats 命令

`stats` 命令會根據指定的欄位彙總資料。例如，若要統計每分鐘依 URL 路徑分組的記錄檔數量，請使用下列查詢：

```sql
| WHERE `resource.attributes.service.name` = 'frontend-proxy'
| WHERE `attributes.url.path` in ("/api/cart","/api/checkout")
| STATS count() by span(time, 1m), `attributes.url.path`
```
{% include copy.html %}

執行此查詢時，介面會自動切換至 **Visualization** 分頁並顯示圖表，如下圖所示。

![從記錄檔建立的視覺化]({{site.url}}{{site.baseurl}}/images/discover-logs/discover-logs-visualization.png)

### 視覺化類型

若要變更視覺化類型，請前往 **Settings** > **Visualization type**，並從可用選項中選擇一項，如下圖所示。

![視覺化類型選項]({{site.url}}{{site.baseurl}}/images/discover-logs/discover-logs-viz-types.png)

下列為可用的視覺化類型。

| 類型 | 說明 |
|:-----|:------------|
| **Line** | 以連接的點顯示資料；適合顯示隨時間變化的趨勢。 |
| **Area** | 與折線圖類似，但線條下方的區域會填滿。 |
| **Bar** | 以垂直或水平長條顯示資料，用於比較類別。 |
| **Metric** | 以大號數字顯示單一彙總值。 |
| **State timeline** | 在水平時間軸上顯示隨時間的狀態變化。 |
| **Heatmap** | 使用色彩濃度以矩陣格式表示數值。 |
| **Bar Gauge** | 以具有可設定門檻的水平長條顯示數值。 |
| **Pie** | 以圓形圖的扇形區塊顯示比例。 |

### 視覺化設定

若要自訂視覺化，請更新 **Settings** 面板中的選項，如下圖所示。

![已交換座標軸的長條圖]({{site.url}}{{site.baseurl}}/images/discover-logs/discover-logs-switch-axes.png)

您可以更新下列選項：

- **Fields**：設定要在 **X-Axis**、**Y-Axis** 與 **Color** 上顯示的欄位 (用於依不同值分組資料序列)。對於長條圖，您可以在 Fields 區段切換 **Switch axes**，將圖表方向從垂直變更為水平 (交換 X 與 Y 軸)。
- **Bar/Bucket**：對於長條圖，設定長條大小 (**Auto** 或 **Manual**) 與桶設定 (**Type** 與 **Interval**)。
- **Thresholds**：使用自訂色彩定義數值門檻。
- **Axes**：設定軸標籤、刻度與格式。
- **Legend**：控制圖例的可見性與位置。

## 將視覺化加入儀表板

您可以使用下列步驟，將視覺化直接儲存至儀表板以進行持續監控：

1. 建立視覺化後，在結果區域選取 **Add to dashboard**。

2. 在 **Save and Add to Dashboard** 對話方塊中，選擇下列其中一個選項：
   - **Save to existing dashboard**：從下拉式清單中選取現有儀表板。
   - **Save to new dashboard**：輸入新儀表板的名稱。

3. 在 **Save search** 欄位中輸入已儲存搜尋的名稱。

4. 選取 **Add**，將視覺化儲存至儀表板。

## 相關文件

- [資料集]({{site.url}}{{site.baseurl}}/observing-your-data/exploring-observability-data/datasets/) -- 建立與管理記錄資料集。
- [PPL]({{site.url}}{{site.baseurl}}/search-plugins/sql/ppl/index/) -- 學習 PPL 查詢語法。
- [關聯]({{site.url}}{{site.baseurl}}/observing-your-data/exploring-observability-data/correlations/) -- 連結記錄檔與追蹤資料集。
