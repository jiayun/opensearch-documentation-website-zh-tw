---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "系統函式"
parent: Functions
grand_parent: PPL
nav_order: 14
---

# 系統函式

PPL 支援下列系統函式。

## TYPEOF

**用法**：`TYPEOF(expr)`

傳回給定運算式的資料類型。這對疑難排解或動態建構 SQL 查詢很有用。

**參數**：

- `expr` (必要)：要判斷資料類型的運算式。可以是任何資料類型。

**回傳類型**：`STRING`

### 範例  
  
```sql
source=people
| eval `typeof(date)` = typeof(DATE('2008-04-14')), `typeof(int)` = typeof(1), `typeof(now())` = typeof(now()), `typeof(column)` = typeof(accounts)
| fields `typeof(date)`, `typeof(int)`, `typeof(now())`, `typeof(column)`
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| typeof(date) | typeof(int) | typeof(now()) | typeof(column) |
| --- | --- | --- | --- |
| DATE | INT | TIMESTAMP | STRUCT |

<!-- vale on -->
