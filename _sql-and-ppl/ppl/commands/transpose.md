---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: transpose
parent: Commands
grand_parent: PPL
nav_order: 51
---

<!-- vale off -->

# transpose 命令

<!-- vale on -->

`transpose` 命令會將所要求數量的資料列輸出為欄位，並將每個結果資料列轉換為由欄位值組成的對應欄位。

## 語法

`transpose` 命令的語法如下：

```sql
transpose [int] [column_name=<string>]
```

## 參數

`transpose` 命令支援下列參數。

| 參數 | 必要/選用 | 說明 |
|---|---|---|
| `<int>` | 選用 | 要轉換為欄位的資料列數。預設為 `5`。最大值為 `10000`。 |
| `column_name=<string>` | 選用 | 轉置資料列時使用的第一個欄位名稱。此欄位存放各欄位的名稱。 |

## 範例 1：轉置嚴重性分佈

下列查詢會將嚴重性分佈轉置為直欄格式。這對於建立精簡的摘要檢視很有用：

```sql
source=otellogs
| stats count() as log_count by severityText
| sort severityText
| transpose
```
{% include copy.html %}
{% include try-in-playground.html %}

查詢會傳回下列結果：

<!-- vale off -->

| column | row 1 | row 2 | row 3 | row 4 | row 5 |
| --- | --- | --- | --- | --- | --- |
| log_count | 3 | 7 | 6 | 4 | null |
| severityText | DEBUG | ERROR | INFO | WARN | null |

<!-- vale on -->

## 範例 2：轉置有限數量的資料列

下列查詢只會轉置前三個嚴重性層級：

```sql
source=otellogs
| stats count() as log_count by severityText
| sort severityText
| transpose 3
```
{% include copy.html %}
{% include try-in-playground.html %}

查詢會傳回下列結果：

<!-- vale off -->

| column | row 1 | row 2 | row 3 |
| --- | --- | --- | --- |
| log_count | 3 | 7 | 6 |
| severityText | DEBUG | ERROR | INFO |

<!-- vale on -->

## 限制

`transpose` 命令會將指定數量的資料列轉換為欄位。如果可用的資料列較少，缺少的值會以 `null` 欄位表示。
