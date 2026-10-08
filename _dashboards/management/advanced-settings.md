---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "進階設定"
parent: Dashboards management
nav_order: 10
---

# OpenSearch Dashboards 中的進階設定

使用 **Advanced settings** 頁面修改控制 OpenSearch Dashboards 行為的設定。這些設定可用於自訂應用程式的外觀與風格、變更特定功能的行為等。下圖顯示此介面的畫面。

![OpenSearch 2.14 中的進階設定介面]({{site.url}}{{site.baseurl}}/images/dashboards/advanced-settings.png){: width="700" }

若要存取 **Advanced settings**，請前往 **Dashboards Management** 並選取 **Advanced settings**。此頁面分為以下區段：[General](#general-settings)、[Appearance](#appearance-settings)、[Discover](#discover-settings)、[Notifications](#notifications-settings)、[Search](#search-settings)、[Timeline](#timeline-settings) 和 [Visualization](#visualization-settings)。每個區段都包含各自的一組設定。您可以編輯這些設定的欄位來修改設定。完成變更後，選取 **Save** 以套用變更。

{::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/icons/alert-icon.png" class="inline-icon" alt="alert icon"/>{:/} **注意**<br>某些設定需要您修改 [`opensearch_dashboards.yml` 檔案](https://github.com/opensearch-project/OpenSearch-Dashboards/blob/main/config/opensearch_dashboards.yml)並重新啟動 OpenSearch Dashboards。
{: .note}

## 必要權限

若要修改設定，您必須具備進行變更的權限。如需將角色存取權指派給租用戶的指引，請參閱[多租用戶組態]({{site.url}}{{site.baseurl}}/security/multi-tenancy/multi-tenancy-config/#give-roles-access-to-tenants)。

## 進階設定說明

下表說明核心進階設定。

### 一般設定

下表說明 **General** 設定。

設定 | 說明
:--- | :---
`csv:quoteValues`  | 定義是否將包含特殊字元的值或多行值以雙引號 `"` 括住。預設為 `On`。  |
`csv:separator`  | 定義是否使用特定字元或字串來分隔匯出的值。預設為 `,`。  |
`dateFormat`  | 定義日期的顯示格式。預設為 `MMM D, YYYY @ HH:mm:ss.SSS`。  |
`dateFormat:dow`  | 定義一週的起始日。預設為 `Sunday`。  |
`dateFormat:scaled`  | 定義時間戳記的格式。時間戳記格式會依測量之間的時間長度（小時、分鐘、秒和毫秒）而變更。鍵為 [ISO8601](https://www.iso.org/iso-8601-date-and-time-format.html) 格式的時間週期：`YYYY-MM-DD`。   |
`dateFormat:tz`  | 定義 OpenSearch Dashboards 的時區。預設為您的瀏覽器偵測到的時區。  |
`dateNanosFormat`  | 定義以奈秒表示日期的格式。預設為 `MMM D, YYYY @ HH:mm:ss.SSSSSSSSS`。  |
`defaultIndex`  | 定義 OpenSearch 叢集中所有索引的預設索引。若未新增任何索引，`defaultIndex` 會設為 `null`。但若新增了一個或多個索引，`defaultIndex` 會被指派為清單中第一個索引的值。預設為 `null`。  |
`defaultRoute`  | 定義入口點。使用此設定可變更 OpenSearch Dashboards 的登陸頁面。此設定必須是相對 URL。預設為 `/app/home`。 |
`fields:popularLimit` | 定義要顯示的欄位數量 N。預設為 `10`。  |
`filterEditor:suggestValues` | 定義篩選器編輯器是否建議欄位值。預設為 `Off`。  |
`filters:pinnedByDefault`  | 定義是否自動釘選篩選器。若要讓篩選器在所有應用程式中保持可見，您可以選取該篩選器，然後選取 **Pin across all apps** 選項。預設為 `Off.`  |
`format:bytes:defaultPattern`  | 定義位元組格式的預設數字格式。預設為 `0,0.[0]b`。  |
`format:currency:defaultPattern` | 定義貨幣格式的預設數字格式。預設為 `($0,0.[00])`。  |
`format:defaultTypeMap` | 使用對應定義每種欄位類型的預設格式名稱。若未指定欄位類型，則使用 `_default_`。  |
`format:number:defaultLocale`  | 定義數字的語言地區設定。預設為 `en`。  |
`format:number:defaultPattern`  | 定義數值格式的預設數字格式。預設為 `0,0.[000]`。  |
`format:percent:defaultPattern`  | 定義百分比格式的預設數字格式。預設為 `0,0.[000]%`。  |
`histogram:barTarget`  |  為使用 `auto` 間隔的日期長條圖定義指定的長條數量。預設為 `50`。  |
`histogram:maxBars`  | 定義日期長條圖中顯示的最大長條數量。預設為 `100`。  |
`history:limit` | 定義要在歷史記錄中儲存多少個最近的值。預設為 `10`。  |
`indexPattern:placeholder`  | 定義建立索引模式時使用的預留位置值。  |
`metaFields` | 允許將不屬於 `_source` 欄位的欄位合併至文件中。預設為 `_source`、`_id`、`_type`、`_index` 和 `_score`。  |
`metrics:max_buckets` | 定義單一資料來源可傳回的最大桶 (bucket) 數量。預設為 `2000`。  |
`query:allowLeadingWildcards`  | 定義是否允許 `*` 作為查詢子句的第一個字元。預設為 `On`。  | 
`query:queryString:options`  |  定義 Lucene 查詢字串剖析器的選項。預設為 `{ "analyze_wildcard": true }`。  |
`reporting:useFOR`  | 啟用或停用 `ForeignObject` 轉譯，以將外部內容嵌入報表中。只有在安裝報表外掛程式後，才會顯示 `reporting:useFOR` 和 `reporting:useOcr` 選項。預設為 `On`。  |
`reporting:useOcr`  | 啟用或停用 PDF 報表的光學字元辨識（OCR）。只有在安裝報表外掛程式後，才會顯示 `reporting:useFOR` 和 `reporting:useOcr` 選項。預設為 `Off`。  |
`savedObjects:listingLimit`  | 定義檢視清單頁面時要擷取的物件數量。預設為 `1000`。  |
`savedObjects:perPage`  | 定義載入對話方塊每頁顯示的物件數量。預設為 `20`。  |
`search:queryLanguage`  | 定義 OpenSearch Dashboards 的查詢語言。預設為 `DQL`。  |
`shortDots:enable`  | 啟用或停用縮短長欄位。預設為 `Off`。  |
`sort:options`  | 定義 sort 參數的選項。預設為 `boolean`。  |
`state:storeInSessionStorage`  | 啟用或停用 URL 工作階段儲存空間。預設為 `Off`。  |
`timepicker:quickRanges`  | 定義時間篩選器中顯示的快速選取時間範圍。  |
`timepicker:refreshIntervalDefaults` | 定義時間篩選器的預設重新整理間隔，以毫秒為單位。預設為 `0`。  |
`timepicker:timeDefaults`  | 定義資料分析的預設時間週期。預設為 `Last 15 minutes`。  |
`truncate:maxHeight`  | 定義表格儲存格的最大高度。預設為 `115` 像素。

## 外觀設定

下表說明 **Appearance** 設定。

設定 | 說明
:--- | :---
`accessibility:disableAnimations`  | 啟用或停用動畫。預設為 `Off`。  |
`pageNavigation`  | 定義導覽窗格樣式。預設為 `Modern`。  |
`theme:darkMode` | 啟用或停用深色模式。預設為 `Off`。深色模式僅適用於 OpenSearch Dashboards 2.10 及更新版本。 |
`theme:version`  | 定義目前及後續版本 OpenSearch Dashboards 所使用的佈景主題。預設為 `v7`。  |

## Discover 設定

下表說明 **Discover** 設定。

設定 | 說明
:--- | :---
`context:defaultSize`  | 定義在內容檢視中顯示的周圍項目數量。預設為 `5`。  |
`context:step`  | 定義增加或減少內容大小時的增減數量。預設為 `5`。  |
`context:tieBreakerFields`  | 定義當文件具有相同時間戳記值時，用來決定先後順序的欄位。系統會使用目前索引模式中第一個存在且可排序的欄位。預設為 `_doc`。  |
`defaultColumns`  | 定義 **Discover** 頁面上預設顯示的欄。預設為 `_source`。  |
`discover:aggs:terms:size`  | 定義在欄位下拉式選單中選取 **Visualize** 按鈕時，要視覺化的詞彙數量。預設為 `20`。  |
`discover:modifyColumnsOnSwitch`  | 定義是否從新的索引模式中移除無法使用的欄。預設為 `On`。  |
`discover:sampleSize`  | 定義表格中顯示的列數。預設為 `20`。  |
`discover:searchOnPageLoad`  | 定義 **Discover** 首次載入時是否執行搜尋。此設定不影響已儲存搜尋的載入。預設為 `On`。  |
`discover:sort:defaultOrder`  | 定義以時間為基礎的索引模式的排序方式。預設為 `Descending`。  |
`doc_table:hideTimeColumn`  | 定義是否在 **Discover** 應用程式及所有已儲存的儀表板搜尋中隱藏 `Time` 欄。預設為 `Off`。  |
`doc_table:highlight`  | 定義是否在 **Discover** 應用程式及儀表板上的已儲存搜尋中醒目提示結果。醒目提示可讓您更容易找到並識別結果，但處理大型文件時也可能拖慢請求速度。  |

## 通知設定

下表說明 **Notifications** 設定。

設定 | 說明
:--- | :---
`notifications:banner`  | 定義用於暫時性使用者通知的自訂橫幅。支援 [Markdown](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax)。  |
`notifications:lifetime:banner`  | 定義橫幅通知的顯示時間長度。預設為 `3000000` 毫秒。將欄位設為 `Infinity` 即可停用通知。  |
`notifications:lifetime:error`  | 定義錯誤通知的顯示時間長度。預設為 `300000` 毫秒。將欄位設為 `Infinity` 即可停用通知。  |
`notifications:lifetime:info`  | 定義資訊通知的顯示時間長度。預設為 `5000` 毫秒。將欄位設為 `Infinity` 即可停用通知。  |
`notifications:lifetime:warning`  | 定義警告通知的顯示時間長度。預設為 `10000` 毫秒。將欄位設為 `Infinity` 即可停用通知。

## 搜尋設定

下表說明 **Search** 設定。

設定 | 說明
:--- | :--- 
`courier:batchSearches`  | 啟用或停用儀表板面板的載入方式。停用時，面板會個別載入，且使用者離開頁面或更新查詢時，搜尋請求就會結束。啟用時，所有面板會在所有資料載入完成後一起載入，且搜尋不會結束。預設為 `Off`。  |
`courier:customRequestPreference`  | 指定是否搭配 `custom` 設定使用[請求偏好設定]({{site.url}}{{site.baseurl}}/api-reference/popular-api/)。預設為 `_local`。  |
`courier:ignoreFilterIfFieldNotInIndex`  | 啟用或停用對包含使用不同索引之視覺化的儀表板的支援。停用時，所有篩選條件都會套用至所有視覺化。啟用時，若視覺化的索引不包含要篩選的欄位，則會忽略該視覺化的篩選條件。預設為 `Off`。  |
`courier:maxConcurrentShardRequests`  | 定義 OpenSearch Dashboards 針對 `_msearch` 請求可發起的並行分片請求數量上限。設為 `0` 可停用此設定，並使用 OpenSearch 設定的預設值。預設為 `0`。  |
`courier:setRequestPreference`  | 定義由哪些分片處理您的搜尋請求。選項包括 **Session ID**、**Custom** 和 **None**。**Session ID** 會限制作業，讓所有搜尋請求都在同一個分片上執行，並在請求之間重複使用分片快取，這可提升效能。**Custom** 用於定義您自己的偏好設定。請使用 `courier:customRequestPreference` 自訂您的偏好設定值。**None** 表示未設定任何偏好設定。此選項可提供較佳的效能，因為請求可以分散到所有分片複本上。不過，由於不同分片可能處於不同的重新整理狀態，結果可能會不一致。預設為 `Session ID`。  |
`search:includeFrozen`  | 指定是否在搜尋結果中包含凍結索引。若啟用，搜尋結果會包含凍結索引。搜尋凍結索引可能會增加搜尋時間。預設為 `Off`。  |

## 時間軸設定

下表說明 **Timeline** 設定。

設定 | 說明
:--- | :--- 
`timeline:es.default_index`  | 定義使用 `.opensearch()` 函式時要搜尋的預設 OpenSearch 索引。若未設定，`.opensearch()` 函式會搜尋所有索引。預設為 `_all`。  | 
`timeline:es.timefield`  | 定義使用 `.opensearch()` 函式時的預設時間戳記欄位。若未設定，則會在 `@timestmap` 欄位中使用 `.opensearch()` 函式。預設為 `@timestmap`。  |
`timeline:graphite.url`  | （實驗性）定義 Graphite 主機 URL。  |
`timeline:max_buckets`   | 定義單一資料來源可傳回的桶 (bucket) 數量上限。預設為 `2000`。  |
`timeline:min_interval`  | 定義使用 `auto` 間隔時要計算的最小間隔。預設為 `1ms`。  |
`timeline:quandl.key`  | （實驗性）定義可讓您存取 Quandl 資料的唯一識別碼 (API 金鑰)。  |
`timeline:target_buckets`  | 定義 OpenSearch Dashboards 在計算視覺化中的自動間隔時嘗試使用的桶數量。預設為 `200`。  |

## 視覺化設定

下表說明 **Visualization** 設定。

設定 | 說明
:--- | :--- 
`visualization:colorMapping`  | 為視覺化中的值指派色彩。預設為 `#00A69B`。  |
`visualization:dimmingOpacity`  | 定義當另一個圖表元素被醒目提示時，變暗的圖表項目的不透明度。值越低，醒目提示的元素就越突出。值必須介於 `0` 與 `1` 之間。預設為 `0.5`。  |
`visualization:enablePluginAugmentation`  | 啟用或停用透過折線圖視覺化存取外掛程式功能。預設為 `On`。  |
` line chart visualizations`  | 定義每個視覺化可關聯的擴充項目數量上限。預設為 `10`。每個視覺化關聯超過 10 個外掛程式資源可能會造成效能問題。  |
`visualization:heatmap:maxBuckets`  | 定義在熱度圖視覺化中，單一資料來源可傳回的桶數量上限。桶數量越多，可能會對瀏覽器的轉譯效能造成負面影響。預設為 `50`。 |
`visualization:regionmap:customVectorMapMaxSize`  | 定義可從自訂向量地圖載入的圖徵數量上限。預設為 `1000`。  |
`visualization:regionmap:showWarnings`  | 指定當詞彙無法與區域地圖上的形狀聯結時，是否顯示警告。預設為 `On`。  |
`visualization:tileMap:WMSdefaults`  | 定義座標地圖中 Web Map Service (WMS) 地圖伺服器的預設[屬性](https://leafletjs.com/reference.html#tilelayer-wms)。預設為 `enabled: false`。  |
`visualization:tileMap:maxPrecision`  | 定義地圖上可顯示的 geohash 精確度上限，其中 7 為高，10 為非常高，12 為最大值。預設為 `7`。  |
`visualize:disableBucketAgg`  | 停用視覺化中的特定桶彙總。此設定接受以逗號分隔的桶彙總名稱清單，例如 `significant_terms` 和 `terms`。  |
`visualize:enableLabs`  | 啟用或停用實驗性視覺化。啟用時，您可以建立、檢視及編輯實驗性視覺化。停用時，您只能使用已可用於正式環境的視覺化。預設為 `On`。  |
