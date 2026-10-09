---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: ml
parent: Commands
grand_parent: PPL
nav_order: 28
---

<!-- vale off -->

# ml 命令

<!-- vale on -->

`ml` 命令會將 ML Commons 外掛程式中的機器學習 (ML) 演算法套用至 PPL 命令所傳回的搜尋結果。它支援各種 ML 操作，包括異常偵測與叢集化。此命令可執行訓練、預測或訓練與預測合併的操作，取決於演算法與指定的動作。

若要使用 `ml` 命令，必須將 `plugins.calcite.enabled` 設定為 `false`。
{: .note}

`ml` 命令支援下列演算法：

- **Random Cut Forest (RCF)**，用於異常偵測，同時支援時間序列與非時間序列資料

- **K-means**，用於將資料點分群為群組

## 語法

`ml` 命令支援不同的語法選項，取決於演算法。

### 時間序列資料的異常偵測

使用此語法來偵測時間序列資料中的異常。此方法使用針對循序資料模式最佳化的 RCF 演算法：

```sql
ml action='train' algorithm='rcf' <number_of_trees> <shingle_size> <sample_size> <output_after> <time_decay> <anomaly_rate> <time_field> <date_format> <time_zone>
```

### 參數

固定時間 RCF 演算法支援下列參數。

| 參數 | 必要/選用 | 說明 |
| --- | --- | --- |
| `number_of_trees` | 選用 | 森林中的樹木數量。預設為 `30`。 |
| `shingle_size` | 選用 | 拼湊 (shingle) 中的記錄數量。拼湊是一連串最近的連續記錄。預設為 `8`。 |
| `sample_size` | 選用 | 此森林中串流取樣器所使用的取樣大小。預設為 `256`。 |
| `output_after` | 選用 | 串流取樣器在傳回結果之前所需的點數。預設為 `32`。 |
| `time_decay` | 選用 | 此森林中串流取樣器所使用的衰減因子。預設為 `0.0001`。 |
| `anomaly_rate` | 選用 | 異常率。預設為 `0.005`。 |
| `time_field` | 必要 | RCF 用來作為時間序列資料的時間欄位。 |
| `date_format` | 選用 | `time_field` 的格式。預設為 `yyyy-MM-dd HH:mm:ss`。 |
| `time_zone` | 選用 | `time_field` 的時區。預設為 `UTC`。 |
| `category_field` | 選用 | 用來將輸入值分組的類別欄位。預測操作會分別套用至每個類別。 |

### 非時間序列資料的異常偵測

使用此語法來偵測順序不重要的資料中的異常。此方法使用針對獨立資料點最佳化的 RCF 演算法：

```sql
ml action='train' algorithm='rcf' <number_of_trees> <sample_size> <output_after> <training_data_size> <anomaly_score_threshold>
```

### 參數

批次 RCF 演算法支援下列參數。

| 參數 | 必要/選用 | 說明 |
| --- | --- | --- |
| `number_of_trees` | 選用 | 森林中的樹木數量。預設為 `30`。 |
| `sample_size` | 選用 | 從訓練資料集提供給每棵樹的隨機樣本數量。預設為 `256`。 |
| `output_after` | 選用 | 串流取樣器在傳回結果之前所需的點數。預設為 `32`。 |
| `training_data_size` | 選用 | 訓練資料集的大小。預設為完整資料集大小。 |
| `anomaly_score_threshold` | 選用 | 異常分數閾值。預設為 `1.0`。 |
| `category_field` | 選用 | 用來將輸入值分組的類別欄位。預測操作會分別套用至每個類別。 |  
  

### K-means 叢集化

使用此語法根據相似度將資料點分群為叢集：

```sql
ml action='train' algorithm='kmeans' <centroids> <iterations> <distance_type>
```

### 參數

k-means 叢集化演算法支援下列參數。

