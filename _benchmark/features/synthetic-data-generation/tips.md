---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "提示與最佳做法"
nav_order: 45
parent: Synthetic data generation
grand_parent: Additional features
---

# 提示與最佳做法

下列提示可協助您有效率地產生合成資料，並在過程中監視效能。

### 視覺化產生過程

產生的 URL 會開啟 [Dask 儀表板](https://docs.dask.org/en/latest/dashboard.html)，以視覺化方式呈現資料產生過程。您可以監視每個 worker 的 CPU 與記憶體使用量，並檢視產生工作流程的 CPU 火焰圖。這有助於追蹤資源使用情況並最佳化效能，尤其是在使用[自訂 Python 模組]({{site.url}}{{site.baseurl}}/benchmark/features/synthetic-data-generation/custom-logic-sdg/)時。

### 使用預設設定

我們建議從預設的合成資料產生設定開始。下列準則可協助您選擇適當的設定，以進行有效率且可靠的合成資料產生：

* 將 worker 數量設定為**不超過負載產生主機的 CPU 數量**。
* 每個區塊使用 **10,000 份文件的區塊大小**。
* 視需要調整 `max_file_size_gb` 設定，以控制寫入每個產生檔案的資料量。
