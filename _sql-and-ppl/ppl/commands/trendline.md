---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: trendline
parent: Commands
grand_parent: PPL
nav_order: 52
---

<!-- vale off -->

# trendline 命令

<!-- vale on -->

`trendline` 命令會計算欄位的移動平均。

## 語法

`trendline` 命令的語法如下：

```sql
trendline [sort [+|-] <sort-field>] (sma | wma)(<number-of-datapoints>, <field>) [as <alias>] [(sma | wma)(<number-of-datapoints>, <field>) [as <alias>]]...
```

## 參數

`trendline` 命令支援下列參數。

| 參數 | 必要/選用 | 說明 |
| --- | --- | --- |
| `[+|-]` | 選用 | 資料的排序順序。`+` 指定遞增排序，`NULL`/`MISSING` 排在最前面；`-` 指定遞減排序，`NULL`/`MISSING` 排在最後面。預設值為 `+`。 |
| `<sort-field>` | 必要 | 用於排序資料的欄位。 |
| `(sma | wma)` | 必要 | 要計算的移動平均類型。`sma` 會計算簡單移動平均，所有值的權重相同；`wma` 會計算加權移動平均，較近期的值權重較高。 |
| `number-of-datapoints` | 必要 | 用於計算移動平均的資料點數量。必須大於零。 |
| `<field>` | 必要 | 要計算移動平均的欄位。 |
| `<alias>` | 選用 | 包含移動平均的結果欄名稱。預設為 `<field>` 名稱後加上 `_trendline`。 |

## 範例 1：追蹤嚴重性是否隨時間升高

下列查詢會計算 `severityNumber` 的 3 點簡單移動平均：
  
```sql
source=otellogs
| sort `@timestamp`
| trendline sma(3, severityNumber) as sev_trend
| fields severityText, severityNumber, sev_trend
| head 6
```
{% include copy.html %}
{% include try-in-playground.html %}
  
此查詢會傳回下列結果：
  
<!-- vale off -->

| severityText | severityNumber | sev_trend |
| --- | --- | --- |
| INFO | 9 | null |
| INFO | 9 | null |
| WARN | 13 | 10.333333333333334 |
| ERROR | 17 | 13.0 |
| DEBUG | 5 | 11.666666666666666 |
| ERROR | 17 | 13.0 |

<!-- vale on -->
  

## 範例 2：使用加權移動平均呈現偏重近期的趨勢

下列查詢會計算加權移動平均，給予較近期的值更高的權重：
  
```sql
source=otellogs
| sort `@timestamp`
| trendline wma(3, severityNumber) as wma_trend
| fields severityText, severityNumber, wma_trend
| head 6
```
{% include copy.html %}
{% include try-in-playground.html %}
  
此查詢會傳回下列結果：
  
<!-- vale off -->

| severityText | severityNumber | wma_trend |
| --- | --- | --- |
| INFO | 9 | null |
| INFO | 9 | null |
| WARN | 13 | 11.0 |
| ERROR | 17 | 14.333333333333334 |
| DEBUG | 5 | 10.333333333333334 |
| ERROR | 17 | 13.0 |

<!-- vale on -->


## 限制

`trendline` 命令有下列限制：

* `trendline` 命令要求指定的 `<field>` 參數中的所有值皆不得為 null。此欄位中值為 `null` 的任何資料列，都會自動從命令的輸出中排除。
