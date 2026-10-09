---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "重新命名鍵"
parent: Processors
grand_parent: Pipelines
nav_order: 310
---

# 重新命名鍵處理器

`rename_keys` 處理器會重新命名事件中的鍵。

## 組態

您可以使用下列選項設定 `rename_keys` 處理器。

| 選項 | 必要 | 說明 |
| :--- | :--- | :--- |
| `entries` | 是 | 要重新命名的事件項目清單。 |
| `from_key` | 是 | 要重新命名的項目之鍵。 |
| `to_key` | 是 | 項目的新鍵。 |
| `overwrite_if_to_key_exists` | 否 | 設為 `true` 時，若事件中已存在 `key`，則會覆寫現有值。預設值為 `false`。 |

## 使用方式

若要開始使用，請建立下列 `pipeline.yaml` 檔案：

```yaml
rename-keys-nested-pipeline:
  source:
    http:
      path: /logs
      ssl: false
  processor:
    - rename_keys:
        entries:
          # Top-level rename
          - from_key: message
            to_key: msg
          # Level-2 (nested) renames — use slash paths
          - from_key: user/name
            to_key: user/username
          - from_key: user/id
            to_key: user/user_id
          - from_key: http/response/code
            to_key: http/status_code
          # If a target exists already, overwrite it
          - from_key: env
            to_key: metadata/environment
            overwrite_if_to_key_exists: true
  sink:
    - opensearch:
        hosts: ["https://opensearch:9200"]
        insecure: true
        username: admin
        password: admin_password
        index_type: custom
        index: rename-%{yyyy.MM.dd}
```
{% include copy.html %}

您可以使用下列命令測試此管線：

```bash
curl -sS -X POST "http://localhost:2021/logs" \
  -H "Content-Type: application/json" \
  -d '[
    {
      "message": "hello world",
      "user": { "name": "alice", "id": 123 },
      "http": { "response": { "code": 200 } },
      "env": "prod",
      "metadata": { "environment": "staging" }
    },
    {
      "message": "goodbye",
      "user": { "name": "bob", "id": 456 },
      "http": { "response": { "code": 503 } },
      "env": "dev"
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
        "_index": "rename-2025.11.04",
        "_id": "kq3NTpoBNvg1WLcAJOak",
        "_score": 1,
        "_source": {
          "user": {
            "username": "alice",
            "user_id": 123
          },
          "http": {
            "response": {},
            "status_code": 200
          },
          "metadata": {
            "environment": "prod"
          },
          "msg": "hello world"
        }
      },
      {
        "_index": "rename-2025.11.04",
        "_id": "k63NTpoBNvg1WLcAJOak",
        "_score": 1,
        "_source": {
          "user": {
            "username": "bob",
            "user_id": 456
          },
          "http": {
            "response": {},
            "status_code": 503
          },
          "msg": "goodbye",
          "metadata": {
            "environment": "dev"
          }
        }
      }
    ]
  }
}
```

## 特殊考量

重新命名作業會依照 `pipeline.yaml` 檔案中鍵值對項目的列出順序執行。這表示 `rename_keys` 處理器會隱含地進行鏈結（依序重新命名鍵值對）。請參閱下列 `pipeline.yaml` 檔案範例：

```yaml
  processor:
    - rename_keys:
        entries:
        - from_key: "message"
          to_key: "message2"
        - from_key: "message2"
          to_key: "message3"
```

如果處理器收到 `{"message": "hello"}`，產生的輸出如下：

```json
{"message3": "hello"}
```
