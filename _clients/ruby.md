---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "Ruby 用戶端"
nav_order: 60
has_children: false
---

# Ruby 用戶端

OpenSearch Ruby 用戶端讓您透過 Ruby 方法與 OpenSearch 叢集互動，而不必使用 HTTP 方法與原始 JSON。如需用戶端的完整 API 文件，請參閱 [`opensearch-ruby` 儲存庫](https://github.com/opensearch-project/opensearch-ruby)文件。如需其他範例，請參閱 [`opensearch-transport`](https://rubygems.org/gems/opensearch-transport/)、[`opensearch-api`](https://rubygems.org/gems/opensearch-api/)、[`opensearch-dsl`](https://rubygems.org/gems/opensearch-dsl/) 與 [`opensearch-ruby`](https://rubygems.org/gems/opensearch-ruby/) gem 文件。

本入門指南說明如何連線至 OpenSearch、將文件編製索引，以及執行查詢。如需用戶端原始碼，請參閱 [`opensearch-ruby` 儲存庫](https://github.com/opensearch-project/opensearch-ruby)。

## 安裝 Ruby 用戶端

若要安裝 Ruby 用戶端的 Ruby gem，請執行下列命令：

```bash
gem install opensearch-ruby
```
{% include copy.html %}

或者，將 gem 新增至您的 `Gemfile`，並執行 `bundle install`。下列範例需要用戶端 3.4.0 版或更新的 3.x 版本：

```ruby
gem 'opensearch-ruby', '~> 3.4'
```
{% include copy.html %}

若要使用用戶端，請將其匯入為模組：

```ruby
require 'opensearch'
```
{% include copy.html %}

## 連線至 OpenSearch

若要連線至預設的 OpenSearch 主機，請建立用戶端物件，並在建構函式中傳入預設主機位址：

```ruby
client = OpenSearch::Client.new(host: 'http://localhost:9200')
```
{% include copy.html %}

下列範例使用自訂 URL 建立用戶端物件，並將 `log` 選項設為 `true`。此範例設定 `retry_on_failure` 參數，將失敗請求的重試次數從預設的三次改為五次。最後，將 `request_timeout` 參數設為 120 秒，以延長逾時時間。接著傳回基本的叢集健康狀態資訊：

```ruby
client = OpenSearch::Client.new(
    url: "http://localhost:9200",
    retry_on_failure: 5,
    request_timeout: 120,
    log: true
  )

client.cluster.health
```
{% include copy.html %}

輸出如下：

```bash
2026-09-30 12:29:58 -0400: GET http://localhost:9200/ [status:200, request:0.009s, query:n/a]
2026-09-30 12:29:58 -0400: < {
  "name" : "opensearch-node1",
  "cluster_name" : "opensearch-cluster",
  "cluster_uuid" : "uwutrwdfTVeh8rroYbZh4g",
  "version" : {
    "distribution" : "opensearch",
    "number" : "3.8.0",
    "build_type" : "tar",
    "build_hash" : "e5a3c5691be87af6c12dbe3e158c59c04ee72973",
    "build_date" : "2026-08-03T21:07:36.443334696Z",
    "build_snapshot" : false,
    "lucene_version" : "10.5.0",
    "minimum_wire_compatibility_version" : "2.19.0",
    "minimum_index_compatibility_version" : "2.0.0"
  },
  "tagline" : "The OpenSearch Project: https://opensearch.org/"
}

2026-09-30 12:29:58 -0400: GET http://localhost:9200/_cluster/health [status:200, request:0.007s, query:n/a]
2026-09-30 12:29:58 -0400: < {"cluster_name":"opensearch-cluster","status":"yellow","timed_out":false,"number_of_nodes":1,"number_of_data_nodes":1,"discovered_master":true,"discovered_cluster_manager":true,"active_primary_shards":57,"active_shards":57,"relocating_shards":0,"initializing_shards":0,"unassigned_shards":28,"delayed_unassigned_shards":0,"number_of_pending_tasks":0,"number_of_in_flight_fetch":0,"task_max_waiting_in_queue_millis":0,"active_shards_percent_as_number":67.05882352941175}
```

若要連線至已啟用 Security 外掛程式的叢集，請使用 HTTPS 並提供使用者認證資訊：

```ruby
client = OpenSearch::Client.new(
    host: 'https://localhost:9200',
    user: 'admin', # Only for demo purposes. Don't specify your credentials in code.
    password: '<custom-admin-password>',
    transport_options: { ssl: { verify: false } } # For testing only. Use a certificate for validation.
)
```
{% include copy.html %}

## 連線至 Amazon OpenSearch Service

若要連線至 Amazon OpenSearch Service，請先安裝 `opensearch-aws-sigv4` gem：

```bash
gem install opensearch-aws-sigv4
```
{% include copy.html %}

接著建立用戶端。將端點替換為您的網域端點，該端點列於 Amazon OpenSearch Service 主控台中的網域詳細資料頁面：

```ruby
require 'opensearch-aws-sigv4'
require 'aws-sigv4'

signer = Aws::Sigv4::Signer.new(service: 'es',
                                region: 'us-east-1', # must match the Region in the endpoint
                                access_key_id: 'key_id',
                                secret_access_key: 'secret',
                                session_token: 'session_token') # required for temporary credentials, such as IAM roles or SSO

client = OpenSearch::Aws::Sigv4Client.new({
    host: 'https://search-<domain-name>-<id>.us-east-1.es.amazonaws.com',
    log: true
}, signer)

# create an index and document
index = 'students'
client.indices.create(index: index)
client.index(index: index, id: '1', body: { firstName: 'John',
                                            lastName: 'Doe',
                                            gpa: 3.89,
                                            gradDate: '2022-05-15' },
                                            refresh: true)

# search for the document
client.search(index: index, body: { query: { match: { firstName: 'John' } } })

# delete the document
client.delete(index: index, id: '1')

# delete the index
client.indices.delete(index: index)
```
{% include copy.html %}

## 連線至 Amazon OpenSearch Serverless

若要連線至 Amazon OpenSearch Serverless，請先安裝 `opensearch-aws-sigv4` gem：

```bash
gem install opensearch-aws-sigv4
```
{% include copy.html %}

接著建立用戶端。將端點替換為您的集合端點，該端點列於 Amazon OpenSearch Service 主控台中的集合詳細資料頁面：

```ruby
require 'opensearch-aws-sigv4'
require 'aws-sigv4'

signer = Aws::Sigv4::Signer.new(service: 'aoss',
                                region: 'us-east-1', # must match the Region in the endpoint
                                access_key_id: 'key_id',
                                secret_access_key: 'secret',
                                session_token: 'session_token') # required for temporary credentials, such as IAM roles or SSO

client = OpenSearch::Aws::Sigv4Client.new({
    host: 'https://<collection-id>.us-east-1.aoss.amazonaws.com', # Amazon OpenSearch Serverless collection endpoint
    log: true
}, signer)

# check whether an index exists
puts client.indices.exists?(index: 'students')
```
{% include copy.html %}

Amazon OpenSearch Serverless 支援部分 OpenSearch API 操作，且不支援本頁範例中使用的 `refresh` 參數。如需詳細資訊，請參閱 [Amazon OpenSearch Serverless 支援的操作與外掛程式](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/serverless-genref.html)。
{: .note}

## 建立索引

您不需要在 OpenSearch 中明確建立索引。當您將文件上傳至不存在的索引時，OpenSearch 就會自動建立該索引。若要明確建立索引，請使用 `indices.create` 方法，並在 `body` 參數中傳入索引設定與對應。

下列範例建立具有一個主要分片與一個副本的索引。此範例明確將 `gradDate` 欄位對應為使用 `yyyy-MM-dd` 格式的 `date`。當您將文件編製索引時，OpenSearch 會動態對應其他文件欄位：

```ruby
index_body = {
  settings: {
    index: {
      number_of_shards: 1,
      number_of_replicas: 1
    }
  },
  mappings: {
    properties: {
      gradDate: { type: 'date', format: 'yyyy-MM-dd' }
    }
  }
}
client.indices.create(index: 'students', body: index_body)
```
{% include copy.html %}

## 對應

OpenSearch 使用動態對應來推斷已編製索引文件的欄位類型。不過，若要更充分控制文件的結構描述，您可以將明確對應傳遞給 OpenSearch，如[建立索引](#creating-an-index)所示。預設情況下，字串欄位會被對應為 `text`。若改為將欄位對應為 `keyword`，則會向 OpenSearch 表明該欄位不應被分析，且僅應支援完整且區分大小寫的比對。

若要驗證索引的對應，請使用 `get_mapping` 方法：

```ruby
response = client.indices.get_mapping(index: 'students')
```
{% include copy.html %}

如果您事先知道文件的對應，並希望避免對應錯誤（例如欄位名稱拼寫錯誤），可以使用 `put_mapping` 方法對應其餘欄位，並將 `dynamic` 參數設定為 `strict`：

```ruby
client.indices.put_mapping(
  index: 'students',
  body: {
    dynamic: 'strict',
    properties: {
      firstName: { type: 'keyword' },
      lastName: { type: 'keyword' },
      gpa: { type: 'float' },
      gradDate: { type: 'date', format: 'yyyy-MM-dd' }
    }
  }
)
```
{% include copy.html %}

使用嚴格對應時，您可以為缺少欄位的文件編製索引，但無法為含有新欄位的文件編製索引。例如，為以下含有拼寫錯誤的 `gradDat` 欄位的文件編製索引將會失敗：

```ruby
student = { firstName: 'John', lastName: 'Doe', gpa: 3.89, gradDat: '2022-05-15' }
client.index(index: 'students', id: '1', body: student, refresh: true)
```
{% include copy.html %}

OpenSearch 會回傳對應錯誤，且用戶端會擲出包含下列訊息的 `OpenSearch::Transport::Transport::Errors::BadRequest` 例外：

```bash
[400] {"error":{"root_cause":[{"type":"strict_dynamic_mapping_exception","reason":"mapping set to strict, dynamic introduction of [gradDat] within [_doc] is not allowed"}],"type":"strict_dynamic_mapping_exception","reason":"mapping set to strict, dynamic introduction of [gradDat] within [_doc] is not allowed"},"status":400}
```

## 為文件編製索引

若要為文件編製索引，請使用 `index` 方法：

```ruby
student = { firstName: 'John', lastName: 'Doe', gpa: 3.89, gradDate: '2022-05-15' }
response = client.index(index: 'students', id: '1', body: student, refresh: true)
```
{% include copy.html %}

## 大量操作

您可以使用 `bulk` 方法同時執行多項操作。這些操作可以是相同類型，也可以是不同類型。

若要為多份文件編製索引，請依序傳遞每個動作標頭及其文件：

```ruby
actions = [
  { index: { _index: 'students', _id: '2' } },
  { firstName: 'Paulo', lastName: 'Santos', gpa: 3.93, gradDate: '2021-05-20' },
  { index: { _index: 'students', _id: '3' } },
  { firstName: 'Shirley', lastName: 'Rodriguez', gpa: 3.91, gradDate: '2019-05-10' }
]
response = client.bulk(body: actions, refresh: true)
```
{% include copy.html %}

或者，您也可以使用 `data:` 鍵來標示資料，將標頭與資料一併傳遞。下列請求為同樣的兩份文件編製索引：

```ruby
actions = [
  { index: { _index: 'students', _id: '2', data: { firstName: 'Paulo', lastName: 'Santos', gpa: 3.93, gradDate: '2021-05-20' } } },
  { index: { _index: 'students', _id: '3', data: { firstName: 'Shirley', lastName: 'Rodriguez', gpa: 3.91, gradDate: '2019-05-10' } } }
]
response = client.bulk(body: actions, refresh: true)
```
{% include copy.html %}

## 搜尋文件

若要搜尋文件，請使用 `search` 方法。如果您省略請求本文，您的查詢會變成 `match_all` 查詢，並回傳索引中的所有文件：

```ruby
require 'json'

response = client.search(index: 'students')
response['hits']['hits'].each { |hit| puts JSON.generate(hit['_source']) }
```
{% include copy.html %}

下列範例使用 `range` 查詢來搜尋 2019 年畢業的學生：

```ruby
query = { query: { range: { gradDate: { gte: '2019-01-01', lte: '2019-12-31' } } } }
response = client.search(index: 'students', body: query)
```
{% include copy.html %}

下列範例搜尋名字或姓氏為 "Santos" 的學生。它使用 `multi_match` 查詢搜尋兩個欄位（`firstName` 和 `lastName`），並使用插入號表示法（`lastName^2`）提高 `lastName` 欄位的相關性權重：

```ruby
query = {
  size: 5,
  query: {
    multi_match: {
      query: 'Santos',
      fields: ['firstName', 'lastName^2']
    }
  }
}
response = client.search(index: 'students', body: query)
```
{% include copy.html %}

## 布林值查詢

Ruby 用戶端提供完整的 OpenSearch 查詢功能。除了使用 match 查詢的簡單搜尋之外，您還可以建立更複雜的布林值查詢，搜尋 2021 年（含）之後畢業的學生，並依 GPA 降序排序。在下列範例中，搜尋結果限制為 10 份文件：

```ruby
query = {
  query: {
    bool: {
      filter: {
        range: {
          gradDate: { gte: '2021-01-01' }
        }
      }
    }
  },
  sort: {
    gpa: { order: 'desc' }
  }
}
response = client.search(index: 'students', from: 0, size: 10, body: query)
```
{% include copy.html %}

## 多重搜尋

您可以將多個查詢合併在一起，並使用 `msearch` 方法執行多重搜尋。下列程式碼搜尋 GPA 大於 3.9 的學生，以及 GPA 小於 3.9 的學生：

```ruby
actions = [
  {},
  { query: { range: { gpa: { gt: 3.9 } } } },
  {},
  { query: { range: { gpa: { lt: 3.9 } } } }
]
response = client.msearch(index: 'students', body: actions)
```
{% include copy.html %}

## 分頁顯示結果

若要分頁顯示結果，請使用 `from` 和 `size` 參數。下列範例依畢業日期排序學生，並每次擷取兩筆結果。第一個請求回傳第一頁結果，第二個請求回傳下一頁：

```ruby
require 'json'

query = { sort: [{ gradDate: 'asc' }] }
response = client.search(index: 'students', from: 0, size: 2, body: query)
response['hits']['hits'].each { |hit| puts JSON.generate(hit['_source']) }

response = client.search(index: 'students', from: 2, size: 2, body: query)
response['hits']['hits'].each { |hit| puts JSON.generate(hit['_source']) }
```
{% include copy.html %}

`from` 和 `size` 參數適用於結果的前幾頁。若要批次處理大量結果，請使用 scroll，如[使用 scroll 分頁](#paginating-using-scroll)所述。

### 使用 scroll 分頁

請使用 Scroll API 來分頁顯示搜尋結果。Scroll 會在叢集上保持搜尋上下文開啟，適合在批次工作中處理所有結果，而非用於面向使用者的請求。若是其他使用情境，請搭配 `search_after` 使用 point in time。如需更多資訊，請參閱[分頁顯示結果]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/paginate/)。

下列範例每次擷取兩名學生，直到取得所有學生：

```ruby
response = client.search(index: 'students', scroll: '2m', size: 2)

while response['hits']['hits'].size.positive?
  scroll_id = response['_scroll_id']
  puts(response['hits']['hits'].map { |hit| "#{hit['_source']['firstName']} #{hit['_source']['lastName']}" })
  response = client.scroll(scroll: '1m', body: { scroll_id: scroll_id })
end

client.clear_scroll(body: { scroll_id: response['_scroll_id'] })
```
{% include copy.html %}

首先，您發出搜尋查詢，指定 `scroll` 和 `size` 參數。`scroll` 參數會告訴 OpenSearch 搜尋上下文應保留多久。在此範例中，它設定為兩分鐘。`size` 參數指定每個請求要回傳多少份文件。

初始搜尋查詢的回應包含一個 `_scroll_id`，您可以用它來取得下一批文件。為此，您需使用 `scroll` 方法，同樣指定 `scroll` 參數，並在本文中傳遞 `_scroll_id`。您不需要為 `scroll` 方法指定查詢或索引。`scroll` 方法會回傳下一批文件以及 `_scroll_id`。請求下一批文件時，務必使用最新的 `_scroll_id`，因為 `_scroll_id` 可能會在請求之間變動。當您擷取完所有文件後，請使用 `clear_scroll` 方法釋放搜尋上下文。

## 更新文件

若要更新文件，請使用 `update` 方法，並在 `doc` 物件中傳入要變更的欄位。接著使用 `get` 方法擷取更新後的文件：

```ruby
response = client.update(index: 'students', id: '1', body: { doc: { gpa: 3.92 } })
response = client.get(index: 'students', id: '1')
```
{% include copy.html %}

## 刪除文件

若要刪除文件，請使用 `delete` 方法：

```ruby
response = client.delete(index: 'students', id: '3', refresh: true)
```
{% include copy.html %}

若要在單一請求中刪除多份文件，請使用 `bulk` 方法：

```ruby
actions = [
  { delete: { _index: 'students', _id: '1' } },
  { delete: { _index: 'students', _id: '2' } }
]
response = client.bulk(body: actions, refresh: true)
```
{% include copy.html %}

## 刪除索引

若要刪除索引，請使用 `indices.delete` 方法：

```ruby
response = client.indices.delete(index: 'students')
```
{% include copy.html %}

## 範例程式

此範例程式結合了前面各節的程式碼。它會連線至已啟用 Security 外掛程式的叢集。若要連線至未啟用 Security 外掛程式的叢集，請變更標有 `# Without security` 註解的行。

此範例程式僅供測試之用。它在程式碼中指定認證資訊，並停用憑證驗證，以便連線至使用自簽憑證的叢集。在正式環境中，請從安全的位置載入認證資訊，並驗證叢集的憑證。
{: .warning}

下列範例程式會建立用戶端、建立索引、個別及批次將文件編製索引、搜尋文件、更新文件、刪除文件，然後刪除索引：

```ruby
require 'opensearch'
require 'json'

client = OpenSearch::Client.new(
  host: 'https://localhost:9200', # Without security, use http://localhost:9200
  user: 'admin', # Without security, remove this line
  password: '<custom-admin-password>', # Without security, remove this line
  transport_options: { ssl: { verify: false } } # Without security, remove this line
)

# Create the index
index = 'students'
puts 'Creating index......'
index_body = {
  settings: {
    index: {
      number_of_shards: 1,
      number_of_replicas: 1
    }
  },
  mappings: {
    properties: {
      gradDate: { type: 'date', format: 'yyyy-MM-dd' }
    }
  }
}
response = client.indices.create(index: index, body: index_body)
puts "Index created: #{response['index']}"

# Index a document
puts "\nIndexing one student......"
student = { firstName: 'John', lastName: 'Doe', gpa: 3.89, gradDate: '2022-05-15' }
response = client.index(index: index, id: '1', body: student, refresh: true)
puts "Result: #{response['result']}, id: #{response['_id']}, version: #{response['_version']}"

# Bulk index documents
puts "\nIndexing many students......"
actions = [
  { index: { _index: index, _id: '2' } },
  { firstName: 'Paulo', lastName: 'Santos', gpa: 3.93, gradDate: '2021-05-20' },
  { index: { _index: index, _id: '3' } },
  { firstName: 'Shirley', lastName: 'Rodriguez', gpa: 3.91, gradDate: '2019-05-10' }
]
response = client.bulk(body: actions, refresh: true)
puts "Errors: #{response['errors']}"
response['items'].each do |item|
  puts "  #{item['index']['result']} id: #{item['index']['_id']}"
end

# Search for all students
puts "\nSearching for all students......"
query = { sort: [{ gradDate: 'asc' }] }
[0, 2].each_with_index do |from, page|
  response = client.search(index: index, from: from, size: 2, body: query)
  puts "Total hits: #{response['hits']['total']['value']}" if page.zero?
  puts "Page #{page + 1}:"
  response['hits']['hits'].each { |hit| puts "  #{JSON.generate(hit['_source'])}" }
end

# Search for students who graduated in 2019
puts "\nSearching for students who graduated in 2019......"
query = { query: { range: { gradDate: { gte: '2019-01-01', lte: '2019-12-31' } } } }
response = client.search(index: index, body: query)
puts "Total hits: #{response['hits']['total']['value']}"
response['hits']['hits'].each { |hit| puts "  #{JSON.generate(hit['_source'])}" }

# Update a document
puts "\nUpdating a student's GPA......"
response = client.update(index: index, id: '1', body: { doc: { gpa: 3.92 } })
puts "Result: #{response['result']}, version: #{response['_version']}"

# Get the updated document
response = client.get(index: index, id: '1')
puts "Updated document: #{JSON.generate(response['_source'])}"

# Delete a document
puts "\nDeleting a student......"
response = client.delete(index: index, id: '3', refresh: true)
puts "Result: #{response['result']}"

# Delete the index
puts "\nDeleting the index......"
response = client.indices.delete(index: index)
puts "Acknowledged: #{response['acknowledged']}"
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

# Ruby AWS Signature Version 4 用戶端

[`opensearch-aws-sigv4`](https://github.com/opensearch-project/opensearch-ruby-aws-sigv4) gem 提供 `OpenSearch::Aws::Sigv4Client` 類別，其具備 `OpenSearch::Client` 的所有功能。這兩個用戶端唯一的差異在於，`OpenSearch::Aws::Sigv4Client` 在具現化時需要 `Aws::Sigv4::Signer` 的執行個體，才能向 AWS 進行驗證：

```ruby
require 'opensearch-aws-sigv4'
require 'aws-sigv4'

signer = Aws::Sigv4::Signer.new(service: 'es',
                                region: 'us-east-1',
                                access_key_id: 'key_id',
                                secret_access_key: 'secret',
                                session_token: 'session_token') # required for temporary credentials, such as IAM roles or SSO

client = OpenSearch::Aws::Sigv4Client.new({
    host: 'https://search-<domain-name>-<id>.us-east-1.es.amazonaws.com',
    log: true
}, signer)

client.cluster.health

client.search(index: 'students', q: 'firstName:John')
```
{% include copy.html %}

## 相關文件

- 如需更多使用用戶端的範例，請參閱 [`opensearch-ruby` 使用者指南](https://github.com/opensearch-project/opensearch-ruby/blob/main/USER_GUIDE.md)。
- 如需特定工作的指南，例如批次編製索引和搜尋，請參閱 [`opensearch-ruby` 指南](https://github.com/opensearch-project/opensearch-ruby/tree/main/guides)。
- 如需完整的範例應用程式，請參閱 [`opensearch-ruby` 範例](https://github.com/opensearch-project/opensearch-ruby/tree/main/samples)。
