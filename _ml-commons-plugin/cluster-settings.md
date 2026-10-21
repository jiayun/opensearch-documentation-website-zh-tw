---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "ML Commons 叢集設定"
has_children: false
nav_order: 120
---

# ML 叢集設定

下列設定可設定 ML Commons 外掛程式。您可以在 `opensearch.yml` 檔案中指定這些設定，或使用 [Cluster Settings API]({{site.url}}{{site.baseurl}}/api-reference/cluster-api/cluster-settings/) 更新它們。本頁所有 ML Commons 設定皆為動態設定。

若要進一步了解靜態與動態設定，請參閱[設定 OpenSearch]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/index/)。

## ML 節點

根據預設，ML 工作與本機模型僅在 ML 節點上執行。若未設定 `data` 節點角色，ML 節點不會儲存任何分片，而是在執行階段計算資源需求。若要使用 ML 節點，請在您的 `opensearch.yml` 檔案中建立節點。為您的節點指定自訂名稱，並將節點角色定義為 `ml`：

```yml
node.roles: [ ml ]
```
{% include copy.html %}

如需具有專用 ML 節點之叢集的範例，請參閱範例 [Docker Compose 檔案](https://github.com/opensearch-project/ml-commons/blob/main/docs/docker/docker-compose.yml)。

## 節點選取設定

ML Commons 支援下列設定，用於選取執行 ML 工作與模型的節點：

- `plugins.ml_commons.only_run_on_ml_node` (動態，布林值)：當設為 `true` 時，本機模型僅在 ML 節點上執行。當設為 `false` 時，本機模型會在 `plugins.ml_commons.task_dispatcher.eligible_node_role.local_model` 中所列角色的節點上執行。若要在資料節點上測試模型，請將其設為 `false`。預設值為 `true`。

- `plugins.ml_commons.task_dispatcher.eligible_node_role.local_model` (動態，清單)：本機模型可執行所在的節點角色。此設定僅在 `plugins.ml_commons.only_run_on_ml_node` 為 `false` 時適用。預設值為 `["data", "ml"]`。

- `plugins.ml_commons.task_dispatcher.eligible_node_role.remote_model` (動態，清單)：外部託管模型可執行所在的節點角色。例如，將其設為 `["ml"]`，即可僅在 ML 節點上執行外部託管模型。預設值為 `["data", "ml"]`。

- `plugins.ml_commons.task_dispatch_policy` (動態，字串)：將 ML 工作分派至 ML 節點的原則。有效值為 `round_robin`，其使用輪詢路由分派工作，以及 `least_load`，其會從所有 ML 節點收集執行階段資訊 (例如 JVM 堆積記憶體使用量與執行中的工作)，並將工作分派至負載最低的節點。預設值為 `round_robin`。

- `plugins.ml_commons.exclude_nodes._name` (動態，字串)：一個節點名稱或以逗號分隔的節點名稱清單 (例如 `node1, node2`)，ML 工作不會在這些節點上執行。

- `plugins.ml_commons.allow_custom_deployment_plan` (動態，布林值)：當設為 `true` 時，使用者可根據其權限將模型部署至特定的 ML 節點。預設值為 `false`。

我們建議在生產叢集上將 `plugins.ml_commons.only_run_on_ml_node` 設為 `true`。
{: .tip}

## 任務與模型限制設定

ML Commons 支援下列設定，用於限制 ML 任務與模型：

- `plugins.ml_commons.max_ml_task_per_node`（動態，整數）：每個 ML 節點可執行的 ML 任務數量上限。設為 `0` 時，任何節點都不會執行 ML 任務。有效值為 0--10,000。預設值為 `10`。

- `plugins.ml_commons.max_model_on_node`（動態，整數）：可部署至每個 ML 節點的模型數量上限。設為 `0` 時，任何節點都無法部署模型。有效值為 0--10,000。預設值為 `10`。

- `plugins.ml_commons.max_register_model_tasks_per_node`（動態，整數）：單一節點上可平行執行的模型註冊任務數量上限。設為 `0` 時，任何節點都無法註冊模型。有效值為 0--10。預設值為 `10`。

- `plugins.ml_commons.max_deploy_model_tasks_per_node`（動態，整數）：單一節點上可平行執行的模型部署任務數量上限。設為 `0` 時，任何節點都無法部署模型。有效值為 0--10。預設值為 `10`。

- `plugins.ml_commons.ml_task_timeout_in_seconds`（動態，整數）：ML 任務可執行的時間長度，以秒為單位。逾時後，任務會失敗。有效值為 1--86,400。預設值為 `600`。

- `plugins.ml_commons.sync_up_job_interval_in_seconds`（動態，整數）：ML Commons 執行作業以同步各節點上新部署或取消部署之模型的間隔，以秒為單位。此作業會讓 [Profile API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/profile/) 傳回的執行階段資訊保持最新。設為 `0` 時，ML Commons 會停止同步作業。有效值為 0--86,400。預設值為 `10`。

- `plugins.ml_commons.monitoring_request_count`（動態，長整數）：每個節點上受監控的預測請求數量。設為 `0` 時，OpenSearch 會從快取清除所有受監控的預測請求，並停止監控新的預測請求。有效值為 0--10,000,000。預設值為 `100`。

- `plugins.ml_commons.max_batch_inference_tasks`（動態，整數）：叢集中可處於 `CREATED` 或 `RUNNING` 狀態的[批次推論]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/model-apis/batch-predict/)任務數量上限。達到此上限時，OpenSearch 會拒絕新的批次推論請求。設為 `0` 時，無法執行任何批次推論任務。有效值為 0--10,000。預設值為 `100`。

