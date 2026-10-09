---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "PPL 語法"
parent: Commands
grand_parent: PPL
nav_order: 1
redirect_from:
  - /search-plugins/sql/ppl/syntax/
---

<!-- vale off -->

# PPL 語法

<!-- vale on -->

每個 PPL 查詢都會以 `search` 命令開頭。它會指定要從中搜尋及擷取文件的索引。

`PPL` 在每個 PPL 查詢中只支援一個 `search` 命令，而且它一律是第一個命令。`search` 這個字可以省略。

後續命令可以依任意順序接續。


## 語法

```sql
search source=<index> [boolean-expression]
source=<index> [boolean-expression]
```
{% include copy.html %}

## 參數

`search` 命令支援下列參數。

| 參數 | 必要/選用 | 說明 |
| --- | --- | --- |
| `<index>` | 必要 | 指定要查詢的索引。 |
| `<boolean-expression>` | 選用 | 指定評估為布林值的運算式。 |


## 語法標記慣例

PPL 命令語法使用下列標記慣例。

### 預留位置

預留位置以角括號表示（`< >`）。這些必須替換為實際值。

**範例**：`<field>` 表示您必須指定實際的欄位名稱，例如 `age` 或 `firstname`。

### 選用元素

選用元素以方括號括住（`[ ]`）。這些可以從命令中省略。

**範例**：
- `[+|-]` 表示加號或減號為選用。
- `[<alias>]` 表示別名預留位置為選用。

### 必要選項

替代選項之間的必要選擇以括號表示，並以直線分隔符號（`(option1 | option2)`）分隔。您必須從指定的選項中選擇恰好一個。

**範例**：`(on | where)` 表示您必須使用 `on` 或 `where`，但不能同時使用兩者。

### 選用選項

替代選項之間的選用選擇以方括號搭配直線分隔符號表示（`[option1 | option2]`）。您可以選擇其中一個選項，或完全省略。

**範例**：`[asc | desc]` 表示您可以指定 `asc`、`desc`，或兩者皆不指定。

### 重複

省略符號（`...`）表示前面的元素可以重複多次。

**範例**：
- `<field>...` 表示一個或多個不以逗號分隔的欄位：`field1 field2 field3`
- `<field>, ...` 表示以逗號分隔的重複：`field1, field2, field3`
  

## 範例

**範例 1：透過索引搜尋**

在下列查詢中，`search` 命令會將 `otellogs` 索引指定為來源，並使用 `fields` 和 `where` 命令做為條件：

```sql
search source=otellogs
| where severityText = 'ERROR'
| fields severityText, `resource.attributes.service.name`
```
{% include copy.html %}
{% include try-in-playground.html %}

查詢會傳回下列結果：

<!-- vale off -->

| severityText | resource.attributes.service.name |
| --- | --- |
| ERROR | payment |
| ERROR | checkout |
| ERROR | payment |
| ERROR | frontend-proxy |
| ERROR | recommendation |
| ERROR | product-catalog |
| ERROR | checkout |

<!-- vale on -->

**範例 2：取得所有文件**

若要從 `otellogs` 索引取得所有文件，請將其指定為 `source`。下列範例使用 `head` 將輸出限制為 5 列：

```sql
source=otellogs
| head 5
| fields severityText, `resource.attributes.service.name`, body
```
{% include copy.html %}
{% include try-in-playground.html %}

查詢會傳回下列結果：

<!-- vale off -->

| severityText | resource.attributes.service.name | body |
| --- | --- | --- |
| INFO | frontend | [2024-02-01T09:10:00.123Z] "GET /api/products HTTP/1.1" 200 - 1024 45 frontend-6b7b4c9f-x2kl9 |
| INFO | cart | Order #1234 placed successfully by user U100 |
| WARN | product-catalog | Slow query detected: SELECT \* FROM products WHERE category = 'electronics' took 3200ms |
| ERROR | payment | Payment failed: connection timeout to payment gateway after 30000ms |
| DEBUG | cart | Cache miss for key user:session:U200 in Valkey cluster |

<!-- vale on -->

**範例 3：取得符合條件的文件**

若要從 `otellogs` 索引取得所有 `severityText` 等於 `ERROR` 且 `resource.attributes.service.name` 等於 `payment` 的文件，請使用下列查詢：

```sql
source=otellogs severityText = 'ERROR' AND `resource.attributes.service.name` = 'payment'
| fields severityText, `resource.attributes.service.name`, body
```
{% include copy.html %}
{% include try-in-playground.html %}

查詢會傳回下列結果：

<!-- vale off -->

| severityText | resource.attributes.service.name | body |
| --- | --- | --- |
| ERROR | payment | Payment failed: connection timeout to payment gateway after 30000ms |
| ERROR | payment | Out of memory: Java heap space - shutting down pod payment-6f8d4b-ht7q3 |

<!-- vale on -->

