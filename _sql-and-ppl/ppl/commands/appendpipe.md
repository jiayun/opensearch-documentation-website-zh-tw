---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: appendpipe
parent: Commands
grand_parent: PPL
nav_order: 7
---

<!-- vale off -->

# appendpipe 命令

<!-- vale on -->

`appendpipe` 命令會將子管線的結果附加到搜尋結果中。與子搜尋不同，子管線不會先執行；只有在搜尋執行到 `appendpipe` 命令時，子管線才會執行。

此命令會對齊具有相同欄位名稱與類型的欄。對於只存在於主搜尋或子管線中的欄，`NULL` 值會插入至各列缺少的欄位中。

## 語法

`appendpipe` 命令的語法如下：

```sql
appendpipe [<subpipeline>]
```

## 參數

`appendpipe` 命令支援下列參數。

| 參數 | 必要/選用 | 說明 |
| --- | --- | --- |
| `<subpipeline>` | 必要 | 套用至搜尋結果的命令清單，這些搜尋結果是由 `appendpipe` 命令之前的命令所產生。 |
  

## 範例 1：將總計列附加至彙總結果  

下列查詢會依嚴重性層級計算記錄資料筆數，然後附加一列總計。這對於建立同時包含分項與總計的摘要報告很有用：
  
```sql
source=otellogs
| stats count() as log_count by severityText
| sort - log_count
| appendpipe [ stats sum(log_count) as total ]
| fields severityText, log_count, total
```
{% include copy.html %}
{% include try-in-playground.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| severityText | log_count | total |
| --- | --- | --- |
| ERROR | 7 | null |
| INFO | 6 | null |
| WARN | 4 | null |
| DEBUG | 3 | null |
| null | null | 20 |

<!-- vale on -->
  

## 範例 2：將摘要統計資料附加至明細列  

下列查詢會顯示各服務的錯誤計數，然後附加所有服務的整體平均錯誤計數：
  
```sql
source=otellogs
| where severityText = 'ERROR'
| stats count() as error_count by `resource.attributes.service.name`
| sort - error_count
| appendpipe [ stats avg(error_count) as avg_errors ]
| fields `resource.attributes.service.name`, error_count, avg_errors
```
{% include copy.html %}
{% include try-in-playground.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| resource.attributes.service.name | error_count | avg_errors |
| --- | --- | --- |
| checkout | 2 | null |
| payment | 2 | null |
| frontend-proxy | 1 | null |
| product-catalog | 1 | null |
| recommendation | 1 | null |
| null | null | 1.4 |

<!-- vale on -->


## 限制

`appendpipe` 命令有下列限制：

* **結構相容性**：當主搜尋與子管線中同時存在名稱相同但類型不相容的欄位時，查詢會失敗並傳回錯誤。為避免類型衝突，請確保名稱相同的欄位共用相同的資料類型。或者，使用不同的欄位名稱。您可以使用 `eval` 重新命名衝突的欄位，或使用 `fields` 選取不衝突的欄。
