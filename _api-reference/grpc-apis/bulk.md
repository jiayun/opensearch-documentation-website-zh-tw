---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "Bulk（gRPC）"
parent: gRPC APIs
nav_order: 20
---

# Bulk API（gRPC）
**於 3.0 引入**
{: .label .label-purple }

gRPC Bulk API 提供高效率、採用二進位編碼的替代方案，可取代 [HTTP Bulk API]({{site.url}}{{site.baseurl}}/api-reference/document-apis/bulk/)，在單次呼叫中執行多項文件操作，例如編製索引、更新和刪除。此服務使用 protocol buffers，並在參數和結構上與 REST API 一致。

## 先決條件

若要提交 gRPC 請求，您必須在用戶端具備一組 protobuf。若要瞭解取得 protobuf 的方式，請參閱[使用 gRPC API]({{site.url}}{{site.baseurl}}/api-reference/grpc-apis/index/#how-to-use-grpc-apis)。

## gRPC 服務與方法

gRPC Document API 位於 [DocumentService](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/services/document_service.proto#L22) 中。

您可以呼叫 `DocumentService` 中的 [`Bulk`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/services/document_service.proto#L24) gRPC 方法來提交批次請求。此方法接收 [`BulkRequest`](#bulkrequest-fields)，並傳回 [`BulkResponse`](#bulkresponse-fields)。

## 文件格式

在 gRPC 中，文件必須以位元組形式提供及傳回。請使用 Base64 編碼，在 gRPC 請求中提供文件。
{: .note }

例如，請看一般 Bulk API 請求中的下列文件：

```json
"doc":  "{\"title\": \"Inception\", \"year\": 2010}"
```

在 gRPC Bulk API 請求中，請以 Base64 編碼提供相同的文件：

```json
"doc": "eyJ0aXRsZSI6ICJJbmNlcHRpb24iLCAieWVhciI6IDIwMTB9"
```

## BulkRequest 欄位

[`BulkRequest`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L851) 訊息是 gRPC 批次操作的最上層容器。它接受下列欄位。

| 欄位 | Protobuf 類型 | 說明 |
| :---- | :---- | :---- |
| `bulk_request_body` | `repeated `[`BulkRequestBody`](#bulkrequestbody-fields) | 批次操作清單，每項操作包含其中一種操作類型（`index`/`create`/`update`/`delete`）。必要。 |
| `index` | `string` | 所有操作的預設索引，除非在 `bulk_request_body` 中覆寫。在 `BulkRequest` 中指定 `index`，即表示您不需要在 [BulkRequestBody](#bulkrequestbody-fields) 中包含它。選用。 |
| `x_source` | [`SourceConfigParam`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L1251) | 控制回應是否傳回完整的 `_source`、不傳回 `_source`，或僅傳回 `_source` 中的特定欄位。選用。 |
| `x_source_excludes` | `repeated string` | 要從 `source` 中排除的欄位。選用。 |
| `x_source_includes` | `repeated string` | 要從 `source` 中包含的欄位。選用。 |
| `pipeline` | `string` | 前置處理資料匯入管線的 ID。選用。 |
| `refresh` | [`Refresh`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L3552) | 是否在編製索引後重新整理分片。選用。 |
| `require_alias` | `bool` | 若為 `true`，動作必須以別名為目標。選用。 |
| `routing` | `string` | 用於分片指派的路由值。選用。 |
| `timeout` | `string` | 逾時時間（例如 `1m`）。選用。 |
| `type`（已棄用） | `string` | 文件類型（一律為 `_doc`）。選用。 |
| `wait_for_active_shards` | [`WaitForActiveShards`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L1162) | 要等待的作用中分片數量下限。選用。 |
| `global_params` | [`GlobalParams`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L1150) | 請求的全域參數。選用。 |


## BulkRequestBody 欄位

[`BulkRequestBody`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L894) 訊息代表 `BulkRequest` 中的單一文件層級操作。它接受下列欄位。

| 欄位 | Protobuf 類型 | 說明 |
| :---- | :---- | :---- |
| `operation_container` | [`OperationContainer`](#operationcontainer-fields) | 要執行的操作（`index`、`create`、`update` 或 `delete`）。必要。 |
| `update_action` | [`UpdateAction`](#updateaction-fields) | 更新專用的額外選項。選用。 |
| `object` | `bytes` | 用於 `create` 和 `index` 操作的完整文件內容。選用。 |

## OperationContainer 欄位

[`OperationContainer`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L918) 訊息恰好包含一種操作類型。它接受下列欄位。

| 欄位 | Protobuf 類型 | 說明 |
| :---- | :---- | :---- |
| `index` | [`IndexOperation`](#index) | 將文件編製索引。若文件已存在，則取代該文件。 |
| `create` | [`WriteOperation`](#create) | 建立新文件。若文件已存在，則失敗。 |
| `update` | [`UpdateOperation`](#update) | 部分更新文件，或使用 upsert／指令碼選項。 |
| `delete` | [`DeleteOperation`](#delete) | 依 ID 刪除文件。 |

## UpdateAction 欄位

[`UpdateAction`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L936) 訊息提供更新操作的額外選項。它接受下列欄位。

| 欄位 | Protobuf 類型 | 說明 |
| :---- | :---- | :---- |
| `detect_noop` | `bool` | 若為 `true`，且文件內容未變更，則略過更新。選用。預設為 `true`。 |
| `doc` | `bytes` | 用於 `update` 操作的部分或完整文件資料。選用。 |
| `doc_as_upsert` | `bool` | 若為 `true`，且目標文件不存在，則將此文件視為完整的 upsert 文件。僅適用於 `update` 操作。選用。 |
| `script` | [`Script`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L1171) | 要套用至文件的指令碼（與 `update` 搭配使用）。選用。 |
| `scripted_upsert` | `bool` | 若為 `true`，則無論文件是否存在，都會執行指令碼。選用。 |
| `upsert` | `bytes` | 目標不存在時要使用的完整文件。與 `script` 搭配使用。選用。 |
| `x_source` | [`SourceConfig`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L1267) | 控制擷取或篩選文件來源的方式。選用。 |


### 建立

`WriteOperation` 僅在文件尚不存在時新增文件。

文件本身必須在 `BulkRequestBody` 訊息的 `object` 欄位中提供。

也可以提供下列選用欄位。

| 欄位 | Protobuf 類型 | 說明 |
| :---- | :---- | :---- |
| `x_id` | `string` | 文件 ID。若省略，則會自動產生。選用。 |
| `x_index` | `string` | 目標索引。若未在 `BulkRequest` 中全域設定，則為必要。選用。 |
| `routing` | `string` | 用於控制分片配置位置的自訂路由值。選用。 |
| `pipeline` | `string` | 前置處理資料匯入管線的 ID。選用。 |
| `require_alias` | `bool` | 若為 `true`，則要求所有動作都以索引別名而非索引為目標。預設為 `false`。選用。 |

#### 範例請求

下列範例顯示包含 `create` 操作的批次請求。它會在 `movies` 索引中建立一個 ID 為 `tt1375666` 的文件。以 Base64 編碼提供的文件內容代表 `{"title": "Inception", "year": 2010}`：

```json
{
  "index": "movies",
  "bulk_request_body": [
    {
      "operation_container": {
        "create": {
          "x_index": "movies",
          "x_id": "tt1375666"
        }
      },
      "object": "eyJ0aXRsZSI6ICJJbmNlcHRpb24iLCAieWVhciI6IDIwMTB9"
    }
  ]
}
```

### 刪除

`DeleteOperation` 會依 ID 刪除文件。它接受下列欄位。

| 欄位 | Protobuf 類型 | 說明 |
| :---- | :---- | :---- |
| `x_id` | `string` | 要刪除之文件的 ID。必要。 |
| `x_index` | `string` | 目標索引。若未在 `BulkRequest` 中全域設定則為必要。選用。 |
| `routing` | `string` | 用於控制分片放置的自訂路由值。選用。 |
| `if_primary_term` | `int64` | 用於並行控制。僅當文件的主要分片任期與此值相符時才會執行操作。選用。 |
| `if_seq_no` | `int64` | 用於並行控制。僅當文件的序號與此值相符時才會執行操作。選用。 |
| `version` | `int64` | 用於並行控制的明確文件版本。選用。 |
| `version_type` | [`VersionType`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L3544) | 控制版本比對行為。選用。 |

#### 範例請求

下列範例顯示包含 `delete` 操作的批次請求。它會從 `movies` 索引中刪除 ID 為 `tt1392214` 的文件：

```json
{
  "index": "movies",
  "bulk_request_body": [
    {
      "operation_container": {
        "delete": {
          "x_index": "movies",
          "x_id": "tt1392214"
        }
      }
    }
  ]
}
```
{% include copy.html %}

### 編製索引

`IndexOperation` 會建立或覆寫文件。若未提供 ID，則會自動產生一個。

文件本身在 `BulkRequestBody` 訊息的 `object` 欄位中提供。

也可以提供下列選用欄位。

| 欄位 | Protobuf 類型 | 說明 |
| :---- | :---- | :---- |
| `x_id` | `string` | 文件 ID。若省略則會自動產生。選用。 |
| `x_index` | `string` | 目標索引。僅在未於 `BulkRequest` 中全域設定時為必要。 |
| `routing` | `string` | 用於控制分片放置的自訂路由值。選用。 |
| `if_primary_term` | `int64` | 用於並行控制。僅當文件的主要分片任期與此值相符時才會執行操作。選用。 |
| `if_seq_no` | `int64` | 用於並行控制。僅當文件的序號與此值相符時才會執行操作。選用。 |
| `op_type` | [`OpType`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L3538) | 操作類型。控制覆寫行為。有效值為 `index`（預設）與 `create`。選用。 |
| `version` | `int64` | 用於並行控制的明確文件版本。選用。 |
| `version_type` | [`VersionType`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L3544) | 控制版本比對行為。選用。 |
| `pipeline` | `string` | 預先處理所用的資料匯入管線 ID。選用。 |
| `require_alias` | `bool` | 若為 `true`，則要求所有操作以索引別名而非索引為目標。預設為 `false`。選用。 |


#### 範例請求

下列範例顯示包含 `index` 操作的批次請求。它會將一個以 Base64 編碼、ID 為 `tt0468569` 的文件編製索引至 `movies` 索引：

```json
{
  "index": "movies",
  "bulk_request_body": [
    {
      "operation_container": {
        "index": {
          "x_index": "movies",
          "x_id": "tt0468569"
        }
      },
      "object": "eyJ0aXRsZSI6ICJUaGUgRGFyayBLbmlnaHQiLCAieWVhciI6IDIwMDh9"
    }
  ]
}
```
{% include copy.html %}

### 更新

`UpdateOperation` 會執行文件的部分更新。

更新選項在 `BulkRequestBody` 訊息內的 `update_action` 欄位中提供。

下表所列的所有 `UpdateOperation` 欄位皆為選用，`x_id` 除外。

| 欄位 | Protobuf 類型 | 說明 |
| :---- | :---- | :---- |
| `x_id` | `string` | 要更新之文件的 ID。必要。 |
| `x_index` | `string` | 目標索引。若未在 `BulkRequest` 中全域設定則為必要。選用。 |
| `routing` | `string` | 用於控制分片放置的自訂路由值。選用。 |
| `if_primary_term` | `int64` | 用於並行控制。僅當文件的主要分片任期與此值相符時才會執行操作。選用。 |
| `if_seq_no` | `int64` | 用於並行控制。僅當文件的序號與此值相符時才會執行操作。選用。 |
| `require_alias` | `bool` | 若為 `true`，則要求所有操作以索引別名而非索引為目標。預設為 `false`。選用。 |
| `retry_on_conflict` | `int32` | 發生版本衝突時重試操作的次數。選用。 |


#### 範例請求

下列範例顯示包含 `update` 操作的批次請求。它會將 `movies` 索引中 ID 為 `tt1375666` 的文件更新為 `{"year": 2011}`：

```json
{
  "index": "movies",
  "bulk_request_body": [
    {
      "operation_container": {
        "update": {
          "x_index": "movies",
          "x_id": "tt1375666"
        }
      },
      "update_action": {
        "doc": "eyJ5ZWFyIjogMjAxMX0=",
        "detect_noop": true
      }
    }
  ]
}
```
{% include copy.html %}

### 更新或插入

`upsert` 操作會在文件已存在時更新該文件；否則，會使用提供的文件內容建立新文件。

若要更新或插入文件，請提供 `UpdateOperation`，並在 `BulkRequestBody` 中將 `doc_as_upsert` 指定為 `true`。要更新或插入的文件應在 `doc` 欄位中提供。

#### 範例請求

下列範例顯示包含 `upsert` 操作的批次請求。它會將 `movies` 索引中 ID 為 `tt1375666` 之文件的 `year` 欄位更新為 `{"year": 2012}`：

```json
{
  "index": "movies",
  "bulk_request_body": [
    {
      "operation_container": {
        "update": {
          "x_index": "movies",
          "x_id": "tt1375666"
        }
      },
      "update_action": {
        "doc": "eyJ5ZWFyIjogMjAxMn0=",
        "doc_as_upsert": true
      }
    }
  ]
}
```
{% include copy.html %}

### 指令碼

執行已儲存或內嵌的指令碼以修改文件。

若要指定指令碼，請在 `BulkRequestBody` 中提供 `UpdateOperation` 與 `script` 欄位。

#### 範例請求

下列範例顯示包含 `script` 操作的批次請求。它會將 `movies` 索引中 ID 為 `tt1375666` 之文件的 `year` 欄位增加 1：

```json
{
  "index": "movies",
  "bulk_request_body": [
    {
      "operation_container": {
        "update": {
          "x_index": "movies",
          "x_id": "tt1375666"
        }
      },
      "update_action": {
        "script": {
          "inline": {
            "source": "ctx._source.year += 1",
            "lang": {
              "builtin": "BUILTIN_SCRIPT_LANGUAGE_PAINLESS"
            }
          }
        }
      }
    }
  ]
}
```
{% include copy.html %}


## 回應欄位

gRPC Bulk API 提供下列回應欄位。

### BulkResponse 欄位

[`BulkResponse`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L1059) 訊息由 `Bulk` gRPC 方法直接回傳，提供批次操作的摘要與每個項目的結果。它包含下列欄位。

| 欄位 | Protobuf 類型 | 說明 |
| :---- | :---- | :---- |
| `errors` | `bool` | 指出批次請求中的任何操作是否失敗。若有任何操作失敗，回應的 `errors` 欄位將為 `true`。您可以逐一檢視各個 `Item` 動作以取得更詳細的資訊。|
| `items` | `repeated` [`Item`](#item-fields) | 批次請求中所有操作的結果，依提交順序排列。 |
| `took` | `int64` | 處理批次請求所花費的時間，單位為毫秒。 |
| `ingest_took` | `int64` | 透過資料匯入管線處理文件所花費的時間，單位為毫秒。 |


### Item 欄位

回應中的每個 `Item` 對應請求中的單一操作。對於每個操作，只會提供下列其中一個欄位。

| 欄位 | Protobuf 類型 | 說明 |
| :---- | :---- | :---- |
| `create` | [`ResponseItem`](#responseitem-fields) | `CreateOperation` 的結果。 |
| `delete` | [`ResponseItem`](#responseitem-fields) | `DeleteOperation` 的結果。   |
| `index` | [`ResponseItem`](#responseitem-fields) | `IndexOperation` 的結果。  |
| `update` | [`ResponseItem`](#responseitem-fields) | `UpdateOperation` 的結果。  |


### ResponseItem 欄位

每個 `ResponseItem` 對應請求中的單一操作。它包含下列欄位。

| 欄位 | Protobuf 類型 | 說明 |
| :---- | :---- | :---- |
| `type` | `string` | 文件類型。 |
| `id` | `string` | 與該操作關聯的文件 ID。 |
| `index` | `string` | 與該操作關聯的索引名稱。若目標為資料串流，此為其後端索引。 |
| `status` | `int32` | 為該操作回傳的 HTTP 狀態碼。*(注意：此欄位未來可能會改為 gRPC 狀態碼。)* |
| `error` | [`ErrorCause`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L1287) | 包含有關失敗操作的額外資訊。 |
| `primary_term` | `int64` | 指派給文件的主要分片任期。 |
| `result` | `string` | 操作結果。有效值為 `created`、`deleted` 與 `updated`。 |
| `seq_no` | `int64` | 指派給文件以維持版本順序的序號。 |
| `shards` | [`ShardInfo`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L1332) | 該操作的分片資訊 (僅在成功的動作時回傳)。 |
| `version` | `int64` | 文件版本 (僅在成功的動作時回傳)。 |
| `forced_refresh` | `bool` | 若為 `true`，則強制文件在操作後立即變為可見。 |
| `get` | [`InlineGetDictUserDefined`](#inlinegetdictuserdefined-fields) | 包含從內嵌 get 回傳的文件 `source` (若有要求)。 |

### InlineGetDictUserDefined 欄位

[`InlineGetDictUserDefined`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L1126) 訊息包含從內嵌 get 操作回傳的文件來源。

| 欄位 | Protobuf 類型 | 說明 |
| :---- | :---- | :---- |
| `metadata_fields` | `optional` [`ObjectMap`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L3890) | 文件的中繼資料欄位。 |
| `fields` | `optional` [`ObjectMap`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L3890) | 文件的儲存欄位。 |
| `found` | `bool` | 文件是否存在。 |
| `x_seq_no` | `optional int64` | 文件的序號。 |
| `x_primary_term` | `optional int64` | 文件的主要分片任期。 |
| `x_routing` | `optional string` | 文件的路由值。 |
| `x_source` | `optional bytes` | 文件的來源資料。 |

## 回應範例

```json
{
  "errors": false,
  "items": [
    {
      "index": {
        "x_id": "2",
        "x_index": "my_index",
        "status": 201,
        "x_primary_term": 1,
        "result": "created",
        "x_seq_no": 0,
        "x_shards": {
          "successful": 1,
          "total": 2
        },
        "x_version": 1,
        "forced_refresh": true
      }
    },
    {
      "create": {
        "x_id": "1",
        "x_index": "my_index",
        "status": 201,
        "x_primary_term": 1,
        "result": "created",
        "x_seq_no": 0,
        "x_shards": {
          "successful": 1,
          "total": 2
        },
        "x_version": 1,
        "forced_refresh": true
      }
    },
    {
      "update": {
        "x_id": "2",
        "x_index": "my_index",
        "status": 200,
        "x_primary_term": 1,
        "result": "updated",
        "x_seq_no": 1,
        "x_shards": {
          "successful": 1,
          "total": 2
        },
        "x_version": 2,
        "forced_refresh": true,
        "get": {
          "found": true,
          "x_seq_no": 1,
          "x_primary_term": 1,
          "x_source": "e30="
        }
      }
    },
    {
      "delete": {
        "x_id": "2",
        "x_index": "my_index",
        "status": 200,
        "x_primary_term": 1,
        "result": "deleted",
        "x_seq_no": 2,
        "x_shards": {
          "successful": 1,
          "total": 2
        },
        "x_version": 3,
        "forced_refresh": true
      }
    }
  ],
  "took": 87,
  "ingest_took": 0
}
```
{% include copy.html %}


## Java gRPC 用戶端範例

下列範例顯示一個 Java 用戶端程式，提交範例批次 gRPC 請求，然後檢查批次回應中是否有任何錯誤：

```java
import org.opensearch.protobufs.*;
import io.grpc.ManagedChannel;
import io.grpc.ManagedChannelBuilder;
import com.google.protobuf.ByteString;

public class BulkClient {
    public static void main(String[] args) {
        ManagedChannel channel = ManagedChannelBuilder.forAddress("localhost", 9400)
                .usePlaintext()
                .build();

        DocumentServiceGrpc.DocumentServiceBlockingStub stub = DocumentServiceGrpc.newBlockingStub(channel);

        // Create an index operation
        IndexOperation indexOp = IndexOperation.newBuilder()
                .setXIndex("my-index")
                .setXId("1")
                .build();

        BulkRequestBody indexBody = BulkRequestBody.newBuilder()
                .setOperationContainer(OperationContainer.newBuilder().setIndex(indexOp).build())
                .setObject(ByteString.copyFromUtf8("{\"field\": \"value\"}"))
                .build();

        // Create a delete operation
        DeleteOperation deleteOp = DeleteOperation.newBuilder()
                .setXIndex("my-index")
                .setXId("2")
                .build();

        BulkRequestBody deleteBody = BulkRequestBody.newBuilder()
                .setOperationContainer(OperationContainer.newBuilder().setDelete(deleteOp).build())
                .build();

        // Build the bulk request
        BulkRequest request = BulkRequest.newBuilder()
                .setIndex("my-index")
                .addBulkRequestBody(indexBody)
                .addBulkRequestBody(deleteBody)
                .build();

        // Execute the bulk request
        try {
            BulkResponse response = stub.bulk(request);

            // Handle the response
            System.out.println("Bulk errors: " + response.getErrors());
            System.out.println("Bulk took: " + response.getTook() + " ms");
            if (response.hasIngestTook()) {
                System.out.println("Ingest took: " + response.getIngestTook() + " ms");
            }

            // Process individual items
            for (Item item : response.getItemsList()) {
                if (item.hasIndex()) {
                    System.out.println("Index operation: " + item.getIndex().getStatus());
                } else if (item.hasDelete()) {
                    System.out.println("Delete operation: " + item.getDelete().getStatus());
                } else if (item.hasCreate()) {
                    System.out.println("Create operation: " + item.getCreate().getStatus());
                } else if (item.hasUpdate()) {
                    System.out.println("Update operation: " + item.getUpdate().getStatus());
                }
            }
        } catch (io.grpc.StatusRuntimeException e) {
            System.err.println("gRPC request failed with status: " + e.getStatus());
            System.err.println("Error message: " + e.getMessage());
        }

        channel.shutdown();
    }
}
```
{% include copy.html %}

## Python gRPC 用戶端範例

下列範例示範如何使用 Python 用戶端應用程式傳送相同的請求。

首先，使用 `pip` 安裝 `opensearch-protobufs` 套件：

```bash
pip install opensearch-protobufs==1.2.0
```
{% include copy.html %}

使用下列程式碼傳送請求：

```python
import grpc

from opensearch.protobufs.schemas import *
from opensearch.protobufs.services import DocumentServiceStub

channel = grpc.insecure_channel(
    target="localhost:9400",
)

document_stub = DocumentServiceStub(channel)

# Add documents to a request body
requestBody = BulkRequestBody(
    operation_container=OperationContainer(index=IndexOperation())
)
requestBody.object = "{\"field\": \"value\"}".encode('utf-8')

# Append to a bulk request
request = BulkRequest()
request.index = "my-index"
request.bulk_request_body.append(requestBody)

# Send request and handle response
try:
    response = document_stub.Bulk(request=request)
    if response.items:
        print("Received {} response items".format(len(response.items)))
        print(response.items)
except grpc.RpcError as e:
    if e.code() == StatusCode.UNAVAILABLE:
        print("Failed to reach server: {}".format(e))
    elif e.code() == StatusCode.PERMISSION_DENIED:
        print("Permission denied: {}".format(e))
    elif e.code() == StatusCode.INVALID_ARGUMENT:
        print("Invalid argument: {}".format(e))
finally:
    channel.close()
```
{% include copy.html %}
