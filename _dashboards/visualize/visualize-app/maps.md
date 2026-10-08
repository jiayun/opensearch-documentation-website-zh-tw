---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "Maps 應用程式"
parent: Visualization types
grand_parent: Creating visualizations in the Visualize application
great_grand_parent: Building data visualizations
has_children: true
has_toc: false
nav_order: 105
redirect_from:
  - /dashboards/visualize/maps/
  - /dashboards/maps-plugin/
  - /dashboards/maps/
---

# Maps 應用程式

**Maps** 應用程式可建立包含多個圖層的地圖視覺化，結合不同索引中的資料。您可以從不同的索引模式建立每個圖層，並設定地圖在不同的縮放層級顯示特定資料。OpenSearch 地圖由 OpenSearch 地圖服務提供支援，該服務使用向量圖磚來轉譯地圖。

## 何時使用 Maps 應用程式

當您需要結合不同索引資料的多圖層地理視覺化、依地理形狀篩選、自訂底圖、工具提示或標籤時，請使用 Maps 應用程式。若要建立較簡單的單一圖層地理視覺化，請考慮使用[座標地圖]({{site.url}}{{site.baseurl}}/dashboards/visualize/coordinate-maps/)或[區域地圖]({{site.url}}{{site.baseurl}}/dashboards/visualize/region-maps/)。

## 建立新地圖

您可以透過下列步驟，從 **Maps** 或 **Visualize** 工作流程建立新地圖：

- 若要從 **Maps** 工作流程建立新地圖，請執行下列步驟：

  1. 在頂端功能表列中，前往 **OpenSearch Plugins > Maps**。
  1. 選擇 **Create map** 按鈕。

- 若要從 **Visualize** 工作流程建立新地圖，請執行下列步驟：

  1. 在頂端功能表列中，前往 **OpenSearch Dashboards > Visualize**。
  1. 選擇 **Create visualization** 按鈕。
  1. 在 **New Visualization** 對話方塊中，選擇 **Maps**。

現在您可以看到預設的 OpenSearch 底圖。

若要檢查 **Default map** 圖層組態，請在地圖左上方的 **Layers** 面板中選取 **Default map**，如下圖所示。

![預設地圖]({{site.url}}{{site.baseurl}}/images/maps/maps-default.png){: width="900" }

若要隱藏 **Layers** 面板，請選取面板右上角的摺疊（箭頭）圖示。
{: .tip}

## 圖層設定

若要變更預設地圖設定，請在 **Layers** 面板中選取 **Default map**。在 **Layer settings** 下，您可以變更圖層名稱和描述，並設定圖層的縮放層級和不透明度：

- **Zoom levels**：根據預設，圖層在所有縮放層級皆可見。若您希望圖層僅在特定縮放層級範圍內可見，可以在文字方塊中輸入縮放層級，或將範圍滑桿拖曳至所需的值來指定。

- **Opacity**：若您的地圖包含多個圖層，一個圖層可能會遮蔽另一個圖層。在此情況下，您可以降低頂層圖層的不透明度，以便同時看到兩個圖層。

## 新增圖層

若要將圖層新增至地圖，請在 **Layers** 面板中選取 **Add layer** 按鈕。**Add layer** 對話方塊如下圖所示。

![新增圖層]({{site.url}}{{site.baseurl}}/images/maps/add-layer.png){: width="450" }

您可以將**基礎圖層**或**資料圖層**新增至地圖：

