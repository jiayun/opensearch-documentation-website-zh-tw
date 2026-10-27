---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "訓練"
parent: Model APIs
grand_parent: ML APIs
nav_order: 50
---

# Train API

Train API 操作會根據選取的演算法訓練模型。訓練可以同步或非同步方式進行。

## 端點

```json
POST /_plugins/_ml/_train/{algorithm}
```

## 路徑參數

下表列出可用的路徑參數。

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `algorithm` | 字串 | 要訓練的演算法名稱，例如 `kmeans`。名稱不區分大小寫。如需演算法清單，請參閱 [支援的演算法]({{site.url}}{{site.baseurl}}/ml-commons-plugin/algorithms/)。必要。 |

## 查詢參數

下表列出可用的查詢參數。所有查詢參數皆為選用。

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `async` | 布林值 | 若為 `true`，請求會以非同步方式執行並傳回任務 ID。若為 `false`，請求會在訓練完成後傳回模型 ID。預設值為 `false`。 |

## 請求本文欄位

下表列出可用的請求本文欄位。請使用 `input_index` 與 `input_query` 或 `input_data` 提供訓練資料。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `parameters` | 物件 | 演算法的超參數。可用參數取決於演算法。各演算法的參數請參閱[支援的演算法]({{site.url}}{{site.baseurl}}/ml-commons-plugin/algorithms/)。選用。 |
| `input_index` | 陣列 | 包含訓練資料的索引清單。 |
| `input_query` | 物件 | 從 `input_index` 選取訓練文件的搜尋查詢。 |
| `input_data` | 物件 | 直接以資料框形式提供的訓練資料，包含 `column_metas` 與 `rows`。 |

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