---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "CAT PIT 區段"
parent: CAT APIs
nav_order: 46
---

# CAT Pit Segments API
**於 2.4 版引入**
{: .label .label-purple }

CAT 時間點（PIT）區段操作透過描述 PIT 的 Lucene 區段，提供該 PIT 磁碟使用情況的底層資訊。PIT Segments API 支援依 ID 列出特定 PIT 的區段資訊，或一次列出所有 PIT 的區段資訊。

## 端點

<!-- spec_insert_start
api: cat.pit_segments
component: endpoints
omit_header: true
-->
```json
GET /_cat/pit_segments
```
<!-- spec_insert_end -->

<!-- spec_insert_start
api: cat.all_pit_segments
component: endpoints
omit_header: true
-->
```json
GET /_cat/pit_segments/_all
```
<!-- spec_insert_end -->

<!-- spec_insert_start
api: cat.pit_segments
component: query_parameters
columns: Parameter, Data type, Description, Default
include_deprecated: false
-->
## 查詢參數

下表列出可用的查詢參數。所有查詢參數皆為選用。

| 參數 | 資料類型 | 說明 | 預設 |
| :--- | :--- | :--- | :--- |
| `bytes` | 字串 | 用於顯示位元組值的單位。<br> 有效值為：`b`、`kb`、`k`、`mb`、`m`、`gb`、`g`、`tb`、`t`、`pb` 和 `p`。 | N/A |
| `format` | 字串 | `Accept` 標頭的簡短版本，例如 `json` 或 `yaml`。 | N/A |
| `h` | 清單 | 要顯示的欄名稱清單，以逗號分隔。 | N/A |
| `help` | 布林值 | 傳回說明資訊。 | `false` |
| `s` | 清單 | 用於排序的欄名稱或欄別名清單，以逗號分隔。 | N/A |
| `v` | 布林值 | 啟用詳細模式，此模式會顯示欄標題。 | `false` |

<!-- spec_insert_end -->

## 請求本文欄位

欄位 | 資料類型 | 說明  
:--- | :--- | :---
`pit_id` | [Base64 編碼的二進位資料]({{site.url}}{{site.baseurl}}/opensearch/supported-field-types/binary/) 或二進位資料陣列 | 要列出區段的 PIT 所對應的 PIT ID。必要。

## 請求範例：所有 PIT 的 PIT 區段

<!-- spec_insert_start
component: example_code
rest: GET /_cat/pit_segments/_all
-->
{% capture step1_rest %}
GET /_cat/pit_segments/_all
{% endcapture %}

{% capture step1_python %}

response = client.cat.all_pit_segments()
{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

如果沒有區段（未儲存任何資料），API 不會傳回任何資訊。

## 請求範例：依 ID 列出 PIT 的 PIT 區段

若要列出一個或多個 PIT 的區段，請在請求本文中指定其 PIT ID：

<!-- spec_insert_start
component: example_code
rest: GET /_cat/pit_segments
body: |
{
    "pit_id": [
        "o463QQEPbXktaW5kZXgtMDAwMDAxFkhGN09fMVlPUkVPLXh6MUExZ1hpaEEAFjBGbmVEZHdGU1EtaFhhUFc4ZkR5cWcAAAAAAAAAAAEWaXBPNVJtZEhTZDZXTWFFR05waXdWZwEWSEY3T18xWU9SRU8teHoxQTFnWGloQQAA",
        "o463QQEPbXktaW5kZXgtMDAwMDAxFkhGN09fMVlPUkVPLXh6MUExZ1hpaEEAFjBGbmVEZHdGU1EtaFhhUFc4ZkR5cWcAAAAAAAAAAAIWaXBPNVJtZEhTZDZXTWFFR05waXdWZwEWSEY3T18xWU9SRU8teHoxQTFnWGloQQAA"
    ]
}
-->
{% capture step1_rest %}
GET /_cat/pit_segments
{
  "pit_id": [
    "o463QQEPbXktaW5kZXgtMDAwMDAxFkhGN09fMVlPUkVPLXh6MUExZ1hpaEEAFjBGbmVEZHdGU1EtaFhhUFc4ZkR5cWcAAAAAAAAAAAEWaXBPNVJtZEhTZDZXTWFFR05waXdWZwEWSEY3T18xWU9SRU8teHoxQTFnWGloQQAA",
    "o463QQEPbXktaW5kZXgtMDAwMDAxFkhGN09fMVlPUkVPLXh6MUExZ1hpaEEAFjBGbmVEZHdGU1EtaFhhUFc4ZkR5cWcAAAAAAAAAAAIWaXBPNVJtZEhTZDZXTWFFR05waXdWZwEWSEY3T18xWU9SRU8teHoxQTFnWGloQQAA"
  ]
}
{% endcapture %}

{% capture step1_python %}


response = client.cat.pit_segments(
  body =   {
    "pit_id": [
      "o463QQEPbXktaW5kZXgtMDAwMDAxFkhGN09fMVlPUkVPLXh6MUExZ1hpaEEAFjBGbmVEZHdGU1EtaFhhUFc4ZkR5cWcAAAAAAAAAAAEWaXBPNVJtZEhTZDZXTWFFR05waXdWZwEWSEY3T18xWU9SRU8teHoxQTFnWGloQQAA",
      "o463QQEPbXktaW5kZXgtMDAwMDAxFkhGN09fMVlPUkVPLXh6MUExZ1hpaEEAFjBGbmVEZHdGU1EtaFhhUFc4ZkR5cWcAAAAAAAAAAAIWaXBPNVJtZEhTZDZXTWFFR05waXdWZwEWSEY3T18xWU9SRU8teHoxQTFnWGloQQAA"
    ]
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 回應範例

```json
index  shard prirep ip            segment generation docs.count docs.deleted  size size.memory committed searchable version compound
index1 0     r      10.212.36.190 _0               0          4            0 3.8kb        1364 false     true       8.8.2   true
index1 1     p      10.212.36.190 _0               0          3            0 3.7kb        1364 false     true       8.8.2   true
index1 2     r      10.212.74.139 _0               0          2            0 3.6kb        1364 false     true       8.8.2   true
```
