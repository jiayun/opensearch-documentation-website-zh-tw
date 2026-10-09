---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "依模式移除"
parent: Ingest processors
nav_order: 225
redirect_from:
   - /ingest-pipelines/processors/remove_by_pattern/
---

# 依模式移除處理器

`remove_by_pattern` 處理器會使用指定的萬用字元模式，從文件中移除根層級的欄位。

## 語法

以下是 `remove_by_pattern` 處理器的語法：

```json
{
    "remove_by_pattern": {
        "field_pattern": "field_name_prefix*"
    }
}
```
{% include copy.html %}

## 組態參數

下表列出 `remove_by_pattern` 處理器的必要與選用參數。

| 參數  | 必要/選用  | 說明  |
|---|---|---|
`field_pattern`  | 選用  | 移除符合指定模式的欄位。所有中繼資料欄位（例如 `_index`、`_version`、`_version_type` 和 `_id`）即使符合模式也會被忽略。此選項僅支援文件中的根層級欄位。 |
`exclude_field_pattern`  | 選用  | 移除不符合指定模式的欄位。所有中繼資料欄位（例如 `_index`、`_version`、`_version_type` 和 `_id`）即使不符合模式也會被忽略。此選項僅支援文件中的根層級欄位。`field_pattern` 與 `exclude_field_pattern` 選項互斥。 |
`description`  | 選用  | 處理器的簡要說明。  |
`if` | 選用 | 執行處理器的條件。 |
`ignore_failure` | 選用 | 指定處理器即使遇到錯誤仍繼續執行。若設定為 `true`，則會忽略失敗。預設為 `false`。 |
`on_failure` | 選用 | 處理器失敗時要執行的處理器清單。 |
`tag` | 選用 | 處理器的識別標籤。有助於除錯時區分相同類型的處理器。 |

## 使用處理器

依照下列步驟在管線中使用處理器。

**步驟 1：建立管線**

下列查詢會建立名為 `remove_fields_by_pattern` 的管線，移除符合模式 `foo*` 的欄位：

```json
PUT /_ingest/pipeline/remove_fields_by_pattern
{
  "description": "Pipeline that removes the fields by patterns.",
  "processors": [
    {
      "remove_by_pattern": {
        "field_pattern": "foo*"
      }
    }
  ]
}
```
{% include copy-curl.html %}

**步驟 2（選用）：測試管線**

建議您在匯入文件之前先測試管線。
{: .tip}

若要測試管線，請執行下列查詢：

```json
POST _ingest/pipeline/remove_fields_by_pattern/_simulate
{
  "docs": [
    {
      "_index": "testindex1",
      "_id": "1",
      "_source":{
         "foo1": "foo1",
         "foo2": "foo2",
         "bar": "bar"
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
          "bar": "bar"
        },
        "_ingest": {
          "timestamp": "2023-08-24T18:02:13.218986756Z"
        }
      }
    }
  ]
}
```

**步驟 3：匯入文件**

下列查詢會將文件匯入名為 `testindex1` 的索引：

```json
PUT testindex1/_doc/1?pipeline=remove_fields_by_pattern
{
  "foo1": "foo1",
  "foo2": "foo2",
  "bar": "bar"
}
```
{% include copy-curl.html %}

**步驟 4（選用）：擷取文件**

若要擷取文件，請執行下列查詢：

```json
GET testindex1/_doc/1
```
{% include copy-curl.html %}
