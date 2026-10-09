---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "使用尋找結果"
parent: Using Security Analytics
nav_order: 35
---

# 使用尋找結果

**Findings** 視窗包含檢視與處理尋找結果的功能。兩項主要功能如下：
* 依數量、日期以及記錄檔類型或規則嚴重性排列的長條圖，顯示尋找結果資訊。
* 依時間、尋找結果 ID、規則名稱及其他詳細資料排列的 **Findings** 清單。

您隨時可以選擇 **Refresh** 來重新整理 **Findings** 頁面上的資訊。

---
## 尋找結果圖表

尋找結果圖表可以依記錄檔類型或規則嚴重性顯示尋找結果。使用 **Group by** 下拉式清單來指定依記錄檔類型或規則嚴重性顯示。

若要指定圖表顯示的日期範圍，請先選取行事曆下拉式清單。日期選擇器視窗隨即開啟。

![Date selector for findings graph]({{site.url}}{{site.baseurl}}/images/Security/find-date-pick.png){: width="55%" }

您可以使用 **Quick select** 設定來指定確切的時間範圍。
* 在第一個下拉式清單中選取 **Last** 或 **Next**，以設定早於或晚於目前設定的時間範圍。
* 在第二個下拉式清單中選取一個數字，以定義範圍的值。
* 在第三個下拉式清單中選取時間單位。可用選項包括秒、分鐘、小時、天、週、月和年。
選擇 **Apply** 將日期範圍套用至圖表。圖表上的資訊會隨之變更，如下圖所示。

![Quick select settings example]({{site.url}}{{site.baseurl}}/images/Security/quickset.png){: width="40%" }

您可以使用左右箭號，將時間範圍移至目前日期範圍之前或之後。使用這些箭號時，開始與結束日期會顯示在日期範圍欄位中。接著您可以選取其中一個，以設定絕對、相對或目前的日期與時間。對於絕對與相對變更，請選擇 **Update** 來套用變更。

![Altering date range]({{site.url}}{{site.baseurl}}/images/Security/date-pick.png){: width="55%" }

或者，您也可以在 **Commonly used** 區段（請參閱前述行事曆下拉式清單的圖片）中選取一個選項，方便地設定時間範圍。選項包括 **Today**、**Yesterday**、**this week** 及 **week to date** 等日期範圍。

選取其中一個常用時間範圍後，您可以在日期範圍欄位中選擇 **Show dates** 來填入日期範圍。接著，您可以選取開始日期或結束日期，以指定絕對、相對或目前的日期與時間設定。對於絕對與相對變更，請選擇 **Update** 來套用變更。

另一種方式是，您可以從 **Recently used date ranges** 區段中選取一個選項，以返回先前的設定。

---
## 尋找結果清單

**Findings** 清單會依尋找結果的時間、尋找結果 ID、產生該尋找結果的規則名稱、擷取該尋找結果的偵測器以及其他詳細資料，顯示所有尋找結果，如下圖所示。

![A list of all findings]({{site.url}}{{site.baseurl}}/images/Security/finding-list.png){: width="85%" }

使用 **Rule severity** 下拉式清單，依嚴重性篩選尋找結果清單。使用 **log type** 下拉式清單，依記錄檔類型篩選清單。

**Actions** 欄為每個尋找結果提供兩個選項：
* 斜向箭號可用來開啟 [**Finding details**](#finding-details) 窗格，其中依建立偵測器時定義的參數描述該尋找結果，並包含產生該尋找結果的文件。
* 鈴鐺圖示可讓您開啟 **Create detector alert trigger** 窗格，您可以在其中快速為特定尋找結果設定警示，並視需要修改規則及其條件。
有關設定警示的資訊，請參閱偵測器建立文件中的 [Step 2. Set up alerts]({{site.url}}{{site.baseurl}}/security-analytics/sec-analytics-config/detectors-config/#step-2-set-up-alerts)。

### 尋找結果詳細資料

清單中的每個尋找結果也包含一個 **Finding ID**。除了使用 **Actions** 中的斜向箭號外，您也可以選取該 ID 來開啟 **Finding details** 窗格。**Finding details** 的範例如下圖所示。

![Finding details pane]({{site.url}}{{site.baseurl}}/images/Security/findings1.png){: width="60%" }

#### 檢視周邊文件

**Finding details** 窗格包含該尋找結果的特定資訊，包括產生該尋找結果的文件。若要調查導致該尋找結果或緊接其後發生的一系列事件，您可以選取 **View surrounding documents**，在 **Discover** 面板中開啟該文件，並檢視其之前或之後的其他文件。

1. 在 **Findings** 清單中選取 **Finding ID**，以開啟 **Finding details**。
1. 在 **Documents** 區段中，選取 **View surrounding documents**。如果該文件已有索引模式，**Discover** 面板會開啟並顯示該文件。如果索引模式不存在，則會開啟 **Create index pattern to view documents** 視窗，提示您建立索引模式，如下圖所示。

    ![popup window prompting users to create an index pattern]({{site.url}}{{site.baseurl}}/images/Security/findings2.png){: width="60%" }

1. 在 **Create index pattern to view documents** 視窗中，索引模式名稱會自動填入。請輸入用於判斷記錄事件時間的記錄索引中適當的時間欄位。選擇 **Create index pattern**。**Create index pattern to view documents** 確認視窗隨即開啟。
1. 在確認視窗中選取 **View surrounding documents**。**Discover** 面板隨即開啟，如下圖所示。

    ![Discover panel with surrounding documents]({{site.url}}{{site.baseurl}}/images/Security/findings4.png){: width="85%" }
    
**Discover** 面板會以醒目提示的背景顯示產生該尋找結果的文件。事件之前或之後的其他文件也會一併顯示。

有關在 OpenSearch Dashboards 中使用 **Discover** 的詳細資訊，請參閱 [Exploring data]({{site.url}}{{site.baseurl}}/dashboards/discover/index-discover/)。

#### 檢視相互關聯的尋找結果

若要查看該尋找結果與其他尋找結果之間的相互關聯，請選取 **Correlations** 索引標籤。相互關聯是尋找結果之間的關係，表達涉及多種記錄檔類型的特定威脅情境。**Correlated findings** 表格中的資訊顯示相互關聯的尋找結果產生的時間、尋找結果的 ID、用來產生該尋找結果的記錄檔類型、其威脅嚴重性，以及關聯性分數——衡量其與參考尋找結果接近程度的指標——如下圖所示。

![A table of correlated findings with respect to the reference finding]({{site.url}}{{site.baseurl}}/images/Security/corr-details-findings.png){: width="60%" }

您可以選取 **View correlations graph**，以視覺化方式呈現尋找結果之間的相互關聯。有關使用關聯圖的更多資訊，請參閱 [Working with the correlation graph]({{site.url}}{{site.baseurl}}/security-analytics/usage/correlation-graph/)。
