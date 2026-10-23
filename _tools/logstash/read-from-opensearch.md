---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "從 OpenSearch 讀取資料"
parent: Logstash
nav_order: 220
redirect_from:
  - /clients/logstash/read-from-opensearch/
---

# 從 OpenSearch 讀取資料

使用 [OpenSearch input 外掛程式](https://github.com/opensearch-project/logstash-input-opensearch) 在 OpenSearch 叢集上執行搜尋查詢，並將符合條件的文件以事件形式載入 Logstash。例如，您可以重新播放測試記錄檔、將文件重新編製索引到另一個叢集，或將文件匯出至檔案。此外掛程式可以執行查詢一次，或依排程定期執行。

開始之前，請先安裝 [Logstash 與 OpenSearch input 外掛程式]({{site.url}}{{site.baseurl}}/tools/logstash/index/#installing-logstash)。

## 設定 OpenSearch input 外掛程式

若要從 OpenSearch 讀取資料，請將 `opensearch` 外掛程式加入管線組態檔的 `input` 區段。以下範例會對名稱以 `logstash-logs-` 開頭的所有索引執行 `match_all` 查詢，並將文件列印到終端機。請將 `<admin-password>` 替換為 `admin` 使用者的密碼，並將 `<path-to-root-ca>` 替換為簽署 OpenSearch 節點憑證的憑證授權單位檔案路徑：

```ruby
input {
  opensearch {
    hosts    => ["localhost:9200"]
    user     => "admin"
    password => "<admin-password>"
    index    => "logstash-logs-*"
    query    => '{ "query": { "match_all": {} } }'
    ssl      => true
    ca_file  => "<path-to-root-ca>"
  }
}

output {
  stdout { }
}
```
{% include copy.html %}

此外掛程式的設定有以下要求：

- 當 `ssl` 為 `true` 時，請將 `hosts` 指定為 `<hostname>:<port>`，不要加上 `https://` 前綴。若包含前綴，外掛程式將無法解析主機名稱。
- 當 `ssl` 為 `true` 時，外掛程式一律會驗證 OpenSearch 節點憑證。`hosts` 中的主機名稱必須與節點憑證中的名稱相符。例如，OpenSearch 示範組態中的憑證僅對 `localhost` 有效。
- `index` 設定不支援 `%{+YYYY.MM.dd}` 這類日期模式。若要從多個索引讀取資料，請使用萬用字元運算式或以逗號分隔的索引名稱清單。

使用管線組態檔啟動 Logstash：

```bash
bin/logstash -f config/pipeline.conf
```
{% include copy.html %}

當查詢完成且外掛程式已載入所有符合條件的文件後，Logstash 會停止。

## 依排程執行查詢

若要依排程執行查詢，請加入包含 cron 運算式的 `schedule` 設定。例如，以下設定會每分鐘執行一次查詢：

```ruby
schedule => "* * * * *"
```
{% include copy.html %}

指定排程後，Logstash 會持續執行，並在每次查詢執行時載入符合條件的文件。如需 cron 運算式語法的詳細資訊，請參閱 [Cron 運算式]({{site.url}}{{site.baseurl}}/api-reference/cron-expressions/)。

## 設定

下表列出最常用的 OpenSearch input 外掛程式設定。

設定 | 資料類型 | 說明
:--- | :--- | :---
`hosts` | 陣列 | 要連線的 OpenSearch 主機，格式為 `<hostname>:<port>`。
`index` | 字串 | 要查詢的一或多個索引。支援萬用字元運算式。預設為 `logstash-*`。
`query` | 字串 | 要執行的查詢，採用 OpenSearch Query DSL 格式。預設為 `{ "sort": [ "_doc" ] }`，會傳回所有文件。
`schedule` | 字串 | 指定何時執行查詢的 cron 運算式。若未指定，查詢只執行一次。
`user` | 字串 | 基本驗證的使用者名稱。
`password` | 字串 | 基本驗證的密碼。
`ssl` | 布林值 | 是否透過 HTTPS 連線至 OpenSearch。預設為 `false`。
`ca_file` | 字串 | 用於驗證 OpenSearch 節點憑證的憑證授權單位檔案路徑。
`size` | 整數 | 每個 scroll 請求傳回的文件數量。預設為 `1000`。
`scroll` | 字串 | scroll 請求之間保持搜尋脈絡 (scroll context) 開啟的時間長度。預設為 `1m`。
`docinfo` | 布林值 | 是否將文件中繼資料（例如索引名稱與文件 ID）加入 `[@metadata][input][opensearch]` 欄位中的每個事件。預設為 `false`。

## 範例：將文件複製到另一個索引

若要將文件從一個索引複製到另一個索引，請使用 OpenSearch input 外掛程式讀取文件，並使用 OpenSearch output 外掛程式寫入文件。以下管線會將 `logstash-logs-*` 索引中的文件複製到 `logstash-logs-copy` 索引，並保留每個文件的 ID：

```ruby
input {
  opensearch {
    hosts    => ["localhost:9200"]
    user     => "admin"
    password => "<admin-password>"
    index    => "logstash-logs-*"
    ssl      => true
    ca_file  => "<path-to-root-ca>"
    docinfo  => true
  }
}

output {
  opensearch {
    hosts       => ["https://localhost:9200"]
    user        => "admin"
    password    => "<admin-password>"
    index       => "logstash-logs-copy"
    document_id => "%{[@metadata][input][opensearch][_id]}"
    ssl         => true
    cacert      => "<path-to-root-ca>"
  }
}
```
{% include copy.html %}

如需 output 外掛程式設定的詳細資訊，請參閱[將事件傳送至 OpenSearch]({{site.url}}{{site.baseurl}}/tools/logstash/ship-to-opensearch/)。
