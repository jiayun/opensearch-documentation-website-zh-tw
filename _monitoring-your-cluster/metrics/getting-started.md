---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "指標架構"
nav_order: 1
has_children: false
has_toc: false
redirect_from:
  - /monitoring-your-cluster/metrics/
---

# 指標架構

這是實驗性功能，不建議在正式環境中使用。如需瞭解此功能的最新進度，或想提供意見回饋，請參閱相關的 [GitHub 議題](https://github.com/opensearch-project/OpenSearch/issues/10141)。    
{: .warning}

雖然 OpenSearch Stats APIs 可讓您深入瞭解每個節點和整個 OpenSearch 叢集的內部運作，但這些統計資料缺少某些細節，例如百分位數，也未提供直方圖等更豐富指標類型的語意。因此，僅使用 Stats API 時，很難找出叢集統計資料中的離群值。 

指標架構功能新增完整的指標支援，可有效監控 OpenSearch 叢集。開發人員可以使用 Metrics Framework APIs、外掛程式和擴充功能，新增監控指標。此外，OpenSearch 發行套件隨附 `telemetry-otel` 外掛程式，提供以 [OpenTelemetry](https://opentelemetry.io) Java SDK 為基礎的指標量測實作。


## 入門

指標架構功能屬於實驗性功能。若要開始使用指標架構功能，您必須先使用 `opensearch.experimental.feature.telemetry.enabled` 功能旗標啟用 `telemetry feature`，接著再使用指標架構功能旗標。 

啟用此功能可能會耗用系統資源。啟用指標架構功能前，請確認您是否有足夠的叢集資源可供配置。
{: .warning}

### 使用 tarball 在節點上啟用功能旗標

`enable` 旗標透過 Java 虛擬機器（JVM）參數切換，此參數設定於 `OPENSEARCH_JAVA_OPTS` 或 `config/jvm.options` 中。

#### 選項 1：在 `opensearch.yml` 檔案中啟用實驗性功能旗標

1. 使用下列命令前往您的 OpenSearch 目錄：

  ```bash
  cd \path\to\opensearch
  ```

2. 開啟您的 `opensearch.yml` 檔案。
3. 將下列設定新增至 `opensearch.yml`：

  ```yaml
  opensearch.experimental.feature.telemetry.enabled: true
  ```
  {% include copy.html %}

4. 儲存變更並關閉檔案。

#### 選項 2：修改 jvm.options

若要使用 `jvm` 啟用指標架構功能，請在啟動 OpenSearch 前，將下列這一行新增至 `config/jvm.options`：

```bash
-Dopensearch.experimental.feature.telemetry.enabled=true
```
{% include copy.html %}

#### 選項 3：透過環境變數啟用

您可以將指標架構環境變數新增至 `OPENSEARCH_JAVA_OPTS` 命令，以單一命令啟用指標架構功能，如下列範例所示：

```bash
OPENSEARCH_JAVA_OPTS="-Dopensearch.experimental.feature.telemetry.enabled=true" ./opensearch-2.9.0/bin/opensearch
```
{% include copy.html %}

您也可以在執行 OpenSearch 前，執行下列命令以單獨定義環境變數：

```bash
export OPENSEARCH_JAVA_OPTS="-Dopensearch.experimental.feature.telemetry.enabled=true"
 ./bin/opensearch
```
{% include copy.html %}

### 使用 Docker 啟用 

如果您使用 Docker 執行 OpenSearch，請將下列這一行新增至 `docker-compose.yml` 中的 `environment` 下方：

```bash
OPENSEARCH_JAVA_OPTS="-Dopensearch.experimental.feature.telemetry.enabled=true"
```
{% include copy.html %}


### 啟用指標架構功能

啟用功能旗標後，您可以使用下列設定啟用指標架構功能，此設定會在 `opensearch.yaml` 檔案中啟用指標：

```bash
telemetry.feature.metrics.enabled: true
```

指標架構功能透過外掛程式支援各種遙測解決方案。請依照下列指示啟用 `telemetry-otel` 外掛程式：


1. **發布間隔：** 指標架構功能可以在本機彙總指標，包含所設定發布間隔的特有資訊，然後匯出這些指標。預設間隔為 1 分鐘。不過，您可以使用 `telemetry.otel.metrics.publish.interval` 叢集設定變更間隔。
2. **匯出器：** 匯出器負責持久儲存資料。OpenTelemetry 提供多種內建匯出器。OpenSearch 支援下列匯出器：
    - `LoggingMetricExporter`：將指標匯出至記錄檔，並在 logs 目錄中產生獨立的 `_otel_metrics.log` 檔案。預設為 `telemetry.otel.metrics.exporter.class=io.opentelemetry.exporter.logging.LoggingMetricExporter`。
    - `OtlpGrpcMetricExporter`：透過 gRPC 匯出跨度。若要使用此匯出器，您必須在節點上安裝 `otel-collector`。依預設，它會寫入 http://localhost:4317/ 端點。若要使用此匯出器，請設定下列靜態設定：`telemetry.otel.metrics.exporter.class=io.opentelemetry.exporter.otlp.metrics.OtlpGrpcMetricExporter`。
  
### 支援的指標類型

指標架構功能支援下列指標類型：

1. **計數器：** 計數器是連續且同步的量測工具，用於追蹤一段時間內事件發生的頻率。計數器只能以正值遞增，因此非常適合量測監控事件的數量，例如錯誤次數、已處理或已接收的位元組數，以及請求總數。
2. **增減計數器：** 增減計數器可以用正值遞增，也可以用負值遞減。增減計數器非常適合追蹤開啟的連線、作用中的請求和其他會波動的數量等指標。
3. **直方圖：** 直方圖是將連續資料的分布視覺化的實用工具。直方圖可讓您深入瞭解指標的集中趨勢、離散程度、偏態，以及可能存在的離群值。您可以輕易辨識常態分布、偏態分布或雙峰分布等模式，因此直方圖非常適合分析延遲指標和評估百分位數。
4. **非同步量測器：** 非同步量測器會在讀取指標的當下擷取目前的值。這些指標不具可加性，通常用於量測每分鐘的 CPU 使用率、記憶體使用率和其他即時數值。

## 監控機器學習工作流程
於 3.1 版推出
{: .label .label-purple }

OpenSearch 為[機器學習（ML）]({{site.url}}{{site.baseurl}}/ml-commons-plugin/)工作流程提供更完善的可觀測性。與 ML 作業相關的指標會直接推送至核心指標清冊，讓您更清楚掌握模型的使用情況和效能。此外，週期性作業每 5 分鐘會收集並匯出狀態資料，協助您持續監控 ML 工作負載的健康狀態和活動。

靜態收集器作業會擷取所建立的不同類型模型和代理程式的下列指標：

- **模型**：部署類型（遠端、預先訓練或自訂）、服務提供者、演算法、模型名稱和模型類型
- **代理程式**：LLM 介面、模型部署類型、服務提供者、模型類型、記憶體類型和模型識別碼


以下是所擷取模型指標的範例：

```
{is_hidden=false, service_provider=openai, model=gpt-4o-mini, type=llm, deployment=remote, algorithm=REMOTE}
```

以下是所擷取代理程式指標的範例：

```
{_llm_interface=bedrock/converse/claude, model_deployment=remote, is_hidden=false, model_service_provider=bedrock, model_type=llm, memory_type=conversation_index, model=us.anthropic.claude-3-7-sonnet-20250219-v1:0, type=CONVERSATIONAL}
```

若要啟用 ML 可觀測性，請在 `opensearch.yml` 中指定下列設定：

```yaml
plugins.ml_commons.metrics_collection_enabled: true
plugins.ml_commons.metrics_static_collection_enabled: true
```
{% include copy.html %}