| 參數 | 必要/選用 | 說明 |
| --- | --- | --- |
| `centroids` | 選用 | 要將資料點分群成的叢集數量。預設為 `2`。 |
| `iterations` | 選用 | 迭代次數。預設為 `10`。 |
| `distance_type` | 選用 | 距離類型。有效值為 `COSINE`、`L1` 與 `EUCLIDEAN`。預設為 `EUCLIDEAN`。 |  
  

## 範例 1：時間序列異常偵測

此範例會訓練 RCF 模型，並使用它來偵測時間序列載客量資料中的異常：
  
```sql
source=nyc_taxi
| fields value, timestamp
| ml action='train' algorithm='rcf' time_field='timestamp'
| where value=10844.0
```
{% include copy.html %}
  
此查詢會傳回下列結果：
  
<!-- vale off -->

| value | timestamp | score | anomaly_grade |
| --- | --- | --- | --- |
| 10844.0 | 2014-07-01 00:00:00 | 0.0 | 0.0 |

<!-- vale on -->
  

## 範例 2：依類別進行時間序列異常偵測

此範例會訓練 RCF 模型，並使用它來偵測多個類別值的時間序列載客量資料中的異常：
  
```sql
source=nyc_taxi
| fields category, value, timestamp
| ml action='train' algorithm='rcf' time_field='timestamp' category_field='category'
| where value=10844.0 or value=6526.0
```
{% include copy.html %}
  
此查詢會傳回下列結果：
  
<!-- vale off -->

| category | value | timestamp | score | anomaly_grade |
| --- | --- | --- | --- | --- |
| night | 10844.0 | 2014-07-01 00:00:00 | 0.0 | 0.0 |
| day | 6526.0 | 2014-07-01 06:00:00 | 0.0 | 0.0 |

<!-- vale on -->
  

## 範例 3：非時間序列異常偵測

此範例會訓練 RCF 模型，並使用它來偵測非時間序列載客量資料中的異常：
  
```sql
source=nyc_taxi
| fields value
| ml action='train' algorithm='rcf'
| where value=10844.0
```
{% include copy.html %}
  
此查詢會傳回下列結果：
  
<!-- vale off -->

| value | score | anomalous |
| --- | --- | --- |
| 10844.0 | 0.0 | False |

<!-- vale on -->
  

## 範例 4：依類別進行非時間序列異常偵測

此範例會訓練 RCF 模型，並使用它來偵測多個類別值的非時間序列載客量資料中的異常：
  
```sql
source=nyc_taxi
| fields category, value
| ml action='train' algorithm='rcf' category_field='category'
| where value=10844.0 or value=6526.0
```
{% include copy.html %}
  
此查詢會傳回下列結果：
  
<!-- vale off -->

| category | value | score | anomalous |
| --- | --- | --- | --- |
| night | 10844.0 | 0.0 | False |
| day | 6526.0 | 0.0 | False |

<!-- vale on -->
  

## 範例 5：Iris 資料集的 K-means 叢集化  

此範例使用 k-means 叢集化，根據從每個樣本測量到的四個特徵組合（花萼與花瓣的長度和寬度），將三種 Iris 物種（Iris setosa、Iris virginica 與 Iris versicolor）分類：
  
```sql
source=iris_data
| fields sepal_length_in_cm, sepal_width_in_cm, petal_length_in_cm, petal_width_in_cm
| ml action='train' algorithm='kmeans' centroids=3
```
{% include copy.html %}
  
此查詢會傳回下列結果：
  
<!-- vale off -->

| sepal_length_in_cm | sepal_width_in_cm | petal_length_in_cm | petal_width_in_cm | ClusterID |
| --- | --- | --- | --- | --- |
| 5.1 | 3.5 | 1.4 | 0.2 | 1 |
| 5.6 | 3.0 | 4.1 | 1.3 | 0 |
| 6.7 | 2.5 | 5.8 | 1.8 | 2 |

<!-- vale on -->
  

