---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "鍵值"
parent: Processors
grand_parent: Pipelines
nav_order: 170
---

# Key-value 處理器


您可以使用 `key_value` 處理器將指定的欄位解析為鍵值對。您可以使用下列選項自訂 `key_value` 處理器，以解析欄位資訊。下列每個選項的類型皆為 `string`。

## 範例

下列範例展示可與此處理器搭配使用的數種組態。

這些範例未使用安全性功能，僅供示範之用。我們強烈建議在正式環境中使用這些範例之前，先設定 SSL。
{: .warning}

### 鍵值解析、正規化與去重

下列範例將 `message` 欄位解析為 `key=value` 鍵值對，正規化並清理鍵、為鍵加上 `meta_` 前綴、去除重複的值，捨棄沒有值的鍵，並將解析結果寫入 `parsed_kv`：

```yaml
kv-basic-pipeline:
  source:
    http:
      path: /logs
      ssl: false

  processor:
    - key_value:
        # Read key=value pairs from the "message" field (default anyway)
        source: message
        # Write parsed pairs into a nested object "parsed_kv"
        destination: parsed_kv

        # Split pairs on '&' and split key vs value on '='
        field_split_characters: "&"
        value_split_characters: "="

        # Normalize keys and trim garbage whitespace around keys/values
        transform_key: lowercase
        delete_key_regex: "\\s+"          # remove spaces from keys
        delete_value_regex: "^\\s+|\\s+$" # trim leading/trailing spaces

        # Add a prefix to every key (after normalization + delete_key_regex)
        prefix: meta_

        # Keep a single unique value for duplicate keys
        skip_duplicate_values: true

        # Drop keys whose value is empty/absent (e.g., `empty=` or `novalue`)
        drop_keys_with_no_value: true

  sink:
    - opensearch:
        hosts: ["https://opensearch:9200"]
        insecure: true
        username: admin
        password: admin_password
        index_type: custom
        index: kv-basic-%{yyyy.MM.dd}
```
{% include copy.html %}

您可以使用下列命令測試此管線：

```bash
curl -sS -X POST "http://localhost:2021/logs" \
  -H "Content-Type: application/json" \
  -d '[
    {"message":"key1=value1&key1=value1&Key Two = value two & empty=&novalue"},
    {"message":"ENV = prod & TEAM = core & owner = alice "}
  ]'
```
{% include copy.html %}

儲存在 OpenSearch 中的文件包含下列資訊：

```json
{
  ...
  "hits": {
    "total": {
      "value": 2,
      "relation": "eq"
    },
    "max_score": 1,
    "hits": [
      {
        "_index": "kv-basic-2025.10.14",
        "_id": "M6d84pkB3P3jd6EROH_f",
        "_score": 1,
        "_source": {
          "message": "key1=value1&key1=value1&Key Two = value two & empty=&novalue",
          "parsed_kv": {
            "meta_key1": "value1",
            "meta_empty": "",
            "meta_keytwo": "value two"
          }
        }
      },
      {
        "_index": "kv-basic-2025.10.14",
        "_id": "NKd84pkB3P3jd6EROH_f",
        "_score": 1,
        "_source": {
          "message": "ENV = prod & TEAM = core & owner = alice ",
          "parsed_kv": {
            "meta_owner": "alice",
            "meta_team": "core",
            "meta_env": "prod"
          }
        }
      }
    ]
  }
}
```

### 分組值寫入根層級

下列範例使用 `&&` 分隔鍵值對、使用 `==` 分隔鍵與值，藉此解析 `payload` 欄位。它會將括號內的分組保留為單一值、將解析結果寫入事件根層級而不覆寫現有欄位，並將任何未比對到的詞元記錄為 `null`：

