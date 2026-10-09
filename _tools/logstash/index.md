---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Logstash
nav_order: 150
has_children: true
has_toc: true
redirect_from:
  - /clients/logstash/
  - /clients/logstash/index/
  - /tools/logstash/
---

# Logstash

Logstash 是即時事件處理引擎。它是 OpenSearch 技術堆疊的一部分，此堆疊包含 OpenSearch、Beats 和 OpenSearch Dashboards。

您可以從許多不同來源將事件傳送至 Logstash。Logstash 會處理事件，並將其傳送至一個或多個目的地。例如，您可以將網頁伺服器的存取記錄檔傳送至 Logstash。Logstash 會從每筆記錄擷取有用的資訊，並將其傳送至 OpenSearch 等目的地。

將事件傳送至 Logstash 可讓您將事件處理與應用程式分離。您的應用程式只需要將事件傳送至 Logstash，不需要知道事件後續如何處理。

開放原始碼社群最初建立 Logstash 是為了處理記錄資料，但現在您可以處理任何類型的事件，包括 XML 或 JSON 格式的事件。

## 管線結構

Logstash 的運作方式是由您設定包含三個階段的管線：輸入、篩選和輸出。

每個階段會使用一個或多個外掛程式。Logstash 有超過 200 個內建外掛程式，因此您很可能找到所需的外掛程式。除了內建外掛程式，您也可以使用社群提供的外掛程式，甚至自行撰寫。

管線的結構如下：

```yml
input {
  input_plugin => {}
}

filter {
  filter_plugin => {}
}

output {
  output_plugin => {}
}
```

其中：

* `input` 同時接收來自多個來源的事件，例如記錄檔。Logstash 支援多種輸入外掛程式，可用於 TCP/UDP、檔案、syslog、Microsoft Windows EventLogs、`stdin`、HTTP 等。您也可以使用稱為 Beats 的開放原始碼輸入工具集合來收集事件。輸入外掛程式會將事件傳送至篩選器。
* `filter` 以各種方式剖析事件並豐富事件內容。Logstash 有大量篩選器外掛程式，可修改事件並將其傳送至輸出。例如，`grok` 篩選器會將非結構化事件剖析為欄位，而 `mutate` 篩選器會變更欄位。篩選器會依序執行。
* `output` 將篩選後的事件傳送至一個或多個目的地。Logstash 支援多種輸出外掛程式，可用於 OpenSearch、TCP/UDP、電子郵件、檔案、`stdout`、HTTP、Nagios 等目的地。

輸入和輸出階段都支援編解碼器，可在事件進入或離開管線時處理事件。
常用的編解碼器包括 `json` 和 `multiline`。`json` 編解碼器會處理 JSON 格式的資料，而 `multiline` 編解碼器會將多行事件合併為單行。

您也可以在管線組態中撰寫條件陳述式，在符合特定條件時執行某些動作。

## 安裝 Logstash

若要在 OpenSearch 上安裝 Logstash，請先在您的叢集上安裝 Logstash，再安裝 OpenSearch Logstash 外掛程式，如下列步驟所述。

### tar 封存檔

