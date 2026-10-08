---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "常見操作"
nav_order: 25
redirect_from:
  - /benchmark/user-guide/understanding-workloads/common-operations/
---

# 常見操作

[測試程序]({{site.url}}{{site.baseurl}}/benchmark/reference/workloads/test-procedures/)會使用各種操作，這些操作位於工作負載的 `operations` 目錄中。本頁詳細說明 OpenSearch Benchmark 工作負載中最常見的操作。

- [常見操作](#common-operations)
  - [bulk](#bulk)
  - [create-index](#create-index)
  - [delete-index](#delete-index)
  - [cluster-health](#cluster-health)
  - [refresh](#refresh)
  - [search](#search)

<!-- vale off -->
## bulk
<!-- vale on -->

`bulk` 操作類型可讓您以工作形式執行 [bulk](/api-reference/document-apis/bulk/) 請求。

下列範例顯示 `bulk` 操作類型，其 `bulk-size` 為 `5000` 份文件：

```yml
{
  "name": "index-append",
  "operation-type": "bulk",
  "bulk-size": 5000
}
```


<!-- vale off -->
## create-index
<!-- vale on -->

`create-index` 操作會執行 [Create Index API](/api-reference/index-apis/create-index/)。它支援下列兩種建立索引的模式：

- 建立工作負載 `indices` 區段中指定的所有索引
- 建立操作本身內定義的一個特定索引

下列範例會建立工作負載 `indices` 區段中定義的所有索引。它會使用工作負載中定義的所有索引設定，但會覆寫分片數：

```yml
{
  "name": "create-all-indices",
  "operation-type": "create-index",
  "settings": {
    "index.number_of_shards": 1
  },
  "request-params": {
    "wait_for_active_shards": "true"
  }
}
```

下列範例會建立新索引，並在操作本文中指定所有索引設定：

```yml
{
  "name": "create-an-index",
  "operation-type": "create-index",
  "index": "people",
  "body": {
    "settings": {
      "index.number_of_shards": 0
    },
    "mappings": {
      "docs": {
        "properties": {
          "name": {
            "type": "text"
          }
        }
      }
    }
  }
}
```



<!-- vale off -->
## delete-index
<!-- vale on -->

`delete-index` 操作會執行 [Delete Index API]({{site.url}}{{site.baseurl}}/api-reference/index-apis/delete-index/)。如同 [`create-index`](#create-index) 操作，您可以刪除工作負載 `indices` 區段中找到的所有索引，或根據 `index` 設定中傳入的字串刪除一或多個索引。

下列範例會刪除工作負載 `indices` 區段中找到的所有索引：

```yml
{
  "name": "delete-all-indices",
  "operation-type": "delete-index"
}
```

下列範例會刪除所有 `logs_*` 索引：

```yml
{
  "name": "delete-logs",
  "operation-type": "delete-index",
  "index": "logs-*",
  "only-if-exists": false,
  "request-params": {
    "expand_wildcards": "all",
    "allow_no_indices": "true",
    "ignore_unavailable": "true"
  }
}
```

<!-- vale off -->
## cluster-health
<!-- vale on -->

`cluster-health` 操作會執行 [Cluster Health API]({{site.url}}{{site.baseurl}}/api-reference/cluster-api/cluster-health/)，它會檢查叢集健康狀態，並根據為 `request-params` 設定的參數傳回預期狀態。若傳回非預期的叢集健康狀態，該操作會回報失敗。您可以在 OpenSearch Benchmark `run` 命令中使用 `--on-error` 選項，以控制 OpenSearch Benchmark 在健康檢查失敗時的行為。


下列範例會建立 `cluster-health` 操作，以檢查任何 `log-*` 索引的 `green` 健康狀態：

```yml
{
  "name": "check-cluster-green",
  "operation-type": "cluster-health",
  "index": "logs-*",
  "request-params": {
    "wait_for_status": "green",
    "wait_for_no_relocating_shards": "true"
  },
  "retry-until-success": true
}

```

<!-- vale off -->
## refresh
<!-- vale on -->

`refresh` 操作會執行 Refresh API。`operation` 不會傳回任何中繼資料。


下列範例會重新整理所有 `logs-*` 索引：

```yml
{
 "name": "refresh",
 "operation-type": "refresh",
 "index": "logs-*"
}
```


<!-- vale off -->
## search
<!-- vale on -->

`search` 操作會執行 [Search API](/api-reference/search/)，您可以使用它在 OpenSearch Benchmark 索引中執行查詢。

下列範例會在 `search` 操作內執行 `match_all` 查詢：

```yml
{
  "name": "default",
  "operation-type": "search",
  "body": {
    "query": {
      "match_all": {}
    }
  },
  "request-params": {
    "_source_include": "some_field",
    "analyze_wildcard": "false"
  }
}
```
