---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "動態範本"
nav_order: 105
has_children: false
has_toc: false
---

# 動態範本

動態範本定義 OpenSearch 在透過[動態對應]({{site.url}}{{site.baseurl}}/mappings/#dynamic-mapping)新增欄位時所套用的對應。若沒有範本，OpenSearch 會根據欄位的 JSON 值為每個新欄位指派預設類型，例如字串使用 `text` 並附帶 `keyword` 子欄位，整數則使用 `long`。動態範本會為其符合的欄位取代這些預設值。

當您無法事先列出所有欄位，但知道某些欄位群組應如何對應時，可以使用動態範本。例如，您可以將所有名稱以 `_id` 結尾的欄位對應為 `keyword`、將整數儲存為 `integer` 以節省空間，或將物件中的每個欄位複製到單一搜尋欄位。

範本會依下列一或多項條件選取欄位：

- OpenSearch 為該值偵測到的 JSON 資料類型，在 `match_mapping_type` 中指定
- 欄位名稱，在 `match` 與 `unmatch` 中指定
- 欄位在文件中的位置，例如 `address.city`，在 `path_match` 與 `path_unmatch` 中指定

動態範本僅適用於對應中尚不存在的欄位，不會變更已對應的欄位。如果您將 [`dynamic`]({{site.url}}{{site.baseurl}}/mappings/mapping-parameters/dynamic/) 參數設為 `strict_allow_templates` 或 `false_allow_templates`，OpenSearch 只會在欄位符合動態範本時才新增該欄位。

## 範本結構

在索引對應的 `dynamic_templates` 陣列中定義動態範本。每個陣列元素都是一個物件，包含單一具名範本：

```json
"dynamic_templates": [
  {
    "<template_name>": {
      "match_mapping_type": "<detected_type>",
      "match": "<field_name_pattern>",
      "mapping": {
        "type": "<field_type>"
      }
    }
  }
]
```

範本名稱由您自行選擇。OpenSearch 在傳回對應以及回報錯誤時，會使用該名稱來識別範本，因此請選擇一個能描述範本目標欄位的名稱。

## 動態範本參數

下表列出範本參數。

參數 | 說明
:--- | :---
`match_mapping_type` | 要符合的偵測 JSON 資料類型。使用 `*` 可符合所有類型。有效值請參閱[符合資料類型](#matching-data-types)。
`match` | 欄位名稱必須符合的模式。該模式僅套用於欄位名稱，不套用於完整路徑。
`unmatch` | 排除由 `match` 選取之欄位名稱的模式。
`match_pattern` | 指定 OpenSearch 如何解讀 `match`、`unmatch`、`path_match` 與 `path_unmatch` 中的模式。有效值為：<br> - `simple`：模式支援 `*` 萬用字元。<br> - `regex`：模式為 Java 正規表示式。<br><br>預設值為 `simple`。
`path_match` | 欄位的完整點號路徑必須符合的模式，例如 `address.*`。
`path_unmatch` | 排除由 `path_match` 選取之路徑的模式。
`mapping` | 必要。要套用至符合欄位的對應。可包含 `{name}` 與 `{dynamic_type}` [範本變數](#template-variables)。

## 動態範本規則

定義動態範本時，請注意下列規則：

- 每個範本必須至少包含 `match_mapping_type`、`match` 或 `path_match` 其中之一。僅包含 `unmatch` 或 `path_unmatch` 的範本會被拒絕。
- 包含無法識別之參數的範本會被拒絕。
- OpenSearch 依陣列順序檢查範本，並套用第一個符合欄位的範本。請將較具體的範本放在較通用的範本之前。
- OpenSearch 會在欄位第一次有值時，將該新欄位加入對應。值為 `null` 或空陣列 (`[]`) 的欄位不會被對應，也不會為其評估任何範本。如果範本設定了 `null_value`，該設定對欄位首次對應之前已編製索引的文件沒有影響。

OpenSearch 會在您建立或更新對應時檢查範本中的模式，但不會完整驗證 `mapping` 的內容。例如，指定不存在之欄位類型的範本會被接受，且 OpenSearch 會在棄用記錄檔中寫入警告。該範本只有在符合的欄位被編製索引時才會失敗，此時 OpenSearch 會拒絕該文件。包含 `{name}` 變數的範本無法事先驗證，因為欄位名稱未知。在正式環境使用新範本之前，請先透過為範例文件編製索引來測試。
{: .note}

不含 `match_mapping_type` 的範本可以接收任何類型的值，但其 `mapping` 可能僅對其中部分類型有效。如果範本的對應對至少一種偵測到的類型有效，OpenSearch 就會接受該範本。例如，下列範本省略了 `type`，因此 OpenSearch 會使用偵測到的類型，並設定 `analyzer`，而該選項只有 `text` 欄位才接受：

```json
PUT /dt-no-type
{
  "mappings": {
    "dynamic_templates": [
      {
        "code_fields": {
          "match": "*_code",
          "mapping": {
            "analyzer": "simple"
          }
        }
      }
    ]
  }
}
```
{% include copy-curl.html %}

包含 `"country_code": "US"` 的文件會被編製索引，且 `country_code` 會使用 `simple` 分析器對應為 `text`。包含 `"zip_code": 97205` 的文件會被拒絕，因為 `long` 欄位不接受分析器。若要讓範本僅套用於字串值，請加入 `"match_mapping_type": "string"`。

## 更新動態範本

若要變更現有索引的範本，請使用 [Create or Update Index Mappings API]({{site.url}}{{site.baseurl}}/api-reference/index-apis/put-mapping/) 傳送完整的 `dynamic_templates` 陣列。新陣列會取代所有現有範本，因此您可以使用此請求重新排序或移除範本。若要移除所有範本，請傳送空陣列。先前已由範本對應的欄位會保留其對應。

## 符合資料類型

`match_mapping_type` 參數會符合 OpenSearch 在 JSON 值中偵測到的資料類型。由於 JSON 不區分整數大小或浮點數精確度，OpenSearch 會偵測最寬的類型。下表列出您可以在 `match_mapping_type` 中指定的值。

值 | 符合的資料類型
:--- | :---
`string` | 未被偵測為日期的字串值。
`long` | 沒有小數部分的數字。
`double` | 有小數部分的數字。
`boolean` | 值 `true` 與 `false`。
`date` | 符合 `dynamic_date_formats` 中某種格式的字串。需要啟用 `date_detection`，此為預設值。更多資訊請參閱[日期偵測]({{site.url}}{{site.baseurl}}/mappings/#date-detection)。
`object` | JSON 物件。
`binary` | 二進位值。JSON 無法包含二進位值，因此此類型僅適用於 CBOR 和 SMILE 等二進位內容格式。
`knn_vector` | 可對應為向量的數字陣列。更多資訊請參閱 [k-NN 向量動態範本]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/knn-vector/#dynamic-templates)。
`*` | 所有資料類型。

偵測到的類型不會決定對應後的類型。例如，符合 `long` 的範本可以將欄位對應為 `integer`，而符合 `string` 的範本可以將欄位對應為 `long`。

### 範例：將整數對應為 integer

建立一個包含兩個範本的索引。第一個範本將整數對應為 `integer`，第二個範本將字串對應為 `text`，並附帶 `exact` 關鍵字子欄位：

```json
PUT /dt-orders
{
  "mappings": {
    "dynamic_templates": [
      {
        "whole_numbers": {
          "match_mapping_type": "long",
          "mapping": {
            "type": "integer"
          }
        }
      },
      {
        "strings_with_exact": {
          "match_mapping_type": "string",
          "mapping": {
            "type": "text",
            "fields": {
              "exact": {
                "type": "keyword",
                "ignore_above": 256
              }
            }
          }
        }
      }
    ]
  }
}
```
{% include copy-curl.html %}

為包含多種類型值的文件編製索引：

```json
PUT /dt-orders/_doc/1
{
  "item_count": 3,
  "customer_name": "Ana Rivera",
  "total": 42.5,
  "gift": true,
  "order_date": "2026-09-30",
  "empty_list": [],
  "note": null
}
```
{% include copy-curl.html %}

擷取對應：

```json
GET /dt-orders/_mapping
```
{% include copy-curl.html %}

在回應中，`item_count` 被對應為 `integer`，`customer_name` 被對應為 `text`，並附帶 `exact` 子欄位。`total`、`gift` 和 `order_date` 欄位不符合任何範本，因此它們會收到預設的動態對應。`empty_list` 和 `note` 欄位不會加入對應，因為它們不含具體值：

```json
{
  "dt-orders": {
    "mappings": {
      "dynamic_templates": [
        {
          "whole_numbers": {
            "match_mapping_type": "long",
            "mapping": {
              "type": "integer"
            }
          }
        },
        {
          "strings_with_exact": {
            "match_mapping_type": "string",
            "mapping": {
              "fields": {
                "exact": {
                  "ignore_above": 256,
                  "type": "keyword"
                }
              },
              "type": "text"
            }
          }
        }
      ],
      "properties": {
        "customer_name": {
          "type": "text",
          "fields": {
            "exact": {
              "type": "keyword",
              "ignore_above": 256
            }
          }
        },
        "gift": {
          "type": "boolean"
        },
        "item_count": {
          "type": "integer"
        },
        "order_date": {
          "type": "date"
        },
        "total": {
          "type": "float"
        }
      }
    }
  }
}
```

## 比對欄位名稱

`match` 參數依名稱選取欄位，而 `unmatch` 則從該選取範圍中排除欄位。這兩個參數僅與欄位名稱進行比對。例如，`"match": "city"` 同時符合頂層的 `city` 欄位以及物件內的 `store.city` 欄位。

### 範例：依欄位名稱將數字字串對應為數值

某些資料來源會以字串傳送數字。建立一個索引，將名稱以 `reading_` 開頭的字串欄位對應為 `double`，但名稱以 `_label` 結尾的欄位除外：

```json
PUT /dt-sensor
{
  "mappings": {
    "dynamic_templates": [
      {
        "numeric_strings": {
          "match_mapping_type": "string",
          "match": "reading_*",
          "unmatch": "*_label",
          "mapping": {
            "type": "double"
          }
        }
      }
    ]
  }
}
```
{% include copy-curl.html %}

為包含這兩種欄位的文件編製索引：

```json
PUT /dt-sensor/_doc/1
{
  "reading_temp": "21.7",
  "reading_label": "lobby"
}
```
{% include copy-curl.html %}

擷取對應：

```json
GET /dt-sensor/_mapping
```
{% include copy-curl.html %}

`reading_temp` 欄位被對應為 `double`。`reading_label` 欄位被 `unmatch` 排除，因此它會收到預設的字串對應：

```json
{
  "dt-sensor": {
    "mappings": {
      ...
      "properties": {
        "reading_label": {
          "type": "text",
          "fields": {
            "keyword": {
              "type": "keyword",
              "ignore_above": 256
            }
          }
        },
        "reading_temp": {
          "type": "double"
        }
      }
    }
  }
}
```

### 範例：使用規則運算式比對欄位名稱

將 `match_pattern` 設定為 `regex`，即可使用 Java 規則運算式撰寫模式。建立一個索引，僅將 `revenue_q1` 到 `revenue_q4` 的欄位對應為 `scaled_float`：

```json
PUT /dt-regex
{
  "mappings": {
    "dynamic_templates": [
      {
        "quarterly_revenue": {
          "match_pattern": "regex",
          "match": "^revenue_q[1-4]$",
          "mapping": {
            "type": "scaled_float",
            "scaling_factor": 100
          }
        }
      }
    ]
  }
}
```
{% include copy-curl.html %}

為包含三個營收欄位的文件編製索引：

```json
PUT /dt-regex/_doc/1
{
  "revenue_q1": 1250.75,
  "revenue_q5": 10.5,
  "revenue_total": 5000.1
}
```
{% include copy-curl.html %}

擷取對應：

```json
GET /dt-regex/_mapping
```
{% include copy-curl.html %}

只有 `revenue_q1` 符合該規則運算式。另外兩個欄位會收到預設的 `float` 對應：

```json
{
  "dt-regex": {
    "mappings": {
      ...
      "properties": {
        "revenue_q1": {
          "type": "scaled_float",
          "scaling_factor": 100.0
        },
        "revenue_q5": {
          "type": "float"
        },
        "revenue_total": {
          "type": "float"
        }
      }
    }
  }
}
```

如果模式不是有效的規則運算式，OpenSearch 會拒絕該對應。

## 比對欄位路徑

`path_match` 和 `path_unmatch` 參數的運作方式類似於 `match` 和 `unmatch`，但它們是將模式與所有父物件及欄位的名稱（以句點連接）進行比對。例如，`address` 物件中 `city` 欄位的路徑為 `address.city`。請使用這些參數來選取特定物件內的欄位。

### 範例：將物件欄位複製到單一欄位

建立一個索引，將 `address` 物件中的每個欄位對應為 `text`，並將其值複製到頂層的 `full_address` 欄位。`zip_code` 欄位會被排除：

```json
PUT /dt-contacts
{
  "mappings": {
    "dynamic_templates": [
      {
        "address_lines": {
          "path_match": "address.*",
          "path_unmatch": "*.zip_code",
          "mapping": {
            "type": "text",
            "copy_to": "full_address"
          }
        }
      }
    ]
  }
}
```
{% include copy-curl.html %}

為包含 `address` 物件的文件編製索引：

```json
PUT /dt-contacts/_doc/1?refresh=true
{
  "address": {
    "street": "221 Harbor Lane",
    "city": "Portland",
    "zip_code": "97205"
  }
}
```
{% include copy-curl.html %}

擷取對應：

```json
GET /dt-contacts/_mapping
```
{% include copy-curl.html %}

`street` 和 `city` 欄位使用範本進行對應，而 `zip_code` 則收到預設的字串對應。`full_address` 欄位未出現在文件中，因此 OpenSearch 會在第一次有值複製到該欄位時，將它加入對應：

```json
{
  "dt-contacts": {
    "mappings": {
      ...
      "properties": {
        "address": {
          "properties": {
            "city": {
              "type": "text",
              "copy_to": [
                "full_address"
              ]
            },
            "street": {
              "type": "text",
              "copy_to": [
                "full_address"
              ]
            },
            "zip_code": {
              "type": "text",
              "fields": {
                "keyword": {
                  "type": "keyword",
                  "ignore_above": 256
                }
              }
            }
          }
        },
        "full_address": {
          "type": "text",
          "fields": {
            "keyword": {
              "type": "keyword",
              "ignore_above": 256
            }
          }
        }
      }
    }
  }
}
```

現在您可以在單一查詢中搜尋兩行地址：

```json
GET /dt-contacts/_search
{
  "query": {
    "match": {
      "full_address": "harbor portland"
    }
  }
}
```
{% include copy-curl.html %}

`path_match` 模式同時符合物件與分葉欄位。在此範例中，`address.*` 也會符合巢狀於 `address` 內的物件，而 OpenSearch 會嘗試將該物件對應為 `text`。為在 `address` 內包含 `unit` 物件的文件編製索引：

```json
PUT /dt-contacts/_doc/2
{
  "address": {
    "street": "9 Elm Court",
    "unit": {
      "number": "4B",
      "floor": 2
    }
  }
}
```
{% include copy-curl.html %}

OpenSearch 會拒絕該文件，因為物件無法被解析為 `text` 值。若要避免範本符合物件，請加入 `"match_mapping_type": "string"`。

## 範本變數

`mapping` 物件可包含下列變數，OpenSearch 在將範本套用至欄位時會取代這些變數：

- `{name}`：欄位的名稱
- `{dynamic_type}`：偵測到的欄位資料類型，例如 `long` 或 `boolean`

### 範例：在對應中使用欄位名稱與偵測到的類型

建立包含兩個範本的索引。第一個範本將每個字串欄位對應為 `text`，並使用欄位名稱作為分析器名稱。第二個範本套用至所有其餘欄位，保留偵測到的類型，並停用 doc values：

```json
PUT /dt-placeholders
{
  "mappings": {
    "dynamic_templates": [
      {
        "language_analyzers": {
          "match_mapping_type": "string",
          "match": "*",
          "mapping": {
            "type": "text",
            "analyzer": "{name}"
          }
        }
      },
      {
        "detected_type_without_doc_values": {
          "match_mapping_type": "*",
          "mapping": {
            "type": "{dynamic_type}",
            "doc_values": false
          }
        }
      }
    ]
  }
}
```
{% include copy-curl.html %}

將包含以內建[語言分析器]({{site.url}}{{site.baseurl}}/analyzers/language-analyzers/index/)命名的欄位的文件編製索引：

```json
PUT /dt-placeholders/_doc/1
{
  "english": "Running shoes for trail use",
  "french": "Chaussures de course",
  "views": 120
}
```
{% include copy-curl.html %}

擷取對應：

```json
GET /dt-placeholders/_mapping
```
{% include copy-curl.html %}

`english` 與 `french` 欄位使用同名的分析器，而 `views` 對應為 `long`，並停用 doc values：

```json
{
  "dt-placeholders": {
    "mappings": {
      ...
      "properties": {
        "english": {
          "type": "text",
          "analyzer": "english"
        },
        "french": {
          "type": "text",
          "analyzer": "french"
        },
        "views": {
          "type": "long",
          "doc_values": false
        }
      }
    }
  }
}
```

由於第一個範本符合每個字串欄位，名稱不是分析器名稱的字串欄位會導致 OpenSearch 拒絕該文件。例如，包含 `description` 欄位的文件會遭到拒絕，因為沒有名為 `description` 的分析器。

## 常見範本模式

下列範例顯示常見索引需求的範本。

### 縮減指標的索引大小

指標文件通常包含許多數值欄位，這些欄位用於彙總和儀表板，但很少出現在查詢篩選條件中。將這些欄位對應時把 [`index`]({{site.url}}{{site.baseurl}}/mappings/mapping-parameters/index-parameter/) 設為 `false`，會略過為它們建立搜尋索引，可節省磁碟空間和編製索引時間。Doc values 仍會寫入，因此彙總和排序不受影響。您仍可查詢這些欄位，因為 OpenSearch 會改為搜尋數值 doc values，但這類查詢的執行速度比對已編製索引欄位的查詢慢：

```json
PUT /dt-metrics
{
  "mappings": {
    "dynamic_templates": [
      {
        "metric_counters": {
          "match_mapping_type": "long",
          "mapping": {
            "type": "long",
            "index": false
          }
        }
      },
      {
        "metric_gauges": {
          "match_mapping_type": "double",
          "mapping": {
            "type": "float",
            "index": false
          }
        }
      }
    ]
  }
}
```
{% include copy-curl.html %}

`metric_gauges` 範本使用 `float`，這是動態對應預設指派給小數的相同類型。`float` 每個值佔用 4 個位元組，而 `double` 佔用 8 個位元組，且其精確度對於負載平均值和百分比等值已足夠。

### 將識別碼欄位對應為關鍵字

商店編號和訂單編號等識別碼會進行完全相符比對，且絕不會用於範圍查詢或計算，即使它們是數值也一樣。下列範本將名稱以 `_id` 結尾的每個欄位對應為 `keyword`，無論其值是字串還是數字：

```json
PUT /dt-id-fields
{
  "mappings": {
    "dynamic_templates": [
      {
        "identifiers": {
          "match": "*_id",
          "mapping": {
            "type": "keyword"
          }
        }
      }
    ]
  }
}
```
{% include copy-curl.html %}

包含 `"store_id": 17` 和 `"order_id": "A-1001"` 的文件會將兩個欄位都對應為 `keyword`。若沒有此範本，`store_id` 會對應為 `long`。由於範本未指定 `match_mapping_type`，它也會符合名稱以 `_id` 結尾的物件。OpenSearch 會拒絕包含這類物件的文件，因為物件無法對應為 `keyword`。如果您的文件包含這類物件，請定義兩個包含相同 `match` 模式的範本，一個使用 `"match_mapping_type": "string"`，另一個使用 `"match_mapping_type": "long"`。如此一來，物件不會符合任一範本，並會對應為 `object` 欄位。

### 僅將字串對應為關鍵字

如果您只搜尋字串欄位的確切值，並將其用於篩選、排序和彙總，您可以將它們對應為 `keyword` 而不使用 `text` 欄位，藉此略過全文索引。此時查詢必須符合完整的已編製索引值，因此搜尋 `Green` 不會符合值 `Forest Green`：

```json
PUT /dt-keyword-only
{
  "mappings": {
    "dynamic_templates": [
      {
        "exact_value_strings": {
          "match_mapping_type": "string",
          "mapping": {
            "type": "keyword"
          }
        }
      }
    ]
  }
}
```
{% include copy-curl.html %}

### 將自由格式物件對應為扁平物件

當物件包含因文件而異的索引鍵時，例如不同賣家提供的產品屬性，每個新索引鍵都會在對應中新增一個欄位，並可能導致[對應爆炸]({{site.url}}{{site.baseurl}}/mappings/mapping-explosion/)。下列範本將名稱以 `_attributes` 結尾的任何物件對應為單一 [`flat_object`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/flat-object/) 欄位。其他物件則正常對應：

```json
PUT /dt-flat-attributes
{
  "mappings": {
    "dynamic_templates": [
      {
        "free_form_objects": {
          "match_mapping_type": "object",
          "match": "*_attributes",
          "mapping": {
            "type": "flat_object"
          }
        }
      }
    ]
  }
}
```
{% include copy-curl.html %}

`product_attributes` 物件會對應為一個 `flat_object` 欄位，無論它包含多少個索引鍵，您仍可使用點記法查詢其子欄位，例如 `product_attributes.dimensions.width`。

### 停用字串欄位的 norms

[Norms]({{site.url}}{{site.baseurl}}/mappings/mapping-parameters/norms/) 會儲存欄位長度資訊，OpenSearch 僅將其用於相關性評分。對於記錄訊息這類資料，您會依其他欄位進行篩選和排序，且不會依分數排序結果，停用 norms 可縮減索引大小。下列範本將字串對應為 `text` 且不使用 norms，並保留動態對應預設新增的 `keyword` 子欄位：

```json
PUT /dt-no-norms
{
  "mappings": {
    "dynamic_templates": [
      {
        "unscored_text": {
          "match_mapping_type": "string",
          "mapping": {
            "type": "text",
            "norms": false,
            "fields": {
              "keyword": {
                "type": "keyword",
                "ignore_above": 256
              }
            }
          }
        }
      }
    ]
  }
}
```
{% include copy-curl.html %}
