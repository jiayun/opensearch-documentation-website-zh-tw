---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "遠端分段背壓"
nav_order: 10
parent: Remote-backed storage
grand_parent: Availability and recovery
---

# 遠端分段背壓

於 2.10 版推出
{: .label .label-purple }

遠端分段背壓是一種分片層級的拒絕機制，當遠端分段儲存落後於主要分片上本機已提交的分段時，會動態拒絕編製索引請求。透過遠端分段背壓，您可以避免遠端儲存與本機主要儲存之間的落後。落後可能由緩慢或失敗的遠端儲存互動、遠端儲存節流、長時間的垃圾收集暫停或高 CPU 使用率所造成。

## 閾值

只要違反下列任一閾值，遠端分段背壓就會啟動：

- **連續失敗**：若連續失敗達 _N_ 次或以上，背壓即會啟動。_N_ 的值可在 `remote_store.segment.pressure.consecutive_failures.limit` 中設定。
- **位元組落後**：位元組落後的計算方式，是將存在於本機已提交分段中但不存在於遠端儲存中的所有檔案大小相加。若位元組落後大於 _K_ 乘以每次重新整理後上傳檔案大小（以位元組為單位）的移動平均值，背壓即會啟動。變異因子 _K_ 可在 `remote_store.segment.pressure.bytes_lag.variance_factor` 中設定。移動視窗大小可透過 `remote_store.moving_average_window_size` 設定來調整。
- **時間落後**：時間落後的計算方式，是比較最近一次本機重新整理與最近一次遠端儲存分段上傳的時間戳記。若時間落後大於 _K_ 乘以每次重新整理後上傳新分段與中繼資料檔案所需時間的移動平均值，背壓即會啟動。變異因子 _K_ 可透過 `remote_store.segment.pressure.time_lag.variance_factor` 設定來調整。移動視窗大小可透過 `remote_store.moving_average_window_size` 設定來調整。  

## 處理分段合併 

每次分段合併時，都會啟動對應的重新整理。由於此重新整理包含新的合併分段，位元組落後會瞬間飆升。為了補償這種飆升，只有在遠端儲存落後本機主要儲存超過一次重新整理時，才會評估位元組落後與時間落後。不過，由連續失敗引發的背壓無論重新整理落後（遠端儲存落後本機儲存的重新整理次數）為何都會啟動。

## 遠端分段背壓設定

遠端分段背壓在標準 OpenSearch 叢集設定中新增了數項設定。這些設定是動態的，因此您無需重新啟動叢集即可變更預設的背壓行為。 

下表列出用於啟動背壓的設定。關於閾值計算，請參閱 [閾值](#thresholds)。

|設定	|資料類型	|說明	|
|:---	|:---	|:---	|
|`remote_store.segment.pressure.enabled`	|布林值 | 啟用遠端分段背壓。預設為 `true`。 |
|`remote_store.segment.pressure.consecutive_failures.limit`	|整數 | 啟動遠端分段背壓所需的最小連續失敗次數。預設為 `5`。	|
|`remote_store.segment.pressure.bytes_lag.variance_factor`	|浮點數 | 與移動平均值搭配使用，以計算啟動遠端分段背壓之動態位元組落後閾值的變異因子。預設為 `10`。	|
|`remote_store.segment.pressure.time_lag.variance_factor`	|浮點數 	|與移動平均值搭配使用，以計算啟動遠端分段背壓之動態時間落後閾值的變異因子。預設為 `10`。	|

下表列出用於統計資料的設定。

|設定	|資料類型	|說明	|
|:---	|:---	|:---	|
| `remote_store.moving_average_window_size` | 整數 | 用於計算透過 [Remote Store Stats API]({{site.url}}{{site.baseurl}}/tuning-your-cluster/availability-and-recovery/remote-store/remote-store-stats-api/) 公開之滾動統計值的移動平均視窗大小。預設為 `20`。強制最小值為 `5`。 |

