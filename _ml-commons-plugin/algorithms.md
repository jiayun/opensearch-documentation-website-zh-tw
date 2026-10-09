---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "支援的演算法"
has_children: false
nav_order: 100
---

# 支援的演算法

OpenSearch 提供內建的機器學習 (ML) 演算法，這些演算法可在您的叢集內原生執行，用於異常偵測、分群及預測分析等工作。這些演算法可讓您直接在 OpenSearch 中分析資料，無需外部 ML 模型或服務。每種演算法都針對特定使用案例進行最佳化，從偵測指標中的異常模式，到將相似的資料點分組在一起。

## 常見限制

除了 Localization 演算法之外，以下所有演算法都只支援從索引擷取 10,000 份文件作為輸入。

## K-means

K-means 是一種簡單且熱門的非監督式分群 ML 演算法，建構於 [Tribuo](https://tribuo.org/) 程式庫之上。K-means 會隨機選擇質心，然後反覆計算以最佳化質心的位置，直到每個觀測值都屬於平均值最接近的叢集為止。

### 參數

參數 | 類型   | 說明 | 預設值
:--- |:--- | :--- | :---
`centroids` | 整數 | 將產生的資料分組的叢集數量 | `2` 
`iterations` | 整數 | 對資料執行的迭代次數，直到產生平均值為止 | `10`
`distance_type` | 列舉，例如 `EUCLIDEAN`、`COSINE` 或 `L1` | 用於測量質心之間距離的測量類型 | `EUCLIDEAN`

### 支援的 API

* [Train]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/train-predict/train/)
* [Predict]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/train-predict/predict/)
* [Train and predict]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/train-predict/train-and-predict/)

### 範例

以下範例使用 Iris Data 索引以同步方式訓練 k-means。 

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

### 限制

訓練程序支援多執行緒，但執行緒數量必須少於 CPU 數量的一半。

## 線性迴歸

