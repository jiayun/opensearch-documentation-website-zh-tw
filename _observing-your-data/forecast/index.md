---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "預測"
nav_order: 130
has_children: true
redirect_from:
  - /observing-your-data/forecast/
---

# 預測

OpenSearch 中的預測功能會使用隨機切割森林 (Random Cut Forest, RCF) 模型，將任何時間序列欄位轉換為可自我更新的訊號。RCF 是一種線上學習模型，會隨著每個新資料點逐步更新。由於 RCF 會即時重新整理，因此能立即因應技術條件的變化，而不需要耗費大量成本的批次重新訓練。每個模型只使用少量儲存空間——通常為數百 KB——因此運算與儲存空間的額外負擔都維持在低水準。

將預測功能與 [Alerting 外掛程式]({{site.url}}{{site.baseurl}}/monitoring-plugins/alerting/) 搭配使用，即可在預測值即將超出您的閾值時收到通知。
{: .note}

## 典型使用案例

預測功能可用於下列使用案例。

| 領域 | 您預測的內容 | 營運效益 |
|--------|-------------------|---------------|
| 預測性維護 | 每部機器未來的溫度、震動或錯誤計數 | 在故障前更換零件，以避免非預期的停機。 |
| 網路預測 | 每個節點未來的輸送量、延遲或連線計數 | 提早配置頻寬，以達成服務等級協定 (SLA) 目標。 |
| 容量與成本最佳化 | 每個微服務未來的 CPU、RAM 或磁碟使用量 | 調整硬體規模並自動擴展。 |
| 財務與營運規劃 | 未來的訂單量、營收或廣告支出效率 | 讓人力配置與預算配合需求訊號。 |





