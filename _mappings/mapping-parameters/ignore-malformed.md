---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "忽略格式錯誤"
parent: Mapping parameters
redirect_from:
  - /field-types/mapping-parameters/ignore-malformed/
nav_order: 130
has_children: false
has_toc: false
---

# 忽略格式錯誤的對應參數

`ignore_malformed` 對應參數會指示索引引擎忽略不符合欄位預期格式的值。啟用後，格式錯誤的值不會被編製索引，避免因為資料格式問題而拒絕整份文件。這可確保即使一或多個欄位包含無法剖析的資料，文件仍會被儲存。

根據預設，`ignore_malformed` 為停用狀態，這表示若某個值無法依據欄位類型剖析，整份文件的索引作業將會失敗。

## 範例：ignore_malformed 關閉

建立一個名為 `people_no_ignore` 的索引，其中包含類型為 `integer` 的 `age` 欄位。根據預設，`ignore_malformed` 設為 `false`：

```json
PUT /people_no_ignore
{
  "mappings": {
    "properties": {
      "age": {
        "type": "integer"
      }
    }
  }
}
```
{% include copy-curl.html %}

將含有格式錯誤值的文件編製索引：

```json
PUT /people_no_ignore/_doc/1
{
  "age": "twenty"
}
```
{% include copy-curl.html %}

由於該值格式錯誤，請求失敗：

```json
{
  "error": {
    "root_cause": [
      {
        "type": "mapper_parsing_exception",
        "reason": "failed to parse field [age] of type [integer] in document with id '1'. Preview of field's value: 'twenty'"
      }
    ],
    "type": "mapper_parsing_exception",
    "reason": "failed to parse field [age] of type [integer] in document with id '1'. Preview of field's value: 'twenty'",
    "caused_by": {
      "type": "number_format_exception",
      "reason": "For input string: \"twenty\""
    }
  },
  "status": 400
}
```

## 範例：ignore_malformed 開啟

建立一個名為 `people_ignore` 的索引，其中 `age` 欄位的 `ignore_malformed` 設為 `true`：

```json
PUT /people_ignore
{
  "mappings": {
    "properties": {
      "age": {
        "type": "integer",
        "ignore_malformed": true
      }
    }
  }
}
```
{% include copy-curl.html %}

將含有格式錯誤值的文件編製索引：

```json
PUT /people_ignore/_doc/1
{
  "age": "twenty"
}
```
{% include copy-curl.html %}

擷取該文件：

```json
GET /people_ignore/_doc/1
```
{% include copy-curl.html %}

回應顯示，儘管該值格式錯誤，文件仍已成功編製索引：

```json
{
  "_index": "people_ignore",
  "_id": "1",
  "_version": 1,
  "_seq_no": 0,
  "_primary_term": 1,
  "found": true,
  "_source": {
    "age": "twenty"
  }
}
```


