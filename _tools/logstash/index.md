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

Logstash 是一個開源的即時事件處理引擎，可從一或多個來源接收事件、加以處理，然後傳送至一或多個目的地。例如，您可以將網頁伺服器的存取記錄檔傳送至 Logstash，從每行記錄擷取欄位，再將產生的事件傳送至 OpenSearch。

將事件傳送至 Logstash 可讓事件處理與您的應用程式解耦。您的應用程式只需將事件傳送至 Logstash，不需要知道事件後續的處理方式。

Logstash 最初是為了處理記錄資料而設計，但它可以處理任何類型的事件，包括 XML 或 JSON 格式的事件。

若要將事件傳送至 OpenSearch，請安裝 [OpenSearch 輸出外掛程式](https://github.com/opensearch-project/logstash-output-opensearch)。若要從 OpenSearch 讀取資料至 Logstash，請安裝 [OpenSearch 輸入外掛程式](https://github.com/opensearch-project/logstash-input-opensearch)。

## 管線結構

Logstash 管線有三個階段：輸入、篩選與輸出。每個階段會使用一個或多個外掛程式。Logstash 內含超過 200 個外掛程式，您也可以安裝社群提供的外掛程式，或自行撰寫。

管線組態的結構如下：

```ruby
input {
  <input-plugin> {
    <setting> => <value>
  }
}

filter {
  <filter-plugin> {
    <setting> => <value>
  }
}

output {
  <output-plugin> {
    <setting> => <value>
  }
}
```

各階段執行下列工作：

- `input`：從一個或多個來源接收事件，例如記錄檔。輸入外掛程式包括 `tcp`、`udp`、`file`、`syslog`、`stdin` 與 `http`。您也可以使用 Beats 代理程式收集事件並傳送至 Logstash。
- `filter`：剖析並擴充事件。例如，`grok` 篩選器會將非結構化文字剖析為欄位，而 `mutate` 篩選器會修改欄位。篩選器會依其在組態中出現的順序執行。
- `output`：將處理後的事件傳送至一個或多個目的地，例如 OpenSearch、檔案、`stdout`、HTTP 端點、TCP 或 UDP 通訊端、電子郵件地址或 Nagios。

輸入與輸出可以使用編解碼器，在事件進入或離開管線時進行解碼或編碼。例如，`json` 編解碼器會剖析 JSON 格式的輸入，而 `multiline` 編解碼器會將多行合併為單一事件。

若只想將外掛程式套用至符合條件的事件，請使用條件陳述式。如需詳細資訊，請參閱[條件陳述式]({{site.url}}{{site.baseurl}}/tools/logstash/advanced-config/#conditional-statements)。

## 安裝 Logstash

若要安裝 Logstash，請先安裝 Logstash 發行版，再安裝 OpenSearch 外掛程式。下列指示使用 Logstash 的開放原始碼（OSS）發行版。

### 先決條件

安裝 Logstash 之前，請先檢閱 [Logstash 相容性對照表]({{site.url}}{{site.baseurl}}/tools/#compatibility-matrix-for-logstash)，並選擇與您的 OpenSearch 版本相容的 Logstash 版本。

### Tarball 壓縮檔

Logstash 內附 JDK，因此您不需要另外安裝 Java。

若要從 tarball 安裝 Logstash，請依照下列步驟操作：

1. 下載適用於您平台的 Logstash OSS tarball。在此範例中，版本為 8.19.23：

    ```bash
    curl -O https://artifacts.elastic.co/downloads/logstash/logstash-oss-8.19.23-linux-x86_64.tar.gz
    ```
    {% include copy.html %}

    其他平台請參閱 [下載 Logstash OSS](https://www.elastic.co/downloads/logstash-oss)。

1. 解壓縮檔案：

    ```bash
    tar -zxvf logstash-oss-8.19.23-linux-x86_64.tar.gz
    ```
    {% include copy.html %}

1. 切換至 Logstash 目錄：

    ```bash
    cd logstash-8.19.23
    ```
    {% include copy.html %}

1. 安裝 OpenSearch 輸出外掛程式：

    ```bash
    bin/logstash-plugin install logstash-output-opensearch
    ```
    {% include copy.html %}

    此命令會傳回下列輸出：

    ```
    Validating logstash-output-opensearch
    Resolving mixin dependencies
    Updating mixin dependencies logstash-mixin-ecs_compatibility_support
    Bundler attempted to update logstash-mixin-ecs_compatibility_support but its version stayed the same
    Installing logstash-output-opensearch
    Installation successful
    ```

1. 如果您打算從 OpenSearch 讀取資料，請安裝 OpenSearch 輸入外掛程式：

    ```bash
    bin/logstash-plugin install logstash-input-opensearch
    ```
    {% include copy.html %}

Logstash 目錄包含下列子目錄：

- `bin`：包含用於啟動 Logstash 及管理外掛程式的執行檔。
- `config`：包含 Logstash 的設定。您可以將管線組態檔存放在此目錄中。
- `data`：包含 Logstash 及其外掛程式在執行之間儲存的資料。

### Docker

Logstash Docker 映像檔並未包含 OpenSearch 外掛程式，因此您需要建置包含這些外掛程式的映像檔。

若要在 Docker 中執行 Logstash 與 OpenSearch，請依照下列步驟操作：

1. 建立名為 `Dockerfile` 的檔案，內容如下。在此範例中，版本為 8.19.23：

    ```
    FROM docker.elastic.co/logstash/logstash-oss:8.19.23
    RUN bin/logstash-plugin install logstash-output-opensearch
    RUN bin/logstash-plugin install logstash-input-opensearch
    ```
    {% include copy.html %}

1. 在包含 `Dockerfile` 的目錄中建置映像檔：

    ```bash
    docker build -t logstash-with-opensearch-plugins .
    ```
    {% include copy.html %}

1. 建立 Docker 網路，讓 Logstash 容器能夠連線至 OpenSearch 容器：

    ```bash
    docker network create opensearch-net
    ```
    {% include copy.html %}

1. 在此網路上啟動 OpenSearch。請將 `<admin-password>` 替換為 `admin` 使用者的高強度密碼：

    ```bash
    docker run -d -p 9200:9200 --name opensearch --net opensearch-net -e "discovery.type=single-node" -e "OPENSEARCH_INITIAL_ADMIN_PASSWORD=<admin-password>" opensearchproject/opensearch:latest
    ```
    {% include copy.html %}

1. 在相同網路上啟動 Logstash。下列管線會從終端機讀取事件，並將其傳送至 OpenSearch：

    ```bash
    docker run -it --rm --name logstash --net opensearch-net logstash-with-opensearch-plugins -e 'input { stdin { } } output {
      opensearch {
        hosts => ["https://opensearch:9200"]
        index => "opensearch-logstash-docker-%{+YYYY.MM.dd}"
        user => "admin"
        password => "<admin-password>"
        ssl => true
        ssl_certificate_verification => false
      }
    }'
    ```
    {% include copy.html %}

    OpenSearch 示範組態使用自簽憑證，因此此範例會停用憑證驗證。在正式環境中，請改為在 `cacert` 設定中提供憑證授權單位檔案。如需詳細資訊，請參閱[設定 OpenSearch 輸出外掛程式]({{site.url}}{{site.baseurl}}/tools/logstash/ship-to-opensearch/#configuring-the-opensearch-output-plugin)。
    {: .warning }

1. 當 Logstash 記錄 `Pipeline started` 時，請在終端機中輸入一些文字，例如 `hello world`。然後按下 `Ctrl+C` 以停止 Logstash。

1. 確認 Logstash 已建立索引：

    ```bash
    curl -k -u 'admin:<admin-password>' "https://localhost:9200/_cat/indices/opensearch-logstash-docker-*?v"
    ```
    {% include copy.html %}

    回應會列出該索引及其文件數量：

    ```bash
    health status index                                 uuid                   pri rep docs.count docs.deleted store.size pri.store.size
    yellow open   opensearch-logstash-docker-2026.10.16 6WKKD-CuTiqV7vIu8puyaA   1   1          1            0      6.9kb          6.9kb
    ```

## 處理來自終端機的文字

以下各節中的範例使用 tarball 安裝方式，並從 Logstash 目錄執行。`stdin` 輸入會從執行 Logstash 的終端機讀取事件，而 `stdout` 輸出會將事件列印到同一個終端機。

若要處理來自終端機的文字，請依照下列步驟操作：

1. 使用 `-e` 引數將管線組態傳遞給 Logstash。在此管線中，`stdin` 是輸入外掛程式，`stdout` 是輸出外掛程式：

    ```bash
    bin/logstash -e "input { stdin { } } output { stdout { } }"
    ```
    {% include copy.html %}

    若要取得更詳細的記錄檔，請加入 `--log.level=debug` 引數。

1. 當 Logstash 記錄 `Pipeline started` 時，請在終端機中輸入 `hello world`。Logstash 會處理該文字並列印產生的事件：

    ```
    {
             "event" => {
            "original" => "hello world"
        },
           "message" => "hello world",
          "@version" => "1",
        "@timestamp" => 2026-10-16T17:55:22.401258801Z,
              "host" => {
            "hostname" => "my-host"
        }
    }
    ```

    該事件包含下列欄位：

    - `message`：您輸入的文字。
    - `event.original`：原始、未經修改的輸入。
    - `host.hostname`：執行 Logstash 的主機名稱。
    - `@timestamp`：Logstash 處理該事件的時間。
    - `@version`：事件格式版本，供 Logstash 內部使用。

1. 按下 `Ctrl+C` 以停止 Logstash。

### 疑難排解

Logstash 在執行期間會鎖定其 `data` 目錄。如果另一個 Logstash 程序已在使用該目錄，Logstash 將無法啟動，並記錄以下訊息：

```
Logstash could not be started because there is already another instance using the configured data directory.
```

若要解決此問題，請停止另一個 Logstash 程序。若要同時執行兩個 Logstash 程序，請使用 `--path.data` 引數，以不同的資料目錄啟動第二個程序。

## 處理 JSON 輸入並將其寫入檔案

若要定義處理 JSON 輸入的管線，請依照下列步驟操作：

1. 建立名為 `config/pipeline.conf` 的檔案，並使用下列組態。`json` 編解碼器會將每一行輸入解析為 JSON，而 `file` 輸出會將處理後的事件寫入 `output.txt` 檔案：

    ```ruby
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

    您可以為管線組態檔指定任何名稱與副檔名。依照慣例，管線組態檔會使用 `.conf` 副檔名。

1. 啟動 Logstash：

    ```bash
    bin/logstash -f config/pipeline.conf
    ```
    {% include copy.html %}

    `config/pipeline.conf` 路徑是相對於 Logstash 目錄。您也可以提供絕對路徑。

1. 在終端機中以單行輸入 JSON 物件：

    ```json
    { "amount": 10, "quantity": 2 }
    ```
    {% include copy.html %}

    `json` 編解碼器會分別解析每一行。如果您輸入無效的 JSON，例如跨越多行的 JSON 物件，Logstash 將無法解析，並會為該事件加上 `_jsonparsefailure` 標籤。Logstash 不會捨棄解析失敗的事件，因此您可以另行處理這些事件，例如傳送電子郵件或傳送通知至 Slack 頻道。

1. 在另一個終端機中，檢視 Logstash 目錄中的 `output.txt` 檔案：

    ```bash
    cat output.txt
    ```
    {% include copy.html %}

    該檔案包含該事件，包括解析後的 `amount` 與 `quantity` 欄位：

    ```json
    {"host":{"hostname":"my-host"},"@version":"1","amount":10,"quantity":2,"@timestamp":"2026-10-16T17:56:05.320077410Z","event":{"original":"{ \"amount\": 10, \"quantity\": 2 }\n"}}
    ```

若要從檔案而非終端機讀取事件，請使用 `file` 輸入外掛程式。`file` 輸入需要絕對路徑：

```ruby
input {
  file {
    path => "/path/to/logstash/events-data/input_data.log"
  }
}
```
{% include copy.html %}

## 處理 HTTP 輸入

若要定義透過 HTTP 接收事件的管線，請依照下列步驟操作：

1. 將 `config/pipeline.conf` 的內容替換為以下組態。`http` 輸入會在連接埠 8080 上監聽 HTTP 請求：

    ```ruby
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

    如果您未指定 `host` 與 `port` 設定，`http` 輸入會在連接埠 8080 上監聽所有網路介面 (`0.0.0.0`)。

1. 啟動 Logstash：

    ```bash
    bin/logstash -f config/pipeline.conf
    ```
    {% include copy.html %}

1. 在另一個終端機中，傳送一個包含 JSON 本文的 HTTP 請求：

    ```bash
    curl -XPUT -H "Content-Type: application/json" -d '{"amount": 7, "quantity": 3}' http://localhost:8080
    ```
    {% include copy.html %}

    Logstash 會傳回 `ok`。

`http` 輸入會根據 `Content-Type` 標頭選擇編解碼器。由於此請求的 `Content-Type` 為 `application/json`，即使管線未指定 `json` 編解碼器，Logstash 也會將請求本文剖析為 JSON。如果 `Content-Type` 不是 `application/json`，Logstash 會將請求本文以文字形式儲存在 `message` 欄位中。

Logstash 會將請求的相關資訊加入事件中。以下事件以 `stdout` 輸出所列印的格式顯示這些資訊：

```
{
      "@version" => "1",
    "@timestamp" => 2026-10-16T17:57:09.851542204Z,
         "event" => {
        "original" => "{\"amount\": 7, \"quantity\": 3}"
    },
          "host" => {
        "ip" => "127.0.0.1"
    },
    "user_agent" => {
        "original" => "curl/8.7.1"
    },
          "http" => {
        "request" => {
                 "body" => {
                "bytes" => "28"
            },
            "mime_type" => "application/json"
        },
        "version" => "HTTP/1.1",
         "method" => "PUT"
    },
           "url" => {
          "port" => 8080,
          "path" => "/",
        "domain" => "localhost"
    },
        "amount" => 7,
      "quantity" => 3
}
```

## 自動重新載入管線組態

Logstash 可以偵測管線組態檔案的變更，並在不重新啟動的情況下重新載入管線。

`stdin` 輸入不支援自動重新載入。
{: .note }

若要為從檔案讀取的管線設定自動重新載入，請依照下列步驟操作：

1. 在 Logstash 目錄中建立名為 `events-data/input_file.log` 的輸入檔案，並在其中新增一行文字。

1. 將 `config/pipeline.conf` 的內容替換為下列組態。將 `<path-to-logstash>` 替換為您的 Logstash 目錄絕對路徑：

    ```ruby
    input {
      file {
        path => "<path-to-logstash>/events-data/input_file.log"
        start_position => "beginning"
      }
    }

    output {
      stdout { }
    }
    ```
    {% include copy.html %}

    依預設，`file` 輸入只會讀取 Logstash 啟動後新增至檔案的行。將 `start_position` 設為 `beginning`，可讓 Logstash 在第一次處理該檔案時從頭開始讀取。

1. 使用 `--config.reload.automatic` 引數啟動 Logstash：

    ```bash
    bin/logstash -f config/pipeline.conf --config.reload.automatic
    ```
    {% include copy.html %}

    Logstash 會為輸入檔案中的每一行印出一個事件。

1. 在輸入檔案中新增一行。Logstash 會偵測到變更，並將新增的行作為事件處理。

1. 變更 `config/pipeline.conf` 檔案，例如在 `stdout` 輸出中新增 `codec => rubydebug`。Logstash 會偵測到變更、記錄 `Reloading pipeline`，並套用新的組態。

為避免重複處理相同的行，`file` 輸入會將其讀取之每個檔案的位置記錄在 `sincedb` 檔案中。Logstash 會將 `sincedb` 檔案儲存在 `data/plugins/inputs/file` 目錄中：

```bash
cat data/plugins/inputs/file/.sincedb_*
```
{% include copy.html %}

`sincedb` 檔案中的每一行對應一個輸入檔案，並包含該檔案的 inode 編號、主裝置與次裝置編號、Logstash 已讀取該檔案的位元組位移、最後更新時間，以及檔案路徑：

```
51956745 0 66305 29 1792174306.332788 /opt/logstash/events-data/input_file.log
```

若要從頭重新處理輸入檔案，請停止 Logstash、刪除 `sincedb` 檔案，然後重新啟動 Logstash：

```bash
rm data/plugins/inputs/file/.sincedb_*
```
{% include copy.html %}
