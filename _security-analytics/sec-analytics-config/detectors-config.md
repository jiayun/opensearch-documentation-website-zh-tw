---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "建立偵測器"
parent: Setting up Security Analytics
nav_order: 15
---

# 建立偵測器

Security Analytics 提供監控與回應各種安全威脅的選項與功能。偵測器是決定要尋找什麼以及如何回應這些威脅的核心元件。本節說明偵測器的建立與組態。

如需使用現有偵測規則的資訊，請參閱[建立偵測規則]({{site.url}}{{site.baseurl}}/security-analytics/usage/detectors/)。

---
## 步驟 1：定義偵測器

您可以為偵測器命名，然後選取資料來源與偵測器類型，以定義新的偵測器。定義偵測器之後，您可以設定欄位對應、建立偵測器排程，以及設定警示。

若要定義偵測器：

1. 在 **Security Analytics** 首頁或 **Detectors** 頁面上，選擇 **Create detector**。
1. 為偵測器命名，並可選擇性地提供描述。
1. 在 **Data source** 區段中，為記錄資料選取一或多個來源。選取多個資料來源時，它們必須都包含相同記錄類型的記錄檔 (例如全部是 Amazon S3 記錄檔或全部是 Windows 記錄檔)。建議為不同的記錄類型建立個別的偵測器。除了索引之外，Security Analytics 還支援下列資料來源類型：

    - [別名]({{site.url}}{{site.baseurl}}/im-plugin/index-alias/)：將別名組態為資料來源時，該別名必須附加至 **Write** 索引別名。使用別名時，請確保您的文件是透過該別名匯入，而**不是**透過建立該別名的索引匯入。
    - [資料串流]({{site.url}}{{site.baseurl}}/im-plugin/data-streams/)：一組儲存在多個索引中的時間序列資料，但透過單一命名資源呼叫。

    不建議使用星號 (*) 來表示資料來源的萬用字元模式。
    {: .note} 
   
1. 在 **Detection** 區段中，為資料來源選取記錄類型。如需支援的記錄類型清單，請參閱[支援的記錄類型]({{site.url}}{{site.baseurl}}/security-analytics/sec-analytics-config/log-types/)。若要建立自己的記錄類型，請參閱[建立自訂記錄類型]({{site.url}}{{site.baseurl}}/security-analytics/sec-analytics-config/custom-log-type/)。
    
    當您選取 `network`、`cloudtrail` 或 `s3` 作為記錄類型時，系統會自動建立偵測器儀表板。該儀表板提供偵測器的視覺化，並可為記錄來源資料提供安全性相關的洞察。如需視覺化的詳細資訊，請參閱[建立資料視覺化]({{site.url}}{{site.baseurl}}/dashboards/visualize/viz-index/)。
    
     
1. 展開 **Detection rules** 以顯示所選記錄類型的可用偵測規則清單。一開始，所有規則預設為已選取。下列範例顯示與 **windows** 記錄類型相關聯的規則。

    ![選取威脅偵測器的記錄類型以自動填入規則]({{site.url}}{{site.baseurl}}/images/Security/detector-rules.png){: width="100%" }

    檢視規則時，您可以執行下列動作：
    
    * 使用 **Rule name** 左側的切換開關來選取或取消選取規則。
    * 使用 **Rule severity** 與 **Source** 下拉式清單來篩選您要選取的規則。
    * 使用 **Search** 搜尋列搜尋特定規則。
    
    若要快速選取一或多個已知規則並略過其他規則，請先關閉 **Rule name** 切換開關以取消選取所有規則，然後搜尋目標規則名稱，並逐一開啟其切換開關來選取。
    {: .tip } 

