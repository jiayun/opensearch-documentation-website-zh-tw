---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "條件式函式"
parent: Functions
grand_parent: PPL
nav_order: 3
---

# 條件式函式

PPL 條件式函式可根據特定條件（例如 `WHERE` 或 `HAVING` 子句）對查詢結果進行全域篩選。這些函式使用 OpenSearch 引擎的搜尋功能，但不會直接在 OpenSearch 外掛程式的記憶體中執行。

## ISNULL

**用法**：`isnull(field)`

若欄位為 `NULL`，則傳回 `TRUE`，否則傳回 `FALSE`。

`isnull()` 函式常用於：
- 在 `eval` 運算式中建立條件式欄位。
- 搭配 `if()` 函式提供預設值。
- 在 `where` 子句中篩選 null 記錄。

**參數**：

- `field` (必要)：要檢查 null 值的欄位。

**傳回類型**：`BOOLEAN`

#### 範例
  
```sql
source=accounts
| eval result = isnull(employer)
| fields result, employer, firstname
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| result | employer | firstname |
<!-- vale off -->

| --- | --- | --- |
| False | Pyrami | Amber |
| False | Netagy | Hattie |
| False | Quility | Nanette |
| True | null | Dale |

<!-- vale on -->

<!-- vale on -->

下列範例示範如何使用 `isnull` 搭配 `if` 函式建立條件式標籤：

```sql
source=accounts
| eval status = if(isnull(employer), 'unemployed', 'employed')
| fields firstname, employer, status
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| firstname | employer | status |
<!-- vale off -->

| --- | --- | --- |
| Amber | Pyrami | employed |
| Hattie | Netagy | employed |
| Nanette | Quility | employed |
| Dale | null | unemployed |

<!-- vale on -->

<!-- vale on -->
  
下列範例在 `where` 子句中使用 `isnull` 篩選記錄：

```sql
source=accounts
| where isnull(employer)
| fields account_number, firstname, employer
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| account_number | firstname | employer |
<!-- vale off -->

| --- | --- | --- |
| 18 | Dale | null |

<!-- vale on -->

<!-- vale on -->
  
## ISNOTNULL

**用法**：`isnotnull(field)`

若欄位「不是」`NULL`，則傳回 `TRUE`，否則傳回 `FALSE`。

`isnotnull()` 函式常用於：
- 在 `eval` 運算式中建立布林值旗標。
- 在 `where` 子句中篩除 null 值。
- 搭配 `if()` 函式進行條件式邏輯。
- 驗證資料是否存在。

**同義詞**：[ISPRESENT](#ispresent)

**參數**：

- `field` (必要)：要檢查非 null 值的欄位。

**傳回類型**：`BOOLEAN`

#### 範例
  
```sql
source=accounts
| eval has_employer = isnotnull(employer)
| fields firstname, employer, has_employer
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| firstname | employer | has_employer |
<!-- vale off -->

| --- | --- | --- |
| Amber | Pyrami | True |
| Hattie | Netagy | True |
| Nanette | Quility | True |
| Dale | null | False |

<!-- vale on -->

<!-- vale on -->

下列範例示範如何在 `where` 子句中使用 `isnotnull` 篩選記錄：

```sql
source=accounts
| where not isnotnull(employer)
| fields account_number, employer
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| account_number | employer |
<!-- vale off -->

| --- | --- |
| 18 | null |

<!-- vale on -->

<!-- vale on -->

下列範例示範如何使用 `isnotnull` 搭配 `if` 函式建立驗證訊息：

```sql
source=accounts
| eval validation = if(isnotnull(employer), 'valid', 'missing employer')
| fields firstname, employer, validation
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| firstname | employer | validation |
<!-- vale off -->

| --- | --- | --- |
| Amber | Pyrami | valid |
| Hattie | Netagy | valid |
| Nanette | Quility | valid |
| Dale | null | missing employer |

<!-- vale on -->

<!-- vale on -->
  
## EXISTS

**用法**：使用 `isnull(field)` 或 `isnotnull(field)` 測試欄位是否存在

