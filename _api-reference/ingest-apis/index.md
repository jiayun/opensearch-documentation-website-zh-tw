---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "資料匯入 API"
has_children: false
nav_order: 70
redirect_from:
  - /opensearch/rest-api/ingest-apis/index/
  - /api-reference/ingest-apis/
---

# 資料匯入 API
**於 1.0 版推出**
{: .label .label-purple }

使用資料匯入 API 來管理[資料匯入管線]({{site.url}}{{site.baseurl}}/ingest-pipelines/)，在 OpenSearch 為文件編製索引之前先轉換文件。管線由一連串的[資料匯入處理器]({{site.url}}{{site.baseurl}}/ingest-pipelines/processors/index-processors/)組成，每個處理器執行一項轉換，例如重新命名欄位、剖析記錄檔行，或產生向量嵌入。

## 管線 API

下列 API 可建立、擷取、測試及刪除資料匯入管線。

API | 端點 | 說明
:--- | :--- | :---
[建立或更新管線]({{site.url}}{{site.baseurl}}/ingest-pipelines/create-ingest/) | `PUT _ingest/pipeline/{pipeline-id}` | 建立管線，或取代現有管線的定義。
[取得管線]({{site.url}}{{site.baseurl}}/ingest-pipelines/get-ingest/) | `GET _ingest/pipeline/{pipeline-id}` | 傳回一或多個管線的定義。省略管線 ID 即可傳回所有管線。
[模擬管線]({{site.url}}{{site.baseurl}}/ingest-pipelines/simulate-ingest/) | `POST _ingest/pipeline/{pipeline-id}/_simulate` | 對範例文件執行管線，但不將其編製索引。您可以模擬現有管線，或在請求本文中提供管線定義。
[刪除管線]({{site.url}}{{site.baseurl}}/ingest-pipelines/delete-ingest/) | `DELETE _ingest/pipeline/{pipeline-id}` | 刪除一或多個管線。

## 處理器 API

下列 API 會傳回特定處理器的相關資訊。

API | 端點 | 說明
:--- | :--- | :---
[取得 grok 模式]({{site.url}}{{site.baseurl}}/ingest-pipelines/processors/grok/#retrieving-built-in-patterns) | `GET _ingest/processor/grok` | 傳回您可以在 `grok` 處理器運算式中參考的內建模式。

## 相關 API

下列 API 並非匯入 API，但會傳回匯入處理的相關資訊：

- 若要列出每個節點上安裝的處理器，請使用 [Nodes Info API]({{site.url}}{{site.baseurl}}/api-reference/nodes-apis/nodes-info/)：`GET _nodes/ingest?filter_path=nodes.*.ingest.processors`。
- 若要檢視每個管線與處理器的統計資料，例如已處理與失敗的文件數量，請使用 [Nodes Stats API]({{site.url}}{{site.baseurl}}/api-reference/nodes-apis/nodes-stats/)：`GET _nodes/stats/ingest`。

若要將管線套用至文件，請在編製索引請求中指定該管線，或將其設為索引的預設管線。如需詳細資訊，請參閱[將管線套用至文件]({{site.url}}{{site.baseurl}}/ingest-pipelines/#applying-a-pipeline-to-documents)。

## 必要權限

如果您使用 Security 外掛程式，必須具備下列權限才能使用資料匯入 API。

權限 | 用於
:--- | :---
`cluster:admin/ingest/pipeline/put` | 建立或更新管線
`cluster:admin/ingest/pipeline/get` | 擷取管線
`cluster:admin/ingest/pipeline/simulate` | 模擬管線
`cluster:admin/ingest/pipeline/delete` | 刪除管線
`cluster:admin/ingest/processor/grok/get` | 擷取 grok 模式

`cluster_manage_pipelines` 動作群組授予所有管線權限（`cluster:admin/ingest/pipeline/*`），但不包含 grok 模式權限。如需更多資訊，請參閱[預設動作群組]({{site.url}}{{site.baseurl}}/security/access-control/default-action-groups/)。
