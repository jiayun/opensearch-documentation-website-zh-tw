---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "建立資料串流"
parent: Data stream APIs
nav_order: 10
---

# Create Data Stream API
**於 1.0 版推出**
{: .label .label-purple }

Create Data Stream API 可建立資料串流。建立資料串流之前，您必須建立索引範本，將一組索引設定為資料串流。如需詳細資訊，請參閱[將資料串流編製索引]({{site.url}}{{site.baseurl}}/im-plugin/data-streams/)。

<!-- spec_insert_start
api: indices.create_data_stream
component: endpoints
-->
## 端點
```json
PUT /_data_stream/{name}
```
<!-- spec_insert_end -->

<!-- spec_insert_start
api: indices.create_data_stream
component: path_parameters
-->
## 路徑參數

下表列出可用的路徑參數。

| 參數 | 必要 | 資料類型 | 說明 |
| :--- | :--- | :--- | :--- |
| `name` | **必要** | 字串 | 資料串流的名稱，必須符合下列條件：僅限小寫；不得包含 `\`、`/`、`*`、`?`、`"`、`<`、`>`、`\|`、`,`、`#`、`:` 或空白字元；不得以 `-`、`_`、`+` 或 `.ds-` 開頭；不得為 `.` 或 `..`；長度不得超過 255 位元組。多位元組字元會更快達到此上限。 |

<!-- spec_insert_end -->

## 查詢參數

下表列出可用的查詢參數。所有查詢參數皆為選用。

| 參數 | 資料類型 | 說明 | 預設 |
| :--- | :--- | :--- | :--- |
| `error_trace` | 布林值 | 是否包含所傳回錯誤的堆疊追蹤。 | `false` |
| `filter_path` | 清單或字串 | 用於縮減回應。此參數接受以逗號分隔的篩選條件清單。支援使用萬用字元來比對任何欄位或欄位名稱的一部分。您也可以使用 `-` 排除欄位。 | 不適用 |
| `human` | 布林值 | 是否傳回以易於閱讀的格式呈現的統計值。 | `false` |
| `pretty` | 布林值 | 是否將傳回的 JSON 回應格式化，使其易於閱讀。 | `false` |
| `source` | 字串 | 經 URL 編碼的請求定義。適用於不接受非 POST 請求之請求本文的程式庫。 | 不適用 |


## 請求範例

下列請求範例使用先前建立且相符的索引範本，建立 `logs-app` 資料串流：

<!-- spec_insert_start
component: example_code
rest: PUT /_data_stream/logs-app
body: {}
-->
{% capture step1_rest %}
PUT /_data_stream/logs-app
{}
{% endcapture %}

{% capture step1_python %}


response = client.indices.create_data_stream(
  name = "logs-app",
  body =   {}
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 回應範例

```json
{
  "acknowledged": true
}
```

## 必要權限

如果您使用 Security 外掛程式，請確認您具備適當的權限：`indices:admin/data_stream/create`。

## 相關文件

- [資料串流]({{site.url}}{{site.baseurl}}/im-plugin/data-streams/)
- [取得資料串流]({{site.url}}{{site.baseurl}}/api-reference/data-stream/data-stream-info/)
- [刪除資料串流]({{site.url}}{{site.baseurl}}/api-reference/data-stream/delete-data-stream/)