由於 OpenSearch 不會區分 null 與缺少的值，因此無法使用 `ismissing`/`isnotmissing` 等函式。請改用 `isnull`/`isnotnull` 測試欄位是否存在。

#### 範例

下列範例顯示帳號 13，其中不含 `email` 欄位：
  
```sql
source=accounts
| where isnull(email)
| fields account_number, email
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| account_number | email |
<!-- vale off -->

| --- | --- |
| 13 | null |

<!-- vale on -->

<!-- vale on -->
  
## IFNULL

**用法**：`ifnull(field1, field2)`

若 `field1` 為 `NULL`，則傳回 `field2`。

**參數**：

- `field1` (必要)：要檢查 `NULL` 值的欄位。
- `field2` (必要)：若 `field1` 為 `NULL` 時要傳回的值。

**傳回類型**：Any (符合輸入類型)

#### 範例

```sql
source=accounts
| eval result = ifnull(employer, 'default')
| fields result, employer, firstname
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| result | employer | firstname |
<!-- vale off -->

| --- | --- | --- |
| Pyrami | Pyrami | Amber |
| Netagy | Netagy | Hattie |
| Quility | Quility | Nanette |
| default | null | Dale |

<!-- vale on -->

<!-- vale on -->
  
#### 巢狀 `ifnull` 模式

在 3.1 之前的 OpenSearch 版本中，可使用巢狀 `ifnull` 陳述式達成類似 `coalesce` 的功能。此模式在可觀測性使用案例中特別實用，因為欄位名稱可能因不同資料來源而異。
用法：`ifnull(field1, ifnull(field2, ifnull(field3, default_value)))`

#### 範例

```sql
source=accounts
| eval result = ifnull(employer, ifnull(firstname, ifnull(lastname, "unknown")))
| fields result, employer, firstname, lastname
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| result | employer | firstname | lastname |
<!-- vale off -->

| --- | --- | --- | --- |
| Pyrami | Pyrami | Amber | Duke |
| Netagy | Netagy | Hattie | Bond |
| Quility | Quility | Nanette | Bates |
| Dale | null | Dale | Adams |

<!-- vale on -->

<!-- vale on -->
  
## NULLIF

**用法**：`nullif(field1, field2)`

若兩個參數相同，則傳回 `NULL`，否則傳回 `field1`。

**參數**：

- `field1` (必要)：若與 `field2` 不同時要傳回的欄位。
- `field2` (必要)：要與 `field1` 比較的值。

**傳回類型**：Any (符合 `field1` 類型)

#### 範例

```sql
source=accounts
| eval result = nullif(employer, 'Pyrami')
| fields result, employer, firstname
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| result | employer | firstname |
<!-- vale off -->

| --- | --- | --- |
| null | Pyrami | Amber |
| Netagy | Netagy | Hattie |
| Quility | Quility | Nanette |
| null | null | Dale |

<!-- vale on -->

<!-- vale on -->
  
## IF

**用法**：`if(condition, expr1, expr2)`

若條件為 `true`，則傳回 `expr1`，否則傳回 `expr2`。

**參數**：

- `condition` (必要)：要評估的布林運算式。
- `expr1` (必要)：若條件為 `true` 時要傳回的值。
- `expr2` (必要)：若條件為 `false` 時要傳回的值。

**傳回類型**：`expr1` 與 `expr2` 中限制最少的共同類型

#### 範例

下列範例在條件為 `true` 時傳回名字 (first name)：

```sql
source=accounts
| eval result = if(true, firstname, lastname)
| fields result, firstname, lastname
```
{% include copy.html %}
  
查詢傳回下列結果：
  
<!-- vale off -->

| result | firstname | lastname |
<!-- vale off -->

| --- | --- | --- |
| Amber | Amber | Duke |
| Hattie | Hattie | Bond |
| Nanette | Nanette | Bates |
| Dale | Dale | Adams |

<!-- vale on -->

<!-- vale on -->

下列範例在條件為 `false` 時傳回姓氏 (last name)：

```sql
source=accounts
| eval result = if(false, firstname, lastname)
| fields result, firstname, lastname
```
{% include copy.html %}
  
