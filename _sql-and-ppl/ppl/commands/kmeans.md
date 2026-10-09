---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: kmeans
parent: Commands
grand_parent: PPL
nav_order: 26
---

<!-- vale off -->

# kmeans 命令（已棄用）

<!-- vale on -->

`kmeans` 命令已棄用，請改用 [`ml` 命令]({{site.url}}{{site.baseurl}}/sql-and-ppl/ppl/commands/ml/)。
{: .warning}

`kmeans` 命令會將 ML Commons 外掛程式中的 k-means 演算法套用至 PPL 命令傳回的搜尋結果。

若要使用 `kmeans` 命令，必須將 `plugins.calcite.enabled` 設為 `false`。
{: .note}

## 語法

`kmeans` 命令的語法如下：

```sql
kmeans <centroids> <iterations> <distance_type>
```

## 參數

`kmeans` 命令支援下列參數。

| 參數 | 必要／選用 | 說明 |
| --- | --- | --- |
| `<centroids>` | 選用 | 將資料點分組成的叢集數量。預設為 `2`。 |
| `<iterations>` | 選用 | 迭代次數。預設為 `10`。 |
| `<distance_type>` | 選用 | 距離類型。有效值為 `COSINE`、`L1` 和 `EUCLIDEAN`。預設為 `EUCLIDEAN`。 |  
  

## 範例：Iris 資料集的分群  

下列查詢根據每個樣本測得的四項特徵（萼片和花瓣的長度與寬度）組合，將三種鳶尾花（Iris setosa、Iris virginica 和 Iris versicolor）分類：
  
```sql
source=iris_data
| fields sepal_length_in_cm, sepal_width_in_cm, petal_length_in_cm, petal_width_in_cm
| kmeans centroids=3
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
  