線性迴歸會對應輸入與輸出之間的線性關係。在 ML Commons 中，線性迴歸演算法採用自公開機器學習程式庫 [Tribuo](https://tribuo.org/)，該程式庫提供多維線性迴歸模型。此模型在訓練中支援線性最佳化器，包括 Linear Decay、SQRT_DECAY、[ADA](https://www.jmlr.org/papers/volume12/duchi11a/duchi11a.pdf)、[ADAM](https://tribuo.org/learn/4.2/javadoc/org/tribuo/math/optimisers/Adam.html) 及 [RMS_PROP](https://tribuo.org/learn/4.2/javadoc/org/tribuo/math/optimisers/RMSProp.html) 等熱門方法。

**支援的最佳化器：**[SIMPLE_SGD](https://tribuo.org/learn/4.2/javadoc/org/tribuo/math/optimisers/SGD.html#:~:text=learning%20rate%20SGD.-,getSimpleSGD,-public%20static%C2%A0)、[LINEAR_DECAY_SGD](https://tribuo.org/learn/4.2/javadoc/org/tribuo/math/optimisers/SGD.html#:~:text=linear%20decay%20SGD.-,getLinearDecaySGD,-public%20static%C2%A0)、[SQRT_DECAY_SGD](https://tribuo.org/learn/4.2/javadoc/org/tribuo/math/optimisers/SGD.html#:~:text=sqrt%20decay%20SGD.-,getSqrtDecaySGD,-public%20static%C2%A0)、[ADA_GRAD](https://tribuo.org/learn/4.2/javadoc/org/tribuo/math/optimisers/AdaGrad.html)、[ADA_DELTA](https://tribuo.org/learn/4.1/javadoc/org/tribuo/math/optimisers/AdaDelta.html)、[ADAM](https://tribuo.org/learn/4.1/javadoc/org/tribuo/math/optimisers/Adam.html) 及 [RMS_PROP](https://tribuo.org/learn/4.1/javadoc/org/tribuo/math/optimisers/RMSProp.html)。  
**支援的目標函式：**[ABSOLUTE_LOSS](https://tribuo.org/learn/4.2/javadoc/org/tribuo/regression/sgd/objectives/AbsoluteLoss.html)、[HUBER](https://tribuo.org/learn/4.2/javadoc/org/tribuo/regression/sgd/objectives/Huber.html) 及 [SQUARED_LOSS](https://tribuo.org/learn/4.2/javadoc/org/tribuo/regression/sgd/objectives/SquaredLoss.html)。  
**支援的 momentum_type：**[STANDARD](https://tribuo.org/learn/4.2/javadoc/org/tribuo/math/optimisers/SGD.Momentum.html#STANDARD:~:text=No%20momentum.-,STANDARD,-public%20static%20final) 及 [NESTEROV](https://tribuo.org/learn/4.2/javadoc/org/tribuo/math/optimisers/SGD.Momentum.html#STANDARD:~:text=Standard%20momentum.-,NESTEROV,-public%20static%20final)。  

### 參數

參數 | 類型   | 說明 | 預設值
:--- |:--- | :--- | :---
`target` | 字串 | 要預測的目標變數名稱。用於識別模型在訓練期間將學習預測哪個特徵。 | `NA`
`learning_rate` | Double | 迭代最佳化演算法中使用的初始步長。 | `0.01`
`momentum_factor` | Double | 加快權重調整速率的額外權重因子。這有助於讓最小化程序脫離局部最小值。  | `0`
`epsilon` | Double | 用於穩定梯度反轉的值。 | `1.00E-06`
`beta1` | Double | 動差估計的指數衰減率。 |  `0.9`
`beta2` | Double | 動差估計的指數衰減率。 |  `0.99`
`decay_rate` | Double | 均方根傳播 (RMSProp)。 | `0.9`
`momentum_type` | 字串 | 所定義的隨機梯度下降 (SGD) 動量類型，有助於將梯度向量朝正確方向加速，進而快速收斂。| `STANDARD`
`optimiser` | 字串 | 模型中使用的最佳化器。 | `ADA_GRAD`
`objective` | 字串 | 所使用的目標函式。 | `SQUARED_LOSS` 
`epochs` | 整數 | 迭代次數。 | `5`|
`batch_size` | 整數 | 最小批次大小。 | `1`
`logging_interval` | 整數 | 訓練迭代期間的記錄頻率。設為 `-1` 可停用記錄。 | `-1`
`seed` | Long | 用於產生可重現結果的隨機種子。控制亂數產生器的初始化。 | `12345`



### 支援的 API

* [Train]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/train-predict/train/)
* [Predict]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/train-predict/predict/)

### 範例

以下範例會根據先前訓練的線性迴歸模型建立新的預測。

#### 範例請求

```json
POST _plugins/_ml/_predict/LINEAR_REGRESSION/ROZs-38Br5eVE0lTsoD9
{
  "parameters": {
    "target": "price"
  },
  "input_data": {
    "column_metas": [
      {
        "name": "A",
        "column_type": "DOUBLE"
      },
      {
        "name": "B",
        "column_type": "DOUBLE"
      }
    ],
    "rows": [
      {
        "values": [
          {
            "column_type": "DOUBLE",
            "value": 3
          },
          {
            "column_type": "DOUBLE",
            "value": 5
          }
        ]
      }
    ]
  }
}
```

#### 範例回應

```json
{
  "status": "COMPLETED",
  "prediction_result": {
    "column_metas": [
      {
        "name": "price",
        "column_type": "DOUBLE"
      }
    ],
    "rows": [
      {
        "values": [
          {
            "column_type": "DOUBLE",
            "value": 17.25701855310131
          }
        ]
      }
    ]
  }
}
```

### 限制

ML Commons 僅支援線性隨機梯度訓練器或最佳化器，無法有效映射訓練資料中的非線性關係。在搭配複雜資料集使用時，線性隨機訓練器可能會導致收斂問題與不準確的結果。

## RCF

[Random Cut Forest](https://github.com/aws/random-cut-forest-by-aws) (RCF) 是一種機率資料結構，主要用於非監督式異常偵測，也可延伸應用於密度估計與預測。OpenSearch 利用 RCF 進行異常偵測。ML Commons 支援兩種適用於不同使用情境的 RCF 新變體：

* Batch RCF：偵測非時間序列資料中的異常。
* Fixed in time (FIT) RCF：偵測時間序列資料中的異常。

### 參數

RCF 支援下列參數。

#### Batch RCF

參數 | 類型   | 說明 | 預設值
:--- |:--- | :--- | :---
`number_of_trees` | 整數 | 森林中的樹木數量。 | `30`
`sample_size` | 整數 | 森林中串流取樣器所使用的樣本大小。 | `256`
`output_after` | 整數 | 串流取樣器在傳回結果前所需的點數。 | `32`
`training_data_size` | 整數 | 訓練資料的大小。 | 資料集大小
`anomaly_score_threshold` | double | 異常分數的門檻值。 | `1.0` 

#### Fit RCF

除 `time_field` 外，所有參數皆為選用。

參數 | 類型   | 說明 | 預設值
:--- |:--- | :--- | :---
`number_of_trees` | 整數 | 森林中的樹木數量。 | `30`
`shingle_size` | 整數 | Shingle，即最近記錄的連續序列。 | `8`
`sample_size` | 整數 | 森林中串流取樣器所使用的樣本大小。 | `256`
`output_after` | 整數 | 串流取樣器在傳回結果前所需的點數。 | `32`
`time_decay` | double | 森林中串流取樣器所使用的衰減因子。 | `0.0001` 
`anomaly_rate` | double | 異常率。 | `0.005`
`time_field` | 字串 | (**必要**) RCF 用作時間序列資料的時間欄位。 | N/A
`date_format` | 字串 | `time_field` 欄位的日期與時間格式。 | `yyyy-MM-ddHH:mm:ss`
`time_zone` | 字串 | `time_field` 欄位的時區。 | `UTC` 


### 支援的 API

* [Train]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/train-predict/train/)
* [Predict]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/train-predict/predict/)
* [Train and predict]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/train-predict/train-and-predict/)