查詢傳回下列結果：
  
<!-- vale off -->

| result | firstname | lastname |
<!-- vale off -->

| --- | --- | --- |
| Duke | Amber | Duke |
| Bond | Hattie | Bond |
| Bates | Nanette | Bates |
| Adams | Dale | Adams |

<!-- vale on -->

<!-- vale on -->

下列範例使用複雜條件來判斷 VIP 身分：

```sql
source=accounts
| eval is_vip = if(age > 30 AND isnotnull(employer), true, false)
| fields is_vip, firstname, lastname
```
{% include copy.html %}

查詢傳回下列結果：
  
<!-- vale off -->

| is_vip | firstname | lastname |
<!-- vale off -->

| --- | --- | --- |
| True | Amber | Duke |
| True | Hattie | Bond |
| False | Nanette | Bates |
| False | Dale | Adams |

<!-- vale on -->

<!-- vale on -->
  
## CASE

**用法**：`case(condition1, expr1, condition2, expr2, ... conditionN, exprN else default)`

當 `condition1` 為 `true` 時傳回 `expr1`，當 `condition2` 為 `true` 時傳回 `expr2`，依此類推。如果沒有任何條件為 `true`，則傳回 `else` 子句的值。如果未定義 `else` 子句，則傳回 `NULL`。

**參數**：

- `condition1, condition2, ..., conditionN` (必要)：依序評估的布林運算式。
- `expr1, expr2, ..., exprN` (必要)：當對應條件為 `true` 時要傳回的值。
- `default` (選用)：當沒有任何條件為 `true` 時要傳回的值。如果未指定，則傳回 `NULL`。

**回傳類型**：所有結果運算式中限制最少的共同類型

#### 限制

當每個條件都是欄位與數值實字的比較，且每個結果運算式都是字串實字時，如果已啟用 push-down 最佳化，查詢會最佳化為[範圍彙總]({{site.url}}{{site.baseurl}}/aggregations/bucket/range/)。不過，此最佳化有下列限制：
- `NULL` 值不會被歸入範圍彙總的任何桶，並會被忽略。
- 預設的 `else` 子句會使用字串實字 `"null"`，而非實際的 NULL 值。
  
#### 範例

下列範例示範帶有 else 子句的 case 敘述：

```sql
source=accounts
| eval result = case(age > 35, firstname, age < 30, lastname else employer)
| fields result, firstname, lastname, age, employer
```
{% include copy.html %}
  
查詢傳回下列結果：
  
<!-- vale off -->

| result | firstname | lastname | age | employer |
<!-- vale off -->

| --- | --- | --- | --- | --- |
| Pyrami | Amber | Duke | 32 | Pyrami |
| Hattie | Hattie | Bond | 36 | Netagy |
| Bates | Nanette | Bates | 28 | Quility |
| null | Dale | Adams | 33 | null |

<!-- vale on -->

<!-- vale on -->

下列範例示範不帶 else 子句的 case 敘述：

```sql
source=accounts
| eval result = case(age > 35, firstname, age < 30, lastname)
| fields result, firstname, lastname, age
```
{% include copy.html %}
  
查詢傳回下列結果：
  
<!-- vale off -->

| result | firstname | lastname | age |
<!-- vale off -->

| --- | --- | --- | --- |
| null | Amber | Duke | 32 |
| Hattie | Hattie | Bond | 36 |
| Bates | Nanette | Bates | 28 |
| null | Dale | Adams | 33 |

<!-- vale on -->

<!-- vale on -->

下列範例在 where 子句中使用 case 來篩選記錄：

```sql
source=accounts
| where true = case(age > 35, false, age < 30, false else true)
| fields firstname, lastname, age
```
{% include copy.html %}
  
查詢傳回下列結果：
  
<!-- vale off -->

| firstname | lastname | age |
<!-- vale off -->

| --- | --- | --- |
| Amber | Duke | 32 |
| Dale | Adams | 33 |

<!-- vale on -->

<!-- vale on -->
  
## COALESCE

**用法**：`coalesce(field1, field2, ...)`

傳回參數清單中第一個非 null 且非缺失的值。

