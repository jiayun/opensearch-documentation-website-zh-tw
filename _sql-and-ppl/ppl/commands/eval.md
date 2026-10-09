---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: eval
parent: Commands
grand_parent: PPL
nav_order: 13
---

<!-- vale off -->

# eval 命令

<!-- vale on -->

`eval` 命令會評估指定的運算式，並將評估結果附加至搜尋結果。

`eval` 命令會在從分片擷取文件之後處理資料。這表示在文件傳回之前，無法使用 `eval` 篩選文件。請使用 `where` 子句進行篩選。此外，由於 `eval` 的運算是在協調節點上執行，而非分散至各資料節點，因此對於大型結果集，效能可能會較慢。

`eval` 命令不會被改寫為 [Query DSL]({{site.url}}{{site.baseurl}}/query-dsl/)，僅會在協調節點上執行。
{: .note}

## 語法

`eval` 命令的語法如下：

```sql
eval <field>=<expression> ["," <field>=<expression> ]...
```

## 參數

`eval` 命令支援下列參數。

| 參數 | 必要/選用 | 說明 |
| --- | --- | --- |
| `<field>` | 必要 | 要建立或更新的欄位名稱。若該欄位不存在，則會新增欄位；若已存在，則會覆寫其值。 |
| `<expression>` | 必要 | 要評估的運算式。 |  
  

## 範例 1：依嚴重性等級分類記錄檔  

下列查詢會建立 `is_critical` 欄位，依據嚴重性將每筆記錄分類為重大或非重大，適合用於建立警示規則：
  
```sql
source=otellogs
| eval is_critical = IF(severityNumber >= 17, 'yes', 'no')
| dedup severityText
| sort severityNumber
| fields severityText, is_critical
```
{% include copy.html %}
{% include try-in-playground.html %}
  
此查詢會傳回下列結果：
  
<!-- vale off -->

| severityText | is_critical |
| --- | --- |
| DEBUG | no |
| INFO | no |
| WARN | no |
| ERROR | yes |

<!-- vale on -->
  

## 範例 2：找出沒有追蹤的錯誤  

下列查詢會建立兩個布林值欄位，用以識別錯誤記錄，以及這些記錄是否具有分散式追蹤內容。未經追蹤的錯誤較難偵錯，因為您無法跨服務追蹤該請求：
  
```sql
source=otellogs
| eval is_error = severityNumber >= 17, is_traced = LENGTH(traceId) > 0
| where is_error = true
| sort `resource.attributes.service.name`
| fields `resource.attributes.service.name`, is_error, is_traced
```
{% include copy.html %}
{% include try-in-playground.html %}
  
此查詢會傳回下列結果：
  
<!-- vale off -->

| resource.attributes.service.name | is_error | is_traced |
| --- | --- | --- |
| checkout | True | True |
| checkout | True | False |
| frontend-proxy | True | True |
| payment | True | True |
| payment | True | False |
| product-catalog | True | False |
| recommendation | True | True |

<!-- vale on -->
  

## 範例 3：建立標準化的記錄行  

下列查詢會在記錄本文前加上嚴重性等級，建立適用於匯出或警示的標準化格式：
  
```sql
source=otellogs
| where severityText IN ('ERROR', 'WARN')
| eval formatted = '[' + severityText + '] ' + body
| sort severityNumber, `resource.attributes.service.name`
| fields formatted
| head 3
```
{% include copy.html %}
{% include try-in-playground.html %}
  
此查詢會傳回下列結果：
  
<!-- vale off -->

| formatted |
| --- |
| [WARN] SSL certificate for api.example.com expires in 14 days |
| [WARN] Rate limit threshold reached: 450/500 requests per minute for API key ending in ...abc789 |
| [WARN] Slow query detected: SELECT \* FROM products WHERE category = 'electronics' took 3200ms |

<!-- vale on -->
  
