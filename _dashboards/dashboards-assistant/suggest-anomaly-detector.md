---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "異常偵測器建議"
parent: OpenSearch Assistant for OpenSearch Dashboards
nav_order: 20
has_children: false
---

# 異常偵測器建議

這是一項實驗性功能，不建議在正式環境中使用。若要了解此功能的最新進度或提供意見回饋，請加入 [OpenSearch 論壇](https://forum.opensearch.org/)上的討論。    
{: .warning}

OpenSearch Dashboards Assistant 可以使用大型語言模型 (LLM) 建議建立異常偵測器。LLM 會分析您 OpenSearch 索引中的資料模式，並為異常偵測器建議組態設定，讓您更容易識別資料中的異常活動或趨勢。

## 組態

若要設定異常偵測器建議，請使用下列步驟。

### 先決條件

使用異常偵測器建議之前，請依下列方式在 OpenSearch Dashboards 中啟用查詢增強功能：

1. 在頂端選單列中，前往 **Management > Dashboards Management**。 
1. 在左側導覽窗格中，選取 **Advanced settings**。
1. 在設定頁面上，將 **Enable query enhancements** 切換為 **On**。

### 步驟 1：啟用異常偵測器建議

若要啟用異常偵測器建議，請在 `opensearch_dashboards.yml` 中進行以下設定：

```yaml
assistant.smartAnomalyDetector.enabled: true
```
{% include copy.html %}

### 步驟 2：建立異常偵測器建議代理程式

若要協調異常偵測器建議，請建立一個異常偵測器建議[代理程式]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/agents/)。若要建立代理程式，請傳送 `POST /_plugins/_flow_framework/workflow?provision=true` 請求，並以代理程式範本作為承載 (payload)。如需更多資訊，請參閱[設定 OpenSearch Assistant]({{site.url}}{{site.baseurl}}/dashboards/dashboards-assistant/index/#configuring-opensearch-assistant)。

如需代理程式範本範例，請參閱 [Flow Framework 範例範本](https://github.com/opensearch-project/flow-framework/tree/2.x/sample-templates)。請記下代理程式 ID，您將在下一個步驟中使用它。

### 步驟 3：設定代理程式

接著，設定在上一個步驟中建立的異常偵測器建議代理程式：

```json
POST /.plugins-ml-config/_doc/os_suggest_ad
{
  "type": "suggest_anomaly_detector_agent",
  "configuration": {
    "agent_id": "<SUGGEST_ANOMALY_DETECTOR_AGENT_ID>"
  }
}
```
{% include copy-curl.html %}

此範例示範的是系統索引。在已啟用安全性的網域中，只有超級管理員具有執行此程式碼的權限。如需進行超級管理員呼叫的相關資訊，請參閱[系統索引]({{site.url}}{{site.baseurl}}/security/configuration/system-indices/)。如需存取權限，請聯絡您的系統管理員。
{: .warning}

### 步驟 4：測試代理程式

您可以使用範例承載呼叫代理程式，以驗證代理程式是否已成功建立：

```json
POST /_plugins/_ml/agents/{SUGGEST_ANOMALY_DETECTOR_AGENT_ID}/_execute
{
  "parameters": {
    "index":"sample_weblogs_test"
  }
}
```
{% include copy-curl.html %}

## 在 OpenSearch Dashboards 中檢視異常偵測器建議

若要在 OpenSearch Dashboards 中檢視異常偵測器建議，請使用下列步驟：

1. 在頂端選單列中，前往 **OpenSearch Dashboards > Discover**。

1. 從索引模式下拉式清單中，選取一個索引模式。

1. 選取 **AI assistant** 下拉式清單，然後選取 **Suggest anomaly detector**，如下圖所示。

    ![按一下 Suggest anomaly detector 動作]({{site.url}}{{site.baseurl}}/images/dashboards-assistant/suggestAD-button.png){: width="420px" }

1. 等待 LLM 填入 **Suggest anomaly detector** 欄位，這些欄位將用於為該索引模式建立異常偵測器。接著選取 **Create detector** 按鈕以建立異常偵測器，如下圖所示。

    ![建議的異常偵測器]({{site.url}}{{site.baseurl}}/images/dashboards-assistant/suggestAD-UI.png){: width="800px" }
