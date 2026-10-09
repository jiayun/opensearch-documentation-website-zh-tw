---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: ad
parent: Commands
grand_parent: PPL
nav_order: 2
---

<!-- vale off -->

# ad 命令 (已棄用)

<!-- vale on -->

`ad` 命令已棄用，請改用 [`ml` 命令]({{site.url}}{{site.baseurl}}/sql-and-ppl/ppl/commands/ml/)。
{: .warning}

`ad` 命令會將 ML Commons 外掛程式中的隨機切割森林 (Random Cut Forest，RCF) 演算法套用至 PPL 命令傳回的搜尋結果。此命令提供兩種異常偵測方法：

- [時間序列資料的異常偵測](#anomaly-detection-for-time-series-data)，使用固定時間 RCF 演算法
- [非時間序列資料的異常偵測](#anomaly-detection-for-non-time-series-data)，使用批次 RCF 演算法

若要使用 `ad` 命令，必須將 `plugins.calcite.enabled` 設定為 `false`。
{: .note}

## 語法

`ad` 命令有兩種不同的語法變體，取決於演算法類型。

### 時間序列資料的異常偵測

使用此語法可偵測時間序列資料中的異常。此方法使用固定時間 RCF 演算法，該演算法已針對循序資料模式進行最佳化。

固定時間 RCF `ad` 命令的語法如下：

```sql
ad [number_of_trees] [shingle_size] [sample_size] [output_after] [time_decay] [anomaly_rate] <time_field> [date_format] [time_zone] [category_field]
```

### 參數

固定時間 RCF 演算法支援下列參數。

| 參數 | 必要/選用 | 說明 |
| --- | --- | --- |
| `time_field` | 必要 | RCF 用來作為時間序列資料的時間欄位。 |
| `number_of_trees` | 選用 | 森林中的樹木數量。預設為 `30`。 |
| `shingle_size` | 選用 | 拼片中的記錄數量。拼片是一連串連續的最近記錄。預設為 `8`。 |
| `sample_size` | 選用 | 此森林中串流取樣器使用的取樣大小。預設為 `256`。 |
| `output_after` | 選用 | 串流取樣器在傳回結果之前所需的點數。預設為 `32`。 |
| `time_decay` | 選用 | 此森林中串流取樣器使用的衰減因子。預設為 `0.0001`。 |
| `anomaly_rate` | 選用 | 異常率。預設為 `0.005`。 |
| `date_format` | 選用 | `time_field` 欄位使用的格式。預設為 `yyyy-MM-dd HH:mm:ss`。 |
| `time_zone` | 選用 | `time_field` 欄位的時區。預設為 `UTC`。 |
| `category_field` | 選用 | 用來將輸入值分組的分類欄位。預測作業會分別套用至每個分類。 |  
  

### 非時間序列資料的異常偵測

使用此語法可偵測順序不重要的資料中的異常。此方法使用批次 RCF 演算法，該演算法已針對獨立資料點進行最佳化。

批次 RCF `ad` 命令的語法如下：

```sql
ad [number_of_trees] [sample_size] [output_after] [training_data_size] [anomaly_score_threshold] [category_field]
```

### 參數

批次 RCF 演算法支援下列參數。

| 參數 | 必要/選用 | 說明 |
| --- | --- | --- |
| `number_of_trees` | 選用 | 森林中的樹木數量。預設為 `30`。 |
| `sample_size` | 選用 | 從訓練資料集提供給每棵樹的隨機取樣數量。預設為 `256`。 |
| `output_after` | 選用 | 串流取樣器在傳回結果之前所需的點數。預設為 `32`。 |
| `training_data_size` | 選用 | 訓練資料集的大小。預設為完整資料集大小。 |
| `anomaly_score_threshold` | 選用 | 異常分數閾值。預設為 `1.0`。 |
| `category_field` | 選用 | 用來將輸入值分組的分類欄位。預測作業會分別套用至每個分類。 |  
  
<!-- vale off -->

## 範例 1：偵測紐約市計程車載客量時間序列資料中的事件

<!-- vale on -->

下列範例使用 `nyc_taxi` 資料集，其中包含紐約市計程車載客量資料，欄位包括 `value` (載客趟數)、`timestamp` (測量時間) 及 `category` (時段分類，例如 'day' 和 'night')。

此範例會訓練 RCF 模型，並使用該模型偵測時間序列載客量資料中的異常：
  
```sql
source=nyc_taxi
| fields value, timestamp
| AD time_field='timestamp'
| where value=10844.0
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| value | timestamp | score | anomaly_grade |
| --- | --- | --- | --- |
| 10844.0 | 2014-07-01 00:00:00 | 0.0 | 0.0 |

<!-- vale on -->
  

<!-- vale off -->

## 範例 2：依分類偵測紐約市計程車載客量時間序列資料中的事件

<!-- vale on -->

此範例會訓練 RCF 模型，並使用該模型偵測多個分類值之時間序列載客量資料中的異常：
  
```sql
source=nyc_taxi
| fields category, value, timestamp
| AD time_field='timestamp' category_field='category'
| where value=10844.0 or value=6526.0
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| category | value | timestamp | score | anomaly_grade |
| --- | --- | --- | --- | --- |
| night | 10844.0 | 2014-07-01 00:00:00 | 0.0 | 0.0 |
| day | 6526.0 | 2014-07-01 06:00:00 | 0.0 | 0.0 |

<!-- vale on -->
  

<!-- vale off -->

## 範例 3：偵測紐約市計程車載客量非時間序列資料中的事件

<!-- vale on -->

此範例會訓練 RCF 模型，並使用該模型偵測非時間序列載客量資料中的異常：
  
```sql
source=nyc_taxi
| fields value
| AD
| where value=10844.0
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| value | score | anomalous |
| --- | --- | --- |
| 10844.0 | 0.0 | False |

<!-- vale on -->
  

<!-- vale off -->

## 範例 4：依分類偵測紐約市計程車載客量非時間序列資料中的事件

<!-- vale on -->

此範例會訓練 RCF 模型，並使用該模型偵測多個分類值之非時間序列載客量資料中的異常：
  
```sql
source=nyc_taxi
| fields category, value
| AD category_field='category'
| where value=10844.0 or value=6526.0
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| category | value | score | anomalous |
| --- | --- | --- | --- |
| night | 10844.0 | 0.0 | False |
| day | 6526.0 | 0.0 | False |

<!-- vale on -->
  

