---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "適用於 OpenSearch Dashboards 的 OpenSearch Assistant"
nav_order: 110
has_children: true
has_toc: false
redirect_from:
  - /dashboards/dashboards-assistant/
---

請注意，機器學習模型具有機率性，且某些模型的表現可能優於其他模型，因此 OpenSearch Assistant 偶爾可能會產生不正確的資訊。我們建議您依據使用案例適當評估輸出的正確性，包括檢閱輸出內容，或將其與其他驗證因素結合使用。
{: .important}

# 適用於 OpenSearch Dashboards 的 OpenSearch Assistant
**於 2.13 版推出**
{: .label .label-purple }

OpenSearch Assistant 工具組可協助您為 OpenSearch Dashboards 建立 AI 驅動的助理，而不需要您具備專門的查詢工具或技能。

## 啟用 OpenSearch Assistant

若要在 OpenSearch Dashboards 中啟用 **OpenSearch Assistant**，請找到您的 `opensearch_dashboards.yml` 檔案副本，並設定下列選項：

```yaml
assistant.chat.enabled: true
```
{% include copy.html %}

接著透過下列 API 設定根 `agent_id`：

```json
PUT .plugins-ml-config/_doc/os_chat
{
    "type":"os_chat_root_agent",
    "configuration":{
        "agent_id": "your root agent id"
    }
}
```
{% include copy-curl.html %}

