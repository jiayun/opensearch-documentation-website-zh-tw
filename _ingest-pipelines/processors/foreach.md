---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Foreach
parent: Ingest processors
nav_order: 110
---

<!-- vale off -->
# Foreach 處理器
<!-- vale on -->

`foreach` 處理器用於迭代輸入文件中的值清單，並對每個值套用轉換。這對於以一致方式處理陣列中的所有元素等工作非常有用，例如將陣列中的所有元素轉換為小寫或大寫。

以下是 `foreach` 處理器的語法：

```json
{
  "foreach": {
    "field": "<field_name>",
    "processor": {
      "<processor_type>": {
        "<processor_config>": "<processor_value>"
      }
    }
  }
}
```
{% include copy.html %}

## 參數

下表列出 `foreach` 處理器的必要與選用參數。

參數 | 必要/選用 | 說明 |
|-----------|-----------|-----------|
`field` | 必要 | 要逐一查看的陣列欄位。
`processor` | 必要 | 要為陣列中每個元素執行的處理器。
`ignore_missing` | 選用 | 若 `true` 且指定的欄位不存在或為 null，則處理器會直接結束，不會修改文件。預設值為 `false`。
`description` | 選用 | 處理器的簡短說明。
`if` | 選用 | 執行處理器的條件。
`ignore_failure` | 選用 | 指定處理器即使遇到錯誤是否仍繼續執行。若設為 `true`，則會忽略失敗。預設值為 `false`。
`on_failure` | 選用 | 處理器失敗時要執行的處理器清單。
`tag` | 選用 | 處理器的識別標籤。有助於偵錯時區分同類型的處理器。如需詳細資訊，請參閱[使用處理器標籤進行監控與偵錯]({{site.url}}{{site.baseurl}}/ingest-pipelines/create-ingest/#using-processor-tags-for-monitoring-and-debugging)。

## 存取陣列元素

對於每個陣列元素，`foreach` 處理器會將該元素儲存在 `_ingest._value` 資料匯入中繼資料欄位中，然後執行內部處理器。若要讀取或修改目前的元素，請將內部處理器的欄位設定為 `_ingest._value`。如果元素是物件，請使用點號表示法存取其欄位，例如 `_ingest._value.name`。

內部處理器也可以讀取和修改文件中的任何其他欄位。

當 `foreach` 處理器執行時，`_ingest._value` 一律保存目前的陣列元素，這會隱藏先前處理器儲存在 `_ingest._value` 中的任何值。當迴圈結束時，OpenSearch 會將先前的值放回，因此管線中較後面的處理器仍然可以讀取它。

## 使用處理器

依照下列步驟在管線中使用處理器。

### 步驟 1：建立管線

下列查詢會建立名為 `test-foreach` 的管線，該管線使用 `foreach` 處理器逐一走訪 `protocols` 欄位中的每個元素：

```json
PUT _ingest/pipeline/test-foreach  
{  
  "description": "Lowercase all the elements in an array",  
  "processors": [  
    {  
      "foreach": {  
        "field": "protocols",  
        "processor": {  
          "lowercase": {  
            "field": "_ingest._value"  
          }  
        }  
      }  
    }  
  ]  
}  
```
{% include copy-curl.html %}

### 步驟 2（選用）：測試管線

建議您在匯入文件之前先測試管線。
{: .tip}

若要測試管線，請執行下列查詢：

```json
POST _ingest/pipeline/test-foreach/_simulate  
{  
  "docs": [  
    {  
      "_index": "testindex1",  
      "_id": "1",  
      "_source": {  
        "protocols": ["HTTP","HTTPS","TCP","UDP"]  
      }  
    }  
  ]  
} 
```
{% include copy-curl.html %}

下列範例回應確認管線如預期運作，顯示四個元素已轉換為小寫：

```json
{  
  "docs": [  
    {  
      "doc": {  
        "_index": "testindex1",  
        "_id": "1",  
        "_source": {  
          "protocols": [  
            "http",  
            "https",  
            "tcp",  
            "udp"  
          ]  
        },  
        "_ingest": {  
          "_value": null,  
          "timestamp": "2024-05-23T02:44:10.8201Z"  
        }  
      }  
    }  
  ]  
}  

```

### 步驟 3：匯入文件

下列查詢會將文件匯入名為 `testindex1` 的索引：

```json
POST testindex1/_doc/1?pipeline=test-foreach  
{  
  "protocols": ["HTTP","HTTPS","TCP","UDP"]  
}  
```
{% include copy-curl.html %}

此請求會將文件編製索引至 `testindex1` 索引，並在編製索引前套用管線：

```json
{  
  "_index": "testindex1",  
  "_id": "1",  
  "_version": 6,  
  "result": "created",  
  "_shards": {  
    "total": 2,  
    "successful": 1,  
    "failed": 0  
  },  
  "_seq_no": 5,  
  "_primary_term": 67  
}  
```

### 步驟 4（選用）：擷取文件

若要擷取文件，請執行下列查詢：

```json
GET testindex1/_doc/1
```
{% include copy-curl.html %}

回應會包含已匯入的文件，其轉換結果如步驟 2 的回應所示。

## 處理物件陣列

下列請求會從 `products` 陣列中的每個物件移除 `internal_sku` 欄位：

```json
POST _ingest/pipeline/_simulate
{
  "pipeline": {
    "processors": [
      {
        "foreach": {
          "field": "products",
          "processor": {
            "remove": {
              "field": "_ingest._value.internal_sku"
            }
          }
        }
      }
    ]
  },
  "docs": [
    {
      "_source": {
        "order_id": "A-1001",
        "products": [
          { "name": "Wireless mouse", "price": 24.99, "internal_sku": "WM-4471" },
          { "name": "USB-C cable", "price": 9.99, "internal_sku": "UC-2210" }
        ]
      }
    }
  ]
}
```
{% include copy-curl.html %}

回應顯示 `internal_sku` 欄位已從兩個物件中移除：

```json
{
  "docs": [
    {
      "doc": {
        "_index": "_index",
        "_id": "_id",
        "_source": {
          "order_id": "A-1001",
          "products": [
            {
              "name": "Wireless mouse",
              "price": 24.99
            },
            {
              "name": "USB-C cable",
              "price": 9.99
            }
          ]
        },
        "_ingest": {
          "_value": null,
          "timestamp": "2026-10-14T19:40:29.753456004Z"
        }
      }
    }
  ]
}
```

## 處理陣列元素的失敗

如果內部處理器對某個元素失敗，且未定義 `on_failure`，則 `foreach` 處理器會停止處理該陣列並失敗。

若要處理個別元素的失敗，請在內部處理器中指定 `on_failure`。在下列請求中，`products` 陣列中的第二個物件不含 `internal_sku` 欄位，因此 `remove` 處理器對該元素失敗。`on_failure` 處理器會將文件傳送至 `failed-orders` 索引：

```json
POST _ingest/pipeline/_simulate
{
  "pipeline": {
    "processors": [
      {
        "foreach": {
          "field": "products",
          "processor": {
            "remove": {
              "field": "_ingest._value.internal_sku",
              "on_failure": [
                {
                  "set": {
                    "field": "_index",
                    "value": "failed-orders"
                  }
                }
              ]
            }
          }
        }
      }
    ]
  },
  "docs": [
    {
      "_index": "orders",
      "_source": {
        "order_id": "A-1002",
        "products": [
          { "name": "Wireless mouse", "price": 24.99, "internal_sku": "WM-4471" },
          { "name": "USB-C cable", "price": 9.99 }
        ]
      }
    }
  ]
}
```
{% include copy-curl.html %}

回應顯示目標索引已變更為 `failed-orders`。由於 `on_failure` 區塊處理了該失敗，`foreach` 處理器繼續處理其餘元素，且處理成功的元素會保留其變更：

```json
{
  "docs": [
    {
      "doc": {
        "_index": "failed-orders",
        "_id": "_id",
        "_source": {
          "order_id": "A-1002",
          "products": [
            {
              "name": "Wireless mouse",
              "price": 24.99
            },
            {
              "name": "USB-C cable",
              "price": 9.99
            }
          ]
        },
        "_ingest": {
          "_value": null,
          "timestamp": "2026-10-14T19:40:29.808936921Z"
        }
      }
    }
  ]
}
```
