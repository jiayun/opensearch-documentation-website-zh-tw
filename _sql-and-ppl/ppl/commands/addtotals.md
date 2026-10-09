---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: addtotals
parent: Commands
grand_parent: PPL
nav_order: 4
---

<!-- vale off -->

# addtotals 命令

<!-- vale on -->

`addtotals` 命令會計算數值欄位的總和，並可同時建立欄位總計 (摘要列) 與列總計 (新欄位)。此命令適合用來建立包含小計或總計的摘要報表。

此命令只會處理數值欄位 (整數、浮點數、雙精確度數)。無論是否在欄位清單中明確指定，非數值欄位都會被忽略。


## 語法

`addtotals` 命令的語法如下：

```sql
addtotals [field-list] [label=<string>] [labelfield=<field>] [row=<boolean>] [col=<boolean>] [fieldname=<field>]
```

## 參數

`addtotals` 命令支援下列參數。

| 參數 | 必要/選用 | 說明 |
| --- | --- | --- |
| `<field-list>` | 選用 | 要加總的數值欄位清單，以逗號分隔。預設會加總所有數值欄位。 |
| `row` | 選用 | 計算每一列的總和，並新增一個欄位來儲存列總計。預設為 `true`。 |
| `col` | 選用 | 計算每一欄的總和，並在結尾新增一個摘要事件，其中包含欄位總計。預設為 `false`。 |
| `labelfield` | 選用 | 放置標籤的欄位。如果該欄位不存在，則會建立該欄位，並在新欄位的摘要列 (最後一列) 中顯示標籤。適用於 `col=true` 時。 |
| `label` | 選用 | 出現在摘要列 (最後一列) 中，用於識別所計算總和的文字。與 `labelfield` 搭配使用時，此文字會放置在摘要列中指定的欄位。預設為 `Total`。適用於 `col=true` 時。當 `labelfield` 與 `fieldname` 參數指定相同的欄位名稱時，此參數沒有作用。 |
| `fieldname` | 選用 | 用來儲存列總計的欄位。適用於 `row=true` 時。 |

## 範例 1：新增欄位總計

下列查詢會統計每個服務的錯誤與警告次數，然後新增一列欄位總計，顯示整體總計：

```sql
source=otellogs
| where severityText IN ('ERROR', 'WARN')
| eval error_count = IF(severityText = 'ERROR', 1, 0), warn_count = IF(severityText = 'WARN', 1, 0)
| stats sum(error_count) as errors, sum(warn_count) as warnings by `resource.attributes.service.name`
| sort `resource.attributes.service.name`
| fields `resource.attributes.service.name`, errors, warnings
| addtotals col=true labelfield='resource.attributes.service.name' label='Total'
```
{% include copy.html %}
{% include try-in-playground.html %}

查詢會傳回下列結果：

<!-- vale off -->

| resource.attributes.service.name | errors | warnings | Total |
| --- | --- | --- | --- |
| checkout | 2 | 0 | 2 |
| frontend-proxy | 1 | 2 | 3 |
| payment | 2 | 0 | 2 |
| product-catalog | 1 | 2 | 3 |
| recommendation | 1 | 0 | 1 |
| Total | 7 | 4 | null |

<!-- vale on -->

## 範例 2：新增列總計

下列查詢會分別統計每個服務的錯誤與警告次數，然後新增一個列總計，顯示每個服務可處理問題的合計次數：

```sql
source=otellogs
| where severityText IN ('ERROR', 'WARN')
| eval error_count = IF(severityText = 'ERROR', 1, 0), warn_count = IF(severityText = 'WARN', 1, 0)
| stats sum(error_count) as errors, sum(warn_count) as warnings by `resource.attributes.service.name`
| sort `resource.attributes.service.name`
| fields `resource.attributes.service.name`, errors, warnings
| addtotals row=true fieldname='total_issues'
```
{% include copy.html %}
{% include try-in-playground.html %}

查詢會傳回下列結果：

<!-- vale off -->

| resource.attributes.service.name | errors | warnings | total_issues |
| --- | --- | --- | --- |
| checkout | 2 | 0 | 2 |
| frontend-proxy | 1 | 2 | 3 |
| payment | 2 | 0 | 2 |
| product-catalog | 1 | 2 | 3 |
| recommendation | 1 | 0 | 1 |

<!-- vale on -->

## 範例 3：使用所有選項

下列查詢使用 `addtotals` 命令並設定所有選項，在單一報表中同時結合列總計與欄位總計：

```sql
source=otellogs
| where severityText IN ('ERROR', 'WARN')
| eval error_count = IF(severityText = 'ERROR', 1, 0), warn_count = IF(severityText = 'WARN', 1, 0)
| stats sum(error_count) as errors, sum(warn_count) as warnings by `resource.attributes.service.name`
| sort `resource.attributes.service.name`
| fields `resource.attributes.service.name`, errors, warnings
| addtotals errors, warnings row=true col=true fieldname='Row Total' label='Sum' labelfield='Column Total'
```
{% include copy.html %}
{% include try-in-playground.html %}

查詢會傳回下列結果：

<!-- vale off -->

| resource.attributes.service.name | errors | warnings | Row Total | Column Total |
| --- | --- | --- | --- | --- |
| checkout | 2 | 0 | 2 | null |
| frontend-proxy | 1 | 2 | 3 | null |
| payment | 2 | 0 | 2 | null |
| product-catalog | 1 | 2 | 3 | null |
| recommendation | 1 | 0 | 1 | null |
| null | 7 | 4 | null | Sum |

<!-- vale on -->
