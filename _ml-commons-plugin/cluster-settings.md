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

## 工作與模型限制設定

ML Commons 支援下列設定，用於限制每個節點上 ML 工作與模型的數量及持續時間：

- `plugins.ml_commons.max_ml_task_per_node` (動態，整數)：每個 ML 節點上可執行之 ML 工作的最大數量。當設為 `0` 時，任何節點上都不會執行 ML 工作。有效值為 0--10,000。預設值為 `10`。

- `plugins.ml_commons.max_model_on_node` (動態，整數)：可部署至每個 ML 節點之模型的最大數量。當設為 `0` 時，無法將任何模型部署至任何節點。有效值為 0--10,000。預設值為 `10`。

- `plugins.ml_commons.max_register_model_tasks_per_node` (動態，整數)：可在單一節點上平行執行之模型註冊工作的最大數量。當設為 `0` 時，無法在任何節點上註冊任何模型。有效值為 0--10。預設值為 `10`。

- `plugins.ml_commons.max_deploy_model_tasks_per_node` (動態，整數)：可在單一節點上平行執行之模型部署工作的最大數量。當設為 `0` 時，無法將任何模型部署至任何節點。有效值為 0--10。預設值為 `10`。

- `plugins.ml_commons.ml_task_timeout_in_seconds` (動態，整數)：ML 工作可執行的時間長度 (以秒為單位)。逾時後，工作會失敗。有效值為 1--86,400。預設值為 `600`。

- `plugins.ml_commons.sync_up_job_interval_in_seconds` (動態，整數)：ML Commons 執行作業以同步每個節點上新部署或取消部署之模型的間隔 (以秒為單位)。此作業會讓 [Profile API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/profile/) 傳回的執行階段資訊保持最新。當設為 `0` 時，ML Commons 會停止同步作業。有效值為 0--86,400。預設值為 `10`。

- `plugins.ml_commons.monitoring_request_count` (動態，長整數)：每個節點上受監控的預測請求數量。當設為 `0` 時，OpenSearch 會從快取中清除所有受監控的預測請求，並停止監控新的預測請求。有效值為 0--10,000,000。預設值為 `100`。

## 模型註冊設定

根據預設，ML Commons 僅允許從 OpenSearch 模型儲存庫註冊[預先訓練模型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/pretrained-models/)。ML Commons 支援下列設定，用於從其他來源註冊模型：

- `plugins.ml_commons.allow_registering_model_via_url` (動態，布林值)：當設為 `true` 時，使用者可使用 URL 註冊模型。預設值為 `false`。

- `plugins.ml_commons.allow_registering_model_via_local_file` (動態，布林值)：當設為 `true` 時，使用者可使用本機檔案註冊模型。預設值為 `false`。

- `plugins.ml_commons.trusted_url_regex` (動態，字串)：模型 URL 必須符合的 Java 正規表示式，模型才能註冊。預設值允許從任何 HTTP、HTTPS、FTP 或本機檔案 URL 註冊模型檔案。預設值為 `"^(https?|ftp|file)://[-a-zA-Z0-9+&@#/%?=~_|!:,.;]*[-a-zA-Z0-9+&@#/%=~_|]"`。

從 URL 註冊模型時，請確認來源受信任。從不受信任的來源載入模型可能會造成安全性風險。如需詳細資訊，請參閱 [PyTorch 不受信任模型的安全性指導方針](https://github.com/pytorch/pytorch/blob/main/SECURITY.md#untrusted-models)。
{: .warning}

`plugins.ml_commons.trusted_url_regex` 的預設值不安全。為確保安全，請將其設為僅符合包含您模型之受信任儲存庫的正規表示式，例如 `https://github.com/opensearch-project/ml-commons/blob/2.x/ml-algorithms/src/test/resources/org/opensearch/ml/engine/algorithms/text_embedding/*`。
{: .warning }

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

ML Commons 支援下列設定，可啟用及停用功能：

- `plugins.ml_commons.remote_inference.enabled`（動態，布林值）：當值為 `false` 時，使用者無法建立連接器，也無法註冊、部署外部託管模型或使用這些模型執行預測。預設值為 `true`。

- `plugins.ml_commons.local_model.enabled`（動態，布林值）：當值為 `false` 時，使用者無法註冊、部署本機模型或使用這些模型執行預測。預設值為 `true`。

- `plugins.ml_commons.connector_access_control_enabled`（動態，布林值）：當值為 `true` 時，管理員可以使用 `backend_roles` 控制 Connector APIs 的存取權。預設值為 `false`。

- `plugins.ml_commons.connector.vertexai_enabled`（動態，布林值）：當值為 `true` 時，使用者可以建立使用 `google_cloud` 通訊協定的連接器。如需詳細資訊，請參閱 [Google Cloud 驗證]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/google-cloud/)。預設值為 `false`。

- `plugins.ml_commons.safe_delete_model`（動態，布林值）：當值為 `true` 時，OpenSearch 會在刪除模型前檢查下游相依性。如果代理程式、搜尋管線、資料匯入管線或其他下游工作正在使用該模型，OpenSearch 會傳回錯誤，且不會刪除模型。預設值為 `false`。

- `plugins.ml_commons.enable_inhouse_python_model`（動態，布林值）：當值為 `true` 時，使用者可以執行 OpenSearch 支援的 Python 模型，例如[指標關聯]({{site.url}}{{site.baseurl}}/ml-commons-plugin/algorithms/#metrics-correlation)。預設值為 `false`。

- `plugins.ml_commons.agent_framework_enabled`（動態，布林值）：當值為 `true` 時，會啟用代理程式架構，包括代理程式與工具，並允許使用者註冊、執行、刪除、擷取及搜尋代理程式。預設值為 `true`。

- `plugins.ml_commons.memory_feature_enabled`（動態，布林值）：當值為 `true` 時，會啟用對話記憶，儲存對話中的所有訊息以供對話式搜尋使用。預設值為 `true`。

- `plugins.ml_commons.agentic_memory_enabled`（動態，布林值）：當值為 `true` 時，會啟用[代理程式記憶]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agentic-memory/)，為 AI 代理程式提供記憶管理功能，包括工作階段記憶、工作記憶、長期記憶，以及依命名空間組織的記憶歷程。預設值為 `true`。

- `plugins.ml_commons.rag_pipeline_feature_enabled`（動態，布林值）：當值為 `true` 時，會啟用用於檢索增強生成（RAG）的搜尋處理器。RAG 使用記憶與先前對話中的相關資訊產生回應，藉此改善查詢結果。預設值為 `true`。
