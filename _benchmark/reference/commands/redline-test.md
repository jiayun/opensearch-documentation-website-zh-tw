---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: redline-test
nav_order: 85
parent: Command reference
grand_parent: Reference
---

# Redline 測試

`--redline-test` 命令可讓 OpenSearch Benchmark 自動判斷您的 OpenSearch 叢集在負載逐漸增加時所能處理的最大請求輸送量。它會根據即時叢集效能動態調整作用中用戶端的數量，有助於進行容量規劃並找出效能退化問題。

使用 `--redline-test` 旗標時，OpenSearch Benchmark 會執行下列步驟：

1. **用戶端初始化**：OpenSearch Benchmark 會初始化大量用戶端（預設：1,000）。您可以使用選用的 `--redline-max-clients=<int>` 旗標覆寫此值。
2. **回饋機制**：OpenSearch Benchmark 會逐步增加作用中用戶端的數量。FeedbackActor 會即時監視請求失敗情形，並據此調整用戶端數量。
3. **共用狀態協調**：OpenSearch Benchmark 使用 Python 的 multiprocessing 程式庫來管理用於處理程序間通訊的共用字典與佇列：
   - **Workers** 會建立用戶端狀態對照表，並與 WorkerCoordinatorActor 共用。
   - **WorkerCoordinatorActor** 會彙總用戶端狀態，並將其轉送至 FeedbackActor。
   - **FeedbackActor** 會增加用戶端數量，直到偵測到請求錯誤為止，接著暫停用戶端、等待 30 秒，然後繼續測試。

下圖提供 redline 測試架構的視覺化概觀。

![Redline 概觀]({{site.url}}{{site.baseurl}}/images/benchmark/osb-actor-system.png){: width="600" }


## 使用方式

若要執行 redline 測試，請使用 `run` 命令，並搭配 `--redline-test` 旗標與計時測試程序。

此測試程序使用 keyword-terms 操作定義計時工作負載。它分為兩個階段執行：

- **暖機階段**：測試會先進行一段暖機期間（`warmup-time-period`），以便在開始量測前穩定效能指標。這有助於避免冷啟動效應使結果失真。
- **量測階段**：在 `time-period` 期間，OpenSearch Benchmark 會使用指定數量的用戶端，以 `target-throughput`（每秒請求數）傳送請求。redline 測試邏輯會以此為基準調整作用中用戶端的數量，以判斷叢集的最大可持續負載。

下列計時測試程序範例會作為 redline 測試的輸入，redline 測試接著會動態調整用戶端負載，以找出您的叢集在不發生錯誤的情況下所能處理的最大請求輸送量：

```json
{
  "name": "timed-mode-test-procedure",
  "schedule": [
    {
       "operation": "keyword-terms",
       "warmup-time-period": {% raw %}{{ warmup_time | default(300) | tojson }}{% endraw %},
       "time-period": {% raw %}{{ time_period | default(900) | tojson }}{% endraw %},
       "target-throughput": {% raw %}{{ target_throughput | default(20) | tojson }}{% endraw %},
       "clients": {% raw %}{{ search_clients | default(20) }}{% endraw %}
    }
  ]
}
```
{% include copy.html %}

執行下列命令，針對您的 OpenSearch 叢集使用計時測試程序啟動 redline 測試：

```bash
opensearch-benchmark run \
  --pipeline=benchmark-only \
  --target-hosts=<your-opensearch-cluster> \
  --workload=<workload> \
  --test-procedure=timed-mode-test-procedure \
  --redline-test
```
{% include copy.html %}

## 以延遲或 CPU 為基礎的回饋

OpenSearch Benchmark 支援為每個請求設定 `timeout` 值，當請求超過指定的時間長度時便會取消該請求。您可以使用 `--client-options=timeout:<int>` 旗標設定此值。預設為 10 秒。

您可以調整此值，以定義 OpenSearch Benchmark 在 redline 測試期間應容許的最大請求延遲。例如，若要判斷您的叢集在延遲不超過 15 秒的情況下所能處理的最高負載，請將用戶端選項中的逾時設為 `15`。

除了延遲與請求錯誤監視之外，redline 測試也支援以 CPU 為基礎的回饋。這有助於避免超出叢集的安全使用率上限。

### 需求

若要在 redline 測試期間使用以 CPU 為基礎的回饋，您的設定必須符合下列需求：

- 必須設定指標儲存區。使用以記憶體為基礎的儲存區會導致下列錯誤：

  ```bash
  [ERROR] Cannot run. Error in worker_coordinator (CPU-based feedback requires a metrics store. You are using an in-memory metrics store)
  ```

- `--redline-cpu-max-usage flag` 為必要項目。此旗標用於設定測試期間每個節點允許的最大 CPU 使用率（以百分比表示）。
- 啟用以 CPU 為基礎的回饋時，會自動啟用 `node-stats` 遙測裝置。

### 行為

redline CPU 回饋迴圈的運作行為如下：

- `FeedbackActor` 會定期查詢指標儲存區，以擷取每個節點的平均 CPU 使用率。
- 若任何節點超過 `--redline-cpu-max-usage` 所設定的閾值，系統便會開始縮減規模。
- 縮減規模後，actor 會先等待一段時間，才會再次嘗試擴大規模。


## 結果

在 redline 測試期間，OpenSearch Benchmark 會提供詳細的記錄檔，內含測試期間的擴縮決策與請求失敗情形。redline 測試結束時，OpenSearch Benchmark 會記錄您的叢集在未發生請求錯誤的情況下所支援的最大用戶端數量。

下列記錄檔輸出範例表示 redline 測試偵測到 keyword-terms 操作的錯誤率為 `15%`，並判斷叢集在發生錯誤前的最大穩定用戶端負載為 `410`：

```
[WARNING] Error rate is 15.0 for operation 'keyword-terms'. Please check the logs.
Redline test finished. Maximum stable client number reached: 410
```

## 組態提示與測試行為

使用下列選用命令旗標，以進一步了解並自訂 redline 測試執行：

- `--redline-scale-step`：指定每次擴大規模反覆運算中要恢復的用戶端數量。
- `--redline-scaledown-percentage`：指定發生錯誤時要暫停的用戶端百分比。
- `--redline-post-scaledown-sleep`：指定回饋 actor 在縮減規模後，開始擴大規模前要等待的秒數。
- `--redline-max-clients`：指定 redline 測試期間允許的最大用戶端數量。若未設定，OpenSearch Benchmark 預設會使用測試程序中定義的用戶端數量。

### 以 CPU 為基礎的回饋

使用下列其他旗標來設定以 CPU 為基礎的回饋：

- `--redline-cpu-max-usage`：（必要）觸發縮減規模前，每個節點允許的最大 CPU 負載（以百分比表示）。
- `--redline-cpu-window-seconds`：計算每個節點平均 CPU 使用率的時間長度（以秒為單位）。預設為 30 秒。
- `--redline-cpu-check-interval`：CPU 使用率檢查之間的間隔（以秒為單位）。預設為 30 秒。