```yaml
kv-grouping-pipeline:
  source:
    http:
      path: /logs
      ssl: false

  processor:
    - key_value:
        source: "payload"
        destination: null

        field_split_characters: "&&"     # pair delimiter (OK with grouping)
        value_split_characters: null     # disable the default "="
        key_value_delimiter_regex: "=="  # exact '==' for key/value

        value_grouping: true
        remove_brackets: false
        overwrite_if_destination_exists: false
        non_match_value: null

  sink:
    - opensearch:
        hosts: ["https://opensearch:9200"]
        insecure: true
        username: admin
        password: "admin_pass"
        index_type: custom
        index: "kv-regex-%{yyyy.MM.dd}"
```
{% include copy.html %}

您可以使用下列命令測試此管線：

```bash
curl -sS -X POST "http://localhost:2021/logs" \
  -H "Content-Type: application/json" \
  -d '[
    {
      "payload":"a==1&&b==[x=y,z=w]&&c==(inner=thing)&&http==http://example.com path",
      "a":"keep-me"
    },
    {
      "payload":"good==yes&&broken-token&&url==https://opensearch.org home",
      "note":"second doc"
    }
  ]'
```
{% include copy.html %}

儲存在 OpenSearch 中的文件包含下列資訊：

```json
{
  ...
  "hits": {
    "total": {
      "value": 2,
      "relation": "eq"
    },
    "max_score": 1,
    "hits": [
      {
        "_index": "kv-regex-2025.10.14",
        "_id": "FuCX4pkB344hN2Iu62oT",
        "_score": 1,
        "_source": {
          "payload": "a==1&&b==[x=y,z=w]&&c==(inner=thing)&&http==http://example.com path",
          "a": "keep-me",
          "b": "[x=y,z=w]",
          "c": "(inner=thing)",
          "http": "http://example.com path"
        }
      },
      {
        "_index": "kv-regex-2025.10.14",
        "_id": "F-CX4pkB344hN2Iu62oT",
        "_score": 1,
        "_source": {
          "payload": "good==yes&&broken-token&&url==https://opensearch.org home",
          "note": "second doc",
          "broken-token": null,
          "good": "yes",
          "url": "https://opensearch.org home"
        }
      }
    ]
  }
}
```

### 條件式遞迴鍵值解析

下列範例僅在 `/type == "nested"` 時，才會將 `body` 中以括號括住的巢狀 `key=value` 結構解析為 `parsed.*`。它會保留分組階層、強制執行嚴格的巢狀規則、套用預設欄位，並讓非巢狀事件保持不變：

```yaml
kv-conditional-recursive-pipeline:
  source:
    http:
      path: /logs
      ssl: false

  processor:
    - key_value:
        source: "body"
        destination: "parsed"

        key_value_when: '/type == "nested"'
        recursive: true

        # Split rules (per docs; not regex)
        field_split_characters: "&"
        value_split_characters: "="

        # Grouping & quoting (per docs)
        value_grouping: true
        string_literal_character: "\""
        remove_brackets: false

        # Keep only some top-level keys; then set defaults
        include_keys: ["item1","item2","owner"]
        default_values:
          owner: "unknown"
          region: "eu-west-1"

        strict_grouping: true
        tags_on_failure: ["keyvalueprocessor_failure"]

  sink:
    - opensearch:
        hosts: ["https://opensearch:9200"]
        insecure: true
        username: admin
        password: "admin_pass"
        index_type: custom
        index: "kv-recursive-%{yyyy.MM.dd}"
```
{% include copy.html %}

您可以使用下列命令測試此管線：

```bash
curl -sS -X POST "http://localhost:2021/logs" \
  -H "Content-Type: application/json" \
  -d '[
  {
    "type":"nested","body":"item1=[a=1&b=(c=3&d=<e=5>)]&item2=2&owner=alice"
  },
  {
    "type":"flat","body":"item1=[should=not&be=parsed]&item2=42"
  },
  {
    "type":"nested","body":"item1=[desc=\"a=b + c=d\"&x=1]&item2=2"
  }
]'
```
{% include copy.html %}

儲存在 OpenSearch 中的文件包含下列資訊：

