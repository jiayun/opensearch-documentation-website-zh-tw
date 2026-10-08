---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "字元篩選器"
nav_order: 90
has_children: true
has_toc: false
redirect_from:
  - /analyzers/character-filters/
---

# 字元篩選器

字元篩選器會在斷詞之前處理文字，為後續分析做好準備。

詞元篩選器處理的是詞元（單字或詞彙），字元篩選器則是在斷詞之前處理原始輸入文字。字元篩選器特別適合用來清理或轉換含有不需要字元的結構化文字，例如 HTML 標籤或特殊符號。字元篩選器可協助移除或取代這些元素，讓文字具備適當的格式以供分析。

字元篩選器的使用案例包括：

- **移除 HTML**：[`html_strip`]({{site.url}}{{site.baseurl}}/analyzers/character-filters/html-character-filter/) 字元篩選器會從內容中移除 HTML 標籤，只將純文字編製索引。
- **模式取代**：[`pattern_replace`]({{site.url}}{{site.baseurl}}/analyzers/character-filters/pattern-replace-character-filter/) 字元篩選器會取代或移除文字中不需要的字元或模式，例如將連字號轉換為空格。
- **自訂對應**：[`mapping`]({{site.url}}{{site.baseurl}}/analyzers/character-filters/mapping-character-filter/) 字元篩選器會將特定字元或序列替換為其他值，例如將貨幣符號轉換為對應的文字。
- **ICU 正規化**：[`icu_normalizer`]({{site.url}}{{site.baseurl}}/analyzers/character-filters/icu-normalization/) 字元篩選器會在斷詞之前將文字轉換為標準的 Unicode 形式，確保等價的字元能獲得一致的處理。需要 `analysis-icu` 外掛程式。
- **日文疊字記號**：[`kuromoji_iteration_mark`]({{site.url}}{{site.baseurl}}/analyzers/character-filters/kuromoji-iteration-mark/) 字元篩選器會將日文疊字記號展開為其所代表的字元，在斷詞之前將文字正規化。需要 `analysis-kuromoji` 外掛程式。
