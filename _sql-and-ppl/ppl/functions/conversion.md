---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "類型轉換函式"
parent: Functions
grand_parent: PPL
nav_order: 4
---

# 類型轉換函式

PPL 支援下列類型轉換函式。

## CAST

**用法**：`cast(expr as dataType)`

將運算式轉換為指定的資料類型，並傳回轉換後的值。

**參數**：

- `expr`（必要）：要轉換為其他資料類型的運算式。
- `dataType`（必要）：轉換作業的目標資料類型。

**回傳類型**：由資料類型指定

下表顯示資料類型之間轉換時所使用的轉換規則：
  
<!-- vale off -->

| Src/Target | STRING | NUMBER | BOOLEAN | TIMESTAMP | DATE | TIME | IP |
| --- | --- | --- | --- | --- | --- | --- | --- |
| STRING |  | Note1 | Note1 | TIMESTAMP() | DATE() | TIME() | IP() |
| NUMBER | Note1 |  | v!=0 | N/A | N/A | N/A | N/A |
| BOOLEAN | Note1 | v?1:0 |  | N/A | N/A | N/A | N/A |
| TIMESTAMP | Note1 | N/A | N/A |  | DATE() | TIME() | N/A |
| DATE | Note1 | N/A | N/A | N/A |  | N/A | N/A |
| TIME | Note1 | N/A | N/A | N/A | N/A |  | N/A |
| IP | Note2 | N/A | N/A | N/A | N/A | N/A |  |

<!-- vale on -->
  
