---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: sort
parent: Commands
grand_parent: PPL
nav_order: 43
---

<!-- vale off -->

# sort 命令

<!-- vale on -->

`sort` 命令會依指定的欄位排序搜尋結果。


## 語法

`sort` 命令支援兩種語法標記法。在單一 `sort` 命令中，您必須一致地使用其中一種標記法。

### 前置標記法

`sort` 命令使用前置標記法時語法如下：

```sql
sort [<count>] [+|-] <field> [, [+|-] <field>]...
```

### 後置標記法

`sort` 命令使用後置標記法時語法如下：

```sql
sort [<count>] <field> [asc|desc|a|d] [, <field> [asc|desc|a|d]]...
```

## 參數

`sort` 命令支援下列參數。

| 參數 | 必要/選用 | 說明 |
| --- | --- | --- |
| `<field>` | 必要 | 用於排序的欄位。使用 `auto(field)`、`str(field)`、`ip(field)` 或 `num(field)` 指定如何解讀欄位值。可以逗號分隔的清單指定多個欄位。 |
| `<count>` | 選用 | 要傳回的結果數。值為 `0` 或更少時會傳回所有結果。預設為 `0`。 |
| `[+|-]` | 選用 | **僅限前置標記法。** 加號 (`+`) 指定遞增順序，減號 (`-`) 指定遞減順序。預設為遞增順序。 |
| `[asc|desc|a|d]` | 選用 | **僅限後置標記法。** 指定排序順序：`asc`/`a` 為遞增，`desc`/`d` 為遞減。預設為遞增順序。 |

## 範例 1：依單一欄位排序

下列查詢依嚴重性編號遞增排序記錄檔，先顯示嚴重性最低的項目：

```sql
source=otellogs
| sort severityNumber
| fields severityText, severityNumber, `resource.attributes.service.name`
| head 4
```
{% include copy.html %}
{% include try-in-playground.html %}

查詢會傳回下列結果：

<!-- vale off -->

| severityText | severityNumber | resource.attributes.service.name |
| --- | --- | --- |
| DEBUG | 5 | cart |
| DEBUG | 5 | product-catalog |
| DEBUG | 5 | cart |
| INFO | 9 | frontend |

<!-- vale on -->


## 範例 2：依單一欄位遞減排序

下列查詢依嚴重性遞減排序記錄檔，以優先呈現最嚴重的問題。您可以使用前置標記法 (`- severityNumber`) 或後置標記法 (`severityNumber desc`)：

```sql
source=otellogs
| dedup severityText
| sort - severityNumber
| fields severityText, severityNumber
```
{% include copy.html %}
{% include try-in-playground.html %}

此查詢等同於下列查詢：

```sql
source=otellogs
| dedup severityText
| sort severityNumber desc
| fields severityText, severityNumber
```
{% include copy.html %}
{% include try-in-playground.html %}

查詢會傳回下列結果：

<!-- vale off -->

| severityText | severityNumber |
| --- | --- |
| ERROR | 17 |
| WARN | 13 |
| INFO | 9 |
| DEBUG | 5 |

<!-- vale on -->


## 範例 3：依多個欄位排序

下列查詢依嚴重性遞減及服務名稱遞增排序錯誤，因此最嚴重的問題會先出現，且在每個嚴重性層級內服務會依字母順序排列。您可以使用前置標記法 (`+`/`-`) 或後置標記法 (`asc`/`desc`)：
  
```sql
source=otellogs
| dedup severityText, `resource.attributes.service.name`
| sort + severityNumber, - `resource.attributes.service.name`
| fields severityText, severityNumber, `resource.attributes.service.name`
| head 5
```
{% include copy.html %}
{% include try-in-playground.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| severityText | severityNumber | resource.attributes.service.name |
| --- | --- | --- |
| DEBUG | 5 | product-catalog |
| DEBUG | 5 | cart |
| INFO | 9 | frontend |
| INFO | 9 | checkout |
| INFO | 9 | cart |

<!-- vale on -->

使用後置標記法的等效查詢為：

```sql
source=otellogs
| dedup severityText, `resource.attributes.service.name`
| sort severityNumber asc, `resource.attributes.service.name` desc
| fields severityText, severityNumber, `resource.attributes.service.name`
| head 5
```
{% include copy.html %}
{% include try-in-playground.html %}

查詢會傳回下列結果：

<!-- vale off -->

| severityText | severityNumber | resource.attributes.service.name |
| --- | --- | --- |
| DEBUG | 5 | product-catalog |
| DEBUG | 5 | cart |
| INFO | 9 | frontend |
| INFO | 9 | checkout |
| INFO | 9 | cart |

<!-- vale on -->
  

## 範例 4：排序含 null 值的欄位

預設的遞增順序會先列出 null 值。下列查詢依 `instrumentationScope.name` 欄位排序，顯示沒有檢測中繼資料的記錄檔會出現在已加入檢測資訊的記錄檔之前：
  
```sql
source=otellogs
| sort instrumentationScope.name
| fields instrumentationScope.name, severityText
| head 6
```
{% include copy.html %}
{% include try-in-playground.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| instrumentationScope.name | severityText |
| --- | --- |
| null | DEBUG |
| null | ERROR |
| null | INFO |
| null | ERROR |
| null | WARN |
| null | INFO |

<!-- vale on -->
  

## 範例 6：指定要傳回的已排序文件數  

下列查詢依嚴重性排序所有記錄檔，並只傳回嚴重性最低的 3 個項目：
  
```sql
source=otellogs
| sort 3 severityNumber
| fields severityText, severityNumber
```
{% include copy.html %}
{% include try-in-playground.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| severityText | severityNumber |
| --- | --- |
| DEBUG | 5 |
| DEBUG | 5 |
| DEBUG | 5 |

<!-- vale on -->
  

## 範例 7：指定欄位類型進行排序

下列查詢使用 `str()` 以字典順序而非數值順序排序嚴重性編號。請注意，`5` 和 `9` 會出現在 `21` 之後，因為字串排序會逐字元比較：

```sql
source=otellogs
| dedup severityText
| sort str(severityNumber)
| fields severityText, severityNumber
```
{% include copy.html %}
{% include try-in-playground.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| severityText | severityNumber |
| --- | --- |
| WARN | 13 |
| ERROR | 17 |
| DEBUG | 5 |
| INFO | 9 |

<!-- vale on -->
  