- `plugins.ml_commons.max_json_size`（動態，整數）：ML Commons 所剖析之 JSON 字串的大小上限，以位元組為單位，例如外部託管模型傳回的回應。若 JSON 字串超過此大小，請求會失敗。若要移除限制，請將此值設為 `-1`。預設值為 `100000000`（100 MB）。

## 模型註冊設定

根據預設，ML Commons 僅允許從 OpenSearch 模型儲存庫註冊[預先訓練模型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/pretrained-models/)。ML Commons 支援下列設定，用於從其他來源註冊模型：

- `plugins.ml_commons.allow_registering_model_via_url` (動態，布林值)：當設為 `true` 時，使用者可使用 URL 註冊模型。預設值為 `false`。

- `plugins.ml_commons.allow_registering_model_via_local_file` (動態，布林值)：當設為 `true` 時，使用者可使用本機檔案註冊模型。預設值為 `false`。

- `plugins.ml_commons.trusted_url_regex` (動態，字串)：模型 URL 必須符合的 Java 正規表示式，模型才能註冊。預設值允許從任何 HTTP、HTTPS、FTP 或本機檔案 URL 註冊模型檔案。預設值為 `"^(https?|ftp|file)://[-a-zA-Z0-9+&@#/%?=~_|!:,.;]*[-a-zA-Z0-9+&@#/%=~_|]"`。

