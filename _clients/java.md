---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "Java 用戶端"
nav_order: 30
---

# Java 用戶端

OpenSearch Java 用戶端可讓您透過 Java 方法和資料結構與 OpenSearch 叢集互動，而不必使用 HTTP 方法和原始 JSON。例如，您可以使用物件向叢集提交請求，以建立索引、將資料新增至文件，或使用用戶端的內建方法完成其他操作。如需用戶端完整的 API 文件和其他範例，請參閱 [javadoc](https://www.javadoc.io/doc/org.opensearch.client/opensearch-java/latest/index.html)。

本入門指南說明如何連線至 OpenSearch、將文件編製索引及執行查詢。如需用戶端原始碼，請參閱 [`opensearch-java` 儲存庫](https://github.com/opensearch-project/opensearch-java)。

## 安裝 Java 用戶端

Java 用戶端需要傳輸層才能與您的叢集通訊。`ApacheHttpClient5Transport` 是預設的傳輸層，也是新應用程式的建議選擇。`RestClient` 傳輸層已遭棄用，並將在未來的版本中移除。

### 使用 Apache HttpClient 5 Transport 安裝用戶端

若要開始使用 OpenSearch Java 用戶端，您需要提供傳輸層。預設的 `ApacheHttpClient5TransportBuilder` 傳輸層隨附於 Java 用戶端。若要搭配預設傳輸層使用 OpenSearch Java 用戶端，請將其作為相依項目新增至您的 `pom.xml` 檔案：

```xml
<dependency>
  <groupId>org.opensearch.client</groupId>
  <artifactId>opensearch-java</artifactId>
  <version>3.10.0</version>
</dependency>
```
{% include copy.html %}

如果您使用 Gradle，請將下列相依項目新增至您的專案：

```groovy
dependencies {
  implementation 'org.opensearch.client:opensearch-java:3.10.0'
}
```
{% include copy.html %}

現在您可以啟動 OpenSearch 叢集。

### 使用 RestClient Transport 安裝用戶端（已棄用）

`RestClientTransport` 傳輸層及其所包裝的 `org.opensearch.client.RestClient` 類別已遭棄用，並將在未來的版本中移除。請改用 [Apache HttpClient 5 Transport](#installing-the-client-using-apache-httpclient-5-transport)。
{: .warning}

或者，您也可以使用以 `RestClient` 為基礎的傳輸層建立 Java 用戶端。在此情況下，請確認您專案的 `pom.xml` 檔案中具有下列相依項目：

```xml
<dependency>
  <groupId>org.opensearch.client</groupId>
  <artifactId>opensearch-rest-client</artifactId>
  <version>{{site.opensearch_version}}</version>
</dependency>

<dependency>
  <groupId>org.opensearch.client</groupId>
  <artifactId>opensearch-java</artifactId>
  <version>3.10.0</version>
</dependency>
```
{% include copy.html %}

如果您使用 Gradle，請將下列相依項目新增至您的專案：

```groovy
dependencies {
  implementation 'org.opensearch.client:opensearch-rest-client:{{site.opensearch_version}}'
  implementation 'org.opensearch.client:opensearch-java:3.10.0'
}
```
{% include copy.html %}

現在您可以啟動 OpenSearch 叢集。

## 範例資料

以下各節中的範例程式使用 `Student` 類別來表示文件。請使用下列包裝類別，此類別將 `gpa` 宣告為 Boxed `Double`，使部分更新能正確序列化：

```java
public class Student {
  private String firstName;
  private String lastName;
  private Double gpa;
  private String gradDate;

  public Student() {}

  public Student(String firstName, String lastName, double gpa, String gradDate) {
    this.firstName = firstName;
    this.lastName = lastName;
    this.gpa = gpa;
    this.gradDate = gradDate;
  }

  public String getFirstName() { return firstName; }
  public void setFirstName(String firstName) { this.firstName = firstName; }
  public String getLastName() { return lastName; }
  public void setLastName(String lastName) { this.lastName = lastName; }
  public Double getGpa() { return gpa; }
  public void setGpa(Double gpa) { this.gpa = gpa; }
  public String getGradDate() { return gradDate; }
  public void setGradDate(String gradDate) { this.gradDate = gradDate; }

  @Override
  public String toString() {
    return String.format("Student{firstName='%s', lastName='%s', gpa=%s, gradDate=%s}",
      firstName, lastName, gpa, gradDate);
  }
}
```
{% include copy.html %}

## 連線至 OpenSearch

下列範例會使用 Apache HttpClient 5 傳輸層或已棄用的 RestClient 傳輸層，連線至已啟用 Security 外掛程式的叢集。

### 使用 Apache HttpClient 5 Transport

此程式碼範例使用 `admin` 使用者。請將 `<custom-admin-password>` 替換為您安裝 OpenSearch 時設定的管理員密碼。

下列範例程式碼會初始化已啟用 SSL 和 TLS 的用戶端：


```java
import javax.net.ssl.SSLContext;
import javax.net.ssl.SSLEngine;

import org.apache.hc.client5.http.auth.AuthScope;
import org.apache.hc.client5.http.auth.UsernamePasswordCredentials;
import org.apache.hc.client5.http.impl.auth.BasicCredentialsProvider;
import org.apache.hc.client5.http.impl.nio.PoolingAsyncClientConnectionManager;
import org.apache.hc.client5.http.impl.nio.PoolingAsyncClientConnectionManagerBuilder;
import org.apache.hc.client5.http.ssl.ClientTlsStrategyBuilder;
import org.apache.hc.core5.function.Factory;
import org.apache.hc.core5.http.HttpHost;
import org.apache.hc.core5.http.nio.ssl.TlsStrategy;
import org.apache.hc.core5.reactor.ssl.TlsDetails;
import org.apache.hc.core5.ssl.SSLContextBuilder;
import org.opensearch.client.opensearch.OpenSearchClient;
import org.opensearch.client.transport.OpenSearchTransport;
import org.opensearch.client.transport.httpclient5.ApacheHttpClient5TransportBuilder;

public class OpenSearchClientExample {
  public static void main(String[] args) throws Exception {
    final HttpHost host = new HttpHost("https", "localhost", 9200);
    final BasicCredentialsProvider credentialsProvider = new BasicCredentialsProvider();
    // Only for demo purposes. Don't specify your credentials in code.
    credentialsProvider.setCredentials(new AuthScope(host), new UsernamePasswordCredentials("admin", "<custom-admin-password>".toCharArray()));

    // Trusts all certificates, including self-signed certificates. For testing only. Don't use in production.
    final SSLContext sslcontext = SSLContextBuilder
      .create()
      .loadTrustMaterial(null, (chains, authType) -> true)
      .build();

    final ApacheHttpClient5TransportBuilder builder = ApacheHttpClient5TransportBuilder.builder(host);
    builder.setHttpClientConfigCallback(httpClientBuilder -> {
      final TlsStrategy tlsStrategy = ClientTlsStrategyBuilder.create()
        .setSslContext(sslcontext)
        // See https://issues.apache.org/jira/browse/HTTPCLIENT-2219
        .setTlsDetailsFactory(new Factory<SSLEngine, TlsDetails>() {
          @Override
          public TlsDetails create(final SSLEngine sslEngine) {
            return new TlsDetails(sslEngine.getSession(), sslEngine.getApplicationProtocol());
          }
        })
        .build();

      final PoolingAsyncClientConnectionManager connectionManager = PoolingAsyncClientConnectionManagerBuilder
        .create()
        .setTlsStrategy(tlsStrategy)
        .build();

      return httpClientBuilder
        .setDefaultCredentialsProvider(credentialsProvider)
        .setConnectionManager(connectionManager);
    });

    final OpenSearchTransport transport = builder.build();
    OpenSearchClient client = new OpenSearchClient(transport);
  }
}
```
{% include copy.html %}

如果您在設定安全性時遇到問題，請參閱 [TLS 疑難排解]({{site.url}}{{site.baseurl}}/security/configuration/troubleshoot-tls/)。

### 使用 RestClient 傳輸層（已棄用）

`RestClientTransport` 傳輸層及其封裝的 `org.opensearch.client.RestClient` 類別已棄用，將在未來版本中移除。請改用 [Apache HttpClient 5 傳輸層](#using-apache-httpclient-5-transport)。
{: .warning}

此程式碼範例使用 `admin` 使用者。請將 `<custom-admin-password>` 替換為您安裝 OpenSearch 時設定的管理員密碼。

RestClient 傳輸層使用 Java 信任儲存庫來驗證叢集的憑證。如果您使用自我簽署憑證或示範憑證，請使用下列命令建立包含根憑證授權單位（CA）憑證的信任儲存庫。出現提示時，請輸入信任儲存庫的密碼：

```bash
keytool -importcert -file <path-to-root-ca-cert> -alias <alias> -keystore <truststore-name>
```
{% include copy.html %}

如果您使用受信任 CA 核發的憑證，就不需要設定信任儲存庫。

在下列程式碼中，請將 `/full/path/to/keystore` 替換為您的信任儲存庫路徑，並將 `password-to-keystore` 替換為信任儲存庫密碼。下列範例程式碼會初始化已啟用 SSL 和 TLS 的用戶端：

```java
import org.apache.hc.core5.http.HttpHost;
import org.apache.hc.client5.http.auth.AuthScope;
import org.apache.hc.client5.http.auth.UsernamePasswordCredentials;
import org.apache.hc.client5.http.impl.async.HttpAsyncClientBuilder;
import org.apache.hc.client5.http.impl.auth.BasicCredentialsProvider;
import org.opensearch.client.RestClient;
import org.opensearch.client.RestClientBuilder;
import org.opensearch.client.json.jackson.JacksonJsonpMapper;
import org.opensearch.client.opensearch.OpenSearchClient;
import org.opensearch.client.transport.OpenSearchTransport;
import org.opensearch.client.transport.rest_client.RestClientTransport;

public class OpenSearchClientExample {
  public static void main(String[] args) throws Exception {
    System.setProperty("javax.net.ssl.trustStore", "/full/path/to/keystore");
    System.setProperty("javax.net.ssl.trustStorePassword", "password-to-keystore");

    final HttpHost host = new HttpHost("https", "localhost", 9200);
    final BasicCredentialsProvider credentialsProvider = new BasicCredentialsProvider();
    //Only for demo purposes. Don't specify your credentials in code.
    credentialsProvider.setCredentials(new AuthScope(host), new UsernamePasswordCredentials("admin", "<custom-admin-password>".toCharArray()));

    //Initialize the client with SSL and TLS enabled
    final RestClient restClient = RestClient.builder(host).
      setHttpClientConfigCallback(new RestClientBuilder.HttpClientConfigCallback() {
        @Override
        public HttpAsyncClientBuilder customizeHttpClient(HttpAsyncClientBuilder httpClientBuilder) {
        return httpClientBuilder.setDefaultCredentialsProvider(credentialsProvider);
        }
      }).build();

    final OpenSearchTransport transport = new RestClientTransport(restClient, new JacksonJsonpMapper());
    final OpenSearchClient client = new OpenSearchClient(transport);
  }
}
```
{% include copy.html %}

## 連線至 Amazon OpenSearch Service

若要連線至 Amazon OpenSearch Service 或 Amazon OpenSearch Serverless，請使用 `AwsSdk2Transport`，它會使用 AWS SDK for Java 2.x 簽署請求。除了 `opensearch-java` 之外，也請將 AWS SDK HTTP 用戶端和驗證模組新增至您的 `pom.xml` 檔案：

```xml
<dependency>
  <groupId>software.amazon.awssdk</groupId>
  <artifactId>aws-crt-client</artifactId>
  <version>2.55.9</version>
</dependency>

<dependency>
  <groupId>software.amazon.awssdk</groupId>
  <artifactId>auth</artifactId>
  <version>2.55.9</version>
</dependency>
```
{% include copy.html %}

如果您使用 Gradle，請將下列相依項目新增至您的專案：

```groovy
dependencies {
  implementation 'software.amazon.awssdk:aws-crt-client:2.55.9'
  implementation 'software.amazon.awssdk:auth:2.55.9'
}
```
{% include copy.html %}

這些範例使用 `AwsCrtHttpClient`。請避免使用 AWS SDK 的 `ApacheHttpClient`，因為它不支援 `GET` 或 `DELETE` 請求中的請求本文，因此 `AwsSdk2Transport` 在執行 `clearScroll()` 和 `deletePit()` 等操作時會擲回 `TransportException`。
{: .note}

在下列範例中，請將端點替換為您的網域端點，該端點列於 Amazon OpenSearch Service 主控台中的網域詳細資訊頁面。

`AwsSdk2Transport` 會從 AWS SDK 預設憑證提供者鏈取得 AWS 憑證。下列範例示範如何連線至 Amazon OpenSearch Service：

```java
import org.opensearch.client.opensearch.OpenSearchClient;
import org.opensearch.client.opensearch.core.InfoResponse;
import org.opensearch.client.transport.aws.AwsSdk2Transport;
import org.opensearch.client.transport.aws.AwsSdk2TransportOptions;
import software.amazon.awssdk.http.SdkHttpClient;
import software.amazon.awssdk.http.crt.AwsCrtHttpClient;
import software.amazon.awssdk.regions.Region;

SdkHttpClient httpClient = AwsCrtHttpClient.builder().build();

OpenSearchClient client = new OpenSearchClient(
    new AwsSdk2Transport(
        httpClient,
        "search-<domain-name>-<id>.us-east-1.es.amazonaws.com", // OpenSearch endpoint, without https://
        "es",
        Region.US_EAST_1, // signing service region
        AwsSdk2TransportOptions.builder().build()
    )
);

InfoResponse info = client.info();
System.out.println(info.version().distribution() + ": " + info.version().number());

httpClient.close();
```
{% include copy.html %}

## 連線至 Amazon OpenSearch Serverless

在下列範例中，請將端點替換為您的集合端點，該端點列於 Amazon OpenSearch Service 主控台中的集合詳細資訊頁面。

下列範例示範如何連線至 Amazon OpenSearch Serverless。由於 Amazon OpenSearch Serverless 不支援根端點，此範例會檢查索引是否存在：

```java
import org.opensearch.client.opensearch.OpenSearchClient;
import org.opensearch.client.transport.aws.AwsSdk2Transport;
import org.opensearch.client.transport.aws.AwsSdk2TransportOptions;
import software.amazon.awssdk.http.SdkHttpClient;
import software.amazon.awssdk.http.crt.AwsCrtHttpClient;
import software.amazon.awssdk.regions.Region;

SdkHttpClient httpClient = AwsCrtHttpClient.builder().build();

OpenSearchClient client = new OpenSearchClient(
    new AwsSdk2Transport(
        httpClient,
        "<collection-id>.us-east-1.aoss.amazonaws.com", // OpenSearch Serverless collection endpoint, without https://
        "aoss",
        Region.US_EAST_1, // signing service region
        AwsSdk2TransportOptions.builder().build()
    )
);

boolean exists = client.indices().exists(e -> e.index("students")).value();
System.out.println("Index exists: " + exists);

httpClient.close();
```
{% include copy.html %}

Amazon OpenSearch Serverless 支援部分 OpenSearch API 操作，且不支援本頁範例中使用的 `refresh` 參數。如需詳細資訊，請參閱 [Amazon OpenSearch Serverless 支援的操作與外掛程式](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/serverless-genref.html)。
{: .note}

## 建立索引

下列範例會建立具有一個主要分片和一個副本的索引。它會將 `gradDate` 欄位明確對應為 `yyyy-MM-dd` 格式的 `date`。當您將文件編製索引時，OpenSearch 會動態對應其他文件欄位：

```java
String index = "students";
CreateIndexRequest createIndexRequest = new CreateIndexRequest.Builder()
  .index(index)
  .settings(s -> s
    .numberOfShards(1)
    .numberOfReplicas(1))
  .mappings(m -> m
    .properties("gradDate", p -> p.date(d -> d.format("yyyy-MM-dd"))))
  .build();
client.indices().create(createIndexRequest);
```
{% include copy.html %}

## 將文件編製索引

使用下列程式碼將文件編製索引：

```java
Student student = new Student("John", "Doe", 3.89, "2022-05-15");
IndexRequest<Student> indexRequest = new IndexRequest.Builder<Student>()
  .index(index).id("1").document(student).refresh(Refresh.True).build();
IndexResponse indexResponse = client.index(indexRequest);
```
{% include copy.html %}

## 大量編製索引

使用下列程式碼，在單一請求中將多份文件編製索引：

```java
List<BulkOperation> operations = new ArrayList<>();
operations.add(new BulkOperation.Builder().index(
  new IndexOperation.Builder<Student>()
    .index(index).id("2")
    .document(new Student("Paulo", "Santos", 3.93, "2021-05-20")).build()
).build());
operations.add(new BulkOperation.Builder().index(
  new IndexOperation.Builder<Student>()
    .index(index).id("3")
    .document(new Student("Shirley", "Rodriguez", 3.91, "2019-05-10")).build()
).build());
BulkRequest bulkRequest = new BulkRequest.Builder()
  .index(index).operations(operations).refresh(Refresh.True).build();
BulkResponse bulkResponse = client.bulk(bulkRequest);
```
{% include copy.html %}

## 搜尋文件

使用下列程式碼搜尋索引中的所有文件：

```java
SearchResponse<Student> searchResponse = client.search(s -> s.index(index), Student.class);
for (int i = 0; i < searchResponse.hits().hits().size(); i++) {
  System.out.println(searchResponse.hits().hits().get(i).source());
}
```
{% include copy.html %}

`searchResponse.hits().hits()` 中的每個命中結果都是一個 `Hit<Student>` 物件，其中 `hit.id()` 包含文件 ID，`hit.source()` 包含 `Student` 物件，其欄位可透過 getter 存取。若要使用 `Hit` 類別，請匯入 `org.opensearch.client.opensearch.core.search.Hit`：

```java
for (Hit<Student> hit : searchResponse.hits().hits()) {
  Student student = hit.source();
  System.out.println("ID: " + hit.id() + ", name: " + student.getFirstName() + " " + student.getLastName()
      + ", GPA: " + student.getGpa() + ", graduation date: " + student.getGradDate());
}
```
{% include copy.html %}

使用範圍查詢進行搜尋。`gte` 和 `lte` 邊界接受 `JsonData` 值，因此請匯入 `org.opensearch.client.json.JsonData`：

```java
SearchResponse<Student> searchResponse = client.search(s -> s
  .index(index)
  .query(q -> q.range(r -> r
    .field("gradDate")
    .gte(JsonData.of("2019-01-01"))
    .lte(JsonData.of("2019-12-31")))),
  Student.class);
```
{% include copy.html %}

## 將結果分頁

若要將結果分頁，請使用 `from` 和 `size` 參數。下列範例會依畢業日期排序學生，並每次擷取兩筆結果。第一個請求會傳回第一頁結果，第二個請求會傳回下一頁。若要使用 `SortOrder` 列舉，請匯入 `org.opensearch.client.opensearch._types.SortOrder`：

```java
SearchResponse<Student> firstPageResponse = client.search(s -> s
  .index(index)
  .from(0)
  .size(2)
  .sort(so -> so.field(f -> f.field("gradDate").order(SortOrder.Asc))),
  Student.class);
for (int i = 0; i < firstPageResponse.hits().hits().size(); i++) {
  System.out.println(firstPageResponse.hits().hits().get(i).source());
}

SearchResponse<Student> nextPageResponse = client.search(s -> s
  .index(index)
  .from(2)
  .size(2)
  .sort(so -> so.field(f -> f.field("gradDate").order(SortOrder.Asc))),
  Student.class);
for (int i = 0; i < nextPageResponse.hits().hits().size(); i++) {
  System.out.println(nextPageResponse.hits().hits().get(i).source());
}
```
{% include copy.html %}

`from` 和 `size` 參數適用於結果的前幾頁。若要在大量結果中分頁，請搭配 `search_after` 使用時間點 (point in time)。如需更多資訊，請參閱[將結果分頁]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/paginate/)。

## 更新文件

使用部分文件物件更新文件。設為 `null` 的欄位不會被傳送，因此只會更新指定的欄位：

```java
Student updatedFields = new Student();
updatedFields.setGpa(3.92);
UpdateRequest<Student, Student> updateRequest = new UpdateRequest.Builder<Student, Student>()
  .index(index).id("1").doc(updatedFields).build();
UpdateResponse<Student> updateResponse = client.update(updateRequest, Student.class);
```
{% include copy.html %}

## 刪除文件

使用下列程式碼刪除文件：

```java
client.delete(b -> b.index(index).id("3").refresh(Refresh.True));
```
{% include copy.html %}

## 刪除索引

使用下列程式碼刪除索引：

```java
DeleteIndexRequest deleteIndexRequest = new DeleteIndexRequest.Builder().index(index).build();
DeleteIndexResponse deleteIndexResponse = client.indices().delete(deleteIndexRequest);
```
{% include copy.html %}

## 範例程式

此範例程式結合了前述各節的程式碼。它會連線至已啟用 Security 外掛程式的叢集。若要連線至未使用 Security 外掛程式的叢集，請變更標有 `// Without security` 註解的程式行。執行範例程式之前，請確認您已在專案中定義 `Student` 類別。請務必變更認證資訊，使其符合您的叢集組態。

此範例程式僅供測試使用。它會在程式碼中指定認證資訊並停用憑證驗證，以便連線至使用自我簽署憑證的叢集。在正式環境中，請從安全的位置載入認證資訊，並驗證叢集的憑證。
{: .warning}

下列範例程式會建立用戶端、建立索引、逐一及大量將文件編製索引、搜尋文件、更新文件、刪除文件，然後刪除索引：

```java
import javax.net.ssl.SSLContext;
import javax.net.ssl.SSLEngine;

import org.apache.hc.client5.http.auth.AuthScope;
import org.apache.hc.client5.http.auth.UsernamePasswordCredentials;
import org.apache.hc.client5.http.impl.auth.BasicCredentialsProvider;
import org.apache.hc.client5.http.impl.nio.PoolingAsyncClientConnectionManager;
import org.apache.hc.client5.http.impl.nio.PoolingAsyncClientConnectionManagerBuilder;
import org.apache.hc.client5.http.ssl.ClientTlsStrategyBuilder;
import org.apache.hc.core5.function.Factory;
import org.apache.hc.core5.http.HttpHost;
import org.apache.hc.core5.http.nio.ssl.TlsStrategy;
import org.apache.hc.core5.reactor.ssl.TlsDetails;
import org.apache.hc.core5.ssl.SSLContextBuilder;
import org.opensearch.client.json.JsonData;
import org.opensearch.client.opensearch.OpenSearchClient;
import org.opensearch.client.opensearch._types.Refresh;
import org.opensearch.client.opensearch._types.SortOrder;
import org.opensearch.client.opensearch.core.IndexRequest;
import org.opensearch.client.opensearch.core.IndexResponse;
import org.opensearch.client.opensearch.core.SearchResponse;
import org.opensearch.client.opensearch.core.UpdateRequest;
import org.opensearch.client.opensearch.core.UpdateResponse;
import org.opensearch.client.opensearch.core.GetResponse;
import org.opensearch.client.opensearch.core.BulkRequest;
import org.opensearch.client.opensearch.core.BulkResponse;
import org.opensearch.client.opensearch.core.DeleteResponse;
import org.opensearch.client.opensearch.core.bulk.BulkOperation;
import org.opensearch.client.opensearch.core.bulk.IndexOperation;
import org.opensearch.client.opensearch.indices.*;
import org.opensearch.client.transport.OpenSearchTransport;
import org.opensearch.client.transport.httpclient5.ApacheHttpClient5TransportBuilder;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

public class OpenSearchClientExample {
  public static void main(String[] args) throws Exception {
    final HttpHost host = new HttpHost("https", "localhost", 9200); // Without security, use new HttpHost("http", "localhost", 9200)
    final BasicCredentialsProvider credentialsProvider = new BasicCredentialsProvider(); // Without security, remove this line
    // Without security, remove this line
    credentialsProvider.setCredentials(new AuthScope(host), new UsernamePasswordCredentials("admin", "<custom-admin-password>".toCharArray()));

    final SSLContext sslcontext = SSLContextBuilder.create()
      .loadTrustMaterial(null, (chains, authType) -> true)
      .build();

    final ApacheHttpClient5TransportBuilder builder = ApacheHttpClient5TransportBuilder.builder(host);
    builder.setHttpClientConfigCallback(httpClientBuilder -> {
      final TlsStrategy tlsStrategy = ClientTlsStrategyBuilder.create()
        .setSslContext(sslcontext)
        .setTlsDetailsFactory(new Factory<SSLEngine, TlsDetails>() {
          @Override
          public TlsDetails create(final SSLEngine sslEngine) {
            return new TlsDetails(sslEngine.getSession(), sslEngine.getApplicationProtocol());
          }
        })
        .build();

      final PoolingAsyncClientConnectionManager connectionManager =
        PoolingAsyncClientConnectionManagerBuilder.create()
          .setTlsStrategy(tlsStrategy)
          .build();

      return httpClientBuilder
        .setDefaultCredentialsProvider(credentialsProvider) // Without security, remove this line
        .setConnectionManager(connectionManager);
    });

    final OpenSearchTransport transport = builder.build();
    final OpenSearchClient client = new OpenSearchClient(transport);

    try {
      // Create the index
      String index = "students";
      System.out.println("Creating index......");
      CreateIndexRequest createIndexRequest = new CreateIndexRequest.Builder()
        .index(index)
        .settings(s -> s
          .numberOfShards(1)
          .numberOfReplicas(1))
        .mappings(m -> m
          .properties("gradDate", p -> p.date(d -> d.format("yyyy-MM-dd"))))
        .build();
      CreateIndexResponse createIndexResponse = client.indices().create(createIndexRequest);
      System.out.println("Index created: " + createIndexResponse.index());

      // Index a document
      System.out.println("\nIndexing one student......");
      Student student = new Student("John", "Doe", 3.89, "2022-05-15");
      IndexRequest<Student> indexRequest = new IndexRequest.Builder<Student>()
        .index(index).id("1").document(student).refresh(Refresh.True).build();
      IndexResponse indexResponse = client.index(indexRequest);
      System.out.println("Result: " + indexResponse.result().jsonValue() + ", id: " + indexResponse.id() + ", version: " + indexResponse.version());

      // Bulk index documents
      System.out.println("\nIndexing many students......");
      List<BulkOperation> operations = new ArrayList<>();
      operations.add(new BulkOperation.Builder().index(
        new IndexOperation.Builder<Student>()
          .index(index).id("2")
          .document(new Student("Paulo", "Santos", 3.93, "2021-05-20")).build()
      ).build());
      operations.add(new BulkOperation.Builder().index(
        new IndexOperation.Builder<Student>()
          .index(index).id("3")
          .document(new Student("Shirley", "Rodriguez", 3.91, "2019-05-10")).build()
      ).build());
      BulkRequest bulkRequest = new BulkRequest.Builder()
        .index(index).operations(operations).refresh(Refresh.True).build();
      BulkResponse bulkResponse = client.bulk(bulkRequest);
      System.out.println("Errors: " + bulkResponse.errors());
      bulkResponse.items().forEach(item ->
        System.out.println("  " + item.result() + " id: " + item.id()));

      // Search for all students
      System.out.println("\nSearching for all students......");
      SearchResponse<Student> searchResponse = client.search(s -> s
        .index(index)
        .from(0)
        .size(2)
        .sort(so -> so.field(f -> f.field("gradDate").order(SortOrder.Asc))),
        Student.class);
      System.out.println("Total hits: " + searchResponse.hits().total().value());
      System.out.println("Page 1:");
      for (int i = 0; i < searchResponse.hits().hits().size(); i++) {
        System.out.println("  " + searchResponse.hits().hits().get(i).source());
      }
      SearchResponse<Student> nextPageResponse = client.search(s -> s
        .index(index)
        .from(2)
        .size(2)
        .sort(so -> so.field(f -> f.field("gradDate").order(SortOrder.Asc))),
        Student.class);
      System.out.println("Page 2:");
      for (int i = 0; i < nextPageResponse.hits().hits().size(); i++) {
        System.out.println("  " + nextPageResponse.hits().hits().get(i).source());
      }

      // Search for students who graduated in 2019
      System.out.println("\nSearching for students who graduated in 2019......");
      SearchResponse<Student> searchResponse2 = client.search(s -> s
        .index(index)
        .query(q -> q.range(r -> r
          .field("gradDate")
          .gte(JsonData.of("2019-01-01"))
          .lte(JsonData.of("2019-12-31")))),
        Student.class);
      System.out.println("Total hits: " + searchResponse2.hits().total().value());
      for (int i = 0; i < searchResponse2.hits().hits().size(); i++) {
        System.out.println("  " + searchResponse2.hits().hits().get(i).source());
      }

      // Update a document
      System.out.println("\nUpdating a student's GPA......");
      Student updatedFields = new Student();
      updatedFields.setGpa(3.92);
      UpdateRequest<Student, Student> updateRequest = new UpdateRequest.Builder<Student, Student>()
        .index(index).id("1").doc(updatedFields).build();
      UpdateResponse<Student> updateResponse = client.update(updateRequest, Student.class);
      System.out.println("Result: " + updateResponse.result().jsonValue() + ", version: " + updateResponse.version());

      // Get the updated document
      GetResponse<Student> getResponse = client.get(g -> g.index(index).id("1"), Student.class);
      System.out.println("Updated document: " + getResponse.source());

      // Delete a document
      System.out.println("\nDeleting a student......");
      DeleteResponse deleteResponse = client.delete(b -> b.index(index).id("3").refresh(Refresh.True));
      System.out.println("Result: " + deleteResponse.result().jsonValue());

      // Delete the index
      System.out.println("\nDeleting the index......");
      DeleteIndexRequest deleteIndexRequest = new DeleteIndexRequest.Builder().index(index).build();
      DeleteIndexResponse deleteIndexResponse = client.indices().delete(deleteIndexRequest);
      System.out.println("Acknowledged: " + deleteIndexResponse.acknowledged());

    } finally {
      transport.close();
    }
  }
}
```
{% include copy.html %}

程式會產生下列輸出：

```
Creating index......
Index created: students

Indexing one student......
Result: created, id: 1, version: 1

Indexing many students......
Errors: false
  created id: 2
  created id: 3

Searching for all students......
Total hits: 3
Page 1:
  Student{firstName='Shirley', lastName='Rodriguez', gpa=3.91, gradDate=2019-05-10}
  Student{firstName='Paulo', lastName='Santos', gpa=3.93, gradDate=2021-05-20}
Page 2:
  Student{firstName='John', lastName='Doe', gpa=3.89, gradDate=2022-05-15}

Searching for students who graduated in 2019......
Total hits: 1
  Student{firstName='Shirley', lastName='Rodriguez', gpa=3.91, gradDate=2019-05-10}

Updating a student's GPA......
Result: updated, version: 2
Updated document: Student{firstName='John', lastName='Doe', gpa=3.92, gradDate=2022-05-15}

Deleting a student......
Result: deleted

Deleting the index......
Acknowledged: true
```

## 相關文件

- 如需更多使用用戶端的範例，請參閱 [`opensearch-java` 使用者指南](https://github.com/opensearch-project/opensearch-java/blob/main/USER_GUIDE.md)。
- 如需特定工作的指南，例如大量編製索引和搜尋，請參閱 [`opensearch-java` 指南](https://github.com/opensearch-project/opensearch-java/tree/main/guides)。
- 如需完整的範例應用程式，請參閱 [`opensearch-java` 範例](https://github.com/opensearch-project/opensearch-java/tree/main/samples)。
