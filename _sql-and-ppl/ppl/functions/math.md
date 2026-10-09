---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "數學函式"
parent: Functions
grand_parent: PPL
nav_order: 10
---

# 數學函式

PPL 支援下列數學函式。

## ABS

**用法**：`ABS(x)`

計算 `x` 的絕對值。

**參數**：

- `x` (必要)：`INTEGER`、`LONG`、`FLOAT` 或 `DOUBLE` 值。

**傳回類型**：`INTEGER`、`LONG`、`FLOAT` 或 `DOUBLE` (與輸入相同類型)

### 範例
  
```sql
source=people
| eval `ABS(-1)` = ABS(-1)
| fields `ABS(-1)`
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| ABS(-1) |
| --- |
| 1 |

<!-- vale on -->
  
## ADD

**用法**：`ADD(x, y)`

計算 `x` 與 `y` 的和。

**參數**：

- `x` (必要)：`INTEGER`、`LONG`、`FLOAT` 或 `DOUBLE` 值。
- `y` (必要)：`INTEGER`、`LONG`、`FLOAT` 或 `DOUBLE` 值。

**傳回類型**：`x` 與 `y` 之間較寬的數值類型

**同義詞**：加號 (`+`)

### 範例
  
```sql
source=people
| eval `ADD(2, 1)` = ADD(2, 1)
| fields `ADD(2, 1)`
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| ADD(2, 1) |
| --- |
| 3 |

<!-- vale on -->
  
## SUBTRACT

**用法**：`SUBTRACT(x, y)`

計算 `x` 減 `y`。

**參數**：

- `x` (必要)：`INTEGER`、`LONG`、`FLOAT` 或 `DOUBLE` 值。
- `y` (必要)：`INTEGER`、`LONG`、`FLOAT` 或 `DOUBLE` 值。

**傳回類型**：`x` 與 `y` 之間較寬的數值類型

**同義詞**：減號 (`-`)

### 範例
  
```sql
source=people
| eval `SUBTRACT(2, 1)` = SUBTRACT(2, 1)
| fields `SUBTRACT(2, 1)`
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| SUBTRACT(2, 1) |
| --- |
| 1 |

<!-- vale on -->
  
## MULTIPLY

**用法**：`MULTIPLY(x, y)`

計算 `x` 與 `y` 的乘積。

**參數**：

- `x` (必要)：`INTEGER`、`LONG`、`FLOAT` 或 `DOUBLE` 值。
- `y` (必要)：`INTEGER`、`LONG`、`FLOAT` 或 `DOUBLE` 值。

**傳回類型**：`x` 與 `y` 之間較寬的數值類型

**同義詞**：乘號 (`*`)

### 範例
  
```sql
source=people
| eval `MULTIPLY(2, 1)` = MULTIPLY(2, 1)
| fields `MULTIPLY(2, 1)`
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| MULTIPLY(2, 1) |
| --- |
| 2 |

<!-- vale on -->
  
## DIVIDE

**用法**：`DIVIDE(x, y)`

計算 `x` 除以 `y`。

**參數**：

- `x` (必要)：`INTEGER`、`LONG`、`FLOAT` 或 `DOUBLE` 值。
- `y` (必要)：`INTEGER`、`LONG`、`FLOAT` 或 `DOUBLE` 值。

**傳回類型**：`x` 與 `y` 之間較寬的數值類型

**同義詞**：除號 (`/`)

### 範例
  
```sql
source=people
| eval `DIVIDE(2, 1)` = DIVIDE(2, 1)
| fields `DIVIDE(2, 1)`
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| DIVIDE(2, 1) |
| --- |
| 2 |

<!-- vale on -->
  
## SUM

**用法**：`SUM(x, y, ...)`

計算所有提供之引數的總和。此函式接受可變數量的引數。

此函式僅適用於 `eval` 命令情境，並在查詢解析期間改寫為算術加法。
{: .note}

**參數**：

- `x, y, ...` (必要)：可變數量的 `INTEGER`、`LONG`、`FLOAT` 或 `DOUBLE` 引數。

**傳回類型**：所有引數中最寬的數值類型

### 範例
  
```sql
source=accounts
| eval `SUM(1, 2, 3)` = SUM(1, 2, 3)
| fields `SUM(1, 2, 3)`
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| SUM(1, 2, 3) |
| --- |
| 6 |
| 6 |
| 6 |
| 6 |

