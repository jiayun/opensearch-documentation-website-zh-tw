---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "桶彙總"
has_children: true
has_toc: false
nav_order: 3
redirect_from:
  - /opensearch/bucket-agg/
  - /query-dsl/aggregations/bucket-agg/
  - /query-dsl/aggregations/bucket/
  - /aggregations/bucket-agg/
  - /aggregations/bucket/
---

# 桶彙總

桶彙總會將文件集合分類為桶 (bucket)。桶彙總的類型決定了特定文件所屬的桶。

您可以使用桶彙總來實作分面導覽（通常以側邊欄的形式放在搜尋結果登陸頁面上），協助您的使用者篩選結果。

## 支援的桶彙總

OpenSearch 支援下列桶彙總：

- [鄰接矩陣]({{site.url}}{{site.baseurl}}/aggregations/bucket/adjacency-matrix/)
- [自動間隔日期長條圖]({{site.url}}{{site.baseurl}}/aggregations/bucket/auto-interval-date-histogram/)
- [子項]({{site.url}}{{site.baseurl}}/aggregations/bucket/children/)
- [日期長條圖]({{site.url}}{{site.baseurl}}/aggregations/bucket/date-histogram/)
- [日期範圍]({{site.url}}{{site.baseurl}}/aggregations/bucket/date-range/)
- [多樣化取樣器]({{site.url}}{{site.baseurl}}/aggregations/bucket/diversified-sampler/)
- [篩選條件]({{site.url}}{{site.baseurl}}/aggregations/bucket/filter/)
- [多重篩選條件]({{site.url}}{{site.baseurl}}/aggregations/bucket/filters/)
- [地理距離]({{site.url}}{{site.baseurl}}/aggregations/bucket/geo-distance/)
- [Geohash 網格]({{site.url}}{{site.baseurl}}/aggregations/bucket/geohash-grid/)
- [Geohex 網格]({{site.url}}{{site.baseurl}}/aggregations/bucket/geohex-grid/)
- [Geotile 網格]({{site.url}}{{site.baseurl}}/aggregations/bucket/geotile-grid/)
- [全域]({{site.url}}{{site.baseurl}}/aggregations/bucket/global/)
- [長條圖]({{site.url}}{{site.baseurl}}/aggregations/bucket/histogram/)
- [IP 範圍]({{site.url}}{{site.baseurl}}/aggregations/bucket/ip-range/)
- [缺少值]({{site.url}}{{site.baseurl}}/aggregations/bucket/missing/)
- [多重詞彙]({{site.url}}{{site.baseurl}}/aggregations/bucket/multi-terms/)
- [巢狀]({{site.url}}{{site.baseurl}}/aggregations/bucket/nested/)
- [父項]({{site.url}}{{site.baseurl}}/aggregations/bucket/parent/)
- [範圍]({{site.url}}{{site.baseurl}}/aggregations/bucket/range/)
- [罕見詞彙]({{site.url}}{{site.baseurl}}/aggregations/bucket/rare-terms/)
- [反向巢狀]({{site.url}}{{site.baseurl}}/aggregations/bucket/reverse-nested/)
- [取樣器]({{site.url}}{{site.baseurl}}/aggregations/bucket/sampler/)
- [顯著詞彙]({{site.url}}{{site.baseurl}}/aggregations/bucket/significant-terms/)
- [顯著文字]({{site.url}}{{site.baseurl}}/aggregations/bucket/significant-text/)
- [詞彙]({{site.url}}{{site.baseurl}}/aggregations/bucket/terms/)
- [可變寬度長條圖]({{site.url}}{{site.baseurl}}/aggregations/bucket/variable-width-histogram/)