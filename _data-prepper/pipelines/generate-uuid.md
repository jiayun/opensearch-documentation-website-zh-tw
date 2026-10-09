---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: generateUuid()
parent: Functions
grand_parent: Pipelines
nav_order: 11
---

<!-- vale off -->
# generateUuid() 函式
<!-- vale on -->

`generateUuid()` 函式不接受任何引數，並傳回隨機產生的 [UUID 第 4 版](https://www.rfc-editor.org/rfc/rfc4122) 字串，例如 `"550e8400-e29b-41d4-a716-446655440000"`。每次呼叫都會使用密碼學上安全的隨機數字產生器產生唯一值，因此在實務上碰撞機率可忽略不計。

當來源記錄不含自然唯一識別碼時，此函式便很實用——例如執行非同步批次推論工作時，需要穩定的鍵將推論結果對應回原始記錄。

## 使用方式

在 [`add_entries`]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/processors/add-entries/) 處理器中，使用 `generateUuid()` 作為 `value_expression`。此範例會為通過處理器的每個事件新增一個包含唯一 UUID 的 `recordId` 欄位：

```yaml
processor:
  - add_entries:
      entries:
        - key: recordId
          value_expression: 'generateUuid()'
```
{% include copy.html %}


## 範例

下列管線會為每個傳入的記錄檔記錄指派唯一的 `recordId`，再將其轉送至 OpenSearch：

```yaml
uuid-demo-pipeline:
  source:
    http:
      ssl: false

  processor:
    - add_entries:
        entries:
          - key: recordId
            value_expression: 'generateUuid()'

  sink:
    - opensearch:
        hosts: ["https://opensearch:9200"]
        insecure: true
        username: admin
        password: admin_password
        index_type: custom
        index: demo-index-%{yyyy.MM.dd}
```
{% include copy.html %}

給定下列輸入事件：

```json
{ "message": "user login", "user": "alice" }
```
{% include copy.html %}

儲存在 OpenSearch 中的文件包含下列資訊：

```json
{
  "message": "user login",
  "user": "alice",
  "recordId": "550e8400-e29b-41d4-a716-446655440000"
}
```
