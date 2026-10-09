---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "建立關聯規則"
parent: Setting up Security Analytics
nav_order: 17
---

# 建立關聯規則

關聯規則可讓您藉由比對不同記錄類型中出現的威脅事件特徵，定義基礎架構中涉及多個系統的威脅情境。一旦規則包含至少兩個不同的記錄來源，以及定義預定威脅情境所需的欄位與欄位值，關聯引擎即可查詢關聯規則中指定的索引，並找出各項發現之間的任何關聯。

---
## 設定規則

規則組態中至少要有兩個資料來源，這是在基礎架構中不同系統之間建立連結並找出關聯的基礎。因此，每個關聯規則至少需要兩個查詢。不過，您可以加入兩個以上的查詢，以更完善地定義威脅情境，並尋找多個系統之間的關聯。請依照下列步驟建立關聯規則：

1. 首先，在 OpenSearch Dashboards 主選單中選取 **Security Analytics**。然後在畫面左側的 Security Analytics 選單中選取 **Correlation rules**。畫面會顯示 **Correlation rules** 頁面，如下圖所示。
   
   ![The correlation rules page]({{site.url}}{{site.baseurl}}/images/Security/sec-analytics/create-corr-rule.png){: width="85%" }

1. 選取 **Create correlation rule**。**Create correlation rule** 視窗隨即開啟。
1. 在 **Correlation rule details** 欄位中，輸入規則的名稱，如下圖所示。
  
   ![The correlation rule name]({{site.url}}{{site.baseurl}}/images/Security/sec-analytics/corr-rule-config1.png){: width="50%" }

1. **Correlation queries** 欄位包含兩個下拉式清單。在 **Select index** 下拉式清單中，指定資料來源的索引或索引模式。在 **Log type** 下拉式清單中，指定與該索引相關聯的記錄類型，如下圖所示。
  
   ![The data source and log type for the query]({{site.url}}{{site.baseurl}}/images/Security/sec-analytics/corr-rule-config2.png){: width="45%" }
  
1. 在 **Field** 下拉式清單中，指定記錄欄位。在 **Field value** 文字方塊中，輸入該欄位的值，如下圖所示。
  
   ![The field and field value for the query]({{site.url}}{{site.baseurl}}/images/Security/sec-analytics/corr-rule-config3.png){: width="45%" }

1. 若要為查詢新增更多欄位，請選取 **Add field**。    
1. 設定好第一個查詢後，重複上述步驟以設定第二個查詢。您可以在視窗底部選取 **Add query**，為規則新增更多查詢，如下圖所示。
  
   ![A second query for the correlation rule]({{site.url}}{{site.baseurl}}/images/Security/sec-analytics/corr-rule-config4.png){: width="50%" }

1. 規則完成後，選取視窗右下角的 **Create correlation rule**。OpenSearch 會建立新規則，畫面會返回 **Correlation rules** 視窗，且新規則會出現在關聯規則表格中。若要編輯規則，請在 **Name** 欄中選取規則名稱。**Edit correlation rule** 視窗隨即開啟。

---
## 設定時間範圍

Cluster Settings API 可讓您在一段設定的時間範圍內關聯各項發現。舉例來說，如果您的時間範圍是三分鐘，系統只會在威脅情境中定義的各項發現彼此出現時間相隔三分鐘內時，才會嘗試加以關聯。根據預設，時間範圍為五分鐘。如需 Cluster Settings API 的詳細資訊，請參閱[叢集設定]({{site.url}}{{site.baseurl}}/api-reference/cluster-api/cluster-settings/)。

### 範例請求

下列 PUT 呼叫會將時間範圍設為兩分鐘：

```json
PUT /_cluster/settings
{
  "transient": {
    "plugins.security_analytics.correlation_time_window": "2m"
  }
}
```
{% include copy-curl.html %}

---
## 後續步驟

建立偵測器和關聯規則後，您可以使用關聯圖來觀察來自不同記錄來源之各項發現之間的關聯。如需使用關聯圖的詳細資訊，請參閱[使用關聯圖]({{site.url}}{{site.baseurl}}/security-analytics/usage/correlation-graph/)。

您也可以為關聯規則新增觸發條件，使其在關聯各項發現時產生警示並傳送通知。如需詳細資訊，請參閱[關聯規則觸發條件]({{site.url}}{{site.baseurl}}/security-analytics/api-tools/correlation-eng/#correlation-rule-triggers)。

