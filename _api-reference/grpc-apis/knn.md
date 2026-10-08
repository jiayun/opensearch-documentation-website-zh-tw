---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: k-NN (gRPC)
parent: gRPC APIs
nav_order: 30
---

# k-NN (gRPC) API
**3.2 版新增**
{: .label .label-purple }


gRPC k-NN API 已正式推出 (GA)。不過，隨著此功能在後續版本中逐漸成熟，protobuf 結構可能會有所更新。

gRPC k-NN API 提供高效能的二進位編碼介面，可透過 gRPC 使用 protocol buffers 執行 k 最近鄰 (k-nearest neighbor) 搜尋。k-NN 外掛程式提供專門用於向量相似度搜尋的查詢類型。與傳統的 HTTP 方式相比，此 API 具有更佳的效能，非常適合大規模機器學習與向量資料庫應用。

如需 HTTP 方式的 k-NN 查詢資訊，請參閱 [k-NN 查詢]({{site.url}}{{site.baseurl}}/query-dsl/specialized/k-nn/)。

## 必要條件

若要送出 gRPC 請求，用戶端必須具備一組 protobufs。取得 protobufs 的方式請參閱 [使用 gRPC API]({{site.url}}{{site.baseurl}}/api-reference/grpc-apis/index/#how-to-use-grpc-apis)。

## gRPC 服務與方法

gRPC k-NN API 位於 [`SearchService`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/services/search_service.proto#L22)，與一般搜尋作業使用相同的服務。

您可以在 `SearchService` 中呼叫 [`Search`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/services/search_service.proto#L23) gRPC 方法來送出 k-NN 搜尋請求，並在搜尋請求中使用 [`KnnQuery`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L2023)。此方法接受 [`SearchRequest`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L20) 並傳回 [`SearchResponse`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L262)。

gRPC 實作使用與 HTTP API 相同的底層 k-NN 功能，同時透過 protocol buffer 序列化提供更佳的效能。

## KnnQuery 欄位

gRPC k-NN API 在 [`QueryContainer`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L1368) 中使用 [`KnnQuery`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L2023) 訊息來執行 k-NN 搜尋。`KnnQuery` 訊息接受下列欄位。

| 欄位 | Protobuf 類型 | 說明 |
| :---- | :---- | :---- |
| `field` | `string` | 要對其執行搜尋查詢的向量欄位。必要。 |
| `vector` | `repeated float` | 查詢向量。必須與向量欄位具有相同的維度數。選用。 |
| `k` | `int32` | 要作為前幾筆結果 (top hits) 傳回的最近鄰數量。選用。 |
| `min_score` | `float` | 鄰居被視為命中所需的最低相似度分數。選用。 |
| `max_distance` | `float` | 鄰居被視為命中所需的向量空間中最大實體距離。選用。 |
| `filter` | [`QueryContainer`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L1368) | k-NN 搜尋查詢的篩選條件。請參閱 [篩選限制](#filter-limitations)。選用。 |
| `boost` | `float` | 用於提高或降低相關性分數的加權值 (boost)。預設為 1.0。選用。 |
| `underscore_name` | `string` | 用於查詢標記的查詢名稱 (JSON 鍵：`_name`)。選用。 |
| `method_parameters` | [`ObjectMap`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L3890) | 演算法專屬參數 (例如 `ef_search` 或 `nprobes`)。選用。 |
| `rescore` | [`KnnQueryRescore`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L2073) | 用於提升準確度的重新評分 (rescoring) 組態。適用於 2.17 之後的版本。選用。 |
| `expand_nested_docs` | `bool` | 當設為 `true` 時，會擷取每個父文件內所有巢狀欄位文件的分數。用於巢狀查詢。選用。 |

## 請求範例

下列範例顯示包含 k-NN 查詢的 gRPC 搜尋請求。它會在 `vector_index` 索引的 `my_vector` 欄位中搜尋與查詢向量 `[0.1, 0.2, 0.3, 0.4]` 最相似的 10 個向量：

```json
{
  "index": ["vector_index"],
  "search_request_body": {
    "query": {
      "knn": {
        "field": "my_vector",
        "vector": [0.1, 0.2, 0.3, 0.4],
        "k": 10
      }
    },
    "size": 10
  }
}
```
{% include copy.html %}

## Java gRPC 用戶端範例

以下是使用 gRPC k-NN API 的基本範例 (實際實作取決於您的 gRPC 用戶端設定)：

```java
import org.opensearch.protobufs.*;
import io.grpc.ManagedChannel;
import io.grpc.ManagedChannelBuilder;

public class KnnGrpcClient {
    public static void main(String[] args) {
        ManagedChannel channel = ManagedChannelBuilder.forAddress("localhost", 9400)
                .usePlaintext()
                .build();

        // Create a gRPC stub for search operations
        SearchServiceGrpc.SearchServiceBlockingStub searchStub =
            SearchServiceGrpc.newBlockingStub(channel);

        // Build a k-NN query using protocol buffers
        QueryContainer knnQuery = QueryContainer.newBuilder()
            .setKnn(KnnQuery.newBuilder()
                .setField("my_vector")
                .addAllVector(Arrays.asList(0.1f, 0.2f, 0.3f, 0.4f))
                .setK(10)
                .build())
            .build();

        // Create the search request
        SearchRequest request = SearchRequest.newBuilder()
            .addIndex("vector_index")
            .setSearchRequestBody(SearchRequestBody.newBuilder()
                .setQuery(knnQuery)
                .setSize(10)
                .build())
            .build();

        // Execute the search
        try {
            SearchResponse response = searchStub.search(request);

            // Handle the response
            System.out.println("Search took: " + response.getTook() + " ms");

            HitsMetadata hits = response.getHits();
            if (hits.hasTotal()) {
                System.out.println("Found " + hits.getTotal().getTotalHits().getValue() + " results");
            }

            // Process k-NN results with similarity scores
            for (HitsMetadataHitsInner hit : hits.getHitsList()) {
                System.out.println("Document ID: " + hit.getXId());
                if (hit.hasXScore()) {
                    System.out.println("Similarity score: " + hit.getXScore().getDouble());
                }
            }
        } catch (io.grpc.StatusRuntimeException e) {
            System.err.println("gRPC k-NN search request failed with status: " + e.getStatus());
            System.err.println("Error message: " + e.getMessage());
        }

        channel.shutdown();
    }
}
```
{% include copy.html %}

## 回應欄位

k-NN 搜尋請求會傳回與一般搜尋作業相同的 [`SearchResponse`](https://github.com/opensearch-project/opensearch-protobufs/blob/1.7.0/protos/schemas/common.proto#L262) 結構。如需回應欄位的資訊，請參閱 [Search (gRPC) 回應欄位]({{site.url}}{{site.baseurl}}/api-reference/grpc-apis/search/#response-fields)。

回應包含標準搜尋中繼資料 (`took`、`timed_out` 與 `shards`)，以及包含 k-NN 文件及其相似度分數的 `hits` 陣列。

## 篩選限制

與 HTTP API 相比，gRPC k-NN API 對 `filter` 子句的支援有限。如需 gRPC 目前支援的查詢類型清單，請參閱 [Search API QueryContainer 文件]({{site.url}}{{site.baseurl}}/api-reference/grpc-apis/search/#querycontainer-fields) 與 [支援的查詢]({{site.url}}{{site.baseurl}}/api-reference/grpc-apis/search/#supported-queries)。

若有複雜的篩選需求，請考慮使用 HTTP k-NN API、簡化您的篩選邏輯，或等待下一版 k-NN gRPC。



## 相關 API

- [Search (gRPC)]({{site.url}}{{site.baseurl}}/api-reference/grpc-apis/search/) - 一般 gRPC 搜尋功能
- [Bulk (gRPC)]({{site.url}}{{site.baseurl}}/api-reference/grpc-apis/bulk/) - 使用 gRPC 的大量作業
- [k-NN 查詢]({{site.url}}{{site.baseurl}}/query-dsl/specialized/k-nn/) - HTTP 方式的 k-NN 查詢文件

## 後續步驟

- 進一步了解 [OpenSearch 中的向量搜尋]({{site.url}}{{site.baseurl}}/search-plugins/knn/index/)。
- 探索 [k-NN 索引設定]({{site.url}}{{site.baseurl}}/search-plugins/knn/knn-index/)。
- 檢閱 [k-NN 效能調校]({{site.url}}{{site.baseurl}}/search-plugins/knn/performance-tuning/)。
- 閱讀 [gRPC 組態]({{site.url}}{{site.baseurl}}/api-reference/grpc-apis/index/#grpc-settings)。
