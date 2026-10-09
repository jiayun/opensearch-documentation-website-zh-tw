---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: nomv
parent: Commands
grand_parent: PPL
nav_order: 32
---

<!-- vale off -->

# nomv 命令

<!-- vale on -->

`nomv` 命令會以換行字元 (`\n`) 連接陣列的所有元素，將多值 (陣列) 欄位轉換為單值字串欄位。此操作會就地執行，以連接後的字串表示取代原始欄位。

該欄位必須是陣列類型。若是純量欄位，請先使用 [`array()`]({{site.url}}{{site.baseurl}}/sql-and-ppl/ppl/functions/collection/#array) 函式將值轉換為陣列。
{: .note}

## 語法

`nomv` 命令的語法如下：

```sql
nomv <field>
```

## 參數

`nomv` 命令支援下列參數。

| 參數 | 必要/選用 | 說明 |
| --- | --- | --- |
| `<field>` | 必要 | 要將多值內容轉換為單值字串的欄位名稱。 |

## 範例：將收集的清單轉換為單值字串

下列查詢會將所有服務名稱收集到一個陣列中，接著篩選出僅回報錯誤的服務，並將該陣列轉換為字串：

```sql
source=otellogs
| where severityText = 'ERROR'
| stats list(`resource.attributes.service.name`) as affected_services by severityText
| nomv affected_services
| fields severityText, affected_services
```
{% include copy.html %}
{% include try-in-playground.html %}

查詢會傳回下列結果：

<!-- vale off -->

| severityText | affected_services |
| --- | --- |
| ERROR | payment |
|  | checkout |
|  | payment |
|  | frontend-proxy |
|  | recommendation |
|  | product-catalog |
|  | checkout |

<!-- vale on -->

## 限制

`nomv` 命令有下列限制：

- `nomv` 命令僅在啟用 Apache Calcite 查詢引擎時可用。
- 換行分隔符 (`\n`) 是固定的，無法自訂。若需自訂分隔符，請在 [`eval`]({{site.url}}{{site.baseurl}}/sql-and-ppl/ppl/commands/eval/) 運算式中直接使用 [`mvjoin`]({{site.url}}{{site.baseurl}}/sql-and-ppl/ppl/functions/collection/#mvjoin) 函式。
- 陣列中的 `NULL` 值會自動被篩除，不會出現在輸出中。

## 相關命令

- [`mvcombine`]({{site.url}}{{site.baseurl}}/sql-and-ppl/ppl/commands/mvcombine/) -- 將多列合併為單一列，並包含多值欄位。
- [`mvexpand`]({{site.url}}{{site.baseurl}}/sql-and-ppl/ppl/commands/mvexpand/) -- 將多值欄位展開為個別的列。