<!-- vale on -->
  
```sql
source=accounts
| eval total = SUM(age, 10, 5)
| fields age, total
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| age | total |
| --- | --- |
| 32 | 47 |
| 36 | 51 |
| 28 | 43 |
| 33 | 48 |

<!-- vale on -->
  
## AVG

**用法**：`AVG(x, y, ...)`

計算所有提供之引數的平均值 (算術平均數)。此函式接受可變數量的引數。

此函式僅適用於 `eval` 命令情境，並在查詢解析期間改寫為算術運算式 (總和或計數)。
{: .note}

**參數**：

- `x, y, ...` (必要)：可變數量的 `INTEGER`、`LONG`、`FLOAT` 或 `DOUBLE` 引數。

**傳回類型**：`DOUBLE`

### 範例
  
```sql
source=accounts
| eval `AVG(1, 2, 3)` = AVG(1, 2, 3)
| fields `AVG(1, 2, 3)`
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| AVG(1, 2, 3) |
| --- |
| 2.0 |
| 2.0 |
| 2.0 |
| 2.0 |

<!-- vale on -->
  
```sql
source=accounts
| eval average = AVG(age, 30)
| fields age, average
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| age | average |
| --- | --- |
| 32 | 31.0 |
| 36 | 33.0 |
| 28 | 29.0 |
| 33 | 31.5 |

<!-- vale on -->
  
## ACOS

**用法**：`ACOS(x)`

計算 `x` 的反餘弦。若 `x` 不在 `[-1, 1]` 範圍內，則傳回 `NULL`。

**參數**：

- `x` (必要)：`INTEGER`、`LONG`、`FLOAT` 或 `DOUBLE` 值。

**傳回類型**：`DOUBLE`

### 範例
  
```sql
source=people
| eval `ACOS(0)` = ACOS(0)
| fields `ACOS(0)`
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| ACOS(0) |
| --- |
| 1.5707963267948966 |

<!-- vale on -->
  
## ASIN

**用法**：`ASIN(x)`

計算 `x` 的反正弦。若 `x` 不在 `[-1, 1]` 範圍內，則傳回 `NULL`。

**參數**：

- `x` (必要)：`INTEGER`、`LONG`、`FLOAT` 或 `DOUBLE` 值。

**傳回類型**：`DOUBLE`

### 範例
  
```sql
source=people
| eval `ASIN(0)` = ASIN(0)
| fields `ASIN(0)`
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| ASIN(0) |
| --- |
| 0.0 |

<!-- vale on -->
  
## ATAN

**用法**：`ATAN(x)`、`ATAN(y, x)`

計算 `x` 的反正切。`ATAN(y, x)` 會計算商 `y / x` 的反正切，並使用兩個引數的正負號來判斷結果所在的象限。

**參數**：

- `x` (必要)：`INTEGER`、`LONG`、`FLOAT` 或 `DOUBLE` 值。
- `y` (選用)：`INTEGER`、`LONG`、`FLOAT` 或 `DOUBLE` 值 (使用雙引數形式時)。

**傳回類型**：`DOUBLE`

### 範例
  
```sql
source=people
| eval `ATAN(2)` = ATAN(2), `ATAN(2, 3)` = ATAN(2, 3)
| fields `ATAN(2)`, `ATAN(2, 3)`
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| ATAN(2) | ATAN(2, 3) |
| --- | --- |
| 1.1071487177940904 | 0.5880026035475675 |

<!-- vale on -->
  
## ATAN2

**用法**：`ATAN2(y, x)`

計算商 `y / x` 的反正切，並使用兩個引數的正負號來判斷結果所在的象限。

**參數**：

- `y` (必要)：`INTEGER`、`LONG`、`FLOAT` 或 `DOUBLE` 值。
- `x` (必要)：`INTEGER`、`LONG`、`FLOAT` 或 `DOUBLE` 值。

**傳回類型**：`DOUBLE`

### 範例
  
