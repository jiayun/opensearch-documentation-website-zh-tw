---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "高階 Python 用戶端（已棄用）"
nav_order: 200
---

# 高階 Python 用戶端

OpenSearch 高階 Python 用戶端（`opensearch-dsl-py`）已棄用，其儲存庫也已封存。我們建議改用 [Python 用戶端（`opensearch-py`）]({{site.url}}{{site.baseurl}}/clients/python-low-level/)，該用戶端現在已包含 `opensearch-dsl-py` 的功能。
{: .warning}

OpenSearch 高階 Python 用戶端（`opensearch-dsl-py`）為文件等常見的 OpenSearch 實體提供包裝類別，讓您可以將這些實體當作 Python 物件來操作。此外，高階用戶端可簡化查詢的撰寫，並提供便利的 Python 方法來執行常見的 OpenSearch 操作。高階 Python 用戶端支援建立文件並將其編製索引、使用或不使用篩選器進行搜尋，以及使用查詢更新文件。

本入門指南說明如何連線至 OpenSearch、將文件編製索引，以及執行查詢。如需用戶端的原始碼，請參閱 [`opensearch-dsl-py` 儲存庫](https://github.com/opensearch-project/opensearch-dsl-py)。

## 設定

若要將用戶端加入您的專案，請使用 [pip](https://pip.pypa.io/) 安裝：

```bash
pip install opensearch-dsl
```
{% include copy.html %}

安裝用戶端後，您可以像匯入其他模組一樣匯入它：

```python
from opensearchpy import OpenSearch
from opensearch_dsl import Search, Document, Text, Keyword
```
{% include copy.html %}

## 連線至 OpenSearch

若要連線至預設的 OpenSearch 主機，請建立用戶端物件；如果您使用 Security 外掛程式，請啟用 SSL。將 `<custom-admin-password>` 替換為您安裝 OpenSearch 時設定的管理員密碼：

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

如果您有自己的用戶端憑證，請在 `client_cert_path` 和 `client_key_path` 參數中指定：

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

如果您未使用 Security 外掛程式，請建立停用 SSL 的用戶端物件：

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

## 建立索引

若要建立 OpenSearch 索引，請使用 `client.indices.create()` 方法。您可以使用下列程式碼建構具有自訂設定的 JSON 物件：

```python
index_name = 'my-dsl-index'
index_body = {
  'settings': {
    'index': {
      'number_of_shards': 4
    }
  }
}

response = client.indices.create(index=index_name, body=index_body)
```
{% include copy.html %}

## 將文件編製索引

您可以透過繼承 `Document` 類別來建立一個類別，代表您將在 OpenSearch 中編製索引的文件：

```python
class Movie(Document):
    title = Text(fields={'raw': Keyword()})
    director = Text()
    year = Text()

    class Index:
        name = index_name

    def save(self, ** kwargs):
        return super(Movie, self).save(** kwargs)
```
{% include copy.html %}

若要將文件編製索引，請建立新類別的物件，並呼叫其 `save()` 方法：

```python
# Set up the opensearch-py version of the document
Movie.init(using=client)
doc = Movie(meta={'id': 1}, title='Moneyball', director='Bennett Miller', year='2011')
response = doc.save(using=client)
```
{% include copy.html %}

## 執行批次操作

您可以使用用戶端的 `bulk()` 方法同時執行多項操作。這些操作可以是相同類型，也可以是不同類型。請注意，各項操作必須以 `\n` 分隔，而且整個字串必須位於同一行：

```python
movies = '{ "index" : { "_index" : "my-dsl-index", "_id" : "2" } } \n { "title" : "Interstellar", "director" : "Christopher Nolan", "year" : "2014"} \n { "create" : { "_index" : "my-dsl-index", "_id" : "3" } } \n { "title" : "Star Trek Beyond", "director" : "Justin Lin", "year" : "2015"} \n { "update" : {"_id" : "3", "_index" : "my-dsl-index" } } \n { "doc" : {"year" : "2016"} }'

client.bulk(body=movies)
```
{% include copy.html %}

## 搜尋文件

您可以使用 `Search` 類別來建構查詢。下列程式碼會建立包含篩選器的布林值查詢：

```python
s = Search(using=client, index=index_name) \
    .filter("term", year="2011") \
    .query("match", title="Moneyball")

response = s.execute()
```
{% include copy.html %}

上述查詢等同於下列以 OpenSearch 領域特定語言（DSL）撰寫的查詢：

```json
GET my-dsl-index/_search 
{
  "query": {
    "bool": {
      "must": {
        "match": {
          "title": "Moneyball"
        }
      },
      "filter": {
        "term" : {
          "year": 2011
        }
      }
    }
  }
}
```

## 刪除文件

您可以使用 `client.delete()` 方法刪除文件：

```python
response = client.delete(
    index = 'my-dsl-index',
    id = '1'
)
```
{% include copy.html %}

## 刪除索引

您可以使用 `client.indices.delete()` 方法刪除索引：

```python
response = client.indices.delete(
    index = 'my-dsl-index'
)
```
{% include copy.html %}

## 範例程式

下列範例程式會建立用戶端、新增具有非預設設定的索引、插入文件、執行批次操作、搜尋該文件、刪除該文件，然後刪除索引：

```python
from opensearchpy import OpenSearch
from opensearch_dsl import Search, Document, Text, Keyword

host = 'localhost'
port = 9200

auth = ('admin', '<custom-admin-password>')  # For testing only. Don't store credentials in code.
ca_certs_path = 'root-ca.pem'

# Create the client with SSL/TLS enabled, but hostname verification disabled.
client = OpenSearch(
    hosts=[{'host': host, 'port': port}],
    http_compress=True,  # enables gzip compression for request bodies
    # http_auth=auth,
    use_ssl=False,
    verify_certs=False,
    ssl_assert_hostname=False,
    ssl_show_warn=False,
    # ca_certs=ca_certs_path
)
index_name = 'my-dsl-index'

index_body = {
  'settings': {
    'index': {
      'number_of_shards': 4
    }
  }
}

response = client.indices.create(index=index_name, body=index_body)
print('\nCreating index:')
print(response)

# Create the structure of the document
class Movie(Document):
    title = Text(fields={'raw': Keyword()})
    director = Text()
    year = Text()

    class Index:
        name = index_name

    def save(self, ** kwargs):
        return super(Movie, self).save(** kwargs)

# Set up the opensearch-py version of the document
Movie.init(using=client)
doc = Movie(meta={'id': 1}, title='Moneyball', director='Bennett Miller', year='2011')
response = doc.save(using=client)

print('\nAdding document:')
print(response)

# Perform bulk operations

movies = '{ "index" : { "_index" : "my-dsl-index", "_id" : "2" } } \n { "title" : "Interstellar", "director" : "Christopher Nolan", "year" : "2014"} \n { "create" : { "_index" : "my-dsl-index", "_id" : "3" } } \n { "title" : "Star Trek Beyond", "director" : "Justin Lin", "year" : "2015"} \n { "update" : {"_id" : "3", "_index" : "my-dsl-index" } } \n { "doc" : {"year" : "2016"} }'

client.bulk(body=movies)

# Search for the document.
s = Search(using=client, index=index_name) \
    .filter('term', year='2011') \
    .query('match', title='Moneyball')

response = s.execute()

print('\nSearch results:')
for hit in response:
    print(hit.meta.score, hit.title)
    
# Delete the document.
print('\nDeleting document:')
print(response)

# Delete the index.
response = client.indices.delete(
    index = index_name
)

print('\nDeleting index:')
print(response)
```
{% include copy.html %}