### 限制

對於 FIT RCF，您可以使用歷史資料訓練模型，並將訓練好的模型儲存在索引中。使用 Predict API 時，該模型會被還原序列化並預測新的資料點。然而，索引中的模型不會以新資料重新整理，因為模型是固定於某個時間點的。

## RCF Summarize

RCF Summarize 是一種以 Clustering Using Representatives (CURE) 演算法為基礎的分群演算法。相較於使用隨機迭代進行分群的 [k-means](#k-means)，RCF Summarize 使用階層式分群技術。此演算法一開始會選取一組數量大於質心真實分布的隨機質心。在迭代過程中，彼此過於接近的質心對會自動合併。因此，質心數量 (`max_k`) 會收斂至符合真實分布的合理叢集數量，而非固定的 `k` 個叢集。  

### 參數

| 參數 | 類型 | 說明 | 預設值 |
|---|---|---|---|
| `max_k` | 整數 | 允許的質心數量上限。 | 2 |
| `distance_type` | 字串。有效值為 `EUCLIDEAN`、`L1`、`L2` 和 `LInfinity` | 用於測量質心之間距離的測量類型。 | `EUCLIDEAN` |

### 支援的 API

* [Train]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/train-predict/train/)
* [Predict]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/train-predict/predict/)
* [Train and predict]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/train-predict/train-and-predict/)

### 範例：Train and predict

下列範例會估計叢集中心，並為給定資料框中的每個樣本提供叢集標籤。

#### 範例請求

```json
POST _plugins/_ml/_train_predict/RCF_SUMMARIZE
{
  "parameters": {
    "centroids": 3,
    "max_k": 15,
    "distance_type": "L2"
  },
  "input_data": {
    "column_metas": [
      {
        "name": "d0",
        "column_type": "DOUBLE"
      },
      {
        "name": "d1",
        "column_type": "DOUBLE"
      }
    ],
    "rows": [
      {
        "values": [
          {
            "column_type": "DOUBLE",
            "value": 6.2
          },
          {
            "column_type": "DOUBLE",
            "value": 3.4
          }
        ]
      }
    ]
  }
}
```

#### 範例回應

預測結果中的 `rows` 參數已因長度而經過修改。在您的回應中，回應本文應包含更多列與欄。

```json
{
  "status": "COMPLETED",
  "prediction_result": {
    "column_metas": [
      {
        "name": "ClusterID",
        "column_type": "INTEGER"
      }
    ],
    "rows": [
      {
        "values": [
          {
            "column_type": "DOUBLE",
            "value": 0
          }
        ]
      }
    ]
  }
}
```
  

## Localization 