```sql
source=people
| eval `ATAN2(2, 3)` = ATAN2(2, 3)
| fields `ATAN2(2, 3)`
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| ATAN2(2, 3) |
| --- |
| 0.5880026035475675 |

<!-- vale on -->
  
## CEIL

**用法**：`CEIL(x)`

傳回數值 `x` 向上取整後的值。

[CEILING](#ceiling) 函式的別名。

**參數**：

- `x` (必要)：`INTEGER`、`LONG`、`FLOAT` 或 `DOUBLE` 值。

**傳回類型**：與輸入相同類型

## CEILING

**用法**：`CEILING(x)`

傳回數值 `x` 的天花板值（向上取整）。

[`CEIL`](#ceil) 與 `CEILING` 函式具有相同的實作與功能。
{: .note}

限制：`CEILING` 只有在 IEEE 754 double 類型儲存時會顯示小數的情況下才能正常運作。

**參數**：

- `x`（必要）：一個 `INTEGER`、`LONG`、`FLOAT` 或 `DOUBLE` 值。

**回傳類型**：與輸入相同類型

### 範例
  
```sql
source=people
| eval `CEILING(0)` = CEILING(0), `CEILING(50.00005)` = CEILING(50.00005), `CEILING(-50.00005)` = CEILING(-50.00005)
| fields `CEILING(0)`, `CEILING(50.00005)`, `CEILING(-50.00005)`
```
{% include copy.html %}
  
查詢會傳回以下結果：
  
<!-- vale off -->

| CEILING(0) | CEILING(50.00005) | CEILING(-50.00005) |
| --- | --- | --- |
| 0 | 51.0 | -50.0 |

<!-- vale on -->
  
```sql
source=people
| eval `CEILING(3147483647.12345)` = CEILING(3147483647.12345), `CEILING(113147483647.12345)` = CEILING(113147483647.12345), `CEILING(3147483647.00001)` = CEILING(3147483647.00001)
| fields `CEILING(3147483647.12345)`, `CEILING(113147483647.12345)`, `CEILING(3147483647.00001)`
```
{% include copy.html %}
  
查詢會傳回以下結果：
  
<!-- vale off -->

| CEILING(3147483647.12345) | CEILING(113147483647.12345) | CEILING(3147483647.00001) |
| --- | --- | --- |
| 3147483648.0 | 113147483648.0 | 3147483648.0 |

<!-- vale on -->
  
## CONV

**用法**：`CONV(x, a, b)`

將數字 `x` 從 `a` 進位制轉換為 `b` 進位制。

**參數**：

- `x`（必要）：一個 `STRING` 值。
- `a`（必要）：一個 `INTEGER` 值。
- `b`（必要）：一個 `INTEGER` 值。

**回傳類型**：`STRING`

### 範例
  
```sql
source=people
| eval `CONV('12', 10, 16)` = CONV('12', 10, 16), `CONV('2C', 16, 10)` = CONV('2C', 16, 10), `CONV(12, 10, 2)` = CONV(12, 10, 2), `CONV(1111, 2, 10)` = CONV(1111, 2, 10)
| fields `CONV('12', 10, 16)`, `CONV('2C', 16, 10)`, `CONV(12, 10, 2)`, `CONV(1111, 2, 10)`
```
{% include copy.html %}
  
查詢會傳回以下結果：
  
<!-- vale off -->

| CONV('12', 10, 16) | CONV('2C', 16, 10) | CONV(12, 10, 2) | CONV(1111, 2, 10) |
| --- | --- | --- | --- |
| c | 44 | 1100 | 15 |

<!-- vale on -->
  
## COS

**用法**：`COS(x)`

計算 `x` 的餘弦值，其中 `x` 以弧度為單位。

**參數**：

- `x`（必要）：一個 `INTEGER`、`LONG`、`FLOAT` 或 `DOUBLE` 值。

**回傳類型**：`DOUBLE`

### 範例
  
```sql
source=people
| eval `COS(0)` = COS(0)
| fields `COS(0)`
```
{% include copy.html %}
  
查詢會傳回以下結果：
  
<!-- vale off -->

| COS(0) |
| --- |
| 1.0 |

<!-- vale on -->
  
## COSH

**用法**：`COSH(x)`

計算 `x` 的雙曲餘弦值，定義為 (((e^x) + (e^(-x))) / 2)。

**參數**：

- `x`（必要）：一個 `INTEGER`、`LONG`、`FLOAT` 或 `DOUBLE` 值。

**回傳類型**：`DOUBLE`

### 範例
  
```sql
source=people
| eval `COSH(2)` = COSH(2)
| fields `COSH(2)`
```
{% include copy.html %}
  
查詢會傳回以下結果：
  
<!-- vale off -->

| COSH(2) |
| --- |
| 3.7621956910836314 |

<!-- vale on -->
  
## COT

**用法**：`COT(x)`

計算 `x` 的餘切值。若 `x` 等於 0 則傳回錯誤。

**參數**：

- `x`（必要）：一個 `INTEGER`、`LONG`、`FLOAT` 或 `DOUBLE` 值。

**回傳類型**：`DOUBLE`

### 範例
  
```sql
source=people
| eval `COT(1)` = COT(1)
| fields `COT(1)`
```
{% include copy.html %}
  
查詢會傳回以下結果：
  
<!-- vale off -->

| COT(1) |
| --- |
| 0.6420926159343306 |

<!-- vale on -->
  
## CRC32

**用法**：`CRC32(expr)`

計算循環冗餘檢查（CRC）值，並傳回一個 32 位元無符號值。

**參數**：

- `expr`（必要）：一個 `STRING` 值。

**回傳類型**：`LONG`

### 範例
  
```sql
source=people
| eval `CRC32('MySQL')` = CRC32('MySQL')
| fields `CRC32('MySQL')`
```
{% include copy.html %}
  
查詢會傳回以下結果：
  
<!-- vale off -->

| CRC32('MySQL') |
| --- |
| 3259397556 |

<!-- vale on -->
  
## DEGREES

**用法**：`DEGREES(x)`

將 `x` 從弧度轉換為角度。

**參數**：

- `x`（必要）：一個 `INTEGER`、`LONG`、`FLOAT` 或 `DOUBLE` 值。

**回傳類型**：`DOUBLE`

### 範例
  
```sql
source=people
| eval `DEGREES(1.57)` = DEGREES(1.57)
| fields `DEGREES(1.57)`
```
{% include copy.html %}
  
查詢會傳回以下結果：
  
<!-- vale off -->

| DEGREES(1.57) |
| --- |
| 89.95437383553924 |

<!-- vale on -->
  
## E

**用法**：`E()`

傳回歐拉數（e ≈ 2.718281828459045）。

**參數**：無

**回傳類型**：`DOUBLE`

### 範例
  
```sql
source=people
| eval `E()` = E()
| fields `E()`
```
{% include copy.html %}
  
查詢會傳回以下結果：
  
<!-- vale off -->

| E() |
| --- |
| 2.718281828459045 |

<!-- vale on -->
  
## EXP

**用法**：`EXP(x)`

傳回 e 的 `x` 次方。

**參數**：

- `x`（必要）：一個 `INTEGER`、`LONG`、`FLOAT` 或 `DOUBLE` 值。

**回傳類型**：`DOUBLE`

### 範例
  
```sql
source=people
| eval `EXP(2)` = EXP(2)
| fields `EXP(2)`
```
{% include copy.html %}
  
查詢會傳回以下結果：
  
<!-- vale off -->

| EXP(2) |
| --- |
| 7.38905609893065 |

<!-- vale on -->
  
## EXPM1

**用法**：`EXPM1(x)`

傳回 e^x - 1（`x` 的指數減 1）。

**參數**：

- `x`（必要）：一個 `INTEGER`、`LONG`、`FLOAT` 或 `DOUBLE` 值。

**回傳類型**：`DOUBLE`

### 範例
  
```sql
source=people
| eval `EXPM1(1)` = EXPM1(1)
| fields `EXPM1(1)`
```
{% include copy.html %}
  
查詢會傳回以下結果：
  
<!-- vale off -->

| EXPM1(1) |
| --- |
| 1.718281828459045 |

<!-- vale on -->
  
## FLOOR

**用法**：`FLOOR(x)`

傳回數值 `x` 的地板值（向下取整）。

限制：`FLOOR` 只有在 IEEE 754 double 類型儲存時會顯示小數的情況下才能正常運作。

**參數**：

- `x`（必要）：一個 `INTEGER`、`LONG`、`FLOAT` 或 `DOUBLE` 值。

**回傳類型**：與輸入相同類型

### 範例
  
```sql
source=people
| eval `FLOOR(0)` = FLOOR(0), `FLOOR(50.00005)` = FLOOR(50.00005), `FLOOR(-50.00005)` = FLOOR(-50.00005)
| fields `FLOOR(0)`, `FLOOR(50.00005)`, `FLOOR(-50.00005)`
```
{% include copy.html %}
  
查詢會傳回以下結果：
  
<!-- vale off -->

| FLOOR(0) | FLOOR(50.00005) | FLOOR(-50.00005) |
| --- | --- | --- |
| 0 | 50.0 | -51.0 |

<!-- vale on -->
  
```sql
source=people
| eval `FLOOR(3147483647.12345)` = FLOOR(3147483647.12345), `FLOOR(113147483647.12345)` = FLOOR(113147483647.12345), `FLOOR(3147483647.00001)` = FLOOR(3147483647.00001)
| fields `FLOOR(3147483647.12345)`, `FLOOR(113147483647.12345)`, `FLOOR(3147483647.00001)`
```
{% include copy.html %}
  
查詢會傳回以下結果：
  
<!-- vale off -->

| FLOOR(3147483647.12345) | FLOOR(113147483647.12345) | FLOOR(3147483647.00001) |
| --- | --- | --- |
| 3147483647.0 | 113147483647.0 | 3147483647.0 |

<!-- vale on -->
  
```sql
source=people
| eval `FLOOR(282474973688888.022)` = FLOOR(282474973688888.022), `FLOOR(9223372036854775807.022)` = FLOOR(9223372036854775807.022), `FLOOR(9223372036854775807.0000001)` = FLOOR(9223372036854775807.0000001)
| fields `FLOOR(282474973688888.022)`, `FLOOR(9223372036854775807.022)`, `FLOOR(9223372036854775807.0000001)`
```
{% include copy.html %}
  
查詢會傳回以下結果：
  
<!-- vale off -->

| FLOOR(282474973688888.022) | FLOOR(9223372036854775807.022) | FLOOR(9223372036854775807.0000001) |
| --- | --- | --- |
| 282474973688888.0 | 9.223372036854776e+18 | 9.223372036854776e+18 |

<!-- vale on -->
  
## LN

**用法**：`LN(x)`

傳回 `x` 的自然對數。

**參數**：

- `x`（必要）：`INTEGER`、`LONG`、`FLOAT` 或 `DOUBLE` 值。

**回傳類型**：`DOUBLE`

### 範例
  
```sql
source=people
| eval `LN(2)` = LN(2)
| fields `LN(2)`
```
{% include copy.html %}
  
查詢會傳回以下結果：
  
<!-- vale off -->

| LN(2) |
| --- |
| 0.6931471805599453 |

<!-- vale on -->
  
## LOG

**用法**：`LOG(x)`、`LOG(B, x)`

傳回 `x` 的自然對數（以 e 為底的對數）。`LOG(B, x)` 等同於 log(x)/log(B)。

**參數**：

- `x`（必要）：`INTEGER`、`LONG`、`FLOAT` 或 `DOUBLE` 值。
- `B`（選用）：`INTEGER`、`LONG`、`FLOAT` 或 `DOUBLE` 值（使用雙參數形式時）。

**回傳類型**：`DOUBLE`

### 範例
  
```sql
source=people
| eval `LOG(2)` = LOG(2), `LOG(2, 8)` = LOG(2, 8)
| fields `LOG(2)`, `LOG(2, 8)`
```
{% include copy.html %}
  
查詢會傳回以下結果：
  
<!-- vale off -->

| LOG(2) | LOG(2, 8) |
| --- | --- |
| 0.6931471805599453 | 3.0 |

<!-- vale on -->
  
## LOG2

**用法**：`LOG2(x)`

傳回 `x` 以 2 為底的對數。等同於 log(x)/log(2)。

**參數**：

- `x`（必要）：`INTEGER`、`LONG`、`FLOAT` 或 `DOUBLE` 值。

**回傳類型**：`DOUBLE`

### 範例
  
```sql
source=people
| eval `LOG2(8)` = LOG2(8)
| fields `LOG2(8)`
```
{% include copy.html %}
  
查詢會傳回以下結果：
  
<!-- vale off -->

| LOG2(8) |
| --- |
| 3.0 |

<!-- vale on -->
  
## LOG10

**用法**：`LOG10(x)`

傳回 `x` 以 10 為底的對數。等同於 log(x)/log(10)。

**參數**：

- `x`（必要）：`INTEGER`、`LONG`、`FLOAT` 或 `DOUBLE` 值。

**回傳類型**：`DOUBLE`

### 範例
  
```sql
source=people
| eval `LOG10(100)` = LOG10(100)
| fields `LOG10(100)`
```
{% include copy.html %}
  
查詢會傳回以下結果：
  
<!-- vale off -->

| LOG10(100) |
| --- |
| 2.0 |

<!-- vale on -->
  
## MOD

**用法**：`MOD(n, m)`

計算數字 `n` 除以 `m` 的餘數。

**參數**：

- `n`（必要）：`INTEGER`、`LONG`、`FLOAT` 或 `DOUBLE` 值。
- `m`（必要）：`INTEGER`、`LONG`、`FLOAT` 或 `DOUBLE` 值。

**回傳類型**：若 `m` 為非零值，則傳回 `n` 與 `m` 之間較寬的類型。若 `m` 等於 `0`，則傳回 `NULL`。

### 範例
  
```sql
source=people
| eval `MOD(3, 2)` = MOD(3, 2), `MOD(3.1, 2)` = MOD(3.1, 2)
| fields `MOD(3, 2)`, `MOD(3.1, 2)`
```
{% include copy.html %}
  
查詢會傳回以下結果：
  
<!-- vale off -->

| MOD(3, 2) | MOD(3.1, 2) |
| --- | --- |
| 1 | 1.1 |

<!-- vale on -->
  
## MODULUS

**用法**：`MODULUS(n, m)`

計算數字 `n` 除以 `m` 的餘數。

**參數**：

- `n`（必要）：`INTEGER`、`LONG`、`FLOAT` 或 `DOUBLE` 值。
- `m`（必要）：`INTEGER`、`LONG`、`FLOAT` 或 `DOUBLE` 值。

**回傳類型**：若 `m` 為非零值，則傳回 `n` 與 `m` 之間較寬的類型。若 `m` 等於 `0`，則傳回 `NULL`。

### 範例
  
```sql
source=people
| eval `MODULUS(3, 2)` = MODULUS(3, 2), `MODULUS(3.1, 2)` = MODULUS(3.1, 2)
| fields `MODULUS(3, 2)`, `MODULUS(3.1, 2)`
```
{% include copy.html %}
  
查詢會傳回以下結果：
  
<!-- vale off -->

| MODULUS(3, 2) | MODULUS(3.1, 2) |
| --- | --- |
| 1 | 1.1 |

<!-- vale on -->
  
## PI

**用法**：`PI()`

傳回數學常數 π（pi ≈ 3.141592653589793）。

**參數**：無

**回傳類型**：`DOUBLE`

### 範例
  
```sql
source=people
| eval `PI()` = PI()
| fields `PI()`
```
{% include copy.html %}
  
查詢會傳回以下結果：
  
<!-- vale off -->

| PI() |
| --- |
| 3.141592653589793 |

<!-- vale on -->
  
## POW

**用法**：`POW(x, y)`

計算 `x` 的 `y` 次方值。無效的輸入會傳回 `NULL`。

**參數**：

- `x`（必要）：`INTEGER`、`LONG`、`FLOAT` 或 `DOUBLE` 值。
- `y`（必要）：`INTEGER`、`LONG`、`FLOAT` 或 `DOUBLE` 值。

**回傳類型**：`DOUBLE`

**同義詞**：[POWER](#power)

### 範例
  
```sql
source=people
| eval `POW(3, 2)` = POW(3, 2), `POW(-3, 2)` = POW(-3, 2), `POW(3, -2)` = POW(3, -2)
| fields `POW(3, 2)`, `POW(-3, 2)`, `POW(3, -2)`
```
{% include copy.html %}
  
查詢會傳回以下結果：
  
<!-- vale off -->

| POW(3, 2) | POW(-3, 2) | POW(3, -2) |
| --- | --- | --- |
| 9.0 | 9.0 | 0.1111111111111111 |

<!-- vale on -->
  
## POWER

**用法**：`POWER(x, y)`

計算 `x` 的 `y` 次方值。無效的輸入會傳回 `NULL`。

**參數**：

- `x`（必要）：`INTEGER`、`LONG`、`FLOAT` 或 `DOUBLE` 值。
- `y`（必要）：`INTEGER`、`LONG`、`FLOAT` 或 `DOUBLE` 值。

**回傳類型**：`DOUBLE`

**同義詞**：[POW](#pow)

### 範例
  
```sql
source=people
| eval `POWER(3, 2)` = POWER(3, 2), `POWER(-3, 2)` = POWER(-3, 2), `POWER(3, -2)` = POWER(3, -2)
| fields `POWER(3, 2)`, `POWER(-3, 2)`, `POWER(3, -2)`
```
{% include copy.html %}
  
查詢會傳回以下結果：
  
<!-- vale off -->

| POWER(3, 2) | POWER(-3, 2) | POWER(3, -2) |
| --- | --- | --- |
| 9.0 | 9.0 | 0.1111111111111111 |

<!-- vale on -->
  
## RADIANS

**用法**：`RADIANS(x)`

將 x 從角度轉換為弧度。

**參數**：

- `x`（必要）：`INTEGER`、`LONG`、`FLOAT` 或 `DOUBLE` 值。

**回傳類型**：`DOUBLE`

### 範例
  
```sql
source=people
| eval `RADIANS(90)` = RADIANS(90)
| fields `RADIANS(90)`
```
{% include copy.html %}
  
查詢會傳回以下結果：
  
<!-- vale off -->

| RADIANS(90) |
| --- |
| 1.5707963267948966 |

<!-- vale on -->
  
## RAND

**用法**：`RAND()`、`RAND(N)`

傳回 `[0, 1)` 範圍內的隨機浮點數值。若指定整數 `N`，則會在執行前初始化種子。因此，以相同的 `N` 值呼叫 `RAND(N)` 時，一律會傳回相同的結果，產生可重複的欄位值序列。

**參數**：

- `N`（選用）：`INTEGER` 值。

**回傳類型**：`FLOAT`

### 範例
  
```sql
source=people
| eval `RAND(3)` = RAND(3)
| fields `RAND(3)`
```
{% include copy.html %}
  
查詢會傳回以下結果：
  
<!-- vale off -->

| RAND(3) |
| --- |
| 0.34346429521113886 |

<!-- vale on -->
  
## ROUND

**用法**：`ROUND(x, d)`

將參數 `x` 四捨五入到 `d` 位小數。`d` 預設為 `0`。

**參數**：

- `x`（必要）：`INTEGER`、`LONG`、`FLOAT` 或 `DOUBLE` 值。
- `d`（選用）：`INTEGER` 值。

**回傳類型**：
- `(INTEGER/LONG [,INTEGER])` -> `LONG`。
- `(FLOAT/DOUBLE [,INTEGER])` -> `LONG`。

### 範例
  
```sql
source=people
| eval `ROUND(12.34)` = ROUND(12.34), `ROUND(12.34, 1)` = ROUND(12.34, 1), `ROUND(12.34, -1)` = ROUND(12.34, -1), `ROUND(12, 1)` = ROUND(12, 1)
| fields `ROUND(12.34)`, `ROUND(12.34, 1)`, `ROUND(12.34, -1)`, `ROUND(12, 1)`
```
{% include copy.html %}
  
查詢會傳回以下結果：
  
<!-- vale off -->

| ROUND(12.34) | ROUND(12.34, 1) | ROUND(12.34, -1) | ROUND(12, 1) |
| --- | --- | --- | --- |
| 12.0 | 12.3 | 10.0 | 12 |

<!-- vale on -->
  
## SIGN

**用法**：`SIGN(x)`

視數字為負數、零或正數，分別以 `-1`、`0` 或 `1` 傳回該參數的正負號。

**參數**：

- `x`（必要）：`INTEGER`、`LONG`、`FLOAT` 或 `DOUBLE` 值。

**回傳類型**：與輸入相同的類型

### 範例
  
```sql
source=people
| eval `SIGN(1)` = SIGN(1), `SIGN(0)` = SIGN(0), `SIGN(-1.1)` = SIGN(-1.1)
| fields `SIGN(1)`, `SIGN(0)`, `SIGN(-1.1)`
```
{% include copy.html %}
  
此查詢會傳回下列結果：
  
<!-- vale off -->

| SIGN(1) | SIGN(0) | SIGN(-1.1) |
| --- | --- | --- |
| 1 | 0 | -1.0 |

<!-- vale on -->
  
## SIGNUM

**用法**：`SIGNUM(x)`

傳回引數的正負號，會是 `-1`、`0` 或 `1`，取決於該數字為負數、零或正數。

**參數**：

- `x` (必要)：`INTEGER`、`LONG`、`FLOAT` 或 `DOUBLE` 值。

**傳回類型**：`INTEGER`

**同義詞**：`SIGN`

### 範例
  
```sql
source=people
| eval `SIGNUM(1)` = SIGNUM(1), `SIGNUM(0)` = SIGNUM(0), `SIGNUM(-1.1)` = SIGNUM(-1.1)
| fields `SIGNUM(1)`, `SIGNUM(0)`, `SIGNUM(-1.1)`
```
{% include copy.html %}
  
此查詢會傳回下列結果：
  
<!-- vale off -->

| SIGNUM(1) | SIGNUM(0) | SIGNUM(-1.1) |
| --- | --- | --- |
| 1 | 0 | -1.0 |

<!-- vale on -->
  
## SIN

**用法**：`SIN(x)`

計算 `x` 的正弦，其中 `x` 以弧度為單位。

**參數**：

- `x` (必要)：`INTEGER`、`LONG`、`FLOAT` 或 `DOUBLE` 值。

**傳回類型**：`DOUBLE`

### 範例
  
```sql
source=people
| eval `SIN(0)` = SIN(0)
| fields `SIN(0)`
```
{% include copy.html %}
  
此查詢會傳回下列結果：
  
<!-- vale off -->

| SIN(0) |
| --- |
| 0.0 |

<!-- vale on -->
  
## SINH

**用法**：`SINH(x)`

計算 `x` 的雙曲正弦，定義為 (((e^x) - (e^(-x))) / 2)。

**參數**：

- `x` (必要)：`INTEGER`、`LONG`、`FLOAT` 或 `DOUBLE` 值。

**傳回類型**：`DOUBLE`

### 範例
  
```sql
source=people
| eval `SINH(2)` = SINH(2)
| fields `SINH(2)`
```
{% include copy.html %}
  
此查詢會傳回下列結果：
  
<!-- vale off -->

| SINH(2) |
| --- |
| 3.626860407847019 |

<!-- vale on -->
  
## SQRT

**用法**：`SQRT(x)`

計算非負數 `x` 的平方根。

**參數**：

- `x` (必要)：`INTEGER`、`LONG`、`FLOAT` 或 `DOUBLE` 值。

**傳回類型**：
- `(Non-negative) INTEGER/LONG/FLOAT/DOUBLE` -> `DOUBLE`。
- `(Negative) INTEGER/LONG/FLOAT/DOUBLE` -> `NULL`。

### 範例
  
```sql
source=people
| eval `SQRT(4)` = SQRT(4), `SQRT(4.41)` = SQRT(4.41)
| fields `SQRT(4)`, `SQRT(4.41)`
```
{% include copy.html %}
  
此查詢會傳回下列結果：
  
<!-- vale off -->

| SQRT(4) | SQRT(4.41) |
| --- | --- |
| 2.0 | 2.1 |

<!-- vale on -->
  
## CBRT

**用法**：`CBRT(x)`

計算數字 `x` 的立方根。

**參數**：

- `x` (必要)：`INTEGER`、`LONG`、`FLOAT` 或 `DOUBLE` 值。

**傳回類型**：`DOUBLE`

### 範例
  
```sql
source=location
| eval `CBRT(8)` = CBRT(8), `CBRT(9.261)` = CBRT(9.261), `CBRT(-27)` = CBRT(-27)
| fields `CBRT(8)`, `CBRT(9.261)`, `CBRT(-27)`
```
{% include copy.html %}
  
此查詢會傳回下列結果：
  
<!-- vale off -->

| CBRT(8) | CBRT(9.261) | CBRT(-27) |
| --- | --- | --- |
| 2.0 | 2.1 | -3.0 |
| 2.0 | 2.1 | -3.0 |

<!-- vale on -->
  
## RINT

**用法**：`RINT(x)`

傳回 `x` 四捨五入至最接近的整數。

**參數**：

- `x` (必要)：`INTEGER`、`LONG`、`FLOAT` 或 `DOUBLE` 值。

**傳回類型**：`DOUBLE`

### 範例
  
```sql
source=people
| eval `RINT(1.7)` = RINT(1.7)
| fields `RINT(1.7)`
```
{% include copy.html %}
  
此查詢會傳回下列結果：
  
<!-- vale off -->

| RINT(1.7) |
| --- |
| 2.0 |

<!-- vale on -->
