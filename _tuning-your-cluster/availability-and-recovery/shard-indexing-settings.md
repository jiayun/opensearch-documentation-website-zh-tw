---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "設定"
parent: Shard indexing backpressure
nav_order: 50
grand_parent: Availability and recovery
redirect_from: 
  - /opensearch/shard-indexing-settings/
---

# 分片索引回壓設定

分片索引回壓在標準的 OpenSearch 叢集設定中新增了數個設定。這些設定是動態的，因此您無需重新啟動叢集即可變更此功能的預設行為。

## 高階控制

高階控制可讓您開啟或關閉分片索引回壓功能。

設定 | 預設 | 說明
:--- | :--- | :---
`shard_indexing_pressure.enabled` | False | 變更為 `true` 以啟用分片索引回壓。
`shard_indexing_pressure.enforced` | False | 以影子模式或強制模式執行分片索引回壓。在影子模式下（值設為 `false`），分片索引回壓會追蹤所有細部層級的指標，但不會實際拒絕任何索引請求。在強制模式下（值設為 `true`），分片索引回壓會拒絕任何可能導致叢集效能下降的請求。

## 節點層級限制

節點層級限制可讓您控制節點上的記憶體使用量。

設定 | 預設 | 說明
:--- | :--- | :---
`shard_indexing_pressure.primary_parameter.node.soft_limit` | 70% | 定義節點層級記憶體門檻的百分比，作為節點負荷的軟性指標。

## 分片層級限制

分片層級限制可讓您控制分片上的記憶體使用量。

設定 | 預設 | 說明
:--- | :--- | :---
`shard_indexing_pressure.primary_parameter.shard.min_limit` | 0.001d | 指定任何角色（協調器、主要或副本）中新分片的最小配置配額。分片索引回壓會根據分片的流量流入情況，增加或減少此配置配額。
`shard_indexing_pressure.operating_factor.lower` | 75% | 指定分片所配置記憶體配額的佔用率下限。如果分片的總記憶體使用量低於此限制，分片索引回壓會減少該分片目前配置的記憶體。
`shard_indexing_pressure.operating_factor.optimal` | 85% | 指定分片所配置記憶體配額的最佳佔用率。如果分片的總記憶體使用量達到此層級，分片索引回壓不會變更該分片目前配置的記憶體。
`shard_indexing_pressure.operating_factor.upper` | 95% | 指定分片所配置記憶體配額的佔用率上限。如果分片的總記憶體使用量高於此限制，分片索引回壓會增加該分片目前配置的記憶體。

## 效能退化因素

效能退化因素可讓您控制分片的動態效能門檻。

設定 | 預設 | 說明
:--- | :--- | :---
`shard_indexing_pressure.secondary_parameter.throughput.request_size_window` | 2,000 | 分片取樣視窗大小中的請求數量。分片索引回壓會將請求的整體效能與取樣視窗中的請求進行比較，以偵測任何效能退化。
`shard_indexing_pressure.secondary_parameter.throughput.degradation_factor` | 5x | 每單位位元組的請求退化因素。此參數決定任何延遲飆升的門檻。預設值為 5x，表示如果延遲在歷史檢視中飆升 5 倍，分片索引回壓會將其標記為效能退化。
`shard_indexing_pressure.secondary_parameter.successful_request.elapsed_timeout` | 300000 ms | 請求在叢集中擱置的時間量。此參數有助於識別任何請求卡住的情境。
`shard_indexing_pressure.secondary_parameter.successful_request.max_outstanding_requests` | 100 | 叢集中擱置請求的最大數量。

## 快取設定

快取設定可控制分片索引回壓系統使用的內部快取。

設定 | 預設 | 說明
:--- | :--- | :---
`shard_indexing_pressure.cache_store.max_size` | 200 | 分片索引壓力系統中冷儲存快取的最大大小。強制最小值為 `100`。允許的最大值為 `1000`。