Localization 演算法會為彙總資料 (例如，隨時間彙總的資料) 找出子集層級的資訊，以呈現感興趣的活動，例如尖峰、驟降、變化或異常。Localization 可應用於不同情境，例如資料探索或根本原因分析，以找出驅動彙總資料中感興趣活動的貢獻因素。

### 參數

除 `filter_query` 和 `anomaly_start` 外，所有參數皆為必要。

參數 | 類型   | 說明 | 預設值
:--- | :--- | :--- | :---
`index_name` | 字串 | 要分析的資料集合。 | N/A
`attribute_field_names` | 串列 | 實體鍵的欄位。 | N/A
`aggregations` | 串列  | 值的欄位與彙總。 | N/A
`time_field_name` | 字串 | 時間戳記欄位。 | `null`
`start_time` | Long | 時間範圍的起點。 | `0` 
`end_time` | Long | 時間範圍的終點。 | `0`
`min_time_interval` | Long | 分析的最小時間間隔/尺度。 | `0`
`num_outputs` | 整數 | 定位/切割所產生的值數量上限。 | `0`
`filter_query` | Long | (選用) 縮減用於分析的資料集合。 | N/A
anomal`y_star | 時間單位 | (選用) 資料在此時間之後將被分析。 | N/A

### 範例：執行 localization

下列範例會對 RCA 索引執行 Localization。

#### 範例請求

```bash
POST /_plugins/_ml/_execute/anomaly_localization
{
  "index_name": "rca-index",
  "attribute_field_names": [
    "attribute"
  ],
  "aggregations": [
    {
      "sum": {
        "sum": {
          "field": "value"
        }
      }
    }
  ],
  "time_field_name": "timestamp",
  "start_time": 1620630000000,
  "end_time": 1621234800000,
  "min_time_interval": 86400000,
  "num_outputs": 10
}
```

#### 回應範例

每次演算法在指定的時間區間內執行時，API 都會回應每個彙總的貢獻值與基礎值總和。

```json
{
  "results" : [
    {
      "name" : "sum",
      "result" : {
        "buckets" : [
          {
            "start_time" : 1620630000000,
            "end_time" : 1620716400000,
            "overall_aggregate_value" : 65.0
          },
          {
            "start_time" : 1620716400000,
            "end_time" : 1620802800000,
            "overall_aggregate_value" : 75.0,
            "entities" : [
              {
                "key" : [
                  "attr0"
                ],
                "contribution_value" : 1.0,
                "base_value" : 2.0,
                "new_value" : 3.0
              },
              {
                "key" : [
                  "attr1"
                ],
                "contribution_value" : 1.0,
                "base_value" : 3.0,
                "new_value" : 4.0
              },
              {
                ...
              },
             {
                "key" : [
                  "attr8"
                ],
                "contribution_value" : 6.0,
                "base_value" : 10.0,
                "new_value" : 16.0
              },
              {
                "key" : [
                  "attr9"
                ],
                "contribution_value" : 6.0,
                "base_value" : 11.0,
                "new_value" : 17.0
              }
            ]
          }
        ]
      }
    }
  ]
}
```  

### 限制

Localization 演算法只能直接執行。因此，它無法與 ML Commons Train 和 Predict API 搭配使用。

## 邏輯迴歸

邏輯迴歸是一種分類演算法，它會根據輸入變數建立離散結果的機率模型。在 ML Commons 中，這些分類包含二元與多類別。最常見的是二元分類，它取兩個值，例如「真/假」或「是/否」，並根據指定的值預測結果。或者，多類別輸出可以依類型將不同的輸入分類。這使得邏輯迴歸最適合用於您想判斷輸入最適合歸入哪個指定類別的情況。

**支援的最佳化器：**[SIMPLE_SGD](https://tribuo.org/learn/4.2/javadoc/org/tribuo/math/optimisers/SGD.html#:~:text=learning%20rate%20SGD.-,getSimpleSGD,-public%20static%C2%A0)、[LINEAR_DECAY_SGD](https://tribuo.org/learn/4.2/javadoc/org/tribuo/math/optimisers/SGD.html#:~:text=linear%20decay%20SGD.-,getLinearDecaySGD,-public%20static%C2%A0)、[SQRT_DECAY_SGD](https://tribuo.org/learn/4.2/javadoc/org/tribuo/math/optimisers/SGD.html#:~:text=sqrt%20decay%20SGD.-,getSqrtDecaySGD,-public%20static%C2%A0)、[ADA_GRAD](https://tribuo.org/learn/4.2/javadoc/org/tribuo/math/optimisers/AdaGrad.html)、[ADA_DELTA](https://tribuo.org/learn/4.1/javadoc/org/tribuo/math/optimisers/AdaDelta.html)、[ADAM](https://tribuo.org/learn/4.1/javadoc/org/tribuo/math/optimisers/Adam.html) 與 [RMS_PROP](https://tribuo.org/learn/4.1/javadoc/org/tribuo/math/optimisers/RMSProp.html)。
**支援的目標函式：**[HINGE](https://tribuo.org/learn/4.2/javadoc/org/tribuo/classification/sgd/objectives/Hinge.html) 與 [LOGMULTICLASS](https://tribuo.org/learn/4.2/javadoc/org/tribuo/classification/sgd/objectives/LogMulticlass.html)。  
**支援的動量類型：**[STANDARD](https://tribuo.org/learn/4.2/javadoc/org/tribuo/math/optimisers/SGD.Momentum.html#STANDARD:~:text=No%20momentum.-,STANDARD,-public%20static%20final) 與 [NESTEROV](https://tribuo.org/learn/4.2/javadoc/org/tribuo/math/optimisers/SGD.Momentum.html#STANDARD:~:text=Standard%20momentum.-,NESTEROV,-public%20static%20final)。  

### 參數

| 參數 | 類型 | 說明 | 預設值 |
|---|---|---|---|
| `learning_rate` | Double | 迭代最佳化演算法中使用的初始步長。 | `1` |
| `momentum_factor` | Double | 用於加速權重調整速率的額外權重因子。這有助於將最小化程序帶離局部最小值。 | `0` |
| `epsilon` | Double | 用於穩定梯度反轉的值。 | `0.1` |
| `beta1` | Double | 矩估計的指數衰減率。 | `0.9` |
| `beta2` | Double | 矩估計的指數衰減率。 | `0.99` |
| `decay_rate` | Double | 均方根傳播 (RMSProp)。 | `0.9` |
| `momentum_type` | 字串 | 隨機梯度下降 (SGD) 動量，有助於將梯度向量朝正確方向加速，從而快速收斂。 | `STANDARD` |
| `optimiser` | 字串 | 模型中使用的最佳化器。  | `ADA_GRAD` |
| `target` | 字串 | 目標欄位。 | null |
| `objective` | 字串 | 目標函式類型。 | `LOGMULTICLASS` |
| `epochs` | 整數 | 迭代次數。 | `5` |
| `batch_size` | 整數 | 最小批次大小。 | `1` |
| `logging_interval` | 整數 | 多次迭代後遺失記錄的間隔。如果演算法不含記錄，則間隔為 `1`。 | `1000` |

### 支援的 API

* [Train]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/train-predict/train/)
* [Predict]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/train-predict/predict/)

### 範例：使用 Iris 資料進行 Train/Predict

下列範例會在 OpenSearch 中使用 [Iris 資料集](https://en.wikipedia.org/wiki/Iris_flower_data_set)建立索引，然後使用邏輯迴歸訓練資料。最後，它會使用訓練好的模型逐列預測 Iris 類型。

#### 建立 Iris 索引

使用此請求之前，請確認您已下載 [Iris 資料](https://archive.ics.uci.edu/dataset/53/iris)。

```bash
PUT /iris_data
{
  "mappings": {
    "properties": {
      "sepal_length_in_cm": {
        "type": "double"
      },
      "sepal_width_in_cm": {
        "type": "double"
      },
      "petal_length_in_cm": {
        "type": "double"
      },
      "petal_width_in_cm": {
        "type": "double"
      },
      "class": {
        "type": "keyword"
      }
    }
  }
}
```

#### 從 IRIS_data.txt 匯入資料

```bash
POST _bulk
{ "index" : { "_index" : "iris_data" } }
{"sepal_length_in_cm":5.1,"sepal_width_in_cm":3.5,"petal_length_in_cm":1.4,"petal_width_in_cm":0.2,"class":"Iris-setosa"}
{ "index" : { "_index" : "iris_data" } }
{"sepal_length_in_cm":4.9,"sepal_width_in_cm":3.0,"petal_length_in_cm":1.4,"petal_width_in_cm":0.2,"class":"Iris-setosa"}
...
...
```

#### 訓練邏輯迴歸模型

此範例使用多類別邏輯迴歸分類方法。在此，使用花萼與花瓣的長度和寬度作為輸入來訓練模型，以根據 `class` 對質心進行分類，如 `target` 參數所指定。

**請求**

```bash
{
  "parameters": {
    "target": "class"
  },
  "input_query": {
    "query": {
      "match_all": {}
    },
    "_source": [
      "sepal_length_in_cm",
      "sepal_width_in_cm",
      "petal_length_in_cm",
      "petal_width_in_cm",
      "class"
    ],
    "size": 200
  },
  "input_index": [
    "iris_data"
  ]
}
```

#### 範例回應

`model_id` 將用於預測 Iris 的類別。

```json
{
  "model_id" : "TOgsf4IByBqD7FK_FQGc",
  "status" : "COMPLETED"
}
```

#### 預測結果

使用已訓練 Iris 資料集的 `model_id`，邏輯迴歸將根據輸入資料預測 Iris 的類別。

```bash
POST _plugins/_ml/_predict/logistic_regression/SsfQaoIBEoC4g4joZiyD
{
  "parameters": {
    "target": "class"
  },
  "input_data": {
    "column_metas": [
      {
        "name": "sepal_length_in_cm",
        "column_type": "DOUBLE"
      },
      {
        "name": "sepal_width_in_cm",
        "column_type": "DOUBLE"
      },
      {
        "name": "petal_length_in_cm",
        "column_type": "DOUBLE"
      },
      {
        "name": "petal_width_in_cm",
        "column_type": "DOUBLE"
      }
    ],
    "rows": [
      {
        "values": [
          {
            "column_type": "DOUBLE",
            "value": 6.2
          },
          {
            "column_type": "DOUBLE",
            "value": 3.4
          },
          {
            "column_type": "DOUBLE",
            "value": 5.4
          },
          {
            "column_type": "DOUBLE",
            "value": 2.3
          }
        ]
      },
      {
        "values": [
          {
            "column_type": "DOUBLE",
            "value": 5.9
          },
          {
            "column_type": "DOUBLE",
            "value": 3.0
          },
          {
            "column_type": "DOUBLE",
            "value": 5.1
          },
          {
            "column_type": "DOUBLE",
            "value": 1.8
          }
        ]
      }
    ]
  }
}
```

#### 範例回應

```json
{
  "status" : "COMPLETED",
  "prediction_result" : {
    "column_metas" : [
      {
        "name" : "result",
        "column_type" : "STRING"
      }
    ],
    "rows" : [
      {
        "values" : [
          {
            "column_type" : "STRING",
            "value" : "Iris-virginica"
          }
        ]
      },
      {
        "values" : [
          {
            "column_type" : "STRING",
            "value" : "Iris-virginica"
          }
        ]
      }
    ]
  }
}
```

### 限制

Tribuo 的訓練器並未內建收斂指標。因此，ML Commons 無法透過 ML Commons API 指出收斂狀態。

## 指標關聯

指標關聯功能是 OpenSearch 2.7 推出的實驗性功能。它無法用於正式環境。若要針對改善此功能提供意見回饋，請在 [ML Commons 儲存庫](https://github.com/opensearch-project/ml-commons) 中建立問題。
{: .warning }

指標關聯演算法會在一組指標資料中找出事件。此演算法將事件定義為一段時間範圍，在此期間內多個指標同時顯示異常行為。當給定一組指標時，此演算法會計算發生的事件數量、每個事件發生的時間，並判斷每個事件涉及哪些指標。

若要啟用指標關聯演算法，請更新下列叢集設定：

```json
PUT /_cluster/settings
{
  "persistent" : {
    "plugins.ml_commons.enable_inhouse_python_model": true
  }
}
```

### 參數

若要使用指標關聯演算法，請包含下列參數。

| 參數 | 類型 | 說明 | 預設值 |
|---|---|---|---|
`metrics` | 陣列 | 時間序列中可與異常行為關聯的指標清單 | N/A

### 輸入

指標關聯的輸入是 M x T 的指標資料陣列，其中 M 是指標數量，T 是每個個別指標值序列的長度。

將指標輸入演算法時，請假設下列事項：

1. 對於每個指標，輸入序列的長度皆相同，為 T。
2. 所有輸入指標都應有相同的對應時間戳記集合。
3. 資料點總數為 M * T <= 10000。

### 範例：簡單指標關聯

下列範例將指標數量 (M) 輸入為 3，並將時間步數 (T) 輸入為 128：

```json
POST /_plugins/_ml/_execute/METRICS_CORRELATION
{"metrics": [[-1.1635416, -1.5003631, 0.46138194, 0.5308311, -0.83149344, -3.7009873, -3.5463789, 0.22571462, -5.0380244, 0.76588845, 1.236113, 1.8460795, 1.7576948, 0.44893077, 0.7363948, 0.70440894, 0.89451003, 4.2006273, 0.3697659, 2.2458954, -2.302939, -1.7706926, 1.7445002, -1.5246059, 0.07985192, -2.7756078, 1.0002468, 1.5977372, 2.9152713, 1.4172368, -0.26551363, -2.2883027, 1.5882446, 2.0145164, 3.4862874, -1.2486862, -2.4811826, -0.17609037, -2.1095612, -1.2184235, 0.63118523, -1.8909532, 2.039797, -0.5317177, -2.2922578, -2.0179775, -0.07992507, -0.12554549, -0.2553092, 1.1450123, -0.4640453, -2.190223, -4.671612, -1.5076426, 1.635445, -1.1394824, -0.7503817, 0.98424894, -0.38896716, 1.0328646, 1.9543738, -0.5236269, 0.14298044, 3.2963762, 8.1641035, 5.717064, 7.4869685, 2.5987444, 11.018798, 9.151356, 5.7354255, 6.862203, 3.0524514, 4.431755, 5.1481285, 7.9548607, 7.4519925, 6.09533, 7.634116, 8.898271, 3.898491, 9.447067, 8.197385, 5.8284273, 5.804283, 7.7688456, 10.574343, 7.5679493, 7.1888094, 7.1107903, 8.454468, 8.066334, 8.83665, 7.11204, 4.4898267, 8.614764, 6.336754, 11.577503, 3.3998494, 9.501525, 13.17289, 6.1116023, 5.143777, 2.7813284, 3.7917604, 7.1683135, 7.627272, 7.290255, 3.1299121, 7.089733, 9.140584, 8.844729, 9.403275, 10.220029, 8.039719, 8.85549, 4.034555, 4.412663, 7.54451, 7.2116737, 4.6346946, 7.0044127, 9.7557, 10.982841, 5.897937, 6.870126, 3.5638695, 5.7872133], [1.3037996, 2.7976995, -0.12042701, 1.3688855, 1.6955005, -2.2575269, 0.080582514, 3.011721, -0.4320283, 3.2440786, -1.0321085, 1.2346085, -2.3152106, -0.9783513, 0.6837618, 1.5320586, -1.6148578, -0.94538075, 0.55978125, -4.7430468, 3.466028, 2.3792691, 1.3269067, -0.35359794, -1.5547276, 0.5202475, 1.0269136, -1.7531714, 0.43987304, -0.18845831, 2.3086758, 2.519588, 2.0116413, 0.019745048, -0.010070452, 2.496933, 1.1557871, 0.08433053, 1.375894, -1.2135965, -1.2588277, -0.31454003, 0.045949124, -1.7518936, -2.3533764, -2.0125146, 0.10255043, 1.1782314, 2.4579153, -0.8780899, -4.1442213, 3.8300152, 2.772975, 2.6803262, 0.9867382, 0.77618766, 0.46541777, 3.8959959, -2.1713195, 0.10609512, -0.26438138, -2.145317, 3.6734529, 1.4830295, -5.3445525, -10.6427765, -8.300354, -1.9608921, -6.6779685, -10.019544, -8.341513, -9.607174, -7.2441607, -3.411102, -6.180552, -8.318714, -6.060591, -7.790343, -5.9695, -7.9429936, -3.775652, -5.2827606, -3.7168224, -6.729588, -9.761094, -7.4683576, -7.2595067, -6.6790915, -9.832726, -8.352172, -6.936336, -8.252518, -6.787475, -9.091013, -11.465944, -6.712504, -8.987438, -6.946672, -8.877166, -6.7854185, -3.6417139, -6.1036086, -5.360772, -4.0435786, -4.5864973, -6.971063, -10.522461, -6.3692527, -4.387658, -9.723745, -4.7020173, -5.097396, -9.903703, -4.882414, -4.1999683, -6.7829437, -6.2555966, -8.121125, -5.334131, -9.174302, -3.9752126, -4.179469, -8.335524, -9.359406, -6.4938803, -6.794677, -8.382997, -9.879416], [1.8792984, -3.1561708, -0.8443318, -1.998743, -0.6319316, 2.4614046, -0.44511616, 0.82785237, 1.7911717, -1.8172283, 0.46574894, -1.8691323, 3.9586513, 0.8078605, 0.9049874, 5.4086914, -0.7425967, -0.20115769, -1.197923, 2.741789, 0.85432875, -1.1688408, -1.7771784, 1.615249, -4.1103697, 0.4721327, -2.75669, -0.38393462, -3.1137516, -2.2572582, 0.9580673, -3.7139492, -0.68303126, 1.6007807, 0.6313973, -2.5115106, 0.703251, 2.4844077, -1.7405633, -3.007687, 2.372802, 2.4684637, 0.6443977, -3.1433117, 0.05976736, -1.9809214, 3.514713, 2.1880944, 1.242541, 1.8236228, 0.8642841, -0.17313614, 1.7042321, 0.8298376, 4.2443194, 0.13983983, 1.1940852, 2.5076652, 39.285202, 82.73858, 44.707516, -4.267148, 0.25930226, 0.20799652, -3.7213502, 1.475217, -1.2394199, -0.0034497892, 1.1413965, 55.18923, -2.2969518, -4.1400924, -2.4707043, 43.193188, -0.19258368, 3.471275, 1.1374166, 1.2147579, 4.13017, -2.0576499, 2.1529694, -0.28360432, 0.8477302, -0.63012695, 1.2569811, 1.943168, 0.17070436, 3.2358394, -2.3737662, 0.77060974, 4.99065, 3.1079204, 3.6347675, 0.6801177, -2.2205186, 1.0961101, -2.4445753, -2.0919478, -2.895031, 2.5458927, 0.38599384, 1.0492333, -0.081834644, -7.4079595, -2.1785216, -0.7277175, -2.7413428, -3.2083786, 3.2958643, -1.1839997, 5.4849496, 2.0259023, 5.607272, -1.0125756, 3.721461, 2.5715313, 0.7741753, -0.55034757, 0.7526307, -2.6758716, -2.964664, -0.57379586, -0.28817406, -3.2334063, -0.22387607, -2.0793931, -6.4562697, 0.80134094]]}
```

#### 回應範例

此 API 會傳回下列資訊：

- `event_window`：事件區間
- `event_pattern`：整個時間範圍內的強度分數，以及事件的整體嚴重程度
- `suspected_metrics`：所涉及的指標集合

在下列回應範例中，每個項目都對應到在指標資料中發現的一個事件。演算法在請求的輸入資料中找到一個事件，這可從 `event_pattern` 中輸出的長度為 `1` 看出。`event_window` 顯示該事件發生於時間點 $t$ = 52 到 $t$ = 72 之間。最後，`suspected_metrics` 顯示該事件涉及全部三個指標。

```json
{
  "function_name": "METRICS_CORRELATION",
  "output": {
    "inference_results": [
      {
        "event_window": [
          52,
          72
        ],
        "event_pattern": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3.99625e-05, 0.0001052875, 0.0002605894, 0.00064648513, 0.0014303402, 0.002980127, 0.005871893, 0.010885878, 0.01904726, 0.031481907, 0.04920215, 0.07283493, 0.10219432, 0.1361888, 0.17257516, 0.20853643, 0.24082609, 0.26901975, 0.28376183, 0.29364157, 0.29541212, 0.2832976, 0.29041746, 0.2574534, 0.2610143, 0.22938538, 0.19999361, 0.18074994, 0.15539801, 0.13064545, 0.10544432, 0.081248805, 0.05965102, 0.041305058, 0.027082501, 0.01676033, 0.009760197, 0.005362286, 0.0027713624, 0.0013381141, 0.0006126331, 0.0002634901, 0.000106459476, 4.0407333e-05, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        "suspected_metrics": [0,1,2]
      }
    ]
  }
}
```


