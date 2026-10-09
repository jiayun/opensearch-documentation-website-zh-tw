---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "格式"
parent: Mapping parameters
redirect_from:
  - /field-types/mapping-parameters/format/
nav_order: 110
has_children: false
has_toc: false
---

# Format 對應參數

`format` 對應參數會指定日期欄位在編製索引期間可接受的[內建日期格式]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/date/#built-in-formats)。透過定義預期的日期格式，您可確保日期值正確剖析並儲存，以利進行精確的搜尋與彙總作業。

## 範例：定義自訂日期格式

建立 `events` 索引，並將 `event_date` 欄位設定為自訂的 `yyyy-MM-dd HH:mm:ss` 日期格式：

```json
PUT events
{
  "mappings": {
    "properties": {
      "event_date": {
        "type": "date",
        "format": "yyyy-MM-dd HH:mm:ss"
      }
    }
  }
}
```
{% include copy-curl.html %}

使用指定的格式為 `event_date` 欄位編製文件索引：

```json
PUT events/_doc/1
{
  "event_name": "Conference",
  "event_date": "2025-03-26 15:30:00"
}
```
{% include copy-curl.html %}

## 範例：使用多種日期格式

建立包含 `log_timestamp` 欄位的索引，該欄位同時接受自訂的 `yyyy-MM-dd HH:mm:ss` 日期格式與 `epoch_millis` 格式：

```json
PUT logs
{
  "mappings": {
    "properties": {
      "log_timestamp": {
        "type": "date",
        "format": "yyyy-MM-dd HH:mm:ss||epoch_millis"
      }
    }
  }
}
```
{% include copy-curl.html %}

使用自訂格式為第一份文件編製索引：

```json
PUT logs/_doc/1
{
  "message": "System rebooted",
  "log_timestamp": "2025-03-26 08:45:00"
}
```
{% include copy-curl.html %}

使用毫秒格式為第二份文件編製索引：

```json
PUT logs/_doc/2
{
  "message": "System updated",
  "log_timestamp": 1711442700000
}
```
{% include copy-curl.html %}

## 內建日期格式

如需完整的內建日期格式清單，請參閱[內建格式]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/date/#built-in-formats)。