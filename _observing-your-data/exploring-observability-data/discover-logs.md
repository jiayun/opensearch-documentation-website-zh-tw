---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "記錄檔"
nav_order: 20
parent: Observability workspace apps
redirect_from:
  - /observability-plugin/discover-logs/
---

# 在 Discover 中分析記錄檔
**於 3.5 版推出**
{: .label .label-purple }

OpenSearch Dashboards 中的 **Logs** 頁面是一項記錄分析工具，可讓您使用管線處理語言（PPL）探索及分析應用程式記錄檔。在此頁面上，您可以查詢記錄資料、根據彙總結果建立視覺化，並將這些視覺化新增至儀表板。

**Logs** 頁面提供下列功能：

- **使用 PPL 查詢**：使用 PPL 語法篩選、彙總及轉換記錄資料。
- **自動視覺化**：當您使用 `stats` 等彙總命令時，介面會自動切換至視覺化檢視。
- **多種視覺化類型**：從各種視覺化類型中選擇。
- **儀表板整合**：將視覺化直接儲存至新的或現有的儀表板。
- **查詢管理**：儲存查詢以供重複使用，並存取最近的查詢。

## 先決條件

使用 **Logs** 頁面之前，請確認您已滿足下列先決條件：

1. **啟用功能旗標**：將下列設定新增至您的 `opensearch_dashboards.yml` 檔案：

   ```yaml
   workspace.enabled: true
   explore.enabled: true
   ```
   {% include copy.html %}

   更新組態檔案後，請重新啟動 OpenSearch Dashboards，讓變更生效。

2. **建立可觀測性工作區**：您必須在可觀測性工作區內操作。**Logs** 頁面僅適用於此工作區類型。

   注意：工作區與多租用戶功能不相容。若要啟用工作區，您必須先設定 `opensearch_security.multitenancy.enabled: false`，以停用多租用戶功能。
   {: .note}

3. **設定記錄資料集**：您必須至少設定一個記錄資料集。如需詳細指示，請參閱[資料集]({{site.url}}{{site.baseurl}}/observing-your-data/exploring-observability-data/datasets/)。

## 存取記錄檔頁面

若要存取 **Logs** 頁面：

1. 在 OpenSearch Dashboards 中前往可觀測性工作區。
2. 在左側導覽列中，選取 **Logs**。

## 探索記錄資料

**Logs** 頁面如下圖所示。

![Discover 記錄檔介面]({{site.url}}{{site.baseurl}}/images/discover-logs/discover-logs-interface.png)

此頁面包含下列元件：

- **PPL 編輯器**：頂端的查詢列，供您撰寫 PPL 查詢。 
- **資料集選取器**：從頁面頂端的下拉式清單中，選取要探索的記錄資料集。
- **最近的查詢**：在頁面頂端存取先前執行的查詢。
- **已儲存的查詢**：在頁面頂端存取您已儲存以供重複使用的查詢。
- **Fields**：位於左側的 **Fields** 面板會顯示可用欄位，並將其分為 **Selected** 欄位和 **Query** 欄位區段。
- **Log count**：**Log count** 直方圖顯示記錄項目隨時間的分布。使用 **Interval** 選取器調整時間桶的大小。
- **結果區域**：透過兩個索引標籤顯示查詢結果：
  - **Logs**：以表格格式顯示個別記錄項目。
  - **Visualization**：使用 `stats` 命令時，以圖表顯示彙總資料。
- **時間範圍選取器**：位於右上角，可讓您設定查詢的時間範圍。

## 使用 PPL 查詢記錄檔

您可以使用 PPL 查詢記錄資料。PPL 可讓您使用管線字元（`|`）串接命令，以篩選、轉換及彙總資料。

### 基本查詢

若要擷取資料集中的所有記錄檔，請輸入不含任何篩選條件的查詢，並選取 **Refresh** 以執行查詢。結果會顯示在 **Logs** 索引標籤中，呈現個別記錄項目。

### 使用 WHERE 子句篩選

使用 `WHERE` 子句，根據欄位值篩選記錄檔：

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

**Logs** 頁面提供工具，協助您有效率地整理及重複使用 PPL 查詢。

