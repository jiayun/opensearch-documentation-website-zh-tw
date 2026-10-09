---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: append
parent: Commands
grand_parent: PPL
nav_order: 5
---

<!-- vale off -->

# append 命令

<!-- vale on -->

`append` 命令會將子搜尋的結果以額外資料列的形式附加至輸入搜尋結果 (主搜尋) 的結尾。

此命令會對齊欄位名稱和資料類型相同的資料行。對於只存在於主搜尋或子搜尋其中之一的資料行，會在對應資料列的缺少欄位中填入 `NULL` 值。

## 語法

`append` 命令的語法如下：

```sql
append <subsearch>
```

## 參數

`append` 命令支援下列參數。

| 參數 | 必要/選用 | 說明 |
| --- | --- | --- |
| `<subsearch>` | 必要 | 以次要搜尋的形式執行 PPL 命令。 |  

## 範例 1：並列附加錯誤與警告計數

下列查詢會顯示每個服務的錯誤計數，然後附加來自個別查詢的警告計數。這可讓您比較各服務的錯誤率與警告率：
  
```sql
source=otellogs
| where severityText = 'ERROR'
| stats count() as error_count by `resource.attributes.service.name`
| sort - error_count
| append [ source=otellogs | where severityText = 'WARN' | stats count() as warn_count by `resource.attributes.service.name` ]
| sort `resource.attributes.service.name`
| fields `resource.attributes.service.name`, error_count, warn_count
```
{% include copy.html %}
{% include try-in-playground.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| resource.attributes.service.name | error_count | warn_count |
| --- | --- | --- |
| checkout | 2 | null |
| frontend-proxy | 1 | null |
| frontend-proxy | null | 2 |
| payment | 2 | null |
| product-catalog | 1 | null |
| product-catalog | null | 2 |
| recommendation | 1 | null |

<!-- vale on -->
  

## 範例 2：將摘要資料列附加至明細資料列

下列查詢會顯示各嚴重性等級的計數，然後附加所有等級的總計數：
  
```sql
source=otellogs
| stats count() as log_count by severityText
| sort - log_count
| append [ source=otellogs | stats count() as log_count | eval severityText = 'ALL' ]
| fields severityText, log_count
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
| ALL | 20 |

<!-- vale on -->

## 限制

`append` 命令有下列限制：

* **結構相容性**：當主搜尋與子搜尋中同時存在同名欄位，但類型不相容時，查詢會失敗並傳回錯誤。為避免類型衝突，請確保同名欄位共用相同的資料類型。或者，使用不同的欄位名稱。您可以使用 `eval` 重新命名衝突的欄位，或使用 `fields` 選取不衝突的資料行。
