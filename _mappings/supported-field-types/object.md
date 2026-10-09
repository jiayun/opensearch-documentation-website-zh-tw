---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "物件"
nav_order: 41
has_children: false
parent: Object field types
grand_parent: Supported field types
redirect_from: 
  - /field-types/supported-field-types/object/
  - /opensearch/supported-field-types/object/
  - /field-types/object/
---

# 物件欄位類型
**於 1.0 版導入**
{: .label .label-purple }

物件欄位類型包含一個 JSON 物件（一組名稱/值配對）。JSON 物件中的值可以是另一個 JSON 物件。在對應物件欄位時，不需要指定 `object` 作為類型，因為 `object` 是預設類型。

## 範例

建立一個包含 object 欄位的對應：

```json
PUT testindex1/_mappings
{
    "properties": {
      "patient": { 
        "properties" :
          {
            "name" : {
              "type" : "text"
            },
            "id" : {
              "type" : "keyword"
            }
          }   
      }
    }
}
```
{% include copy-curl.html %}

將一個包含 object 欄位的文件編製索引：

```json
PUT testindex1/_doc/1
{ 
  "patient": { 
    "name" : "John Doe",
    "id" : "123456"
  } 
}
```
{% include copy-curl.html %}

巢狀物件在內部以扁平的鍵值配對形式儲存。若要參照巢狀物件中的欄位，請使用 `parent field`.`child field`（例如 `patient.id`）。

搜尋 ID 為 123456 的病患：

```json
GET testindex1/_search
{
  "query": {
    "term" : {
      "patient.id" : "123456"
    }
  }
}
```
{% include copy-curl.html %}

## 參數

下表列出物件欄位類型接受的參數。所有參數皆為選用。

參數 | 說明 
:--- | :--- 
[`dynamic`](#the-dynamic-parameter) | 指定是否可以動態地將新欄位新增至物件。有效值為 `true`、`false`、`strict`、`strict_allow_templates` 和 `false_allow_templates`。預設值為 `true`。
`enabled` | 一個布林值，指定是否應解析物件的 JSON 內容。若 `enabled` 設定為 `false`，物件的內容不會被編製索引，也無法搜尋，但仍可從 `_source` 欄位擷取。預設值為 `true`。
`properties` | 此物件的欄位，可以是任何支援的類型。若 `dynamic` 設定為 `true`，則可以動態地將新屬性新增至此物件。

### `dynamic` 參數

`dynamic` 參數指定是否可以動態地將新欄位新增至已編製索引的物件。

例如，您可以先建立一個對應，其中包含只有一個欄位的 `patient` 物件：

```json
PUT testindex1/_mappings
{
    "properties": {
      "patient": { 
        "properties" :
          {
            "name" : {
              "type" : "text"
            }
          }   
      }
    }
}
```
{% include copy-curl.html %}

接著，您將一個在 `patient` 中含有新 `id` 欄位的文件編製索引：

```json
PUT testindex1/_doc/1
{ 
  "patient": { 
    "name" : "John Doe",
    "id" : "123456"
  } 
}
```
{% include copy-curl.html %}

結果，欄位 `id` 會被新增至對應：

```json
{
  "testindex1" : {
    "mappings" : {
      "properties" : {        
        "patient" : {
          "properties" : {
            "id" : {
              "type" : "text",
              "fields" : {
                "keyword" : {
                  "type" : "keyword",
                  "ignore_above" : 256
                }
              }
            },
            "name" : {
              "type" : "text"
            }
          }
        }
      }
    }
  }
}
```

`dynamic` 參數有以下有效值。

值 | 說明 
:--- | :--- 
`true` | 可以動態地將新欄位新增至對應。這是預設值。
`false` | 無法動態地將新欄位新增至對應。若偵測到新欄位，該欄位不會被編製索引，也無法搜尋，但仍可從 `_source` 欄位擷取。 
`strict` | 當動態地將新欄位新增至對應時，會擲回例外狀況。若要將新欄位新增至物件，您必須先將其新增至對應。
`strict_allow_templates` | 若新偵測到的欄位符合對應中任何預先定義的動態範本，則會將其新增至對應；若不符合任何範本，則會擲回例外狀況。
`false_allow_templates` | 若新偵測到的欄位符合對應中任何預先定義的動態範本，則會將其新增至對應。只有符合動態範本或對應屬性的欄位會被編製索引。

內部物件會從其父物件繼承 `dynamic` 參數值，除非它們自行宣告 `dynamic` 參數值。
{: .note }

## 相關文件

- [停用物件]({{site.url}}{{site.baseurl}}/mappings/mapping-parameters/disable-objects/)
