---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: lookup
parent: Commands
grand_parent: PPL
nav_order: 27
---

<!-- vale off -->

# lookup 命令

<!-- vale on -->

`lookup` 命令透過新增或取代來自查詢索引 (維度表) 的值，以充實搜尋資料。它可讓您使用維度表中的值擴充索引中的欄位，並在查詢條件符合時附加或取代值。與 `join` 命令相比，`lookup` 更適合使用靜態資料集來充實來源資料。

## 語法

`lookup` 命令的語法如下：

```sql
lookup <lookupIndex> (<lookupMappingField> [as <sourceMappingField>])... [(replace | append | output) (<inputField> [as <outputField>])...]
```

以下是 `lookup` 命令語法的範例：

```sql
source = table1 | lookup table2 id
source = table1 | lookup table2 id, name
source = table1 | lookup table2 id as cid, name
source = table1 | lookup table2 id as cid, name replace dept as department
source = table1 | lookup table2 id as cid, name replace dept as department, city as location
source = table1 | lookup table2 id as cid, name append dept as department
source = table1 | lookup table2 id as cid, name append dept as department, city as location
source = table1 | lookup table2 id as cid, name output dept as department
source = table1 | lookup table2 id as cid, name output dept as department, city as location
```

## 參數

`lookup` 命令支援下列參數。

| 參數 | 必要/選用 | 說明 |
| --- | --- | --- |
| `<lookupIndex>` | 必要 | 查詢索引 (維度表) 的名稱。 |
| `<lookupMappingField>` | 必要 | 查詢索引中用於比對的鍵，類似右側資料表中的聯結鍵。可指定多個欄位，以逗號分隔。 |
| `<sourceMappingField>` | 選用 | 來源資料 (左側) 中用於比對的鍵，類似左側資料表中的聯結鍵。預設為 `lookupMappingField`。 |
| `<inputField>` | 選用 | 查詢索引中的欄位，其符合的值會套用至結果 (輸出)。可指定多個欄位，以逗號分隔。若未指定，查詢索引中除 `lookupMappingField` 以外的所有欄位都會套用至結果。 |
| `<outputField>` | 選用 | 結果 (輸出) 中放置符合值的欄位名稱。可指定多個欄位，以逗號分隔。若 `outputField` 指定來源查詢中已存在的欄位，其值會被取代或附加來自 `inputField` 的符合值。若 `outputField` 中指定的欄位不是已存在的欄位，使用 `replace` 時會在結果中新增欄位，使用 `append` 時則操作會失敗。 |
| `(replace \| append \| output)` | 選用 | 指定符合值如何套用至輸出。`replace` 會以查詢索引中的符合值覆寫現有值。`append` 僅以查詢索引中的符合值填補結果中缺少的值。`output` 是 `replace` 的同義詞 (為了 SPL 相容性而提供)。預設為 `replace`。 |
  
## 範例 1：取代現有值  

下列查詢使用 `lookup` 命令搭配 `replace` 策略來覆寫現有值：  
  
```sql
source = worker
  | LOOKUP work_information uid AS id REPLACE department
  | fields id, name, occupation, country, salary, department
```
{% include copy.html %}
  
查詢會傳回下列結果：

<!-- vale off -->

| id | name | occupation | country | salary | department |
| --- | --- | --- | --- | --- | --- |
| 1000 | Jake | Engineer | England | 100000 | IT |
| 1001 | Hello | Artist | USA | 70000 | null |
| 1002 | John | Doctor | Canada | 120000 | DATA |
| 1003 | David | Doctor | null | 120000 | HR |
| 1004 | David | null | Canada | 0 | null |
| 1005 | Jane | Scientist | Canada | 90000 | DATA |

<!-- vale on -->
  

## 範例 2：附加缺少的值  

下列查詢使用 `lookup` 命令搭配 `append` 策略，僅附加缺少的值：
  
```sql
source = worker
  | LOOKUP work_information uid AS id APPEND department
  | fields id, name, occupation, country, salary, department
```
{% include copy.html %}
  

## 範例 3：不指定輸入欄位  

下列查詢使用 `lookup` 命令但不指定 `inputField`，這會將查詢索引中的所有欄位新增至結果：
  
```sql
  source = worker
  | LOOKUP work_information uid AS id, name
  | fields id, name, occupation, country, salary, department
```
{% include copy.html %}
  
查詢會傳回下列結果：

<!-- vale off -->

| id | name | country | salary | department | occupation |
| --- | --- | --- | --- | --- | --- |
| 1000 | Jake | England | 100000 | IT | Engineer |
| 1001 | Hello | USA | 70000 | null | null |
| 1002 | John | Canada | 120000 | DATA | Scientist |
| 1003 | David | null | 120000 | HR | Doctor |
| 1004 | David | Canada | 0 | null | null |
| 1005 | Jane | Canada | 90000 | DATA | Engineer |

<!-- vale on -->
  
## 範例 4：將符合值新增至新欄位

下列查詢將符合值放入 `outputField` 指定的新欄位：
  
```sql
  source = worker
  | LOOKUP work_information name REPLACE occupation AS new_col
  | fields id, name, occupation, country, salary, new_col
```
{% include copy.html %}
  
查詢會傳回下列結果：

<!-- vale off -->

| id | name | occupation | country | salary | new_col |
| --- | --- | --- | --- | --- | --- |
| 1003 | David | Doctor | null | 120000 | Doctor |
| 1004 | David | null | Canada | 0 | Doctor |
| 1001 | Hello | Artist | USA | 70000 | null |
| 1000 | Jake | Engineer | England | 100000 | Engineer |
| 1005 | Jane | Scientist | Canada | 90000 | Engineer |
| 1002 | John | Doctor | Canada | 120000 | Scientist |

<!-- vale on -->

## 範例 5：使用 OUTPUT 關鍵字

`OUTPUT` 關鍵字是 `REPLACE` 的同義詞。下列查詢示範使用 `OUTPUT` 來覆寫現有值：

```sql
source = worker
  | LOOKUP work_information uid AS id OUTPUT department
  | fields id, name, occupation, country, salary, department
```
{% include copy.html %}

此查詢產生的結果與範例 1 (使用 `REPLACE`) 相同：

<!-- vale off -->

| id | name | occupation | country | salary | department |
| --- | --- | --- | --- | --- | --- |
| 1000 | Jake | Engineer | England | 100000 | IT |
| 1001 | Hello | Artist | USA | 70000 | null |
| 1002 | John | Doctor | Canada | 120000 | DATA |
| 1003 | David | Doctor | null | 120000 | HR |
| 1004 | David | null | Canada | 0 | null |
| 1005 | Jane | Scientist | Canada | 90000 | DATA |

<!-- vale on -->
