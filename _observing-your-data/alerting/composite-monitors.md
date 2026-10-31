---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "複合監視器"
nav_order: 25
parent: Monitors
grand_parent: Alerting
has_children: false
---

# 複合監視器

## 關於複合式監視器

警示功能中的基本[監視器類型]({{site.url}}{{site.baseurl}}/observing-your-data/alerting/monitors/#monitor-types)設計用來定義單一觸發條件類型。例如，每文件監視器可以根據查詢與文件的相符情形觸發警示，而每桶監視器則可以根據針對資料來源中彙總值的查詢觸發警示。複合式監視器會依序結合多個監視器，根據多項條件分析資料來源，然後利用各監視器的個別警示產生單一的鏈結警示。這讓您能夠取得資料來源更細微的資訊，而且不需要手動協調各個監視器的排程。

由於複合式監視器傳送的是單一鏈結警示，而不是每個委派監視器各傳送一則警示，因此可減少使用者收到的警示數量。委派監視器會依您定義的順序以單次執行方式執行，因此您不需要協調它們的排程。

## 重要詞彙

下表的重要詞彙說明複合監視器的基本概念。如需所有類型監視器通用的其他詞彙，請參閱 Alerting 一節中的[重要詞彙]({{site.url}}{{site.baseurl}}/observing-your-data/alerting/index/#key-terms)。

| 詞彙 | 定義 |
| :--- | :--- |
| 複合監視器 | 複合監視器是一種支援以循序工作流程執行多個監視器的監視器類型。它支援設定觸發條件以建立連鎖警示。 |
| 委派監視器 | 委派監視器會依據其在複合監視器定義中的順序循序執行。當委派監視器的觸發條件符合時，它會產生稽核警示。此稽核警示接著會成為複合監視器觸發條件的條件。複合監視器支援每查詢、每桶及每文件監視器作為委派監視器。 |
| workflow ID | workflow ID 為所有委派監視器的整個工作流程提供識別碼。它與複合監視器的 monitor ID 同義。 |
| 連鎖警示 | 當委派監視器產生稽核警示時，連鎖警示會從複合監視器觸發條件產生。連鎖警示觸發條件支援使用邏輯運算子 `AND`、`OR` 及 `NOT`，因此您可以將多個函式結合成單一運算式。 |
| 稽核警示 | 委派監視器會產生處於 **audit** 狀態的警示。使用者不會收到每個個別稽核警示的通知，也不需要確認它們。稽核警示用於評估複合監視器中的連鎖警示觸發條件。 |
| 執行 | 在複合監視器組態中定義的順序中，所有委派監視器的單次執行。 |

## 基本工作流程

您可將個別監視器結合成工作流程來建立複合監視器，該工作流程會依定義的順序執行每個監視器。當委派監視器的個別稽核警示符合複合監視器的觸發條件時，複合監視器會產生自己的連鎖警示。請考量下列事件順序，以了解設定兩個委派監視器的簡單複合監視器如何執行其工作流程。在此範例中，當第一個監視器與第二個監視器都產生警示時，即符合複合監視器的觸發條件。

1. 複合監視器開始執行並將其委派給第一個監視器。第一個監視器的觸發條件符合，並產生稽核警示。
1. 複合監視器接著將執行委派給第二個監視器。第二個監視器的觸發條件也符合，並產生自己的稽核警示。
1. 由於複合監視器的觸發條件要求第一個與第二個監視器都產生稽核警示，因此複合監視器接著會觸發連鎖警示。
1. 若在複合監視器的定義中設定了通知，使用者會收到連鎖警示的通知。不過，他們不會收到兩個委派監視器所產生的個別稽核警示。

在這個簡單範例中，第一個監視器可以是設定為使用三個不同查詢分析資料來源的每文件監視器，而第二個監視器則可以是依用戶端 IP 彙總資料的每桶監視器。透過結合每個委派監視器的需求，複合監視器會聚焦於決定是否產生警示的準則。這可提升警示的意義，同時移除沒有確定價值的多餘警示。


## 使用 API 管理組合監視器

若要使用 REST API 建立和管理組合監視器與鏈結警示，請參閱 [Composite Monitor API]({{site.url}}{{site.baseurl}}/observing-your-data/alerting/composite-monitors-api/)。

## 在 OpenSearch Dashboards 中建立複合監視器

首先前往 OpenSearch Dashboards 的 **Create monitor** 頁面：**Alerting > Monitors**，然後選取 **Create monitor**。為監視器命名，然後選取 **Composite monitor** 作為監視器類型。建立複合監視器工作流程與觸發條件的步驟，會因您使用 **Visual editor** 或 **Extraction query editor** 而有所不同。前者提供定義複合監視器的基本 UI 選取器，後者則允許您使用指令碼建立工作流程與觸發條件。決定使用哪種方法後，請參閱對應的章節。

### 視覺化編輯器

若要使用視覺化編輯器定義工作流程與觸發條件，請在 **Monitor defining method** 區段中選取 **Visual editor** 單選按鈕。如下圖所示。

![選取 Visual editor]({{site.url}}{{site.baseurl}}/images/alerting/vis-editor.png){: width="50%" }

若要在視覺化編輯器中完成建立複合監視器，請依照下列步驟操作：

1. 在 **Frequency** 下拉式清單中，選取 **By interval**、**Daily**、**Weekly**、**Monthly** 或 **Custom cron expression**：
  * **By interval** — 允許您根據指定的分鐘、小時或天數重複執行排程。
  * **Daily** — 指定一天中的時間與時區。
  * **Weekly** — 指定一週中的某一天、一天中的時間與時區。
  * **Monthly** — 指定一個月中的某一天、一天中的時間與時區。
  * **Custom cron expression** — 為排程建立自訂 cron 運算式。可使用 **cron expressions** 連結協助建立這些運算式，或參閱 [Cron 運算式]({{site.url}}{{site.baseurl}}/api-reference/cron-expressions/)。

1. 在 **Delegate monitors** 區段中，透過下拉式清單選取要納入工作流程的個別監視器。在 **Visual editor** 中，選取監視器的順序會決定它們在工作流程中的順序。
  
   選取 **Add another monitor** 以新增另一個下拉式清單。至少需要兩個委派監視器，總計最多允許 10 個。請注意，複合監視器支援以每查詢、每桶及每文件監視器作為委派監視器。
   
   在每個下拉式清單旁，您可以選取檢視監視器圖示 ({::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/dashboards/view-monitor-icon.png" class="inline-icon" alt="view monitor icon"/>{:/}) 以開啟監視器的詳細資訊視窗，並檢視其相關資訊。
   
1. 為複合監視器定義一或多個觸發條件。在 **Triggers** 區段中，選取 **Add trigger**。新增觸發條件名稱，然後定義觸發條件。
    * 使用 **Select delegate monitor** 標籤開啟下圖所示的快顯視窗。
    
    ![此快顯視窗顯示選取委派監視器與觸發條件運算子的選項]({{site.url}}{{site.baseurl}}/images/alerting/trigger1.png){: width="50%" }
    
    * 使用 **Select delegate monitor** 下拉式清單，從先前步驟中定義的監視器中選取一個委派監視器。對於第一個委派監視器，您可以視需要選取 NOT 作為運算子。監視器填入欄位後，您可以使用清單右側的垃圾桶圖示 ({::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/alerting/trash-can-icon.png" class="inline-icon" alt="trash can icon"/>{:/}) 在需要時移除該監視器。
    * 選取第一個監視器右側的加號 ({::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/alerting/plus-sign-icon.png" class="inline-icon" alt="plus sign"/>{:/}) 以選取第二個委派監視器。選取第二個監視器後，選取其中一個運算子 `AND`、`OR`、`AND NOT` 或 `OR NOT`，將條件套用於兩個監視器之間。套用運算子後，您可以選取該運算子再次開啟快顯視窗並變更選取項目。
    * 選取警示的嚴重性等級。選項包括 **1 (Highest)**、**2 (High)**、**3 (Medium)**、**4 (Low)** 與 **5 (Lowest)**。
    * 在 **Notifications** 區段中，從下拉式清單選取通知頻道。如果沒有任何頻道，請選取下拉式清單右側的 **Manage channels** 標籤以設定通知頻道。如需通知的詳細資訊，請參閱[通知]({{site.url}}{{site.baseurl}}/observing-your-data/notifications/index/)文件。您也可以選取 **Add notification** 為警示觸發條件指定其他通知。
      
      所有監視器類型的通知皆為選用。
      {: .note }

    * 若要定義其他觸發條件，請選取 **Add another trigger**。總計最多可有 10 個觸發條件。選取畫面右側的 **Remove trigger** 以移除觸發條件。
    
1. 完成監視器工作流程並定義觸發條件後，選取畫面右下角的 **Create**。複合監視器即建立完成，並會開啟監視器的詳細資訊視窗。

### 擷取查詢編輯器

若要使用擷取查詢編輯器來定義工作流程與觸發條件，請在 **Monitor defining method** 區段中選取 **Extraction query editor** 選項按鈕。如下圖所示。

![選取 Extraction query editor]({{site.url}}{{site.baseurl}}/images/alerting/extract-q-editor.png){: width="50%" }

擷取查詢編輯器遵循與視覺化編輯器相同的一般步驟，但可讓您使用 API 查詢中的擷取內容來建立複合監視器工作流程與警示觸發條件。這讓您能夠建立視覺化編輯器不支援的進階組態。下列各節提供這兩個欄位各自的內容範例。建立複合監視器的其他所有步驟皆與視覺化編輯器相同。

* **Define workflow**
  
  在 **Define workflow** 欄位中，輸入定義委派監視器及其在工作流程中順序的序列。下列範例顯示工作流程中包含的委派監視器，以及它們在序列中的順序：

  ```json
  {
      "sequence": {
          "delegates": [
              {
                  "order": 1,
                  "monitor_id": "0TgBZokB2ZtsLaRvXz70"
              },
              {
                  "order": 2,
                  "monitor_id": "8jgBZokB2ZtsLaRv6z4N"
              }
          ]
      }
  }
  ```
  
  工作流程中包含的所有委派監視器都需要 `monitor_id` 以及 `order` 的值。
  
* **Trigger condition**
  
  在 **Trigger condition** 欄位中，輸入監視器以及用來定義其間條件的運算子。此欄位要求觸發條件必須以 Painless 指令碼語言格式化。若要了解這些指令碼如何形成觸發條件，請參閱[使用 Painless 指令碼定義連鎖警示觸發條件]({{site.url}}{{site.baseurl}}/observing-your-data/alerting/composite-monitors-api/#defining-chained-alert-trigger-conditions)。

  下列範例顯示一個觸發條件，要求第一個監視器或第二個監視器產生稽核警示後，複合監視器才能產生連鎖警示：

  ```painless
  (monitor[id=8d36S4kB0DWOHH7wpkET] || monitor[id=4t36S4kB0DWOHH7wL0Hk])
  ```

### 檢視監視器詳細資料

建立複合監視器後，它會出現在 **Monitors** 索引標籤的監視器清單中。**Type** 欄會指出監視器類型，包括複合監視器類型。**Associations with composite monitors** 欄會提供基本監視器作為委派監視器用於多少個複合監視器的計數。在 **Monitor name** 欄中選取監視器，即可開啟其詳細資料視窗。

對於複合監視器，詳細資料視窗的 **Alerts** 區段包含 **Actions** 欄，其中包含檢視詳細資料圖示 ({::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/dashboards/view-monitor-icon.png" class="inline-icon" alt="view monitor icon"/>{:/})。下圖顯示 **Actions** 欄位於最右側的最後一欄。

![監視器詳細資料視窗的警示區段]({{site.url}}{{site.baseurl}}/images/alerting/comp-details-alerts.png){: width="75%" }

選取此圖示可開啟 **Alert details** 視窗。此視窗會顯示屬於產生連鎖警示之執行作業一部分的所有稽核警示，並包含產生稽核警示的委派監視器。選取視窗右上角的 **X** 以關閉 **Alert details**。

返回監視器詳細資料視窗的 **Alerts** 區段後，您可以選取 **Alert start time** 左側的核取方塊來醒目顯示該警示。醒目顯示警示後，您可以選取此區段右上部分的 **Acknowledge**。警示即會確認，且 **State** 欄中的狀態會從 Active 變更為 Acknowledged。 
