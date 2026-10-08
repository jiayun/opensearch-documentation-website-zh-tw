---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "刪除資料串流"
parent: Data stream APIs
nav_order: 40
---

# 刪除資料串流 API
**引進於 1.0**
{: .label .label-purple }

刪除資料串流 API 會刪除資料串流及其後端索引。

<!-- spec_insert_start
api: indices.delete_data_stream
component: endpoints
-->
## 端點
```json
DELETE /_data_stream/{name}
```
<!-- spec_insert_end -->

<!-- spec_insert_start
api: indices.delete_data_stream
component: path_parameters
-->
## 路徑參數

下表列出可用的路徑參數。

| 參數 | 必要 | 資料類型 | 說明 |
| :--- | :--- | :--- | :--- |
| `name` | **必要** | 清單或字串 | 以逗號分隔的資料串流清單，用於指定要刪除的資料串流。支援萬用字元 (`*`) 運算式。 |

<!-- spec_insert_end -->

## 查詢參數

下表列出可用的查詢參數。所有查詢參數皆為選用。

| 參數 | 資料類型 | 說明 | 預設 |
| :--- | :--- | :--- | :--- |
| `error_trace` | 布林值 | 是否包含所傳回錯誤的堆疊追蹤。 | `false` |
| `filter_path` | 清單或字串 | 用於精簡回應。此參數接受以逗號分隔的篩選條件清單。支援使用萬用字元來比對任何欄位或欄位名稱的一部分。您也可以使用 `-` 排除欄位。 | N/A |
| `human` | 布林值 | 是否傳回人類可讀的統計值。 | `false` |
| `pretty` | 布林值 | 是否將傳回的 JSON 回應格式化為易讀的格式。 | `false` |
| `source` | 字串 | 經 URL 編碼的請求定義。適用於不接受非 POST 請求帶有請求本文的程式庫。 | N/A |

## 範例請求

下列範例請求會刪除 `logs-app` 資料串流及其後端索引：

<!-- spec_insert_start
component: example_code
rest: DELETE /_data_stream/logs-app
-->
{% capture step1_rest %}
DELETE /_data_stream/logs-app
{% endcapture %}

{% capture step1_python %}


response = client.indices.delete_data_stream(
  name = "logs-app"
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 範例回應

```json
{
  "acknowledged": true
}
```

## 必要權限

如果您使用 Security 外掛程式，請確認您具有適當的權限：`indices:admin/data_stream/delete`。

## 相關文件

- [資料串流]({{site.url}}{{site.baseurl}}/im-plugin/data-streams/)
- [建立或更新資料串流]({{site.url}}{{site.baseurl}}/api-reference/data-stream/create-data-stream/)