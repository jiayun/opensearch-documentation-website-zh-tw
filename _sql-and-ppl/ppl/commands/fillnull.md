---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: fillnull
parent: Commands
grand_parent: PPL
nav_order: 19
---

<!-- vale off -->

# fillnull 命令

<!-- vale on -->

`fillnull` 命令會以指定的值取代搜尋結果中一或多個欄位裡的 `null` 值。

`fillnull` 命令不會改寫為[查詢領域特定語言（Query DSL）]({{site.url}}{{site.baseurl}}/query-dsl/)，只會在協調節點上執行。
{: .note}

## 語法

`fillnull` 命令的語法如下：

```sql
fillnull with <replacement> [in <field-list>]
fillnull using <field> = <replacement> [, <field> = <replacement>]
fillnull value=<replacement> [<field-list>]
```

可使用下列語法變化：

* `with <replacement> in <field-list>` -- 將相同的值套用至指定的欄位。
* `using <field>=<replacement>, ...` -- 將不同的值套用至不同的欄位。
* `value=<replacement> [<field-list>]` -- 替代語法，可選用以空格分隔的欄位清單。

## 參數

`fillnull` 命令支援下列參數。

| 參數 | 必要/選用 | 說明 |
| --- | --- | --- |
| `<replacement>` | 必要 | 用來取代 null 值的值。 |
| `<field>` | 必要 (使用 `using` 語法時) | 套用特定取代值的欄位名稱。 |
| `<field-list>` | 選用 | 要取代 null 值的欄位清單。您可以將清單指定為逗號分隔 (使用 `with` 或 `using` 語法) 或空格分隔 (使用 `value=` 語法)。預設會處理所有欄位。 |

## 範例 1：為每個欄位以不同的值取代 null 值

下列查詢會以預設值填入遺漏的檢測範圍名稱：

```sql
source=otellogs
| where severityText IN ('ERROR', 'WARN')
| fields severityText, `resource.attributes.service.name`, instrumentationScope.name
| fillnull using instrumentationScope.name = 'unknown'
| sort `resource.attributes.service.name`
```
{% include copy.html %}
{% include try-in-playground.html %}

查詢會傳回下列結果：

<!-- vale off -->

| severityText | resource.attributes.service.name | instrumentationScope.name |
| --- | --- | --- |
| ERROR | checkout | unknown |
| ERROR | checkout | unknown |
| ERROR | frontend-proxy | unknown |
| WARN | frontend-proxy | unknown |
| WARN | frontend-proxy | unknown |
| ERROR | payment | @opentelemetry/instrumentation-http |
| ERROR | payment | unknown |
| WARN | product-catalog | go.opentelemetry.io/contrib/instrumentation/google.golang.org/grpc/otelgrpc |
| WARN | product-catalog | unknown |
| ERROR | product-catalog | unknown |
| ERROR | recommendation | unknown |

<!-- vale on -->


## 範例 2：使用 value= 語法取代 null 值

下列查詢使用 `value=` 語法填入值為 null 的檢測範圍名稱，協助識別尚未加入檢測機制的服務：

```sql
source=otellogs
| where severityText = 'ERROR'
| fields severityText, `resource.attributes.service.name`, instrumentationScope.name
| fillnull value='unknown' instrumentationScope.name
| sort `resource.attributes.service.name`
```
{% include copy.html %}
{% include try-in-playground.html %}

查詢會傳回下列結果：

<!-- vale off -->

| severityText | resource.attributes.service.name | instrumentationScope.name |
| --- | --- | --- |
| ERROR | checkout | unknown |
| ERROR | checkout | unknown |
| ERROR | frontend-proxy | unknown |
| ERROR | payment | @opentelemetry/instrumentation-http |
| ERROR | payment | unknown |
| ERROR | product-catalog | unknown |
| ERROR | recommendation | unknown |

<!-- vale on -->


## 限制

`fillnull` 命令有下列限制：

* 在未指定欄位名稱的情況下將相同的值套用至所有欄位時，所有欄位必須屬於相同類型。若為混合類型，請使用個別的 `fillnull` 命令或明確指定欄位。
* 取代值的類型必須符合欄位清單中所有欄位的類型。將相同的值套用至多個欄位時，所有欄位必須屬於相同類型 (全部為字串或全部為數值)。下列查詢顯示違反此規則時發生的錯誤：

    ```sql
      # This FAILS - same value for mixed-type fields
      source=accounts | fillnull value=0 firstname, age
      # ERROR: fillnull failed: replacement value type INTEGER is not compatible with field 'firstname' (type: VARCHAR). The replacement value type must match the field type.
    ```