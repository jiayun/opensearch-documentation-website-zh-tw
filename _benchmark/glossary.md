---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "詞彙表"
nav_order: 100
---

# OpenSearch Benchmark 詞彙表

以下是 OpenSearch Benchmark 中的常用術語：

- **Corpora（語料庫）**：文件的集合。
- **Latency（延遲）**：如果停用 `target-throughput`（沒有值或值為 `0)`），延遲等於服務時間。如果啟用 `target-throughput`（值為 1 或更大），延遲等於服務時間加上請求在傳送前於佇列中等待的時間。
- **Metric keys（指標鍵）**：OpenSearch Benchmark 根據[指標記錄]({{site.url}}{{site.baseurl}}/benchmark/metrics/metric-records/)中的組態所儲存的指標。
- **Operations（操作）**：在工作負載中，由工作負載執行的 API 操作清單。
- **Pipeline（管線）**：在執行工作負載之前與之後發生、用來決定基準測試結果的一系列步驟。
- **Schedule（排程）**：執行工作負載時，依出現順序執行的兩個或多個操作的清單。
- **Service time（服務時間）**：OpenSearch Benchmark 的主要用戶端 `opensearch-py` 傳送請求並從 OpenSearch 叢集接收回應所花費的時間。其中包含伺服器處理請求所花費的時間，以及網路延遲、負載平衡器額外負荷和還原序列化／序列化所花費的時間。
- **Summary report（摘要報告）**：在測試結束時，根據工作負載中定義的指標鍵所產生的報告。
- **Test（測試）**：對 OpenSearch Benchmark 二進位檔的單次呼叫。
- **Throughput（吞吐量）**：在指定時間內完成的操作數量。
- **Workload（工作負載）**：一或多個基準測試的集合，這些測試使用特定的文件語料庫對叢集執行基準測試。文件語料庫包含工作負載執行時所呼叫的任何索引、資料檔案或操作。