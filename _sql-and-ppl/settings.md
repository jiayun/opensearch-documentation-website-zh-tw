---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "設定"
nav_order: 77
redirect_from:
  - /search-plugins/sql/settings/
---

# SQL 設定

SQL 外掛程式會為標準 OpenSearch 叢集設定新增一些設定。大多數設定為動態設定，因此您不需要重新啟動叢集，即可變更外掛程式的預設行為。若要進一步了解靜態與動態設定，請參閱[設定 OpenSearch]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/index/)。

您可以個別停用 `PPL` 或 `SQL` 查詢的處理。

您可以像更新任何其他叢集設定一樣更新這些設定：

```json
PUT _cluster/settings
{
  "transient" : {
    "plugins.sql.enabled" : false
  }
}
```
{% include copy-curl.html %}

或者，您也可以使用下列請求格式：

```json
PUT _cluster/settings
{
  "transient": {
    "plugins": {
      "ppl": {
        "enabled": "false"
      }
    }
  }
}
```
{% include copy-curl.html %}

同樣地，您可以將請求傳送至 `_plugins/_query/settings` 端點來更新設定：

```json
PUT _plugins/_query/settings
{
  "transient" : {
    "plugins.sql.enabled" : false
  }
}
```
{% include copy-curl.html %}

或者，您也可以使用下列請求格式：

```json
PUT _plugins/_query/settings
{
  "transient": {
    "plugins": {
      "ppl": {
        "enabled": "false"
      }
    }
  }
}
```
{% include copy-curl.html %}

傳送至 `_plugins/_ppl` 與 `_plugins/_sql` 端點的請求會在請求本文中包含索引名稱，因此它們與 `bulk`、`mget` 及 `msearch` 作業具有相同的存取原則考量。將 `rest.action.multi.allow_explicit_index` 參數設為 `false` 會同時停用 `SQL` 與 `PPL` 端點。
{: .note}

## 可用的設定