1. 檢閱欄位對應。欄位對應可讓系統準確地將事件資料從記錄檔傳遞至偵測器，然後使用該資料觸發警示。如需欄位對應的詳細資訊，請參閱[欄位對應注意事項](#a-note-on-field-names)一節。

1. 選擇是否啟用[威脅情報]({{site.url}}{{site.baseurl}}/security-analytics/usage/detectors#threat-intelligence-feeds)來源。威脅情報來源僅適用於 **standard** 記錄類型。
    
1. 在 **Detector schedule** 區段中，建立偵測器執行頻率的排程。指定時間單位與對應的數字來設定間隔。下圖顯示偵測器每 3 分鐘執行一次。
    
    ![設定偵測器排程以決定執行頻率]({{site.url}}{{site.baseurl}}/images/Security/detector-schedule.png){: width="40%" }
    
1. 選取 **Next**。**Set up alerts** 頁面隨即出現，並顯示警示觸發條件的設定。


---
## 步驟 2：設定警示

建立偵測器的第二個步驟是設定警示。警示的組態會建立觸發條件，當符合一組偵測規則條件時，即傳送可能安全事件的通知。您可以以任意組合選取規則名稱、規則嚴重性與標籤來定義觸發條件。定義觸發條件後，警示設定可讓您選擇接收通知的頻道，並提供自訂通知訊息的選項。

偵測器開始產生發現結果之前，至少需要一個警示條件。
{: .note }

您也可以從 **Findings** 視窗組態警示。如需如何從 **Findings** 視窗設定警示，請參閱[發現結果清單]({{site.url}}{{site.baseurl}}/security-analytics/usage/findings/#the-findings-list)。新增其他警示的最後一個選項是編輯偵測器並前往 **Alert triggers** 索引標籤，您可以在該處編輯現有警示以及新增警示。如需詳細資訊，請參閱[編輯偵測器]({{site.url}}{{site.baseurl}}/security-analytics/usage/detectors/#editing-a-detector)。

若要為偵測器設定警示，請繼續執行下列步驟：

1. 在 **Trigger name** 方塊中，選擇性地輸入觸發條件的名稱，或編輯預設名稱。
1. 若要定義警示的規則符合條件，請選取安全性規則、嚴重性層級與標籤。
    
    ![定義警示]({{site.url}}{{site.baseurl}}/images/Security/alert_rules.png){: width="70%" }

    * 選取一或多個將觸發警示的規則。將游標放在 **Rule names** 方塊中並輸入名稱以進行搜尋。若要移除規則名稱，請選取名稱旁的 **X**。若要移除所有規則名稱，請選取下拉式清單向下箭頭旁的 **X**。

    ![刪除所有已選取的規則]({{site.url}}{{site.baseurl}}/images/Security/rule_name_delete.png){: width="45%" }

    * 選取一或多個規則嚴重性層級作為警示的條件。
    * 從標籤清單中選取要納入作為警示條件的標籤。

1. 若要定義警示的通知，請指派警示嚴重性、選取通知頻道，並自訂為警示產生的訊息。

    ![警示的通知設定]({{site.url}}{{site.baseurl}}/images/Security/alert_notify.png){: width="45%" }

    * 為警示指派嚴重性層級，讓收件者了解其急迫程度。
    * 從 **Select channel to notify** 下拉式清單中選取通知頻道。範例包括 Slack、Chime 或電子郵件。若要建立新頻道，請選取欄位右側的 **Manage channels** 連結。Notifications 的 **Channels** 頁面會在新索引標籤中開啟，您可以在該處編輯與建立新頻道。如需通知的詳細資訊，請參閱 [Notifications]({{site.url}}{{site.baseurl}}/observing-your-data/notifications/index/) 文件。
    * 展開 **Show notify message** 以顯示訊息偏好設定。訊息主旨與訊息內文會填入目前警示組態的詳細資訊。您可以編輯這些文字欄位來自訂訊息。在訊息內文文字方塊下方，您可以選取 **Generate message** 以在訊息中填入更多詳細資訊，例如規則名稱、規則嚴重性層級與規則標籤。
    * 選取 **Add another alert trigger** 以組態其他警示。

1. 在上述欄位中組態完條件後，選取畫面右下角的 **Create detector**。

## 整合式警示外掛程式工作流程

根據預設，當您建立威脅偵測器時，系統會自動建立複合監視器，並為警示外掛程式觸發工作流程。偵測器的規則會轉換為警示外掛程式監視器的搜尋查詢，而監視器會依照偵測器組態衍生的排程執行其查詢。

您可以透過 `plugins.security_analytics.enable_workflow_usage` 設定啟用或停用工作流程功能，藉此變更自動產生之複合監視器的行為。此設定是使用 [Cluster settings API]({{site.url}}{{site.baseurl}}/api-reference/cluster-api/cluster-settings/) 定義。

如需複合監視器及其工作流程的詳細資訊，請參閱[複合監視器]({{site.url}}{{site.baseurl}}/observing-your-data/alerting/composite-monitors/)。

---


## 自動對應的欄位

當您選取資料來源和記錄類型後，系統會嘗試自動對應記錄與規則欄位之間的欄位。切換至 **Mapped fields** 索引標籤，即可顯示這些對應的清單。當欄位名稱彼此相似時，系統可以成功配對兩者，如下圖所示。

![自動對應的欄位對應範例]({{site.url}}{{site.baseurl}}/images/Security/automatic-mappings.png){: width="85%" }

雖然這些自動配對通常很可靠，但仍建議您檢閱 **Mapped fields** 表格中的對應，並確認它們正確且符合預期。如果您發現某個對應似乎不準確，可以使用下拉式清單搜尋並選取正確的欄位名稱。如需配對欄位名稱的詳細資訊，請參閱下一節。

如需欄位對應的詳細資訊，請參閱[使用記錄類型]({{site.url}}{{site.baseurl}}/security-analytics/sec-analytics-config/log-types)文件中的[關於欄位對應]({{site.url}}{{site.baseurl}}/security-analytics/sec-analytics-config/log-types#about-field-mappings)一節。

## 可用欄位

未自動對應的欄位名稱會顯示在 **Available fields** 表格中。在此表格中，您可以手動將偵測規則欄位對應至資料來源欄位，如下圖所示。

![可用對應的欄位對應範例]({{site.url}}{{site.baseurl}}/images/Security/pending-mappings.png){: width="85%" }

對應欄位時，請考量下列事項：
* **Detection rule field** 欄會列出以所選記錄類型相關的所有預先封裝規則為基礎的欄位名稱。
* **Data source field** 欄包含每個偵測器欄位的下拉式清單。每個下拉式清單都包含從記錄索引擷取的欄位名稱。
* 若要將偵測器欄位名稱對應至記錄來源欄位名稱，請使用下拉式箭頭開啟記錄來源欄位清單，然後從清單中選取記錄欄位名稱。若要在記錄欄位清單中搜尋名稱，請在 **Select a data source field** 方塊中輸入文字。
  
* 一旦選取記錄來源欄位名稱並對應至偵測器欄位名稱後，右側 **Status** 欄中的圖示就會從警示圖示變更為核取記號。
* 盡可能在欄位名稱之間建立越多配對越好，以完成偵測器與記錄來源欄位的準確對應。

### 欄位名稱的注意事項

如果您選擇執行手動欄位對應，您應該熟悉記錄索引中的欄位名稱，並了解這些欄位中包含的資料。如果您了解索引中的記錄來源欄位，對應通常會是簡單直接的程序。

Security Analytics 運用預先封裝的 Sigma 規則來偵測安全性事件。因此，欄位名稱是衍生自 Sigma 規則欄位標準。為了讓它們更容易辨識，已根據下列規格建立 Sigma 規則欄位的別名：

- 針對所有記錄類型，使用開放原始碼的 Elastic Common Schema (ECS)
- 針對 AWS CloudTrail 和 DNS 記錄類型，使用 [Open Cybersecurity Schema Framework](https://github.com/ocsf/ocsf-schema) (OCSF)

別名規則的欄位名稱會用於下列步驟，並列在對應表格中的 **Detector field name** 欄內。

將 Sigma 規則的欄位名稱關聯至所有支援記錄類型之 ECS 規則欄位名稱的預先定義對應，可於下列資源中取得：

- [支援的記錄類型]({{site.url}}{{site.baseurl}}/security-analytics/sec-analytics-config/log-types/)參考文件
- GitHub Security Analytics 儲存庫。若要尋找欄位對應：
   1. 瀏覽至 [`OSMappings`](https://github.com/opensearch-project/security-analytics/tree/main/src/main/resources/OSMapping) 資料夾。
   2. 選取特定記錄類型的檔案。例如，針對 `windows` 記錄類型，若要檢視從 Sigma 規則關聯至 ECS 規則的欄位名稱，請選取 [`windows_logtype.json`](https://github.com/opensearch-project/security-analytics/blob/main/src/main/resources/OSMapping/windows_logtype.json) 檔案。`raw_field` 值代表對應中 Sigma 規則的欄位名稱。

## Amazon Security Lake 記錄

[Amazon Security Lake](https://docs.aws.amazon.com/security-lake/latest/userguide/what-is-security-lake.html) 會將安全性記錄與事件資料轉換為 [OCSF](https://docs.aws.amazon.com/security-lake/latest/userguide/open-cybersecurity-schema-framework.html) 格式，以將合併的資料標準化並簡化管理。OpenSearch 支援以 OCSF 格式匯入來自 Amazon Security Lake 的記錄資料。Security Analytics 可以自動將欄位從 OCSF 對應至 ECS (預設欄位對應結構描述)。

可作為偵測器建立之記錄來源的 Amazon Security Lake 記錄類型包括 AWS CloudTrail、Amazon Route 53 和 VPC Flow Logs。由於 Amazon Route 53 記錄會擷取 DNS 活動，因此[定義偵測器](#step-1-define-a-detector)時，記錄類型必須指定為 **dns**。由於 AWS CloudTrail 記錄可以原始格式和 OCSF 擷取，您應該以獨特且可辨識的方式命名索引。在與 Security Analytics 相關的 API 中指定索引名稱時，這會很有幫助。

支援的記錄類型可於下列資源中取得：

- 針對所有記錄類型，請參閱開放原始碼 ECS 規格。
- 針對 AWS CloudTrail、DNS 記錄類型和 VPC Flow Logs，請參閱 [OCSF](https://github.com/ocsf/ocsf-schema)。


別名規則的欄位名稱會用於下列步驟，並列在對應表格中的 **Detector field name** 欄內。

將 Sigma 規則的欄位名稱關聯至所有支援記錄類型之 ECS 規則欄位名稱的預先定義對應，可於下列資源中取得：

- [支援的記錄類型]({{site.url}}{{site.baseurl}}/security-analytics/sec-analytics-config/log-types/)參考文件。

- [GitHub Security Analytics](https://github.com/opensearch-project/security-analytics) 儲存庫。若要尋找欄位對應：
   1. 瀏覽至 [`OSMappings`](https://github.com/opensearch-project/security-analytics/tree/main/src/main/resources/OSMapping) 資料夾。
   2. 選取特定記錄類型的檔案。例如，針對 `windows` 記錄類型，若要檢視從 Sigma 規則關聯至 ECS 規則的欄位名稱，請選取 [`windows_logtype.json`](https://github.com/opensearch-project/security-analytics/blob/main/src/main/resources/OSMapping/windows_logtype.json) 檔案。`raw_field` 值代表對應中 Sigma 規則的欄位名稱。


## 接下來

如果您已準備好檢視新偵測器產生的發現項目，請參閱[使用發現項目]({{site.url}}{{site.baseurl}}/security-analytics/usage/findings/)一節。如果您想在處理發現項目之前匯入規則或設定自訂規則，請參閱[使用偵測規則]({{site.url}}{{site.baseurl}}/security-analytics/usage/rules/)一節。

若要設定 Security Analytics 以找出系統中不同記錄檔所發生事件之間的關聯，請參閱[使用關聯規則]({{site.url}}{{site.baseurl}}/security-analytics/usage/rules/)。
