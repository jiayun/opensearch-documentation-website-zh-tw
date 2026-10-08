---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "PHP 用戶端"
nav_order: 70
---

# PHP 用戶端

OpenSearch PHP 用戶端提供一種更安全、更簡單的方式來與您的 OpenSearch 叢集互動。與其在瀏覽器中使用 OpenSearch 而可能將資料暴露給公眾，您可以建立一個 OpenSearch 用戶端，由它負責向叢集傳送請求。該用戶端包含一個 API 程式庫，讓您能對叢集執行不同的操作並回傳標準的回應本文。

本入門指南說明如何連線至 OpenSearch、將文件編製索引，以及執行查詢。用戶端的原始碼請參閱 [`opensearch-php` 儲存庫](https://github.com/opensearch-project/opensearch-php)。

## 安裝 PHP 用戶端

此用戶端需要 PHP 8.2 或更新版本。若要將用戶端加入您的專案，請使用 [Composer](https://getcomposer.org/) 安裝：

```bash
composer require opensearch-project/opensearch-php
```
{% include copy.html %}

若要安裝特定版本的用戶端，請執行以下命令：

```bash
composer require opensearch-project/opensearch-php:<version>
```
{% include copy.html %}

用戶端會透過任何實作 [PSR-18](https://www.php-fig.org/psr/psr-18/) 的 HTTP 用戶端傳送請求，因此您也必須安裝一個。若要使用 [Guzzle](https://docs.guzzlephp.org/en/stable/)，請執行以下命令：

```bash
composer require guzzlehttp/guzzle
```
{% include copy.html %}

若要使用 [Symfony HTTP 用戶端](https://symfony.com/doc/current/http_client.html)，請執行以下命令：

```bash
composer require symfony/http-client
```
{% include copy.html %}

然後在您的程式碼中 require `composer` 內的 `autoload` 檔案：

```php
require __DIR__ . '/vendor/autoload.php';
```
{% include copy.html %}

## 連線至 OpenSearch

使用 `GuzzleClientFactory` 或 `SymfonyClientFactory` 建立用戶端。`base_uri` 選項為必要。工廠會將所有其他選項傳遞給底層的 HTTP 用戶端。以下程式碼連線至未啟用 Security 外掛程式的叢集：

```php
$client = (new \OpenSearch\GuzzleClientFactory())->create([
    'base_uri' => 'http://localhost:9200',
]);
```
{% include copy.html %}

若要連線至已啟用 Security 外掛程式的叢集，請提供憑證與 TLS 選項：

```php
$client = (new \OpenSearch\GuzzleClientFactory())->create([
    'base_uri' => 'https://localhost:9200',
    // Only for demo purposes. Don't specify your credentials in code.
    'auth' => ['admin', '<custom-admin-password>'],
    'verify' => false, // Disables TLS certificate verification. Use only for local development.
]);
```
{% include copy.html %}

Symfony HTTP 用戶端接受等效的選項：

```php
$client = (new \OpenSearch\SymfonyClientFactory())->create([
    'base_uri' => 'https://localhost:9200',
    // Only for demo purposes. Don't specify your credentials in code.
    'auth_basic' => ['admin', '<custom-admin-password>'],
    'verify_peer' => false, // Disables TLS certificate verification. Use only for local development.
]);
```
{% include copy.html %}

如需支援的 PSR 用戶端詳細資訊，請參閱 [用戶端工廠](https://github.com/opensearch-project/opensearch-php/blob/main/USER_GUIDE.md#client-factories)。如需基本驗證的詳細資訊，請參閱 [使用 PSR 用戶端進行基本驗證](https://github.com/opensearch-project/opensearch-php/blob/main/guides/auth.md#using-a-psr-client)。

## 連線至 Amazon OpenSearch Service

若要使用 AWS Identity and Access Management (IAM) 憑證簽署請求，請安裝 AWS SDK for PHP：

```bash
composer require aws/aws-sdk-php
```
{% include copy.html %}

在以下範例中，請將端點替換為您的網域端點，該端點列於 Amazon OpenSearch Service 主控台中網域的詳細資料頁面。

然後在建立用戶端時傳遞 `auth_aws` 選項：

```php
$client = (new \OpenSearch\GuzzleClientFactory())->create([
    'base_uri' => 'https://search-<domain-name>-<id>.us-east-1.es.amazonaws.com',
    'auth_aws' => [
        'region' => 'us-east-1',
        'service' => 'es',
    ],
]);
```
{% include copy.html %}

由於範例未指定 `credentials`，AWS SDK for PHP 會使用預設的憑證供應商鏈來解析憑證。該鏈會檢查環境變數、共用的 AWS 組態與憑證檔案，以及程式碼執行所在的 Amazon EC2 執行個體或容器的 IAM 角色。

若要明確傳遞憑證，請新增 `credentials` 選項。僅在使用暫時性憑證時才指定 `session_token`：

```php
$client = (new \OpenSearch\GuzzleClientFactory())->create([
    'base_uri' => 'https://search-<domain-name>-<id>.us-east-1.es.amazonaws.com',
    'auth_aws' => [
        'region' => 'us-east-1',
        'service' => 'es',
        'credentials' => [
            'access_key' => getenv('AWS_ACCESS_KEY_ID'),
            'secret_key' => getenv('AWS_SECRET_ACCESS_KEY'),
            'session_token' => getenv('AWS_SESSION_TOKEN'),
        ],
    ],
]);
```
{% include copy.html %}

如需詳細資訊，請參閱 [使用 PSR 用戶端進行 IAM 驗證](https://github.com/opensearch-project/opensearch-php/blob/main/guides/auth.md#using-a-psr-client-1)。

## 連線至 Amazon OpenSearch Serverless

在以下範例中，請將端點替換為您的集合端點，該端點列於 Amazon OpenSearch Service 主控台中集合的詳細資料頁面。

若要連線至 Amazon OpenSearch Serverless，請將 `service` 設定為 `aoss` 並指定您的集合端點。以下範例檢查索引是否存在：

```php
$client = (new \OpenSearch\GuzzleClientFactory())->create([
    'base_uri' => 'https://<collection-id>.us-east-1.aoss.amazonaws.com',
    'auth_aws' => [
        'region' => 'us-east-1',
        'service' => 'aoss',
    ],
]);

$exists = $client->indices()->exists(['index' => 'students']);
echo $exists ? 'Index exists' : 'Index does not exist', PHP_EOL;
```
{% include copy.html %}

Amazon OpenSearch Serverless 支援 OpenSearch API 操作的子集，且不支援本頁範例中使用的 `refresh` 參數。如需詳細資訊，請參閱 [Amazon OpenSearch Serverless 支援的操作與外掛程式](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/serverless-genref.html)。
{: .note}

## 建立索引

以下範例建立一個具有一個主要分片與一個副本的索引。它將 `gradDate` 欄位明確對應為 `yyyy-MM-dd` 格式的 `date`。當您將文件編製索引時，OpenSearch 會動態對應其他文件欄位：

```php
$index = 'students';

$client->indices()->create([
    'index' => $index,
    'body' => [
        'settings' => [
            'index' => [
                'number_of_shards' => 1,
                'number_of_replicas' => 1,
            ],
        ],
        'mappings' => [
            'properties' => [
                'gradDate' => ['type' => 'date', 'format' => 'yyyy-MM-dd'],
            ],
        ],
    ],
]);
```
{% include copy.html %}

## 將文件編製索引

使用以下程式碼將文件編製索引。將 `refresh` 設定為 `true`，讓文件立即可供搜尋：

```php
$response = $client->index([
    'index' => $index,
    'id' => '1',
    'body' => [
        'firstName' => 'John',
        'lastName' => 'Doe',
        'gpa' => 3.89,
        'gradDate' => '2022-05-15',
    ],
    'refresh' => true,
]);
```
{% include copy.html %}

若要只在文件 ID 尚不存在時建立文件，請使用 `create()` 而非 `index()`。對已存在的 ID 發出 `create()` 請求會回傳 `409` 回應。

## 大量編製索引

使用下列程式碼，在單一請求中將多份文件編製索引。請求本文會交替出現動作行，以及該動作所套用的文件：

```php
$response = $client->bulk([
    'body' => [
        ['index' => ['_index' => $index, '_id' => '2']],
        ['firstName' => 'Paulo', 'lastName' => 'Santos', 'gpa' => 3.93, 'gradDate' => '2021-05-20'],
        ['index' => ['_index' => $index, '_id' => '3']],
        ['firstName' => 'Shirley', 'lastName' => 'Rodriguez', 'gpa' => 3.91, 'gradDate' => '2019-05-10'],
    ],
    'refresh' => true,
]);
```
{% include copy.html %}

當個別動作失敗時，大量請求不會擲回例外狀況，因此請檢查回應的 `errors` 欄位與 `items` 陣列，以取得各個動作的結果。

## 搜尋文件

使用下列程式碼搜尋索引中的所有文件：

```php
$response = $client->search([
    'index' => $index,
]);

foreach ($response['hits']['hits'] as $hit) {
    echo json_encode($hit['_source']) . "\n";
}
```
{% include copy.html %}

使用範圍查詢進行搜尋：

```php
$response = $client->search([
    'index' => $index,
    'body' => [
        'query' => [
            'range' => [
                'gradDate' => [
                    'gte' => '2019-01-01',
                    'lte' => '2019-12-31',
                ],
            ],
        ],
    ],
]);
```
{% include copy.html %}

若要以 SQL 撰寫查詢，請使用 `sql()` 命名空間。回應包含描述各欄的 `schema` 陣列，以及包含相符資料列的 `datarows` 陣列：

```php
$response = $client->sql()->query([
    'body' => [
        'query' => "SELECT firstName, lastName, gpa FROM $index WHERE gradDate BETWEEN '2019-01-01' AND '2019-12-31'",
    ],
]);
```
{% include copy.html %}

## 將結果分頁

若要將結果分頁，請使用 `from` 和 `size` 參數。下列範例依畢業日期排序學生，並每次擷取兩筆結果。第一個請求會傳回第一頁結果，第二個請求則傳回下一頁：

```php
foreach ([0, 2] as $from) {
    $response = $client->search([
        'index' => $index,
        'body' => [
            'from' => $from,
            'size' => 2,
            'sort' => [['gradDate' => 'asc']],
        ],
    ]);

    foreach ($response['hits']['hits'] as $hit) {
        echo json_encode($hit['_source']) . "\n";
    }
}
```
{% include copy.html %}

`from` 和 `size` 參數適用於結果的前幾頁。若要逐頁瀏覽大量結果，請搭配 `search_after` 使用時間點，如[使用時間點進行分頁](#paginating-using-a-point-in-time)中所述。

### 使用時間點進行分頁

若要逐頁瀏覽大量結果，或逐頁瀏覽索引的固定檢視，請搭配 `search_after` 使用時間點 (PIT)。建立 PIT，在搜尋本文中傳入其 ID，並將最後一筆命中結果的 `sort` 值作為下一頁的 `search_after` 值：

```php
$response = $client->createPit([
    'index' => $index,
    'keep_alive' => '10m',
]);
$pitId = $response['pit_id'];

// Get the first page of results.
$response = $client->search([
    'body' => [
        'pit' => ['id' => $pitId, 'keep_alive' => '10m'],
        'size' => 2,
        'sort' => [['gradDate' => 'asc']],
    ],
]);
$last = end($response['hits']['hits']);

// Get the next page of results.
$response = $client->search([
    'body' => [
        'pit' => ['id' => $pitId, 'keep_alive' => '10m'],
        'search_after' => $last['sort'],
        'size' => 2,
        'sort' => [['gradDate' => 'asc']],
    ],
]);

// Delete the point in time.
$client->deletePit([
    'body' => ['pit_id' => [$pitId]],
]);
```
{% include copy.html %}

## 更新文件

將變更的欄位包裝在 `doc` 物件中，以更新文件：

```php
$response = $client->update([
    'index' => $index,
    'id' => '1',
    'body' => [
        'doc' => [
            'gpa' => 3.92,
        ],
    ],
]);
```
{% include copy.html %}

## 刪除文件

使用下列程式碼刪除文件：

```php
$response = $client->delete([
    'index' => $index,
    'id' => '3',
    'refresh' => true,
]);
```
{% include copy.html %}

若要刪除所有符合查詢的文件，請使用 `deleteByQuery()`：

```php
$response = $client->deleteByQuery([
    'index' => $index,
    'body' => [
        'query' => [
            'range' => [
                'gradDate' => [
                    'gte' => '2021-01-01',
                    'lte' => '2021-12-31',
                ],
            ],
        ],
    ],
]);
```
{% include copy.html %}

## 刪除索引

使用下列程式碼刪除索引：

```php
$response = $client->indices()->delete([
    'index' => $index,
]);
```
{% include copy.html %}

## 範例程式

此範例程式結合了前述各節的程式碼。它會連線至已啟用 Security 外掛程式的叢集。若要連線至未使用 Security 外掛程式的叢集，請變更標有 `// Without security` 註解的程式碼行。

此範例程式僅供測試使用。它在程式碼中指定認證資訊，並停用憑證驗證，以便連線至使用自我簽署憑證的叢集。在正式環境中，請從安全的位置載入認證資訊，並驗證叢集的憑證。
{: .warning}

下列範例程式會建立用戶端、建立索引、逐一及大量將文件編製索引、搜尋文件、更新文件、刪除文件，最後刪除索引：

```php
<?php

require __DIR__ . '/vendor/autoload.php';

$client = (new \OpenSearch\GuzzleClientFactory())->create([
    'base_uri' => 'https://localhost:9200', // Without security, use http://localhost:9200
    'auth' => ['admin', '<custom-admin-password>'], // Without security, remove this line
    'verify' => false, // Without security, remove this line
]);

try {
    // Create the index
    $index = 'students';
    echo "Creating index......\n";
    $response = $client->indices()->create([
        'index' => $index,
        'body' => [
            'settings' => [
                'index' => [
                    'number_of_shards' => 1,
                    'number_of_replicas' => 1,
                ],
            ],
            'mappings' => [
                'properties' => [
                    'gradDate' => ['type' => 'date', 'format' => 'yyyy-MM-dd'],
                ],
            ],
        ],
    ]);
    echo "Index created: {$response['index']}\n";

    // Index a document
    echo "\nIndexing one student......\n";
    $response = $client->index([
        'index' => $index,
        'id' => '1',
        'body' => [
            'firstName' => 'John',
            'lastName' => 'Doe',
            'gpa' => 3.89,
            'gradDate' => '2022-05-15',
        ],
        'refresh' => true,
    ]);
    echo "Result: {$response['result']}, id: {$response['_id']}, version: {$response['_version']}\n";

    // Bulk index documents
    echo "\nIndexing many students......\n";
    $response = $client->bulk([
        'body' => [
            ['index' => ['_index' => $index, '_id' => '2']],
            ['firstName' => 'Paulo', 'lastName' => 'Santos', 'gpa' => 3.93, 'gradDate' => '2021-05-20'],
            ['index' => ['_index' => $index, '_id' => '3']],
            ['firstName' => 'Shirley', 'lastName' => 'Rodriguez', 'gpa' => 3.91, 'gradDate' => '2019-05-10'],
        ],
        'refresh' => true,
    ]);
    echo 'Errors: ' . var_export($response['errors'], true) . "\n";
    foreach ($response['items'] as $item) {
        $action = array_key_first($item);
        echo "  {$item[$action]['result']} id: {$item[$action]['_id']}\n";
    }

    // Search for all students
    echo "\nSearching for all students......\n";
    $response = $client->search([
        'index' => $index,
        'body' => [
            'from' => 0,
            'size' => 2,
            'sort' => [['gradDate' => 'asc']],
        ],
    ]);
    echo "Total hits: {$response['hits']['total']['value']}\n";
    echo "Page 1:\n";
    foreach ($response['hits']['hits'] as $hit) {
        echo '  ' . json_encode($hit['_source']) . "\n";
    }

    $response = $client->search([
        'index' => $index,
        'body' => [
            'from' => 2,
            'size' => 2,
            'sort' => [['gradDate' => 'asc']],
        ],
    ]);
    echo "Page 2:\n";
    foreach ($response['hits']['hits'] as $hit) {
        echo '  ' . json_encode($hit['_source']) . "\n";
    }

    // Search for students who graduated in 2019
    echo "\nSearching for students who graduated in 2019......\n";
    $response = $client->search([
        'index' => $index,
        'body' => [
            'query' => [
                'range' => [
                    'gradDate' => [
                        'gte' => '2019-01-01',
                        'lte' => '2019-12-31',
                    ],
                ],
            ],
        ],
    ]);
    echo "Total hits: {$response['hits']['total']['value']}\n";
    foreach ($response['hits']['hits'] as $hit) {
        echo '  ' . json_encode($hit['_source']) . "\n";
    }

    // Update a document
    echo "\nUpdating a student's GPA......\n";
    $response = $client->update([
        'index' => $index,
        'id' => '1',
        'body' => [
            'doc' => [
                'gpa' => 3.92,
            ],
        ],
    ]);
    echo "Result: {$response['result']}, version: {$response['_version']}\n";

    // Get the updated document
    $response = $client->get([
        'index' => $index,
        'id' => '1',
    ]);
    echo 'Updated document: ' . json_encode($response['_source']) . "\n";

    // Delete a document
    echo "\nDeleting a student......\n";
    $response = $client->delete([
        'index' => $index,
        'id' => '3',
        'refresh' => true,
    ]);
    echo "Result: {$response['result']}\n";

    // Delete the index
    echo "\nDeleting the index......\n";
    $response = $client->indices()->delete([
        'index' => $index,
    ]);
    echo 'Acknowledged: ' . var_export($response['acknowledged'], true) . "\n";
} catch (\OpenSearch\Exception\HttpExceptionInterface $e) {
    echo 'OpenSearch returned an error: ' . $e->getMessage() . "\n";
}
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

## 相關文件

- 如需更多使用用戶端的範例，請參閱 [`opensearch-php` 使用者指南](https://github.com/opensearch-project/opensearch-php/blob/main/USER_GUIDE.md)。
- 如需特定工作的指南，例如驗證與傳送原始請求，請參閱 [`opensearch-php` 指南](https://github.com/opensearch-project/opensearch-php/tree/main/guides)。
- 如需完整的範例應用程式，請參閱 [`opensearch-php` 範例](https://github.com/opensearch-project/opensearch-php/tree/main/samples)。
