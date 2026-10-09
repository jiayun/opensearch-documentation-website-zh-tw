---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "工具"
nav_order: 50
has_children: false
nav_exclude: true
permalink: /tools/
redirect_from:
  - /clients/agents-and-ingestion-tools/index/
  - /tools/index/
---

# OpenSearch 工具

OpenSearch 提供命令列工具與公用程式，用於匯入資料、管理叢集，以及從其他搜尋引擎遷移。支援的工具包括：

- [代理程式與資料匯入工具](#agents-and-ingestion-tools)
- [OpenSearch CLI](#opensearch-cli)
- [OpenSearch Kubernetes operator]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/operator/)
- [OpenSearch 升級、遷移與比較工具](#opensearch-upgrade-migration-and-comparison-tools)
- [Sycamore](#sycamore)，用於對複雜文件執行 AI 驅動的擷取、轉換、載入 (ETL)，以進行向量搜尋與混合搜尋

如需 Data Prepper 的相關資訊，這是用於篩選、充實、轉換、正規化及彙總資料，以供下游分析與視覺化使用的伺服器端資料收集器，請參閱 [Data Prepper]({{site.url}}{{site.baseurl}}/data-prepper/index/)。

## 代理程式與資料匯入工具

過去以來，許多熱門的代理程式與資料匯入工具都能與 Elasticsearch OSS 搭配運作，例如 Beats、Logstash、Fluentd、FluentBit 與 OpenTelemetry。OpenSearch 的目標是持續支援廣泛的代理程式與資料匯入工具，但並非所有工具都經過測試或已明確加入 OpenSearch 相容性。

作為中繼相容性解決方案，OpenSearch 1.x 與 2.x 提供一項設定，指示叢集回傳版本 7.10.2 而非其實際版本。

如果您使用的用戶端包含版本檢查，例如 7.x 至 7.12.x 之間的 Logstash OSS 或 Filebeat OSS 版本，請啟用該設定：

```json
PUT _cluster/settings
{
  "persistent": {
    "compatibility": {
      "override_main_response_version": true
    }
  }
}
```

[如同任何其他設定]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/)，另一種做法是在每個節點的 `opensearch.yml` 中加入以下一行，然後重新啟動節點：

```yml
compatibility.override_main_response_version: true
```

Logstash OSS 8.0 導入一項重大變更：所有外掛程式預設都在 ECS 相容模式下執行。如果您使用相容的 [OSS 用戶端](#compatibility-matrices)，則必須覆寫預設值以維持舊有行為：

```yml
ecs_compatibility => disabled
```

### 下載

您可以從 [OpenSearch 下載頁面](https://opensearch.org/downloads.html)下載適用於 Logstash 的 OpenSearch output 外掛程式。該 Logstash output 外掛程式與 OpenSearch 及 Elasticsearch OSS (7.10.2 或更低版本) 相容。

以下為具 OpenSearch 相容性的最新 Beats OSS 版本。如需更多資訊，請參閱下方的相容性矩陣一節。

- [Filebeat OSS 7.12.1](https://www.elastic.co/downloads/past-releases/filebeat-oss-7-12-1)
- [Metricbeat OSS 7.12.1](https://www.elastic.co/downloads/past-releases/metricbeat-oss-7-12-1)
- [Packetbeat OSS 7.12.1](https://www.elastic.co/downloads/past-releases/packetbeat-oss-7-12-1)
- [Heartbeat OSS 7.12.1](https://elastic.co/downloads/past-releases/heartbeat-oss-7-12-1)
- [Winlogbeat OSS 7.12.1](https://www.elastic.co/downloads/past-releases/winlogbeat-oss-7-12-1)
- [Auditbeat OSS 7.12.1](https://elastic.co/downloads/past-releases/auditbeat-oss-7-12-1)

有使用者反映這些版本的 Beats 在資料匯入管線方面有相容性問題。如果您在 OpenSearch 中使用資料匯入管線，請考慮改用 7.10.2 版的 Beats。
{: .note }


## 相容性矩陣

*斜體*儲存格表示未經測試，但根據現有資訊指出該值理論上應有的結果。


### Logstash 相容性矩陣

| | Logstash OSS 7.0.0 至 7.11.x | Logstash OSS 7.12.x\* | Logstash 7.13.x-7.16.x (不含 OpenSearch output 外掛程式) | Logstash 7.13.x-7.16.x (含 OpenSearch output 外掛程式) | Logstash 8.x+ (含 OpenSearch output 外掛程式) 
| :---| :--- | :--- | :--- | :--- | :--- |
| Elasticsearch OSS 7.0.0 至 7.9.x | *是* | *是* | *否* | *是* | *是* |
| Elasticsearch OSS 7.10.2 | *是* | *是* | *否* | *是* | *是* |
| ODFE 1.0 至 1.12 | *是* | *是* | *否* | *是* | *是* |
| ODFE 1.13 | *是* | *是* | *否* | *是* | *是* |
| OpenSearch 1.x 至 2.x | 透過版本設定可支援 | 透過版本設定可支援 | *否* | *是* | 是，需使用 Elastic Common Schema 設定 |
| OpenSearch 3.x | *否* | *否* | *否* | *是* | 是，需使用 Elastic Common Schema 設定 |

\* 與 Elasticsearch OSS 相容的最新版本。


<!-- vale off -->
### Beats 相容性矩陣
<!-- vale on -->

| | Beats OSS 7.0.0 至 7.11.x\*\* | Beats OSS 7.12.x\* | Beats 7.13.x |
| :--- | :--- | :--- | :--- |
| Elasticsearch OSS 7.0.0 至 7.9.x | *是* | *是* | 否 |
| Elasticsearch OSS 7.10.2 | *是* | *是* | 否 |
| ODFE 1.0 至 1.12 | *是* | *是* | 否 |
| ODFE 1.13 | *是* | *是* | 否 |
| OpenSearch 1.x 至 2.x | 透過版本設定可支援 | 透過版本設定可支援 | 否 |
| Logstash OSS 7.0.0 至 7.11.x | *是* | *是* | *是* |
| Logstash OSS 7.12.x\* | *是* | *是* | *是* |
| Logstash 7.13.x (含 OpenSearch output 外掛程式) | *是* | *是* | *是* |

\* 與 Elasticsearch OSS 相容的最新版本。

\*\* Beats OSS 包含所有 Apache 2.0 授權的 Beats 代理程式 (即 Filebeat、Metricbeat、Auditbeat、Heartbeat、Winlogbeat 與 Packetbeat)。

OpenSearch 不支援 7.12.x 以後的 Beats 版本。如果您必須將環境中的 Beats 代理程式更新至較新版本，可以將流量從 Beats 導向 Logstash，並使用 Logstash Output 外掛程式將資料匯入 OpenSearch，以避開此不相容問題。
{: .warning }

如需記錄檔與指標收集工具的建議，請參閱[常見問題](https://opensearch.org/faq/#q1.20)。

## OpenSearch CLI

OpenSearch CLI 命令列介面 (`opensearch-cli`) 讓您能從命令列管理 OpenSearch 叢集並自動化工作。如需 OpenSearch CLI 的更多資訊，請參閱 [OpenSearch CLI]({{site.url}}{{site.baseurl}}/tools/cli/)。

## OpenSearch Kubernetes operator

OpenSearch Kubernetes Operator 是一個開放原始碼的 Kubernetes operator，可協助在容器化環境中自動化部署與供應 OpenSearch 及 OpenSearch Dashboards。如需如何使用該 operator 的資訊，請參閱 [OpenSearch Kubernetes Operator]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/operator/)。

## OpenSearch 升級、遷移與比較工具

OpenSearch 遷移工具可協助遷移至 OpenSearch，以及升級至較新版本的 OpenSearch。這些工具可協助您使用 Docker 容器在本機建立概念驗證環境，或使用一鍵部署指令碼部署至 AWS。這讓您能在遷移前更有效地微調叢集組態並管理工作負載。

如需 OpenSearch 遷移工具的更多資訊，請參閱 [OpenSearch Migration Assistant]({{site.url}}{{site.baseurl}}/migration-assistant/)。

## Sycamore 

[Sycamore](https://github.com/aryn-ai/sycamore) 是一個開放原始碼、AI 驅動的文件處理引擎，旨在使用 Python 為擷取增強生成 (RAG) 與語意搜尋準備非結構化資料。Sycamore 支援對多種複雜文件類型進行分塊與充實，包括報告、簡報、逐字稿與手冊。此外，Sycamore 可以擷取並處理內嵌元素，例如表格、圖形、圖表及其他資訊圖表。接著，它可以使用 [OpenSearch 連接器](https://sycamore.readthedocs.io/en/stable/sycamore/connectors/opensearch.html)將資料載入目標索引，包括向量索引與關鍵字索引。

如需更多資訊，請參閱 [Sycamore]({{site.url}}{{site.baseurl}}/tools/sycamore/)。
