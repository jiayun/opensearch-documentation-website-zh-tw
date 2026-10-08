---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "指標彙總"
has_children: true
has_toc: false
nav_order: 2
redirect_from:
  - /opensearch/metric-agg/
  - /query-dsl/aggregations/metric-agg/
  - /aggregations/metric-agg/
  - /query-dsl/aggregations/metric/
  - /aggregations/metric/
---

# 指標彙總

指標彙總讓您能夠執行計算，例如尋找欄位的最小值、最大值和平均值。

## 指標彙總的類型

指標彙總分為兩種類型：單值指標彙總和多值指標彙總。

### 單值指標彙總

單值指標彙總會回傳單一指標，例如 `sum`、`min`、`max`、`avg`、`cardinality` 或 `value_count`。

### 多值指標彙總

多值指標彙總會回傳多個指標。這些包括 `stats`、`extended_stats`、`matrix_stats`、`percentile`、`percentile_ranks`、`geo_bound`、`top_hits` 和 `scripted_metric`。

## 支援的指標彙總

OpenSearch 支援以下指標彙總：

- [平均值]({{site.url}}{{site.baseurl}}/aggregations/metric/average/)
- [基數]({{site.url}}{{site.baseurl}}/aggregations/metric/cardinality/)
- [延伸統計]({{site.url}}{{site.baseurl}}/aggregations/metric/extended-stats/)
- [地理邊界]({{site.url}}{{site.baseurl}}/aggregations/metric/geobounds/)
- [矩陣統計]({{site.url}}{{site.baseurl}}/aggregations/metric/matrix-stats/)
- [最大值]({{site.url}}{{site.baseurl}}/aggregations/metric/maximum/)
- [最小值]({{site.url}}{{site.baseurl}}/aggregations/metric/minimum/)
- [百分位數排名]({{site.url}}{{site.baseurl}}/aggregations/metric/percentile-ranks/)
- [百分位數]({{site.url}}{{site.baseurl}}/aggregations/metric/percentile/)
- [指令碼指標]({{site.url}}{{site.baseurl}}/aggregations/metric/scripted-metric/)
- [統計]({{site.url}}{{site.baseurl}}/aggregations/metric/stats/)
- [總和]({{site.url}}{{site.baseurl}}/aggregations/metric/sum/)
- [熱門命中]({{site.url}}{{site.baseurl}}/aggregations/metric/top-hits/)
- [值計數]({{site.url}}{{site.baseurl}}/aggregations/metric/value-count/)