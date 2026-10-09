---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "清單轉對應"
parent: Processors
grand_parent: Pipelines
nav_order: 180
---

# List to map 處理器

`list_to_map` 處理器會將事件中的物件清單轉換為目標鍵的對應，其中每個物件都包含 `key` 欄位。

## 組態

下表說明用於為對應產生目標鍵的組態選項。

選項 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`source` | 是 | 字串 | 含有 `key` 欄位、要轉換為所產生對應之鍵的物件清單。
`target` | 否 | 字串 | 所產生對應的目標。未指定時，所產生的對應會放置在根節點中。
`key` | 有條件 | 字串 | 要擷取為所產生對應中之鍵的欄位鍵。當 `use_source_key` 為 `false` 時必須指定。
`use_source_key` | 否 | 布林值 | 當 `true` 時，所產生對應中的鍵會使用來源的原始鍵。預設為 `false`。
`value_key` | 否 | 字串 | 指定時，來源清單所含物件中具有 `value_key` 的值會被擷取，並根據所產生的對應轉換為此選項指定的值。未指定時，來源清單所含的物件在對應時會保留其原始值。
`extract_value` | 否 | 布林值 | 當 `true` 時，會擷取來源清單的物件值並加入所產生的對應。當 `false` 時，來源清單的物件值會依其在來源清單中的順序加入所產生的對應。預設為 `false`
`flatten` | 否 | 布林值 | 當 `true` 時，所產生對應輸出中的值會根據 `flattened_element` 扁平化為單一項目。否則，對應至所產生對應中值的物件會以清單形式呈現。
`flattened_element` | 有條件 | 字串 | 當 `flatten` 設為 `true` 時要保留的元素，可為 `first` 或 `last`。

## 使用方式

下列範例說明如何在您自己的來源上使用 `list_to_map` 處理器之前，先測試其使用方式。

建立名為 `logs_json.log` 的來源檔案。由於 `file` 來源會將 `.log` 檔案中的每一行讀取為一個事件，因此物件清單即使包含多個物件，仍會顯示為一行：

```json
{"mylist":[{"name":"a","value":"val-a"},{"name":"b","value":"val-b1"},{"name":"b",  "value":"val-b2"},{"name":"c","value":"val-c"}]}
```
{% include copy.html %}

接著，建立一個 `pipeline.yaml` 檔案，將 `logs_json.log` 檔案用作 `source`，並指向 `.log` 檔案的正確路徑：

```yaml
pipeline:
  source:
    file:
      path: "/full/path/to/logs_json.log"
      record_type: "event"
      format: "json"
  processor:
    - list_to_map:
        key: "name"
        source: "mylist"
        value_key: "value"
        flatten: true
  sink:
    - stdout:
```
{% include copy.html %}

執行管線。若成功，處理器會傳回所產生的對應，其中的物件會依其 `value_key` 進行對應。與原始來源類似，原始來源只包含一行，因此只有一個事件，處理器會傳回下列 JSON 作為一行。為方便閱讀，下列範例及後續所有 JSON 範例均已調整為跨越多行：

```json
{
  "mylist": [
    {
      "name": "a",
      "value": "val-a"
    },
    {
      "name": "b",
      "value": "val-b1"
    },
    {
      "name": "b",
      "value": "val-b2"
    },
    {
      "name": "c",
      "value": "val-c"
    }
  ],
  "a": "val-a",
  "b": "val-b1",
  "c": "val-c"
}
```

### 範例：對應設為 `target`

下列範例 `pipeline.yaml` 檔案顯示 `list_to_map` 處理器設為指定目標 `mymap` 時的情形：

```yaml
pipeline:
  source:
    file:
      path: "/full/path/to/logs_json.log"
      record_type: "event"
      format: "json"
  processor:
    - list_to_map:
        key: "name"
        source: "mylist"
        target: "mymap"
        value_key: "value"
        flatten: true
  sink:
    - stdout:
```
{% include copy.html %}

所產生的對應會顯示在目標鍵之下：

```json
{
  "mylist": [
    {
      "name": "a",
      "value": "val-a"
    },
    {
      "name": "b",
      "value": "val-b1"
    },
    {
      "name": "b",
      "value": "val-b2"
    },
    {
      "name": "c",
      "value": "val-c"
    }
  ],
  "mymap": {
    "a": "val-a",
    "b": "val-b1",
    "c": "val-c"
  }
}
```

