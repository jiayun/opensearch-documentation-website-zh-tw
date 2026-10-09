---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: reverse
parent: Commands
grand_parent: PPL
nav_order: 39
---

<!-- vale off -->

# reverse 命令

<!-- vale on -->

`reverse` 命令會反轉搜尋結果的顯示順序。它會傳回相同的結果，但順序相反。

`reverse` 命令會處理整個資料集。如果直接套用於數百萬筆記錄，會耗用大量協調節點的記憶體資源。請只對較小的資料集套用 `reverse` 命令，通常是在彙總操作之後。
{: .note}

## 語法

`reverse` 命令的語法如下：

```sql
reverse
```

## 範例 1：使用基本的反轉操作

下列查詢會反轉結果中所有文件的順序：

```sql
source=otellogs
| fields severityText, `resource.attributes.service.name`
| head 5
| reverse
```
{% include copy.html %}
{% include try-in-playground.html %}

此查詢會傳回下列結果：

<!-- vale off -->

| severityText | resource.attributes.service.name |
| --- | --- |
| DEBUG | cart |
| ERROR | payment |
| WARN | product-catalog |
| INFO | cart |
| INFO | frontend |

<!-- vale on -->

## 範例 2：使用 reverse 和 sort 命令

下列查詢會先依 `severityNumber` 遞增排序，再反轉結果，實際上即可達成遞減排序：

```sql
source=otellogs
| sort severityNumber
| fields severityText, severityNumber
| head 5
| reverse
```
{% include copy.html %}
{% include try-in-playground.html %}

此查詢會傳回下列結果：

<!-- vale off -->

| severityText | severityNumber |
| --- | --- |
| INFO | 9 |
| INFO | 9 |
| DEBUG | 5 |
| DEBUG | 5 |
| DEBUG | 5 |

<!-- vale on -->

## 範例 3：使用 reverse 和 head 命令

下列查詢將 `reverse` 命令與 `head` 命令搭配使用，以擷取原始結果順序中的最後兩筆記錄：

```sql
source=otellogs
| reverse
| head 2
| fields severityText, `resource.attributes.service.name`
```
{% include copy.html %}
{% include try-in-playground.html %}

此查詢會傳回下列結果：

<!-- vale off -->

| severityText | resource.attributes.service.name |
| --- | --- |
| ERROR | checkout |
| DEBUG | cart |

<!-- vale on -->

## 範例 4：雙重反轉

下列查詢說明套用 `reverse` 兩次會以原始順序傳回文件：

```sql
source=otellogs
| reverse
| reverse
| fields severityText, `resource.attributes.service.name`
| head 5
```
{% include copy.html %}
{% include try-in-playground.html %}

此查詢會傳回下列結果：

<!-- vale off -->

| severityText | resource.attributes.service.name |
| --- | --- |
| INFO | frontend |
| INFO | cart |
| WARN | product-catalog |
| ERROR | payment |
| DEBUG | cart |

<!-- vale on -->

## 範例 5：搭配篩選使用 reverse 命令

下列查詢將 `reverse` 命令與篩選及欄位選取搭配使用：

```sql
source=otellogs
| where severityText = 'ERROR'
| fields severityText, `resource.attributes.service.name`
| reverse
```
{% include copy.html %}
{% include try-in-playground.html %}

此查詢會傳回下列結果：

<!-- vale off -->

| severityText | resource.attributes.service.name |
| --- | --- |
| ERROR | checkout |
| ERROR | product-catalog |
| ERROR | recommendation |
| ERROR | frontend-proxy |
| ERROR | payment |
| ERROR | checkout |
| ERROR | payment |

<!-- vale on -->
