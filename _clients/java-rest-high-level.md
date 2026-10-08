---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "Java 高階 REST 用戶端（已棄用）"
nav_order: 190
---

# Java 高階 REST 用戶端

OpenSearch Java 高階 REST 用戶端已棄用，未來版本將移除對其的支援。我們建議改用 [Java 用戶端]({{site.url}}{{site.baseurl}}/clients/java/)。
{: .warning}

OpenSearch Java 高階 REST 用戶端可讓您透過 Java 方法和資料結構與 OpenSearch 叢集和索引互動，而不必使用 HTTP 方法和 JSON。

## 設定

若要開始使用 OpenSearch Java 高階 REST 用戶端，請確認您專案的 `pom.xml` 檔案中包含下列相依性：

```
<dependency>
  <groupId>org.opensearch.client</groupId>
  <artifactId>opensearch-rest-high-level-client</artifactId>
  <version>{{site.opensearch_version}}</version>
</dependency>
```

現在您可以啟動 OpenSearch 叢集。請使用與您的 OpenSearch 版本相符的高階 REST 用戶端版本。

## 安全性

在 Java 應用程式中使用 REST 用戶端之前，您必須設定應用程式的信任存放區 (truststore)，才能連線至 Security 外掛程式。如果您使用自我簽署憑證或示範組態，可以使用下列命令建立自訂信任存放區，並加入根憑證授權單位憑證。

如果您使用的是受信任憑證授權單位 (CA) 所核發的憑證，則不需要設定信任存放區。

```bash
keytool -importcert -file <path-to-root-ca-cert> -alias <alias> -keystore <truststore-name>
```

現在您可以將 Java 用戶端指向該信任存放區，並設定可存取安全叢集的基本驗證認證資訊（作法請參閱下方的範例程式碼）。

如果您在設定安全性時遇到問題，請參閱 [TLS 疑難排解]({{site.url}}{{site.baseurl}}/security/configuration/troubleshoot-tls/)。

## 範例程式

此程式碼範例使用 `admin` 使用者。請將 `<custom-admin-password>` 替換為您安裝 OpenSearch 時設定的管理員密碼。請將 `/full/path/to/keystore` 替換為您信任存放區的路徑，並將 `password-to-keystore` 替換為信任存放區的密碼。

```java
import org.apache.hc.client5.http.auth.AuthScope;
import org.apache.hc.client5.http.auth.UsernamePasswordCredentials;
import org.apache.hc.client5.http.impl.async.HttpAsyncClientBuilder;
import org.apache.hc.client5.http.impl.auth.BasicCredentialsProvider;
import org.apache.hc.core5.http.HttpHost;
import org.opensearch.action.admin.indices.delete.DeleteIndexRequest;
import org.opensearch.action.delete.DeleteRequest;
import org.opensearch.action.delete.DeleteResponse;
import org.opensearch.action.get.GetRequest;
import org.opensearch.action.get.GetResponse;
import org.opensearch.action.index.IndexRequest;
import org.opensearch.action.index.IndexResponse;
import org.opensearch.action.support.clustermanager.AcknowledgedResponse;
import org.opensearch.client.RequestOptions;
import org.opensearch.client.RestClient;
import org.opensearch.client.RestClientBuilder;
import org.opensearch.client.RestHighLevelClient;
import org.opensearch.client.indices.CreateIndexRequest;
import org.opensearch.client.indices.CreateIndexResponse;
import org.opensearch.common.settings.Settings;

import java.io.IOException;
import java.util.HashMap;

public class RESTClientSample {

  public static void main(String[] args) throws IOException {

    //Point to keystore with appropriate certificates for security.
    System.setProperty("javax.net.ssl.trustStore", "/full/path/to/keystore");
    System.setProperty("javax.net.ssl.trustStorePassword", "password-to-keystore");

    //Establish credentials to use basic authentication.
    //Only for demo purposes. Don't specify your credentials in code.
    final HttpHost host = new HttpHost("https", "localhost", 9200);
    final BasicCredentialsProvider credentialsProvider = new BasicCredentialsProvider();

    credentialsProvider.setCredentials(new AuthScope(host),
      new UsernamePasswordCredentials("admin", "<custom-admin-password>".toCharArray()));

    //Create a client.
    RestClientBuilder builder = RestClient.builder(host)
      .setHttpClientConfigCallback(new RestClientBuilder.HttpClientConfigCallback() {
        @Override
        public HttpAsyncClientBuilder customizeHttpClient(HttpAsyncClientBuilder httpClientBuilder) {
          return httpClientBuilder.setDefaultCredentialsProvider(credentialsProvider);
            }
          });
    RestHighLevelClient client = new RestHighLevelClient(builder);

    //Create a non-default index with custom settings and mappings.
    CreateIndexRequest createIndexRequest = new CreateIndexRequest("custom-index");

    createIndexRequest.settings(Settings.builder() //Specify in the settings how many shards you want in the index.
      .put("index.number_of_shards", 4)
      .put("index.number_of_replicas", 3)
      );
    //Create a set of maps for the index's mappings.
    HashMap<String, String> typeMapping = new HashMap<String,String>();
    typeMapping.put("type", "integer");
    HashMap<String, Object> ageMapping = new HashMap<String, Object>();
    ageMapping.put("age", typeMapping);
    HashMap<String, Object> mapping = new HashMap<String, Object>();
    mapping.put("properties", ageMapping);
    createIndexRequest.mapping(mapping);
    CreateIndexResponse createIndexResponse = client.indices().create(createIndexRequest, RequestOptions.DEFAULT);

    //Adding data to the index.
    IndexRequest request = new IndexRequest("custom-index"); //Add a document to the custom-index we created.
    request.id("1"); //Assign an ID to the document.

    HashMap<String, String> stringMapping = new HashMap<String, String>();
    stringMapping.put("message:", "Testing Java REST client");
    request.source(stringMapping); //Place your content into the index's source.
    IndexResponse indexResponse = client.index(request, RequestOptions.DEFAULT);

    //Getting back the document
    GetRequest getRequest = new GetRequest("custom-index", "1");
    GetResponse response = client.get(getRequest, RequestOptions.DEFAULT);

    System.out.println(response.getSourceAsString());

    //Delete the document
    DeleteRequest deleteDocumentRequest = new DeleteRequest("custom-index", "1"); //Index name followed by the ID.
    DeleteResponse deleteResponse = client.delete(deleteDocumentRequest, RequestOptions.DEFAULT);

    //Delete the index
    DeleteIndexRequest deleteIndexRequest = new DeleteIndexRequest("custom-index"); //Index name.
    AcknowledgedResponse deleteIndexResponse = client.indices().delete(deleteIndexRequest, RequestOptions.DEFAULT);

    client.close();
  }
}
```

## Elasticsearch OSS Java 高階 REST 用戶端

我們建議使用 OpenSearch 用戶端連線至 OpenSearch 叢集，但如果您必須使用 Elasticsearch OSS Java 高階 REST 用戶端，Elasticsearch OSS 用戶端 7.10.2 版也可搭配 OpenSearch 1.x 版使用。

### 遷移至 OpenSearch Java 高階 REST 用戶端

從 Elasticsearch OSS 用戶端遷移至 OpenSearch 高階 REST 用戶端非常簡單，只需將您的 Maven 相依性變更為參照 [OpenSearch 的相依性](#setup) 即可。

之後，將所有 `org.elasticsearch` 的參照變更為 `org.opensearch`，即可開始向您的 OpenSearch 叢集提交請求。
