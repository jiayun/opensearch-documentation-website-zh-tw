---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "工作負載參數"
parent: Anatomy of a workload
nav_order: 60
---

# 工作負載參數

工作負載參數可讓您自訂工作負載的行為，而不必直接編輯工作負載檔案。您可以在執行階段傳遞參數，藉此控制大量處理大小、分片數量、索引名稱和搜尋組態等設定。

OpenSearch Benchmark 工作負載使用 [Jinja2](https://jinja.palletsprojects.com/) 範本。當您使用 `--workload-params` 旗標傳遞參數時，OpenSearch Benchmark 會在執行前將這些參數注入工作負載 JSON 檔案中。

例如，工作負載的 `index.json` 可能包含下列設定：

```json
{
  "settings": {
    "index.number_of_shards": {% raw %}{{ number_of_shards | default(1) }}{% endraw %},
    "index.number_of_replicas": {% raw %}{{ number_of_replicas | default(0) }}{% endraw %}
  }
}
```

當您使用 `--workload-params='{"number_of_shards": 3}'` 執行基準測試時，OpenSearch Benchmark 會將 `{% raw %}{{ number_of_shards | default(1) }}{% endraw %}` 取代為 `3`。您未覆寫的參數會使用其預設值。

## 傳遞參數

您可以透過下列方式傳遞參數。

### JSON 檔案（建議用於大量參數）

建立包含參數的 JSON 檔案：

```json
{
  "number_of_shards": 3,
  "number_of_replicas": 1,
  "bulk_size": 5000,
  "target_index_name": "my_index"
}
```
{% include copy.html %}

然後依下列方式參照該檔案：

```bash
opensearch-benchmark run --workload=geonames --workload-params=my-params.json
```
{% include copy.html %}

### 內嵌 JSON

直接在命令列上傳遞參數：

```bash
opensearch-benchmark run --workload=geonames --workload-params='{"number_of_shards": 3, "bulk_size": 5000}'
```
{% include copy.html %}

### 以逗號分隔的鍵值組

使用下列格式傳遞鍵值組：

```bash
opensearch-benchmark run --workload=geonames --workload-params="number_of_shards:3,bulk_size:5000"
```
{% include copy.html %}

以逗號分隔的格式僅支援字串值。若要使用數字、布林值或巢狀物件，請使用 JSON 檔案或內嵌 JSON。
{: .note}

## 參數優先順序

當同一個參數在多個來源中定義時，OpenSearch Benchmark 會依下列順序套用（優先順序由高至低）：

1. **`--workload-params`**（CLI 旗標）：覆寫所有其他值。
1. **工作負載範本預設值**：在工作負載 JSON 檔案中以 `{% raw %}{{ var | default(value) }}{% endraw %}` 運算式指定的預設值（例如 `{% raw %}{{ number_of_shards | default(1) }}{% endraw %}`）。
1. **未定義**：如果未指定預設值，也未提供該參數，OpenSearch Benchmark 會引發範本轉譯錯誤。

## 範本語法

本節說明工作負載檔案中最常用的範本模式。

### 具有預設值的變數

使用 `default` 篩選器，指定未提供參數時要使用的備用值。例如，如果 `--workload-params` 中未提供 `bulk_size`，運算式的求值結果為 `5000`：

```json
{% raw %}{{ bulk_size | default(5000) }}{% endraw %}
```
{% include copy.html %}

### 布林值

對布林值使用 `tojson` 篩選器，以確保 JSON 輸出正確。例如，下列運算式的求值結果為 `false`（不含引號），而非 `"false"`：

```json
{% raw %}{{ query_cache_enabled | default(false) | tojson }}{% endraw %}
```
{% include copy.html %}

### 字串值

以引號括住字串變數：

```json
{% raw %}"{{ conflicts | default('random') }}"{% endraw %}
```
{% include copy.html %}

### 條件式區段

使用 `{% raw %}{% if %}{% endraw %}` 區塊，根據參數是否已定義或參數的值，納入或排除區段。

#### 僅在已定義時納入欄位

下列範本會有條件地納入 `target-throughput` 欄位。如果未使用 `--workload-params` 提供 `target_throughput`，轉譯輸出中會省略整個欄位：

```json
{% raw %}{% if target_throughput is defined %}
"target-throughput": {{ target_throughput }},
{% endif %}{% endraw %}
```
{% include copy.html %}

<!-- vale off -->
#### 使用 If/else 提供替代值
<!-- vale on -->

使用 `{% raw %}{% else %}{% endraw %}` 提供備用值。例如，如果在 `--workload-params` 中將 `use_zstd` 設為 `true`，轉譯輸出會將 `source-file` 參數設為 `documents.json.zst`；否則會將 `source-file` 設為 `documents.json.bz2`：

```json
{% raw %}{% if use_zstd %}
"source-file": "documents.json.zst",
{% else %}
"source-file": "documents.json.bz2",
{% endif %}{% endraw %}
```
{% include copy.html %}

#### 有條件地新增索引欄位

此模式常用於在 `vectorsearch` 工作負載範本中定義選用欄位。`{% raw %}{%- endif %}{% endraw %}`（含破折號）會修剪結尾的空白字元和換行字元，避免出現空白行，並防止產生無效的 JSON 格式（例如結尾逗號或結構錯位）：

```json
"properties": {
  {% raw %}{% if id_field_name is defined and id_field_name != "_id" %}
  "{{ id_field_name }}": {
    "type": "keyword"
  },
  {%- endif %}{% endraw %}
  "embedding": {
    "type": "knn_vector",
    "dimension": {% raw %}{{ target_index_dimension }}{% endraw %}
  }
}
```
{% include copy.html %}

#### 以版本為依據的條件式

部分工作負載會根據 `distribution_version` 調整其行為，此值由 OpenSearch Benchmark 依據目標叢集自動設定。此模式可讓單一工作負載有條件地納入特定版本的操作或設定，藉此支援多個 OpenSearch 版本：

```json
{% raw %}{% if distribution_version is not defined %}
  {% set distribution_version = "2.11.0" %}
{% endif %}

{% if distribution_version.split('.') | map('int') | list >= "2.19.1".split('.') | map('int') | list %}
  {# Include features available in 2.19.1+ #}
{% endif %}{% endraw %}
```
{% include copy.html %}

#### For 迴圈

使用 `{% raw %}{% for %}{% endraw %}` 迴圈產生重複的結構：

```json
{% raw %}{% for i in range(1, 101) %}
{
  "name": "query-{{ i }}",
  "operation-type": "search",
  "body": { ... }
},
{% endfor %}{% endraw %}
```
{% include copy.html %}

### 整數轉換

當參數必須為整數時，請使用 `int` 篩選器：

```json
{% raw %}{{ target_index_dimension | default(768) | int }}{% endraw %}
```
{% include copy.html %}

### 納入外部檔案

為了提高可讀性，工作負載通常會分成多個檔案。`{% raw %}{{ benchmark.collect }}{% endraw %}` 輔助程式會在轉譯時，將多個 JSON 檔案組合成單一工作負載定義。

#### 匯入輔助程式

每個使用 `benchmark.collect` 的 `workload.json` 都必須在檔案開頭匯入該輔助程式：

```json
{% raw %}{% import "benchmark.helpers" as benchmark with context %}{% endraw %}
```
{% include copy.html %}

`with context` 子句可確保所有工作負載參數都能在納入的檔案中使用。

#### 收集操作與測試程序

典型的 `workload.json` 會將其操作和測試程序委派給個別的檔案：

```json
{% raw %}{% import "benchmark.helpers" as benchmark with context %}{% endraw %}
{
  "version": 2,
  "description": "My workload",
  "indices": [ ... ],
  "corpora": [ ... ],
  "operations": [
    {% raw %}{{ benchmark.collect(parts="operations/*.json") }}{% endraw %}
  ],
  "test_procedures": [
    {% raw %}{{ benchmark.collect(parts="test_procedures/*.json") }}{% endraw %}
  ]
}
```
{% include copy.html %}

`parts` 引數接受 glob 模式。模式 `operations/*.json` 會比對 `operations/` 目錄中的所有 JSON 檔案，並納入其內容，以逗號分隔。如此一來，主要的 `workload.json` 能保持簡潔，而操作與測試程序的定義則放在個別的檔案中。

#### 以共用部分組成排程

測試程序可以重複使用通用的排程片段。例如，`vectorsearch` 工作負載在 `test_procedures/common/` 下有共用的排程：

```
test_procedures/
  common/
    index-only-schedule.json
    search-only-schedule.json
    force-merge-schedule.json
    vespa-search-only-schedule.json
  default.json
```
{% include copy.html %}

`default.json` 中的測試程序會以這些部分組成其排程：

```json
{
  "name": "no-train-test",
  "default": true,
  "schedule": [
    {% raw %}{{ benchmark.collect(parts="common/index-only-schedule.json") }}{% endraw %},
    {% raw %}{{ benchmark.collect(parts="common/force-merge-schedule.json") }}{% endraw %},
    {% raw %}{{ benchmark.collect(parts="common/search-only-schedule.json") }}{% endraw %}
  ]
}
```
{% include copy.html %}

每個收集的檔案都包含一或多個排程項目。這些檔案中的參數（例如 `{% raw %}{{ target_index_name }}{% endraw %}`）會從命令列上傳入的同一個 `--workload-params` 解析，因為 `with context` 匯入會將所有參數傳遞給所包含的檔案。

#### 索引本文的檔案

索引定義中的 `body` 欄位會參照一個獨立的 JSON 檔案，用於對應和設定：

```json
"indices": [
  {
    "name": "geonames",
    "body": "index.json"
  }
]
```
{% include copy.html %}

`index.json` 檔案與其他工作負載檔案一樣是 Jinja2 範本，因此可以使用參數：

```json
{
  "settings": {
    "index.number_of_shards": {% raw %}{{ number_of_shards | default(1) }}{% endraw %}
  },
  "mappings": { ... }
}
```
{% include copy.html %}

## 探索可用的參數

若要檢視工作負載支援的參數，請使用 `info` 命令。此命令會列出工作負載的測試程序，以及其可設定的參數和預設值：

```bash
opensearch-benchmark info --workload=geonames
```
{% include copy.html %}

您也可以直接檢查工作負載的原始碼。參數在工作負載 JSON 檔案中以 `{% raw %}{{ variable_name | default(value) }}{% endraw %}` 的形式出現。主要的工作負載檔案如下：

- `workload.json` -- 最上層的工作負載定義。
- `index.json` -- 索引設定和對應。
- `test_procedures/default.json` -- 測試程序排程。
- `_operations/default.json` -- 操作定義。

## 常用參數

大多數官方工作負載都支援下列參數。

| 參數 | 說明 | 預設值 |
|-----------|-------------|-----------------|
| `number_of_shards` | 所建立索引的主要分片數量。 | `1` |
| `number_of_replicas` | 所建立索引的副本數量。 | `0` |
| `bulk_size` | 每個大量請求的文件數量。 | `5000` 或 `10000` |
| `bulk_indexing_clients` | 並行大量編製索引用戶端的數量。 | `8` |
| `ingest_percentage` | 要匯入的文件語料庫百分比。 | `100` |
| `target_throughput` | 每個用戶端每秒的目標操作次數。 | 不限速 |
| `search_clients` | 並行搜尋用戶端的數量。 | `1` |
| `cluster_health` | 繼續進行前所需的叢集健康狀態。 | `green` |
| `source_enabled` | 是否儲存 `_source` 欄位。 | `true` |

## 向量搜尋工作負載參數

`vectorsearch` 工作負載支援用於向量搜尋基準測試的其他參數。

| 參數 | 說明 | 預設值 |
|-----------|-------------|---------|
| `target_index_name` | 向量索引名稱。 | `target_index` |
| `target_field_name` | 向量欄位名稱。| `target_field` |
| `target_index_dimension` | 向量維度數量。 | `768` |
| `target_index_space_type` | 距離度量。有效值為 `l2`、`innerproduct` 和 `cosinesimil`。 | 視情況而定 |
| `target_index_body` | 索引設定檔案的路徑。 | `indices/faiss-index.json` |
| `target_index_bulk_size` | 每個大量請求的文件數量。 | `500` |
| `target_index_bulk_index_data_set_format` | 語料庫格式。有效值為 `hdf5` 和 `bigann`。 | `hdf5` |
| `target_index_bulk_index_data_set_corpus` | 語料庫名稱（例如 `cohere-1m`）。 | 視情況而定 |
| `target_index_bulk_indexing_clients` | 並行編製索引用戶端的數量。 | `10` |
| `target_index_max_num_segments` | 強制合併後的區段數量。 | `1` |
| `hnsw_ef_construction` | HNSW 圖形建置時的探索因子。 | `256` |
| `hnsw_ef_search` | HNSW 搜尋時的探索因子。 | `256` |
| `query_k` | 要擷取的最近鄰數量。 | `100` |
| `query_count` | 要執行的查詢數量。使用 `-1` 表示所有查詢。 | `-1` |
| `query_data_set_format` | 查詢向量格式。有效值為 `hdf5` 和 `bigann`。 | `hdf5` |
| `query_data_set_corpus` | 查詢向量語料庫名稱。 | 視情況而定 |
| `search_clients` | 並行搜尋用戶端的數量。 | `1` |
| `neighbors_data_set_corpus` | 用於召回率評估的真實鄰居語料庫。| 視情況而定 |
| `neighbors_data_set_format` | 鄰居資料集格式。 | `hdf5` |

### 向量搜尋參數檔案範例

以下範例顯示 `vectorsearch` 工作負載的完整參數檔案：

```json
{
  "target_index_name": "vector_1m",
  "target_field_name": "embedding",
  "target_index_body": "indices/faiss-index.json",
  "target_index_primary_shards": 1,
  "target_index_replica_shards": 0,
  "target_index_dimension": 768,
  "target_index_space_type": "innerproduct",
  "target_index_bulk_size": 500,
  "target_index_bulk_index_data_set_format": "hdf5",
  "target_index_bulk_index_data_set_corpus": "cohere-1m",
  "target_index_bulk_indexing_clients": 10,
  "target_index_max_num_segments": 1,
  "hnsw_ef_construction": 200,
  "hnsw_ef_search": 256,
  "query_k": 100,
  "query_data_set_format": "hdf5",
  "query_data_set_corpus": "cohere-1m",
  "query_count": 10000,
  "search_clients": 1,
  "neighbors_data_set_corpus": "cohere-1m",
  "neighbors_data_set_format": "hdf5"
}
```
{% include copy.html %}

若要使用此參數檔案，請將其儲存為 `params.json`，並使用 `--workload-params` 旗標執行基準測試：

```bash
opensearch-benchmark run \
  --pipeline=benchmark-only \
  --workload-path=/path/to/vectorsearch \
  --workload-params=params.json \
  --target-hosts=localhost:9200
```
{% include copy.html %}