**參數**：

- `field1, field2, ...` (必要)：要評估非 null 值的欄位或運算式。

**回傳類型**：所有輸入參數中限制最少的共同類型

**行為**：
- 傳回第一個不為 `NULL` 且不缺失的值 (缺失包括不存在的欄位)。
- 空字串 (`""`) 與空白字串 (`" "`) 視為有效值。
- 如果所有參數皆為 `NULL` 或缺失，則傳回 `NULL`。
- 會套用自動型別強制轉換，以符合決定的回傳類型。
- 如果型別轉換失敗，該值會轉換為字串表示法。
- 為獲得最佳結果，請使用相同資料類型的參數，以避免非預期的型別轉換。

**效能考量**：
- 針對多欄位評估進行最佳化，比巢狀 `ifnull` 模式更有效率。
- 依序評估參數，在第一個非 null 值處停止。
- 請依包含值的可能性考量欄位順序，以將評估負擔降至最低。

**限制**：
- 型別強制轉換可能導致不相容類型發生非預期的字串轉換。
- 使用大量引數時，效能可能會降低。

#### 範例

```sql
source=accounts
| eval result = coalesce(employer, firstname, lastname)
| fields result, firstname, lastname, employer
```
{% include copy.html %}
  
查詢傳回下列結果：
  
<!-- vale off -->

| result | firstname | lastname | employer |
<!-- vale off -->

| --- | --- | --- | --- |
| Pyrami | Amber | Duke | Pyrami |
| Netagy | Hattie | Bond | Netagy |
| Quility | Nanette | Bates | Quility |
| Dale | Dale | Adams | null |

<!-- vale on -->

<!-- vale on -->
  
#### 空字串處理範例
  
```sql
source=accounts
| eval empty_field = ""
| eval result = coalesce(empty_field, firstname)
| fields result, empty_field, firstname
```
{% include copy.html %}
  
查詢傳回下列結果：
  
<!-- vale off -->

| result | empty_field | firstname |
<!-- vale off -->

| --- | --- | --- |
|  |  | Amber |
|  |  | Hattie |
|  |  | Nanette |
|  |  | Dale |

<!-- vale on -->

<!-- vale on -->
  
```sql
source=accounts
| eval result = coalesce(" ", firstname)
| fields result, firstname
```
{% include copy.html %}
  
查詢傳回下列結果：
  
<!-- vale off -->

| result | firstname |
<!-- vale off -->

| --- | --- |
|  | Amber |
|  | Hattie |
|  | Nanette |
|  | Dale |

<!-- vale on -->

<!-- vale on -->
  
#### 混合資料類型與自動強制轉換
  
```sql
source=accounts
| eval result = coalesce(employer, balance, "fallback")
| fields result, employer, balance
```
{% include copy.html %}
  
查詢傳回下列結果：
  
<!-- vale off -->

| result | employer | balance |
<!-- vale off -->

| --- | --- | --- |
| Pyrami | Pyrami | 39225 |
| Netagy | Netagy | 5686 |
| Quility | Quility | 32838 |
| 4180 | null | 4180 |

<!-- vale on -->

<!-- vale on -->
  
#### 不存在欄位的處理
  
```sql
source=accounts
| eval result = coalesce(nonexistent_field, firstname, "unknown")
| fields result, firstname
```
{% include copy.html %}
  
此查詢會傳回下列結果：
  
<!-- vale off -->

| result | firstname |
<!-- vale off -->

| --- | --- |
| Amber | Amber |
| Hattie | Hattie |
| Nanette | Nanette |
| Dale | Dale |

<!-- vale on -->

<!-- vale on -->
  
## ISPRESENT

**用法**：`ispresent(field)`

若欄位存在則傳回 `TRUE`，否則傳回 `FALSE`。

**參數**：

- `field` (必要)：要檢查是否存在的欄位。

**傳回類型**：`BOOLEAN`