### 範例：未指定 `value_key`

下列範例 `pipeline.yaml` 檔案顯示未指定 `value_key` 的 `list_to_map` 處理器。由於 `key` 設為 `name`，處理器會擷取物件名稱以用作對應中的鍵。

```yaml
pipeline:
  source:
    file:
      path: "/full/path/to/logs_json.log"
      record_type: "event"
      format: "json"
  processor:
    - list_to_map:
        key: "name"
        source: "mylist"
        flatten: true
  sink:
    - stdout:
```
{% include copy.html %}

所產生對應中的值會以 `.log` 來源的原始物件形式呈現，如下列範例回應所示：

```json
{
  "mylist": [
    {
      "name": "a",
      "value": "val-a"
    },
    {
      "name": "b",
      "value": "val-b1"
    },
    {
      "name": "b",
      "value": "val-b2"
    },
    {
      "name": "c",
      "value": "val-c"
    }
  ],
  "a": {
    "name": "a",
    "value": "val-a"
  },
  "b": {
    "name": "b",
    "value": "val-b1"
  },
  "c": {
    "name": "c",
    "value": "val-c"
  }
}
```

### 範例：`flattened_element` 設為 `last`

下列範例 `pipeline.yaml` 檔案將 `flattened_element` 設為 last，因此會根據每個值的最後一個元素，將處理器輸出扁平化：

```yaml
pipeline:
  source:
    file:
      path: "/full/path/to/logs_json.log"
      record_type: "event"
      format: "json"
  processor:
    - list_to_map:
        key: "name"
        source: "mylist"
        target: "mymap"
        value_key: "value"
        flatten: true
        flattened_element: "last"
  sink:
    - stdout:
```
{% include copy.html %}

處理器會將物件 `b` 對應至值 `val-b2`，因為 `val-b2` 是物件 `b` 中的最後一個元素，如下列輸出所示：

```json
{
  "mylist": [
    {
      "name": "a",
      "value": "val-a"
    },
    {
      "name": "b",
      "value": "val-b1"
    },
    {
      "name": "b",
      "value": "val-b2"
    },
    {
      "name": "c",
      "value": "val-c"
    }
  ],
  "a": "val-a",
  "b": "val-b2",
  "c": "val-c"
}
```


### 範例：`flatten` 設為 false

下列範例 `pipeline.yaml` 檔案將 `flatten` 設為 `false`，使處理器將所產生對應中的值以清單形式輸出：

```yaml
pipeline:
  source:
    file:
      path: "/full/path/to/logs_json.log"
      record_type: "event"
      format: "json"
  processor:
    - list_to_map:
        key: "name"
        source: "mylist"
        target: "mymap"
        value_key: "value"
        flatten: false
  sink:
    - stdout:
```
{% include copy.html %}

回應中的部分物件，其值可能包含多個元素，如下列回應所示：

```json
{
  "mylist": [
    {
      "name": "a",
      "value": "val-a"
    },
    {
      "name": "b",
      "value": "val-b1"
    },
    {
      "name": "b",
      "value": "val-b2"
    },
    {
      "name": "c",
      "value": "val-c"
    }
  ],
  "a": [
    "val-a"
  ],
  "b": [
    "val-b1",
    "val-b2"
  ],
  "c": [
    "val-c"
  ]
}
```

### 範例：`use_source_key` 與 `extract_value` 設為 `true`

下列範例 `pipeline.yaml` 檔案將 `flatten` 設為 `false`，使處理器將所產生對應中的值以清單形式輸出：

```yaml
pipeline:
  source:
    file:
      path: "/full/path/to/logs_json.log"
      record_type: "event"
      format: "json"
  processor:
    - list_to_map:
        source: "mylist"
        use_source_key: true
        extract_value: true
  sink:
    - stdout:
```
{% include copy.html %}

來自 `mylist` 的物件值會被擷取，並加入具有來源鍵 `name` 與 `value` 的欄位，如下列回應所示：

```json
{
  "mylist": [
    {
      "name": "a",
      "value": "val-a"
    },
    {
      "name": "b",
      "value": "val-b1"
    },
    {
      "name": "b",
      "value": "val-b2"
    },
    {
      "name": "c",
      "value": "val-c"
    }
  ],
  "name": ["a", "b", "b", "c"],
  "value": ["val-a", "val-b1", "val-b2", "val-c"]
}
```