- **基礎圖層**可作為底圖。若要使用您自己的地圖或第三方地圖作為基礎圖層，請[將其新增為 **Custom map**](#adding-a-custom-map)。

- **資料圖層**可讓您將來自各種資料來源的資料視覺化。

## 新增自訂地圖

OpenSearch 支援 Web Map Service (WMS) 或 Tile Map Service (TMS) 自訂地圖。若要新增 TMS 自訂地圖，請執行下列步驟：

1. 在 **Layers** 面板中，選取 **Add layer** 按鈕。
1. 在 **Add layer** 對話方塊中，選取 **Base layer > Custom map**。
    在 **New layer** 對話方塊中依照後續步驟操作，該對話方塊如下圖所示。

    ![新增自訂地圖]({{site.url}}{{site.baseurl}}/images/maps/custom-map.png)

1. 在 **Custom type** 下拉式清單中，選取 **Tile Map Service (TMS)**。
1. 輸入 TMS URL。
1. （選用）在 **TMS attribution** 中，輸入底圖的 TMS 出處標示。例如，若您使用自訂底圖，請輸入自訂地圖名稱。此名稱會顯示在地圖的右下角。
1. 選取 **Settings** 索引標籤以編輯圖層設定。
1. 在 **Name** 中輸入圖層名稱。
1. （選用）在 **Description** 中輸入圖層描述。
1. （選用）選取此圖層的縮放層級和不透明度。
1. 選取 **Update** 按鈕。

## 新增文件圖層

新增文件圖層可讓您將資料視覺化。每個文件圖層可新增一個索引模式。若要檢視多個索引模式，請建立多個圖層。

文件圖層可顯示 geopoint 和 geoshape 文件欄位。
{: .note}

下列範例假設您已安裝 `opensearch_dashboards_sample_data_flights` 資料集。若您尚未安裝此資料集，請執行下列步驟：

1. 在左上方，選取首頁圖示。
1. 選取 **Add sample data**。
1. 在 **Sample flight data** 面板中，選取 **Add data** 按鈕。

依照下列方式新增文件圖層：

1. 在 **Layers** 面板中，選取 **Add layer** 按鈕。
1. 在 **Add layer** 對話方塊中，選取 **Data layer > Documents**。
1. 在 **Data source** 中，選取 `opensearch_dashboards_sample_data_flights`。或者，您也可以輸入其他要視覺化的索引模式。
1. 在 **Geospatial field** 中，選取要在視覺化中顯示的地理空間欄位（geopoint 或 geoshape）。在此範例中，請選取 `DestLocation`。
1. （選用）選取 **Style** 索引標籤以變更填滿色彩、框線色彩、框線粗細或標記大小。
1. 選取 **Settings** 索引標籤以編輯圖層設定。
1. 在 **Name** 中輸入 `Flight destination`。
1. 選取 **Update** 按鈕。
1. 若要查看更多資料，請在右上角選取日曆圖示下拉式清單，然後在 **Quick select** 下選擇 **Last 15 days**，並選取 **Apply** 按鈕。

您應該會看到航班目的地資料，如下圖所示。

![航班目的地地圖]({{site.url}}{{site.baseurl}}/images/maps/new-layer.png)

## 篩選資料

若要顯示索引中的部分資料，請篩選資料。您可以在圖層層級篩選資料，或在地圖上繪製形狀，以全域方式篩選所有圖層資料。

### 在圖層層級篩選資料

若要在圖層層級篩選資料，請選取圖層並為其新增篩選條件。

下列範例示範如何篩選航班目的地資料，僅顯示美國境內的目的地：

1. 在 **Layers** 面板中，選取 **Flight destination**。
1. 選取 **Filters**。
1. 選取 **Add filter**。
1. 在 **Edit filter** 中，於 **Field** 選取 **DestCountry**。
1. 在 **Operator** 中，選取 **is**。
1. 在 **Value** 中，選取 **US**。
1. 選取 **Save** 按鈕。
1. 選取 **Update** 按鈕。

對於大型資料集，您可能希望避免載入整個地圖的資料。若要僅載入特定地理區域的資料，請選取 **Only request data around map extent**。
{: .tip}

### 繪製形狀以篩選資料

您可以在地圖上繪製[形狀]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/geo-shape/)，以全域方式篩選資料。若要在地圖上繪製矩形或多邊形，請執行下列步驟：

