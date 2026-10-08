---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "指標參考"
nav_order: 25
has_children: true
parent: Reference
redirect_from:
  - /benchmark/metrics/
  - /benchmark/metrics/index/
  - /benchmark/reference/metrics/
---

# OpenSearch Benchmark 指標

工作負載完成後，OpenSearch Benchmark 會將所有指標記錄儲存在其指標存放區中。這些指標可以保存在記憶體或 OpenSearch 叢集中。

## 儲存指標

您可以在 `benchmark.ini` 檔案中設定 [`datastore.type`]({{site.url}}{{site.baseurl}}/benchmark/configuring-benchmark/#reporting) 參數，指定執行基準測試時要將指標儲存在記憶體或指標存放區中。

### 記憶體中

如果您想在執行基準測試時將指標儲存在記憶體中，請在 `benchmark.ini` 的 `reporting` 區段中提供下列設定：

```ini
[reporting]
datastore.type = in-memory
datastore.host = <host-url>
datastore.port = <host-port>
datastore.secure = False
datastore.ssl.verification_mode = <ssl-verification-details>
datastore.user = <username>
datastore.password = <password>
```

### OpenSearch

如果您想在執行基準測試時將指標儲存在外部 OpenSearch 記憶體存放區中，請在 `benchmark.ini` 的 `reporting` 區段中提供下列設定：

```ini
[reporting]
datastore.type = opensearch
datastore.host = <opensearch endpoint>
datastore.port = 443
datastore.secure = true
datastore.ssl.verification_mode = none
datastore.user = <opensearch basic auth username>
datastore.password = <opensearch basic auth password>
datastore.number_of_replicas =
datastore.number_of_shards =
```
若未提供 `datastore.number_of_replicas` 和 `datastore.number_of_shards`，OpenSearch 會使用預設值：副本數為 `0`，分片數為 `1`。如果在建立資料存放區叢集後變更這些設定，新的副本和分片設定只會在月底建立新的結果索引時套用。

執行已設定為使用 OpenSearch 作為資料存放區的 OpenSearch Benchmark 後，OpenSearch Benchmark 會建立三個索引：

- `benchmark-metrics-YYYY-MM`：存放細粒度的指標和遙測資料。
- `benchmark-results-YYYY-MM`：存放以最終結果為基礎的資料。
- `benchmark-test-executions-YYYY-MM`：存放關於 `execution-ids` 的資料。

您可以在 OpenSearch Dashboards 中將這些索引內的資料視覺化。


## 後續步驟

- 如需如何設計指標存放區的更多資訊，請參閱 [指標記錄]({{site.url}}{{site.baseurl}}/benchmark/metrics/metric-records/)。
- 如需儲存了哪些指標的更多資訊，請參閱 [指標鍵]({{site.url}}{{site.baseurl}}/benchmark/metrics/metric-keys/)。
