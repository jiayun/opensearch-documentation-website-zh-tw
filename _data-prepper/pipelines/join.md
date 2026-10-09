---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: join()
parent: Functions
grand_parent: Pipelines
nav_order: 25
---

<!-- vale off -->
# join() 函式
<!-- vale on -->


`join()` 函式會將清單中的元素串接起來以形成字串。此函式接受一個 JSON 指標，代表清單或對應 (其值為清單類型) 的鍵，並使用分隔符號將清單以字串形式串接。預設分隔符號為逗號 (`,`)。

## 參數

`join` 函式接受下列參數：

- `delimiter` (字串，選用)：放置在元素之間的字串。範例：`,`、` | `、`; `。預設值為 `,`。
- `pointer` (必要)：解析至事件中某個清單的 JSON 指標。

## 回傳值
`join` 命令回傳下列值：

- `string`：使用指定的 `delimiter` 串接所有元素後的結果。

## 快速範例
- `join("-", /labels)` 在 `labels: ["prod","api","us"]` 時回傳 `"prod-api-us"`
- `join(" | ", /authors)` 在 `authors: ["Ada","Linus","Grace"]` 時回傳 `"Ada | Linus | Grace"`

## 在管線中使用 `join()`

您可以在支援 `value_expression` 的處理器中使用 `join()`，例如 `add_entries` 處理器：

```yaml
processor:
  - add_entries:
      entries:
        - key: labels_csv
          value_expression: join(" | ", /labels)
```
{% include copy.html %}

## 範例

下列管線使用 `http` 來源匯入 JSON 事件，接著使用 `add_entries` 搭配 `join()` 建立兩個新欄位 `labels_csv` 和 `authors_pipe`：

```yaml
join-demo:
  source:
    http:
      path: /events
      ssl: false
  processor:
    - add_entries:
        entries:
          - key: labels_csv
            value_expression: join(/labels) # Comma is used by default
          - key: authors_pipe
            value_expression: join(" | ", /authors)
  sink:
    - opensearch:
        hosts: ["https://opensearch:9200"]
        index: join-demo-%{yyyy.MM.dd}
        username: admin
        password: admin_password
        index_type: custom
        insecure: true  # set to true for self-signed local clusters
```
{% include copy.html %}

您可以使用下列命令測試此管線：

```bash
curl "http://localhost:2021/events" \
   -H "Content-Type: application/json" \
   -d '[
    {"message":"hello","labels":["prod","api","us"],"authors":["Ada","Linus","Grace"]},
    {"message":"world","labels":["stage","etl"],"authors":["Marie","Alan"]}
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
        "_index": "join-demo-2025.11.06",
        "_id": "aGFyWZoBjfY5UoR7NC36",
        "_score": 1,
        "_source": {
          "message": "hello",
          "labels": [
            "prod",
            "api",
            "us"
          ],
          "authors": [
            "Ada",
            "Linus",
            "Grace"
          ],
          "labels_csv": "prod,api,us",
          "authors_pipe": "Ada | Linus | Grace"
        }
      },
      {
        "_index": "join-demo-2025.11.06",
        "_id": "aWFyWZoBjfY5UoR7NC36",
        "_score": 1,
        "_source": {
          "message": "world",
          "labels": [
            "stage",
            "etl"
          ],
          "authors": [
            "Marie",
            "Alan"
          ],
          "labels_csv": "stage,etl",
          "authors_pipe": "Marie | Alan"
        }
      }
    ]
  }
}
```