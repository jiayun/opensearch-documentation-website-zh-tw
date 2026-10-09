---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "特殊搜尋欄位類型"
nav_order: 95
has_children: true
has_toc: false
parent: Supported field types
redirect_from:
  - /field-types/supported-field-types/specialized-search/
---

# 特殊搜尋欄位類型

特殊搜尋欄位類型提供進階搜尋功能與效能最佳化。

欄位資料類型 | 說明
:--- | :---
[`semantic`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/semantic/) | 包裝文字或二進位欄位，以簡化語意搜尋的設定。
[`rank_feature`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/rank/) | 提升或降低文件的相關性分數。
[`rank_features`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/rank/) | 提升或降低文件的相關性分數。用於特徵清單稀疏的情況。
[`percolator`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/percolator/) | 一種欄位，可作為反向搜尋作業的儲存查詢。
[`star_tree`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/star-tree/) | 使用星狀樹索引預先計算彙總，以提升效能。
[`derived`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/derived/) | 使用指令碼從其他欄位計算得出的動態產生欄位。