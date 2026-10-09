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

我們可以使用 [OpenSearch output plugin](https://github.com/opensearch-project/logstash-output-opensearch) 將 Logstash 事件傳送至 OpenSearch 叢集，同樣地，也可以使用 [OpenSearch input plugin](https://github.com/opensearch-project/logstash-input-opensearch) 對 OpenSearch 叢集執行讀取操作，並將資料載入 Logstash。

OpenSearch input plugin 會讀取在 OpenSearch 叢集上執行的搜尋查詢結果，並將其載入 Logstash。這讓您可以重新播放測試記錄檔、重新編製索引，並根據載入的資料執行其他操作。您可以使用
[cron 運算式]({{site.url}}{{site.baseurl}}/api-reference/common-parameters/#cron-expressions) 排定資料匯入操作定期執行，也可以只執行一次查詢，手動將資料載入 Logstash。



## OpenSearch input plugin

若要執行 OpenSearch input plugin，請將組態新增至 Logstash `config` 資料夾內的 `pipeline.conf` 檔案。下列範例會執行 `match_all` 查詢篩選器，並載入資料一次。

```yml
input {
  opensearch {
    hosts       => "https://hostname:port"
    user        => "admin"
    password    => "admin"
    index       => "logstash-logs-%{+YYYY.MM.dd}"
    query       => '{ "query": { "match_all": {}} }'
  }
}

filter {
}

output {
}
```

若要依照排程匯入資料，請使用指定所需排程的 cron 運算式。例如，若要每分鐘載入一次資料，請在 `pipeline.conf` 檔案的 input 區段中新增 `schedule => "* * * * *"`。

與 output plugin 相同，將組態新增至 `pipeline.conf` 檔案後，請提供該檔案的路徑來啟動 Logstash：

 ```bash
 $ bin/logstash -f config/pipeline.conf --config.reload.automatic
 ```

`config/pipeline.conf` 是 `pipeline.conf` 檔案的相對路徑，您也可以使用絕對路徑。

在 `pipeline.conf` 檔案的 `output{}` 區段中新增 `stdout{}`，即可將查詢結果輸出至主控台。

若要將資料重新編製索引至 OpenSearch 網域，請如[這裡]({{site.url}}{{site.baseurl}}/tools/logstash/index/)所示，在 `output{}` 區段中新增目的地網域的組態。