如需設定根代理程式的詳細資訊，請參閱[建立您自己的聊天機器人教學]({{site.url}}{{site.baseurl}}/ml-commons-plugin/tutorials/build-chatbot/#step-5-configure-a-root-chatbot-agent-in-opensearch-dashboards)。

此範例顯示的是系統索引。在已啟用安全性的網域中，只有超級管理員才有權限執行此程式碼。如需進行超級管理員呼叫的相關資訊，請參閱[系統索引]({{site.url}}{{site.baseurl}}/security/configuration/system-indices/)指南。如需存取權限，請聯絡您的 IT 管理員。
{: .warning}

接下來，請重新啟動 OpenSearch Dashboards 伺服器。成功重新啟動後，**OpenSearch Assistant** 會顯示在 OpenSearch Dashboards 介面中。

下圖顯示介面的螢幕擷取畫面。

![OpenSearch Assistant 介面]({{site.url}}{{site.baseurl}}/images/dashboards/opensearch-assistant-full-frame.png){: width="700" }

## 設定 OpenSearch Assistant

您可以使用 OpenSearch Dashboards 介面來設定 OpenSearch Assistant。請前往[入門指南](https://github.com/opensearch-project/dashboards-assistant/blob/main/GETTING_STARTED_GUIDE.md)以取得逐步操作說明。如需聊天機器人範本，請前往 [Flow Framework 外掛程式](https://github.com/opensearch-project/flow-framework)文件。您可以修改此範本，以使用您自己的模型並自訂聊天機器人工具。

如需透過 REST API 設定 OpenSearch Assistant 的相關資訊，請參閱 [OpenSearch Assistant 工具組]({{site.url}}{{site.baseurl}}/ml-commons-plugin/opensearch-assistant/)。

## 在 OpenSearch Dashboards 中使用 OpenSearch Assistant

下列教學將引導您在 OpenSearch Dashboards 中使用 OpenSearch Assistant。OpenSearch Assistant 可以全畫面或在側邊欄中檢視。預設檢視位於右側邊欄。若要在左側邊欄或以全畫面檢視助理，請選取工具列中的 {::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/icons/frame-icon.png" class="inline-icon" alt="frame icon"/>{:/}（框架）圖示，然後選擇偏好的選項。

### 開始對話

在 **Ask a question** 搜尋方塊中輸入提示，或使用快速鍵 `ctrl + /` 來開始對話。選取 **Go** 以開始對話。系統隨即產生回應。

下列螢幕擷取畫面顯示提示與回應的範例。

![在 OpenSearch Dashboards 中使用 OpenSearch Assistant 的提示與回應]({{site.url}}{{site.baseurl}}/images/dashboards/opensearch-assistant-QandA.png){: width="700" }

### 重新產生回應

在回應下方，選取重新產生圖示，即可為您原本的問題產生另一個答案。新的答案會取代先前的答案，並同時顯示在介面和聊天記錄中。下圖顯示重新產生的範例。

![重新產生的回應]({{site.url}}{{site.baseurl}}/images/dashboards/opensearch-assistant-regenerate.png){: width="700" }

### 建議的提示

OpenSearch Assistant 會建議提示，以協助您入門、延伸您現有的提示，或探索您可能未曾考慮過的其他查詢等。請選取回應欄位下方列出的建議提示。下圖顯示螢幕擷取畫面。

![建議的提示]({{site.url}}{{site.baseurl}}/images/dashboards/opensearch-assistant-suggestions.png){: width="700" }

### 為回應評分

若要為回應評分，請選取大拇指向上或大拇指向下圖示。下圖顯示介面的螢幕擷取畫面。意見回饋會儲存在訊息索引的 `additional_info` 欄位中。

### 回應產生

選取 **How was this generated?** 選項，即可了解回應是如何產生的。此選項包含在可用的建議中，可協助您了解建立回應時使用了哪些工具。如果使用了多個工具，每個步驟都會顯示工具名稱及其輸入和輸出。此功能有助於疑難排解。下圖顯示螢幕擷取畫面。

![回應產生詳細資料]({{site.url}}{{site.baseurl}}/images/dashboards/opensearch-assistant-how-generated.png){: width="700" }

### 繼續之前的對話

若要檢視之前的對話，請選取時鐘圖示以開啟對話記錄面板並顯示聊天記錄。您也可以依對話名稱搜尋對話記錄。下圖顯示螢幕擷取畫面。

![對話記錄]({{site.url}}{{site.baseurl}}/images/dashboards/opensearch-assistant-conversation-history.png){: width="400" }

#### 編輯和刪除之前的對話

選取鉛筆圖示以編輯對話名稱並重新命名。選取 **Confirm name** 按鈕以儲存新名稱。下圖顯示螢幕擷取畫面。

![編輯對話名稱]({{site.url}}{{site.baseurl}}/images/dashboards/opensearch-assistant-edit-convo.png){: width="300" }

選取垃圾桶圖示以刪除對話。確認對話方塊出現後，選取 **Delete conversation**。該對話隨即會從您的聊天記錄中刪除。下圖顯示螢幕擷取畫面。

![刪除對話]({{site.url}}{{site.baseurl}}/images/dashboards/opensearch-assistant-delete-convo.png){: width="300" }

### 透過 Notebooks 分享對話

您可以使用 [Notebooks]({{site.url}}{{site.baseurl}}/observing-your-data/notebooks/) 來儲存您的對話。若要使用此選項，請從 **OpenSearch Assistant** 右側的下拉式選單中選取 **Save to notebook**。輸入 Notebook 的名稱，然後選取 **Save**。右下角會出現快顯訊息，確認對話已儲存。

您與大型語言模型 (LLM) 之間的所有對話（提示與回應／問題與答案）都會儲存到此 Notebook。

若要開啟已儲存的 Notebook 或檢視其他 Notebook 清單，請從 OpenSearch Dashboards 導覽選單中選取 **Observability** > **Notebooks**。

下圖顯示包含已儲存對話清單的 Notebooks 介面螢幕擷取畫面。

![包含已儲存 OpenSearch Assistant 對話的 Notebooks 介面]({{site.url}}{{site.baseurl}}/images/dashboards/opensearch-assistant-notebooks.png){: width="700" }

下列螢幕擷取畫面顯示一個已儲存的對話，以及您可以對該已儲存對話執行的動作。

![包含已儲存 OpenSearch Assistant 對話的 Notebooks 介面]({{site.url}}{{site.baseurl}}/images/dashboards/opensearch-assistant-save-notebook.png){: width="700" }

## 啟用 Dashboards Assistant 實驗性功能
**於 2.16 版推出**
{: .label .label-purple }

若要啟用實驗性助理功能（例如文字轉視覺化），請找到您的 `opensearch_dashboards.yml` 檔案副本，並設定下列選項：

```yaml
assistant.next.enabled: true
```
{% include copy-curl.html %}

## 其他 Dashboards Assistant 功能

如需其他 Dashboards Assistant 功能的相關資訊，請參閱下列頁面：

- [產生警示洞察]({{site.url}}{{site.baseurl}}/dashboards/dashboards-assistant/alert-insight/)
- [產生資料摘要]({{site.url}}{{site.baseurl}}/dashboards/dashboards-assistant/data-summary/)
- [產生異常偵測器建議]({{site.url}}{{site.baseurl}}/dashboards/dashboards-assistant/suggest-anomaly-detector/)
- [從文字產生視覺化]({{site.url}}{{site.baseurl}}/dashboards/dashboards-assistant/text-to-visualization/)

## 相關文件

- [OpenSearch Dashboards 中 OpenSearch Assistant 的入門指南](https://github.com/opensearch-project/dashboards-assistant/blob/main/GETTING_STARTED_GUIDE.md)
- [透過 REST API 設定 OpenSearch Assistant]({{site.url}}{{site.baseurl}}/ml-commons-plugin/opensearch-assistant/)
- [建立您自己的聊天機器人]({{site.url}}{{site.baseurl}}/ml-commons-plugin/tutorials/build-chatbot/)