請確認您已安裝 [Java Development Kit（JDK）](https://www.oracle.com/java/technologies/javase-downloads.html) 8 或 11 版。

1. 從 [Logstash 下載頁面](https://www.elastic.co/downloads/logstash)下載 Logstash tar 封存檔。

2. 在終端機中前往下載的資料夾，並解壓縮檔案。請確認您的 Logstash 版本和平台與下載的版本和平台相符：

     ```bash
     tar -zxvf logstash-8.8.2-linux-x86_64.tar.gz
     ```
     {% include copy.html %}

3. 前往 `logstash-8.8.2` 目錄。

4. 使用下列命令安裝外掛程式：

     ```bash
     bin/logstash-plugin install logstash-output-opensearch
     ```
     {% include copy.html %}
  
   您應該會收到下列輸出：

     ```
     Validating logstash-output-opensearch
     Resolving mixin dependencies
     Updating mixin dependencies logstash-mixin-ecs_compatibility_support
     Bundler attempted to update logstash-mixin-ecs_compatibility_support but its version stayed the same
     Installing logstash-output-opensearch
     Installation successful
     ```

您可以將管線組態新增至 `config` 目錄。Logstash 會將外掛程式的所有資料儲存在 `data` 目錄中。`bin` 目錄包含用於啟動 Logstash 和管理外掛程式的二進位檔。

### Docker

您可以使用自訂 Dockerfile 建置 Logstash 映像檔，或使用標準 Logstash 映像檔。

#### 選項 1：使用自訂 Dockerfile（建議）

1. 建立自訂 Dockerfile，以建置包含必要 OpenSearch 外掛程式的 Logstash 映像檔：

    ```
    FROM logstash:<LATEST_VERSION>
    RUN bin/logstash-plugin install logstash-output-opensearch
    RUN bin/logstash-plugin install logstash-input-opensearch
    ```
    {% include copy.html %}

1. 建置映像檔：

    ```
    docker build -t logstash-with-opensearch-plugins .
    ```
    {% include copy.html %}

#### 選項 2：使用標準 Logstash 映像檔

1. 依照 [Logstash 下載頁面](https://www.elastic.co/downloads/logstash)所述，下載最新的 Logstash 映像檔。

    ```
    docker pull docker.elastic.co/logstash/logstash:8.8.2
    ```
    {% include copy.html %}

1. 建立 Docker 網路：

    ```
    docker network create test
    ```
    {% include copy.html %}

1. 使用此網路啟動 OpenSearch：

    ```
    docker run -p 9200:9200 -p 9600:9600 --name opensearch --net test -e "discovery.type=single-node" opensearchproject/opensearch:1.2.0
    ```
    {% include copy.html %}

1. 啟動 Logstash：

    ```
    docker run -it --rm --name logstash --net test opensearchproject/logstash-oss-with-opensearch-output-plugin:7.16.2 -e 'input { stdin { } } output {
      opensearch {
        hosts => ["https://opensearch:9200"]
        index => "opensearch-logstash-docker-%{+YYYY.MM.dd}"
        user => "admin"
        password => "admin"
        ssl => true
        ssl_certificate_verification => false
      }
    }'
    ```
    {% include copy.html %}

## 處理終端機中的文字

您可以定義管線，在 `stdin` 接聽事件，並在 `stdout` 輸出事件。`stdin` 和 `stdout` 指的是您執行 Logstash 的終端機。

若要在終端機中輸入一些文字，並在輸出中查看事件資料：

1. 使用 `-e` 引數，將管線組態直接傳遞至 Logstash 二進位檔。在此情況下，`stdin` 是輸入外掛程式，而 `stdout` 是輸出外掛程式：

    ```bash
    bin/logstash -e "input { stdin { } } output { stdout { } }"
    ```
    {% include copy.html %}

    新增 `—debug` 旗標，以查看更詳細的輸出。

2. 在您的終端機中輸入「hello world」。Logstash 會處理文字，並將其輸出回終端機：

    ```yml
    {
     "message" => "hello world",
     "host" => "a483e711a548.ant.amazon.com",
     "@timestamp" => 2021-05-30T05:15:56.816Z,
     "@version" => "1"
    }
    ```

    `message` 欄位包含您的原始輸入。當您未在本機執行 Logstash 時，`host` 欄位是 IP 位址。`@timestamp` 顯示事件處理時的日期和時間。Logstash 使用 `@version` 欄位進行內部處理。

3. 按下 `Ctrl + C` 以關閉 Logstash。

### 疑難排解

如果您已經有正在執行的 Logstash 程序，就會收到錯誤。若要修正此問題：

1. 從 `data` 目錄刪除 `.lock` 檔案：

    ```bash
    cd data
    rm -rf .lock
    ```
    {% include copy.html %}

2. 重新啟動 Logstash。

## 處理 JSON 或 HTTP 輸入並將其輸出至檔案

若要定義處理 JSON 請求的管線：

1. 用您喜歡的任何文字編輯器開啟 `config/pipeline.conf` 檔案。您可以用任何副檔名建立管線組態檔，`.conf` 副檔名是 Logstash 的慣例。新增 `json` 編解碼器以接受 JSON 作為輸入，並新增 `file` 外掛程式，將處理後的事件輸出至 `.txt` 檔案：

    ```json
    input {
      stdin {
        codec => json
      }
    }
    output {
      file {
        path => "output.txt"
      }
    }
    ```
    {% include copy.html %}

    若要處理來自檔案的輸入，請將輸入檔案新增至 `events-data` 目錄，然後在輸入時將其路徑傳遞給 `file` 外掛程式：

    ```json
    input {
      file {
        path => "events-data/input_data.log"
      }
    }
    ```
    {% include copy.html %}

2. 啟動 Logstash：

    ```bash
    bin/logstash -f config/pipeline.conf
    ```
    {% include copy.html %}

    `config/pipeline.conf` 是 `pipeline.conf` 檔案的相對路徑。您也可以使用絕對路徑。

3. 在終端機中新增 JSON 物件：

    ```json
    { "amount": 10, "quantity": 2}
    ```
    {% include copy.html %}

    此管線只會處理單行輸入。如果您貼上跨越多行的 JSON，就會收到錯誤。

4. 檢查 JSON 物件中的欄位是否已新增至 `output.txt` 檔案：

    ```bash
    cat output.txt
    ```
    {% include copy.html %}

    ```json
    {
      "@version": "1",
      "@timestamp": "2021-05-30T05:52:52.421Z",
      "host": "a483e711a548.ant.amazon.com",
      "amount": 10,
      "quantity": 2
    }
    ```

    如果您輸入一些無效的 JSON 作為輸入，就會看到 JSON 剖析錯誤。Logstash 不會捨棄無效的 JSON，因為您可能仍想對它做些處理。例如，您可以觸發電子郵件或傳送通知至 Slack 頻道。

若要定義處理 HTTP 請求的管線：

1. 使用 `http` 外掛程式，透過 HTTP 將事件傳送至 Logstash：

    ```json
    input {
      http {
        host => "127.0.0.1"
        port => 8080
      }
    }

    output {
      file {
        path => "output.txt"
      }
    }
    ```
    {% include copy.html %}

    如果您未指定任何選項，`http` 外掛程式會繫結至 `localhost` 並在連接埠 8080 上接聽。

2. 啟動 Logstash：

    ```bash
    bin/logstash -f config/pipeline.conf
    ```
    {% include copy.html %}

3. 使用 Postman 傳送 HTTP 請求。將 `Content-Type` 設為 HTTP 標頭，其值為 `application/json`：

    ```json
    PUT 127.0.0.1:8080
    {
      "amount": 10,
      "quantity": 2
    }
    ```
    {% include copy.html %}

    或者，您可以使用 `curl` 命令：

    ```bash
    curl -XPUT -H "Content-Type: application/json" -d ' {"amount": 7, "quantity": 3 }' http://localhost:8080 (http://localhost:8080/)
    ```
    {% include copy.html %}

    即使我們未將 `json` 外掛程式新增至輸入，管線組態仍可運作，因為 HTTP 外掛程式會根據 `Content-Type` 標頭自動套用適當的編解碼器。
    如果您指定值為 `applications/json`，Logstash 會將請求本文剖析為 JSON。

    `headers` 欄位包含 Logstash 收到的 HTTP 標頭：

    ```json
    {
      "host": "127.0.0.1",
      "quantity": "3",
      "amount": 10,
      "@timestamp": "2021-05-30T06:05:48.135Z",
      "headers": {
        "http_version": "HTTP/1.1",
        "request_method": "PUT",
        "http_user_agent": "PostmanRuntime/7.26.8",
        "connection": "keep-alive",
        "postman_token": "c6cd29cf-1b37-4420-8db3-9faec66b9e7e",
        "http_host": "127.0.0.1:8080",
        "cache_control": "no-cache",
        "request_path": "/",
        "content_type": "application/json",
        "http_accept": "*/*",
        "content_length": "41",
        "accept_encoding": "gzip, deflate, br"
      },
    "@version": "1"
    }
    ```


## 自動重新載入管線組態

您可以設定 Logstash 偵測管線組態檔或輸入記錄檔的任何變更，並自動重新載入組態。

`stdin` 外掛程式不支援自動重新載入。
{: .note }

1. 在輸入外掛程式中新增名為 `start_position` 的選項，其值為 `beginning`：

    ```json
    input {
      file {
        path => "/Users/<user>/Desktop/logstash7-12.1/events-data/input_file.log"
        start_position => "beginning"
      }
    }
    ```
    {% include copy.html %}

    Logstash 只會處理新增至輸入檔案的新事件，並忽略已處理過的事件，以避免在重新啟動時重複處理相同的事件。

    Logstash 會將其進度記錄在稱為 `sinceDB` 檔案的檔案中。Logstash 會為其監看的每個檔案建立一個 `sinceDB` 檔案。

2. 開啟 `sinceDB` 檔案，以檢查輸入檔案已處理多少：

    ```bash
    cd data/plugins/inputs/file/
    ls -al

    -rw-r--r--  1 user  staff   0 Jun 13 10:50 .sincedb_9e484f2a9e6c0d1bdfe6f23ac107ffc5

    cat .sincedb_9e484f2a9e6c0d1bdfe6f23ac107ffc5

    51575938 1 4 7727
    ```
    {% include copy.html %}

    `sinceDB` 檔案中的最後一個數字 (7727) 是上次已知已處理事件的位元組位移。

5. 若要從頭開始處理輸入檔案，請刪除 `sinceDB` 檔案：

    ```bash
    rm .sincedb_*
    ```
    {% include copy.html %}

2. 使用 `—-config.reload.automatic` 引數啟動 Logstash：

    ```bash
    bin/logstash -f config/pipeline.conf --config.reload.automatic
    ```
    {% include copy.html %}

    只有在您於管線組態檔結尾新增一行時，`reload` 選項才會重新載入。

    範例輸出：

    ```json
    {
       "message" => "216.243.171.38 - - [20/Sep/2017:19:11:52 +0200] \"GET /products/view/123 HTTP/1.1\" 200 12798 \"https://codingexplained.com/products\" \"Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)\"",
       "@version" => "1",
          "host" => "a483e711a548.ant.amazon.com",
          "path" => "/Users/kumarjao/Desktop/odfe1/logstash-7.12.1/events-data/input_file.log",
       "@timestamp" => 2021-06-13T18:03:30.423Z
    }
    {
       "message" => "91.59.108.75 - - [20/Sep/2017:20:11:43 +0200] \"GET /js/main.js HTTP/1.1\" 200 588 \"https://codingexplained.com/products/view/863\" \"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0\"",
      "@version" => "1",
          "host" => "a483e711a548.ant.amazon.com",
          "path" => "/Users/kumarjao/Desktop/odfe1/logstash-7.12.1/events-data/input_file.log",
    "@timestamp" => 2021-06-13T18:03:30.424Z
    }
    ```

7. 在輸入檔案中新增一行。
    - Logstash 會立即偵測到變更，並將新行處理為事件。

8. 變更 `pipeline.conf` 檔案。
    - Logstash 會立即偵測到變更，並重新載入修改後的管線。
