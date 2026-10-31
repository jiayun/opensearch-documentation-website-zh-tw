---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "逐文件監視器"
nav_order: 20
parent: Monitors
grand_parent: Alerting
has_children: false
---

# 每份文件監視器
於 2.0 版推出
{: .label .label-purple }

每份文件監視器會針對自監視器上次執行以來新增至索引的文件執行一或多個查詢，並為符合觸發條件的文件產生警示。例如，您可以使用每份文件監視器來：

- 在記錄項目匯入時，偵測其中是否包含錯誤或安全性事件。
- 偵測違反資料品質規則的文件，例如欄位中包含非預期值的文件。

每份文件監視器在首次執行時，不會評估索引中既有的文件，只會評估之後新增的文件。

每份文件監視器不支援跨叢集搜尋。
{: .note}

## 建立每份文件的監視器

以下範例建立一個監視器，當含有 `404` 回應的網頁記錄檔被編製索引時，便會產生警示。

1. 為範例記錄檔建立一個索引。在 **Dev Tools** 中，傳送以下請求：

   ```json
   PUT web-logs
   {
     "mappings": {
       "properties": {
         "response": { "type": "keyword" },
         "request": { "type": "keyword" },
         "timestamp": { "type": "date" }
       }
     }
   }
   ```
{% include copy-curl.html %}

1. 在頂端選單中，前往 **OpenSearch Plugins** > **Alerting**。
1. 選取 **Monitors** 標籤，然後選取 **Create monitor**。
1. 在 **Monitor details** 中，輸入 **Monitor name**，例如 `Not found responses`，並選取 **Per document monitor**。在 **Monitor defining method** 中，選取 **Visual editor**。您可以視需要變更 **Schedule**。預設情況下，監視器每分鐘執行一次。
1. 在 **Select data** 中，於 **Index** 輸入 `web-logs` 並按下 Enter。
1. 在 **Query** 中定義查詢：
   - **Query name**：輸入 `not-found`。
   - **Field**：選取 `response`，選取 **is**，然後輸入 `404`。
   - **Tags**：視需要選取 **Add tag** 並輸入 `errors`。標籤會將查詢分組，使觸發條件能夠參照所有帶有該標籤的查詢。

   若要定義更多查詢，請選取 **Add another query**。一個監視器最多支援 10 個查詢。可用的運算子取決於欄位類型。例如，數值欄位支援 **is greater than** 與 **is less than**。
1. 在 **Triggers** 中選取 **Add trigger**，然後設定觸發條件：
   - **Trigger name**：輸入 `Not found responses`。
   - **Trigger conditions**：選取 `not-found` 查詢。若要改為參照所有帶有某個標籤的查詢，請選取該標籤。若要組合多個條件，請選取 **Add condition**。
1. 您可以視需要在 **Actions** 中新增一個動作，在符合觸發條件時傳送通知。如需更多資訊，請參閱 [動作]({{site.url}}{{site.baseurl}}/observing-your-data/alerting/actions/)。
1. 選取 **Create**。
1. 將一份符合查詢條件的文件編製索引：

   ```json
   POST web-logs/_doc
   {
     "response": "404",
     "request": "/missing-page",
     "timestamp": "2026-10-28T02:00:00Z"
   }
   ```
{% include copy-curl.html %}

在監視器下次執行時，會為符合條件的文件產生一個處於 **Active** 狀態的警示。若文件具有其他回應碼，例如 `200`，則不符合查詢條件，也不會產生警示。

若要使用 API 定義查詢與觸發條件，請參閱 [文件層級監視器]({{site.url}}{{site.baseurl}}/observing-your-data/alerting/api/#document-level-monitors)。

## 文件發現項目

當文件符合查詢時，監視器會建立一個_發現項目_（finding），也就是該文件與其符合之查詢的記錄。發現項目會儲存在 `.opensearch-alerting-finding*` 索引中。每個發現項目包含下列資訊。

欄位 | 說明
:--- | :---
Document | 文件 ID 與索引名稱，以垂直線分隔，例如 `Re5akdirhj3fl` 和 `web-logs`。
Query | 符合該文件之查詢的名稱。
Time found | 監視器發現該文件的時間。

Security Analytics 會使用發現項目，將查詢符合情況與警示分開分析。如需詳細資訊，請參閱[使用發現項目]({{site.url}}{{site.baseurl}}/security-analytics/usage/findings/)。
{: .note}

在匯入大量文件的叢集中，範圍廣泛的查詢可能會建立許多發現項目。只有在查詢具有特定性時，才為每個發現項目傳送通知。
{: .important}
