---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: convert
parent: Commands
grand_parent: PPL
nav_order: 10
---

<!-- vale off -->

# convert 命令

<!-- vale on -->

`convert` 命令使用轉換函式將欄位值轉換為數值。除非使用 `AS` 子句以轉換後的值建立新欄位，否則原始欄位值會被覆寫。

`convert` 命令具有下列屬性：

- 若值無法轉換為數字，所有轉換函式都會傳回 `null`。
- 所有數值轉換函式都會傳回雙精度值，以支援彙總。
- 轉換後的值會以十進位標記法顯示 (例如 `1234.0` 或 `1234.56`)。

使用 `AS` 子句可在建立轉換後欄位的同時保留原始欄位。您可以在單一命令中套用多個轉換 (請參閱[範例 4](#example-4-converting-multiple-fields))。

## 語法

`convert` 命令具有下列語法：

```sql
convert <convert-function>(<field>) [AS <field>] [, <convert-function>(<field>) [AS <field>]]...
```

## 參數

`convert` 命令支援下列參數。

| 參數 | 必要/選用 | 說明 |
| --- | --- | --- |
| `<convert-function>` | 必要 | 下列其中一個轉換函式：`auto()`、`num()`、`rmcomma()`、`rmunit()`、`memk()` 或 `none()`。 |
| `<field>` | 必要 | 要轉換的單一欄位名稱。 |
| `AS <field>` | 選用 | 使用轉換後的值建立新欄位，並保留原始欄位。 |

## 轉換函式

| 函式 | 說明 |
| --- | --- |
| `auto(field)` | 使用智慧轉換自動將欄位轉換為數字。支援單位，包括記憶體單位前置字元，例如 `k`、`m` 或 `g`、逗號及科學標記法。若值無法轉換，則傳回 `null`。 |
| `num(field)` | 擷取字串開頭的數字部分。對於不含字母的字串，逗號會解譯為千分位分隔符號並移除。對於包含字母的字串，擷取會在第一次出現字母或逗號時停止。若值無法轉換，則傳回 `null`。 |
| `rmcomma(field)` | 從數字字串中移除逗號 (千分位分隔符號)，並將結果轉換為數字。若值包含字母，則傳回 `null`。 |
| `rmunit(field)` | 擷取字串開頭的數字部分。會在遇到第一個字母或逗號時停止。若值無法轉換，則傳回 `null`。 |
| `memk(field)` | 將包含記憶體單位後置字元的值轉換為 KB。接受包含選用單位後置字元的數字，例如 `k`、`m` 或 `g` (大小寫不拘)。若輸入為不含單位後置字元的數字字串，則假設該值以 KB 為單位。若格式無效，則傳回 `null`。 |
| `none(field)` | 不執行任何操作的函式，會保留原始欄位值。用於從萬用字元轉換中排除特定欄位。 |

## 範例 1：自動轉換欄位

下列查詢使用 `auto()` 函式將 `balance` 欄位轉換為數字：

```sql
source=accounts
| convert auto(balance)
| fields account_number, balance
| head 3
```
{% include copy.html %}

查詢會傳回下列結果：

<!-- vale off -->

| account_number | balance |
| --- | --- |
| 1 | 39225.0 |
| 6 | 5686.0 |
| 13 | 32838.0 |

<!-- vale on -->

## 範例 2：轉換包含逗號的欄位

下列查詢會轉換包含逗號分隔數字的欄位：

```sql
source=accounts
| eval price='1,234'
| convert num(price)
| fields price
```
{% include copy.html %}

查詢會傳回下列結果：

<!-- vale off -->

| price |
| --- |
| 1234.0 |

<!-- vale on -->

## 範例 3：轉換包含記憶體單位的欄位

下列查詢會將記憶體大小字串轉換為 KB：

```sql
source=system_metrics
| eval memory='100m'
| convert memk(memory)
| fields memory
```
{% include copy.html %}

查詢會傳回下列結果：

<!-- vale off -->

| memory |
| --- |
| 102400.0 |

<!-- vale on -->

## 範例 4：轉換多個欄位

下列查詢使用不同的轉換函式轉換多個欄位：

```sql
source=accounts
| convert auto(balance), num(age)
| fields account_number, balance, age
| head 3
```
{% include copy.html %}

查詢會傳回下列結果：

<!-- vale off -->

| account_number | balance | age |
| --- | --- | --- |
| 1 | 39225.0 | 32.0 |
| 6 | 5686.0 | 36.0 |
| 13 | 32838.0 | 28.0 |

<!-- vale on -->

## 範例 5：使用 AS 子句保留原始值

下列查詢會建立包含轉換後值的新欄位，同時保留原始欄位：

```sql
source=accounts
| convert auto(balance) AS balance_num
| fields account_number, balance, balance_num
| head 3
```
{% include copy.html %}

查詢會傳回下列結果：

<!-- vale off -->

| account_number | balance | balance_num |
| --- | --- | --- |
| 1 | 39225 | 39225.0 |
| 6 | 5686 | 5686.0 |
| 13 | 32838 | 32838.0 |

<!-- vale on -->

## 範例 6：從包含單位的字串中擷取數字

下列查詢會從包含單位的字串中擷取數值：

```sql
source=accounts
| head 1
| eval duration='2.000 sec'
| convert rmunit(duration)
| fields duration
```
{% include copy.html %}

查詢會傳回下列結果：

<!-- vale off -->

| duration |
| --- |
| 2.0 |

<!-- vale on -->

## 範例 7：使用彙總函式

下列查詢會轉換值並將其用於彙總：

```sql
source=accounts
| convert auto(age)
| stats sum(age) by gender
```
{% include copy.html %}

查詢會傳回下列結果：

<!-- vale off -->

| sum(age) | gender |
| --- | --- |
| 28.0 | F |
| 101.0 | M |

<!-- vale on -->

## 範例 8：使用 none() 保留欄位值

`none()` 函式會傳回未變更的欄位值。這在多重欄位轉換中明確保留欄位時很有用：

```sql
source=accounts
| convert auto(balance), num(age), none(account_number)
| fields account_number, balance, age
| head 3
```
{% include copy.html %}

查詢會傳回下列結果：

<!-- vale off -->

| account_number | balance | age |
| --- | --- | --- |
| 1 | 39225.0 | 32.0 |
| 6 | 5686.0 | 36.0 |
| 13 | 32838.0 | 28.0 |

<!-- vale on -->

### 搭配 AS 子句使用 none() 重新命名欄位

`none()` 函式可與 `AS` 子句搭配使用，以重新命名欄位而不修改其值：

```sql
source=accounts
| convert none(account_number) AS account_id
| fields account_id, firstname, lastname
| head 3
```
{% include copy.html %}

查詢會傳回下列結果：

<!-- vale off -->

| account_id | firstname | lastname |
| --- | --- | --- |
| 1 | Amber | Duke |
| 6 | Hattie | Bond |
| 13 | Nanette | Bates |

<!-- vale on -->

`none()` 函式在搭配萬用字元支援時很有用，可讓您從大量轉換中排除特定欄位。
{: .note}

## 限制

`convert` 命令需要將 `plugins.calcite.enabled` 設定為 `true`。

若停用 Apache Calcite，使用任何 convert 函式都會導致不支援的函式錯誤。