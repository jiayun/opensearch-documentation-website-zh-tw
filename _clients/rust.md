---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "Rust 用戶端"
nav_order: 100
---

# Rust 用戶端

OpenSearch Rust 用戶端可讓您將 Rust 應用程式連線至 OpenSearch 叢集中的資料。如需用戶端的完整 API 文件與更多範例，請參閱 [OpenSearch docs.rs 文件](https://docs.rs/opensearch/)。

本入門指南說明如何連線至 OpenSearch、將文件編製索引，以及執行查詢。用戶端的原始碼請參閱 [`opensearch-rs` 儲存庫](https://github.com/opensearch-project/opensearch-rs)。

## 安裝 Rust 用戶端

如果您要開始新專案，請將 `opensearch` crate 加入 Cargo.toml：

```toml
[dependencies]
opensearch = "2.4.0"
```
{% include copy.html %}

此外，您可能想要加入下列 `serde` 相依套件，以協助將型別序列化為 JSON，並將 JSON 回應還原序列化。`derive` 功能可讓您為自己的結構衍生 `Serialize` 與 `Deserialize`：

```toml
serde = { version = "~1", features = ["derive"] }
serde_json = "~1"
```
{% include copy.html %}

Rust 用戶端使用較高階的 [`reqwest`](https://crates.io/crates/reqwest) HTTP 用戶端程式庫來傳送 HTTP 請求，而 `reqwest` 則使用 [`tokio`](https://crates.io/crates/tokio) 平台來支援非同步請求。如果您打算使用非同步函式，則需要在 Cargo.toml 中加入 `tokio` 相依套件：

```toml
tokio = { version = "1", features = ["full"] }
```
{% include copy.html %}

完整的 Cargo.toml 檔案請參閱[範例程式](#sample-program)一節。

若要使用 Rust 用戶端 API，請匯入您需要的模組、結構與列舉：

```rust
use opensearch::OpenSearch;
```
{% include copy.html %}

## 範例資料

本頁的範例使用 `Student` 結構來表示文件。`#[serde(rename_all = "camelCase")]` 屬性會將結構欄位序列化為 `firstName`、`lastName`、`gpa` 與 `gradDate` JSON 欄位：

```rust
use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
struct Student {
    first_name: String,
    last_name: String,
    gpa: f64,
    grad_date: String,
}

impl Student {
    fn new(first_name: &str, last_name: &str, gpa: f64, grad_date: &str) -> Self {
        Student {
            first_name: first_name.to_string(),
            last_name: last_name.to_string(),
            gpa,
            grad_date: grad_date.to_string(),
        }
    }
}
```
{% include copy.html %}

## 連線至 OpenSearch

若要連線至預設的 OpenSearch 主機，請建立一個預設的用戶端物件，該物件會連線至位於 `http://localhost:9200` 位址的 OpenSearch：

```rust
let client = OpenSearch::default();
```
{% include copy.html %}

本頁其餘的連線範例需要下列匯入：

```rust
use opensearch::{
    http::transport::{SingleNodeConnectionPool, Transport, TransportBuilder},
    http::Url,
    OpenSearch,
};
```
{% include copy.html %}

若要連線至執行於不同位址的 OpenSearch 主機，請使用指定的位址建立用戶端：

```rust
let transport = Transport::single_node("http://localhost:9200")?;
let client = OpenSearch::new(transport);
```
{% include copy.html %}

或者，您可以建立 `TransportBuilder` 結構並將其傳遞給 `OpenSearch::new` 來建立新的用戶端執行個體，以自訂 URL 並使用連線集區：

```rust
let url = Url::parse("http://localhost:9200")?;
let conn_pool = SingleNodeConnectionPool::new(url);
let transport = TransportBuilder::new(conn_pool).disable_proxy().build()?;
let client = OpenSearch::new(transport);
```
{% include copy.html %}

若要連線至已啟用 Security 外掛程式的叢集，請使用 HTTPS 並提供基本驗證憑證。下列範例也會停用憑證驗證，讓用戶端接受自我簽署的示範憑證。請從 `opensearch::auth` 匯入 `Credentials`，並從 `opensearch::cert` 匯入 `CertificateValidation`：

```rust
let url = Url::parse("https://localhost:9200")?;
let conn_pool = SingleNodeConnectionPool::new(url);
let transport = TransportBuilder::new(conn_pool)
    // Only for demo purposes. Don't specify your credentials in code.
    .auth(Credentials::Basic(
        "admin".to_string(),
        "<custom-admin-password>".to_string(),
    ))
    // Only for demo purposes. Disables certificate validation for self-signed certificates.
    .cert_validation(CertificateValidation::None)
    .build()?;
let client = OpenSearch::new(transport);
```
{% include copy.html %}

## 連線至 Amazon OpenSearch Service

若要使用 AWS Signature Version 4 簽署請求，請啟用 `opensearch` crate 的 `aws-auth` 功能，並在 Cargo.toml 中加入 `aws-config` 相依套件：

```toml
opensearch = { version = "2.4.0", features = ["aws-auth"] }
aws-config = "1"
```
{% include copy.html %}

然後匯入 AWS 組態型別：

```rust
use aws_config::{meta::region::RegionProviderChain, BehaviorVersion};
```
{% include copy.html %}

在下列範例中，請將端點替換為您的網域端點，該端點列於 Amazon OpenSearch Service 主控台中網域的詳細資料頁面。

下列範例說明如何連線至 Amazon OpenSearch Service：

```rust
let url = Url::parse("https://search-<domain-name>-<id>.us-east-1.es.amazonaws.com")?;
let service_name = "es";
let conn_pool = SingleNodeConnectionPool::new(url);
let region_provider = RegionProviderChain::default_provider().or_else("us-east-1");
let aws_config = aws_config::defaults(BehaviorVersion::latest())
    .region(region_provider)
    .load()
    .await;
let transport = TransportBuilder::new(conn_pool)
    .auth(aws_config.try_into()?)
    .service_name(service_name)
    .build()?;
let client = OpenSearch::new(transport);
```
{% include copy.html %}

## 連線至 Amazon OpenSearch Serverless

在下列範例中，請將端點替換為您的集合端點，該端點列於 Amazon OpenSearch Service 主控台中集合的詳細資料頁面。

連線至 Amazon OpenSearch Serverless 需要與[連線至 Amazon OpenSearch Service](#connecting-to-amazon-opensearch-service)相同的 `aws-auth` 功能、`aws-config` 相依套件與匯入。下列範例說明如何連線至 Amazon OpenSearch Serverless：

```rust
let url = Url::parse("https://<collection-id>.us-east-1.aoss.amazonaws.com")?;
let service_name = "aoss";
let conn_pool = SingleNodeConnectionPool::new(url);
let region_provider = RegionProviderChain::default_provider().or_else("us-east-1");
let aws_config = aws_config::defaults(BehaviorVersion::latest())
    .region(region_provider)
    .load()
    .await;
let transport = TransportBuilder::new(conn_pool)
    .auth(aws_config.try_into()?)
    .service_name(service_name)
    .build()?;
let client = OpenSearch::new(transport);
```
{% include copy.html %}

Amazon OpenSearch Serverless 支援 OpenSearch API 操作的子集，且不支援本頁範例中使用的 `refresh` 參數。如需更多資訊，請參閱 [Amazon OpenSearch Serverless 支援的操作與外掛程式](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/serverless-genref.html)。
{: .note}

## 建立索引

下列範例會建立一個具有一個主要分片和一個副本的索引。此範例會將 `gradDate` 欄位明確對應為 `yyyy-MM-dd` 格式的 `date`。當您將文件編製索引時，OpenSearch 會動態對應其他文件欄位：

```rust
let index = "students";
let response = client
    .indices()
    .create(IndicesCreateParts::Index(index))
    .body(json!({
        "settings": {
            "index": {
                "number_of_shards": 1,
                "number_of_replicas": 1
            }
        },
        "mappings": {
            "properties": {
                "gradDate": { "type": "date", "format": "yyyy-MM-dd" }
            }
        }
    }))
    .send()
    .await?;
```
{% include copy.html %}

## 將文件編製索引

您可以使用用戶端的 `index` 函式將文件編製索引到 OpenSearch 中。`refresh(Refresh::True)` 呼叫可讓文件立即可供搜尋。`Refresh` 定義於 `opensearch::params` 模組中：

```rust
let student = Student::new("John", "Doe", 3.89, "2022-05-15");
let response = client
    .index(IndexParts::IndexId(index, "1"))
    .body(student)
    .refresh(Refresh::True)
    .send()
    .await?;
```
{% include copy.html %}

## 執行大量操作

您可以使用用戶端的 `bulk` 函式同時執行多項操作。首先，建立 Bulk API 呼叫的 JSON 本文，然後將其傳遞給 `bulk` 函式：

```rust
let body: Vec<JsonBody<Value>> = vec![
    json!({"index": {"_id": "2"}}).into(),
    serde_json::to_value(Student::new("Paulo", "Santos", 3.93, "2021-05-20"))?.into(),
    json!({"index": {"_id": "3"}}).into(),
    serde_json::to_value(Student::new("Shirley", "Rodriguez", 3.91, "2019-05-10"))?.into(),
];
let response = client
    .bulk(BulkParts::Index(index))
    .body(body)
    .refresh(Refresh::True)
    .send()
    .await?;
```
{% include copy.html %}

## 搜尋文件

若要搜尋索引中的所有文件，請傳送不含查詢的搜尋請求：

```rust
let response = client
    .search(SearchParts::Index(&[index]))
    .send()
    .await?;
```
{% include copy.html %}

接著，您可以將回應本文讀取為 JSON，並逐一處理 `hits` 陣列，將每個 `_source` 文件還原序列化為 `Student`：

```rust
let response_body = response.json::<Value>().await?;
println!("Total hits: {}", response_body["hits"]["total"]["value"]);
for hit in response_body["hits"]["hits"].as_array().unwrap_or(&vec![]) {
    let student: Student = serde_json::from_value(hit["_source"].clone())?;
    println!("  {}", serde_json::to_string(&student)?);
}
```
{% include copy.html %}

每個 `_source` 文件都會還原序列化為 `Student` 結構，因此文件欄位可作為結構欄位使用，例如 `student.first_name`。每個命中結果都在 `hit["_id"]` 中包含文件 ID，並在 `hit["_source"]` 中包含文件。若要列印每個文件的 ID 和欄位，請使用下列程式碼：

```rust
for hit in response_body["hits"]["hits"].as_array().unwrap_or(&vec![]) {
    let id = hit["_id"].as_str().unwrap_or_default();
    let student: Student = serde_json::from_value(hit["_source"].clone())?;
    println!(
        "ID: {}, name: {} {}, GPA: {}, graduation date: {}",
        id, student.first_name, student.last_name, student.gpa, student.grad_date
    );
}
```
{% include copy.html %}

若要搜尋 2019 年畢業的學生，請對 `gradDate` 欄位使用 `range` 查詢：

```rust
let response = client
    .search(SearchParts::Index(&[index]))
    .body(json!({
        "query": {
            "range": {
                "gradDate": {
                    "gte": "2019-01-01",
                    "lte": "2019-12-31"
                }
            }
        }
    }))
    .send()
    .await?;
```
{% include copy.html %}

## 將結果分頁

若要將結果分頁，請使用 `from` 和 `size` 參數。下列範例會依畢業日期排序學生，並每次擷取兩筆結果。第一個請求會傳回第一頁結果，第二個請求會傳回下一頁：

```rust
let response = client
    .search(SearchParts::Index(&[index]))
    .from(0)
    .size(2)
    .sort(&["gradDate:asc"])
    .send()
    .await?;

let next_page = client
    .search(SearchParts::Index(&[index]))
    .from(2)
    .size(2)
    .sort(&["gradDate:asc"])
    .send()
    .await?;
```
{% include copy.html %}

`from` 和 `size` 參數適用於結果的前幾頁。若要逐頁瀏覽大量結果，請搭配 `search_after` 使用時間點 (point in time)。如需詳細資訊，請參閱[將結果分頁]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/paginate/)。

## 更新文件

您可以使用用戶端的 `update` 函式更新文件。下列範例會將 ID 為 `1` 之文件的 `gpa` 欄位設為 `3.92`：

```rust
let response = client
    .update(UpdateParts::IndexId(index, "1"))
    .body(json!({
        "doc": {
            "gpa": 3.92
        }
    }))
    .send()
    .await?;
```
{% include copy.html %}

若要擷取更新後的文件，請使用用戶端的 `get` 函式：

```rust
let response = client
    .get(GetParts::IndexId(index, "1"))
    .send()
    .await?;
```
{% include copy.html %}

## 刪除文件

您可以使用用戶端的 `delete` 函式刪除文件：

```rust
let response = client
    .delete(DeleteParts::IndexId(index, "3"))
    .refresh(Refresh::True)
    .send()
    .await?;
```
{% include copy.html %}

## 刪除索引

您可以使用 `opensearch::indices::Indices` 結構的 `delete` 函式刪除索引：

```rust
let response = client
    .indices()
    .delete(IndicesDeleteParts::Index(&[index]))
    .send()
    .await?;
```
{% include copy.html %}

## 範例程式

此範例程式結合了前述各節的程式碼。它會連線至已啟用 Security 外掛程式的叢集。若要連線至未使用 Security 外掛程式的叢集，請變更標有 `// Without security` 註解的程式行。

此範例程式使用下列 Cargo.toml 檔案，其中包含[安裝 Rust 用戶端](#installing-the-rust-client)一節所述的所有相依項目：

```toml
[package]
name = "os_rust_project"
version = "0.1.0"
edition = "2021"

# See more keys and their definitions at https://doc.rust-lang.org/cargo/reference/manifest.html

[dependencies]
opensearch = "2.4.0"
tokio = { version = "1", features = ["full"] }
serde = { version = "~1", features = ["derive"] }
serde_json = "~1"
```
{% include copy.html %}

此範例程式僅供測試使用。它在程式碼中指定認證資訊，並停用憑證驗證，以便連線至使用自我簽署憑證的叢集。在正式環境中，請從安全的位置載入認證資訊，並驗證叢集的憑證。
{: .warning}

下列範例程式會建立用戶端、建立索引、個別及大量將文件編製索引、搜尋文件、更新文件、刪除文件，然後刪除索引：

```rust
use opensearch::{
    auth::Credentials, // Without security, remove this line
    cert::CertificateValidation, // Without security, remove this line
    http::request::JsonBody,
    http::transport::{SingleNodeConnectionPool, TransportBuilder},
    http::Url,
    indices::{IndicesCreateParts, IndicesDeleteParts},
    params::Refresh,
    BulkParts, DeleteParts, GetParts, IndexParts, OpenSearch, SearchParts, UpdateParts,
};
use serde::{Deserialize, Serialize};
use serde_json::{json, Value};

#[derive(Debug, Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
struct Student {
    first_name: String,
    last_name: String,
    gpa: f64,
    grad_date: String,
}

impl Student {
    fn new(first_name: &str, last_name: &str, gpa: f64, grad_date: &str) -> Self {
        Student {
            first_name: first_name.to_string(),
            last_name: last_name.to_string(),
            gpa,
            grad_date: grad_date.to_string(),
        }
    }
}

fn print_students(response_body: &Value) -> Result<(), Box<dyn std::error::Error>> {
    for hit in response_body["hits"]["hits"].as_array().unwrap_or(&vec![]) {
        let student: Student = serde_json::from_value(hit["_source"].clone())?;
        println!("  {}", serde_json::to_string(&student)?);
    }
    Ok(())
}

fn print_hits(response_body: &Value) -> Result<(), Box<dyn std::error::Error>> {
    println!("Total hits: {}", response_body["hits"]["total"]["value"]);
    print_students(response_body)
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let url = Url::parse("https://localhost:9200")?; // Without security, use http://localhost:9200
    let conn_pool = SingleNodeConnectionPool::new(url);
    let transport = TransportBuilder::new(conn_pool)
        // Without security, remove this line
        .auth(Credentials::Basic("admin".to_string(), "<custom-admin-password>".to_string()))
        .cert_validation(CertificateValidation::None) // Without security, remove this line
        .build()?;
    let client = OpenSearch::new(transport);

    // Create the index
    let index = "students";
    println!("Creating index......");
    let response_body = client
        .indices()
        .create(IndicesCreateParts::Index(index))
        .body(json!({
            "settings": {
                "index": {
                    "number_of_shards": 1,
                    "number_of_replicas": 1
                }
            },
            "mappings": {
                "properties": {
                    "gradDate": { "type": "date", "format": "yyyy-MM-dd" }
                }
            }
        }))
        .send()
        .await?
        .json::<Value>()
        .await?;
    println!("Index created: {}", response_body["index"].as_str().unwrap_or_default());

    // Index a document
    println!("\nIndexing one student......");
    let student = Student::new("John", "Doe", 3.89, "2022-05-15");
    let response_body = client
        .index(IndexParts::IndexId(index, "1"))
        .body(student)
        .refresh(Refresh::True)
        .send()
        .await?
        .json::<Value>()
        .await?;
    println!(
        "Result: {}, id: {}, version: {}",
        response_body["result"].as_str().unwrap_or_default(),
        response_body["_id"].as_str().unwrap_or_default(),
        response_body["_version"]
    );

    // Bulk index documents
    println!("\nIndexing many students......");
    let body: Vec<JsonBody<Value>> = vec![
        json!({"index": {"_id": "2"}}).into(),
        serde_json::to_value(Student::new("Paulo", "Santos", 3.93, "2021-05-20"))?.into(),
        json!({"index": {"_id": "3"}}).into(),
        serde_json::to_value(Student::new("Shirley", "Rodriguez", 3.91, "2019-05-10"))?.into(),
    ];
    let response_body = client
        .bulk(BulkParts::Index(index))
        .body(body)
        .refresh(Refresh::True)
        .send()
        .await?
        .json::<Value>()
        .await?;
    println!("Errors: {}", response_body["errors"]);
    for item in response_body["items"].as_array().unwrap_or(&vec![]) {
        println!(
            "  {} id: {}",
            item["index"]["result"].as_str().unwrap_or_default(),
            item["index"]["_id"].as_str().unwrap_or_default()
        );
    }

    // Search for all students, two at a time, sorted by graduation date
    println!("\nSearching for all students......");
    for (page, from) in [(1, 0), (2, 2)] {
        let response_body = client
            .search(SearchParts::Index(&[index]))
            .from(from)
            .size(2)
            .sort(&["gradDate:asc"])
            .send()
            .await?
            .json::<Value>()
            .await?;
        if page == 1 {
            println!("Total hits: {}", response_body["hits"]["total"]["value"]);
        }
        println!("Page {}:", page);
        print_students(&response_body)?;
    }

    // Search for students who graduated in 2019
    println!("\nSearching for students who graduated in 2019......");
    let response_body = client
        .search(SearchParts::Index(&[index]))
        .body(json!({
            "query": {
                "range": {
                    "gradDate": {
                        "gte": "2019-01-01",
                        "lte": "2019-12-31"
                    }
                }
            }
        }))
        .send()
        .await?
        .json::<Value>()
        .await?;
    print_hits(&response_body)?;

    // Update a document
    println!("\nUpdating a student's GPA......");
    let response_body = client
        .update(UpdateParts::IndexId(index, "1"))
        .body(json!({
            "doc": {
                "gpa": 3.92
            }
        }))
        .send()
        .await?
        .json::<Value>()
        .await?;
    println!(
        "Result: {}, version: {}",
        response_body["result"].as_str().unwrap_or_default(),
        response_body["_version"]
    );

    // Get the updated document
    let response_body = client
        .get(GetParts::IndexId(index, "1"))
        .send()
        .await?
        .json::<Value>()
        .await?;
    let student: Student = serde_json::from_value(response_body["_source"].clone())?;
    println!("Updated document: {}", serde_json::to_string(&student)?);

    // Delete a document
    println!("\nDeleting a student......");
    let response_body = client
        .delete(DeleteParts::IndexId(index, "3"))
        .refresh(Refresh::True)
        .send()
        .await?
        .json::<Value>()
        .await?;
    println!("Result: {}", response_body["result"].as_str().unwrap_or_default());

    // Delete the index
    println!("\nDeleting the index......");
    let response_body = client
        .indices()
        .delete(IndicesDeleteParts::Index(&[index]))
        .send()
        .await?
        .json::<Value>()
        .await?;
    println!("Acknowledged: {}", response_body["acknowledged"]);

    Ok(())
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

## 相關文件

- 如需更多使用用戶端的範例，請參閱 [`opensearch-rs` 使用者指南](https://github.com/opensearch-project/opensearch-rs/blob/main/USER_GUIDE.md)。
- 如需大量編製索引與搜尋等特定工作的指南，請參閱 [`opensearch-rs` 指南](https://github.com/opensearch-project/opensearch-rs/tree/main/guides)。
