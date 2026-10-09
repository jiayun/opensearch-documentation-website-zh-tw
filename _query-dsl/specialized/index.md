---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "特殊查詢"
has_children: true
nav_order: 60
has_toc: false
redirect_from:
  - /query-dsl/specialized/
---

# 特殊查詢

特殊查詢提供標準全文搜尋與詞彙查詢之外的進階評分、篩選與公用功能。

如需 AI 與向量搜尋查詢 (k-NN、Neural、Neural sparse、Agentic、Template)，請參閱 [AI 與向量搜尋查詢]({{site.url}}{{site.baseurl}}/query-dsl/ai-vector-search/)。

| 查詢類型 | 說明 |
| :--- | :--- |
| [`distance_feature`]({{site.url}}{{site.baseurl}}/query-dsl/specialized/distance-feature/) | 根據原點與文件 `date`、`date_nanos` 或 `geo_point` 欄位之間動態計算的距離來計算文件分數。此查詢可以略過不具競爭力的命中結果。 |
| [`more_like_this`]({{site.url}}{{site.baseurl}}/query-dsl/specialized/more-like-this/) | 尋找與所提供文字、文件或文件集合相似的文件。 |
| [`percolate`]({{site.url}}{{site.baseurl}}/query-dsl/specialized/percolate/) | 尋找符合所提供文件的查詢 (以文件形式儲存)。 |
| [`rank_feature`]({{site.url}}{{site.baseurl}}/query-dsl/specialized/rank-feature/) | 根據數值特徵的值計算分數。此查詢可以略過不具競爭力的命中結果。 |
| [`script`]({{site.url}}{{site.baseurl}}/query-dsl/specialized/script/) | 使用指令碼作為篩選條件。 |
| [`script_score`]({{site.url}}{{site.baseurl}}/query-dsl/specialized/script-score/) | 使用指令碼為符合的文件計算自訂分數。 |
| [`wrapper`]({{site.url}}{{site.baseurl}}/query-dsl/specialized/wrapper/) | 接受以 JSON 或 YAML 字串表示的其他查詢。 |