從 URL 註冊模型時，請確認來源受信任。從不受信任的來源載入模型可能會造成安全性風險。如需詳細資訊，請參閱 [PyTorch 不受信任模型的安全性指導方針](https://github.com/pytorch/pytorch/blob/main/SECURITY.md#untrusted-models)。
{: .warning}

`plugins.ml_commons.trusted_url_regex` 的預設值不安全。為確保安全，請將其設為僅符合包含您模型之受信任儲存庫的正規表示式，例如 `https://github.com/opensearch-project/ml-commons/blob/2.x/ml-algorithms/src/test/resources/org/opensearch/ml/engine/algorithms/text_embedding/*`。
{: .warning }

## 連接器端點設定

ML Commons 支援下列設定，用於控制連接器傳送請求的目標端點：

- `plugins.ml_commons.trusted_connector_endpoints_regex`（動態，清單）：Java 正規表示式清單。只有當連接器的端點 URL 符合其中一個表示式時，OpenSearch 才會接受該連接器。您提供的值會取代整份預設清單。如需預設清單，請參閱[新增受信任的端點]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/index/#adding-trusted-endpoints)。

- `plugins.ml_commons.connector.private_ip_enabled`（動態，布林值）：當值為 `true` 時，連接器可以將請求傳送至解析為私有、連結本機或迴路 IP 位址的主機，例如 `10.0.0.1` 或 `127.0.0.1`。當值為 `false` 時，如果模型的連接器端點解析為這類位址，OpenSearch 就會拒絕該模型的預測請求。若要將變更套用至已部署的模型，請重新部署模型。預設值為 `false`。

- `plugins.ml_commons.trusted_connector_private_endpoints_regex`（動態，清單）：Java 正規表示式清單，用於限制連接器可傳送請求的私有端點。此設定僅在 `plugins.ml_commons.connector.private_ip_enabled` 為 `true` 時適用。如果清單包含表示式，則主機解析為私有 IP 位址的連接器 URL 必須符合其中一個表示式。如果清單為空，連接器可以將請求傳送至任何私有端點。若要將變更套用至已部署的模型，請重新部署模型。預設值為 `[]`。

## 斷路器設定

執行 ML 工作之前，ML Commons 會檢查記憶體與磁碟使用量。若使用量超過閾值，OpenSearch 會觸發斷路器、擲回例外狀況，且不執行該工作。ML Commons 支援下列斷路器設定：

- `plugins.ml_commons.native_memory_threshold` (動態，整數)：ML 工作可執行時的原生記憶體使用量上限，以總系統記憶體的百分比表示。此斷路器可防止載入過多模型時發生記憶體不足錯誤。當設為 `0` 時，不會執行任何 ML 工作。當設為 `100` 時，會停用斷路器。有效值為 0--100。預設值為 `90`。

- `plugins.ml_commons.jvm_heap_memory_threshold` (動態，整數)：ML 工作可執行時的 JVM 堆積記憶體使用量上限，以總 JVM 堆積的百分比表示。當設為 `0` 時，不會執行任何 ML 工作。當設為 `100` 時，會停用斷路器。有效值為 0--100。預設值為 `85`。

- `plugins.ml_commons.disk_free_space_threshold` (動態，位元組大小)：執行 ML 工作所需的最小可用磁碟空間量。若可用磁碟空間低於此值，就會觸發斷路器。若要停用斷路器，請將此值設為 `-1`。預設值為 `5gb`。

## 模型部署設定

ML Commons 支援下列設定，可自動部署及重新部署模型：

- `plugins.ml_commons.model_auto_deploy.enable`（動態，布林值）：當值為 `true` 時，若 OpenSearch 收到外部託管模型的預測請求，且該模型尚未部署，就會自動部署該模型。預設值為 `true`。

- `plugins.ml_commons.model_auto_redeploy.enable`（動態，布林值）：當值為 `true` 時，OpenSearch 會在叢集故障後，自動重新部署已部署或部分部署的模型。如果叢集中的所有 ML 節點都故障，模型會進入 `DEPLOY_FAILED` 狀態，且必須手動部署。預設值為 `true`。

- `plugins.ml_commons.model_auto_redeploy.lifetime_retry_times`（動態，整數）：當叢集中的 ML 節點故障，或新的 ML 節點加入叢集時，OpenSearch 嘗試重新部署已部署或部分部署模型的次數上限。設定為 `0` 或負值時，OpenSearch 不會自動重新部署模型。預設值為 `3`。

- `plugins.ml_commons.model_auto_redeploy_success_ratio`（動態，浮點數）：自動重新部署成功所需的最低可用 ML 節點比例，模型必須在至少此比例的節點上重新部署。例如，如果比例為 `0.7`，且模型已在 70% 的可用 ML 節點上重新部署，則重新部署成功。如果模型重新部署的節點少於可用 ML 節點的 70%，OpenSearch 會重試重新部署，直到成功或達到 `plugins.ml_commons.model_auto_redeploy.lifetime_retry_times` 上限。有效值為 0--1。預設值為 `0.8`。

## 動態批次處理記憶體設定

節點上的所有模型共用可供[動態批次處理]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/batching-requests/#dynamically-batching-small-prediction-requests)使用的記憶體。當此記憶體耗盡時，OpenSearch 會拒絕新的佇列項目。請使用退避機制重試遭拒絕的請求，或依工作負載調整記憶體設定。ML Commons 支援下列設定，可控制此記憶體的大小：

- `plugins.ml_commons.dynamic_batching.memory.fraction`（動態，雙精度浮點數）：用於計算每個節點可供動態批次處理使用的記憶體大小，占 JVM 堆積上限的比例。計算出的值受 `plugins.ml_commons.dynamic_batching.memory.min` 和 `plugins.ml_commons.dynamic_batching.memory.max` 限制。有效值為 0.0--0.1。預設值為 `0.01`。

- `plugins.ml_commons.dynamic_batching.memory.min`（動態，位元組大小）：每個節點可供動態批次處理使用的記憶體大小下限。預設值為 `64mb`。

- `plugins.ml_commons.dynamic_batching.memory.max`（動態，位元組大小）：每個節點可供動態批次處理使用的記憶體大小上限。此值必須大於或等於 `plugins.ml_commons.dynamic_batching.memory.min`。預設值為 `512mb`。

## 功能設定

ML Commons 支援下列用於啟用與停用功能的設定：

- `plugins.ml_commons.remote_inference.enabled`（動態，布林值）：當設為 `false` 時，使用者無法建立連接器，也無法使用外部託管的模型註冊、部署或執行預測。預設值為 `true`。

- `plugins.ml_commons.local_model.enabled`（動態，布林值）：當設為 `false` 時，使用者無法使用本機模型註冊、部署或執行預測。預設值為 `true`。

- `plugins.ml_commons.offline_batch_inference_enabled`（動態，布林值）：當設為 `false` 時，使用者無法執行[批次推論]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/model-apis/batch-predict/)，也無法取得或取消批次推論任務。預設值為 `true`。