設定 | 預設 | 說明
:--- | :--- | :---
`plugins.sql.enabled` | `true` | 變更為 `false` 以停用外掛程式中的 `SQL` 支援。
`plugins.ppl.enabled` | `true` | 變更為 `false` 以停用外掛程式中的 `PPL` 支援。
`plugins.sql.slowlog` | `2` | 設定慢速查詢的時間限制 (以秒為單位)。外掛程式會將慢速查詢記錄為 `opensearch.log` 中的 `Slow query: elapsed=xxx (ms)`。
`plugins.sql.cursor.keep_alive` | `1m` | 設定游標內容保持開啟的時間長度。由於游標內容會耗用大量資源，建議您設定較低的值。
`plugins.query.memory_limit` | `85%` | 設定查詢引擎斷路器的堆積記憶體使用量限制。
`plugins.query.size_limit` | `10000` | 設定查詢執行所傳回的最大資料列數。
`plugins.query.datasources.enabled` | `true` | 變更為 `false` 以停用外掛程式中的資料來源支援。
`plugins.query.field_type_tolerance` | `true` | 若為 `false`，則陣列會在任何巢狀層級縮減為第一個非陣列值。例如，`[[1, 2], [3, 4]]` 會縮減為 `1`。若為 `true`，則會保留陣列。預設為 `true`。
`plugins.query.buckets` | `10000` | 設定單一回應中傳回的彙總桶數。預設為 `plugins.query.size_limit` 值。
`plugins.calcite.enabled` | `true` | 啟用 Apache Calcite 查詢引擎，包括進階 SQL 與 PPL 功能，例如子搜尋、`join` 及 `lookup` 作業。
`plugins.calcite.pushdown.enabled` | `true` | 變更為 `false` 以停用運算子下推最佳化。建議您使用預設值。
`plugins.calcite.fallback.allowed` | `false` | 變更為 `true` 以允許回復至 v2 引擎。
`plugins.calcite.pushdown.rowcount.estimation.factor` | `0.9` | 用於將資料表掃描的資料列數相乘，以預估結果資料列數的因數。建議您使用預設值。
`plugins.calcite.all_join_types.allowed` | `false` | 啟用對效能敏感的聯結類型，例如 `RIGHT`、`FULL` 及 `CROSS` 聯結。變更為 `true` 以允許這些聯結作業。
`plugins.ppl.syntax.legacy.preferred` | `true` | 控制 PPL 語法行為，包括預設引數值。當為 `false` 時，會使用較新的語法標準。如需詳細資訊，請參閱[舊版語法文件](https://github.com/opensearch-project/sql/blob/main/docs/user/ppl/admin/settings.md#pluginspplsyntaxlegacypreferred)。
`plugins.ppl.values.max.limit` | `0` | 設定 `VALUES` 彙總函式可傳回的唯一值數上限。值為 `0` 表示無限制。
`plugins.ppl.rex.max_match.limit` | `10` | 設定 `rex` 命令所擷取的相符項數上限。
`plugins.ppl.subsearch.maxout` | `10000` | 設定子搜尋可傳回的資料列數上限。
`plugins.ppl.join.subsearch_maxout` | `50000` | 設定聯結作業中所用子搜尋可傳回的資料列數上限。
`plugins.ppl.pattern.method` | `simple_pattern` | 設定 `patterns` 命令的方法。有效值為 `simple_pattern` 與 `brain`。如需詳細資訊，請參閱[`patterns` 語法](https://github.com/opensearch-project/sql/blob/main/docs/user/ppl/cmd/patterns.md#syntax)。
`plugins.ppl.pattern.mode` | `label` | 設定 `patterns` 命令的模式。有效值為 `label` 與 `aggregation`。如需詳細資訊，請參閱[`patterns` 語法](https://github.com/opensearch-project/sql/blob/main/docs/user/ppl/cmd/patterns.md#syntax)。
`plugins.ppl.pattern.max.sample.count` | `10` | 設定彙總模式下每個模式所傳回的範例記錄數上限。
`plugins.ppl.pattern.buffer.limit` | `100000` | 設定 `brain` 演算法所用內部暫存緩衝區的大小。
`plugins.ppl.pattern.show.numbered.token` | `false` | 變更為 `true` 以啟用編號詞元輸出格式。
`plugins.ppl.query.timeout` | `5m` | 設定 PPL 查詢可執行的時間上限。若查詢超過此限制，執行會停止並傳回逾時錯誤。

## Spark 連接器設定

SQL 外掛程式支援 [Apache Spark](https://spark.apache.org/) 作為擴增運算來源。當資料來源在 Apache Spark 中定義為資料表時，OpenSearch 可取用這些資料表。這可讓您在 OpenSearch Dashboards 的 [Discover]({{site.url}}{{site.baseurl}}/dashboards/discover/index-discover/) 及可觀測性記錄檔中，對外部來源執行 SQL 查詢。

若要開始使用，請啟用下列設定，以將 Spark 新增為資料來源並啟用正確的權限。

設定 | 說明
:--- | :---
`spark.uri` | 您的 Spark 資料來源識別碼。
`spark.auth.type` | 用於驗證進入 Spark 的授權類型。
`spark.auth.username` | 您的 Spark 資料來源使用者名稱。
`spark.auth.password` | 您的 Spark 資料來源密碼。
`spark.datasource.flint.host` | Spark 資料來源的主機。預設為 `localhost`。
`spark.datasource.flint.port` | Spark 的連接埠號碼。預設為 `9200`。
`spark.datasource.flint.scheme` | Spark 查詢使用的通訊協定。有效值為 `http` 與 `https`。
`spark.datasource.flint.auth` | 存取 Spark 資料來源所需的授權。有效值為 `false` 與 `sigv4`。
`spark.datasource.flint.region` | 您的 OpenSearch 叢集所在的 AWS 區域。僅在 `auth` 設為 `sigv4` 時使用。預設值為 `us-west-2`。
`spark.datasource.flint.write.id_name` | Spark 連接器寫入的索引名稱。
`spark.datasource.flint.ignore.id_column` | 在查詢中匯出資料時排除 `id` 欄位。預設為 `true`。
`spark.datasource.flint.write.batch_size` | 設定寫入 Spark 連線索引時的批次大小。預設為 `1000`。
`spark.datasource.flint.write.refresh_policy` | 設定連接器無法將資料寫入 OpenSearch 時，Spark 連線的重新整理原則。可為不重新整理 (`false`)、立即重新整理 (`true`)，或設定等待時間 `wait_for: X`。預設值為 `false`。
`spark.datasource.flint.read.scroll_size` | 設定使用 Spark 執行之查詢所傳回的結果數。預設為 `100`。
`spark.flint.optimizer.enabled` | 啟用 OpenSearch 以針對 Spark 連線進行最佳化。預設為 `true`。
`spark.flint.index.hybridscan.enabled` | 啟用 OpenSearch 以從資料來源掃描非分割裝置上的寫入資料。預設為 `false`。

設定完成後，您可以使用下列 API 呼叫測試您的 Spark 連線：

```json
POST /_plugins/_ppl
content-type: application/json

{
   "query": "source = my_spark.sql('select * from alb_logs')"
}
```
{% include copy-curl.html %}
