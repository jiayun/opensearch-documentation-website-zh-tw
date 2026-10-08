---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "合成資料產生"
nav_order: 5
has_children: true
parent: Additional features
has_toc: false
redirect_from:
  - /benchmark/features/synthetic-data-generation/
cards:
- heading: 使用索引對應產生資料
  description: 根據您的 OpenSearch 索引對應建立合成資料。
  link: /benchmark/features/synthetic-data-generation/mapping-sdg/
- heading: 使用自訂邏輯產生資料
  description: 使用您自己的指令碼或領域特定規則來建立合成資料。
  link: /benchmark/features/synthetic-data-generation/custom-logic-sdg/
more_cards:
- heading: 產生向量
  description: 產生合成稠密與稀疏向量，並提供可設定的參數，適用於擬真的 AI/ML 基準測試情境。
  link: /benchmark/features/synthetic-data-generation/generating-vectors/
tip_cards:
- heading: 提示與最佳實務
  description: 了解實用指引與最佳實務，以最佳化您的合成資料產生工作流程。
  link: /benchmark/features/synthetic-data-generation/tips/
---

# 合成資料產生
**於 2.0 版導入**
{: .label .label-purple }

OpenSearch Benchmark 提供內建的合成資料產生器，可為任何使用情境建立任何規模的資料集。它支援兩種產生方法：

* **隨機資料產生**會產生具有隨機值的欄位。這適用於壓力測試，以及評估系統在負載下的效能。
* **規則式資料產生**會依據使用者定義的規則建立資料。這有助於測試特定情境、為查詢行為進行基準測試，或模擬領域特定的模式。

## 資料產生方法

OpenSearch Benchmark 支援下列資料產生方法。

{% include cards.html cards=page.cards %}

如需進階的合成資料產生功能，請探索向量產生。

{% include cards.html cards=page.more_cards %}

## 提示與最佳實務

{% include cards.html cards=page.tip_cards %}