- **最近的查詢**：選取 **Recent queries**，檢視並重新執行先前執行過的查詢。
- **已儲存的查詢**：選取 **Saved queries**，存取您已儲存的查詢。若要儲存目前的查詢，請選取 **Actions** > **Save query**。

## 從記錄檔建立視覺化

當您使用 `stats` 命令彙總資料時，**Logs** 頁面會自動切換至 **Visualization** 索引標籤，以圖表顯示結果。

### 使用 stats 命令

`stats` 命令會根據指定的欄位彙總資料。例如，若要依 URL 路徑分組，計算每分鐘的記錄檔數量，請使用下列查詢：

```sql
| WHERE `resource.attributes.service.name` = 'frontend-proxy'
| WHERE `attributes.url.path` in ("/api/cart","/api/checkout")
| STATS count() by span(time, 1m), `attributes.url.path`
```
{% include copy.html %}

執行此查詢時，介面會自動切換至 **Visualization** 索引標籤並顯示圖表，如下圖所示。

![從記錄檔建立的視覺化]({{site.url}}{{site.baseurl}}/images/discover-logs/discover-logs-visualization.png)

### 視覺化類型

若要變更視覺化類型，請前往 **Settings** > **Visualization type**，並選取其中一個可用選項，如下圖所示。

![視覺化類型選項]({{site.url}}{{site.baseurl}}/images/discover-logs/discover-logs-viz-types.png)

可用的視覺化類型如下。

| 類型 | 說明 |
|:-----|:------------|
| **Line** | 以相連的資料點顯示資料；適合呈現隨時間變化的趨勢。 |
| **Area** | 類似折線圖，但會填滿線條下方的區域。 |
| **Bar** | 以垂直或水平長條顯示資料，以便比較類別。 |
| **Metric** | 以大型數字顯示單一彙總值。|
| **State timeline** | 在水平時間軸上顯示隨時間發生的狀態變化。 |
| **Heatmap** | 使用顏色深淺，以矩陣格式呈現數值。 |
| **Bar Gauge** | 以水平長條顯示數值，並可設定閾值。 |
| **Pie** | 以圓形圖表的扇形區塊顯示比例。 |

### 視覺化設定

若要自訂視覺化，請更新 **Settings** 面板中的選項，如下圖所示。

![切換座標軸後的長條圖]({{site.url}}{{site.baseurl}}/images/discover-logs/discover-logs-switch-axes.png)

您可以更新下列選項：

- **Fields**：設定要顯示於 **X-Axis**、**Y-Axis** 及 **Color** 的欄位（用於依不同值將資料序列分組）。對於長條圖，您可以在 Fields 區段切換 **Switch axes**，將圖表方向從垂直改為水平（交換 X 軸和 Y 軸）。
- **Bar/Bucket**：對於長條圖，設定長條大小（**Auto** 或 **Manual**）及桶設定（**Type** 和 **Interval**）。
- **Thresholds**：使用自訂顏色定義數值閾值。
- **Axes**：設定座標軸標籤、刻度及格式。
- **Legend**：控制圖例的顯示狀態及位置。

## 將視覺化新增至儀表板

您可以使用下列步驟，將視覺化直接儲存至儀表板，以便持續監控：

1. 建立視覺化後，在結果區域中選取 **Add to dashboard**。

2. 在 **Save and Add to Dashboard** 對話方塊中，選擇下列其中一個選項：
   - **Save to existing dashboard**：從下拉式清單中選取現有的儀表板。
   - **Save to new dashboard**：輸入新儀表板的名稱。

3. 在 **Save search** 欄位中，輸入已儲存搜尋的名稱。

4. 選取 **Add**，將視覺化儲存至儀表板。

## 相關文件

- [資料集]({{site.url}}{{site.baseurl}}/observing-your-data/exploring-observability-data/datasets/) -- 建立及管理記錄資料集。
- [PPL]({{site.url}}{{site.baseurl}}/search-plugins/sql/ppl/index/) -- 瞭解 PPL 查詢語法。
- [關聯]({{site.url}}{{site.baseurl}}/observing-your-data/exploring-observability-data/correlations/) -- 連結記錄與追蹤資料集。
