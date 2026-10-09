---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "統計函式"
parent: Functions
grand_parent: PPL
nav_order: 12
---

# 統計函式

PPL 支援下列統計函式。

## MAX

**用法**：`MAX(x, y, ...)`

傳回所提供引數中的最大值。當同時提供字串與數字時，字串會被視為大於數字，函式會傳回依字典序最大的字串。此函式僅能在 `eval` 命令中使用。

**參數**：

- `x, y, ...` (必要)：數量可變的引數，類型為 `INTEGER`、`LONG`、`FLOAT`、`DOUBLE` 或 `STRING`。

**傳回類型**：所選引數的類型

### 範例
  
```sql
source=accounts
| eval max_val = MAX(age, 30)
| fields age, max_val
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| age | max_val |
| --- | --- |
| 32 | 32 |
| 36 | 36 |
| 28 | 30 |
| 33 | 33 |

<!-- vale on -->
  
```sql
source=accounts
| eval result = MAX(firstname, 'John')
| fields firstname, result
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| firstname | result |
| --- | --- |
| Amber | John |
| Hattie | John |
| Nanette | Nanette |
| Dale | John |

<!-- vale on -->
  
```sql
source=accounts
| eval result = MAX(age, 35, 'John', firstname)
| fields age, firstname, result
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| age | firstname | result |
| --- | --- | --- |
| 32 | Amber | John |
| 36 | Hattie | John |
| 28 | Nanette | Nanette |
| 33 | Dale | John |

<!-- vale on -->
  
## MIN

**用法**：`MIN(x, y, ...)`

傳回所提供引數中的最小值。當同時提供字串與數字時，數字會被視為小於字串，函式會傳回最小的數值。此函式僅能在 `eval` 命令中使用。

**參數**：

- `x, y, ...` (必要)：數量可變的引數，類型為 `INTEGER`、`LONG`、`FLOAT`、`DOUBLE` 或 `STRING`。

**傳回類型**：所選引數的類型

### 範例
  
```sql
source=accounts
| eval min_val = MIN(age, 30)
| fields age, min_val
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| age | min_val |
| --- | --- |
| 32 | 30 |
| 36 | 30 |
| 28 | 28 |
| 33 | 30 |

<!-- vale on -->
  
```sql
source=accounts
| eval result = MIN(firstname, 'John')
| fields firstname, result
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| firstname | result |
| --- | --- |
| Amber | Amber |
| Hattie | Hattie |
| Nanette | John |
| Dale | Dale |

<!-- vale on -->
  
```sql
source=accounts
| eval result = MIN(age, 35, firstname)
| fields age, firstname, result
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| age | firstname | result |
| --- | --- | --- |
| 32 | Amber | 32 |
| 36 | Hattie | 35 |
| 28 | Nanette | 28 |
| 33 | Dale | 33 |

<!-- vale on -->