```json
{
  ...
  "hits": {
    "total": {
      "value": 3,
      "relation": "eq"
    },
    "max_score": 1,
    "hits": [
      {
        "_index": "kv-recursive-2025.10.14",
        "_id": "Q7fC4pkBc0UY8I7pZ6vZ",
        "_score": 1,
        "_source": {
          "type": "nested",
          "body": "item1=[a=1&b=(c=3&d=<e=5>)]&item2=2&owner=alice",
          "parsed": {
            "owner": "alice",
            "item2": "2",
            "item1": {
              "a": "1",
              "b": {
                "c": "3",
                "d": {
                  "e": "5"
                }
              }
            },
            "region": "eu-west-1"
          }
        }
      },
      {
        "_index": "kv-recursive-2025.10.14",
        "_id": "RLfC4pkBc0UY8I7pZ6vZ",
        "_score": 1,
        "_source": {
          "type": "flat",
          "body": "item1=[should=not&be=parsed]&item2=42"
        }
      },
      {
        "_index": "kv-recursive-2025.10.14",
        "_id": "RbfC4pkBc0UY8I7pZ6vZ",
        "_score": 1,
        "_source": {
          "type": "nested",
          "body": """item1=[desc="a=b + c=d"&x=1]&item2=2""",
          "parsed": {
            "owner": "unknown",
            "item2": "2",
            "item1": {
              "desc": "\"a=b + c=d\"",
              "x": "1"
            },
            "region": "eu-west-1"
          }
        }
      }
    ]
  }
}
```

## 組態

