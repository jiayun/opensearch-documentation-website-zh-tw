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

使用 [OpenSearch 輸出外掛程式](https://github.com/opensearch-project/logstash-output-opensearch)將 Logstash 事件傳送至 OpenSearch 叢集。接著，您可以在 OpenSearch 中搜尋這些事件，並在 OpenSearch Dashboards 中將其視覺化。

開始之前，請安裝 [Logstash 和 OpenSearch 輸出外掛程式]({{site.url}}{{site.baseurl}}/tools/logstash/index/#installing-logstash)、[OpenSearch]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/index/)，並視需要安裝 [OpenSearch Dashboards]({{site.url}}{{site.baseurl}}/install-and-configure/install-dashboards/index/)。

## 設定 OpenSearch 輸出外掛程式

若要將事件傳送至 OpenSearch，請將 `opensearch` 外掛程式新增至管線組態檔案的 `output` 區段。將 `<admin-password>` 替換為 `admin` 使用者的密碼，並將 `<path-to-root-ca>` 替換為簽署 OpenSearch 節點憑證的憑證授權單位檔案路徑：

```ruby
output {
  opensearch {
    hosts    => ["https://localhost:9200"]
    user     => "admin"
    password => "<admin-password>"
    index    => "logstash-logs-%{+YYYY.MM.dd}"
    ssl      => true
    cacert   => "<path-to-root-ca>"
  }
}
```
{% include copy.html %}

`index` 設定使用 `%{+YYYY.MM.dd}` 日期模式，因此 Logstash 會將每天的事件寫入各自的索引，例如 `logstash-logs-2026.10.16`。日期取自每個事件的 `@timestamp` 欄位。

如果您正在使用示範安全性組態的叢集上進行測試，而該組態使用自我簽署憑證，您可以將 `cacert` 設定替換為 `ssl_certificate_verification => false`。請勿在正式環境中停用憑證驗證。
{: .warning }

## 設定 TLS

當 `hosts` 包含 `https://` URL 時，此外掛程式會透過 TLS 連線至 OpenSearch，並驗證 OpenSearch 節點憑證。請以下列任一方式提供簽署節點憑證的憑證授權單位 (CA)：

- 將 `cacert` 設為 PEM 格式 CA 憑證的路徑，如前述範例所示。
- 將 `truststore` 設為包含 CA 憑證的 Java KeyStore (JKS) 檔案路徑，並將 `truststore_password` 設為信任儲存庫密碼。

您無法同時指定 `cacert` 與 `truststore`。

### 使用用戶端憑證進行驗證

如果 OpenSearch 已設定為使用[用戶端憑證驗證]({{site.url}}{{site.baseurl}}/security/authentication-backends/client-auth/)，Logstash 可以向 OpenSearch 出示用戶端憑證。請將 `tls_certificate` 設為 PEM 格式用戶端憑證的路徑，並將 `tls_key` 設為其私密金鑰的路徑。您必須同時指定這兩項設定：

```ruby
output {
  opensearch {
    hosts           => ["https://localhost:9200"]
    index           => "logstash-logs-%{+YYYY.MM.dd}"
    ssl             => true
    cacert          => "<path-to-root-ca>"
    tls_certificate => "<path-to-client-cert>"
    tls_key         => "<path-to-client-key>"
  }
}
```
{% include copy.html %}

私密金鑰必須是 PKCS #8 格式且未加密的 PEM 檔案，其開頭為 `-----BEGIN PRIVATE KEY-----`。開頭為 `-----BEGIN RSA PRIVATE KEY-----` 的 PKCS #1 格式金鑰會遭到拒絕。若要轉換 PKCS #1 金鑰，請執行下列命令：

```bash
openssl pkcs8 -topk8 -nocrypt -in <client-key> -out <client-key-pkcs8>
```
{% include copy.html %}

或者，您也可以將用戶端憑證和私密金鑰儲存在金鑰儲存區（keystore）中。請將 `keystore` 設為 JKS 或 PKCS #12（`.p12`）檔案的路徑，並將 `keystore_password` 設為金鑰儲存區的密碼。

Security 外掛程式會根據憑證的辨別名稱（DN）將用戶端憑證對應至使用者。此範例省略了 `user` 和 `password` 設定，因此 OpenSearch 僅使用憑證來驗證 Logstash。

## 範例：將 JSON 事件傳送至 OpenSearch

若要將您在終端機中輸入的事件傳送至 OpenSearch，請依照下列步驟操作：

1. 在 Logstash 目錄中建立名為 `config/pipeline.conf` 的檔案，並使用下列組態：

    ```ruby
    input {
      stdin {
        codec => json
      }
    }

    output {
      opensearch {
        hosts    => ["https://localhost:9200"]
        user     => "admin"
        password => "<admin-password>"
        index    => "logstash-logs-%{+YYYY.MM.dd}"
        ssl      => true
        ssl_certificate_verification => false
      }
    }
    ```
    {% include copy.html %}

    此管線會接受來自終端機的 JSON 輸入，並將事件寫入在 `localhost` 上執行的 OpenSearch 叢集中的 `logstash-logs-%{+YYYY.MM.dd}` 索引。

1. 啟動 Logstash：

    ```bash
    bin/logstash -f config/pipeline.conf
    ```
    {% include copy.html %}

1. 當 Logstash 記錄 `Pipeline started` 時，請在終端機中以單行輸入 JSON 物件：

    ```json
    { "amount": 10, "quantity": 2 }
    ```
    {% include copy.html %}

1. 確認 Logstash 已建立索引。在 OpenSearch Dashboards 中，前往 **Dev Tools** 並傳送下列請求：

    ```json
    GET _cat/indices/logstash-logs-*?v
    ```
    {% include copy-curl.html %}

    回應會列出索引及其文件數量：

    ```
    health status index                    uuid                   pri rep docs.count docs.deleted store.size pri.store.size
    yellow open   logstash-logs-2026.10.16 iuh648LYSnmQrkGf70pplA   1   1          1            0      5.2kb          5.2kb
    ```

## 驗證

OpenSearch 輸出外掛程式支援基本驗證和 AWS Identity and Access Management（IAM）驗證。

### 基本驗證

若要使用基本驗證，請提供 `user` 和 `password` 設定，如前述範例所示。您也可以在 `auth_type` 設定中指定認證資訊：

```ruby
output {
  opensearch {
    hosts => ["https://<hostname>:<port>"]
    auth_type => {
      type => "basic"
      user => "admin"
      password => "<admin-password>"
    }
    index => "logstash-logs-%{+YYYY.MM.dd}"
  }
}
```
{% include copy.html %}

下表列出基本驗證的 `auth_type` 設定。

設定 | 資料類型 | 說明
:--- | :--- | :---
`type` | 字串 | 驗證類型。設為 `basic`。
`user` | 字串 | 使用者名稱。
`password` | 字串 | 密碼。

### AWS IAM 驗證

若要使用 AWS IAM 驗證將事件傳送至 Amazon OpenSearch Service 網域，請在 `auth_type` 設定中將 `type` 設為 `aws_iam`。外掛程式會使用 AWS Signature Version 4 簽署每個請求：

```ruby
output {
  opensearch {
    hosts => ["https://<domain-endpoint>:443"]
    auth_type => {
      type => "aws_iam"
      region => "us-west-2"
      service_name => "es"
    }
    index => "logstash-logs-%{+YYYY.MM.dd}"
  }
}
```
{% include copy.html %}

將 `<domain-endpoint>` 替換為網域端點，不含 `https://` 前綴。Amazon OpenSearch Service 網域會透過連接埠 443 上的 HTTPS 接受請求。網域的存取政策必須允許 Logstash 使用的 IAM 身分將 HTTP 請求傳送至該網域。

下表列出 AWS IAM 驗證的 `auth_type` 設定。

設定 | 資料類型 | 說明
:--- | :--- | :---
`type` | 字串 | 驗證類型。設為 `aws_iam`。必要。
`region` | 字串 | 網域所在的 AWS 區域。預設為 `us-east-1`。如果網域位於其他區域，您必須設定此值。
`service_name` | 字串 | 用於簽署請求的服務名稱。預設為 `es`。
`aws_access_key_id` | 字串 | AWS 存取金鑰 ID。如果未指定，外掛程式會依照[認證資訊解析](#credential-resolution)中的說明解析認證資訊。
`aws_secret_access_key` | 字串 | AWS 私密存取金鑰。
`session_token` | 字串 | 工作階段權杖。當 `aws_access_key_id` 和 `aws_secret_access_key` 包含臨時認證資訊（例如從 AWS Security Token Service（AWS STS）取得的認證資訊）時，此項為必要。
`profile` | 字串 | 要使用的 AWS 認證資訊檔案中的設定檔。預設為 `default`。

#### 認證資訊解析

如果您未在 `auth_type` 設定中指定認證資訊，外掛程式會依序在下列位置尋找，並使用最先找到的認證資訊：

1. `auth_type` 設定中的 `aws_access_key_id` 和 `aws_secret_access_key` 設定。
1. `AWS_ACCESS_KEY_ID`、`AWS_SECRET_ACCESS_KEY` 和 `AWS_SESSION_TOKEN` 環境變數。外掛程式也會辨識 `AWS_ACCESS_KEY` 和 `AWS_SECRET_KEY` 環境變數。
1. 預設位置（`~/.aws/credentials`）中的認證資訊檔案。
1. Amazon EC2 執行個體中繼資料服務提供的執行個體設定檔認證資訊。

若要避免將認證資訊儲存在管線組態檔案中，請使用環境變數；如果 Logstash 在 Amazon EC2 上執行，則可使用執行個體設定檔。

## 選用設定

下表列出 OpenSearch 輸出外掛程式的選用設定。

設定 | 資料類型 | 說明
:--- | :--- | :---
`cacert` | 字串 | 用於驗證 OpenSearch 節點憑證的憑證授權單位檔案路徑。
`ssl_certificate_verification` | 布林值 | 是否驗證 OpenSearch 節點憑證。預設為 `true`。
`truststore` | 字串 | 包含憑證授權單位（用於驗證 OpenSearch 節點憑證）的 JKS 信任儲存庫路徑。不能與 `cacert` 一起使用。
`truststore_password` | 字串 | 信任儲存庫密碼。
`tls_certificate` | 字串 | PEM 格式的用戶端憑證路徑。需要 `tls_key`。請參閱[使用用戶端憑證進行驗證](#authenticating-using-a-client-certificate)。
`tls_key` | 字串 | 用戶端憑證私密金鑰的路徑，為 PKCS #8 格式的未加密 PEM 檔案。需要 `tls_certificate`。
`keystore` | 字串 | 包含用戶端憑證及其私密金鑰的 JKS 或 PKCS #12 金鑰儲存庫路徑。
`keystore_password` | 字串 | 金鑰儲存庫密碼。
`template` | 字串 | 自訂索引範本檔案的路徑。若未指定，外掛程式會使用其預設範本。
`template_name` | 字串 | OpenSearch 中索引範本的名稱。
`legacy_template` | 布林值 | 是否使用舊版 `_template` API 安裝索引範本。若為 `false`，外掛程式會使用 `_index_template` API。預設為 `true`。
`manage_template` | 布林值 | 外掛程式是否在 OpenSearch 中安裝索引範本。預設為 `true`。
`default_server_major_version` | 整數 | 當外掛程式無法從叢集的根端點取得版本時，要使用的 OpenSearch 主要版本。若未指定且無法取得版本，外掛程式會失敗。
`target_bulk_bytes` | 整數 | 大量請求的大小上限（以位元組為單位）。當緩衝的事件達到此大小時，Logstash 會將其傳送至 OpenSearch。若 OpenSearch 因大量請求過大而以 `429` 狀態碼拒絕，請降低此值。

## 資料串流

對於僅附加的時間序列資料，例如記錄資料、事件和指標，建議使用資料串流。如需詳細資訊，請參閱[資料串流]({{site.url}}{{site.baseurl}}/im-plugin/data-streams/)。

若要將事件傳送至資料串流，請先在 OpenSearch 中建立資料串流。接著將 `index` 設為資料串流名稱，並將 `action` 設為 `create`：

```ruby
output {
  opensearch {
    hosts => ["https://<hostname>:<port>"]
    auth_type => {
      type => "basic"
      user => "admin"
      password => "<admin-password>"
    }
    index => "my-data-stream"
    action => "create"
  }
}
```
{% include copy.html %}

資料串流僅接受 `create` 操作。如果您未將 `action` 設為 `create`，OpenSearch 會以 `400` 狀態碼拒絕事件。
