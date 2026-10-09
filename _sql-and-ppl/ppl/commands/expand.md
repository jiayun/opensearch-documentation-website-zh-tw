---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: expand
parent: Commands
grand_parent: PPL
nav_order: 15
---

<!-- vale off -->

# expand 命令

<!-- vale on -->

`expand` 命令會將含有巢狀陣列欄位的單一文件轉換為多份文件，每份文件各包含該陣列中的一個元素。原始文件中的所有其他欄位都會複製到產生的文件中。

`expand` 命令的運作方式如下：

* 它會為指定陣列欄位中的每個元素產生一列。
* 指定的陣列欄位會轉換成個別資料列。
* 若提供別名，展開後的值會顯示在別名之下，而非原始欄位名稱。
* 若指定的欄位是空陣列，則會保留該列，並將展開的欄位設為 `null`。

## 語法

`expand` 命令的語法如下：

```sql
expand <field> [as alias]
```

## 參數

`expand` 命令支援下列參數。

| 參數 | 必要/選用 | 說明 |
| --- | --- | --- |
| `<field>` | 必要 | 要展開的欄位。僅支援巢狀陣列。 |
| `<alias>` | 選用 | 用來取代原始欄位名稱的名稱。 |  
  

## 範例：將收集到的服務清單展開為個別資料列  

下列查詢會先使用 `stats list()` 將每個嚴重性層級的所有服務名稱收集到陣列中，再將每個陣列元素展開為各自的資料列。當您需要從彙總檢視回到個別資料列時，這項功能相當實用：
  
```sql
source=otellogs
| where severityText = 'WARN'
| stats list(`resource.attributes.service.name`) as services by severityText
| expand services as service
| fields severityText, service
```
{% include copy.html %}
{% include try-in-playground.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| severityText | service |
| --- | --- |
| WARN | product-catalog |
| WARN | product-catalog |
| WARN | frontend-proxy |
| WARN | frontend-proxy |

<!-- vale on -->
  

## 限制

`expand` 命令有下列限制：

* `expand` 命令僅支援巢狀陣列。不支援儲存陣列的原始類型欄位。例如，儲存字串陣列的字串欄位無法展開。