選項 | 說明 | 範例 
:--- | :--- | :--- 
`source` | 要剖析的訊息欄位。選用。預設值為 `message`。 | 若 `source` 為 `"message1"`，`{"message1": {"key1=value1"}, "message2": {"key2=value2"}}` 會剖析為 `{"message1": {"key1=value1"}, "message2": {"key2=value2"}, "parsed_message": {"key1": "value1"}}`。 
`destination` | 剖析後來源的目標欄位。剖析後的來源會覆寫該鍵原有的資料。選用。若 `destination` 設為 `null`，剖析後的欄位將寫入事件的根層級。預設值為 `parsed_message`。 | 若 `destination` 為 `"parsed_data"`，`{"message": {"key1=value1"}}` 會剖析為 `{"message": {"key1=value1"}, "parsed_data": {"key1": "value1"}}`。 
`field_delimiter_regex` | 指定分隔鍵值對之分隔符的規則運算式。特殊規則運算式字元（例如 `[` 與 `]`）必須以 `\\` 逸出。不可與 `field_split_characters` 同時定義。選用。若未定義此選項，則使用 `field_split_characters`。 | 若 `field_delimiter_regex` 為 `"&\\{2\\}"`，`{"key1=value1&&key2=value2"}` 會剖析為 `{"key1": "value1", "key2": "value2"}`。 
`field_split_characters` | 指定分隔鍵值對之分隔符的字元字串。特殊規則運算式字元（例如 `[` 與 `]`）必須以 `\\` 逸出。不可與 `field_delimiter_regex` 同時定義。選用。預設值為 `&`。 | 若 `field_split_characters` 為 `"&&"`，`{"key1=value1&&key2=value2"}` 會剖析為 `{"key1": "value1", "key2": "value2"}`。 
`key_value_delimiter_regex` | 指定分隔鍵值對內鍵與值之分隔符的規則運算式。特殊規則運算式字元（例如 `[` 與 `]`）必須以 `\\` 逸出。此選項不可與 `value_split_characters` 同時定義。選用。若未定義此選項，則使用 `value_split_characters`。 | 若 `key_value_delimiter_regex` 為 `"=\\{2\\}"`，`{"key1==value1"}` 會剖析為 `{"key1": "value1"}`。 
`value_split_characters` | 指定分隔鍵值對內鍵與值之分隔符的字元字串。特殊規則運算式字元（例如 `[` 與 `]`）必須以 `\\` 逸出。不可與 `key_value_delimiter_regex` 同時定義。選用。預設值為 `=`。 | 若 `value_split_characters` 為 `"=="`，`{"key1==value1"}` 會剖析為 `{"key1": "value1"}`。 
`non_match_value` | 當鍵值對無法成功分割時，該鍵值對會放入 `key` 欄位，而指定的值會放入 `value` 欄位。選用。預設值為 `null`。 | `key1value1&key2=value2` 會剖析為 `{"key1value1": null, "key2": "value2"}`。 |
`prefix` | 附加在所有鍵前面的字首。選用。預設值為空字串。 | 若 `prefix` 為 `"custom"`，`{"key1=value1"}` 會剖析為 `{"customkey1": "value1"}`。 
`delete_key_regex` | 指定要從鍵中刪除之字元的規則運算式。特殊規則運算式字元（例如 `[` 與 `]`）必須以 `\\` 逸出。不可為空字串。選用。無預設值。 | 若 `delete_key_regex` 為 `"\s"`，`{"key1 =value1"}` 會剖析為 `{"key1": "value1"}`。 
`delete_value_regex` | 指定要從值中刪除之字元的規則運算式。特殊規則運算式字元（例如 `[` 與 `]`）必須以 `\\` 逸出。不可為空字串。選用。無預設值。 | 若 `delete_value_regex` 為 `"\s"`，`{"key1=value1 "}` 會剖析為 `{"key1": "value1"}`。 
`include_keys` | 指定剖析時應加入哪些鍵的陣列。預設會加入所有鍵。 | 若 `include_keys` 為 `["key2"]`，`key1=value1&key2=value2` 會剖析為 `{"key2": "value2"}`。 
`exclude_keys` | 指定哪些剖析後的鍵不應加入事件的陣列。預設不排除任何鍵。 | 若 `exclude_keys` 為 `["key2"]`，`key1=value1&key2=value2` 會剖析為 `{"key1": "value1"}`。 
`default_values` | 指定預設鍵及其值的對應，當被剖析的來源欄位中不存在這些鍵時，會將其加入事件。若預設鍵已存在於訊息中，則不會變更其值。`include_keys` 篩選器會在 `default_values` 之前套用於訊息。 | 若 `default_values` 為 `{"defaultkey": "defaultvalue"}`，`key1=value1` 會剖析為 `{"key1": "value1", "defaultkey": "defaultvalue"}`。 <br /> 若 `default_values` 為 `{"key1": "abc"}`，`key1=value1` 會剖析為 `{"key1": "value1"}`。 <br /> 若 `include_keys` 為 `["key1"]` 且 `default_values` 為 `{"key2": "value2"}`，`key1=value1&key2=abc` 會剖析為 `{"key1": "value1", "key2": "value2"}`。 
`transform_key` | 指定將鍵轉為小寫、大寫或首字母大寫。 | 若 `transform_key` 為 `lowercase`，`{"Key1=value1"}` 會剖析為 `{"key1": "value1"}`。 <br /> 若 `transform_key` 為 `uppercase`，`{"key1=value1"}` 會剖析為 `{"KEY1": "value1"}`。 <br /> 若 `transform_key` 為 `capitalize`，`{"key1=value1"}` 會剖析為 `{"Key1": "value1"}`。 
`whitespace` | 指定對設定的值分隔序列周圍不必要空白字元的接受方式為寬鬆或嚴格。預設為 `lenient`。 | 若 `whitespace` 為 `"lenient"`，`{"key1  =  value1"}` 會剖析為 `{"key1  ": "  value1"}`。若 `whitespace` 為 `"strict"`，`{"key1  =  value1"}` 會剖析為 `{"key1": "value1"}`。 
`skip_duplicate_values` | 用於移除重複鍵值對的布林值選項。設為 `true` 時，只會保留一組唯一的鍵值對。預設為 `false`。 | 若 `skip_duplicate_values` 為 `false`，`{"key1=value1&key1=value1"}` 會剖析為 `{"key1": ["value1", "value1"]}`。若 `skip_duplicate_values` 為 `true`，`{"key1=value1&key1=value1"}` 會剖析為 `{"key1": "value1"}`。 
`remove_brackets` | 指定是否將方括號、角括號與圓括號視為應從值中移除的值「包裝符」。預設為 `false`。 | 若 `remove_brackets` 為 `true`，`{"key1=(value1)"}` 會剖析為 `{"key1": value1}`。若 `remove_brackets` 為 `false`，`{"key1=(value1)"}` 會剖析為 `{"key1": "(value1)"}`。 
`recursive` | 指定是否從值中遞迴取得額外的鍵值對。額外的鍵值對會儲存為根鍵的子鍵。預設為 `false`。遞迴剖析的層級必須依此順序以不同的括號定義：`[]`、`()` 與 `<>`。其他指定的組態只會套用於最外層的鍵。 <br />當 `recursive` 為 `true` 時： <br /> `remove_brackets` 不可同時為 `true`；<br />`skip_duplicate_values` 一律為 `true`； <br />`whitespace` 一律為 `"strict"`。 | 若 `recursive` 為 true，`{"item1=[item1-subitem1=item1-subitem1-value&item1-subitem2=(item1-subitem2-subitem2A=item1-subitem2-subitem2A-value&item1-subitem2-subitem2B=item1-subitem2-subitem2B-value)]&item2=item2-value"}` 會剖析為 `{"item1": {"item1-subitem1": "item1-subitem1-value", "item1-subitem2" {"item1-subitem2-subitem2A": "item1-subitem2-subitem2A-value", "item1-subitem2-subitem2B": "item1-subitem2-subitem2B-value"}}}`。 
`overwrite_if_destination_exists` | 指定將剖析後的欄位寫入事件時若發生鍵衝突，是否覆寫現有欄位。預設為 `true`。 | 若 `overwrite_if_destination_exists` 為 `true` 且 destination 為 `null`，`{"key1": "old_value", "message": "key1=new_value"}` 會剖析為 `{"key1": "new_value", "message": "key1=new_value"}`。 
`tags_on_failure` | 當 `kv` 作業在處理器內造成執行期例外時，該作業會安全停止而不會使處理器當機，並以提供的標籤標記該事件。 | 若 `tags_on_failure` 設為 `["keyvalueprocessor_failure"]`，發生執行期例外時 `{"tags": ["keyvalueprocessor_failure"]}` 會加入事件的中繼資料。 
`value_grouping` | 指定是否使用預先定義的值分組分隔符進行分組：`{...}`、`[...]`、`<...>`、`(...)`、`"..."`、`'...'`、`http://... (space)` 與 `https:// (space)`。若啟用此旗標，分隔符之間的內容會被視為單一實體，不會剖析為鍵值對。預設為 `false`。若 `value_grouping` 為 `true`，則 `{"key1=[a=b,c=d]&key2=value2"}` 會剖析為 `{"key1": "[a=b,c=d]", "key2": "value2"}`。 
`drop_keys_with_no_value` | 指定鍵的值為 null 時是否捨棄該鍵。預設為 `false`。若 `drop_keys_with_no_value` 設為 `true`，則 `{"key1=value1&key2"}` 會剖析為 `{"key1": "value1"}`。 
`strict_grouping` | 指定使用 `value_grouping` 或 `string_literal_character` 選項時是否啟用嚴格分組。預設為 `false`。 | 啟用時，結尾字元不匹配的分組會產生錯誤。錯誤記錄後該事件會被忽略。 
`string_literal_character` | 可設為單引號（`'`）或雙引號（`"`）。預設為 `null`。 | 使用此選項時，包含在指定引號字元內的任何文字都會被忽略，並排除於鍵值剖析之外。例如，`text1 "key1=value1" text2 key2=value2` 會剖析為 `{"key2": "value2"}`。 
`key_value_when` | 允許您指定[條件運算式]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/expression-syntax/)，例如 `/some-key == "test"`，系統會評估該運算式以判斷是否應將處理器套用於事件。 


