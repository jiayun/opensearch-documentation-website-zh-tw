---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "啟用"
parent: Mapping parameters
redirect_from:
  - /field-types/mapping-parameters/enabled/
nav_order: 40
has_children: false
has_toc: false
---

# 啟用對應參數

OpenSearch 會嘗試將您提供的所有欄位編製索引，但有時您可能想要儲存某個欄位而不使其可供搜尋。舉例來說，如果您使用 OpenSearch 作為網站工作階段儲存區，您可能會將工作階段 ID 和上次更新時間編製索引，但儲存工作階段資料本身而不將其編製索引，因為您不需要搜尋或彙總這些資料。

將 `enabled` 參數設為 `false` 會讓 OpenSearch 完全略過剖析欄位內容。OpenSearch 仍會將欄位的值儲存在 `_source` 欄位中，但不會將其內容編製索引或剖析，因此該欄位無法搜尋。此參數只能套用於最上層的對應定義和物件欄位。

`enabled` 參數接受下列值。

參數 | 說明
:--- | :---
`true` (預設) | 欄位會被剖析並編製索引。
`false` | 欄位不會被剖析或編製索引，但仍可從 `_source` 欄位擷取。

現有欄位和最上層對應定義的 `enabled` 參數無法更新。
{: .warning}

## 停用物件欄位

建立一個含有已停用 `session_data` 物件欄位的索引。OpenSearch 會將其內容儲存在 `_source` 欄位中，但不會將其編製索引或剖析：

```json
PUT /session_store
{
  "mappings": {
    "properties": {
      "user_id": {
        "type": "keyword"
      },
      "last_updated": {
        "type": "date"
      },
      "session_data": {
        "type": "object",
        "enabled": false
      }
    }
  }
}
```
{% include copy-curl.html %}

在已停用的欄位中，為含有不同類型資料的文件編製索引：

```json
PUT /session_store/_doc/session_1
{
  "user_id": "johndoe",
  "session_data": {
    "user_preferences": {
      "theme_settings": ["dark_mode", "compact_layout", {"font_size": 14}]
    }
  },
  "last_updated": "2025-02-10T07:10:53"
}
```
{% include copy-curl.html %}

```json
PUT /session_store/_doc/session_2
{
  "user_id": "janedoe",
  "session_data": "none",
  "last_updated": "2025-02-10T07:12:48"
}
```
{% include copy-curl.html %}

`session_data` 欄位可接受任何任意資料，因為 OpenSearch 會完全略過剖析其內容。物件和非物件資料皆可接受。

## 停用整個對應

停用整個對應，以儲存文件而不將任何欄位編製索引：

```json
PUT /raw_storage
{
  "mappings": {
    "enabled": false
  }
}
```
{% include copy-curl.html %}

在已停用的對應中為文件編製索引：

```json
PUT /raw_storage/_doc/doc_1
{
  "user_id": "janedoe",
  "session_data": {
    "user_preferences": {
      "theme_settings": ["dark_mode", "compact_layout", {"font_size": 14}]
    }
  },
  "last_updated": "2025-12-10T07:10:53"
}
```
{% include copy-curl.html %}

若要確認文件已儲存，請擷取該文件：

```json
GET /raw_storage/_doc/doc_1
```
{% include copy-curl.html %}

回應顯示文件已成功儲存，且可從 `_source` 欄位擷取：

```json
{
  "_index": "raw_storage",
  "_id": "doc_1",
  "_version": 1,
  "_seq_no": 0,
  "_primary_term": 1,
  "found": true,
  "_source": {
    "user_id": "janedoe",
    "session_data": {
      "user_preferences": {
        "theme_settings": [
          "dark_mode",
          "compact_layout",
          {
            "font_size": 14
          }
        ]
      }
    },
    "last_updated": "2025-12-10T07:10:53"
  }
}
```

確認對應，以驗證未新增任何欄位：

```json
GET /raw_storage/_mapping
```
{% include copy-curl.html %}

文件可從 `_source` 擷取，但其內容皆未編製索引，因此對應中不會出現任何欄位，且該文件無法搜尋：

```json
{
  "raw_storage": {
    "mappings": {
      "enabled": false
    }
  }
}
```
