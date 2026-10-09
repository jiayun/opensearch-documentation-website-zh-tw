---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "概念"
nav_order: 3
parent: User guide
has_toc: false
---

# OpenSearch Benchmark 概念

在開始使用 OpenSearch Benchmark 之前，建議您先了解下列概念，以便有效設計、執行及分析您的基準測試，評估 OpenSearch 在不同情境下的效能。

## 基準測試架構

下圖說明 OpenSearch Benchmark 對本機主機執行時的操作方式。

![基準測試工作流程]({{site.url}}{{site.baseurl}}/images/benchmark/osb-workflow.jpg)。

## 核心概念與定義

- **Workload**：一組或多組基準測試情境的集合，使用特定的文件語料庫對您的叢集執行基準測試。文件語料庫包含工作負載執行時所叫用的任何索引、資料檔案及操作。您可以使用 `opensearch-benchmark list workloads` 列出可用的工作負載，或在 [OpenSearch Benchmark Workloads 儲存庫](https://github.com/opensearch-project/opensearch-benchmark-workloads/) 中檢視任何隨附的工作負載。如需工作負載元素的詳細資訊，請參閱[工作負載的結構]({{site.url}}{{site.baseurl}}/benchmark/anatomy-of-a-workload/)。如需建立自訂工作負載的資訊，請參閱[建立自訂工作負載]({{site.url}}{{site.baseurl}}/benchmark/creating-custom-workloads/)。工作負載通常包含下列元件：
  - 一或多個匯入至索引的資料串流。
  - 一組在基準測試中叫用的查詢與操作。

- **Pipeline**：在工作負載執行前後發生的一連串步驟，用來決定基準測試結果。OpenSearch Benchmark 支援三種管線：
  - `from-sources`：建置並佈建 OpenSearch、執行基準測試，然後發佈結果。
  - `from-distribution`：下載 OpenSearch 發行版、佈建它、執行基準測試，然後發佈結果。
  - `benchmark-only`：預設管線。假設已有執行中的 OpenSearch 執行個體，在該執行個體上執行基準測試，然後發佈結果。

- **Test**：OpenSearch Benchmark 二進位檔的單次叫用。

## 測試概念

在每次測試結束時，OpenSearch Benchmark 會產生一份表格，彙總下列項目：

  - [處理時間](#processing-time)
  - [Took time](#took-time)
  - [服務時間](#service-time)
  - [延遲](#latency)
  - [輸送量](#throughput)

下圖說明在涉及 OpenSearch 叢集、OpenSearch 用戶端及 OpenSearch Benchmark 的請求生命週期中，如何測量表格中的每個元件。

![圖表顯示在請求生命週期中如何測量服務時間、延遲及輸送量]({{site.url}}{{site.baseurl}}/images/benchmark/concepts-diagram.png)

### OpenSearch Benchmark 與傳統用戶端-伺服器系統的差異

雖然 _輸送量_ 的定義與其他用戶端-伺服器系統一致，但在 OpenSearch Benchmark 的情境中，`service time` 與 `latency` 的定義與大多數用戶端-伺服器系統不同。下表比較 OpenSearch Benchmark 對服務時間與延遲的定義，以及用戶端-伺服器系統的常見定義。

| 指標 | 常見定義 | **OpenSearch Benchmark 定義**	|
| :--- | :--- |:--- |
| **輸送量** | 在給定時間內完成的操作數。	| 在給定時間內完成的操作數。 |
| **服務時間**	| 伺服器處理請求所花費的時間，從收到請求到傳回回應為止。它包含在伺服器端佇列中等待的時間，但_不包含_網路延遲、負載平衡器額外負荷，以及還原序列化/序列化。 | `opensearch-py` 傳送請求並從 OpenSearch 叢集接收回應所花費的時間。它包含伺服器處理請求所花費的時間，也_包含_網路延遲、負載平衡器額外負荷，以及還原序列化/序列化。  |
| **延遲** | 總時間量，包含服務時間以及請求在回應前等待的時間。 | 根據使用者設定的 `target-throughput`，請求在收到回應前等待的總時間量，加上請求傳送前發生的任何其他延遲。 |

如需 OpenSearch Benchmark 中服務時間與延遲的詳細資訊，請參閱[服務時間](#service-time)與[延遲](#latency)章節。


### 處理時間

*處理時間* 涵蓋 OpenSearch Benchmark 在請求生命週期期間執行的任何額外負荷工作，例如設定請求情境管理員，或呼叫方法將請求傳遞至 OpenSearch 用戶端。這與 *服務時間* 不同，後者只涵蓋請求傳送時與 OpenSearch 用戶端收到回應時之間的差異。

### Took time

*Took time* 測量叢集在伺服器端處理請求所花費的時間量。它不包含請求從用戶端傳輸至叢集，或回應從叢集傳輸至用戶端所花費的時間。

### 服務時間


除了擷取請求的 [took time](#took-time) 之外，OpenSearch Benchmark 無法得知 OpenSearch 處理請求需要多久時間。它會呼叫 `opensearch-py` 的函式，以便與 OpenSearch 叢集通訊。

OpenSearch Benchmark 測量 *服務時間*，也就是 `opensearch-py` 用戶端傳送請求至 OpenSearch 叢集並從其接收回應之間的時間量。與傳統的服務時間定義不同，OpenSearch Benchmark 的定義包含額外負荷，例如網路延遲、負載平衡器額外負荷，或還原序列化/序列化。下圖顯示傳統定義與 OpenSearch Benchmark 定義之間的差異。

![傳統服務時間定義與 OpenSearch Benchmark 服務時間定義的比較]({{site.url}}{{site.baseurl}}/images/benchmark/service-time.png)

### 延遲

*延遲* 測量請求在收到回應前等待的總時間，以及請求傳送前發生的任何延遲。在大多數情況下，延遲的測量方式與服務時間相同，除非您是在[輸送量節流模式]({{site.url}}{{site.baseurl}}/benchmark/user-guide/target-throughput/)下測試。在此情況下，延遲的測量方式為服務時間加上請求在佇列中等待的時間。


### 輸送量

**輸送量** 測量 OpenSearch Benchmark 發出請求的速率，假設回應會立即傳回。 



