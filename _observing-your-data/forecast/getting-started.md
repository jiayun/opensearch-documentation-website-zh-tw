---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "預測入門"
nav_order: 5
parent: Forecasting
has_children: false
---

# 預測入門

您可以在 OpenSearch Dashboards 中，從導覽面板選取 **Forecasting**，以定義及設定預測器。

## 步驟 1：定義預測器

**預測器**代表單一預測工作。您可以建立多個預測器並行執行，每個預測器分析不同的資料來源。請依照下列步驟定義新的預測器：

1. 在 **Forecaster list** 檢視中，選擇 **Create forecaster**。

2. 輸入下列資訊以定義資料來源：
   * **Name** – 提供唯一且具描述性的名稱，例如 `requests-10min`。  
   * **Description** – 簡述預測器的用途，例如 `Forecast total request count every 10 minutes`。  
   * **Indexes** – 選取一或多個索引、索引模式或別名。透過跨叢集搜尋（`cluster-name:index-pattern`）可支援遠端索引。如需詳細資訊，請參閱[跨叢集搜尋]({{site.url}}{{site.baseurl}}/search-plugins/cross-cluster-search/)。如果已啟用 Security 外掛程式，請參閱[透過細粒度存取控制選取遠端索引]({{site.url}}{{site.baseurl}}/observing-your-data/forecast/security/#selecting-remote-indexes-with-fine-grained-access-control)。

3. （選用）選擇 **Add data filter** 以設定 **Field**、**Operator** 和 **Value**，或選擇 **Use query DSL** 以定義[布林查詢]({{site.url}}{{site.baseurl}}/query-dsl/compound/bool/)。下列範例使用查詢領域專用語言（DSL）篩選器來比對三個 URL 路徑：

     ```json
     {
       "bool": {
         "should": [
           { "term": { "urlPath.keyword": "/domain/{id}/short" } },
           { "term": { "urlPath.keyword": "/sub_dir/{id}/short" } },
           { "term": { "urlPath.keyword": "/abcd/123/{id}/xyz" } }
         ]
       }
     }
    ```


4. 在 **Timestamp field** 下，選取儲存時間戳記的欄位。

5. 在 **Indicator (metric)** 區段中，為預測器新增指標。每個預測器支援一個指標，以達到最佳準確度。請選擇下列其中一個選項：

   - 選取預先定義的彙總：`average()`、`count()`、`sum()`、`min()` 或 `max()`。  
   - 若要使用自訂彙總，請在 **Forecast based on** 下選擇 **Custom expression**，並定義您自己的 [Query DSL]({{site.url}}{{site.baseurl}}/opensearch/query-dsl/index/) 運算式。例如，下列查詢會預測具有特定帳戶類型的不重複帳戶數量：

   ```json
   {
    "bbb_unique_accounts": {
        "filter": {
            "bool": {
                "must": [
                    {
                        "wildcard": {
                            "accountType": {
                                "wildcard": "*blah*",
                                "boost": 1
                            }
                        }
                    }
                ],
                "adjust_pure_negative": true,
                "boost": 1
            }
        },
        "aggregations": {
            "uniqueAccounts": {
                "cardinality": {
                    "field": "account"
                }
            }
        }
    }
   }
   ```

6. （選用）在 **Categorical fields** 區段中，啟用 **Split time series using categorical fields**，以產生實體層級的預測（例如依 IP 位址、產品 ID 或國家編碼）。

   可快取於記憶體中的不重複實體數量有限。請使用下列公式估算容量：

   ```
   (data nodes × heap size × plugins.forecast.model_max_size_percent)
   ──────────────────────────────────────────────────────────────────
                 entity-model size (MB)
   ```

   例如，一個叢集有 3 個資料節點，每個節點具有 8 GB 的 JVM 堆積記憶體，並採用預設的 10% 模型記憶體配置，其可容納的實體數量如下：

   ```
   (8096 MB × 0.10 ÷ 1 MB) × 3 nodes ≈ 2429 entities
   ```

   若要判斷實體模型的大小，請使用 [Profile Forecaster API]({{site.url}}{{site.baseurl}}/observing-your-data/forecast/api/#profile-forecaster)。您可以透過 `plugins.forecast.model_max_size_percent` 設定提高或降低記憶體上限。


預測器會在可用記憶體的限制內，快取最常觀察到且最近觀察到的實體模型。對於較少出現的實體，每個間隔都會盡力從索引載入其模型，但不保證符合服務水準協議（SLA）。請務必使用具代表性的工作負載驗證記憶體使用量。

如需詳細資訊，請參閱部落格文章[改善異常偵測：一分鐘內處理一百萬個實體](https://opensearch.org/blog/one-million-enitities-in-one-minute/)。雖然該文章著重於異常偵測，但其中的建議也適用於預測，因為這兩項功能共用相同的底層隨機切割森林（RCF）模型。

## 步驟 2：新增模型參數

OpenSearch Dashboards 中的 **Suggest parameters** 按鈕會啟動近期歷史資料的檢視，以建議合理的預設值。您可以調整下列參數來覆寫這些預設值：

* **Forecasting interval** – 指定彙總桶的時間間隔（例如 10 分鐘）。較長的間隔可平滑雜訊並降低運算成本，但會延遲偵測。較短的間隔能更早偵測變化，但會增加資源使用量，且可能引入雜訊。請選擇仍能產生穩定訊號的最短間隔。
* **Window delay** – 告知預測器事件發生與資料匯入之間的預期延遲時間。此延遲會將預測間隔向前移，以確保完整涵蓋資料。例如，如果預測間隔為 10 分鐘，且匯入延遲 1 分鐘，將視窗延遲設為 1 分鐘可確保預測器評估 1:49 至 1:59 的資料，而非 1:50 至 2:00 的資料。
  * 為避免遺漏資料，請將視窗延遲設為預期匯入延遲的上限。不過，較長的延遲會降低預測的即時回應能力。
* **Horizon** – 指定要預測多少個未來的桶。預測準確度會隨預測時間的距離增加而下降，因此請僅選擇對實際作業有意義的預測視窗。
* **History** – 設定用於訓練初始（冷啟動）模型的歷史資料點數量。上限為 10,000。在此上限內，更多歷史資料可提高初始模型的準確度。

**Advanced** 面板預設為收合狀態，讓大多數使用者可使用建議的參數繼續操作。如果展開面板，您可以微調另外三個參數：[shingle 大小](#choosing-a-shingle-size)、[建議的季節性](#choosing-a-shingle-size)和[近期資料權重](#choosing-a-shingle-size)。這些參數控制預測器如何平衡近期波動與長期模式。

除非您的資料或使用案例有其他需求，否則預設值——**shingle 大小為 8**、**未明確指定季節性**及**近期資料權重為 2560**——是可靠的起始設定。

### 選擇 shingle 大小

將 **Shingle size** 欄位留空，以使用自動啟發式方法：

1. 從預設值 8 開始。
2. 如果已定義 **Suggested seasonality** 且其值大於 16，則將候選值替換為季節週期長度的一半。
3. 如果已定義 **Horizon** 且其值的三分之一大於目前的候選值，則據此更新候選值。

最終值為這三者中的最大值：
`max(8, seasonality ÷ 2, horizon ÷ 3)`

如果您提供自訂值，該值會覆寫此計算結果。

### 決定儲存空間用量

根據預設，預測結果會儲存在 `opensearch-forecast-results` 索引別名中。您可以：

* 建立儀表板和視覺化。
* 將結果連接至 Alerting 外掛程式。
* 像查詢任何其他 OpenSearch 索引一樣查詢結果。

為了管理儲存空間，此外掛程式會套用輪替原則：

* **輪替觸發條件** – 當主要分片達到約 65 GB 時，會建立新的後端索引並更新別名。
* **保留期** – 已輪替的索引會保留至少 30 天後才刪除。

您可以使用下列設定來自訂此行為。

| 設定 | 說明 | 預設值 |
|---------|-------------|---------|
| `plugins.forecast.forecast_result_history_max_docs_per_shard` | 觸發輪替前，每個分片允許的 Lucene 文件數上限。一筆結果約為 4 份文件，每份約 47 位元組，總計約 65 GB。 | `1_350_000_000` |
| `plugins.forecast.forecast_result_history_retention_period` | 預測結果的保留期間。支援 `7d`、`90d` 等期間格式。 | `30d` |

### 指定自訂結果索引

您可以選取 **Custom index** 並提供別名名稱 (例如 `abc`)，將預測結果儲存在自訂索引中。此外掛程式會建立類似 `opensearch-forecast-result-abc` 的別名，指向後端索引 (例如 `opensearch-forecast-result-abc-history-2024.06.12-000002`)。

若要管理權限，請使用以連字號分隔的命名空間。例如，將 `opensearch-forecast-result-financial-us-*` 指派給 `financial` 部門 `us` 群組的角色。
{: .note } 如果已啟用 Security 外掛程式，請確保已設定適當的[權限]({{site.url}}{{site.baseurl}}/observing-your-data/forecast/security/#custom-result-index-permissions)。

### 扁平化巢狀欄位

如果您的自訂結果索引文件包含巢狀欄位，請啟用 **Flattened custom result index** 以簡化彙總和視覺化。

這會建立一個以自訂索引和預測器名稱為前置字串的個別索引 (例如 `opensearch-forecast-result-abc-flattened-test`)，並附加使用 [Painless 指令碼](https://github.com/opensearch-project/anomaly-detection/blob/main/src/main/resources/scripts/flatten-custom-result-index-painless.txt) 的資料匯入管線來扁平化巢狀資料。如需詳細資訊，請參閱 [Painless 指令碼語言]({{site.url}}{{site.baseurl}}/scripting/painless/)。

如果您之後停用此選項，相關聯的資料匯入管線會遭到移除。

請使用 [Index State Management]({{site.url}}{{site.baseurl}}/im-plugin/ism/index/) 來管理扁平化結果索引的輪替和刪除。

### 自訂結果索引生命週期管理

當符合下列任一條件時，此外掛程式會觸發自訂結果索引的輪替。

| 參數 | 說明 | 類型 | 單位 | 預設值 | 必要 |
|----------|-------------|------|------|---------|----------|
| `result_index_min_size` | 觸發輪替所需的主要分片大小總和下限。 | 整數 | MB | `51200` (50 GB) | 否 |
| `result_index_min_age` | 觸發輪替所需的索引存在時間下限。 | 整數 | 天 | `7` | 否 |
| `result_index_ttl` | 已輪替索引遭到刪除前的最短保留時間 | 整數 | 天 | `60` | 否 |


## 步驟 3：測試您的預測器

回溯測試是評估及調整 **Interval** 和 **Horizon** 等重要預測設定的最快方式。在回溯測試期間，模型會以歷史資料進行訓練、產生預測，並將預測與實際值一起繪製，以協助您視覺化預測準確度。如果結果不符合預期，您可以調整設定並再次執行測試。

回溯測試使用下列方法：

1. **訓練視窗**：模型會以 **History** 設定所定義的歷史資料進行訓練。

2. **滾動預測**：模型會沿著時間序列推進，重複執行下列動作：
   * 匯入下一個實際資料點
   * 在每個步驟發出預測

   由於這是回溯模擬，預測值會繪製在其原始時間戳記上，讓您能看到模型在即時情況下可能達到的表現。


### 開始回溯測試

若要開始測試：

1. 捲動至 **Add model parameters** 頁面底部。
2. 選取 **Create and test**。

若要略過測試並立即建立預測器，請選取 **Create**。

回溯測試通常需要 1 到 2 分鐘，但執行時間取決於下列因素。

| 因素                | 重要性                                                           |
| --------------------- | ------------------------------------------------------------------------ |
| **歷史長度**    | 歷史資料越多，訓練時間越長。                            |
| **資料密度**      | 資料越密集，彙總速度越慢。                                   |
| **類別欄位** | 模型會為每個實體個別訓練。                             |
| **Horizon**           | 預測範圍越長，產生的預測數量越多。 |


如果圖表是空的 (如下圖所示)，請檢查您的索引在選取的間隔下是否包含至少一個具有超過 40 個資料點的時間序列。

![測試失敗]({{site.url}}{{site.baseurl}}/images/forecast/no_result.png){: width="800" height="800" }


### 解讀圖表

測試成功時，將游標停留在圖表上的任何點，即可檢視確切值和信賴界限：

- **實際資料** – 實線
- **中位數預測 (P50)** – 虛線
- **信賴區間** – P10 和 P90 之間的陰影帶

下圖顯示圖表檢視。

![含信賴界限的預測圖表]({{site.url}}{{site.baseurl}}/images/forecast/bound.png){: width="800" height="800" }

### 檢視特定日期的預測

預測圖表會顯示從最後一個實際資料點開始，到設定的預測範圍結束為止的預測。

例如，您可能會在 **Forecast from** 欄位中設定下列設定：

- **Last actual timestamp**：2025 年 3 月 5 日 19:23
- **Interval**：1 分鐘
- **Horizon**：24

使用這些設定時，預測範圍會涵蓋 `Mar 5, 2025, 19:23 – 19:47`，如下圖所示。

![顯示趨勢的預測圖表]({{site.url}}{{site.baseurl}}/images/forecast/trend.png){: width="800" height="800" }

您也可以使用 **Forecast from** 下拉式清單，檢視先前測試執行的預測，如下圖所示。

![Forecast from 下拉式清單]({{site.url}}{{site.baseurl}}/images/forecast/forecast_from_1.png){: width="800" height="800" }

當您選取較早的 **Forecast from** 時間時，預測線會直接繪製在該時刻可用的歷史資料上。這會導致兩個數列重疊，如下圖所示。

![重疊的預測與實際資料]({{site.url}}{{site.baseurl}}/images/forecast/forecast_from_2.png){: width="800" height="800" }

若要返回最近的預測視窗，請選取 **Show latest**。

### 疊加模式：並排準確度檢查

根據預設，圖表會顯示從單一原點開始的預測。切換「疊加模式」可將預測曲線直接疊在實際數列上，並檢查整個時間軸的準確度。

由於模型會在每個預測範圍步驟發出一個預測，例如預測範圍為 24 時會產生 24 個預測，因此單一時間戳記可能會有許多從不同原點產生的預測。疊加模式可讓您決定要繪製哪個前置時間 (k)：

* 預測範圍索引 0 = 緊接的下一個步驟
* 預測範圍索引 1 = 提前 1 個步驟
* 預測範圍索引 23 = 提前 23 個步驟

預測範圍控制項預設為 **索引 3**，但您可以選擇任何值，以聚焦於不同的前置時間。

下圖顯示已啟用疊加模式且預測範圍索引為 3。視覺化會將預測曲線 (紫色) 直接繪製在實際資料點 (以白色填充標記顯示) 上。這可讓您評估模型在整個時間軸上提前三步預測的準確度。預測範圍會以預測值周圍的陰影帶顯示，有助於突顯不確定性。

![疊加模式組態]({{site.url}}{{site.baseurl}}/images/forecast/overlay_3.png){: width="800" height="800" }

### 檢視多個預測序列

高基數的預測器可以同時顯示許多時間序列。使用結果面板中的 **Time series per page** 下拉式功能表，即可在下列檢視之間切換：

- **Single-series view** (預設)：每頁呈現一個實體，以獲得最佳可讀性。
- **Multi-series view**：最多並排繪製五個實體。信賴區間預設為半透明—將游標停留在某條線上，即可突顯其對應的區間。

實際線與預測線會重疊顯示，讓您可以逐點評估準確度。不過，在 **Multi-series view** 中，重疊的線條可能會讓圖表更難以解讀。若要減少視覺雜亂，請前往 **Visualization options** 並關閉 **Show actual data at forecast**。

下圖顯示實際線與預測線重疊的圖表。

![實際線與預測線重疊的圖表]({{site.url}}{{site.baseurl}}/images/forecast/toggle_overlay_before.png){: width="800" height="800" }

下圖顯示同一張圖表在預測時間點隱藏實際線後的簡化檢視。

![僅顯示預測線的圖表]({{site.url}}{{site.baseurl}}/images/forecast/toggle_overlay_after.png){: width="800" height="800" }


### 探索時間軸

使用下列時間軸控制項，即可瀏覽、放大及篩選預測歷史記錄中的任何時間範圍：

* **Zoom** – 選取 **+ / –** 以放大預測，或擴大檢視範圍。
* **Pan** – 使用箭頭按鈕移至較早或較晚的資料點 (若有)。
* **Quick Select** – 選擇常見的範圍，例如「Last 24 hours」，或為結果範圍提供自訂日期。

### 多序列檢視中的排序選項

當預測器追蹤超過五個實體時，圖表無法一次顯示所有線條。  
因此在 **Multi-series view** 中，您可以選擇五個最具資訊價值的序列，並透過選取排序方法來決定「具資訊價值」的定義。下表列出可用的排序方法。

| 排序方法 | 顯示內容 | 適用時機 |
|-------------|--------------|----------------|
| **Minimum confidence-interval width** *(預設)* | 預測區間最窄的五個序列。區間狹窄表示模型對其預測高度確定。 | 呈現最「值得信賴」的預測。 |
| **Maximum confidence-interval width** | 區間最寬的五個序列—模型最不確定的預測。 | 找出可能需要檢閱或更多訓練資料的高風險或雜訊序列。 |
| **Minimum value within the horizon** | 每個實體在預測範圍內的最低預測點，並以遞增順序排序。 | 找出預期下降幅度最大的實體—適合用於容量規劃或針對可能的下探發出警示。 |
| **Maximum value within the horizon** | 每個實體在預測範圍內的最高預測點，並以遞減順序排序。 | 突顯預期尖峰最大的序列，例如流量暴增或銷售激增。 |
| **Distance to threshold value** | 依數值閾值 (>, <, ≥, ≤) 篩選預測，再依其與該閾值的距離排序其餘項目。 | 調查違反—或幾乎違反—SLA 或業務 KPI 的實體，例如「顯示任何預測超過 10,000 次請求的項目」。 |

如果預測器監視五個或更少的實體，**Multi-series view** 會顯示全部實體。當超過五個時，每次您變更排序方法或調整閾值時，此檢視都會動態重新排序，確保最相關的序列保持聚焦。

若要聚焦於特定實體子集，請將 **Filter by** 切換為 **Custom query**，並輸入 query DSL 查詢。下列範例顯示 `host` 等於 `server_1` 的實體：

```json
{
  "nested": {
    "path": "entity",
    "query": {
      "bool": {
        "must": [
          { "term":     { "entity.name":  "host"     } },
          { "wildcard": { "entity.value": "server_1" } }
        ]
      }
    }
  }
}
```

接著選取排序方法，例如 **Maximum value within the horizon**，然後選取 **Update visualization**。圖表會更新，只顯示 `host:server_1` 的預測序列，並依您選取的準則排序。

### 編輯預測器

如果初始回溯測試顯示效能不佳，您可以調整預測器的組態並再次執行測試。

若要編輯預測器：

1. 開啟預測器的 **Details** 頁面，然後選取 **Edit** 進入編輯模式。  
2. 視需要修改設定—例如新增 **Category field**、變更 **Interval**，或增加 **History** 視窗。  
3. 選取 **Update**。驗證面板會自動評估新的組態，並標示任何問題。

   下圖顯示驗證程序正在進行中。

   ![驗證面板載入中]({{site.url}}{{site.baseurl}}/images/forecast/validation_loading.png){: width="800" height="800" }

4. 解決任何驗證錯誤。當面板變成綠色時，選取右上角的 **Start test**，以更新後的參數執行另一次回溯測試。

### 即時預測

當您對預測組態有信心後，請前往 **Details** 頁面並按一下 **Start forecasting**，開始即時預測。預測器之後會在每個間隔產生新的預測。

當圖表與最新資料同步時，會出現 **Live** 徽章。

與回溯測試不同，如果歷史資料不足，即時預測會持續嘗試使用即時資料進行初始化。在此初始化期間，預測器會顯示初始化狀態，直到有足夠的資料開始產生預測為止。

## 後續步驟

測試並調整預測器之後，您就可以開始使用它來產生即時預測，或長期管理它。若要了解如何啟動、停止、刪除或更新現有的預測器，請參閱[管理預測器]({{site.url}}{{site.baseurl}}/observing-your-data/forecast/managing-forecasters/)。

