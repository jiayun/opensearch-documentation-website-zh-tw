---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "工作流程步驟"
nav_order: 10
---

# 工作流程步驟

_工作流程步驟_ 是流程自動化的基本「建置區塊」。大多數步驟直接對應 OpenSearch 或外掛程式 API 操作，例如對機器學習 (ML) 連接器、模型和代理程式的 CRUD 操作。有些步驟透過在多個步驟之間重複使用這些 API 預期的請求本文來簡化設定。例如，設定好 _工具_ 之後，即可將它與多個 _代理程式_ 搭配使用。  

## 工作流程步驟欄位

工作流程步驟仍在積極開發中，以擴充自動化功能。工作流程步驟 (圖形節點) 的組態包含下列欄位。

|欄位	|資料類型	|必要/選用	|說明	|
|:---	|:---	|:---	|:---	|
|`id`	|字串	|必要	|使用者為該步驟提供的 ID。此 ID 在指定的工作流程中必須是唯一的，並有助於識別該步驟建立的資源。例如，`register_agent` 步驟可能會傳回已註冊的 `agent_id`。使用此 ID，您可以判斷哪個步驟產生了哪個資源。	|
|`type`	|字串	|必要	|要執行的動作類型，例如 `deploy_model`，它對應於該步驟所使用的 API。多個步驟可以共用相同的類型，但每個步驟都必須有自己的唯一 ID。如需支援的類型清單，請參閱 [工作流程步驟類型](#workflow-step-types)。	|
|`previous_node_inputs`	|物件	|選用	|鍵值對應，指定由工作流程中前一個步驟產生的使用者輸入。對於每個鍵值對，鍵是前一個步驟的 `id`，值是將作為工作流程中前一個步驟輸出而產生的 API 本文欄位名稱 (例如 `model_id`)。例如，`register_remote_model` (鍵) 可能會產生後續 `deploy_model` 步驟所需的 `model_id` (值)。<br> 系統會自動在工作流程中新增一條圖形邊，以前一個步驟的鍵作為來源、以目前節點作為目的地。<br>在某些情況下，您可以在此欄位中包含[其他輸入](#additional-fields)。	|
|`user_inputs`	|物件	|選用	|對應 API 為此特定步驟所支援輸入的鍵值對應。有些輸入是 API 的必要項目，有些則是選用項目。必要輸入若已知，可在此處指定，或在 `previous_node_inputs` 欄位中指定。[Get Workflow Steps API]({{site.url}}{{site.baseurl}}/automating-configurations/api/get-workflow-steps/) 會識別必要輸入和步驟輸出。<br> 字串值、字串清單以及值為字串的對應皆支援替換。模式 `{% raw %}${{previous_step_id.output_key}}{% endraw %}` 將會被前一個步驟輸出中具有指定鍵的值所取代。例如，如果使用者輸入中的參數對應包含鍵 `embedding_model_id` 及其值 `{% raw %}${{deploy_embedding_model.model_id}}{% endraw %}`，則 `deploy_embedding_model` 步驟的 `model_id` 輸出將會在此處替換。它的功能類似 `previous_node_input` 對應，但不會進行驗證，也不會自動推斷邊。<br>在某些情況下，您可以在此欄位中包含[其他輸入](#additional-fields)。	|

## 工作流程步驟類型

下表列出工作流程步驟類型。這些步驟的 `user_inputs` 欄位直接對應所連結的 API。

|步驟類型	|對應的 API	|說明	|
|---	|---	|---	|
| `noop` | 無 API | 不執行任何動作的無操作 (no-op) 步驟，適合用於同步平行步驟。如果 `user_inputs` 欄位包含 `delay` 鍵，此步驟將等待指定的時間。	|
|`create_connector`	|[Create Connector]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/connector-apis/create-connector/)	|建立連至託管於第三方平台之模型的連接器。	|
|`delete_connector`	|[Delete Connector]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/connector-apis/delete-connector/)	|刪除連至託管於第三方平台之模型的連接器。	|
|`register_model_group`	|[Register Model Group]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/model-group-apis/register-model-group/)	|註冊模型群組。當群組中沒有任何模型時，模型群組將自動刪除。	|
|`register_remote_model`	|[Register Model (remote)]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/model-apis/register-model/#register-a-model-hosted-on-a-third-party-platform)	| 註冊託管於第三方平台的模型。如果 `user_inputs` 欄位包含設定為 `true` 的 `deploy` 鍵，則同時部署該模型。	| 
|`register_local_pretrained_model`	|[Register Model (pretrained)]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/model-apis/register-model/#register-a-pretrained-text-embedding-model)	| 註冊由 OpenSearch 提供並託管於您 OpenSearch 叢集上的預先訓練文字嵌入模型。如果 `user_inputs` 欄位包含設定為 `true` 的 `deploy` 鍵，也會部署該模型。	|
|`register_local_sparse_encoding_model`	|[Register Model (sparse)]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/model-apis/register-model/#register-a-pretrained-sparse-encoding-model)	| 註冊由 OpenSearch 提供並託管於您 OpenSearch 叢集上的預先訓練稀疏編碼模型。如果 `user_inputs` 欄位包含設定為 `true` 的 `deploy` 鍵，也會部署該模型。	|
|`register_local_custom_model`	|[Register Model (custom)]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/model-apis/register-model/#register-a-custom-model)	| 註冊託管於您 OpenSearch 叢集上的自訂模型。如果 `user_inputs` 欄位包含設定為 `true` 的 `deploy` 鍵，也會部署該模型。		|
|`delete_model`	|[Delete Model]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/model-apis/delete-model/)	|取消註冊並刪除模型。	|
|`deploy_model`	|[Deploy Model]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/model-apis/deploy-model/)	|將已註冊的模型部署至記憶體。	|
|`undeploy_model`	|[Undeploy Model]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/model-apis/undeploy-model/)	|將已部署的模型從記憶體中解除部署。	|
|`register_agent`	|[Register Agent API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/)	|將代理程式註冊為 ML Commons Agent Framework 的一部分。	|
|`delete_agent`	|[Delete Agent API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/)	|刪除代理程式。	|
|`create_tool`	|無 API	| 一種特殊的非 API 步驟，封裝 ML Commons Agent Framework 中代理程式的工具規格。這些會在適當的註冊代理程式步驟中列為 `previous_node_inputs`，其值設定為 `tools`。	|
|`create_index`|[Create Index]({{site.url}}{{site.baseurl}}/api-reference/index-apis/create-index/)     | 建立新的 OpenSearch 索引。輸入包括 `index_name` (應為要建立的索引名稱) 和 `configurations` (包含建立索引之一般 REST 請求的承載本文)。
|`create_ingest_pipeline`|[Create Ingest Pipeline]({{site.url}}{{site.baseurl}}/ingest-pipelines/create-ingest/) | 建立或更新資料匯入管線。輸入包括 `pipeline_id` (應為管線的 ID) 和 `configurations` (包含建立資料匯入管線之一般 REST 請求的承載本文)。
|`create_search_pipeline`|[Create Search Pipeline]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/creating-search-pipeline/) | 建立或更新搜尋管線。輸入包括 `pipeline_id` (應為管線的 ID) 和 `configurations` (包含建立搜尋管線之一般 REST 請求的承載本文)。
|`reindex`|[Reindex]({{site.url}}{{site.baseurl}}/api-reference/document-apis/reindex/)  | 重新編製索引文件 API 操作可讓您將全部或部分資料從來源索引複製到目的地索引。輸入包括 source_index、destination_index，以及文件重新編製索引 API 的下列選用參數：`refresh`、`requests_per_second`、`require_alias`、`slices` 和 `max_docs`。如需更多資訊，請參閱[重新編製索引的注意事項](#reindexing-considerations)。

## 重新編製索引的注意事項

重新編製索引可能是一項耗用大量資源的作業，若未妥善管理，可能導致您的叢集不穩定。 

使用 `reindex` 步驟時，請遵循下列最佳實務，以確保重新編製索引的程序順利進行，並避免叢集不穩定：

- **叢集擴充**：開始重新編製索引作業前，請確保您的 OpenSearch 叢集已適當擴充，足以處理額外的工作負載。視需要增加節點數量並調整資源配置（CPU、記憶體和磁碟），以支應重新編製索引程序，同時避免影響其他作業。

- **請求速率控制**：使用 `requests_per_second` 參數控制向叢集傳送重新編製索引請求的速率。這有助於調節叢集負載並避免資源耗盡。請先使用較低的值，再依據叢集的容量和效能逐步提高。

- **切片與平行處理**：`slices` 參數可讓您將重新編製索引程序分割成較小的平行任務。這有助於將工作負載分散至多個節點，並改善整體效能。不過，增加切片數量時請謹慎，因為新增切片可能會增加資源耗用量。

- **監控與調整**：重新編製索引期間，請密切監控叢集效能指標（例如 CPU、記憶體、磁碟使用量和執行緒集區）。如果您發現任何資源競爭或效能下降的跡象，請相應調整重新編製索引的參數，或考慮暫停作業，直到叢集恢復穩定。

- **優先順序與排程**：如果可能，請將重新編製索引作業安排在離峰時段或叢集使用率較低的期間，以盡量降低對其他作業和使用者流量的影響。

遵循這些最佳實務並謹慎管理重新編製索引程序，可確保您的 OpenSearch 叢集維持穩定且具備良好效能，同時有效率地在索引之間複製資料。

## 額外欄位

如果指定的步驟類型支援某個欄位，您可以在 `user_inputs` 欄位中加入下列額外欄位。

|欄位	|資料類型	| 步驟類型 | 說明	|
|---	|---	|---	|
|`node_timeout`	| 時間單位	| 全部 | 使用者為此步驟提供的逾時時間。例如，`20s` 表示 20 秒的逾時時間。	|
|`deploy`	| 布林值	| 註冊模型 | 若設為 `true`，也會部署模型。	|
|`tools_order`	| 清單	| 註冊代理程式 | 指定 `tools` 的順序。例如，指定 `["foo_tool", "bar_tool"]`，即可依照該順序排列這些工具。	|
|`delay`	| 時間單位	| 無操作 | 等待指定的時間。例如，`250ms` 指定等待 250 毫秒後再繼續工作流程。	|

在指定的情況下，您可以在 `previous_node_inputs` 欄位中加入下列額外欄位。

| 欄位	          |資料類型	| 說明	                                                                                                                                                                                                                                                                                                                                                                                                           |
|-----------------|---	|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `model_id`	     |字串	| `model_id` 用作多個步驟的輸入。`register_agent` 步驟類型有一個特殊情況：若 `user_inputs` 和 `previous_node_inputs` 中都沒有 `llm.model_id` 欄位，則可使用前一個節點的 `model_id` 欄位作為模型 ID 的備用值。`model_id` 也會包含在 `MLModelTool` 的 `create_tool` 步驟之 `parameters` 輸入中。	 |
| `agent_id`	     |字串	| `agent_id` 用作多個步驟的輸入。`agent_id` 也會包含在 `AgentTool` 的 `create_tool` 步驟之 `parameters` 輸入中。                                                                                                                                                                                                                                                          |
| `connector_id`	 |字串	| `connector_id` 用作多個步驟的輸入。`connector_id` 也會包含在 `ConnectorTool` 的 `create_tool` 步驟之 `parameters` 輸入中。                                                                                                                                                                                                                                              |

## 工作流程步驟範例

如需工作流程步驟的實作範例，請參閱[工作流程教學]({{site.url}}{{site.baseurl}}/automating-configurations/workflow-tutorial/)。
