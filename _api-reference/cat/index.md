---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: CAT APIs
nav_order: 10
has_children: true
has_toc: false
redirect_from:
  - /opensearch/catapis/
  - /opensearch/rest-api/cat/index/
  - /api-reference/cat/
---

# CAT APIs
**於 1.0 版導入**
{: .label .label-purple }

您可以使用精簡且對齊的文字 (CAT) API，以易於理解的表格格式取得叢集的重要統計資料。CAT API 是一種人類可讀的介面，會傳回純文字而非傳統的 JSON。

使用 CAT API，您可以回答諸如哪個節點是當選的叢集管理員節點、叢集目前處於什麼狀態、每個索引中有多少文件等問題。

## 範例

若要查看 CAT API 中可用的操作，請使用下列命令：

<!-- spec_insert_start
component: example_code
rest: GET /_cat
-->
{% capture step1_rest %}
GET /_cat
{% endcapture %}

{% capture step1_python %}

response = client.cat.help()
{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

回應是一隻 ASCII 貓 (`=^.^=`) 以及一份操作清單：

```
=^.^=
/_cat/allocation
/_cat/segment_replication
/_cat/segment_replication/{index}
/_cat/shards
/_cat/shards/{index}
/_cat/cluster_manager
/_cat/nodes
/_cat/tasks
/_cat/indices
/_cat/indices/{index}
/_cat/segments
/_cat/segments/{index}
/_cat/count
/_cat/count/{index}
/_cat/recovery
/_cat/recovery/{index}
/_cat/health
/_cat/pending_tasks
/_cat/aliases
/_cat/aliases/{alias}
/_cat/thread_pool
/_cat/thread_pool/{thread_pools}
/_cat/plugins
/_cat/fielddata
/_cat/fielddata/{fields}
/_cat/nodeattrs
/_cat/repositories
/_cat/snapshots/{repository}
/_cat/templates
/_cat/pit_segments
/_cat/pit_segments/{pit_id}
```

## 選用的查詢參數

根 `_cat` API 不接受任何參數，但個別的 API，例如 `/_cat/nodes`，接受下列查詢參數。

參數 | 說明
:--- | :--- |
`v` |  在欄位上方加入標頭，以提供詳細輸出。它也會加入一些格式設定，協助將各欄位對齊。本節的所有範例都包含 `v` 參數。
`help` | 列出指定操作的預設標頭及其他可用標頭。
`h`  |  將輸出限制為特定標頭。
`format` |  傳回結果時使用的格式。有效值為 `json`、`yaml`、`cbor` 和 `smile`。
`s` | 依指定的欄位排序輸出。

### 查詢參數使用範例

您可以對任何 CAT 操作指定查詢參數，以取得更具體的結果。

### 取得詳細輸出

若要查詢別名並取得包含回應中所有欄位標題的詳細輸出，請使用 `v` 查詢參數。

<!-- spec_insert_start
component: example_code
rest: GET /_cat/aliases?v
-->
{% capture step1_rest %}
GET /_cat/aliases?v
{% endcapture %}

{% capture step1_python %}


response = client.cat.aliases(
  params = { "v": "true" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

回應會提供更多詳細資訊，例如回應中每個欄位的名稱。

```
alias index filter routing.index routing.search is_write_index
.kibana .kibana_1 - - - -
sample-alias1 sample-index-1 - - - -
```
若未使用 verbose 參數 `v`，回應只會傳回別名名稱：

```
.kibana .kibana_1 - - - -
sample-alias1 sample-index-1 - - - -
```

### 取得所有可用的標頭

若要查看所有可用的標頭，請使用 `help` 參數：

```
GET _cat/{operation_name}?help
```

例如，若要查看 CAT aliases 操作可用的標頭，請傳送下列請求：

<!-- spec_insert_start
component: example_code
rest: GET /_cat/aliases?help
-->
{% capture step1_rest %}
GET /_cat/aliases?help
{% endcapture %}

{% capture step1_python %}


response = client.cat.aliases(
  params = { "help": "true" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

回應包含可用的標頭：

```
alias          | a                | alias name
index          | i,idx            | index alias points to
filter         | f,fi             | filter
routing.index  | ri,routingIndex  | index routing
routing.search | rs,routingSearch | search routing
is_write_index | w,isWriteIndex   | write index
```

### 取得標頭的子集

若要將輸出限制為標頭的子集，請使用 `h` 參數：

```
GET _cat/{operation_name}?h={header_name_1},{header_name_2}&v
```

例如，若要將別名限制為只顯示別名名稱與索引，請傳送下列請求：

<!-- spec_insert_start
component: example_code
rest: GET /_cat/aliases?h=alias,index
-->
{% capture step1_rest %}
GET /_cat/aliases?h=alias,index
{% endcapture %}

{% capture step1_python %}


response = client.cat.aliases(
  params = { "h": "alias,index" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

回應包含所請求的資訊：

```
.kibana .kibana_1
sample-alias1 sample-index-1
```

一般而言，對於任何操作，您都可以使用 `help` 參數找出有哪些可用的標頭，然後使用 `h` 參數將輸出限制為只顯示您關心的標頭。

### 依標頭排序

若要依標頭排序輸出，請使用 `s` 參數：

```json
GET _cat/{operation_name}?s={header_name_1},{header_name_2}
```

例如，若要先依別名再依索引排序別名，請傳送下列請求：

<!-- spec_insert_start
component: example_code
rest: GET /_cat/aliases?s=i,a
-->
{% capture step1_rest %}
GET /_cat/aliases?s=i,a
{% endcapture %}

{% capture step1_python %}


response = client.cat.aliases(
  params = { "s": "i,a" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

回應包含所請求的資訊：

```
sample-alias2 sample-index-1
sample-alias1 sample-index-2
```

### 以 JSON 格式擷取資料

預設情況下，CAT API 會以 `text/plain` 格式傳回資料。

若要以 JSON 格式擷取資料，請使用 `format=json` 參數：

```json
GET _cat/{operation_name}?format=json
```

例如，若要以 JSON 格式擷取別名，請傳送下列請求：

<!-- spec_insert_start
component: example_code
rest: GET /_cat/aliases?format=json
-->
{% capture step1_rest %}
GET /_cat/aliases?format=json
{% endcapture %}

{% capture step1_python %}


response = client.cat.aliases(
  params = { "format": "json" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

回應包含 JSON 格式的資料：

```json
[
  {"alias":".kibana","index":".kibana_1","filter":"-","routing.index":"-","routing.search":"-","is_write_index":"-"},
  {"alias":"sample-alias-1","index":"sample-index-1","filter":"-","routing.index":"-","routing.search":"-","is_write_index":"-"}
]
```

其他支援的格式有 [YAML](https://yaml.org/)、[CBOR](https://cbor.io/) 和 [Smile](https://github.com/FasterXML/smile-format-specification)。

## CAT API 操作

下列 CAT API 操作可供使用。

### 叢集與節點資訊
- [CAT aliases]({{site.url}}{{site.baseurl}}/api-reference/cat/cat-aliases/)
- [CAT allocation]({{site.url}}{{site.baseurl}}/api-reference/cat/cat-allocation/)
- [CAT cluster manager]({{site.url}}{{site.baseurl}}/api-reference/cat/cat-cluster_manager/)
- [CAT health]({{site.url}}{{site.baseurl}}/api-reference/cat/cat-health/)
- [CAT nodes]({{site.url}}{{site.baseurl}}/api-reference/cat/cat-nodes/)
- [CAT node attributes]({{site.url}}{{site.baseurl}}/api-reference/cat/cat-nodeattrs/)
- [CAT pending tasks]({{site.url}}{{site.baseurl}}/api-reference/cat/cat-pending-tasks/)
- [CAT plugins]({{site.url}}{{site.baseurl}}/api-reference/cat/cat-plugins/)
- [CAT repositories]({{site.url}}{{site.baseurl}}/api-reference/cat/cat-repositories/)
- [CAT tasks]({{site.url}}{{site.baseurl}}/api-reference/cat/cat-tasks/)
- [CAT templates]({{site.url}}{{site.baseurl}}/api-reference/cat/cat-templates/)
- [CAT thread pool]({{site.url}}{{site.baseurl}}/api-reference/cat/cat-thread-pool/)

### 索引與文件資訊
- [CAT count]({{site.url}}{{site.baseurl}}/api-reference/cat/cat-count/)
- [CAT field data]({{site.url}}{{site.baseurl}}/api-reference/cat/cat-field-data/)
- [CAT indices]({{site.url}}{{site.baseurl}}/api-reference/cat/cat-indices/)
- [CAT PIT segments]({{site.url}}{{site.baseurl}}/api-reference/cat/cat-pit-segments/)
- [CAT recovery]({{site.url}}{{site.baseurl}}/api-reference/cat/cat-recovery/)
- [CAT segment replication]({{site.url}}{{site.baseurl}}/api-reference/cat/cat-segment-replication/)
- [CAT segments]({{site.url}}{{site.baseurl}}/api-reference/cat/cat-segments/)
- [CAT shards]({{site.url}}{{site.baseurl}}/api-reference/cat/cat-shards/)

### 快照資訊
- [CAT snapshots]({{site.url}}{{site.baseurl}}/api-reference/cat/cat-snapshots/)

如果您使用 Security 外掛程式，請確認您具備適當的權限。
{: .note }
