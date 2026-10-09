---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "異常偵測"
nav_order: 120
has_children: true
redirect_from:
  - /monitoring-plugins/ad/
  - /monitoring-plugins/ad/index/
  - /observing-your-data/ad/
---

# 異常偵測

OpenSearch 中的_異常_是指時間序列資料中任何不尋常的行為變化。異常可以為您的資料提供寶貴的洞察。例如，對 IT 基礎架構資料而言，記憶體使用量指標中的異常有助於及早發現系統故障的徵兆。

視覺化和儀表板等傳統技術可能難以發掘異常。雖然可以根據靜態閾值設定警示，但這種方法需要領域知識，而且可能無法適應有機成長或季節性趨勢的資料。

異常偵測會使用 Random Cut Forest (RCF) 演算法，以近乎即時的方式自動偵測 OpenSearch 資料中的異常。RCF 是一種非監督式機器學習演算法，會為傳入的資料串流建立模型草圖，以計算每個傳入資料點的_異常等級_和_信賴分數_。這些數值用於區分異常與正常變化。如需 RCF 運作方式的詳細資訊，請參閱 [Robust Random Cut Forest Based Anomaly Detection on Streams](https://www.semanticscholar.org/paper/Robust-Random-Cut-Forest-Based-Anomaly-Detection-on-Guha-Mishra/ecb365ef9b67cd5540cc4c53035a6a7bd88678f9)。

您可以將 Anomaly Detection 外掛程式與 [Alerting 外掛程式]({{site.url}}{{site.baseurl}}/monitoring-plugins/alerting/)搭配使用，在偵測到異常時立即通知您。
{: .note}

## 在 OpenSearch Dashboards 中開始使用異常偵測

若要開始使用，請前往 **OpenSearch Dashboards** > **OpenSearch Plugins** > **Anomaly Detection**。

## 步驟 1：定義偵測器

_偵測器_是一個獨立的異常偵測任務。您可以定義多個偵測器，而且所有偵測器可以同時執行，各自分析來自不同來源的資料。您可以依照下列步驟定義偵測器：

1. 在 **Anomaly detection** 頁面上，選取 **Create detector** 按鈕。
2. 在 **Define detector** 頁面上，新增偵測器詳細資訊。輸入名稱和簡短描述。名稱必須是唯一的，並且具有足夠的描述性，以協助您識別偵測器的用途。

3. 在 **Select data** 窗格中，從 **Index** 下拉式選單選取一個或多個來源，以指定資料來源。您可以選取索引、索引模式或別名。

   - 偵測器可以使用遠端索引，您可以透過 `cluster-name:index-name` 模式存取。如需詳細資訊，請參閱[跨叢集搜尋]({{site.url}}{{site.baseurl}}/search-plugins/cross-cluster-search/)。您也可以直接選取叢集和索引。如果已啟用 Security 外掛程式，請參閱[異常偵測安全性]({{site.url}}{{site.baseurl}}/observing-your-data/ad/security/)文件中的[以細微存取控制選取遠端索引]({{site.url}}{{site.baseurl}}/observing-your-data/ad/security/#selecting-remote-indexes-with-fine-grained-access-control)。

   - 若要在 OpenSearch Dashboards 中建立跨叢集偵測器，您必須具備下列[權限]({{site.url}}{{site.baseurl}}/security/access-control/permissions/)：`indices:data/read/field_caps`、`indices:admin/resolve/index` 和 `cluster:monitor/remote/info`。

4. (選用) 選取 **Add data filter**，然後指定 **Field**、**Operator** 和 **Value** 的條件，以篩選資料來源。或者，選取 **Use query DSL**，並以 JSON 格式的[布林查詢]({{site.url}}{{site.baseurl}}/query-dsl/compound/bool/)輸入篩選條件。查詢特定領域語言 (DSL) 僅支援布林查詢。




### 範例：使用 query DSL 篩選資料

下列範例查詢會擷取 `urlPath.keyword` 欄位符合任何指定值的文件：

```json
 {
    "bool": {
       "should": [
             {
                "term": {
                   "urlPath.keyword": "/domain/{id}/short"
                }
             },
             {
                "term": {
                   "urlPath.keyword": "/sub_dir/{id}/short"
                }
             },
             {
                "term": {
                   "urlPath.keyword": "/abcd/123/{id}/xyz"
                }
             }
       ]
    }
 }
```
{% include copy-curl.html %}

5. 在 **Timestamp** 窗格中，從 **Timestamp field** 下拉式清單選取一個欄位。

6. (選用) 若要將異常偵測結果儲存在自訂索引中，請選取 **Enable custom results index**，並提供索引名稱 (例如 `abc`)。此外掛程式會建立一個以 `opensearch-ad-plugin-result-` 為前置詞、後接您所選名稱的別名 (例如 `opensearch-ad-plugin-result-abc`)。此別名指向名稱包含日期和序號的實際索引，例如 `opensearch-ad-plugin-result-abc-history-2024.06.12-000002`，您的結果會儲存在其中。

您可以使用 `-` 來分隔命名空間，以管理自訂結果索引的權限。例如，如果您使用 `opensearch-ad-plugin-result-financial-us-group1` 作為結果索引，您可以根據 `opensearch-ad-plugin-result-financial-us-*` 模式建立權限角色，以細微層級代表 `us` 群組的 `financial` 部門。
{: .note }

#### 權限

啟用 Security 外掛程式 (細微存取控制) 時，預設結果索引會變成系統索引，且無法再透過標準 Index 或 Search API 存取。若要存取其內容，您必須使用 Anomaly Detection RESTful API 或儀表板。因此，如果已啟用 Security 外掛程式，您就無法使用預設結果索引建立自訂儀表板。不過，您可以建立自訂結果索引來建立自訂儀表板。

如果您指定的自訂索引不存在，Anomaly Detection 外掛程式會在您建立偵測器並開始即時或歷史分析時建立它。

如果自訂索引已存在，此外掛程式會驗證索引對應是否符合異常結果所需的結構。在此情況下，請確保自訂索引具有 [`anomaly-results.json`](https://github.com/opensearch-project/anomaly-detection/blob/main/src/main/resources/mappings/anomaly-results.json) 檔案中定義的有效對應。
若要使用自訂結果索引選項，您必須具備下列權限：

- `indices:admin/create` -- 需要 `create` 權限才能建立及輪替自訂索引。
- `indices:admin/aliases` -- 需要 `aliases` 權限才能建立及管理自訂索引的別名。
- `indices:data/write/index` -- 需要 `write` 權限才能將結果寫入單一實體偵測器的自訂索引。
- `indices:data/read/search` -- 需要 `search` 權限才能搜尋自訂結果索引，以在 Anomaly Detection 介面上顯示結果。
- `indices:data/write/delete` -- 偵測器可能會產生大量異常結果。需要 `delete` 權限才能刪除舊資料並節省磁碟空間。
- `indices:data/write/bulk*` -- 需要 `bulk*` 權限，因為外掛程式使用 Bulk API 將結果寫入自訂索引。

#### 攤平巢狀欄位

包含巢狀欄位的自訂結果索引對應會造成彙總和視覺化方面的挑戰。**Enable flattened custom result index** 選項會攤平自訂結果索引中的巢狀欄位。選取此選項時，外掛程式會建立一個以自訂結果索引名稱和偵測器名稱為前置詞的個別索引。例如，如果偵測器 `Test` 使用自訂結果索引 `abc`，則會由一個具有別名 `opensearch-ad-plugin-result-abc-flattened-test` 的個別索引來儲存巢狀欄位已攤平的異常偵測結果。

除了建立個別索引之外，外掛程式還會設定一個包含指令碼處理器的資料匯入管線。此管線繫結至該個別索引，並使用 Painless 指令碼攤平自訂結果索引中的所有巢狀欄位。如需詳細資訊，請參閱 [Painless scripting language]({{site.url}}{{site.baseurl}}/scripting/painless/)。

在執行中的偵測器上停用此選項會移除其攤平用的資料匯入管線；它也不再是結果索引的預設值。
使用攤平自訂結果選項時，請考慮下列事項：

- Anomaly Detection 外掛程式會根據自訂結果索引和偵測器名稱建構索引名稱，而由於偵測器名稱可以編輯，因此可能會發生衝突。如果發生衝突，外掛程式會重複使用該索引名稱。
- 管理自訂結果索引時，請考慮下列事項：
   - Anomaly Detection 儀表板會查詢所有自訂結果索引中的所有偵測器結果。自訂結果索引過多可能會影響外掛程式的效能。
   - 您可以使用 [Index State Management]({{site.url}}{{site.baseurl}}/im-plugin/ism/index/) 來輪替舊的結果索引。您也可以手動刪除或封存任何舊的結果索引。建議將自訂結果索引重複用於多個偵測器。

當自訂結果索引符合下表中的任一條件時，外掛程式會將別名輪替至新索引。

參數 | 說明 | 類型 | 單位 | 範例 | 必要
:--- | :--- |:--- |:--- |:--- |:---
`result_index_min_size` | 索引輪替所需的最小主要分片總大小 (不含副本)。當索引有 5 個主要分片及 5 個副本分片，且每個分片皆為 20 GiB，並將此值設為 100 GiB 時，就會執行輪替。 | `integer` | `MB` | `51200` | 否
`result_index_min_age` | 輪替所需的最小索引存在時間，從索引建立時間計算至目前時間。 | `integer` |`day` | `7` | 否
`result_index_ttl` | 刪除已輪替索引所需的最小存在時間。 | `integer` | `day` | `60` | 否

定義偵測器設定之後，選取 **Next** 以設定模型。

## 步驟 2：設定模型

為您的偵測器新增特徵。_特徵_ 是某個欄位的彙總或 Painless 指令碼。偵測器可以跨一或多個特徵探索異常。

您必須為每個特徵選擇彙總方法：`average()`、`count()`、`sum()`、`min()` 或 `max()`。彙總方法決定什麼構成異常。例如，若選擇 `min()`，偵測器會專注於根據特徵的最小值尋找異常。若選擇 `average()`，偵測器會根據特徵的平均值尋找異常。

您也可以使用[自訂 JSON 彙總查詢](#configuring-a-model-based-on-a-json-aggregation-query)作為彙總方法。如需建立 JSON 彙總查詢的更多資訊，請參閱 [Query DSL]({{site.url}}{{site.baseurl}}/opensearch/query-dsl/index/)。


對於每個已設定的特徵，您也可以選取異常條件。預設情況下，當實際值異常地高於或低於預期值時，模型會偵測到異常。不過，您可以自訂特徵設定，讓系統只在實際值高於預期值（表示資料出現尖峰）或低於預期值（表示資料出現低谷）時才記錄異常。例如，為 `cpu_utilization` 欄位建立偵測器時，您可以選擇只在數值出現尖峰時記錄異常，以減少警示疲勞。


### 使用以門檻為基礎的規則抑制異常

在 **Feature selection** 窗格中，您可以設定規則來抑制異常，這些規則以絕對值或相對百分比定義預期值與實際值之間可接受的差異。這有助於減少由微小波動造成的錯誤異常，讓您能專注於顯著的偏差。

若要抑制與預期值偏差小於 30% 的異常，您可以在特徵選取窗格中設定下列規則：

- 當實際值高出預期值不超過 30% 時，忽略異常。
- 當實際值低於預期值不超過 30% 時，忽略異常。

下圖顯示名為 `LogVolume` 的特徵窗格，您可以在其中設定相對偏差百分比設定：

![新增具有抑制規則之特徵的介面]({{site.url}}{{site.baseurl}}/images/anomaly-detection/add-feature-with-relative-rules.png){: width="800" height="800" }

如果您預期記錄量應與預期值相差至少 10,000 才視為異常，您可以設定下列絕對門檻：

- 當實際值高出預期值不超過 10,000 時，忽略異常。
- 當實際值低於預期值不超過 10,000 時，忽略異常。

下圖顯示名為 `LogVolume` 的特徵窗格，您可以在其中設定絕對門檻設定：

![新增絕對值抑制規則的介面]({{site.url}}{{site.baseurl}}/images/anomaly-detection/add-suppression-rules-absolute.png){: width="800" height="800" }

若未設定自訂抑制規則，系統會預設使用一個篩選器，對每個已啟用的特徵忽略與預期值偏差小於 20% 的異常。

多特徵模型會跨其所有特徵關聯異常。[維度詛咒](https://en.wikipedia.org/wiki/Curse_of_dimensionality)使得多特徵模型相較於單特徵模型，較不容易識別較小的異常。新增更多特徵可能會對模型的[精確率與召回率](https://en.wikipedia.org/wiki/Precision_and_recall)造成負面影響。資料中雜訊比例越高，會進一步放大此負面影響。若要為異常選擇最佳的特徵集上限，我們建議採用反覆測試不同上限的流程。預設情況下，偵測器的特徵數上限為 `5`。若要調整此上限，請使用 `plugins.anomaly_detection.max_anomaly_features` 設定。
{: .note}

### 根據彙總方法設定模型

若要根據彙總方法設定異常偵測模型，請依照下列步驟操作：

1. 在 **Detectors** 頁面上，從清單中選取所需的偵測器。
2. 在偵測器的詳細資料頁面上，選取 **Actions** 按鈕以開啟下拉式選單，然後選取 **Edit model configuration**。
3. 在 **Edit model configuration** 頁面上，選取 **Add another feature** 按鈕。
4. 在 **Feature name** 欄位中輸入名稱，並勾選 **Enable feature** 核取方塊。
5. 在 **Find anomalies based on** 下方的下拉式選單中選取 **Field value**。
6. 在 **Aggregation method** 下方的下拉式選單中選取所需的彙總方式。
7. 在 **Field** 下方的下拉式選單中，從列出的選項中選取所需的欄位。
8. 選取 **Save changes** 按鈕。

### 根據 JSON 彙總查詢設定模型

若要根據 JSON 彙總查詢設定異常偵測模型，請依照下列步驟操作：

1. 在 **Edit model configuration** 頁面上，選取 **Add another feature** 按鈕。
2. 在 **Feature name** 欄位中輸入名稱，並勾選 **Enable feature** 核取方塊。
3. 在 **Find anomalies based on** 下方的下拉式選單中選取 **Custom expression**。JSON 編輯器視窗將會開啟。
4. 在編輯器中輸入您的 JSON 彙總查詢。
5. 選取 **Save changes** 按鈕。

如需可接受的 JSON 查詢語法，請參閱 [OpenSearch Query DSL]({{site.url}}{{site.baseurl}}/opensearch/query-dsl/index/)。
{: .note}

### 為高基數設定類別欄位

您可以根據 keyword 或 IP 欄位類型來分類異常。您可以啟用 **Categorical fields** 選項，使用某個維度（例如 IP 位址、產品 ID 或國家碼）對來源時間序列進行分類或「切片」。這讓您能以細緻的視角檢視類別欄位中每個實體內的異常，協助隔離與除錯問題。

若要設定類別欄位，請選取 **Enable categorical fields** 並選取一個欄位。建立偵測器後，您無法變更類別欄位。

類別欄位僅支援一定數量的唯一實體。請使用下列公式計算叢集中建議支援的實體總數：

```
(data nodes * heap size * anomaly detection maximum memory percentage) / (entity model size of a detector)
```

若要取得偵測器的實體模型大小，請使用 [Profile Detector API]({{site.url}}{{site.baseurl}}/monitoring-plugins/ad/api/#profile-detector)。您可以使用 `plugins.anomaly_detection.model_max_size_percent` 設定來調整最大記憶體百分比。

假設有一個包含 3 個資料節點的叢集，每個節點具有 8 GB 的 JVM heap 大小以及預設的 10% 記憶體配置。在實體模型大小為 1 MB 的情況下，下列公式可計算估計的唯一實體數量：

```
(8096 MB * 0.1 / 1 MB ) * 3 = 2429
```

如果唯一實體的實際總數高於您計算出的數量（在此例中為 2,429），則異常偵測器會嘗試為額外的實體建立模型。偵測器會優先處理出現頻率較高且較新的實體。

此公式僅作為起點。請務必以具代表性的工作負載進行測試。如需更多資訊，請參閱 OpenSearch 部落格文章 [Improving Anomaly Detection: One million entities in one minute](https://opensearch.org/blog/one-million-enitities-in-one-minute/)。
{: .note }

#### 作業設定

OpenSearch Dashboards 中的 **Suggest parameters** 按鈕會啟動近期歷史記錄的檢閱，以建議合理的預設值。您可以調整下列參數來覆寫這些預設值。

##### 偵測器間隔

指定彙總桶大小 (例如 10 分鐘)。您應根據實際的資料特性來設定偵測器間隔：

- **較長的間隔**：可平滑化雜訊並降低運算成本，但會延遲偵測。
- **較短的間隔**：可更快偵測到變更，但會增加資源用量，並可能引入雜訊。

間隔必須夠大，讓您很少遺漏資料。模型使用 shingling (連續、相鄰的桶)，而遺漏的桶會降低資料品質與 shingle 的形成。

##### 頻率 (選用)

指定工作查詢、評分及寫入結果的頻率。較短的值可提供更即時的更新，但成本較高；較長的值可降低負載，但會拖慢更新速度。頻率必須是間隔的倍數，且預設為間隔值。

如果您不確定，請將此欄位留空---工作預設會使用間隔值。

**使用大於間隔的頻率的常見情境包括：**

1. **批次處理短桶以提升效率**：在高頻率或高資料量的記錄檔串流中，不需要超快速的警示。對於需要大量連接操作或具有高基數特性的工作負載，或需要**不可變的每日異常帳冊**以供檢閱或稽核的法規遵循導向夜間彙總，每 1--2 分鐘執行一次偵測器可能很浪費。反之，請將偵測器排程為較不頻繁地執行，讓它一次批次處理許多短間隔 (例如 **6 小時**，一次處理約 **360** 個 1 分鐘桶)。請選擇符合您警示延遲與成本目標的頻率 (例如 30 分鐘、1 小時、3 小時、6 小時或 12 小時)。

  - **優點**：降低排程負擔並提升資源使用率，尤其是在執行許多工作或叢集忙碌時。
  - **取捨**：增加偵測延遲---1 分鐘桶中的異常可能只有在批次執行時才會回報。
  - **最適合**：成本與負載控制、法規遵循與稽核。

2. **配合不頻繁或批次記錄檔匯入**：當記錄檔不規則地或以批次方式送達時 (例如每天一次從 S3 送達，或 IoT 裝置以突發方式上傳)。每分鐘執行偵測器大多會產生空結果並浪費週期。請將頻率設定為接近資料送達速率 (例如 1 天)，讓每次搜尋更有可能找到新資料。當時間戳記不規則且資料量偏低時 (零星的記錄檔常見的情況)，過渡結果往往會損害準確性，因為 RCF 模型是有狀態的，並假設時間戳記嚴格遞增。藉由使用較不頻繁的排程，您實際上可讓工作等待完整資料，而不是反覆檢查空索引。

   - **優點**：減少無意義的查詢與 CPU 負擔；提升效率與更準確的結果——異常將在批次記錄檔送達後進行評估，且幾乎沒有誤判過渡異常的風險。
   - **取捨**：異常評估的頻率較低。
   - **最適合**：批次工作與零星記錄檔匯入模式。

##### 視窗延遲 (選用)

若要為資料收集增加額外的處理時間，請指定 **Window delay** 值。這會向偵測器表示資料並非即時匯入 OpenSearch，而是有某種延遲。

**運作方式**：

設定視窗延遲可位移偵測器間隔，以因應匯入延遲。例如：
- 偵測器間隔：10 分鐘
- 資料匯入延遲：1 分鐘
- 偵測器執行時間：下午 2:00

若沒有視窗延遲，偵測器會嘗試取得下午 1:50–2:00 的資料，但只取得 9 分鐘的資料，遺漏了下午 1:59–2:00 的資料。將視窗延遲設為 1 分鐘會將間隔視窗位移至下午 1:49–1:59，確保偵測器擷取到全部 10 分鐘的資料。

**最佳做法**：
- 將 **Window delay** 設為預期匯入延遲的上限，以避免遺漏資料。
- 在資料準確性與及時偵測之間取得平衡——延遲太長會妨礙即時異常偵測。

##### 歷史記錄 (選用)

設定用於訓練初始 (冷啟動) 模型的歷史資料點數目。上限為 10,000 個資料點。在該上限內，更多歷史記錄可提升初始模型的準確性。

##### 在頻率與視窗延遲之間做選擇

**frequency** 與 **window delay** 都能處理匯入延遲，但較適合不同的資料模式：

- **Window delay**：最適合串流資料 (持續少量送達)
- **Frequency**：最適合批次資料 (週期性大量送達)

**範例情境**：

- **範例 A -- 資料每分鐘送達，但總是遲 1 天 → 使用 window delay**：
   - **模式**：`Day-1 00:01, 00:02, ..., 23:59` 的資料穩定送達，但只在 `Day-2` 的相同分鐘標記送達。
   - **組態**：`interval = 1 min`、`window_delay = 1 day`、`frequency = 1 min`。
   - **效果**：
      - `Day-2 00:01` 的執行會處理 `Day-1 00:01` 的資料。
      - `Day-2 00:02` 的執行會處理 `Day-1 00:02` 的資料。
      - ...
      - `Day-2 23:59` 的執行會處理 `Day-1 23:59` 的資料。
   - **為何適合**：每分鐘的資料都以可預測的 24 小時延遲送達。設定 1 天的視窗延遲可確保每筆記錄在其預定的時間戳記進行處理，同時讓工作負載保持增量。

- **範例 B -- `Day-1` 的所有資料都在 `Day-2 00:00` 送達 → 使用每日頻率**：
   - **模式**：`Day-1` 期間沒有資料出現；反之，包含全部 1,440 分鐘資料的單一批次會在 `Day-2 00:00` 送達。
   - **組態**：`interval = 1 min`、`frequency = 1 day` (一次處理整天)。
   *(提示：新增一個小的 `window_delay`——例如 1–5 分鐘——以因應索引或重新整理的延遲。)*
   - **效果**：
      - **最佳情況**：如果偵測器在 `00:00` 左右啟動，`Day-2 00:00` 的執行會在 `Day-1` 的資料送達後立即處理所有資料。
      - **最壞情況**：如果偵測器在 `23:59` 左右啟動，每日執行要到 `Day-2 23:59` 才會發生，大約是資料送達後的 `24 hours`。
      - **一般規則**：對於午夜資料送達，額外的等待時間等於您偵測器的每日啟動時間。
   - **為何可行**：因為整天的資料會一次全部可用，單次每日執行比逐分鐘處理資料有效率得多。

下圖說明使用視窗延遲與使用頻率來處理 1 天匯入延遲的時序差異。時間軸顯示第 1 天匯入 (上方)、使用 `window_delay = 1 day` 的第 2 天處理 (中間，連續帶狀)，以及當 `frequency = 1 day` 時的單次每日執行 (下方，垂直長條)。視您何時啟動偵測器而定，每日頻率可能會在第 1 天結束後不久觸發 (最佳情況，額外延遲極少)，或晚得多才觸發 (最壞情況，最多約 +1 天)。工作會每天在您首次啟動它的時間左右執行。

![時間軸顯示第 1 天匯入 (上方)、使用視窗延遲的第 2 天處理 (中間)，以及當頻率 = 1 天時的單次每日執行 (下方)]({{site.url}}{{site.baseurl}}/images/anomaly-detection/window-delay-vs-frequency.png){: width="1200" height="350" }


### 設定 shingle 大小

在 **Advanced settings** 窗格中，您可以設定要納入偵測視窗的資料串流彙總間隔數量。請根據您的實際資料選擇此值，以找出最適合您使用案例的設定。若要設定 shingle 大小，請在 **Advanced settings** 窗格中選取 **Show**，並在 **intervals** 欄位中輸入所需的大小。

異常偵測器要求 shingle 大小必須介於 1 到 128 之間。預設值為 `8`。只有在您至少有兩個特徵時才使用 `1`。小於 `8` 的值可能會提高[召回率](https://en.wikipedia.org/wiki/Precision_and_recall)，但也可能增加誤報。大於 `8` 的值可能有助於忽略訊號中的雜訊。

### 設定遺漏值填補選項

在 **Advanced settings** 窗格中，您可以設定遺漏值填補選項。這可讓您管理資料串流中的遺漏資料。選項包括以下幾種：

- **Ignore Missing Data (Default)：** 系統會繼續運作，不考慮遺漏的資料點，維持現有的資料流。
- **Fill with Custom Values：** 為每個特徵指定自訂值以取代遺漏的資料點，讓您能針對自己的資料進行目標式的遺漏值填補。
- **Fill with Zeros：** 以零取代遺漏的值。當資料缺席代表重大事件時（例如事件計數降至零），這是理想的選擇。
- **Use Previous Values：** 以最後觀察到的值填補間隙，以維持時間序列資料的連續性。此方法將遺漏資料視為非異常，延續先前的趨勢。

使用這些選項可以改善異常偵測的召回率。例如，如果您正在監視事件計數的下降（包括部分下降和完全下降），以零填補遺漏值有助於偵測重大的資料缺席，進而提升偵測召回率。

在大量遺漏資料時進行填補請務必謹慎，因為過多的間隙可能會影響模型準確性。輸入品質至關重要——資料品質不佳會導致模型效能不佳。發生遺漏值填補時，信心分數也會降低。您可以使用異常結果索引中的 `feature_imputed` 欄位來檢查特徵值是否已被填補。如需更多資訊，請參閱[異常結果對應]({{site.url}}{{site.baseurl}}/monitoring-plugins/ad/result-mapping/)。
{: note}


### 預覽範例異常

您可以根據範例特徵輸入預覽異常，並視需要調整特徵設定。Anomaly Detection 外掛程式會選取少量資料樣本——例如每 30 分鐘 1 個資料點——並使用內插法估算其餘資料點，以近似實際的特徵資料。樣本資料集會載入偵測器，偵測器再使用該樣本資料集產生異常預覽。

1. 選取 **Preview sample anomalies**。
    - 如果未顯示範例異常結果，請檢查偵測器間隔，確認在預覽日期範圍內為實體設定了 400 個以上的資料點。
2. 選取 **Next** 按鈕。

## 步驟 3：設定偵測器工作

若要啟動偵測器以近乎即時地找出資料中的異常，請選取 **Start real-time detector automatically (recommended)**。

或者，如果您想執行歷史分析，並在較長的歷史資料視窗（數週或數月）中尋找模式，請勾選 **Run historical analysis detection** 方塊，並選取至少 128 個偵測間隔的日期範圍。

分析歷史資料可以幫助您熟悉 Anomaly Detection 外掛程式。例如，您可以針對歷史資料評估偵測器的效能，以便進行微調。

您可以在使用即時偵測器之前，先以不同的特徵集實驗歷史分析，並檢查精確度。

## 步驟 4：檢閱偵測器設定

檢閱您的偵測器設定與模型組態，確認其有效後，再選取 **Create detector**。

如果發生驗證錯誤，請編輯設定以修正錯誤，然後返回偵測器頁面。
{: .note }

## 步驟 5：觀察結果

選取 **Real-time results** 或 **Historical analysis** 索引標籤。若為即時結果，顯示異常結果需要一些時間。例如，如果偵測器間隔為 10 分鐘，偵測器可能需要一小時才會啟動，因為它正在等待足夠的資料才能產生異常。

較短的間隔會讓模型更快通過 shingle 處理程序，並更快產生異常結果。您可以使用 [profile detector]({{site.url}}{{site.baseurl}}/monitoring-plugins/ad/api#profile-detector) 操作來確認您有足夠的資料點。

如果偵測器停留在「initialization」狀態超過 1 天，請彙總現有資料，並使用偵測器間隔檢查是否有遺漏的資料點。如果發現許多遺漏的資料點，請考慮增加偵測器間隔。

在異常折線圖上按住並拖曳即可放大，檢視異常的詳細畫面。
{: .note }

您可以使用下列視覺化來分析異常：

- **Live anomalies**（適用於即時結果）顯示最近 60 個間隔的即時異常結果。例如，如果間隔為 `10`，則會顯示最近 600 分鐘的結果。圖表每 30 秒重新整理一次。
- **Anomaly overview**（適用於即時結果）或 **Anomaly history**（適用於 **Historical analysis** 索引標籤上的歷史分析）會繪製異常等級與對應的信心量測值。該窗格包括：
    - 依據給定資料時間範圍計算的異常發生次數。
    - **Average anomaly grade**：介於 0 到 1 之間的數字，表示資料點的異常程度。異常等級為 `0` 代表「非異常」，非零值則代表異常的相對嚴重性。
    - **Confidence**：所回報異常等級符合預期異常等級的機率估計值。隨著模型觀察到更多資料並學習資料行為與趨勢，信心會隨之提高。請注意，信心與模型準確性不同。
    - **Last anomaly occurrence**：最後一次異常發生的時間。

在 **Anomaly overview** 與 **Anomaly history** 之下可以找到下列區段：

- **Feature breakdown** 依據彙總方法繪製特徵。您可以變更偵測器的日期時間範圍。選取特徵折線圖上的某個點，會顯示 **Feature output**（欄位在索引中出現的次數）以及 **Expected value**（特徵輸出的預測值）。在沒有異常的情況下，輸出值與預期值會相等。

- **Anomaly occurrences** 顯示每個偵測到的異常的 `Start time`、`End time`、`Data confidence` 與 `Anomaly grade`。若要在 Discover 中檢視與某次異常相關的記錄檔，請在 **Actions** 欄位中選取 **View in Discover** 圖示。記錄檔包含開始與結束時間前後各 10 分鐘的緩衝資料。

選取異常折線圖上的某個點，會顯示 **Feature Contribution**，即該特徵對異常的貢獻百分比。

如果您設定了類別欄位，會看到額外的 **Heat map** 圖表。熱度圖會將異常實體的結果相互關聯。在您選取某個異常實體之前，此圖表是空白的。您也會看到該異常時段的異常折線圖與特徵折線圖（`anomaly_grade` > 0）。


如果您設定了多個類別欄位，可以選取欄位的子集來篩選與排序欄位。選取欄位子集可讓您查看某個欄位中與另一個欄位共用相同值的前幾名值。

例如，如果您的偵測器具有類別欄位 `ip` 與 `endpoint`，您可以在 **View by** 下拉式選單中選取 `endpoint`。然後選取特定儲存格，將 `ip` 的前 20 名值疊加在圖表上。Anomaly Detection 外掛程式預設會選取排名最前面的 `ip`。您最多可以同時查看 5 個個別的時間序列值。

## 步驟 6：設定警示

在 **Real-time results** 底下，選取 **Set up alerts**，並設定監視器，以便在偵測到異常時通知您。如需有關如何建立監視器並根據您的異常偵測器設定通知的指示，請參閱[設定異常警示]({{site.url}}{{site.baseurl}}/observing-your-data/ad/managing-anomalies/)。

如果您停止或刪除偵測器，請務必刪除與其相關聯的任何監視器。

## 檢視及更新偵測器組態

若要檢視偵測器的所有組態設定，請選取 **Detector configuration** 索引標籤。

1. 若要對偵測器組態進行任何變更，或微調時間間隔以盡量減少誤判，請前往 **Detector configuration** 區段並選取 **Edit**。
   您必須停止即時與歷史分析，才能變更偵測器的組態。請確認您要停止偵測器並繼續。
   {: .important}
2. 若要啟用或停用特徵，請在 **Features** 區段中選取 **Edit**，並視需要調整特徵設定。完成變更後，請選取 **Save and start detector**。

## 管理您的偵測器

若要啟動、停止或刪除偵測器，請前往 **Detectors** 頁面。

1. 選取偵測器名稱。
2. 選取 **Actions**，然後選取 **Start real-time detectors**、**Stop real-time detectors** 或 **Delete detectors**。
