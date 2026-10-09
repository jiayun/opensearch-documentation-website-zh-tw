---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "新增項目"
parent: Processors
grand_parent: Pipelines
nav_order: 10
---

# 新增項目處理器

`add_entries` 處理器會將項目新增至事件。

## 組態

您可以使用下列選項設定 `add_entries` 處理器。

| 選項 | 必要 | 說明 |
| :--- | :--- | :--- |
| `entries` | 是 | 要新增至事件的項目清單。 |
| `key` | 否 | 要新增之項目的鍵。鍵的範例包括 `my_key`、`myKey` 和 `object/sub_Key`。鍵也可以是格式運算式，例如使用 `${/key1}`，將欄位 `key1` 的值作為鍵。 |
| `metadata_key` | 否 | 新中繼資料屬性的鍵。引數必須是字串常值鍵，不能是 JSON Pointer。必須提供一個字串鍵或 `metadata_key`。 |
| `value` | 否 | 要新增之項目的值，可使用下列任一資料類型：字串、布林值、數字、null、巢狀物件和陣列。 |
| `format` | 否 | 作為新項目值的格式字串，例如 `${key1}-${key2}`，其中 `key1` 和 `key2` 是事件中既有的鍵。如果未指定 `value` 或 `value_expression`，則此選項為必要。 |
| `value_expression` | 否 | 作為新項目值的運算式字串。例如，`/key` 是事件中既有的鍵，其類型為數字、字串或布林值。運算式也可以包含傳回數字／字串／整數的函式。例如，當鍵為字串時，`length(/key)` 會傳回事件中該鍵的長度。如需鍵的詳細資訊，請參閱[運算式語法]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/expression-syntax/)。如需函式的詳細資訊，請參閱[函式]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/functions/)。 |
| `add_when` | 否 | 用於判斷是否對事件執行處理器的[條件運算式]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/expression-syntax/)，例如 `/some-key == "test"'`。 |
| `overwrite_if_key_exists` | 否 | 設為 `true` 時，若事件中已存在 `key`，則會覆寫現有值。預設值為 `false`。 |
| `append_if_key_exists` | 否 | 設為 `true` 時，若事件中已存在 `key`，則會將新值附加至現有值。若現有值不是陣列，則會建立陣列。預設值為 `false`。 |


## 使用方式

下列範例示範如何在不同情況下使用 `add_entries` 處理器。

### 範例：新增具有簡單值的項目

下列範例示範如何設定處理器，以新增具有簡單值的項目：

```yaml
... 
  processor:
    - add_entries:
        entries:
          - key: "name"
            value: "John"
          - key: "age"
            value: 20
...
```
{% include copy.html %}

當輸入事件包含下列資料時：

```json
{"message": "hello"}
```

處理後的事件將包含下列資料：

```json
{"message": "hello", "name": "John", "age": 20}
```

### 範例：使用格式字串新增項目

下列範例示範如何設定處理器，以新增值來自其他欄位的項目：

```yaml
... 
  processor:
    - add_entries:
        entries:
          - key: "date"
            format: "${month}-${day}"
...
```
{% include copy.html %}

當輸入事件包含下列資料時：

```json
{"month": "Dec", "day": 1}
```

處理後的事件將包含下列資料：

```json
{"month": "Dec", "day": 1, "date": "Dec-1"}
```

### 範例：使用值運算式新增項目

下列範例示範如何設定處理器，以使用 `value_expression` 選項：

```yaml
... 
  processor:
    - add_entries:
        entries:
          - key: "length"
            value_expression: "length(/message)"
...
```
{% include copy.html %}

當輸入事件包含下列資料時：

```json
{"message": "hello"}
```

處理後的事件將包含下列資料：

```json
{"message": "hello", "length": 5}
```

### 範例：新增中繼資料

下列範例示範如何設定處理器，以將中繼資料新增至事件：

```yaml
... 
  processor:
    - add_entries:
        entries:
          - metadata_key: "length"
            value_expression: "length(/message)"
...
```
{% include copy.html %}

當輸入事件包含下列資料時：

```json
{"message": "hello"}
```

處理後的事件將保有相同的資料，並附加中繼資料 `{"length": 5}`。您之後可以在管線中使用 `getMetadata("length")` 等運算式。如需詳細資訊，請參閱 [`getMetadata` 函式]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/get-metadata/)。


### 範例：新增動態鍵

下列範例示範如何設定處理器，以使用動態鍵將中繼資料新增至事件：

```yaml
... 
  processor:
    - add_entries:
        entries:
          - key: "${/param_name}"
            value_expression: "/param_value"
...
```
{% include copy.html %}

當輸入事件包含下列資料時：

```json
{"param_name": "cpu", "param_value": 50}
```

處理後的事件將包含下列資料：

