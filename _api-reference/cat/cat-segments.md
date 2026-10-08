---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: CAT segments
parent: CAT APIs
nav_order: 55
has_children: false
redirect_from:
- /opensearch/rest-api/cat/cat-segments/
---

# CAT Segments API
**於 1.0 版推出**
{: .label .label-purple }

cat segments 操作會列出每個索引的 Lucene 區段層級資訊。


<!-- spec_insert_start
api: cat.segments
component: endpoints
-->
## 端點
```json
GET /_cat/segments
GET /_cat/segments/{index}
```
<!-- spec_insert_end -->


<!-- spec_insert_start
api: cat.segments
component: query_parameters
columns: Parameter, Data type, Description, Default
include_deprecated: false
-->
## 查詢參數

下表列出可用的查詢參數。所有查詢參數皆為選用。

| 參數 | 資料類型 | 說明 | 預設 |
| :--- | :--- | :--- | :--- |
| `bytes` | 字串 | 用於顯示位元組值的單位。<br> 有效值為：`b`、`kb`、`k`、`mb`、`m`、`gb`、`g`、`tb`、`t`、`pb` 和 `p`。 | N/A |
| `cluster_manager_timeout` | 字串 | 允許用於建立與叢集管理員節點連線的時間。 | N/A |
| `format` | 字串 | `Accept` 標頭的簡短版本，例如 `json` 或 `yaml`。 | N/A |
| `h` | 清單 | 要顯示的資料行名稱清單，以逗號分隔。 | N/A |
| `help` | 布林值 | 傳回說明資訊。 | `false` |
| `s` | 清單 | 用於排序的資料行名稱或資料行別名清單，以逗號分隔。 | N/A |
| `v` | 布林值 | 啟用詳細模式，以顯示資料行標頭。 | `false` |

<!-- spec_insert_end -->

## 請求範例

<!-- spec_insert_start
component: example_code
rest: GET /_cat/segments?v
-->
{% capture step1_rest %}
GET /_cat/segments?v
{% endcapture %}

{% capture step1_python %}


response = client.cat.segments(
  params = { "v": "true" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

若要僅查看特定索引的區段資訊，請在您的查詢後面加上索引名稱。

<!-- spec_insert_start
component: example_code
rest: GET /_cat/segments/<index>?v
-->
{% capture step1_rest %}
GET /_cat/segments/<index>?v
{% endcapture %}

{% capture step1_python %}


response = client.cat.segments(
  index = "<index>",
  params = { "v": "true" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

如果您想取得多個索引的資訊，請以逗號分隔索引：

<!-- spec_insert_start
component: example_code
rest: GET /_cat/segments/index1,index2,index3
-->
{% capture step1_rest %}
GET /_cat/segments/index1,index2,index3
{% endcapture %}

{% capture step1_python %}


response = client.cat.segments(
  index = "index1,index2,index3"
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 回應範例

```json
index | shard | prirep | ip | segment | generation | docs.count | docs.deleted | size | size.memory | committed | searchable | version | compound
movies | 0 | p | 172.18.0.4 | _0 | 0 | 1 | 0 | 3.5kb | 1364 | true | true | 8.7.0 | true
movies | 0 | r | 172.18.0.3 | _0 | 0 | 1 | 0 | 3.5kb | 1364 | true | true | 8.7.0 | true
```

## 限制回應大小

若要限制傳回的索引數量，請設定 `cat.segments.response.limit.number_of_indices` 設定。如需詳細資訊，請參閱[叢集層級 CAT 回應限制設定]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/cluster-settings/#cluster-level-cat-response-limit-settings)。

## 必要權限

如果您使用 Security 外掛程式，請確認您具備適當的權限：`indices:monitor/segments`。
