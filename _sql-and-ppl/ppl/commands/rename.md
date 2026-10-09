---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: rename
parent: Commands
grand_parent: PPL
nav_order: 37
---

<!-- vale off -->

# rename 命令

<!-- vale on -->

`rename` 命令會重新命名搜尋結果中的一或多個欄位。

`rename` 命令對不存在的欄位處理方式如下：

* **將不存在的欄位重新命名為不存在的欄位**：搜尋結果不會有任何變更。
* **將不存在的欄位重新命名為現有的欄位**：現有的目標欄位會從搜尋結果中移除。
* **將現有的欄位重新命名為現有的欄位**：現有的目標欄位會移除，並將來源欄位重新命名為目標欄位。

`rename` 命令不會改寫為 [Query DSL]({{site.url}}{{site.baseurl}}/query-dsl/)。它只會在協調節點上執行。
{: .note}

## 語法

`rename` 命令的語法如下：

```sql
rename <source-field> AS <target-field>[, <source-field> AS <target-field>]...
```

## 參數

`rename` 命令支援下列參數。

| 參數 | 必要/選用 | 說明 |
| --- | --- | --- |
| `<source-field>` | 必要 | 您要重新命名的欄位名稱。支援使用 `*` 的萬用字元模式。 |
| `<target-field>` | 必要 | 您要重新命名成的名稱。其萬用字元數量必須與來源相同。 |

## 範例 1：重新命名欄位  

下列查詢會重新命名一個欄位：
  
```sql
source=otellogs
| rename severityText as severity
| fields severity
| head 4
```
{% include copy.html %}
{% include try-in-playground.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| severity |
| --- |
| INFO |
| INFO |
| WARN |
| ERROR |

<!-- vale on -->
  

## 範例 2：重新命名多個欄位  

下列查詢會重新命名多個欄位：
  
```sql
source=otellogs
| rename severityText as severity, `resource.attributes.service.name` as service
| fields severity, service
| head 4
```
{% include copy.html %}
{% include try-in-playground.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| severity | service |
| --- | --- |
| INFO | frontend |
| INFO | cart |
| WARN | product-catalog |
| ERROR | payment |

<!-- vale on -->
  

## 範例 3：使用萬用字元重新命名欄位  

下列查詢會使用萬用字元模式重新命名多個欄位。`severityText` 和 `severityNumber` 都符合 `severity*`，並會重新命名為 `sev*`：
  
```sql
source=otellogs
| rename severity* as sev*
| fields sevText, sevNumber
| head 4
```
{% include copy.html %}
{% include try-in-playground.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| sevText | sevNumber |
| --- | --- |
| INFO | 9 |
| INFO | 9 |
| WARN | 13 |
| ERROR | 17 |

<!-- vale on -->
  

## 範例 4：使用多個萬用字元模式重新命名欄位  

下列查詢會使用多個萬用字元模式重新命名多個欄位：
  
```sql
source=otellogs
| rename severity* as sev*, `@*` as otel_*
| fields sevText, sevNumber, otel_timestamp
| head 4
```
{% include copy.html %}
{% include try-in-playground.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| sevText | sevNumber | otel_timestamp |
| --- | --- | --- |
| INFO | 9 | 2024-02-01 09:10:00 |
| INFO | 9 | 2024-02-01 09:11:00 |
| WARN | 13 | 2024-02-01 09:12:00 |
| ERROR | 17 | 2024-02-01 09:13:00 |

<!-- vale on -->
  

## 範例 5：將現有的欄位重新命名為另一個現有的欄位  

下列查詢會將現有的欄位重新命名為另一個現有的欄位。目標欄位會移除，並將來源欄位重新命名為目標欄位：
  
```sql
source=otellogs
| rename severityText as body
| fields body
| head 4
```
{% include copy.html %}
{% include try-in-playground.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| body |
| --- |
| INFO |
| INFO |
| WARN |
| ERROR |

<!-- vale on -->
  

## 限制

`rename` 命令有下列限制：

* 欄位名稱中的字面星號 (`*`) 字元無法取代，因為星號用於萬用字元比對。
