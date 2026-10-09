---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "遠端分段預熱器"
nav_order: 10
parent: Remote-backed storage
grand_parent: Availability and recovery
---

# 遠端分段預熱器
於 3.4 版推出
{: .label .label-purple }

遠端分段預熱器會預先複製合併後的分段，以減少主要分片與副本分片之間的複寫延遲。

## 遠端分段預熱器設定

遠端分段預熱器會在標準 OpenSearch 叢集設定中新增數個設定。這些設定是動態的，因此您不需要重新啟動叢集即可變更預設行為。

下表列出遠端分段預熱器所使用的設定。

|設定	| 資料類型	 | 說明	                                                                                     |
|:---	|:-----------|:-------------------------------------------------------------------------------------------------|
|`indices.replication.merges.warmer.enabled`	| 布林值    | 啟用遠端分段預熱器。預設為 `false`。                                               |
|`indices.replication.merges.warmer.max_bytes_per_sec`	| 整數    | 合併分段複寫的個別速度設定。預設為 `-1`（使用復原速度）。	 |
|`indices.replication.merges.warmer.timeout`	| 時間單位  | 控制系統將合併後的分段複寫至副本時等待的時間上限。預設為 `10`。	  |
|`indices.replication.merges.warmer.min_segment_size_threshold`	| 位元組單位	 | 設定要預熱之合併分段的最小大小閾值。預設為 `500MB`。	          |


