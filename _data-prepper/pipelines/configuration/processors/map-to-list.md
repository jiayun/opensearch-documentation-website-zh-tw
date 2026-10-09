---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "對應至清單"
parent: Processors
grand_parent: Pipelines
nav_order: 200
---

# Map to list 處理器

`map_to_list` 處理器會將鍵值對的 map 轉換為物件清單。每個物件會在個別欄位中包含鍵與值。

## 組態

下表說明 `map_to_list` 處理器的組態選項。

選項 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`source` | 是 | String | 用於執行對應作業的來源 map。設為空字串 (`""`) 時，會使用事件的根作為 `source`。
`target` | 是 | String | 產生的清單的目標。
`key_name` | 否 | String | 用來儲存原始鍵的欄位名稱。預設為 `key`。
`value_name` | 否 | String | 用來儲存原始值的欄位名稱。預設為 `value`。
`exclude_keys` | 否 | List | 來源 map 中將排除處理的鍵。預設為空清單 (`[]`)。
`remove_processed_fields` | 否 | Boolean | 當 `true` 時，處理器會從來源 map 移除已處理的欄位。預設為 `false`。
`convert_field_to_list` | 否 | Boolean | 若為 `true`，處理器會將來源 map 中的欄位轉換為清單，並將其放置在目標清單的欄位中。預設為 `false`。
`map_to_list_when` | 否 | String | 一個[條件運算式]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/expression-syntax/)，例如 `/some-key == "test"'`，會評估以判斷處理器是否要在該事件上執行。預設為 `null`。除非另有說明，否則會處理所有事件。
`tags_on_failure` | 否 | List | 當事件處理失敗時，要新增至事件中繼資料的標籤清單。

## 使用方式

下列範例顯示如何在您的管線中使用 `map_to_list` 處理器。

### 範例：最小組態

下列範例顯示僅設定必要參數 `source` 與 `target` 的 `map_to_list` 處理器：

```yaml
...
  processor:
    - map_to_list:
        source: "my-map"
        target: "my-list"
...
```
{% include copy.html %}

當輸入事件包含下列資料時：

```json
{
  "my-map": {
    "key1": "value1",
    "key2": "value2",
    "key3": "value3"
  }
}
```


處理後的事件會包含下列輸出：

```json
{
  "my-list": [
    {
      "key": "key1",
      "value": "value1"
    },
    {
      "key": "key2",
      "value": "value2"
    },
    {
      "key": "key3",
      "value": "value3"
    }
  ],
  "my-map": {
    "key1": "value1",
    "key2": "value2",
    "key3": "value3"
  }
}
```

### 範例：自訂鍵名稱與值名稱

下列範例顯示如何設定自訂鍵名稱與值名稱：

```yaml
...
  processor:
    - map_to_list:
        source: "my-map"
        target: "my-list"
        key_name: "name"
        value_name: "data"
...
```
{% include copy.html %}

當輸入事件包含下列資料時：

```json
{
  "my-map": {
    "key1": "value1",
    "key2": "value2",
    "key3": "value3"
  }
}
```

處理後的事件會包含下列輸出：

```json
{
  "my-list": [
    {
      "name": "key1",
      "data": "value1"
    },
    {
      "name": "key2",
      "data": "value2"
    },
    {
      "name": "key3",
      "data": "value3"
    }
  ],
  "my-map": {
    "key1": "value1",
    "key2": "value2",
    "key3": "value3"
  }
}
```

### 範例：排除特定鍵不處理並移除任何已處理的欄位

下列範例顯示如何排除特定鍵並從輸出中移除任何已處理的欄位：

```yaml
...
  processor:
    - map_to_list:
        source: "my-map"
        target: "my-list"
        exclude_keys: ["key1"]
        remove_processed_fields: true
...
```
{% include copy.html %}

當輸入事件包含下列資料時：
```json
{
  "my-map": {
    "key1": "value1",
    "key2": "value2",
    "key3": "value3"
  }
}
```

處理後的事件會移除 "key2" 與 "key3" 欄位，但 "my-map" 物件、"key1" 會保留，如下列輸出所示：

```json
{
  "my-list": [
    {
      "key": "key2",
      "value": "value2"
    },
    {
      "key": "key3",
      "value": "value3"
    }
  ],
  "my-map": {
    "key1": "value1"
  }
}
```

### 範例：使用 convert_field_to_list

下列範例顯示如何在處理器中使用 `convert_field_to_list` 選項：

```yaml
...
  processor:
    - map_to_list:
        source: "my-map"
        target: "my-list"
        convert_field_to_list: true
...
```
{% include copy.html %}

當輸入事件包含下列資料時：

```json
{
  "my-map": {
    "key1": "value1",
    "key2": "value2",
    "key3": "value3"
  }
}
```

處理後的事件會將所有欄位轉換為清單，如下列輸出所示：

```json
{
  "my-list": [
    ["key1", "value1"],
    ["key2", "value2"],
    ["key3", "value3"]
  ],
  "my-map": {
    "key1": "value1",
    "key2": "value2",
    "key3": "value3"
  }
}
```

### 範例：使用事件根作為來源

下列範例顯示如何將 `source` 設定設為空字串 (`""`)，以使用事件的根作為來源：

```yaml
...
  processor:
    - map_to_list:
        source: ""
        target: "my-list"
...
```
{% include copy.html %}

當輸入事件包含下列資料時：

```json
{
  "key1": "value1",
  "key2": "value2",
  "key3": "value3"
}
```

處理後的事件會包含下列輸出：

```json
{
  "my-list": [
    {
      "key": "key1",
      "value": "value1"
    },
    {
      "key": "key2",
      "value": "value2"
    },
    {
      "key": "key3",
      "value": "value3"
    }
  ],
  "key1": "value1",
  "key2": "value2",
  "key3": "value3"
}
```
