---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "使用偵測規則"
parent: Using Security Analytics
nav_order: 40
---

# 使用偵測規則

**Detection rules** 視窗會列出所有用於建立偵測的安全性規則，並提供篩選清單及檢視各規則詳細資訊的選項。其他選項可讓您匯入規則，或先複製 Sigma 規則再加以修改，藉此建立新規則。本節說明如何瀏覽 **Rules** 頁面，並描述您可執行的動作。

![Rules 頁面]({{site.url}}{{site.baseurl}}/images/Security/Rules.png){: width="90%" }

---
## 檢視及篩選規則

開啟 **Detection rules** 頁面時，表格中會列出所有規則。若要搜尋特定規則，請在搜尋列中輸入完整或部分名稱，然後按下鍵盤上的 **Return/Enter**。清單會隨即篩選並顯示符合的結果。

或者，您可以使用 **Rule type**、**Rule severity** 和 **Source** 下拉式清單深入檢視警示，並篩選出想要的結果。您可以從每個清單中選取多個選項，並組合使用這三個清單來縮小結果範圍。

![用於篩選結果的規則選單]({{site.url}}{{site.baseurl}}/images/Security/rule-menu.png){: width="40%" }

### 規則詳細資訊

若要查看規則詳細資訊，請在清單的 Rule name 欄中選取該規則。規則詳細資訊窗格隨即開啟。

![規則詳細資訊窗格]({{site.url}}{{site.baseurl}}/images/Security/Rule_details.png){: width="50%" }

在 Visual 檢視中，規則詳細資訊會依欄位排列，且連結皆可使用。選取 **YAML** 即可以 YAML 檔案格式顯示規則。

![YAML 檔案檢視中的規則詳細資訊窗格]({{site.url}}{{site.baseurl}}/images/Security/rule_detail_yaml.png){: width="50%" }

