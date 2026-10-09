---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "版本"
parent: String field types
grand_parent: Supported field types
nav_order: 75
redirect_from:
  - /opensearch/supported-field-types/version/
  - /field-types/supported-field-types/version/
---

# 版本欄位類型
**於 3.2 版引入**
{: .label .label-purple }

`version` 欄位類型專為符合[語意化版本（SemVer）](https://semver.org/)規範的版本字串編製索引與查詢而設計。此欄位類型可正確排序與比較版本字串，例如 `1.0.0`、`2.1.0-alpha`、`1.3.0+build.1` 等。

`version` 欄位類型提供下列功能：

- 正確剖析包含主要版本、次要版本與修補版本組成部分的語意化版本字串
- 處理預發行識別碼，例如 `-alpha`、`-beta` 和 `-rc.1`
- 接受建置中繼資料，例如 `+build.123`，但排序時會忽略這些資料（依據 SemVer 規範）
- 依據語意化版本規則排序版本（例如 `1.0.0-alpha < 1.0.0-beta < 1.0.0`）
- 與各種查詢類型相容，包括範圍、詞彙、多詞彙、萬用字元、前綴等查詢

## 版本格式

版本字串必須遵循語意化版本格式：

```
<major>.<minor>.<patch>[-<pre-release>][+<build-metadata>]
```

上述格式中的變數必須依下列方式提供。

| 組成部分 | 必要／選用 | 說明 | 範例 |
|:----------|:------------------|:------------|:--------|
| `major`、`minor`、`patch` | 必要 | 表示核心版本號碼的非負整數 | `1.2.3` |
| `pre-release` | 選用 | 以點分隔的英數字識別碼，表示預發行版本 | `-alpha`、`-beta.1`、`-rc.2` |
| `build-metadata` | 選用 | 以點分隔的英數字識別碼，提供建置資訊（排序時會忽略） | `+build.123`、`+20230815` |

## 對應範例

建立包含版本欄位的索引：

```json
PUT test_versions
{
  "mappings": {
    "properties": {
      "app": {
        "type": "keyword"
      },
      "version": {
        "type": "version"
      },
      "release_date": {
        "type": "date"
      },
      "description": {
        "type": "text"
      }
    }
  }
}
```
{% include copy-curl.html %}


## 為版本資料編製索引

將包含版本欄位的文件編製索引：

```json
POST test_versions/_bulk
{ "index": {} }
{ "app": "AlphaApp", "version": "1.0.0", "release_date": "2023-01-01", "description": "Initial release" }
{ "index": {} }
{ "app": "AlphaApp", "version": "1.0.1", "release_date": "2023-02-15", "description": "Bug fix release" }
{ "index": {} }
{ "app": "AlphaApp", "version": "1.1.0", "release_date": "2023-05-10", "description": "Minor feature update" }
{ "index": {} }
{ "app": "AlphaApp", "version": "2.0.0", "release_date": "2024-01-01", "description": "Major release" }
{ "index": {} }
{ "app": "BetaApp", "version": "0.9.0", "release_date": "2022-12-01", "description": "Beta release" }
{ "index": {} }
{ "app": "BetaApp", "version": "1.0.0-alpha", "release_date": "2023-03-01", "description": "Alpha pre-release" }
{ "index": {} }
{ "app": "BetaApp", "version": "1.0.0-alpha.1", "release_date": "2023-03-10", "description": "Alpha patch" }
{ "index": {} }
{ "app": "BetaApp", "version": "1.0.0-beta", "release_date": "2023-04-01", "description": "Beta pre-release" }
{ "index": {} }
{ "app": "BetaApp", "version": "1.0.0-rc.1", "release_date": "2023-04-15", "description": "Release candidate" }
{ "index": {} }
{ "app": "BetaApp", "version": "1.0.0+20230815", "release_date": "2023-08-15", "description": "Build metadata release" }
```
{% include copy-curl.html %}

## 查詢版本欄位

版本欄位類型支援各種查詢類型。

### 詞彙查詢

尋找具有特定版本的文件：

```json
GET test_versions/_search
{
  "query": {
    "term": { "version": "1.0.1" }
  }
}
```
{% include copy-curl.html %}

#### 回應

```json
{
  "took": 5,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 1,
      "relation": "eq"
    },
    "max_score": 1.0466295,
    "hits": [
      {
        "_index": "test_versions",
        "_id": "cSWNQpcBY7cEASBv3Vr1",
        "_score": 1.0466295,
        "_source": {
          "app": "AlphaApp",
          "version": "1.0.1",
          "release_date": "2023-02-15",
          "description": "Bug fix release"
        }
      }
    ]
  }
}
```

### 範圍查詢

尋找特定範圍內的版本：

```json
GET test_versions/_search
{
  "query": {
    "range": {
      "version": { "gte": "2.0.0" }
    }
  }
}
```
{% include copy-curl.html %}

#### 回應

```json
{
  "took": 3,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 1,
      "relation": "eq"
    },
    "max_score": 1,
    "hits": [
      {
        "_index": "test_versions",
        "_id": "cyWNQpcBY7cEASBv3Vr1",
        "_score": 1,
        "_source": {
          "app": "AlphaApp",
          "version": "2.0.0",
          "release_date": "2024-01-01",
          "description": "Major release"
        }
      }
    ]
  }
}
```

### 多詞彙查詢

尋找符合多個特定版本的文件：

```json
GET test_versions/_search
{
  "query": {
    "terms": {
      "version": ["1.0.0", "1.0.0-alpha"]
    }
  }
}
```
{% include copy-curl.html %}

### 萬用字元查詢

尋找符合模式的版本：

```json
GET test_versions/_search
{
  "query": {
    "wildcard": {
      "version": "1.2.0-*"
    }
  }
}
```
{% include copy-curl.html %}

### 前綴查詢

尋找具有特定前綴的版本：

```json
GET test_versions/_search
{
  "query": {
    "prefix": {
      "version": {
        "value": "1.0.0-"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 依版本排序

若要依版本排序，請在請求中提供 `sort` 參數。版本會依據語意化版本規則排序：

```json
GET test_versions/_search
{
  "query": { "match_all": {} },
  "sort": [
    { "version": { "order": "asc" } }
  ]
}
```
{% include copy-curl.html %}

此請求會傳回依版本順序排序的文件，預發行版本會出現在其對應的穩定版本之前：`0.9.0`、`1.0.0-alpha`、`1.0.0-alpha.1`、`1.0.0-beta`、`1.0.0-rc.1`、`1.0.0+20230815`、`1.0.1`、`1.1.0`、`2.0.0`。

## 版本比較規則

版本欄位遵循語意化版本比較規則：

1. `major`、`minor`、`patch`：以數值比較（`1.2.3` < `1.2.4` < `1.3.0` < `2.0.0`）。
2. 預發行版本優先順序：預發行版本的優先順序低於正式版本（`1.0.0-alpha` < `1.0.0`）。
3. 預發行版本比較：當兩個版本都是預發行版本時，會依字典順序逐一比較以點分隔的識別碼（`1.0.0-alpha` < `1.0.0-alpha.1` < `1.0.0-beta`）。
4. 忽略建置中繼資料：建置中繼資料不會影響版本優先順序（就排序而言，`1.0.0+build.1` 等於 `1.0.0+build.2`）。

## 參數

下表列出版本欄位類型接受的參數。所有參數皆為選用。

參數 | 說明 
:--- | :--- 
`doc_values` | 布林值，指定是否應將欄位儲存在磁碟上，以便用於彙總、排序或指令碼。預設為 `true`。
`index` | 布林值，指定欄位是否可供搜尋。預設為 `true`。
`meta` | 接受此欄位的中繼資料。
`store` | 布林值，指定是否應儲存欄位值，並可獨立於 `_source` 欄位擷取。預設為 `false`。

## 限制

- 版本字串必須遵循語意化版本格式。無效的版本字串會導致編製索引失敗。
- 接受建置中繼資料，但比較與排序時會忽略這些資料。
- 此欄位不支援進階版本範圍規格，例如 `^1.2.3` 或 `~1.2.0`；請改用 [`range` 查詢]({{site.url}}{{site.baseurl}}/query-dsl/term/range/)。
