---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "將事件傳送至 OpenSearch"
parent: Logstash
nav_order: 220
redirect_from:
 - /clients/logstash/ship-to-opensearch/
---

# 將事件傳送至 OpenSearch

您可以將 Logstash 事件傳送至 OpenSearch 叢集，然後使用 OpenSearch Dashboards 將事件視覺化。

請確認您已安裝 [Logstash]({{site.url}}{{site.baseurl}}/tools/logstash/index#install-logstash)、[OpenSearch]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/index/) 與 [OpenSearch Dashboards]({{site.url}}{{site.baseurl}}/install-and-configure/install-dashboards/index/)。
{: .note }

## OpenSearch output 外掛程式

若要執行 OpenSearch output 外掛程式，請在您的 `pipeline.conf` 檔案中加入以下組態：

```yml
output {
  opensearch {
    hosts       => "https://localhost:9200"
    user        => "admin"
    password    => "admin"
    index       => "logstash-logs-%{+YYYY.MM.dd}"
    ssl_certificate_verification => false
  }
}
```

## 範例逐步解說

以下逐步解說示範如何傳送 Logstash 事件的範例。

1.  開啟 `config/pipeline.conf` 檔案並加入以下組態：

    ```yml
    input {
      stdin {
        codec => json
      }
    }

    output {
      opensearch {
        hosts       => "https://localhost:9200"
        user        => "admin"
        password    => "admin"
        index       => "logstash-logs-%{+YYYY.MM.dd}"
        ssl_certificate_verification => false
      }
    }
    ```

此 Logstash 管線透過終端機接受 JSON 輸入，並將事件傳送至在本機執行的 OpenSearch 叢集。Logstash 會依照 `logstash-logs-%{+YYYY.MM.dd}` 命名慣例將事件寫入索引。

2. 啟動 Logstash：

    ```bash
    $ bin/logstash -f config/pipeline.conf --config.reload.automatic
    ```

    `config/pipeline.conf` 是 `pipeline.conf` 檔案的相對路徑。您也可以使用絕對路徑。

3. 在終端機中加入 JSON 物件：

    ```json
    { "amount": 10, "quantity": 2}
    ```

4. 啟動 OpenSearch Dashboards 並選擇 **Dev Tools**：

    ```json
    GET _cat/indices?v

    health | status | index | uuid | pri | rep | docs.count | docs.deleted | store.size | pri.store.size
    green | open | logstash-logs-2021.07.01 | iuh648LYSnmQrkGf70pplA | 1 | 1 | 1 | 0 | 10.3kb | 5.1kb
    ```

## 在 Output 外掛程式中加入不同的驗證機制

除了現有的驗證機制之外，您可以使用 `auth_type` 設定加入新的驗證機制，如下列範例組態所示：

```yml
output {    
    opensearch {        
          hosts  => ["https://hostname:port"]     
          auth_type => {            
              type => 'basic'           
              user => 'admin'           
              password => 'admin'           
          }             
          index => "logstash-logs-%{+YYYY.MM.dd}"       
   }            
}               
```
### auth_type 內的參數

`auth_type` 設定支援下列參數：

- `type` (字串)：驗證類型。
- `user`：使用者名稱。
- `password`：用於基本驗證的密碼。

## AWS IAM 驗證的組態

若要使用 `aws_iam` 驗證執行 Logstash Output OpenSearch 外掛程式，請加入以下組態：

```yml
output {        
   opensearch {     
          hosts => ["https://hostname:port"]              
          auth_type => {    
              type => 'aws_iam'     
              aws_access_key_id => 'ACCESS_KEY'     
              aws_secret_access_key => 'SECRET_KEY'     
              region => 'us-west-2'    
              service_name => 'es'     
          }         
          index  => "logstash-logs-%{+YYYY.MM.dd}"      
   }            
}
```

### 必要參數

- `hosts` (字串陣列)：`AmazonOpensearchService` 網域端點與連接埠號碼。
- `auth_type` (JSON 物件)：驗證設定。
    - `type` (字串)："aws_iam"。
    - `aws_access_key_id` (字串)：AWS 存取金鑰。
    - `aws_secret_access_key` (字串)：AWS 私密存取金鑰。
    - `region` (字串，:default => "us-east-1")：網域所在的區域。
- port (字串)：AmazonOpensearchService 在連接埠 443 上監聽 `HTTPS`。
- protocol (字串)：用於連線的通訊協定。對於 `AmazonOpensearchService`，通訊協定為 `https`。

### 選用參數

- `template` (路徑)：您可以在此設定自己的範本路徑。若未指定範本，外掛程式會使用預設範本。
- `template_name` (字串，default => `logstash`)：定義範本在 OpenSearch 內部的命名方式。
- `service_name` (字串)：定義用於 `aws_iam` 驗證的服務名稱。
- `legacy_template` (布林值，default => `true`)：選取 OpenSearch 範本 API。當為 `true` 時，使用衍生自 `_template` API 的舊版範本。當為 `false` 時，使用 `index_template` API。
- `default_server_major_version` (數字)：當無法從 OpenSearch 根 URL 取得時所要使用的 OpenSearch 伺服器主要版本。若未設定，當無法取得版本時，外掛程式會擲回例外狀況。
- `target_bulk_bytes` (數字)：緩衝區的最大位元組數。達到上限時，Logstash 會將資料排清至 OpenSearch。當大量請求對 OpenSearch 叢集而言過大，且叢集傳回 `429` 錯誤時，此設定很有用。

### 憑證解析邏輯

下列清單提供憑證解析邏輯的詳細資訊：

- 使用者在組態中傳遞 `aws_access_key_id` 與 `aws_secret_access_key`。
- 建議使用環境變數，例如 `AWS_ACCESS_KEY_ID` 與 `AWS_SECRET_ACCESS_KEY`，因為除了 `.NET` 之外，所有 AWS SDK 與 CLI 都能識別這些變數。您也可以使用 Java SDK 能識別的 `AWS_ACCESS_KEY` 與 `AWS_SECRET_KEY`。
- 位於 `~/.aws/credentials` 目錄中的憑證設定檔，由所有 AWS SDK 與 AWS CLI 共用。
- 執行個體設定檔憑證透過 Amazon EC2 中繼資料服務傳遞。

## 資料串流

OpenSearch output 外掛程式可以將時間序列資料集 (例如記錄檔、事件與指標) 以及非時間序列資料儲存在 OpenSearch 中。
建議使用資料串流將時間序列資料集 (例如記錄檔、指標與事件) 編製索引至 OpenSearch。

若要進一步了解資料串流，請參閱[資料串流文件]({{site.url}}{{site.baseurl}}/opensearch/data-streams/)。

若要透過 Logstash 將資料匯入資料串流，請建立資料串流、指定資料串流的名稱，並將 `action` 設定設為 `create`，如下列範例組態所示：

```yml
output {    
    opensearch {        
          hosts  => ["https://hostname:port"]     
          auth_type => {            
              type => 'basic'           
              user => 'admin'           
              password => 'admin'           
          }
          index => "my-data-stream"
          action => "create"
   }            
}               
```
