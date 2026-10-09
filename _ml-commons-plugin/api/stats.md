---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "統計資料"
parent: ML Commons APIs
nav_order: 120
---

# ML Commons Stats API

Stats API 提供 ML Commons 的基本統計資料，例如執行中的任務數量。若要使用更詳細的時間序列指標監視機器學習工作流程，請參閱[監視機器學習工作流程]({{site.url}}{{site.baseurl}}/monitoring-your-cluster/metrics/getting-started/#monitoring-machine-learning-workflows)。
{: .note }

取得與任務數量相關的統計資料。 

## 端點

```json
GET /_plugins/_ml/stats
GET /_plugins/_ml/stats/{stat}
GET /_plugins/_ml/{nodeId}/stats/
GET /_plugins/_ml/{nodeId}/stats/{stat}
```

## 請求範例：取得所有節點的所有統計資料

```json
GET /_plugins/_ml/stats
```
{% include copy-curl.html %}

## 回應範例

```json
{
  "zbduvgCCSOeu6cfbQhTpnQ" : {
    "ml_executing_task_count" : 0
  },
  "54xOe0w8Qjyze00UuLDfdA" : {
    "ml_executing_task_count" : 0
  },
  "UJiykI7bTKiCpR-rqLYHyw" : {
    "ml_executing_task_count" : 0
  },
  "zj2_NgIbTP-StNlGZJlxdg" : {
    "ml_executing_task_count" : 0
  },
  "jjqFrlW7QWmni1tRnb_7Dg" : {
    "ml_executing_task_count" : 0
  },
  "3pSSjl5PSVqzv5-hBdFqyA" : {
    "ml_executing_task_count" : 0
  },
  "A_IiqoloTDK01uZvCjREaA" : {
    "ml_executing_task_count" : 0
  }
}
```

## 請求範例：取得特定節點的所有統計資料

```json
GET /_plugins/_ml/{nodeId}/stats/
```
{% include copy-curl.html %}

## 請求範例：取得特定節點的指定統計資料 

```json
GET /_plugins/_ml/{nodeId}/stats/{stat}
```
{% include copy-curl.html %}

## 請求範例：取得所有節點的指定統計資料

```json
GET /_plugins/_ml/stats/{stat}
```
{% include copy-curl.html %}




