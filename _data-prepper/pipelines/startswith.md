---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: startsWith()
parent: Functions
grand_parent: Pipelines
nav_order: 40
---

<!-- vale off -->
# startsWith() 函式
<!-- vale on -->

`startsWith()` 函式會檢查字串是否以指定的字串開頭。它接受兩個引數：

- 第一個引數是常值字串，或代表要檢查之欄位或值的 JSON 指標。

- 第二個引數是要在第一個引數中檢查的字串。
如果第一個引數所代表的字串或欄位值以第二個引數指定的字串開頭，函式會傳回 `true`，否則傳回 `false`。

例如，若要檢查名為 `message` 的欄位值是否以字串 `"abcd"` 開頭，請使用 `startsWith()` 函式，如下所示：

```
startsWith('/message', 'abcd')
```
{% include copy.html %}

如果 `message` 欄位以字串 `abcd` 開頭，此呼叫會傳回 `true`，否則傳回 `false`。

或者，您也可以使用常值字串作為第一個引數：

```
startsWith('abcdef', 'abcd')
```
{% include copy.html %}

在此情況下，函式會傳回 `true`，因為字串 `abcdef` 以 `abcd` 開頭。

`startsWith()` 函式會執行區分大小寫的檢查。
{: .note }

## 範例

下列管線使用 `startsWith()` 函式，將兩個布林值旗標 `starts_abcd` 和 `starts_error` 新增至每個事件，並只將以字串 `ERROR:` 開頭的事件轉送至 OpenSearch：

```yaml
startswith-demo:
  source:
    http:
      ssl: false

  processor:
    - add_entries:
        entries:
          - key: starts_abcd
            value_expression: startsWith(/message, "abcd")

          - key: starts_error
            value_expression: startsWith(/message, "ERROR:")

    # forward only messages that start with "ERROR:"
    - drop_events:
        drop_when: not startsWith(/message, "ERROR:")

  sink:
    - opensearch:
        hosts: ["https://opensearch:9200"]  
        insecure: true  
        username: admin
        password: admin_pass
        index_type: custom
        index: startswith-demo-%{yyyy.MM.dd}
```
{% include copy.html %}

您可以使用下列命令測試管線：

```bash
curl -X POST "http://localhost:2021/log/ingest" \
  -H "Content-Type: application/json" \
  -d '[                                                              
        {"message":"ok hello"},
        {"message":"abcd-hello"},
        {"message":"ERROR: something bad"},
        {"message":"ERROR: abcd unit test failed"}
      ]'
```
{% include copy.html %}

儲存在 OpenSearch 中的文件包含下列資訊：

```json
{
  ...
  "hits" : {
    "total" : {
      "value" : 2,
      "relation" : "eq"
    },
    "max_score" : 1.0,
    "hits" : [
      {
        "_index" : "startswith-demo-2025.11.10",
        "_id" : "X97tbpoBnoSLj36HBGoL",
        "_score" : 1.0,
        "_source" : {
          "starts_abcd" : false,
          "starts_error" : true,
          "message" : "ERROR: something bad"
        }
      },
      {
        "_index" : "startswith-demo-2025.11.10",
        "_id" : "YN7tbpoBnoSLj36HBGoL",
        "_score" : 1.0,
        "_source" : {
          "starts_abcd" : false,
          "starts_error" : true,
          "message" : "ERROR: abcd unit test failed"
        }
      }
    ]
  }
}
```