```json
{"param_name": "cpu", "param_value": 50, "cpu": 50}
```

### 範例：覆寫現有項目

下列範例示範如何設定處理器，以覆寫現有項目：

```yaml
... 
  processor:
    - add_entries:
        entries:
          - key: "message"
            value: "bye"
            overwrite_if_key_exists: true
...
```
{% include copy.html %}

當輸入事件包含下列資料時：

```json
{"message": "hello"}
```

處理後的事件將包含下列資料：

```json
{"message": "bye"}
```

如果 `overwrite_if_key_exists` 未設為 `true`，則輸入事件在處理後不會變更。

### 範例：將值附加至現有項目

下列範例示範如何設定處理器，以將值附加至現有項目：

```yaml
... 
  processor:
    - add_entries:
        entries:
          - key: "message"
            value: "world"
            append_if_key_exists: true
...
```
{% include copy.html %}

當輸入事件包含下列資料時：

```json
{"message": "hello"}
```

處理後的事件將包含下列資料：

```json
{"message": ["hello", "world"]}
```

## 範例

下列管線會執行這些動作：

1. 使用格式字串 `${app}-${env}` 新增 `app_id` 欄位。
2. 新增 `message_len` 欄位，其值為 `length(/message)`。
3. 新增中繼資料鍵 `msg_len_meta`，其值為 `length(/message)`。
4. 如果 `/metric/name` 和 `/metric/value` 都存在，則建立以 `/metric/name` 命名的新欄位，並將其值設為 `/metric/value`。
5. 如果 `/level == "error"`，則新增欄位 `severity: "high"`。
6. 將 `"ingested"` 附加至 `tags` 欄位，確保 `tags` 欄位為陣列。
7. 設定 `env_normalized: "prod"`，如果欄位已存在，則覆寫現有值。

```yaml
example-pipeline:
  source:
    http:
      path: /events
      ssl: false

  processor:
    - add_entries:
        entries:
          - key: app_id
            format: ${app}-${env}

          - key: message_len
            value_expression: length(/message)

          - metadata_key: msg_len_meta
            value_expression: length(/message)

          # dynamic key from the event, only when both metric fields exist
          - key: ${/metric/name}
            value_expression: /metric/value
            add_when: "/metric/name != null and /metric/value != null"

          # set severity ONLY on error level
          - key: severity
            value: high
            add_when: '/level == "error"'

          # append behavior: if tags already exists, it becomes/extends an array
          - key: tags
            value: ingested
            append_if_key_exists: true

          # overwrite behavior
          - key: env_normalized
            value: prod
            overwrite_if_key_exists: true

  sink:
    - opensearch:
        hosts: [https://opensearch:9200]
        insecure: true
        username: admin
        password: admin_password
        index_type: custom
        index: example-%{yyyy.MM.dd}
```
{% include copy.html %}

您可以執行下列命令來測試此管線：

```bash
curl -sS -X POST "http://localhost:2021/events" \
  -H "Content-Type: application/json" \
  -d '[
        {"app":"shop","env":"dev","message":"hello","level":"info","metric":{"name":"cpu","value":42}},
        {"app":"shop","env":"prod","message":"boom","level":"error"},
        {"app":"api","env":"stage","message":"hi","level":"warn","metric":{"name":"mem","value":2048},"tags":"pretag"}
      ]'
```
{% include copy.html %}

儲存在 OpenSearch 中的文件包含下列資訊：

```json
"hits": [
  {
    "_index": "example-2025.10.10",
    "_id": "BnvWzpkBTMZ443JmHuHI",
    "_score": 1,
    "_source": {
      "app": "shop",
      "env": "dev",
      "message": "hello",
      "level": "info",
      "metric": {
        "name": "cpu",
        "value": 42
      },
      "app_id": "shop-dev",
      "message_len": 5,
      "cpu": 42,
      "tags": "ingested",
      "env_normalized": "prod"
    }
  },
  {
    "_index": "example-2025.10.10",
    "_id": "B3vWzpkBTMZ443JmHuHI",
    "_score": 1,
    "_source": {
      "app": "shop",
      "env": "prod",
      "message": "boom",
      "level": "error",
      "app_id": "shop-prod",
      "message_len": 4,
      "severity": "high",
      "tags": "ingested",
      "env_normalized": "prod"
    }
  },
  {
    "_index": "example-2025.10.10",
    "_id": "CHvWzpkBTMZ443JmHuHI",
    "_score": 1,
    "_source": {
      "app": "api",
      "env": "stage",
      "message": "hi",
      "level": "warn",
      "metric": {
        "name": "mem",
        "value": 2048
      },
      "tags": [
        "pretag",
        "ingested"
      ],
      "app_id": "api-stage",
      "message_len": 2,
      "mem": 2048,
      "env_normalized": "prod"
    }
  }
]

```