* 規則詳細資訊會依照 Sigma 規則規格格式化為 YAML 檔案。
* 若要複製規則，請選取規則右上角的複製圖示。若要快速建立新的自訂規則，您可以將規則貼到 YAML 編輯器中，並在儲存前進行任何修改。如需詳細資訊，請參閱[自訂規則](#customizing-rules)。

---
## 建立偵測規則

在 **Detection rules** 頁面上有多種建立規則的方式，包括手動建立自訂規則、匯入規則，以及複製現有規則再加以自訂。以下各節將詳細說明這些方式。  

### 自訂規則

第一種建立規則的方式，是使用 Visual Editor 或 YAML Editor 手動填寫完成規則所需的欄位，藉此建立自訂規則。若要執行此操作，請選取畫面右上角的 **Create detection rule**。**Create detection rule** 視窗隨即開啟。

如果您選擇手動建立規則，可以參閱 Sigma 的[規則建立指南](https://github.com/SigmaHQ/sigma/wiki/Rule-Creation-Guide)，進一步了解各欄位的詳細資訊。
{: .tip }

<!-- vale off -->
#### Visual Editor
<!-- vale on -->

**Create detection rule** 視窗開啟時，預設會顯示 **Visual Editor**。**Visual Editor** 中的必要欄位對應於以 Sigma 規則格式撰寫的 YAML 檔案中的基本欄位。若對應關係不夠明顯，以下步驟的說明中會特別提及。
  
1. 在 **Rule overview** 區段中，輸入規則名稱、說明（選用）及規則作者。**Rule name** 對應於以 YAML 檔案格式撰寫的 Sigma 規則中的 [title](https://github.com/SigmaHQ/sigma/wiki/Rule-Creation-Guide#title)。下圖提供已填入欄位的範例。
  
   ![Create detection rule 視窗中的 Rule overview 欄位，包括規則名稱、說明及作者欄位。]({{site.url}}{{site.baseurl}}/images/Security/overview-rule.png){: width="50%" }
  
1. 在 **Details** 區段中，輸入資料來源的記錄檔類型、規則層級及規則狀態。**Log type** 對應於 [`logsource`](https://github.com/SigmaHQ/sigma/wiki/Rule-Creation-Guide#log-source) 欄位（具體而言是 `logsource: product` 欄位），而規則層級和規則狀態則分別對應於 [`level`](https://github.com/SigmaHQ/sigma/wiki/Rule-Creation-Guide#level) 和 [`status`](https://github.com/SigmaHQ/sigma/wiki/Rule-Creation-Guide#status)。Sigma 規則中的層級包括 *informational*、*low*、*medium*、*high* 和 *critical*。下圖提供範例。
  
   ![Create detection rule 視窗中的 Details 欄位，包括記錄檔類型、規則層級及規則狀態欄位。]({{site.url}}{{site.baseurl}}/images/Security/details-rule.png){: width="40%" }
  
1. 在 **Detection** 區段中，指定鍵值組來表示記錄檔來源中的欄位及其值，這些欄位與值即為偵測的目標。這些鍵值組定義了偵測內容。您可以將鍵值表示為單一值，或是包含多個值的清單。 
   
   若要定義簡單的鍵值組，請先將游標置於 **Selection_1** 標籤上，並將其取代為描述該鍵值組的選取項目名稱。接著，輸入記錄檔來源中想要使用的欄位作為 **Key**，然後使用 **Modifier** 下拉式清單定義值的處理方式。可用的修飾詞如下：
     * `contains` – 在值的兩側加上萬用字元，使值在欄位中的任何位置都能符合。
     * `all` – 若為清單，邏輯會從以 OR 邏輯分隔各值改為 AND，並尋找與所有值皆符合的結果。
     * `endswith` – 表示當值出現在欄位結尾時即視為符合。
     * `startswith` – 表示當值出現在欄位開頭時即視為符合。
   
   選取修飾詞後，請選取 **Value** 選項按鈕，然後在其後的文字欄位中輸入該鍵的值。
   
   您可以選取 **Add map** 來新增欄位，以對應第二個鍵值組。請依照此步驟先前的指引對應該鍵值組。下圖顯示兩個鍵值組的定義在 **Create detection rule** 視窗中的呈現方式。
   
   ![Detection 欄位的範例。]({{site.url}}{{site.baseurl}}/images/Security/detection1.png){: width="50%" }
   
   若要比較此定義與在 YAML 檔案中的設定方式，請參閱以下範例：

   ```yaml
   detection:
      selection:
       selection_schtasks:
         Image|endswith: \schtasks.exe
         CommandLine|contains: '/Create '
   ```
   
   若要新增第二個選取項目，請使用第一個選取項目後方的 **Add selection** 列，開啟另一個鍵值組對應。此選取項目的值會以清單形式提供。如同第一個選取項目的說明，將 **Selection_2** 標籤取代為選取項目名稱，輸入記錄檔中的欄位名稱作為鍵，並從 **Modifier** 下拉式清單中選取修飾詞。

   接著，若要使用清單而非單一值來定義鍵值組，請選取 **List** 選項按鈕。**Upload file** 按鈕隨即出現，且文字方塊會展開以容納清單。

   您可以上傳 .csv 或 .txt 格式的現有值清單。選取 **Upload file**，並依照提示將檔案內容上傳至文字欄位。或者，您也可以直接在文字欄位中手動撰寫清單。下圖顯示包含值清單的鍵值組對應的呈現方式。

   ![Detection 欄位的範例。]({{site.url}}{{site.baseurl}}/images/Security/detection2.png){: width="50%" }
   
   若要比較包含前述兩個選取項目的定義與在 YAML 檔案中的設定方式，請參閱以下範例：

   ```yml
   detection:
     selection:
       selection_schtasks:
         Image|endswith: \schtasks.exe
         CommandLine|contains: '/Create '
       selection_rare:
         CommandLine|contains:
         - ' bypass '
         - .DownloadString
         - .DownloadFile
         - FromBase64String
         - ' -w hidden '
         - ' IEX'
         - ' -enc '
         - ' -decode '
         - '/c start /min '
         - ' curl '
   ```

1. 在 **Condition** 區段中，指定偵測定義中所含選取項目的條件。這些條件決定偵測規則如何處理已定義的選取項目。至少需要一個選取項目。以前述範例而言，這表示必須在 **Conditions** 區段中至少新增 `selection_schtasks` 和 `selection_rare` 這兩個選取項目的其中一個。 

   選取 **Select** 旁的 `+` 符號以新增第一個選取項目。再次選取 `+` 符號，即可從偵測定義中新增更多選取項目。當有兩個選取項目作為條件時，兩者之間會出現布林運算子 AND，表示兩者都會用於偵測規則查詢。您可以選取運算子的標籤以開啟運算子下拉式清單，並從 `AND`、`OR` 和 `NOT` 選項中選擇。下圖顯示此選項的呈現方式。

   ![指定偵測定義中選取項目的條件。]({{site.url}}{{site.baseurl}}/images/Security/condition1.png){: width="50%" }

1. 指定偵測規則的選用欄位。
  
   * 在 **Tags** 區段中新增標籤，將偵測規則與網路安全知識庫（例如 [MITRE ATT&CK](https://attack.mitre.org/)）所記錄的任何攻擊技術建立關聯。選取 **Add tag** 可新增多個標籤。
   * 在 **References** 區段中，您可以新增規則參考資料的 URL。選取 **Add URL** 可新增多個 URL。
   * **False positive cases** 區段提供空間，讓您列出可能觸發此規則非預期警示的誤判條件說明。選取 **Add false positive** 可新增多個說明。
  
 1. 規則完成並符合您的需求後，請選取視窗右下角的 **Create detection rule** 以儲存規則。系統會自動為新規則指派規則 ID，且該規則會出現在偵測規則清單中。
  
<!-- vale off -->  
#### YAML Editor
<!-- vale on -->

**Create detection rule** 視窗也包含 **YAML Editor**，讓您可以直接以 YAML 檔案格式建立新規則。選取 **YAML Editor**，然後輸入預先填入的欄位類型資訊。規則的 `id` 會在儲存規則時提供並指派。以下範例顯示典型規則的基本元素：

```yml
title: RDP Sensitive Settings Changed
logsource:
  product: windows
description: 'Detects changes to RDP terminal service sensitive settings'
detection:
  selection:
    EventType: SetValue
    TargetObject|contains:
      - \services\TermService\Parameters\ServiceDll
      - \Control\Terminal Server\fSingleSessionPerUser
      - \Control\Terminal Server\fDenyTSConnections
      - \Policies\Microsoft\Windows NT\Terminal Services\Shadow
      - \Control\Terminal Server\WinStations\RDP-Tcp\InitialProgram
  condition: selection
level: high
tags:
  - attack.defense_evasion
  - attack.t1112
references:
  - https://blog.menasec.net/2019/02/threat-hunting-rdp-hijacking-via.html
  - https://knowledge.insourcess.com/Supporting_Technologies/Wonderware/Tech_Notes/TN_WW213_How_to_shadow_an_established_RDP_Session_on_Windows_10_Pro
  - https://twitter.com/SagieSec/status/1469001618863624194?t=HRf0eA0W1YYzkTSHb-Ky1A&s=03
  - http://etutorials.org/Microsoft+Products/microsoft+windows+server+2003+terminal+services/Chapter+6+Registry/Registry+Keys+for+Terminal+Services/
falsepositives:
  - Unknown
author:
  - Samir Bousseaden 
  - David ANDRE
status: experimental
```
{% include copy.html %}

為了協助您使用 **YAML Editor** 建立規則，您可以參考 Sigma 的[規則建立指南](https://github.com/SigmaHQ/sigma/wiki/Rule-Creation-Guide)，並使用各欄位的說明來進一步了解如何定義規則。

### 匯入規則

Security Analytics 也支援匯入 YAML 格式的 Sigma 規則。在 **Detection rules** 視窗中，依照下列步驟匯入規則。

1. 首先，選取頁面右上角的 **Import detection rule**。**Import rule** 頁面隨即開啟。
1. 將 YAML 格式的 Sigma 規則拖曳至視窗，或選取連結並開啟檔案來瀏覽檔案。**Import a rule** 視窗隨即開啟，規則定義欄位會自動填入 Visual Editor 與 YAML Editor 中。
1. 驗證或修改欄位中的資訊。
1. 確認規則資訊正確無誤後，選取視窗右下角的 **Create detection rule**。系統會建立新規則，並顯示在偵測規則清單中。

### 自訂規則

建立新偵測規則的另一個選項是複製 Sigma 規則，然後加以修改以建立自訂規則。首先在 **Rule name** 清單中搜尋或篩選規則，以找出您要複製的規則。下圖顯示以關鍵字篩選後的清單。

![在 Rules name 清單中選取規則]({{site.url}}{{site.baseurl}}/images/Security/rules-dup1.png){: width="75%" }

1. 首先，在 **Rule name** 欄中選取該規則。規則詳細資料隨即顯示。

    ![開啟規則詳細資料窗格]({{site.url}}{{site.baseurl}}/images/Security/rule-dup2.png){: width="50%" }

1. 選取窗格右上角的 **Duplicate** 按鈕。Duplicate rule 視窗會以 Visual Editor 檢視開啟，且所有欄位都會自動填入規則的詳細資料。YAML Editor 檢視中也會填入詳細資料。

    ![選取 Duplicate 按鈕會開啟 Duplicate rule 視窗]({{site.url}}{{site.baseurl}}/images/Security/dupe-rule.png){: width="50%" }

1. 在 Visual Editor 檢視或 YAML Editor 檢視中，修改任何欄位以自訂規則。
1. 對規則進行任何修改後，選取視窗右下角的 **Create detection rule**。系統會建立新的自訂規則。它會顯示在 **Detection rules** 視窗主頁面的規則清單中。

    ![自訂規則現在顯示在規則清單中。]({{site.url}}{{site.baseurl}}/images/Security/custom-rule.png){: width="70%" }

您無法修改 Sigma 規則本身。原始 Sigma 規則一律會保留在系統中。其複本在修改後會成為新增至規則清單的自訂規則。
{: .note }