- `plugins.ml_commons.controller_enabled`（動態，布林值）：當設為 `false` 時，使用者無法使用 [Controller APIs]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/controller-apis/index/) 建立、更新、取得或刪除模型控制器。預設值為 `true`。

- `plugins.ml_commons.model_access_control_enabled`（動態，布林值）：當設為 `true` 且 Security 外掛程式已啟用時，管理員可以使用模型群組控制模型的存取權。如需更多資訊，請參閱[模型存取控制]({{site.url}}{{site.baseurl}}/ml-commons-plugin/model-access-control/)。預設值為 `false`。

- `plugins.ml_commons.connector_access_control_enabled`（動態，布林值）：當設為 `true` 時，管理員可以使用 `backend_roles` 控制 Connector APIs 的存取權。預設值為 `false`。

- `plugins.ml_commons.connector.vertexai_enabled`（動態，布林值）：當設為 `true` 時，使用者可以建立使用 `google_cloud` 協定的連接器。如需更多資訊，請參閱 [Google Cloud 驗證]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/google-cloud/)。預設值為 `false`。

- `plugins.ml_commons.connector.mutual_tls_enabled`（動態，布林值）：當設為 `true` 時，使用者可以建立連接器，在 `client_config` 中將 `mutual_tls_enabled` 設為 `true`，以使用用戶端憑證進行驗證。如需更多資訊，請參閱[用戶端憑證驗證]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/http-authentication/#client-certificate-authentication)。預設值為 `false`。

- `plugins.ml_commons.mcp_connector_enabled`（動態，布林值）：當設為 `true` 時，使用者可以建立使用 `mcp_sse` 或 `mcp_streamable_http` 協定的連接器，並註冊使用 MCP 連接器的代理程式。如需更多資訊，請參閱[連線至外部 MCP 伺服器]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/mcp/mcp-connector/)。預設值為 `false`。

- `plugins.ml_commons.safe_delete_model`（動態，布林值）：當設為 `true` 時，OpenSearch 會在刪除模型前檢查下游相依項。如果模型正被代理程式、搜尋管線、資料匯入管線或其他下游任務使用，OpenSearch 會傳回錯誤且不會刪除該模型。預設值為 `false`。

- `plugins.ml_commons.enable_inhouse_python_model`（動態，布林值）：當設為 `true` 時，使用者可以執行 OpenSearch 支援的 Python 型模型，例如[指標相關性分析]({{site.url}}{{site.baseurl}}/ml-commons-plugin/algorithms/#metrics-correlation)。預設值為 `false`。

- `plugins.ml_commons.agent_framework_enabled`（動態，布林值）：當設為 `true` 時，會啟用代理程式框架（包括代理程式與工具），並允許使用者註冊、執行、刪除、擷取及搜尋代理程式。預設值為 `true`。

- `plugins.ml_commons.unified_agent_api_enabled`（動態，布林值）：當設為 `false` 時，使用者無法使用[統一註冊方法]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/agents/#unified-registration-method)註冊代理程式，也無法使用標準化的 `input` 欄位執行代理程式。預設值為 `true`。

- `plugins.ml_commons.execute_tools_enabled`（動態，布林值）：當設為 `false` 時，使用者無法使用 [Execute Tool API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/execute-tool/) 執行工具。預設值為 `true`。

- `plugins.ml_commons.mcp_server_enabled`（動態，布林值）：當設為 `true` 時，會啟用 [MCP server APIs]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/mcp-server-apis/index/)，讓代理程式能夠使用 Model Context Protocol (MCP) 連線至 OpenSearch 並使用其工具。預設值為 `false`。

- `plugins.ml_commons.memory_feature_enabled`（動態，布林值）：當設為 `true` 時，會啟用對話記憶，儲存對話中的所有訊息以供對話式搜尋使用。預設值為 `true`。

- `plugins.ml_commons.agentic_memory_enabled`（動態，布林值）：當設為 `true` 時，會啟用[代理記憶]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agentic-memory/)（agentic memory），為 AI 代理程式提供記憶管理，包括工作階段記憶、工作記憶、長期記憶，以及依命名空間組織的記憶歷程。預設值為 `true`。

- `plugins.ml_commons.rag_pipeline_feature_enabled`（動態，布林值）：當設為 `true` 時，會啟用用於檢索增強生成 (RAG) 的搜尋處理器。RAG 透過使用記憶與先前對話中的相關資訊來產生回應，以強化查詢結果。預設值為 `true`。
