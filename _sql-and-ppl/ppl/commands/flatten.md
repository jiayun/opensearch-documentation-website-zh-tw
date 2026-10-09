---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: flatten
parent: Commands
grand_parent: PPL
nav_order: 20
---

<!-- vale off -->

# flatten 命令

<!-- vale on -->

`flatten` 命令會將結構體或物件欄位轉換為文件中的個別欄位。

產生的扁平化欄位會依其原始鍵名以字典序排序。例如，若某個結構體包含鍵 `b`、`c` 和 `Z`，則扁平化欄位的順序為 `Z`、`b`、`c`。

`flatten` 不應套用於陣列。若要將陣列欄位展開為多個資料列，請使用 `expand` 命令。請注意，在 OpenSearch 中，陣列可以儲存在非陣列欄位中；當扁平化包含巢狀陣列的欄位時，只會扁平化陣列的第一個元素。
{: .important}

## 語法

`flatten` 命令的語法如下：

```sql
flatten <field> [as (<alias-list>)]
```

## 參數

`flatten` 命令支援下列參數。

| 參數 | 必要/選用 | 說明 |
| --- | --- | --- |
| `<field>` | 必要 | 要扁平化的欄位。僅支援物件和巢狀欄位。 |
| `<alias-list>` | 選用 | 用來取代原始鍵名的名稱清單，以逗號分隔。若指定多個別名，請將清單括在括號中。別名的數量必須與結構體中的鍵數量相符，且別名必須依對應原始鍵的字典序排列。 |  
  

## 範例：扁平化 instrumentation scope 物件  

下列查詢會將 `instrumentationScope` 巢狀物件扁平化為個別欄位，可用於分析目前使用哪些 OTel SDK 版本：
  
```sql
source=otellogs
| where NOT ISNULL(instrumentationScope.name)
| flatten instrumentationScope
| fields severityText, name, version
```
{% include copy.html %}
{% include try-in-playground.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| severityText | name | version |
| --- | --- | --- |
| INFO | @opentelemetry/instrumentation-http | 0.57.0 |
| INFO | Microsoft.Extensions.Hosting | 9.0.0 |
| WARN | go.opentelemetry.io/contrib/instrumentation/google.golang.org/grpc/otelgrpc | 0.49.0 |
| ERROR | @opentelemetry/instrumentation-http | 0.57.0 |

<!-- vale on -->
  

## 限制

`flatten` 命令有下列限制：

* 若要扁平化的欄位無法顯示，`flatten` 命令可能無法如預期運作。例如，在查詢 `source=my-index | fields message | flatten message` 中，`flatten message` 命令無法如預期執行，因為某些扁平化欄位（例如 `message.info` 和 `message.author`）在 `fields message` 命令之後會隱藏。替代做法是使用 `source=my-index | flatten message`。
