---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "JavaScript 用戶端"
has_children: true
has_toc: false
nav_order: 40
redirect_from:
  - /clients/javascript/
---

# JavaScript 用戶端

OpenSearch JavaScript (JS) 用戶端提供更安全、更簡便的方式與您的 OpenSearch 叢集互動。與其在瀏覽器中使用 OpenSearch 而可能將資料暴露給公眾，您可以建立一個 OpenSearch 用戶端來處理傳送至叢集的請求。如需用戶端的完整 API 文件與更多範例，請參閱 [JS 用戶端 API 文件](https://opensearch-project.github.io/opensearch-js/3.6/index.html)。

用戶端包含一組 API 程式庫，讓您對叢集執行各種操作並回傳標準的回應本文。此處的範例示範一些基本操作，例如建立索引、新增文件，以及搜尋您的資料。

您可以使用輔助方法來簡化複雜的 API 任務。如需更多資訊，請參閱[輔助方法]({{site.url}}{{site.baseurl}}/clients/javascript/helpers/)。如需更進階的索引操作，請參閱 GitHub 上的 [`opensearch-js` 指南](https://github.com/opensearch-project/opensearch-js/tree/main/guides)。

## 安裝 JavaScript 用戶端

用戶端需要 Node.js 14 或更新版本。

若要將用戶端加入您的專案，請從 [`npm`](https://www.npmjs.com) 安裝：

```bash
npm install @opensearch-project/opensearch
```
{% include copy.html %}

若要安裝特定版本的用戶端，請執行以下命令：

```bash
npm install @opensearch-project/opensearch@<version>
```
{% include copy.html %}

如果您偏好手動新增用戶端，或只想檢視原始碼，請參閱 GitHub 上的 [`opensearch-js`](https://github.com/opensearch-project/opensearch-js)。

然後引入用戶端：

```javascript
const { Client } = require("@opensearch-project/opensearch");
```
{% include copy.html %}

## 連線至 OpenSearch

若要連線至預設的 OpenSearch 主機，如果您使用 Security 外掛程式，請以位址 `https://localhost:9200` 建立用戶端物件：

```javascript
var host = "localhost";
var protocol = "https";
var port = 9200;
var auth = "admin:<custom-admin-password>"; // For testing only. Don't store credentials in code.
var ca_certs_path = "/full/path/to/root-ca.pem";

// Optional client certificates if you don't want to use HTTP basic authentication.
// var client_cert_path = '/full/path/to/client.pem'
// var client_key_path = '/full/path/to/client-key.pem'

// Create a client with SSL/TLS enabled.
var { Client } = require("@opensearch-project/opensearch");
var fs = require("fs");
var client = new Client({
  node: protocol + "://" + auth + "@" + host + ":" + port,
  ssl: {
    ca: fs.readFileSync(ca_certs_path),
    // You can turn off certificate verification (rejectUnauthorized: false) if you're using 
    // self-signed certificates with a hostname mismatch.
    // cert: fs.readFileSync(client_cert_path),
    // key: fs.readFileSync(client_key_path)
  },
});
```
{% include copy.html %}

如果您未使用 Security 外掛程式，請以位址 `http://localhost:9200` 建立用戶端物件：

```javascript
var host = "localhost";
var protocol = "http";
var port = 9200;

// Create a client
var { Client } = require("@opensearch-project/opensearch");
var client = new Client({
  node: protocol + "://" + host + ":" + port
});
```
{% include copy.html %}

## 使用 Amazon OpenSearch Service 進行驗證：AWS Signature Version 4

若要使用 AWS SDK for JavaScript V3 簽署請求，請安裝 V3 憑證供應商套件：

```bash
npm install @aws-sdk/credential-provider-node
```
{% include copy.html %}

若要使用 AWS SDK for JavaScript V2 簽署請求，請安裝 V2 SDK：

```bash
npm install aws-sdk
```
{% include copy.html %}

AWS SDK for JavaScript V2 已於 2025 年 9 月 8 日終止支援。對於新的應用程式，請使用本節中的 AWS SDK for JavaScript V3 範例。
{: .note}

在下列範例中，請將端點替換為您的網域或集合端點，該端點列於 Amazon OpenSearch Service 主控台中網域或集合的詳細資料頁面。

請使用以下程式碼以 AWS V2 SDK 進行驗證：

```javascript
const AWS = require('aws-sdk'); // V2 SDK.
const { Client } = require('@opensearch-project/opensearch');
const { AwsSigv4Signer } = require('@opensearch-project/opensearch/aws');

const client = new Client({
  ...AwsSigv4Signer({
    region: 'us-east-1',
    service: 'es',
    // Must return a Promise that resolves to an AWS.Credentials object.
    // This function acquires the credentials when the client starts and
    // when the credentials expire.
    // The client refreshes the credentials only when they expire, using
    // Credentials.refreshPromise when it is available.

    // Example with AWS SDK V2:
    getCredentials: () =>
      new Promise((resolve, reject) => {
        // Any other method to acquire a new Credentials object can be used.
        AWS.config.getCredentials((err, credentials) => {
          if (err) {
            reject(err);
          } else {
            resolve(credentials);
          }
        });
      }),
  }),
  node: 'https://search-<domain-name>-<id>.us-east-1.es.amazonaws.com', // OpenSearch domain endpoint
});
```
{% include copy.html %}

請使用以下程式碼以適用於 Amazon OpenSearch Serverless 的 AWS V2 SDK 進行驗證：

```javascript
const AWS = require('aws-sdk'); // V2 SDK.
const { Client } = require('@opensearch-project/opensearch');
const { AwsSigv4Signer } = require('@opensearch-project/opensearch/aws');

const client = new Client({
  ...AwsSigv4Signer({
    region: 'us-east-1',
    service: 'aoss',
    // Must return a Promise that resolves to an AWS.Credentials object.
    // This function acquires the credentials when the client starts and
    // when the credentials expire.
    // The client refreshes the credentials only when they expire, using
    // Credentials.refreshPromise when it is available.

    // Example with AWS SDK V2:
    getCredentials: () =>
      new Promise((resolve, reject) => {
        // Any other method to acquire a new Credentials object can be used.
        AWS.config.getCredentials((err, credentials) => {
          if (err) {
            reject(err);
          } else {
            resolve(credentials);
          }
        });
      }),
  }),
  node: 'https://<collection-id>.us-east-1.aoss.amazonaws.com', // OpenSearch Serverless collection endpoint
});
```
{% include copy.html %}

請使用以下程式碼以 AWS V3 SDK 進行驗證：

```javascript
const { defaultProvider } = require('@aws-sdk/credential-provider-node'); // V3 SDK.
const { Client } = require('@opensearch-project/opensearch');
// Use the aws-v3 import path with the AWS SDK for JavaScript V3. It lazy loads
// only the V3 credential providers.
const { AwsSigv4Signer } = require('@opensearch-project/opensearch/aws-v3');

const client = new Client({
  ...AwsSigv4Signer({
    region: 'us-east-1',
    service: 'es',  // 'aoss' for OpenSearch Serverless
    // Must return a Promise that resolves to a credentials object containing
    // accessKeyId, secretAccessKey, and, optionally, sessionToken and expiration.
    // This function acquires the credentials when the client starts and
    // when the credentials expire.
    // The client treats the credentials as expired if they are within
    // requestTimeout milliseconds of expiration (the default is 30,000).

    // Example with AWS SDK V3:
    getCredentials: () => {
      // Any other credential provider that returns such a Promise can be used.
      const credentialsProvider = defaultProvider();
      return credentialsProvider();
    },
  }),
  node: 'https://search-<domain-name>-<id>.us-east-1.es.amazonaws.com', // OpenSearch domain endpoint
  // node: 'https://<collection-id>.us-east-1.aoss.amazonaws.com' for an OpenSearch Serverless collection endpoint
});
```
{% include copy.html %}

請使用以下程式碼以適用於 Amazon OpenSearch Serverless 的 AWS V3 SDK 進行驗證：

```javascript
const { defaultProvider } = require('@aws-sdk/credential-provider-node'); // V3 SDK.
const { Client } = require('@opensearch-project/opensearch');
// Use the aws-v3 import path with the AWS SDK for JavaScript V3. It lazy loads
// only the V3 credential providers.
const { AwsSigv4Signer } = require('@opensearch-project/opensearch/aws-v3');

const client = new Client({
  ...AwsSigv4Signer({
    region: 'us-east-1',
    service: 'aoss',
    // Must return a Promise that resolves to a credentials object containing
    // accessKeyId, secretAccessKey, and, optionally, sessionToken and expiration.
    // This function acquires the credentials when the client starts and
    // when the credentials expire.
    // The client treats the credentials as expired if they are within
    // requestTimeout milliseconds of expiration (the default is 30,000).

    // Example with AWS SDK V3:
    getCredentials: () => {
      // Any other credential provider that returns such a Promise can be used.
      const credentialsProvider = defaultProvider();
      return credentialsProvider();
    },
  }),
  node: 'https://<collection-id>.us-east-1.aoss.amazonaws.com', // OpenSearch Serverless collection endpoint
});
```
{% include copy.html %}

Amazon OpenSearch Serverless 支援 OpenSearch API 操作的子集，且不支援本頁範例中使用的 `refresh` 參數。如需更多資訊，請參閱 [Amazon OpenSearch Serverless 支援的操作與外掛程式](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/serverless-genref.html)。
{: .note}

### 在 AWS Lambda 函式中進行驗證

在 AWS Lambda 函式中，於處理常式函式外部宣告的物件會保留其初始化狀態。如需更多資訊，請參閱 [Lambda 執行環境](https://docs.aws.amazon.com/lambda/latest/dg/lambda-runtime-environment.html)。因此，您必須在處理常式函式外部初始化 OpenSearch 用戶端，以確保後續叫用時能重複使用原始連線。這可提升效率，並免除每次都要建立新連線的需求。

在處理常式函式內初始化用戶端，可能會有遇到 `ConnectionError: getaddrinfo EMFILE error` 的風險。當後續叫用時建立了多個連線，超過系統的檔案描述元上限，就會發生此錯誤。

以下的 AWS Lambda 函式程式碼範例示範如何正確初始化 OpenSearch 用戶端：

```javascript
const { defaultProvider } = require('@aws-sdk/credential-provider-node'); // V3 SDK.
const { Client } = require('@opensearch-project/opensearch');
// Use the aws-v3 import path with the AWS SDK for JavaScript V3. It lazy loads
// only the V3 credential providers.
const { AwsSigv4Signer } = require('@opensearch-project/opensearch/aws-v3');

const client = new Client({
  ...AwsSigv4Signer({
    region: 'us-east-1',
    service: 'es',  // 'aoss' for OpenSearch Serverless
    // Must return a Promise that resolves to a credentials object containing
    // accessKeyId, secretAccessKey, and, optionally, sessionToken and expiration.
    // This function acquires the credentials when the client starts and
    // when the credentials expire.
    // The client treats the credentials as expired if they are within
    // requestTimeout milliseconds of expiration (the default is 30,000).

    // Example with AWS SDK V3:
    getCredentials: () => {
      // Any other credential provider that returns such a Promise can be used.
      const credentialsProvider = defaultProvider();
      return credentialsProvider();
    },
  }),
  node: 'https://search-<domain-name>-<id>.us-east-1.es.amazonaws.com', // OpenSearch domain endpoint
  // node: 'https://<collection-id>.us-east-1.aoss.amazonaws.com' for an OpenSearch Serverless collection endpoint
});

exports.handler = async (event, context) => {
  // Use the already initialized client
  const response = await client.indices.create({
    index: "students",
  });

  return response.body;
};
```
{% include copy.html %}

## 建立索引

以下範例建立一個具有一個主要分片和一個副本的索引。它會以 `yyyy-MM-dd` 格式，將 `gradDate` 欄位明確對應為 `date`。當您將文件編製索引時，OpenSearch 會動態對應其他文件欄位：

```javascript
var index_name = "students";

var response = await client.indices.create({
  index: index_name,
  body: {
    settings: {
      index: {
        number_of_shards: 1,
        number_of_replicas: 1,
      },
    },
    mappings: {
      properties: {
        gradDate: { type: "date", format: "yyyy-MM-dd" },
      },
    },
  },
});
```
{% include copy.html %}

## 將文件編製索引

使用用戶端的 `index` 方法，將文件編製索引至 OpenSearch：

```javascript
var student = { firstName: "John", lastName: "Doe", gpa: 3.89, gradDate: "2022-05-15" };

var response = await client.index({
  index: index_name,
  id: "1",
  body: student,
  refresh: true,
});
```
{% include copy.html %}

## 大量編製索引

使用用戶端的 `bulk` 方法，在單一請求中將多個文件編製索引。請求本文是一個陣列，其中每個動作後面接著該動作所套用的文件：

```javascript
var response = await client.bulk({
  body: [
    { index: { _index: index_name, _id: "2" } },
    { firstName: "Paulo", lastName: "Santos", gpa: 3.93, gradDate: "2021-05-20" },
    { index: { _index: index_name, _id: "3" } },
    { firstName: "Shirley", lastName: "Rodriguez", gpa: 3.91, gradDate: "2019-05-10" },
  ],
  refresh: true,
});
```
{% include copy.html %}

若要從陣列、串流或非同步產生器建立請求本文，請使用 [bulk 輔助方法]({{site.url}}{{site.baseurl}}/clients/javascript/helpers/#bulk-helper)。

## 搜尋文件

使用用戶端的 `search` 方法，搜尋索引中的所有文件：

```javascript
var response = await client.search({
  index: index_name,
  body: {
    query: {
      match_all: {},
    },
  },
});
response.body.hits.hits.forEach((hit) => console.log(hit._source));
```
{% include copy.html %}

`response.body.hits.hits` 中的每個項目都是純 JavaScript 物件。文件 ID 位於 `_id` 屬性中，而文件欄位則是 `_source` 物件的屬性：

```javascript
response.body.hits.hits.forEach((hit) => {
  console.log(
    `ID: ${hit._id}, name: ${hit._source.firstName} ${hit._source.lastName}, GPA: ${hit._source.gpa}, graduation date: ${hit._source.gradDate}`
  );
});
```
{% include copy.html %}

使用 `range` 查詢進行搜尋：

```javascript
var response = await client.search({
  index: index_name,
  body: {
    query: {
      range: {
        gradDate: {
          gte: "2019-01-01",
          lte: "2019-12-31",
        },
      },
    },
  },
});
```
{% include copy.html %}

## 分頁顯示結果

若要分頁顯示結果，請使用 `from` 和 `size` 參數。以下範例依畢業日期排序學生，並一次擷取兩筆結果。第一個請求會傳回第一頁結果，第二個請求則會傳回下一頁：

```javascript
var response = await client.search({
  index: index_name,
  body: {
    from: 0,
    size: 2,
    sort: [{ gradDate: "asc" }],
  },
});
response.body.hits.hits.forEach((hit) => console.log(hit._source));

var nextPage = await client.search({
  index: index_name,
  body: {
    from: 2,
    size: 2,
    sort: [{ gradDate: "asc" }],
  },
});
nextPage.body.hits.hits.forEach((hit) => console.log(hit._source));
```
{% include copy.html %}

`from` 和 `size` 參數適用於結果的前幾頁。若要在大量結果中分頁，請使用時間點 (point in time) 搭配 `search_after`。如需更多資訊，請參閱 [分頁顯示結果]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/paginate/)。

## 更新文件

使用用戶端的 `update` 方法更新文件。`doc` 物件僅包含要更新的欄位：

```javascript
var response = await client.update({
  index: index_name,
  id: "1",
  body: {
    doc: { gpa: 3.92 },
  },
});
```
{% include copy.html %}

## 刪除文件

使用用戶端的 `delete` 方法刪除文件：

```javascript
var response = await client.delete({
  index: index_name,
  id: "3",
  refresh: true,
});
```
{% include copy.html %}

## 刪除索引

使用 `indices.delete()` 方法刪除索引：

```javascript
var response = await client.indices.delete({
  index: index_name,
});
```
{% include copy.html %}

## 範例程式

此範例程式結合了前述各節的程式碼。它會連線至已啟用 Security 外掛程式的叢集。若要連線至未啟用 Security 外掛程式的叢集，請變更標有 `// Without security` 註解的行。

此範例程式僅供測試之用。它會在程式碼中指定認證資訊。在正式環境中，請從安全的位置載入認證資訊。
{: .warning}

以下範例程式會建立用戶端、建立索引、個別及大量將文件編製索引、搜尋文件、更新文件、刪除文件，然後刪除索引：

```javascript
"use strict";

var host = "localhost";
var protocol = "https"; // Without security, use "http"
var port = 9200;
// Without security, remove the following line
var auth = "admin:<custom-admin-password>";
var ca_certs_path = "/full/path/to/root-ca.pem"; // Without security, remove this line

// Optional client certificates if you don't want to use HTTP basic authentication
// var client_cert_path = '/full/path/to/client.pem'
// var client_key_path = '/full/path/to/client-key.pem'

// Create a client with SSL/TLS enabled
var { Client } = require("@opensearch-project/opensearch");
var fs = require("fs"); // Without security, remove this line
var client = new Client({
  // Without security, use node: protocol + "://" + host + ":" + port,
  node: protocol + "://" + auth + "@" + host + ":" + port,
  ssl: { // Without security, remove the ssl block
    ca: fs.readFileSync(ca_certs_path),
    // You can turn off certificate verification (rejectUnauthorized: false) if you're using
    // self-signed certificates with a hostname mismatch.
    // cert: fs.readFileSync(client_cert_path),
    // key: fs.readFileSync(client_key_path)
  },
});

async function main() {
  // Create the index
  var index_name = "students";
  console.log("Creating index......");
  var response = await client.indices.create({
    index: index_name,
    body: {
      settings: {
        index: {
          number_of_shards: 1,
          number_of_replicas: 1,
        },
      },
      mappings: {
        properties: {
          gradDate: { type: "date", format: "yyyy-MM-dd" },
        },
      },
    },
  });
  console.log("Index created: " + response.body.index);

  // Index a document
  console.log("\nIndexing one student......");
  var student = { firstName: "John", lastName: "Doe", gpa: 3.89, gradDate: "2022-05-15" };
  response = await client.index({
    index: index_name,
    id: "1",
    body: student,
    refresh: true,
  });
  console.log("Result: " + response.body.result + ", id: " + response.body._id + ", version: " + response.body._version);

  // Bulk index documents
  console.log("\nIndexing many students......");
  response = await client.bulk({
    body: [
      { index: { _index: index_name, _id: "2" } },
      { firstName: "Paulo", lastName: "Santos", gpa: 3.93, gradDate: "2021-05-20" },
      { index: { _index: index_name, _id: "3" } },
      { firstName: "Shirley", lastName: "Rodriguez", gpa: 3.91, gradDate: "2019-05-10" },
    ],
    refresh: true,
  });
  console.log("Errors: " + response.body.errors);
  response.body.items.forEach((item) =>
    console.log("  " + item.index.result + " id: " + item.index._id));

  // Search for all students
  console.log("\nSearching for all students......");
  response = await client.search({
    index: index_name,
    body: {
      from: 0,
      size: 2,
      sort: [{ gradDate: "asc" }],
    },
  });
  console.log("Total hits: " + response.body.hits.total.value);
  console.log("Page 1:");
  response.body.hits.hits.forEach((hit) => console.log("  " + JSON.stringify(hit._source)));
  response = await client.search({
    index: index_name,
    body: {
      from: 2,
      size: 2,
      sort: [{ gradDate: "asc" }],
    },
  });
  console.log("Page 2:");
  response.body.hits.hits.forEach((hit) => console.log("  " + JSON.stringify(hit._source)));

  // Search for students who graduated in 2019
  console.log("\nSearching for students who graduated in 2019......");
  response = await client.search({
    index: index_name,
    body: {
      query: {
        range: {
          gradDate: {
            gte: "2019-01-01",
            lte: "2019-12-31",
          },
        },
      },
    },
  });
  console.log("Total hits: " + response.body.hits.total.value);
  response.body.hits.hits.forEach((hit) => console.log("  " + JSON.stringify(hit._source)));

  // Update a document
  console.log("\nUpdating a student's GPA......");
  response = await client.update({
    index: index_name,
    id: "1",
    body: {
      doc: { gpa: 3.92 },
    },
  });
  console.log("Result: " + response.body.result + ", version: " + response.body._version);

  // Get the updated document
  response = await client.get({
    index: index_name,
    id: "1",
  });
  console.log("Updated document: " + JSON.stringify(response.body._source));

  // Delete a document
  console.log("\nDeleting a student......");
  response = await client.delete({
    index: index_name,
    id: "3",
    refresh: true,
  });
  console.log("Result: " + response.body.result);

  // Delete the index
  console.log("\nDeleting the index......");
  response = await client.indices.delete({
    index: index_name,
  });
  console.log("Acknowledged: " + response.body.acknowledged);
}

main().catch(console.log);
```
{% include copy.html %}

此程式會產生下列輸出：

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
  {"firstName":"Shirley","lastName":"Rodriguez","gpa":3.91,"gradDate":"2019-05-10"}
  {"firstName":"Paulo","lastName":"Santos","gpa":3.93,"gradDate":"2021-05-20"}
Page 2:
  {"firstName":"John","lastName":"Doe","gpa":3.89,"gradDate":"2022-05-15"}

Searching for students who graduated in 2019......
Total hits: 1
  {"firstName":"Shirley","lastName":"Rodriguez","gpa":3.91,"gradDate":"2019-05-10"}

Updating a student's GPA......
Result: updated, version: 2
Updated document: {"firstName":"John","lastName":"Doe","gpa":3.92,"gradDate":"2022-05-15"}

Deleting a student......
Result: deleted

Deleting the index......
Acknowledged: true
```

## 斷路器

`memoryCircuitBreaker` 選項可用來防止因回應承載過大、無法放入用戶端可用的堆積記憶體而導致的錯誤。

`memoryCircuitBreaker` 物件包含兩個欄位：

- `enabled`：用於開啟或關閉斷路器的布林值。預設為 `false`。
- `maxPercentage`：決定斷路器是否啟動的閾值。有效值為 [0, 1] 範圍內的浮點數，以小數形式表示百分比。任何超出該範圍的值都會被修正為 `1.0`。

下列範例會建立一個已啟用斷路器的用戶端執行個體，並將其閾值設定為可用堆積大小上限的 80%：

```javascript
var client = new Client({
  memoryCircuitBreaker: {
    enabled: true,
    maxPercentage: 0.8,
  },
});
```
{% include copy.html %}

## 相關文件

- 若要使用用戶端的輔助方法大量編製索引、更新及刪除文件，請參閱[輔助方法]({{site.url}}{{site.baseurl}}/clients/javascript/helpers/)。
- 如需更多使用用戶端的範例，請參閱 [`opensearch-js` 使用者指南](https://github.com/opensearch-project/opensearch-js/blob/main/USER_GUIDE.md)。
- 如需特定工作（例如大量編製索引與搜尋）的指南，請參閱 [`opensearch-js` 指南](https://github.com/opensearch-project/opensearch-js/tree/main/guides)。
- 如需完整的範例應用程式，請參閱 [`opensearch-js` 範例](https://github.com/opensearch-project/opensearch-js/tree/main/samples)。