**同義詞**：[ISNOTNULL](#isnotnull)

#### 範例

```sql
source=accounts
| where ispresent(employer)
| fields employer, firstname
```
{% include copy.html %}
  
此查詢會傳回下列結果：
  
<!-- vale off -->

| employer | firstname |
<!-- vale off -->

| --- | --- |
| Pyrami | Amber |
| Netagy | Hattie |
| Quility | Nanette |

<!-- vale on -->

<!-- vale on -->
  
## ISBLANK

**用法**：`isblank(field)`

若欄位為 `NULL`、空字串或僅包含空白字元，則傳回 `TRUE`。

**參數**：

- `field` (必要)：要檢查是否為空白值的欄位。

**傳回類型**：`BOOLEAN`

#### 範例

```sql
source=accounts
| eval temp = ifnull(employer, '   ')
| eval `isblank(employer)` = isblank(employer), `isblank(temp)` = isblank(temp)
| fields `isblank(temp)`, temp, `isblank(employer)`, employer
```
{% include copy.html %}
  
此查詢會傳回下列結果：
  
<!-- vale off -->

| isblank(temp) | temp | isblank(employer) | employer |
<!-- vale off -->

| --- | --- | --- | --- |
| False | Pyrami | False | Pyrami |
| False | Netagy | False | Netagy |
| False | Quility | False | Quility |
| True |  | True | null |

<!-- vale on -->

<!-- vale on -->
  
## ISEMPTY

**用法**：`isempty(field)`

若欄位為 `NULL` 或空字串，則傳回 `TRUE`。

**參數**：

- `field` (必要)：要檢查是否為空值的欄位。

**傳回類型**：`BOOLEAN`

#### 範例

```sql
source=accounts
| eval temp = ifnull(employer, '   ')
| eval `isempty(employer)` = isempty(employer), `isempty(temp)` = isempty(temp)
| fields `isempty(temp)`, temp, `isempty(employer)`, employer
```
{% include copy.html %}
  
此查詢會傳回下列結果：
  
<!-- vale off -->

| isempty(temp) | temp | isempty(employer) | employer |
<!-- vale off -->

| --- | --- | --- | --- |
| False | Pyrami | False | Pyrami |
| False | Netagy | False | Netagy |
| False | Quility | False | Quility |
| False |  | True | null |

<!-- vale on -->

<!-- vale on -->
  
## EARLIEST

**用法**：`earliest(relative_string, field)`

若欄位值晚於從 `relative_string` 相對於目前時間所推算出的時間戳記，則傳回 `TRUE`，否則傳回 `FALSE`。

**參數**：

- `relative_string` (必要)：支援格式之一的參考時間規格。
- `field` (必要)：要與參考時間比較的時間戳記欄位。

**傳回類型**：`BOOLEAN`

**相對字串格式**：
1. `"now"` 或 `"now()"`：使用目前的系統時間。
2. 絕對格式 (`MM/dd/yyyy:HH:mm:ss` 或 `yyyy-MM-dd HH:mm:ss`)：將字串轉換為時間戳記，並與欄位值比較。
3. 相對格式：`(+|-)<time_integer><time_unit>[+<...>]@<snap_unit>`

**指定相對時間的步驟**：
- **時間位移**：使用 `+` 或 `-` 指出與目前時間的位移。
- **時間量**：提供數值，後接時間單位 (`s`、`m`、`h`、`d`、`w`、`M`、`y`)。
- **對齊單位**：可選擇使用 `@<unit>` 指定對齊單位，將結果向下捨入至最接近的單位 (例如小時、日、月)。

**範例** (假設目前時間為 `2025-05-28 14:28:34`)：
- `-3d+2y` → `2027-05-25 14:28:34`。
- `+1d@m` → `2025-05-29 14:28:00`。
- `-3M+1y@M` → `2026-02-01 00:00:00`。

#### 範例

下列範例會將時間戳記與目前時間及相對時間比較：

```sql
source=accounts
| eval now = utc_timestamp()
| eval a = earliest("now", now), b = earliest("-2d@d", now)
| fields a, b
| head 1
```
{% include copy.html %}
  
此查詢會傳回下列結果：
  
<!-- vale off -->

| a | b |
<!-- vale off -->

| --- | --- |
| False | True |

<!-- vale on -->

<!-- vale on -->

下列範例使用絕對時間格式篩選記錄：

```sql
source=nyc_taxi
| where earliest('07/01/2014:00:30:00', timestamp)
| stats COUNT() as cnt
```
{% include copy.html %}
  
此查詢會傳回下列結果：
  
<!-- vale off -->

| cnt |
<!-- vale off -->

| --- |
| 972 |

<!-- vale on -->

<!-- vale on -->
  
## LATEST

**用法**：`latest(relative_string, field)`

若欄位值早於從 `relative_string` 相對於目前時間所推算出的時間戳記，則傳回 `TRUE`，否則傳回 `FALSE`。

**參數**：

- `relative_string` (必要)：支援格式之一的參考時間規格。
- `field` (必要)：要與參考時間比較的時間戳記欄位。

**傳回類型**：`BOOLEAN`

#### 範例

下列範例使用 latest 函式比較時間戳記：

```sql
source=accounts
| eval now = utc_timestamp()
| eval a = latest("now", now), b = latest("+2d@d", now)
| fields a, b
| head 1
```
{% include copy.html %}
  
此查詢會傳回下列結果：
  
<!-- vale off -->

| a | b |
<!-- vale off -->

| --- | --- |
| True | True |

<!-- vale on -->

<!-- vale on -->

下列範例使用 latest 搭配絕對時間格式篩選記錄：

```sql
source=nyc_taxi
| where latest('07/21/2014:04:00:00', timestamp)
| stats COUNT() as cnt
```
{% include copy.html %}
  
此查詢會傳回下列結果：
  
<!-- vale off -->

| cnt |
<!-- vale off -->

| --- |
| 969 |

<!-- vale on -->

<!-- vale on -->
  
## REGEXP_MATCH

**用法**：`regexp_match(string, pattern)`

若規則運算式模式在字串值的任何子字串中找到相符項，則傳回 `TRUE`，否則傳回 `FALSE`。此函式使用 Java 規則運算式語法做為模式。

**參數**：

- `string` (必要)：要在其中搜尋的字串。
- `pattern` (必要)：要比對的規則運算式模式。

**傳回類型**：`BOOLEAN`

#### 範例

下列範例使用 regex 模式篩選記錄訊息：

```sql
source=logs
| where regexp_match(message, 'ERROR|WARN|FATAL')
| fields timestamp, message
```
{% include copy.html %}
  
<!-- vale off -->

| timestamp | message |
| --- | --- |
| 2024-01-15 10:23:45 | ERROR: Connection timeout to database |
| 2024-01-15 10:24:12 | WARN: High memory usage detected |
| 2024-01-15 10:25:33 | FATAL: System crashed unexpectedly |

<!-- vale on -->

下列範例使用 regex 驗證電子郵件地址：

```sql
source=users
| where regexp_match(email, '[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
| fields name, email
```
{% include copy.html %}
  
<!-- vale off -->

| name | email |
| --- | --- |
| John | john@example.com |
| Alice | alice@company.org |

<!-- vale on -->

下列範例使用 regex 篩選有效的公用 IP 位址：

```sql
source=network
| where regexp_match(ip_address, '^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$') AND NOT regexp_match(ip_address, '^(10\.|172\.(1[6-9]|2[0-9]|3[01])\.|192\.168\.)')
| fields ip_address, status
```
{% include copy.html %}
  
<!-- vale off -->

| ip_address | status |
| --- | --- |
| 8.8.8.8 | active |
| 1.1.1.1 | active |

<!-- vale on -->

下列範例使用 regex 進行產品分類，並以不區分大小寫的方式比對：

```sql
source=products
| eval category = if(regexp_match(name, '(?i)(laptop|computer|desktop)'), 'Computing', if(regexp_match(name, '(?i)(phone|tablet|mobile)'), 'Mobile', 'Other'))
| fields name, category
```
{% include copy.html %}
  
<!-- vale off -->

| name | category |
| --- | --- |
| Dell Laptop XPS | Computing |
| iPhone 15 Pro | Mobile |
| Wireless Mouse | Other |

<!-- vale on -->
