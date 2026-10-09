---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: table
parent: Commands
grand_parent: PPL
nav_order: 48
---

<!-- vale off -->

# table 命令

<!-- vale on -->

`table` 命令是 [`fields`]({{site.url}}{{site.baseurl}}/sql-and-ppl/ppl/commands/fields/) 命令的別名，提供相同的欄位選取功能。您可以使用增強的語法選項，保留或移除搜尋結果中的欄位。

## 語法

`table` 命令的語法如下：

```sql
table [+|-] <field-list>
```

## 參數

`table` 命令支援下列參數。

| 參數 | 必要/選用 | 說明 |
| --- | --- | --- |
| `<field-list>` | 必要 | 以逗號或空格分隔的欄位清單，列出要保留或移除的欄位。支援萬用字元模式。 |
| `[+|-]` | 選用 | 指定要保留或移除的欄位。如果使用加號（`+`），則只保留欄位清單中指定的欄位。如果使用減號（`-`），則移除欄位清單中指定的所有欄位。預設為 `+`。 |

## 範例：table 命令的基本用法  

下列查詢會快速建立事件摘要表，顯示近期錯誤的嚴重性、服務和記錄訊息：
  
```sql
source=otellogs
| where severityText IN ('ERROR', 'WARN')
| sort - severityNumber, `resource.attributes.service.name`
| table severityText `resource.attributes.service.name` body
| head 3
```
{% include copy.html %}
{% include try-in-playground.html %}
  
此查詢會傳回下列結果：
  
<!-- vale off -->

| severityText | resource.attributes.service.name | body |
| --- | --- | --- |
| ERROR | checkout | NullPointerException in CheckoutService.placeOrder at line 142 |
| ERROR | checkout | Kafka producer delivery failed: message too large for topic order-events (max 1048576 bytes) |
| ERROR | frontend-proxy | [2024-02-01T09:20:00.456Z] "POST /api/checkout HTTP/1.1" 503 - 0 30000 checkout-8d4f7b-mk2p9 |

<!-- vale on -->
  

## 相關文件 

- [`fields`]({{site.url}}{{site.baseurl}}/sql-and-ppl/ppl/commands/fields/) -- 功能相同的別名命令  