Note1：轉換遵循 JDK 規格。
Note2：IP 位址會轉換為其標準表示法。IPv6 的標準表示法詳見 [RFC 5952](https://datatracker.ietf.org/doc/html/rfc5952)。

#### 範例

下列範例將不同的資料類型轉換為字串：

```sql
source=people
| eval `cbool` = CAST(true as string), `cint` = CAST(1 as string), `cdate` = CAST(CAST('2012-08-07' as date) as string)
| fields `cbool`, `cint`, `cdate`
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| cbool | cint | cdate |
| --- | --- | --- |
| TRUE | 1 | 2012-08-07 |

<!-- vale on -->
  
下列範例將值轉換為整數類型：

```sql
source=people
| eval `cbool` = CAST(true as int), `cstring` = CAST('1' as int)
| fields `cbool`, `cstring`
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| cbool | cstring |
| --- | --- |
| 1 | 1 |

<!-- vale on -->
  
下列範例將字串轉換為 date、time 與 timestamp 類型：

```sql
source=people
| eval `cdate` = CAST('2012-08-07' as date), `ctime` = CAST('01:01:01' as time), `ctimestamp` = CAST('2012-08-07 01:01:01' as timestamp)
| fields `cdate`, `ctime`, `ctimestamp`
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| cdate | ctime | ctimestamp |
| --- | --- | --- |
| 2012-08-07 | 01:01:01 | 2012-08-07 01:01:01 |

<!-- vale on -->
  
下列範例示範鏈結多個轉換函式：

```sql
source=people
| eval `cbool` = CAST(CAST(true as string) as boolean)
| fields `cbool`
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| cbool |
| --- |
| True |

<!-- vale on -->
  
## 隱含類型轉換  

隱含轉換是自動的類型轉換。當函式沒有與輸入類型完全相符的簽名時，引擎會尋找另一個能安全處理這些值的簽名。它會選擇需要對原始類型進行最少轉換的選項，因此您可以在不加入明確 `cast` 函式的情況下混合使用字面值與欄位。

### 字串轉數值類型

當字串被用在需要數值的地方時，引擎會嘗試將該字串剖析為數字：

- 字串必須代表有效的數值，例如 `"3.14"` 或 `"42"`。任何其他值都會導致查詢失敗。
- 如果字串與數值引數一起使用，引擎會將它視為 `DOUBLE`，以便套用函式的數值版本。

#### 範例

下列範例示範在算術運算中使用字串：

```sql
source=people
| eval divide="5"/10, multiply="5" * 10, add="5" + 10, minus="5" - 10, concat="5" + "5"
| fields divide, multiply, add, minus, concat
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| divide | multiply | add | minus | concat |
| --- | --- | --- | --- | --- |
| 0.5 | 50.0 | 15.0 | -5.0 | 55 |

<!-- vale on -->
  
下列範例示範在比較運算中使用字串：

```sql
source=people
| eval e="1000"==1000, en="1000"!=1000, ed="1000"==1000.0, edn="1000"!=1000.0, l="1000">999, ld="1000">999.9, i="malformed"==1000
| fields e, en, ed, edn, l, ld, i
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| e | en | ed | edn | l | ld | i |
| --- | --- | --- | --- | --- | --- | --- |
| True | False | True | False | True | True | null |

<!-- vale on -->
  
## TOSTRING

**用法**：`tostring(value[, format])`

將值轉換為字串表示法。若有提供格式，則將數字轉換為指定的格式類型。對於布林值，會轉換為 `TRUE` 或 `FALSE`。

**參數**：

- `value`（必要）：要轉換為字串的值（任何資料類型）。
- `format`（選用）：數字轉換所使用的格式類型。此參數僅在 `value` 為數字時使用。若 `value` 為布林值，則會忽略此參數。

格式類型：

- `binary`：將數字轉換為二進位值。
- `hex`：將數字轉換為十六進位值。
- `commas`：使用逗號格式化數字。若數字包含小數，函式會將數字四捨五入至最接近的兩位小數。
- `duration`：將以秒為單位的值轉換為可讀的時間格式 `HH:MM:SS`。
- `duration_millis`：將以毫秒為單位的值轉換為可讀的時間格式 `HH:MM:SS`。

**回傳類型**：`STRING`

#### 範例

下列範例將數字轉換為其二進位字串表示法：

```sql
source=accounts
| where firstname = "Amber"
| eval balance_binary = tostring(balance, "binary")
| fields firstname, balance_binary, balance
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| firstname | balance_binary | balance |
| --- | --- | --- |
| Amber | 1001100100111001 | 39225 |

<!-- vale on -->
  
下列範例將數字轉換為其十六進位字串表示法：

```sql
source=accounts
| where firstname = "Amber"
| eval balance_hex = tostring(balance, "hex")
| fields firstname, balance_hex, balance
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| firstname | balance_hex | balance |
| --- | --- | --- |
| Amber | 9939 | 39225 |

<!-- vale on -->
  
下列範例以逗號分隔符格式化數字：
  
```sql
source=accounts
| where firstname = "Amber"
| eval balance_commas = tostring(balance, "commas")
| fields firstname, balance_commas, balance
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| firstname | balance_commas | balance |
| --- | --- | --- |
| Amber | 39,225 | 39225 |

<!-- vale on -->
  
### 範例：將秒數轉換為時長格式

下列範例將秒數轉換為代表時、分、秒的 `HH:MM:SS` 格式：
  
```sql
source=accounts
| where firstname = "Amber"
| eval duration = tostring(6500, "duration")
| fields firstname, duration
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| firstname | duration |
| --- | --- |
| Amber | 01:48:20 |

<!-- vale on -->
  
下列範例將布林值轉換為字串：
  
```sql
source=accounts
| where firstname = "Amber"
| eval `boolean_str` = tostring(1=1)
| fields `boolean_str`
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| boolean_str |
| --- |
| TRUE |

<!-- vale on -->

## TONUMBER

**用法**：`tonumber(string[, base])`

將字串值轉換為數字。選用的 `base` 參數指定輸入字串的基數。若未提供，函式會假設基數為 `10`。

**參數**：

- `string`（必要）：要轉換之數字的字串表示法。
- `base`（選用）：輸入字串的基數（介於 `2` 與 `36` 之間）。預設為 `10`。

**回傳類型**：`NUMBER`

您可以在 `eval` 命令中使用此函式，也可以將它用於 `eval` 運算式。基數值可介於 `2` 與 `36` 之間。

**數值限制**：
- 基數 10：最大值為 `+(2-2^-52)·2^1023`，最小值為 `-(2-2^-52)·2^1023`。
- 其他基數：最大值為 `2^63-1`（或 `7FFFFFFFFFFFFFFF`），最小值為 `-2^63`（或 `-7FFFFFFFFFFFFFFF`）。

若 `tonumber` 函式無法將欄位值剖析為數字，函式會傳回 `NULL`。您可以使用此函式將各種基數的數字字串表示法轉換為對應的基數 10 值。

#### 範例：將二進位字串轉換為數字

```sql
source=people
| eval int_value = tonumber('010101',2)
| fields int_value
| head 1
```
{% include copy.html %}

查詢會傳回下列結果：

<!-- vale off -->

| int_value |
| --- |
| 21.0 |

<!-- vale on -->

#### 範例：將十六進位字串轉換為數字

```sql
source=people
| eval int_value = tonumber('FA34',16)
| fields int_value
| head 1
```
{% include copy.html %}

查詢會傳回下列結果：

<!-- vale off -->

| int_value |
| --- |
| 64052.0 |

<!-- vale on -->

#### 範例：將不含小數部分的十進位字串轉換為數字

```sql
source=people
| eval int_value = tonumber('4598')
| fields int_value
| head 1
```
{% include copy.html %}

查詢會傳回下列結果：

<!-- vale off -->

| int_value |
| --- |
| 4598.0 |

<!-- vale on -->

#### 範例：將含小數部分的十進位字串轉換為數字

```sql
source=people
| eval double_value = tonumber('4598.678')
| fields double_value
| head 1
```
{% include copy.html %}

查詢會傳回下列結果：

<!-- vale off -->

| double_value |
| --- |
| 4598.678 |

<!-- vale on -->
