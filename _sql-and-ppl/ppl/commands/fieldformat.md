---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: fieldformat
parent: Commands
grand_parent: PPL
nav_order: 17
---

<!-- vale off -->

# fieldformat 命令

<!-- vale on -->

`fieldformat` 命令會將欄位設定為指定運算式的結果，並將評估後的欄位附加到搜尋結果。此命令是 [`eval`]({{site.url}}{{site.baseurl}}/sql-and-ppl/ppl/commands/eval/) 的別名。

它也支援使用點 (`.`) 運算子進行字串串接，讓您可以將字串附加到運算式。

## 語法

`fieldformat` 命令具有下列語法：

```sql
 fieldformat <field>=[(prefix).]<expression>[.(suffix)] ["," <field>=[(prefix).]<expression>[.(suffix)] ]...
```

## 參數

`fieldformat` 命令支援下列參數。

| 參數| 必要/選用 | 說明                                                                                                                                   |
|----------------|-------------------|-----------------------------------------------------------------------------------------------------------------------------------------------|
| `<field>`      | 必要 | 要建立或更新的欄位名稱。若欄位不存在，則會新增該欄位。若欄位已存在，則會覆寫其值。 |
| `<expression>` | 必要 | 要評估的運算式。可包含使用點 (`.`) 運算子串接的選用前置字串及/或後置字串。 |
| `prefix`       | 選用 | 置於運算式前面的字串。使用點 (`.`) 運算子結合時，會串接為評估結果的前置字串。 |
| `suffix`       | 選用 | 置於運算式後面的字串。使用點 (`.`) 運算子結合時，會串接為評估結果的後置字串。 |

## 範例 1：建立用於事件分類的計算欄位  

下列查詢會建立一個 `is_critical` 欄位，用來指出記錄項目是否代表重大問題，適合在儀表板中進行篩選：
  
```sql
source=otellogs
| where severityText IN ('ERROR', 'WARN')
| fieldformat is_critical = IF(severityNumber >= 21, 'CRITICAL', 'ERROR')
| sort severityNumber, `resource.attributes.service.name`
| fields severityText, `resource.attributes.service.name`, is_critical
| head 4
```
{% include copy.html %}
{% include try-in-playground.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| severityText | resource.attributes.service.name | is_critical |
| --- | --- | --- |
| WARN | frontend-proxy | ERROR |
| WARN | frontend-proxy | ERROR |
| WARN | product-catalog | ERROR |
| WARN | product-catalog | ERROR |

<!-- vale on -->
  

## 範例 2：以格式化值覆寫欄位  

下列查詢會以人類可讀的嚴重性層級覆寫 `severityNumber` 欄位：
  
```sql
source=otellogs
| dedup severityText
| sort severityNumber
| fieldformat severityNumber = CASE(severityNumber < 9, 'low', severityNumber < 17, 'medium', severityNumber >= 17, 'high')
| fields severityText, severityNumber
```
{% include copy.html %}
{% include try-in-playground.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| severityText | severityNumber |
| --- | --- |
| DEBUG | low |
| INFO | medium |
| WARN | medium |
| ERROR | high |

<!-- vale on -->
  
## 相關命令

- [`eval`]({{site.url}}{{site.baseurl}}/sql-and-ppl/ppl/commands/eval/)