1. 選取地圖右側的 **Rectangle** 或 **Polygon** 圖示。
1. 在 **Filter label** 欄位中，輸入篩選條件的名稱。
1. 選擇空間關係類型。根據預設，會選取 **Intersects**。如需空間關係類型的詳細資訊，請參閱[空間關係]({{site.url}}{{site.baseurl}}/query-dsl/geo-and-xy/xy#spatial-relations)。
1. 選取 **Draw Rectangle** 或 **Draw Polygon** 按鈕。
1. 在您要選取的地圖區域上繪製形狀：
  - 若要繪製矩形，請在地圖上選取任一起點（此點會成為矩形的頂點）。接著將游標移至（請勿拖曳）地圖上的另一點並選取該點（此點會成為對角頂點）。
  - 若要繪製多邊形，請在地圖上選取任一起點（此點會成為多邊形的頂點），然後將游標移至（請勿拖曳）後續的每個頂點並選取該點。最後，請務必再次選取起點以封閉多邊形，如下圖所示。

![在地圖上繪製多邊形]({{site.url}}{{site.baseurl}}/images/maps/draw-shape.png)

### 停用地圖圖層的形狀篩選器

根據預設，形狀篩選器會全域套用至地圖上的所有圖層。若要停用某個地圖圖層的形狀篩選器，請執行下列步驟：
1. 從 **Layers** 面板中選取該圖層。
1. 在 **Filters** 區段中，取消選取 **Apply global filters**。
1. 選取 **Update** 按鈕。

### 修改現有的形狀篩選器

若要修改現有的形狀篩選器，請在地圖上方左上角選取您的篩選器。您可以對現有篩選器執行下列操作：

- **Edit filter**：變更篩選器名稱或修改形狀的座標。
- **Exclude results**：反轉篩選器，也就是顯示篩選器所套用之資料點 _以外_ 的所有資料點。
- **Temporarily disable**：停用篩選器，直到您選取 **Re-enable** 為止。
- **Delete**：完全移除您的篩選器。

## 使用工具提示將其他資料視覺化

文件圖層會將 geopoint 與 geoshape 文件欄位顯示為地圖上的位置。若要為這些位置加入更多資訊，您可以使用工具提示。例如，您可能想在 **Flight destination** 圖層中顯示航班延誤、目的地天氣及目的地國家資訊。請執行下列步驟來設定工具提示以顯示其他資料：

1. 在 **Layers** 面板中，選取 **Flight destination**。
1. 選取 **Tooltips**。
1. 選取 **Show tooltips** 核取方塊。
1. 在 **Tooltip fields** 下拉式清單中，選取您想顯示的欄位。在此範例中，請選取 `FlightDelay`、`DestWeather` 及 `DestCountry`。
1. 選取 **Update** 按鈕。

若要檢視工具提示，請將滑鼠游標停留在您感興趣的地理點上。一個工具提示可以顯示多個資料點。例如，在 **Flight destination** 圖層中，單一目的地城市會有多個航班。若要分頁瀏覽這些航班，請選取您感興趣的城市，並使用工具提示中的箭頭，如下圖所示。

![航班目的地工具提示]({{site.url}}{{site.baseurl}}/images/maps/tooltip.png){: width="450" }

如果地圖上的某個點包含來自多個圖層的資料，一個工具提示可以顯示來自多個圖層的資料。若要查看所有圖層，請選取 **All layers**。若要選擇特定圖層，請在工具提示的圖層選取面板中選取該圖層名稱，如下圖所示。

![含有圖層選取面板的工具提示]({{site.url}}{{site.baseurl}}/images/maps/layer-selection-panel.png){: width="450" }

## 為圖層加入標籤

為圖層加入標籤可讓您在地圖上將其他資料視覺化。例如，您可能想在 **Flight destination** 圖層中查看出發地天氣。請執行下列步驟，為 **Flight destination** 圖層加入標籤：

1. 在 **Layers** 面板中，選取 **Flight destination**。
1. 在 **Style** 索引標籤中，選取 **Add label** 核取方塊。
1. 您可以選擇為圖層中的所有資料點加入以固定文字為基礎的標籤，或使用欄位值作為標籤文字。
  - 若要加入固定文字標籤，請在 **Label text** 下選取 **Fixed**，並輸入所需的標籤文字。
  - 若要加入以欄位值為基礎的標籤，請在 **Label text** 下選取 **Field value**，並選取欄位名稱。在此範例中，請選取 `OriginWeather`。
1. （選用）變更標籤大小、色彩、框線色彩或框線寬度。
1. 選取 **Update** 按鈕。

含有出發地天氣的標籤會顯示在地圖上，同時也會加入工具提示中，如下圖所示。

![以欄位類型為基礎的標籤已加入地圖與工具提示]({{site.url}}{{site.baseurl}}/images/maps/label.png){: width="450" }

## 重新排序、隱藏及刪除圖層

**Layers** 面板可讓您重新排序、隱藏及刪除圖層：

- 地圖上的圖層會彼此堆疊。若要重新排序圖層，請使用圖層名稱旁的把手（兩條水平線）圖示，將圖層拖曳至所需位置。

- 若要隱藏圖層，請選取圖層名稱旁的顯示/隱藏（眼睛）圖示。再次切換顯示/隱藏圖示即可重新顯示該圖層。

- 若要刪除圖層，請選取圖層名稱旁的刪除（垃圾桶）圖示。

## 重新整理即時資料集的資料

若要將即時資料集視覺化，請在將圖層加入地圖後，執行下列步驟來設定重新整理間隔：

1. 選取右上角的日曆圖示。
1. 在 **Refresh every** 下，選取或輸入重新整理間隔（例如 1 秒）。
1. 選取 **Start** 按鈕。

![重新整理地圖]({{site.url}}{{site.baseurl}}/images/maps/refresh.png){: width="450" }

## 儲存地圖

若要儲存包含您所設定之所有圖層的地圖，請執行下列步驟：

1. 選取右上角的 **Save** 按鈕。
1. 在 **Save map** 對話方塊中，於 **Title** 文字方塊輸入地圖名稱。
1. （選用）在 **Description** 文字方塊中，輸入地圖說明。
1. 選取 **Save** 按鈕。

若要開啟已儲存的地圖，請選擇左上角的 **Maps**。系統會顯示已儲存的地圖清單。

## 將地圖加入儀表板

您可以執行下列步驟，將新的或現有的地圖加入新的或現有的儀表板：

- 若要將地圖加入新的儀表板，請先依下列方式建立儀表板：

  1. 在頂端選單列中，前往 **OpenSearch Dashboards > Dashboard**。
  1. 選擇 **Create dashboard** 按鈕。
  1. 選擇 **Create new** 按鈕。

- 若要將地圖加入現有的儀表板，請先依下列方式開啟儀表板：
  1. 在頂端選單列中，前往 **OpenSearch Dashboards > Dashboard**。
  1. 從清單中選取您要開啟的儀表板。
  1. 在右上角選擇 **Edit**。

開啟儀表板後，您可以在其中加入新的或現有的地圖。

### 加入現有的地圖

1. 在頂端選單中，選擇 **Add**。
1. 在 **Types** 下拉式清單中，選取 **Maps**。
1. 從清單中選取您要加入的地圖。

### 加入新的地圖

1. 在頂端選單中，選擇 **Create new** 按鈕。
1. 在 **New Visualization** 對話方塊中，選擇 **Maps**。
1. 透過加入底圖、圖層或工具提示來編輯預設地圖。
1. 在右上角選擇 **Save** 按鈕。
1. 在 **Save map** 對話方塊中，輸入地圖的 **Title** 及選用的 **Description**。
1. 選取 **Add to Dashboard after saving**（此選項預設為選取）。
1. 選擇 **Save and return** 按鈕。

## 從儀表板編輯地圖

1. 在儀表板中，選擇您要編輯之地圖右上角的齒輪圖示。
1. 選擇 **Edit maps**。
1. 編輯地圖。
1. 在右上角選擇 **Save** 按鈕。
1. 在 **Save map** 對話方塊中，選擇 **Save and return** 按鈕。

## 相關文件

- [Maps Stats API]({{site.url}}{{site.baseurl}}/dashboards/visualize/maps-stats-api/)
- [設定地圖]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualize-app/configuring-maps/)