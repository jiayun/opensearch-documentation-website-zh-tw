---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "運算式"
parent: Functions
grand_parent: PPL
nav_order: 7
---

# PPL 中的運算式

運算式，特別是值運算式，會傳回純量值。運算式有不同的類型與形式。例如，有作為原子運算式的字面值，也有建構在其之上的算術、述詞與函式運算式。您可以在不同的子句中使用運算式，例如在 `Filter` 或 `Stats` 命令中使用算術運算式。

## 算術運算子

算術運算式由數值字面值與二元算術運算子組合而成。可用的運算子如下：
1. `+`：加法
2. `-`：減法
3. `*`：乘法
4. `/`：除法。當 [`plugins.ppl.syntax.legacy.preferred`]({{site.url}}{{site.baseurl}}/sql-and-ppl/settings/) 為 `true`（預設）時，整數運算元會遵循舊式的截斷結果。當該設定為 `false` 時，運算元會升級為浮點數，保留小數部分。除以零會傳回 `NULL`。
5. `%`：取模。此運算子只能用於整數，並傳回除法的餘數。

### 優先順序

您可以使用括號來控制算術運算子的優先順序。否則，優先順序較高的運算子會先執行。

### 類型轉換

系統在判斷要使用哪個運算子時，會執行隱含類型轉換。例如，將整數與實數相加會符合簽名 `+(double,double)`，結果為實數。相同的類型轉換規則也適用於函式呼叫。

### 範例

以下是不同類型算術運算式的範例：
  
```sql
source=accounts
| where age > (25 + 5)
| fields age
```
{% include copy.html %}
  
查詢會傳回以下結果：
  
<!-- vale off -->

| age |
| --- |
| 32 |
| 36 |
| 33 |

<!-- vale on -->
  
## 述詞運算子

述詞運算子是評估結果為 `true` 或 `false` 的運算式。

`MISSING` 與 `NULL` 值的比較遵循以下規則：
- `MISSING` 值只等於其他 `MISSING` 值，並且小於所有其他值。
- `NULL` 值等於其他 `NULL` 值，大於 `MISSING` 值，但小於所有其他值。

### 運算子
  
| 名稱 | 說明 |
| --- | --- |
| `>` | 大於 |
| `>=` | 大於或等於 |
| `<` | 小於 |
| `!=` | 不等於 |
| `<=` | 小於或等於 |
| `=` | 等於 |
| `==` | 等於（替代語法） |
| `LIKE` | 簡單模式比對 |
| `IN` | 值清單成員測試 |
| `AND` | 邏輯 AND |
| `OR` | 邏輯 OR |
| `XOR` | 邏輯 XOR |
| `NOT` | 邏輯 NOT |
  
您可以比較日期與時間值。比較不同的日期與時間類型時（例如 `DATE` 與 `TIME`），兩個值都會轉換為 `DATETIME`。

系統會套用以下轉換規則：
- `TIME` 值會與今天的日期合併。
- `DATE` 值會被解讀為該日期的午夜。

### 範例

以下範例示範如何在 PPL 查詢中使用述詞運算子。

#### 基本述詞運算子

以下是比較運算子的範例：
  
```sql
source=accounts
| where age > 33
| fields age
```
{% include copy.html %}
  
查詢會傳回以下結果：
  
<!-- vale off -->

| age |
| --- |
| 36 |

<!-- vale on -->
  
`==` 運算子可以作為 `=` 的替代方式，用於相等比較。
  
```sql
source=accounts
| where age == 32
| fields age
```
{% include copy.html %}
  
查詢會傳回以下結果：
  
<!-- vale off -->

| age |
| --- |
| 32 |

<!-- vale on -->
  
`=` 與 `==` 執行相同的相等比較。您可以依偏好任選其一使用。
{: .note}

#### IN

`IN` 運算子測試欄位值是否位於指定的值清單中。
  
```sql
source=accounts
| where age in (32, 33)
| fields age
```
{% include copy.html %}
  
查詢會傳回以下結果：
  
<!-- vale off -->

| age |
| --- |
| 32 |
| 33 |

<!-- vale on -->

#### OR

`OR` 運算子在兩個布林運算式之間執行邏輯 OR 運算。
  
```sql
source=accounts
| where age = 32 OR age = 33
| fields age
```
{% include copy.html %}
  
查詢會傳回以下結果：
  
<!-- vale off -->

| age |
| --- |
| 32 |
| 33 |

<!-- vale on -->

#### NOT

`NOT` 運算子執行邏輯 NOT 運算，對布林運算式取反。
  
```sql
source=accounts
| where not age in (32, 33)
| fields age
```
{% include copy.html %}
  
查詢會傳回以下結果：
  
<!-- vale off -->

| age |
| --- |
| 36 |
| 28 |

<!-- vale on -->
