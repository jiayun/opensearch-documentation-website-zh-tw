---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: addcoltotals
parent: Commands
grand_parent: PPL
nav_order: 3
---

<!-- vale off -->

# addcoltotals 命令

<!-- vale on -->

`addcoltotals` 命令會計算每個資料行的總和，並新增一個摘要列，顯示每個資料行的總計。此命令等同於將 `addtotals` 搭配 `row=false` 和 `col=true` 使用，因此適合用來建立包含資料行總計的摘要報表。

此命令只會處理數值欄位（整數、浮點數、雙精度浮點數）。無論非數值欄位是否明確列在欄位清單中，都會被忽略。


## 語法

`addcoltotals` 命令的語法如下：

```sql
addcoltotals [field-list] [label=<string>] [labelfield=<field>]
```

## 參數

`addcoltotals` 命令支援下列參數。

| 參數 | 必要/選用 | 說明 |
| --- | --- | --- |
| `<field-list>` | 選用 | 要加總的數值欄位清單，以逗號分隔。預設會加總所有數值欄位。 |
| `labelfield` | 選用 | 放置標籤的欄位。如果該欄位不存在，系統會建立該欄位，並在新欄位的摘要列（最後一列）中顯示標籤。 |
| `label` | 選用 | 顯示在摘要列（最後一列）中、用來識別計算總計的文字。與 `labelfield` 搭配使用時，此文字會放在摘要列的指定欄位中。預設為 `Total`。 |

## 範例 1：為嚴重性分類新增資料行總計

下列查詢會為嚴重性分類新增一個總計列，顯示所有記錄檔項目的總計：

```sql
source=otellogs
| stats count() as log_count by severityText
| sort severityText
| fields severityText, log_count
| addcoltotals labelfield='severityText'
```
{% include copy.html %}
{% include try-in-playground.html %}

查詢會傳回下列結果：

<!-- vale off -->

| severityText | log_count |
| --- | --- |
| DEBUG | 3 |
| ERROR | 7 |
| INFO | 6 |
| WARN | 4 |
| Total | 20 |

<!-- vale on -->

## 範例 2：使用自訂標籤新增資料行總計

下列查詢會為每個服務的錯誤計數新增總計，並使用自訂的摘要標籤：

```sql
source=otellogs
| where severityText = 'ERROR'
| stats count() as errors by `resource.attributes.service.name`
| sort `resource.attributes.service.name`
| addcoltotals errors label='Grand Total' labelfield='Summary'
```
{% include copy.html %}
{% include try-in-playground.html %}

查詢會傳回下列結果：

<!-- vale off -->

| errors | resource.attributes.service.name | Summary |
| --- | --- | --- |
| 2 | checkout | null |
| 1 | frontend-proxy | null |
| 2 | payment | null |
| 1 | product-catalog | null |
| 1 | recommendation | null |
| 7 | null | Grand Total |

<!-- vale on -->

## 範例 3：使用所有選項

下列查詢使用 `addcoltotals` 命令並設定所有選項，只加總指定的數值欄位，並將摘要標籤放在新的資料行中：

```sql
source=otellogs
| where severityText IN ('ERROR', 'WARN')
| eval error_count = IF(severityText = 'ERROR', 1, 0), warn_count = IF(severityText = 'WARN', 1, 0)
| stats sum(error_count) as errors, sum(warn_count) as warnings by `resource.attributes.service.name`
| sort `resource.attributes.service.name`
| addcoltotals errors, warnings label='Sum' labelfield='Column Total'
```
{% include copy.html %}
{% include try-in-playground.html %}

查詢會傳回下列結果：

<!-- vale off -->

| errors | warnings | resource.attributes.service.name | Column Total |
| --- | --- | --- | --- |
| 2 | 0 | checkout | null |
| 1 | 2 | frontend-proxy | null |
| 2 | 0 | payment | null |
| 1 | 2 | product-catalog | null |
| 1 | 0 | recommendation | null |
| 7 | 4 | null | Sum |

<!-- vale on -->
