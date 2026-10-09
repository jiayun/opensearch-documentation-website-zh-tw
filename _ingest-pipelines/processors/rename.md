---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "重新命名"
parent: Ingest processors
nav_order: 227
redirect_from:
   - /api-reference/ingest-apis/processors/rename/
---

# Rename 處理器

`rename` 處理器用於重新命名現有的欄位，也可以用來將欄位從一個物件移動到另一個物件或根層級。

## 語法

以下是 `rename` 處理器的語法：

```json
{
    "rename": {
        "field": "field_name",
        "target_field" : "target_field_name"
    }
}
```
{% include copy.html %}

## 組態參數

下表列出 `rename` 處理器的必要與選用參數。

參數  | 必要／選用  | 說明  |
---|---|---|
`field`  | 必要  | 包含要移除之資料的欄位名稱。支援[範本片段]({{site.url}}{{site.baseurl}}/ingest-pipelines/create-ingest/#template-snippets)。 |
`target_field`  | 必要  | 欄位的新名稱。支援[範本片段]({{site.url}}{{site.baseurl}}/ingest-pipelines/create-ingest/#template-snippets)。 |
`ignore_missing`  | 選用  | 指定處理器是否應忽略不含指定 `field` 的文件。若設為 `true`，當 `field` 不存在時，處理器不會修改文件。預設為 `false`。 |
`override_target`  | 選用  | 決定當文件中已存在 `target_field` 時的處理方式。若設為 `true`，處理器會以新值覆寫現有的 `target_field` 值。若設為 `false`，則保留現有值，處理器不會覆寫。預設為 `false`。 |
`description`  | 選用  | 處理器的簡短描述。  |
`if` | 選用 | 執行處理器的條件。 |
`ignore_failure` | 選用 | 指定處理器即使遇到錯誤也繼續執行。若設為 `true`，則會忽略失敗。預設為 `false`。 |
`on_failure` | 選用 | 當處理器失敗時要執行的處理器清單。 |
`tag` | 選用 | 處理器的識別標籤。有助於除錯時區分相同類型的處理器。 |

## 使用處理器

依照下列步驟在管線中使用處理器。

**步驟 1：建立管線**

下列查詢會建立名為 `rename_field` 的管線，將物件中的欄位移動到根層級：

```json
PUT /_ingest/pipeline/rename_field
{
  "description": "Pipeline that moves a field to the root level.",
  "processors": [
    {
      "rename": {
        "field": "message.content",
        "target_field": "content"
      }
    }
  ]
}
```
{% include copy-curl.html %}

**步驟 2 (選用)：測試管線**

建議您在匯入文件之前先測試管線。
{: .tip}

若要測試管線，請執行下列查詢：

```json
POST _ingest/pipeline/rename_field/_simulate
{
  "docs": [
    {
      "_index": "testindex1",
      "_id": "1",
      "_source":{
         "message": {
           "type": "nginx",
           "content": "192.168.1.10 - - [03/Nov/2023:15:20:45 +0000] \"POST /login HTTP/1.1\" 200 3456"
         }
      }
    }
  ]
}
```
{% include copy-curl.html %}

**回應**

下列範例回應確認管線如預期運作：

```json
{
  "docs": [
    {
      "doc": {
        "_index": "testindex1",
        "_id": "1",
        "_source": {
          "message": {
            "type": "nginx",
          },
          "content": """192.168.1.10 - - [03/Nov/2023:15:20:45 +0000] "POST /login HTTP/1.1" 200 3456"""
        },
        "_ingest": {
          "timestamp": "2024-04-15T07:54:16.010447Z"
        }
      }
    }
  ]
}
```

**步驟 3：匯入文件**

下列查詢會將文件匯入名為 `testindex1` 的索引：

```json
PUT testindex1/_doc/1?pipeline=rename_field
{
  "message": {
    "type": "nginx",
    "content": "192.168.1.10 - - [03/Nov/2023:15:20:45 +0000] \"POST /login HTTP/1.1\" 200 3456"
  }
}
```
{% include copy-curl.html %}

**步驟 4 (選用)：擷取文件**

若要擷取文件，請執行下列查詢：

```json
GET testindex1/_doc/1
```
{% include copy-curl.html %}
