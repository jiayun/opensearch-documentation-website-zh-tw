---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "使用記錄檔類型"
parent: Setting up Security Analytics
nav_order: 14
redirect_from: 
   - /security-analytics/sec-analytics-config/custom-log-type/
---

# 使用記錄檔類型

記錄檔類型代表 Security Analytics 中用於威脅偵測的不同資料來源。記錄檔類型可用於在從來源建立偵測器時，對[偵測規則]({{site.url}}{{site.baseurl}}/security-analytics/sec-analytics-config/detectors-config/)進行分類或預先填入。

Security Analytics 支援下列記錄檔類型：

- [標準記錄檔類型](#standard-log-types)：Security Analytics 會根據從每個來源編製索引的資料，自動產生資料來源清單，以及其欄位對應與規則。
- [自訂記錄檔類型](#creating-custom-log-types)：當您的資料無法歸類為其中一種[標準記錄檔類型]({{site.url}}{{site.baseurl}}/security-analytics/sec-analytics-config/log-types/)時，您可以建立使用者自訂的記錄檔類型。為了強化威脅偵測，Security Analytics 支援整合自訂記錄檔類型。

若要前往 **Log types** 頁面，請在 **Security Analytics** 導覽選單中選取 **Detectors** 底下的 **Log types**。

## 頁面操作

**Log types** 主要 UI 的功能與操作如下圖所示。這些功能將在圖片後面的清單中說明。

![記錄檔類型首頁]({{site.url}}{{site.baseurl}}/images/Security/c-log-type.png){: width="85%" }


1. 搜尋 **Standard** 與 **Custom** 記錄檔類型。
   - 如需 **Standard** 記錄檔類型的清單，請參閱[支援的記錄檔類型]({{site.url}}{{site.baseurl}}/security-analytics/sec-analytics-config/log-types/)。
2. 建立[自訂記錄檔類型](#creating-custom-log-types)。
3. 選取記錄檔類型的 **Name** 以開啟詳細資料頁面。預設會顯示 **Details** 索引標籤。此索引標籤包含記錄檔類型的 ID。您也可以選取 **Detection rules** 索引標籤，以顯示與該記錄檔類型相關聯的所有偵測規則。
4. 選取 **Category** 或 **Source** 下拉式選單，以依記錄檔類型類別或來源排序。
5. 在 **Actions** 欄中，選取 {::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/alerting/trash-can-icon.png" class="inline-icon" alt="trash can icon"/>{:/} 圖示以刪除自訂記錄檔類型 (您無法刪除 OpenSearch 定義的標準記錄檔類型)。然後依照提示確認並刪除。

## 標準記錄檔類型

所有標準記錄檔類型依下列類別分組：

- **Access Management** 包含 [AD/LDAP]({{site.url}}{{site.baseurl}}/security-analytics/log-types-reference/ad-ldap/)、[Apache Access]({{site.url}}{{site.baseurl}}/security-analytics/log-types-reference/apache-access/) 與 [Okta]({{site.url}}{{site.baseurl}}/security-analytics/log-types-reference/okta/)。
- **Applications** 包含 [GitHub]({{site.url}}{{site.baseurl}}/security-analytics/log-types-reference/github/)、[Google Workspace]({{site.url}}{{site.baseurl}}/security-analytics/log-types-reference/gworkspace/) 與 [Microsoft 365]({{site.url}}{{site.baseurl}}/security-analytics/log-types-reference/m365/)。
- **Cloud Services** 包含 [Azure]({{site.url}}{{site.baseurl}}/security-analytics/log-types-reference/azure/)、[AWS CloudTrail]({{site.url}}{{site.baseurl}}/security-analytics/log-types-reference/cloudtrail/) 與 [Amazon S3]({{site.url}}{{site.baseurl}}/security-analytics/log-types-reference/s3/)。
- **Network Activity** 包含 [DNS]({{site.url}}{{site.baseurl}}/security-analytics/log-types-reference/dns/)、[Network]({{site.url}}{{site.baseurl}}/security-analytics/log-types-reference/network/)、[NetFlow]({{site.url}}{{site.baseurl}}/security-analytics/log-types-reference/netflow/) 與 [VPC Flow]({{site.url}}{{site.baseurl}}/security-analytics/log-types-reference/vpc/)。
- **Security** 包含 [WAF]({{site.url}}{{site.baseurl}}/security-analytics/log-types-reference/waf/)。
- **System Activity** 包含 [Linux]({{site.url}}{{site.baseurl}}/security-analytics/log-types-reference/linux/) 與 [Windows]({{site.url}}{{site.baseurl}}/security-analytics/log-types-reference/windows/)。
- **Other** 涵蓋不屬於特定類別的記錄檔類型。如需更多資訊，請參閱[其他記錄檔類型]({{site.url}}{{site.baseurl}}/security-analytics/log-types-reference/other/)。


## 建立自訂記錄檔類型

當連線到標準記錄檔類型不支援的資料來源時，請依照下列步驟建立自訂記錄檔類型：

1. 在 OpenSearch Dashboards 中，依序選取 **OpenSearch Plugins** > **Security Analytics**，然後選取 **Detectors** > **Log types**。
1. 選取 **Create log type**。
1. 輸入記錄檔類型的名稱，並可選擇性地輸入描述。
   
   記錄檔類型名稱支援字元 a--z (小寫)、0--9、連字號與底線。
   {: .note }
   
1. 選取一個類別。類別列於[支援的記錄檔類型]({{site.url}}{{site.baseurl}}/security-analytics/sec-analytics-config/log-types/)文件中。
1. 在畫面右下角選取 **Create log type**。畫面會返回 **Log types** 頁面，新的記錄檔類型會出現在清單中。請注意，新記錄檔類型的來源會顯示 **Custom**。

## 關於欄位對應

建立偵測器時指定的記錄檔類型，會決定哪些欄位可用於對應。例如，當選取 **Windows logs** 時，此參數與特定的偵測規則會決定可用於對應的偵測欄位名稱清單。同樣地，所選的資料來源會決定可用於對應的記錄來源欄位名稱清單。

Security Analytics 使用預先封裝的 Sigma 規則來建立偵測器。它可以自動將特定記錄檔類型的重要欄位對應到 Sigma 規則中的相關欄位。**Field Mappings** 區段會顯示已自動對應的欄位。在此區段中，您可以自訂、變更或新增欄位對應。當偵測器包含自訂規則時，您可以手動將偵測器規則欄位名稱對應到記錄來源欄位名稱。

由於系統可以自動對應欄位名稱，因此當文件中存在 `ecs` 欄位時，手動對應欄位是選用的。不過，偵測器規則需要某些對應才能運作。這些對應取決於偵測器規則。偵測器欄位與記錄來源欄位之間可對應的欄位越多，所產生發現結果的準確度就越高。



## 記錄檔類型 API

使用記錄檔類型 API，透過 REST API 執行自訂記錄檔類型操作。如需更多資訊，請參閱[記錄檔類型 API]({{site.url}}{{site.baseurl}}/security-analytics/api-tools/log-type-api/) 文件。





