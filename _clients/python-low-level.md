---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "Python 用戶端"
nav_order: 10
has_children: true
has_toc: false
redirect_from: 
  - /clients/python/
---

# Python 用戶端

OpenSearch 低階 Python 用戶端 (`opensearch-py`) 為 OpenSearch REST API 提供封裝方法，讓您能夠在 Python 中以更自然的方式與叢集互動。您不需要將原始 HTTP 請求傳送至指定的 URL，而是可以為您的叢集建立 OpenSearch 用戶端，並呼叫用戶端的內建函式。

本入門指南說明如何連線至 OpenSearch、將文件編製索引，以及執行查詢。如需更多資訊，請參閱下列資源：
- [OpenSearch Python 儲存庫](https://github.com/opensearch-project/opensearch-py)
- [API 參考](https://opensearch-project.github.io/opensearch-py/api-ref.html)
- [使用者指南](https://github.com/opensearch-project/opensearch-py/tree/main/guides)
- [範例](https://github.com/opensearch-project/opensearch-py/tree/main/samples)

如果您有任何問題或想要參與貢獻，可以[建立 issue](https://github.com/opensearch-project/opensearch-py/issues) 直接與 OpenSearch Python 團隊互動。

## 安裝 Python 用戶端

用戶端的最新版本 `opensearch-py` 3.2.0 需要 Python 3.10 或更新版本。若要將用戶端加入您的專案，請使用 [pip](https://pip.pypa.io/) 安裝：

```bash
pip install opensearch-py
```
{% include copy.html %}

安裝用戶端後，您可以像其他模組一樣匯入它：

```python
from opensearchpy import OpenSearch
```
{% include copy.html %}

## 範例資料

本頁的範例使用學生文件。每份文件都是一個 Python 字典，包含 `firstName`、`lastName`、`gpa` 和 `gradDate` 欄位。例如，下列字典代表一名學生：

```python
document = {'firstName': 'John', 'lastName': 'Doe', 'gpa': 3.89, 'gradDate': '2022-05-15'}
```
{% include copy.html %}

## 連線至 OpenSearch

若要連線至預設的 OpenSearch 主機，如果您使用 Security 外掛程式，請建立啟用 SSL 的用戶端物件。將 `<custom-admin-password>` 替換為您在安裝 OpenSearch 時設定的管理員密碼：

```python
host = 'localhost'
port = 9200
auth = ('admin', '<custom-admin-password>') # For testing only. Don't store credentials in code.
ca_certs_path = '/full/path/to/root-ca.pem' # Provide a CA bundle if you use intermediate CAs with your root CA.

# Create the client with SSL/TLS enabled, but hostname verification disabled.
client = OpenSearch(
    hosts = [{'host': host, 'port': port}],
    http_compress = True, # enables gzip compression for request bodies
    http_auth = auth,
    use_ssl = True,
    verify_certs = True,
    ssl_assert_hostname = False,
    ssl_show_warn = False,
    ca_certs = ca_certs_path
)
```
{% include copy.html %}

如果您有自己的用戶端憑證，請在 `client_cert_path` 和 `client_key_path` 參數中指定它們：

```python
host = 'localhost'
port = 9200
auth = ('admin', '<custom-admin-password>') # For testing only. Don't store credentials in code.
ca_certs_path = '/full/path/to/root-ca.pem' # Provide a CA bundle if you use intermediate CAs with your root CA.

# Optional client certificates if you don't want to use HTTP basic authentication.
client_cert_path = '/full/path/to/client.pem'
client_key_path = '/full/path/to/client-key.pem'

# Create the client with SSL/TLS enabled, but hostname verification disabled.
client = OpenSearch(
    hosts = [{'host': host, 'port': port}],
    http_compress = True, # enables gzip compression for request bodies
    http_auth = auth,
    client_cert = client_cert_path,
    client_key = client_key_path,
    use_ssl = True,
    verify_certs = True,
    ssl_assert_hostname = False,
    ssl_show_warn = False,
    ca_certs = ca_certs_path
)
```
{% include copy.html %}

如果您沒有使用 Security 外掛程式，請建立停用 SSL 的用戶端物件：

```python
host = 'localhost'
port = 9200

# Create the client with SSL/TLS and hostname verification disabled.
client = OpenSearch(
    hosts = [{'host': host, 'port': port}],
    http_compress = True, # enables gzip compression for request bodies
    use_ssl = False,
    verify_certs = False,
    ssl_assert_hostname = False,
    ssl_show_warn = False
)
```
{% include copy.html %}

## 連線至 Amazon OpenSearch Service

若要使用 IAM 憑證簽署對 Amazon OpenSearch Service 或 Amazon OpenSearch Serverless 的請求，請安裝 AWS SDK for Python (Boto3)：

```bash
pip install boto3
```
{% include copy.html %}

在下列範例中，請將端點替換為您的網域端點，該端點列於 Amazon OpenSearch Service 主控台中網域的詳細資訊頁面。

下列範例示範如何使用 IAM 憑證連線至 Amazon OpenSearch Service：

```python
from opensearchpy import OpenSearch, RequestsHttpConnection, RequestsAWSV4SignerAuth
import boto3

host = 'search-<domain-name>-<id>.us-east-1.es.amazonaws.com' # Domain endpoint without https://
region = 'us-east-1'
service = 'es'
credentials = boto3.Session().get_credentials()
auth = RequestsAWSV4SignerAuth(credentials, region, service)

client = OpenSearch(
    hosts = [{'host': host, 'port': 443}],
    http_auth = auth,
    use_ssl = True,
    verify_certs = True,
    connection_class = RequestsHttpConnection,
    pool_maxsize = 20
)
```
{% include copy.html %}

若要透過 HTTP 使用使用者名稱和密碼連線至 Amazon OpenSearch Service，請使用下列程式碼：

```python
from opensearchpy import OpenSearch

host = 'search-<domain-name>-<id>.us-east-1.es.amazonaws.com' # Domain endpoint without https://
auth = ('admin', '<custom-admin-password>') # For testing only. Don't store credentials in code.

client = OpenSearch(
    hosts=[{"host": host, "port": 443}],
    http_auth=auth,
    http_compress=True,  # enables gzip compression for request bodies
    use_ssl=True,
    verify_certs=True,
    ssl_assert_hostname=False,
    ssl_show_warn=False,
)
```
{% include copy.html %}

## 連線至 Amazon OpenSearch Serverless

在下列範例中，請將端點替換為您的集合端點，該端點列於 Amazon OpenSearch Service 主控台中集合的詳細資訊頁面。

下列範例示範如何連線至 Amazon OpenSearch Serverless：

```python
from opensearchpy import OpenSearch, RequestsHttpConnection, RequestsAWSV4SignerAuth
import boto3

host = '<collection-id>.us-east-1.aoss.amazonaws.com' # Collection endpoint without https://
region = 'us-east-1'
service = 'aoss'
credentials = boto3.Session().get_credentials()
auth = RequestsAWSV4SignerAuth(credentials, region, service)

client = OpenSearch(
    hosts = [{'host': host, 'port': 443}],
    http_auth = auth,
    use_ssl = True,
    verify_certs = True,
    connection_class = RequestsHttpConnection,
    pool_maxsize = 20
)
```
{% include copy.html %}

Amazon OpenSearch Serverless 支援 OpenSearch API 操作的子集，且不支援本頁範例中使用的 `refresh` 參數。如需更多資訊，請參閱 [Amazon OpenSearch Serverless 支援的操作與外掛程式](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/serverless-genref.html)。
{: .note}

## 建立索引

下列範例建立一個具有一個主要分片和一個副本的索引。它將 `gradDate` 欄位明確對應為 `yyyy-MM-dd` 格式的 `date`。當您將文件編製索引時，OpenSearch 會動態對應其他文件欄位：

```python
index_name = 'students'
index_body = {
    'settings': {
        'index': {
            'number_of_shards': 1,
            'number_of_replicas': 1
        }
    },
    'mappings': {
        'properties': {
            'gradDate': {'type': 'date', 'format': 'yyyy-MM-dd'}
        }
    }
}
response = client.indices.create(index=index_name, body=index_body)
```
{% include copy.html %}

## 將文件編製索引

若要從[範例資料](#sample-data)將 `document` 字典編製索引，請使用 `client.index()` 方法：

```python
response = client.index(index=index_name, id='1', body=document, refresh=True)
```
{% include copy.html %}

## 執行大量操作

您可以使用用戶端的 `bulk()` 方法同時執行多項操作。這些操作的類型可以相同，也可以不同。請以清單形式提供操作，其中每個動作後面接著其文件：

```python
operations = [
    {'index': {'_index': index_name, '_id': '2'}},
    {'firstName': 'Paulo', 'lastName': 'Santos', 'gpa': 3.93, 'gradDate': '2021-05-20'},
    {'index': {'_index': index_name, '_id': '3'}},
    {'firstName': 'Shirley', 'lastName': 'Rodriguez', 'gpa': 3.91, 'gradDate': '2019-05-10'}
]
response = client.bulk(body=operations, refresh=True)
```
{% include copy.html %}

## 搜尋文件

若要在索引中搜尋所有文件，請使用 `client.search()` 方法，不需提供查詢：

```python
response = client.search(index=index_name)
```
{% include copy.html %}

回應是字典，而 `response['hits']['hits']` 中的每個項目都是字典，其中 `_id` 鍵包含文件 ID，`_source` 鍵則包含文件欄位：

```python
for hit in response['hits']['hits']:
    source = hit['_source']
    print(f"ID: {hit['_id']}, name: {source['firstName']} {source['lastName']}, GPA: {source['gpa']}, graduation date: {source['gradDate']}")
```
{% include copy.html %}

若要使用查詢進行搜尋，請在請求本文中提供查詢。下列程式碼使用範圍查詢來搜尋 2019 年畢業的學生：

```python
query = {'query': {'range': {'gradDate': {'gte': '2019-01-01', 'lte': '2019-12-31'}}}}
response = client.search(index=index_name, body=query)
```
{% include copy.html %}

## 將結果分頁

若要將結果分頁，請使用 `from` 和 `size` 參數。下列範例依畢業日期排序學生，並一次擷取兩筆結果。第一個請求會傳回第一頁結果，第二個請求則會傳回下一頁：

```python
response = client.search(index=index_name, body={'from': 0, 'size': 2, 'sort': [{'gradDate': 'asc'}]})
next_response = client.search(index=index_name, body={'from': 2, 'size': 2, 'sort': [{'gradDate': 'asc'}]})
for page in [response, next_response]:
    for hit in page['hits']['hits']:
        print(hit['_source'])
```
{% include copy.html %}

`from` 和 `size` 參數適用於結果的前幾頁。若要對大量結果進行分頁，請使用時間點功能搭配 `search_after`。如需更多資訊，請參閱[將結果分頁]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/paginate/)。

## 更新文件

您可以使用 `client.update()` 方法更新文件。`doc` 物件中的欄位會合併到現有文件中：

```python
response = client.update(index=index_name, id='1', body={'doc': {'gpa': 3.92}})
```
{% include copy.html %}

## 刪除文件

您可以使用 `client.delete()` 方法刪除文件：

```python
response = client.delete(index=index_name, id='3', refresh=True)
```
{% include copy.html %}

## 刪除索引

您可以使用 `client.indices.delete()` 方法刪除索引：

```python
response = client.indices.delete(index=index_name)
```
{% include copy.html %}

## 範例程式

此範例程式結合了前述各節的程式碼。它會連線到已啟用 Security 外掛程式的叢集。若要連線到未啟用 Security 外掛程式的叢集，請變更標有 `# Without security` 註解的行。

此範例程式僅供測試之用。它會在程式碼中指定登入憑證。在正式環境中，請從安全的位置載入登入憑證。
{: .warning}

下列範例程式會建立用戶端、建立索引、個別及大量地將文件編製索引、搜尋文件、更新文件、刪除文件，然後刪除索引：

```python
import json
from opensearchpy import OpenSearch

host = 'localhost'
port = 9200
# Without security, remove this line
auth = ('admin', '<custom-admin-password>')
# Without security, remove this line
ca_certs_path = '/full/path/to/root-ca.pem' # Provide a CA bundle if you use intermediate CAs with your root CA.

# Create the client with SSL/TLS enabled, but hostname verification disabled.
client = OpenSearch(
    hosts = [{'host': host, 'port': port}],
    http_compress = True, # enables gzip compression for request bodies
    http_auth = auth, # Without security, remove this line
    use_ssl = True, # Without security, use use_ssl = False
    verify_certs = True, # Without security, use verify_certs = False
    ssl_assert_hostname = False,
    ssl_show_warn = False,
    ca_certs = ca_certs_path # Without security, remove this line
)

# Create the index.
index_name = 'students'
index_body = {
    'settings': {
        'index': {
            'number_of_shards': 1,
            'number_of_replicas': 1
        }
    },
    'mappings': {
        'properties': {
            'gradDate': {'type': 'date', 'format': 'yyyy-MM-dd'}
        }
    }
}
print('Creating index......')
response = client.indices.create(index=index_name, body=index_body)
print(f"Index created: {response['index']}")

# Index a document.
print('\nIndexing one student......')
document = {'firstName': 'John', 'lastName': 'Doe', 'gpa': 3.89, 'gradDate': '2022-05-15'}
response = client.index(index=index_name, id='1', body=document, refresh=True)
print(f"Result: {response['result']}, id: {response['_id']}, version: {response['_version']}")

# Bulk index documents.
print('\nIndexing many students......')
operations = [
    {'index': {'_index': index_name, '_id': '2'}},
    {'firstName': 'Paulo', 'lastName': 'Santos', 'gpa': 3.93, 'gradDate': '2021-05-20'},
    {'index': {'_index': index_name, '_id': '3'}},
    {'firstName': 'Shirley', 'lastName': 'Rodriguez', 'gpa': 3.91, 'gradDate': '2019-05-10'}
]
response = client.bulk(body=operations, refresh=True)
print(f"Errors: {str(response['errors']).lower()}")
for item in response['items']:
    print(f"  {item['index']['result']} id: {item['index']['_id']}")

# Search for all students.
print('\nSearching for all students......')
for page, start in enumerate([0, 2], start=1):
    response = client.search(index=index_name, body={'from': start, 'size': 2, 'sort': [{'gradDate': 'asc'}]})
    if page == 1:
        print(f"Total hits: {response['hits']['total']['value']}")
    print(f"Page {page}:")
    for hit in response['hits']['hits']:
        print(f"  {json.dumps(hit['_source'], separators=(',', ':'))}")

# Search for students who graduated in 2019.
print('\nSearching for students who graduated in 2019......')
query = {'query': {'range': {'gradDate': {'gte': '2019-01-01', 'lte': '2019-12-31'}}}}
response = client.search(index=index_name, body=query)
print(f"Total hits: {response['hits']['total']['value']}")
for hit in response['hits']['hits']:
    print(f"  {json.dumps(hit['_source'], separators=(',', ':'))}")

# Update a document.
print("\nUpdating a student's GPA......")
response = client.update(index=index_name, id='1', body={'doc': {'gpa': 3.92}})
print(f"Result: {response['result']}, version: {response['_version']}")

# Get the updated document.
response = client.get(index=index_name, id='1')
print(f"Updated document: {json.dumps(response['_source'], separators=(',', ':'))}")

# Delete a document.
print('\nDeleting a student......')
response = client.delete(index=index_name, id='3', refresh=True)
print(f"Result: {response['result']}")

# Delete the index.
print('\nDeleting the index......')
response = client.indices.delete(index=index_name)
print(f"Acknowledged: {str(response['acknowledged']).lower()}")
```
{% include copy.html %}

該程式會產生下列輸出：

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

- 若要從 Python 分析資料並上傳 ML 模型，請參閱 [Python ML 用戶端]({{site.url}}{{site.baseurl}}/clients/opensearch-py-ml/)。
- 如需用戶端 API 參考資料，請參閱 [`opensearch-py` API 文件](https://opensearch-project.github.io/opensearch-py/)。
- 如需更多使用用戶端的範例，請參閱 [`opensearch-py` 使用者指南](https://github.com/opensearch-project/opensearch-py/blob/main/USER_GUIDE.md)。
- 如需特定工作的指南，例如大量編製索引和搜尋，請參閱 [`opensearch-py` 指南](https://github.com/opensearch-project/opensearch-py/tree/main/guides)。
- 如需完整的範例應用程式，請參閱 [`opensearch-py` 範例](https://github.com/opensearch-project/opensearch-py/tree/main/samples)。
