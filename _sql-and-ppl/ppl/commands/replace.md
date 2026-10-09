---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: replace
parent: Commands
grand_parent: PPL
nav_order: 38
---

<!-- vale off -->

# replace 命令

<!-- vale on -->

`replace` 命令會取代搜尋結果中一個或多個欄位內的文字。它支援字面字串取代，以及使用 `*` 的萬用字元模式。

## 語法

`replace` 命令的語法如下：

```sql
replace '<pattern>' WITH '<replacement>' [, '<pattern>' WITH '<replacement>']... IN <field-name>[, <field-name>]...
```

## 參數

`replace` 命令支援下列參數。

| 參數 | 必要/選用 | 說明 |
| --- | --- | --- |
| `<pattern>` | 必要 | 要取代的文字模式。 |
| `<replacement>` | 必要 | 用來取代的文字。 |
| `<field-name>` | 必要 | 要套用取代的一個或多個欄位。 |

## 範例 1：取代單一欄位中的文字  

下列查詢會取代單一欄位中的文字：
  
```sql
source=otellogs
| replace "product-catalog" WITH "product catalog" IN `resource.attributes.service.name`
| fields `resource.attributes.service.name`, severityText
| head 5
```
{% include copy.html %}
{% include try-in-playground.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| resource.attributes.service.name | severityText |
| --- | --- |
| frontend | INFO |
| cart | INFO |
| product catalog | WARN |
| payment | ERROR |
| cart | DEBUG |

<!-- vale on -->
  

## 範例 2：取代多個欄位中的文字  

下列查詢會取代多個欄位中的文字：
  
```sql
source=otellogs
| replace "ERROR" WITH "Error", "WARN" WITH "Warning" IN severityText
| fields severityText, `resource.attributes.service.name`
| head 5
```
{% include copy.html %}
{% include try-in-playground.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| severityText | resource.attributes.service.name |
| --- | --- |
| INFO | frontend |
| INFO | cart |
| Warning | product-catalog |
| Error | payment |
| DEBUG | cart |

<!-- vale on -->
  

## 範例 3：在管線中使用 replace 命令

下列查詢會在查詢管線中將 `replace` 命令與其他命令搭配使用：
  
```sql
source=otellogs
| where severityText = 'ERROR'
| replace "frontend-proxy" WITH "frontend proxy" IN `resource.attributes.service.name`
| fields `resource.attributes.service.name`, body
| head 3
```
{% include copy.html %}
{% include try-in-playground.html %}
```sql
| where age > 30
| fields state, age
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
```text
fetched rows / total rows = 3/3
+----------------------------------+-------------------------------------------------------------------------+
| resource.attributes.service.name | body                                                                    |
|----------------------------------+-------------------------------------------------------------------------|
| payment                          | Payment failed: connection timeout to payment gateway after 30000ms     |
| checkout                         | NullPointerException in CheckoutService.placeOrder at line 142          |
| payment                          | Out of memory: Java heap space - shutting down pod payment-6f8d4b-ht7q3 |
+----------------------------------+-------------------------------------------------------------------------+
```
  

## 範例 4：使用多組模式-取代配對來取代文字

下列查詢會在單一 replace 命令中使用 `replace` 命令搭配多組模式與取代配對。這些取代會依序套用：
  
```sql
source=accounts
| replace "IL" WITH "Illinois", "TN" WITH "Tennessee" IN state
| fields state
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
```text
fetched rows / total rows = 4/4
+-----------+
| state     |
|-----------|
| Illinois  |
| Tennessee |
| VA        |
| MD        |
+-----------+
```
  

## 範例 5：使用 LIKE 進行模式比對

下列查詢會使用 `LIKE` 命令搭配 `replace` 命令進行模式比對，因為 `replace` 命令僅支援純字串常值：
  
```sql
source=accounts
| where LIKE(address, '%Holmes%')
| replace "Holmes" WITH "HOLMES" IN address
| fields address, state, gender, age, city
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
```text
fetched rows / total rows = 1/1
+-----------------+-------+--------+-----+--------+
| address         | state | gender | age | city   |
|-----------------+-------+--------+-----+--------|
| 880 HOLMES Lane | IL    | M      | 32  | Brogan |
+-----------------+-------+--------+-----+--------+
```
  

## 範例 6：萬用字元後置字元比對  

下列查詢示範萬用字元後置字元比對，其中 `*` 會比對特定結尾模式之前的所有字元：
  
```sql
source=accounts
| replace "*IL" WITH "Illinois" IN state
| fields state
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
```text
fetched rows / total rows = 4/4
+----------+
| state    |
|----------|
| Illinois |
| TN       |
| VA       |
| MD       |
+----------+
```
  

## 範例 7：萬用字元前置字元比對  

下列查詢示範萬用字元前置字元比對，其中 `*` 會比對特定起始模式之後的所有字元：
  
```sql
source=accounts
| replace "IL*" WITH "Illinois" IN state
| fields state
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
```text
fetched rows / total rows = 4/4
+----------+
| state    |
|----------|
| Illinois |
| TN       |
| VA       |
| MD       |
+----------+
```
  

## 範例 8：萬用字元擷取與替換  

下列查詢會在模式與取代中同時使用萬用字元，以擷取並重複使用比對到的部分。模式與取代中的萬用字元數量必須相符：
  
```sql
source=accounts
| replace "* Lane" WITH "Lane *" IN address
| fields address
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
```text
fetched rows / total rows = 4/4
+----------------------+
| address              |
|----------------------|
| Lane 880 Holmes      |
| 671 Bristol Street   |
| 789 Madison Street   |
| 467 Hutchinson Court |
+----------------------+
```
  

## 範例 9：使用多個萬用字元轉換模式  

下列查詢會使用多個萬用字元來轉換模式。取代中的每個萬用字元都會以對應的擷取值來替換：
  
```sql
source=accounts
| replace "* *" WITH "*_*" IN address
| fields address
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
```text
fetched rows / total rows = 4/4
+----------------------+
| address              |
|----------------------|
| 880_Holmes Lane      |
| 671_Bristol Street   |
| 789_Madison Street   |
| 467_Hutchinson Court |
+----------------------+
```
  

## 範例 10：將任何比對結果取代為固定值  

下列查詢示範當取代中包含零個萬用字元時，所有比對到的值都會以字面取代字串來取代：
  
```sql
source=accounts
| replace "*IL*" WITH "Illinois" IN state
| fields state
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
```text
fetched rows / total rows = 4/4
+----------+
| state    |
|----------|
| Illinois |
| TN       |
| VA       |
| MD       |
+----------+
```
  

## 範例 11：比對字面星號  

使用 `\*` 來比對字面星號字元，並使用 `\\` 來比對字面反斜線字元。下列查詢使用 `\*`：
  
```sql
source=accounts
| eval note = 'price: *sale*'
| replace 'price: \*sale\*' WITH 'DISCOUNTED' IN note
| fields note
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
```text
fetched rows / total rows = 4/4
+------------+
| note       |
|------------|
| DISCOUNTED |
| DISCOUNTED |
| DISCOUNTED |
| DISCOUNTED |
+------------+
```

## 範例 12：以字面星號符號取代文字  

下列查詢示範如何在文字中插入字面星號符號，同時使用萬用字元保留模式的其他部分：
  
```sql
source=accounts
| eval label = 'file123.txt'
| replace 'file*.*' WITH '\**.*' IN label
| fields label
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
```text
fetched rows / total rows = 4/4
+----------+
| label    |
|----------|
| *123.txt |
| *123.txt |
| *123.txt |
| *123.txt |
+----------+
```
  

## 限制

`replace` 命令有下列限制：

* **萬用字元**：`*` 萬用字元會比對零個或多個字元，且區分大小寫。
* **萬用字元比對**：取代中的萬用字元數量必須與模式中的萬用字元數量相符，或為零。
* **逸出序列**：使用 `\*` 表示字面星號，並使用 `\\` 表示字面反斜線字元。  
