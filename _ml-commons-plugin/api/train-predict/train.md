---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "訓練"
parent: Model APIs
grand_parent: ML Commons APIs
nav_order: 50
---

# Train API

Train API 操作會根據選取的演算法訓練模型。訓練可以同步或非同步方式進行。

## 範例請求 

下列範例使用 k-means 演算法訓練索引資料。

**以 k-means 同步訓練** 

```json
POST /_plugins/_ml/_train/kmeans
{
    "parameters": {
        "centroids": 3,
        "iterations": 10,
        "distance_type": "COSINE"
    },
    "input_query": {
        "_source": ["petal_length_in_cm", "petal_width_in_cm"],
        "size": 10000
    },
    "input_index": [
        "iris_data"
    ]
}
```
{% include copy-curl.html %}

**以 k-means 非同步訓練**

```json
POST /_plugins/_ml/_train/kmeans?async=true
{
    "parameters": {
        "centroids": 3,
        "iterations": 10,
        "distance_type": "COSINE"
    },
    "input_query": {
        "_source": ["petal_length_in_cm", "petal_width_in_cm"],
        "size": 10000
    },
    "input_index": [
        "iris_data"
    ]
}
```
{% include copy-curl.html %}

## 範例回應

**同步**

同步回應時，API 會傳回 `model_id`，可用於取得或刪除模型。

```json
{
  "model_id" : "lblVmX8BO5w8y8RaYYvN",
  "status" : "COMPLETED"
}
```

**非同步**

非同步回應時，API 會傳回 `task_id`，可用於取得或刪除任務。

```json
{
  "task_id" : "lrlamX8BO5w8y8Ra2otd",
  "status" : "CREATED"
}
```