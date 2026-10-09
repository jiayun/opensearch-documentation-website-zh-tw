---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "目標輸送量"
nav_order: 60
redirect_from:
  - /benchmark/user-guide/target-throughput/
  - /benchmark/user-guide/optimizing-benchmarks/target-throughput/
---

# 目標輸送量

目標輸送量是理解 OpenSearch Benchmark 中*延遲*定義的關鍵。目標輸送量是 OpenSearch Benchmark 發出請求的速率，並假設回應會立即傳回。`target-throughput` 是常見的工作負載參數，可為每個測試設定，並以每秒作業數為單位測量。

OpenSearch Benchmark 有兩種測試模式，兩者都與輸送量、延遲和服務時間相關：

- [基準測試模式](#benchmarking-mode)：延遲的測量方式與服務時間相同。
- [輸送量節流模式](#throughput-throttled-mode)：延遲的測量方式為服務時間加上請求在佇列中等待的時間。

## 基準測試模式

當 `target-throughput` 設為 `0` 時，OpenSearch Benchmark 延遲測試會以*基準測試模式*執行。在此模式下，OpenSearch 用戶端會以最快的速度向 OpenSearch 叢集傳送請求。叢集收到前一個請求的回應後，OpenSearch Benchmark 會立即向 OpenSearch 用戶端傳送下一個請求。在此測試模式下，延遲與服務時間相同。

OpenSearch Benchmark 對每個單一用戶端一次只發出一個請求。用戶端數量由工作負載參數中的 `search-clients` 設定決定。

## 輸送量節流模式

如果 `target-throughput` 未設為 `0`，則 OpenSearch Benchmark 會依據 `target-throughput` 發出下一個請求，並假設回應會立即傳回。

**輸送量**測量 OpenSearch Benchmark 發出請求的速率，並假設回應會立即傳回。若要設定請求速率，您可以將 `target-throughput` 工作負載參數設為每個測試所需的每秒作業數。

當您想模擬部署正式叢集時可能遇到的流量類型時，請將基準測試中的 `target-throughput` 設為您估計正式叢集可能收到的請求數量。下列範例說明 `target-throughput` 設定如何影響延遲測量。

### 範例 A

下列圖表說明在預期請求回應時間為 200 ms 且使用下列設定時，如何計算延遲：

- `search-clients` 設為 `1`。
- `target-throughput` 設為每秒 `1` 次作業。

![請求排程顯示在每秒 1 次作業下預期的 200 ms 回應時間]({{site.url}}{{site.baseurl}}/images/benchmark/latency-explanation-1.png)

當請求花費的時間超過 200 ms 時，例如請求花費 1110 ms 而非 400 ms，OpenSearch Benchmark 會在 4.10 s 傳送原本根據 `target-throughput` 應在 4.00 s 發生的下一個請求。4.10 s 請求之後的所有請求都會嘗試與 `target-throughput` 設定重新同步，如下圖所示：

![請求排程顯示延遲的請求與目標輸送量重新同步]({{site.url}}{{site.baseurl}}/images/benchmark/latency-explanation-2.png)

在測量整體延遲時，OpenSearch Benchmark 會納入所有已執行的請求。除了下列兩個請求外，所有請求的延遲皆為 200 ms：

- 持續 1100 ms 的請求。
- 原本應在 4.00 s 開始的後續請求。此請求延遲了 100 ms，以下圖中的橘色區域表示，且回應時間為 200 ms。在計算此請求的延遲時，OpenSearch Benchmark 會將延遲的開始時間納入考量，並與回應時間合併計算。此請求的延遲為 **300 ms**。

![延遲計算顯示延遲的請求合併等待時間與回應時間]({{site.url}}{{site.baseurl}}/images/benchmark/latency-explanation-3.png)

### 範例 B

在此範例中，OpenSearch Benchmark 假設延遲為 200 ms，並使用下列延遲設定：

- `search_clients` 設為 `1`。
- `target-throughput` 設為每秒 `10` 次作業。

下圖顯示 OpenSearch Benchmark 依據預期回應時間建立的排程。

![請求排程顯示目標輸送量為每秒 10 次作業且預期回應時間為 200 ms]({{site.url}}{{site.baseurl}}/images/benchmark/b-latency-explanation-1.png)

然而，如果假設所有回應的延遲都是 200 ms，那麼每秒 10 次作業將無法達成。因此，OpenSearch Benchmark 可達到的最高輸送量為每秒 5 次作業，如下圖所示。

![由於回應時間為 200 ms，實際輸送量限制為每秒 5 次作業]({{site.url}}{{site.baseurl}}/images/benchmark/b-latency-explanation-2.png)

OpenSearch Benchmark 並不會考量此限制，仍會繼續嘗試達到每秒 `target-throughput` 10 次作業的目標。因此，每個請求的延遲開始層層累積，如下圖所示。

![OpenSearch Benchmark 嘗試在超出容量時維持目標輸送量所造成的延遲層層累積]({{site.url}}{{site.baseurl}}/images/benchmark/b-latency-explanation-3.png)

將服務時間與每個作業的延遲合併計算後，每個作業會得到下列延遲測量結果：

- 作業 1 為 200 ms
- 作業 2 為 300 ms
- 作業 3 為 400 ms
- 作業 4 為 500 ms
- 作業 5 為 600 ms

此延遲累積會持續下去，每個後續請求的延遲增加 100 ms。

### 建議

如前述範例所示，您應了解每個任務的平均服務時間，並提供能將服務時間納入考量的 `target-throughput`。OpenSearch Benchmark 的延遲是根據使用者設定的 `target-throughput` 計算；因此，*延遲*可以重新定義為*以輸送量為基礎的延遲*。


