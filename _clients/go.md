---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "Go 用戶端"
nav_order: 50
---

# Go 用戶端

OpenSearch Go 用戶端可讓您將 Go 應用程式連線至 OpenSearch 叢集中的資料。本入門指南說明如何連線至 OpenSearch、將文件編製索引，以及執行查詢。如需用戶端完整的 API 文件和其他範例，請參閱 [Go 用戶端 API 文件](https://pkg.go.dev/github.com/opensearch-project/opensearch-go/v5)。

如需用戶端原始碼，請參閱 [`opensearch-go` 儲存庫](https://github.com/opensearch-project/opensearch-go)。


## 安裝 Go 用戶端

Go 用戶端需要 Go 1.26 或更新版本。

如果您要開始新專案，請執行下列命令來建立新模組：

```bash
go mod init <mymodulename>
```
{% include copy.html %}

若要將 Go 用戶端加入您的專案，請執行下列命令：

```bash
go get github.com/opensearch-project/opensearch-go/v5
```
{% include copy.html %}

第 5 版用戶端與為第 4 版撰寫的程式碼不相容。如需遷移說明，請參閱 [v5 升級指南](https://github.com/opensearch-project/opensearch-go/blob/main/UPGRADING_V5.md)。

## 連線至 OpenSearch

本頁的範例使用下列匯入：

```go
import (
	"context"
	"encoding/json"
	"fmt"
	"strings"

	"github.com/opensearch-project/opensearch-go/v5"
	"github.com/opensearch-project/opensearch-go/v5/opensearchapi"
	"github.com/opensearch-project/opensearch-go/v5/opensearchutil"
)
```
{% include copy.html %}

若要連線至預設的 OpenSearch 主機，如果您使用 Security 外掛程式，請建立位址為 `https://localhost:9200` 的用戶端物件：

```go
client, err := opensearchapi.NewClient(opensearchapi.Config{
	Client: opensearch.Config{
		Addresses:            []string{"https://localhost:9200"},
		InsecureSkipVerify:   true,    // For testing only. Use certificate for validation.
		Username:             "admin", // For testing only. Don't store credentials in code.
		Password:             "<custom-admin-password>",
		DiscoverNodesOnStart: new(false),
	},
})
```
{% include copy.html %}

如果您未使用 Security 外掛程式，請建立位址為 `http://localhost:9200` 的用戶端物件：

```go
client, err := opensearchapi.NewClient(opensearchapi.Config{
	Client: opensearch.Config{
		Addresses:            []string{"http://localhost:9200"},
		DiscoverNodesOnStart: new(false),
	},
})
```
{% include copy.html %}

根據預設，用戶端會在啟動時探索叢集中的節點，然後將請求傳送至節點的發布位址。如果您的應用程式無法連線至這些位址（例如 OpenSearch 在 Docker 中執行時），請求就會逾時。將 `DiscoverNodesOnStart` 設為 `false` 可讓用戶端只將請求傳送至您在 `Addresses` 中指定的位址。

## 連線至 Amazon OpenSearch Service

在下列範例中，請將端點取代為您的網域端點，該端點列於 Amazon OpenSearch Service 主控台中網域的詳細資料頁面。

下列範例說明如何連線至 Amazon OpenSearch Service：

```go
package main

import (
	"context"
	"log"

	"github.com/aws/aws-sdk-go-v2/aws"
	"github.com/aws/aws-sdk-go-v2/config"
	"github.com/opensearch-project/opensearch-go/v5"
	"github.com/opensearch-project/opensearch-go/v5/opensearchapi"
	requestsigner "github.com/opensearch-project/opensearch-go/v5/signer/awsv2"
)

const endpoint = "https://search-<domain-name>-<id>.us-east-1.es.amazonaws.com" // OpenSearch domain endpoint

func main() {
	ctx := context.Background()

	awsCfg, err := config.LoadDefaultConfig(ctx,
		config.WithRegion("us-east-1"),
		config.WithCredentialsProvider(
			getCredentialProvider("<AWS_ACCESS_KEY>", "<AWS_SECRET_ACCESS_KEY>", "<AWS_SESSION_TOKEN>"),
		),
	)
	if err != nil {
		log.Fatal(err) // Do not log.Fatal in a production-ready app.
	}

	// Create an AWS request signer for Amazon OpenSearch Service.
	signer, err := requestsigner.NewSignerWithService(awsCfg, "es")
	if err != nil {
		log.Fatal(err) // Do not log.Fatal in a production-ready app.
	}

	// Create an OpenSearch client that uses the request signer.
	client, err := opensearchapi.NewClient(opensearchapi.Config{
		Client: opensearch.Config{
			Addresses:            []string{endpoint},
			Signer:               signer,
			DiscoverNodesOnStart: new(false),
		},
	})
	if err != nil {
		log.Fatal("client creation err", err)
	}

	_ = client
	// Your code here
}

func getCredentialProvider(accessKey, secretAccessKey, token string) aws.CredentialsProviderFunc {
	return func(ctx context.Context) (aws.Credentials, error) {
		c := &aws.Credentials{
			AccessKeyID:     accessKey,
			SecretAccessKey: secretAccessKey,
			SessionToken:    token,
		}
		return *c, nil
	}
}
```
{% include copy.html %}

若要在此範例或 Amazon OpenSearch Serverless 範例中使用預設的 AWS 憑證鏈，請省略 `config.WithCredentialsProvider` 選項。

## 連線至 Amazon OpenSearch Serverless

在下列範例中，請將端點取代為您的集合端點，該端點列於 Amazon OpenSearch Service 主控台中集合的詳細資料頁面。

下列範例說明如何連線至 Amazon OpenSearch Serverless：

```go
package main

import (
	"context"
	"log"

	"github.com/aws/aws-sdk-go-v2/aws"
	"github.com/aws/aws-sdk-go-v2/config"
	"github.com/opensearch-project/opensearch-go/v5"
	"github.com/opensearch-project/opensearch-go/v5/opensearchapi"
	requestsigner "github.com/opensearch-project/opensearch-go/v5/signer/awsv2"
)

const endpoint = "https://<collection-id>.us-east-1.aoss.amazonaws.com" // OpenSearch Serverless collection endpoint

func main() {
	ctx := context.Background()

	awsCfg, err := config.LoadDefaultConfig(ctx,
		config.WithRegion("us-east-1"),
		config.WithCredentialsProvider(
			getCredentialProvider("<AWS_ACCESS_KEY>", "<AWS_SECRET_ACCESS_KEY>", "<AWS_SESSION_TOKEN>"),
		),
	)
	if err != nil {
		log.Fatal(err) // Do not log.Fatal in a production-ready app.
	}

	// Create an AWS request signer for Amazon OpenSearch Serverless.
	signer, err := requestsigner.NewSignerWithService(awsCfg, "aoss")
	if err != nil {
		log.Fatal(err) // Do not log.Fatal in a production-ready app.
	}

	// Create an OpenSearch client that uses the request signer.
	client, err := opensearchapi.NewClient(opensearchapi.Config{
		Client: opensearch.Config{
			Addresses:            []string{endpoint},
			Signer:               signer,
			DiscoverNodesOnStart: new(false),
		},
	})
	if err != nil {
		log.Fatal("client creation err", err)
	}

	_ = client
	// Your code here
}

func getCredentialProvider(accessKey, secretAccessKey, token string) aws.CredentialsProviderFunc {
	return func(ctx context.Context) (aws.Credentials, error) {
		c := &aws.Credentials{
			AccessKeyID:     accessKey,
			SecretAccessKey: secretAccessKey,
			SessionToken:    token,
		}
		return *c, nil
	}
}
```
{% include copy.html %}

Amazon OpenSearch Serverless 支援部分 OpenSearch API 操作，且不支援本頁範例中使用的 `refresh` 參數。如需詳細資訊，請參閱 [Amazon OpenSearch Serverless 中支援的操作和外掛程式](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/serverless-genref.html)。
{: .note}

`opensearchapi.NewClient` 建構函式接受 `opensearchapi.Config{}` 類型。其 `Client` 欄位包含 `opensearch.Config{}` 類型，可使用 OpenSearch 節點位址清單或使用者名稱與密碼組合等選項進行自訂。

若要連線至多個 OpenSearch 節點，請在 `Addresses` 參數中指定這些節點：

```go
var (
	urls = []string{"http://localhost:9200", "http://localhost:9201", "http://localhost:9202"}
)

client, err := opensearchapi.NewClient(opensearchapi.Config{
	Client: opensearch.Config{
		Addresses:            urls,
		DiscoverNodesOnStart: new(false),
	},
})
```
{% include copy.html %}

根據預設，Go 用戶端最多會重試請求三次。若要自訂重試次數，請設定 `MaxRetries` 參數。此外，您可以設定 `RetryOnStatus` 參數，變更會觸發請求重試的回應碼清單。下列程式碼片段會建立具有自訂 `MaxRetries` 和 `RetryOnStatus` 值的新 Go 用戶端：

```go
client, err := opensearchapi.NewClient(opensearchapi.Config{
	Client: opensearch.Config{
		Addresses:            []string{"http://localhost:9200"},
		DiscoverNodesOnStart: new(false),
		MaxRetries:           5,
		RetryOnStatus:        []int{502, 503, 504},
	},
})
```
{% include copy.html %}

## 範例資料

本頁的範例使用 `Student` 結構來表示文件。JSON 標籤決定已編製索引文件中的欄位名稱：

```go
type Student struct {
	FirstName string  `json:"firstName"`
	LastName  string  `json:"lastName"`
	GPA       float64 `json:"gpa"`
	GradDate  string  `json:"gradDate"`
}
```
{% include copy.html %}

## 建立索引

下列範例建立具有一個主要分片和一個副本的索引。它明確將 `gradDate` 欄位對應為採用 `yyyy-MM-dd` 格式的 `date`。當您將文件編製索引時，OpenSearch 會動態對應其他文件欄位：

```go
ctx := context.Background()
index := "students"
body := `{
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
}`
createResp, err := client.Indices.Create(ctx, opensearchapi.IndicesCreateReq{
	Index:      index,
	BodyReader: strings.NewReader(body),
})
```
{% include copy.html %}

## 將文件編製索引

使用下列程式碼將文件編製索引。將 `Refresh` 參數設定為 `true`，即可立即搜尋該文件：

```go
student := Student{FirstName: "John", LastName: "Doe", GPA: 3.89, GradDate: "2022-05-15"}
indexResp, err := client.Doc.Index(ctx, opensearchapi.IndexReq{
	Index:  index,
	ID:     "1",
	Body:   opensearchutil.NewJSONReader(student),
	Params: &opensearchapi.IndexParams{Refresh: "true"},
})
```
{% include copy.html %}

## 批次編製索引

使用下列程式碼，在單一請求中將多個文件編製索引。請求本文中，每個文件都有一行動作，後面接著一行文件內容，而且每一行都必須以換行字元結尾：

```go
students := []struct {
	id      string
	student Student
}{
	{"2", Student{FirstName: "Paulo", LastName: "Santos", GPA: 3.93, GradDate: "2021-05-20"}},
	{"3", Student{FirstName: "Shirley", LastName: "Rodriguez", GPA: 3.91, GradDate: "2019-05-10"}},
}
var bulkBody strings.Builder
for _, s := range students {
	doc, err := json.Marshal(s.student)
	if err != nil {
		return err
	}
	fmt.Fprintf(&bulkBody, "{\"index\":{\"_id\":%q}}\n%s\n", s.id, doc)
}
bulkResp, err := client.Doc.Bulk(ctx, opensearchapi.BulkReq{
	Index:  index,
	Body:   strings.NewReader(bulkBody.String()),
	Params: &opensearchapi.BulkParams{Refresh: "true"},
})
```
{% include copy.html %}

如果任何操作失敗，此方法會連同回應一起傳回 `*opensearchapi.PartialBulkError` 錯誤。若要檢查每個操作的結果，請查看 `bulkResp.Items` 欄位。

## 搜尋文件

使用下列程式碼搜尋索引中的所有文件：

```go
searchResp, err := client.Search(ctx, &opensearchapi.SearchReq{
	Indices: []string{index},
})
if err != nil {
	return err
}
for _, hit := range searchResp.Hits.Hits {
	var s Student
	if err := json.Unmarshal(hit.Source, &s); err != nil {
		return err
	}
	out, err := json.Marshal(s)
	if err != nil {
		return err
	}
	fmt.Println(string(out))
}
```
{% include copy.html %}

在 `searchResp.Hits.Hits` 的每個項目中，`ID` 欄位包含指向文件 ID 的指標，而 `Source` 欄位包含原始 JSON 格式的文件。若要存取文件欄位，請將 `Source` 反序列化為 `Student` 結構：

```go
for _, hit := range searchResp.Hits.Hits {
	var s Student
	if err := json.Unmarshal(hit.Source, &s); err != nil {
		return err
	}
	fmt.Printf("ID: %s, name: %s %s, GPA: %v, graduation date: %s\n", *hit.ID, s.FirstName, s.LastName, s.GPA, s.GradDate)
}
```
{% include copy.html %}

使用範圍查詢進行搜尋：

```go
searchResp, err := client.Search(ctx, &opensearchapi.SearchReq{
	Indices:    []string{index},
	BodyReader: strings.NewReader(`{"query": {"range": {"gradDate": {"gte": "2019-01-01", "lte": "2019-12-31"}}}}`),
})
```
{% include copy.html %}

## 將結果分頁

若要將結果分頁，請使用 `from` 和 `size` 參數。下列範例依畢業日期排序學生，並且每次擷取兩筆結果。第一個請求傳回第一頁結果，第二個請求則傳回下一頁：

```go
searchResp, err := client.Search(ctx, &opensearchapi.SearchReq{
	Indices: []string{index},
	Params:  &opensearchapi.SearchParams{From: 0, Size: new(2), Sort: []string{"gradDate:asc"}},
})
if err != nil {
	return err
}
nextResp, err := client.Search(ctx, &opensearchapi.SearchReq{
	Indices: []string{index},
	Params:  &opensearchapi.SearchParams{From: 2, Size: new(2), Sort: []string{"gradDate:asc"}},
})
if err != nil {
	return err
}
for i, resp := range []*opensearchapi.SearchResp{searchResp, nextResp} {
	fmt.Printf("Page %d:\n", i+1)
	for _, hit := range resp.Hits.Hits {
		var s Student
		if err := json.Unmarshal(hit.Source, &s); err != nil {
			return err
		}
		out, err := json.Marshal(s)
		if err != nil {
			return err
		}
		fmt.Println("  " + string(out))
	}
}
```
{% include copy.html %}

`from` 和 `size` 參數適合用於前幾頁的結果。若要瀏覽大量結果的各個分頁，請搭配 `search_after` 使用時間點。若需詳細資訊，請參閱[將結果分頁]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/paginate/)。

## 更新文件

使用 `doc` 欄位中的部分文件，更新文件的特定欄位。只會更新指定的欄位：

```go
updateResp, err := client.Doc.Update(ctx, opensearchapi.UpdateReq{
	Index:      index,
	ID:         "1",
	BodyReader: strings.NewReader(`{"doc": {"gpa": 3.92}}`),
})
```
{% include copy.html %}

## 刪除文件

使用下列程式碼刪除文件：

```go
deleteResp, err := client.Doc.Delete(ctx, opensearchapi.DeleteReq{
	Index:  index,
	ID:     "3",
	Params: &opensearchapi.DeleteParams{Refresh: "true"},
})
```
{% include copy.html %}

## 刪除索引

使用下列程式碼刪除索引：

```go
deleteIndexResp, err := client.Indices.Delete(ctx, &opensearchapi.IndicesDeleteReq{Indices: []string{index}})
```
{% include copy.html %}

## 範例程式

此範例程式整合了前面各節的程式碼。它會連線至已啟用 Security 外掛程式的叢集。若要連線至未使用 Security 外掛程式的叢集，請修改以 `// Without security` 註解標記的程式碼行。

此範例程式僅供測試使用。它在程式碼中指定認證資訊，並停用憑證驗證，以便連線至使用自我簽署憑證的叢集。在正式環境中，請從安全的位置載入認證資訊，並驗證叢集的憑證。
{: .warning}

下列範例程式會建立用戶端、建立索引、逐一及批次將文件編製索引、搜尋文件、更新文件、刪除文件，最後刪除索引：

```go
package main

import (
	"context"
	"encoding/json"
	"fmt"
	"os"
	"strings"

	"github.com/opensearch-project/opensearch-go/v5"
	"github.com/opensearch-project/opensearch-go/v5/opensearchapi"
	"github.com/opensearch-project/opensearch-go/v5/opensearchutil"
)

type Student struct {
	FirstName string  `json:"firstName"`
	LastName  string  `json:"lastName"`
	GPA       float64 `json:"gpa"`
	GradDate  string  `json:"gradDate"`
}

func main() {
	if err := run(); err != nil {
		fmt.Println("Error:", err)
		os.Exit(1)
	}
}

func run() error {
	ctx := context.Background()

	client, err := opensearchapi.NewClient(opensearchapi.Config{
		Client: opensearch.Config{
			// Without security, use http://localhost:9200
			Addresses: []string{"https://localhost:9200"},
			// Without security, remove this line
			InsecureSkipVerify: true,
			// Without security, remove this line
			Username: "admin",
			// Without security, remove this line
			Password:             "<custom-admin-password>",
			DiscoverNodesOnStart: new(false),
		},
	})
	if err != nil {
		return err
	}

	// Create the index
	index := "students"
	fmt.Println("Creating index......")
	body := `{
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
	}`
	createResp, err := client.Indices.Create(ctx, opensearchapi.IndicesCreateReq{
		Index:      index,
		BodyReader: strings.NewReader(body),
	})
	if err != nil {
		return err
	}
	fmt.Println("Index created:", createResp.Index)

	// Index a document
	fmt.Println("\nIndexing one student......")
	student := Student{FirstName: "John", LastName: "Doe", GPA: 3.89, GradDate: "2022-05-15"}
	indexResp, err := client.Doc.Index(ctx, opensearchapi.IndexReq{
		Index:  index,
		ID:     "1",
		Body:   opensearchutil.NewJSONReader(student),
		Params: &opensearchapi.IndexParams{Refresh: "true"},
	})
	if err != nil {
		return err
	}
	fmt.Printf("Result: %s, id: %s, version: %d\n", indexResp.Result, indexResp.ID, indexResp.Version)

	// Bulk index documents
	fmt.Println("\nIndexing many students......")
	students := []struct {
		id      string
		student Student
	}{
		{"2", Student{FirstName: "Paulo", LastName: "Santos", GPA: 3.93, GradDate: "2021-05-20"}},
		{"3", Student{FirstName: "Shirley", LastName: "Rodriguez", GPA: 3.91, GradDate: "2019-05-10"}},
	}
	var bulkBody strings.Builder
	for _, s := range students {
		doc, err := json.Marshal(s.student)
		if err != nil {
			return err
		}
		fmt.Fprintf(&bulkBody, "{\"index\":{\"_id\":%q}}\n%s\n", s.id, doc)
	}
	bulkResp, err := client.Doc.Bulk(ctx, opensearchapi.BulkReq{
		Index:  index,
		Body:   strings.NewReader(bulkBody.String()),
		Params: &opensearchapi.BulkParams{Refresh: "true"},
	})
	if err != nil {
		return err
	}
	fmt.Println("Errors:", bulkResp.Errors)
	for _, item := range bulkResp.Items {
		fmt.Printf("  %s id: %s\n", *item.Index.Result, *item.Index.ID)
	}

	// Search for all students
	fmt.Println("\nSearching for all students......")
	searchResp, err := client.Search(ctx, &opensearchapi.SearchReq{
		Indices: []string{index},
		Params:  &opensearchapi.SearchParams{From: 0, Size: new(2), Sort: []string{"gradDate:asc"}},
	})
	if err != nil {
		return err
	}
	total, err := searchResp.Hits.Total.TotalHits()
	if err != nil {
		return err
	}
	fmt.Println("Total hits:", total.Value)
	nextResp, err := client.Search(ctx, &opensearchapi.SearchReq{
		Indices: []string{index},
		Params:  &opensearchapi.SearchParams{From: 2, Size: new(2), Sort: []string{"gradDate:asc"}},
	})
	if err != nil {
		return err
	}
	for i, resp := range []*opensearchapi.SearchResp{searchResp, nextResp} {
		fmt.Printf("Page %d:\n", i+1)
		for _, hit := range resp.Hits.Hits {
			var s Student
			if err := json.Unmarshal(hit.Source, &s); err != nil {
				return err
			}
			out, err := json.Marshal(s)
			if err != nil {
				return err
			}
			fmt.Println("  " + string(out))
		}
	}

	// Search for students who graduated in 2019
	fmt.Println("\nSearching for students who graduated in 2019......")
	searchResp, err = client.Search(ctx, &opensearchapi.SearchReq{
		Indices:    []string{index},
		BodyReader: strings.NewReader(`{"query": {"range": {"gradDate": {"gte": "2019-01-01", "lte": "2019-12-31"}}}}`),
	})
	if err != nil {
		return err
	}
	total, err = searchResp.Hits.Total.TotalHits()
	if err != nil {
		return err
	}
	fmt.Println("Total hits:", total.Value)
	for _, hit := range searchResp.Hits.Hits {
		var s Student
		if err := json.Unmarshal(hit.Source, &s); err != nil {
			return err
		}
		out, err := json.Marshal(s)
		if err != nil {
			return err
		}
		fmt.Println("  " + string(out))
	}

	// Update a document
	fmt.Println("\nUpdating a student's GPA......")
	updateResp, err := client.Doc.Update(ctx, opensearchapi.UpdateReq{
		Index:      index,
		ID:         "1",
		BodyReader: strings.NewReader(`{"doc": {"gpa": 3.92}}`),
	})
	if err != nil {
		return err
	}
	fmt.Printf("Result: %s, version: %d\n", updateResp.Result, updateResp.Version)

	// Get the updated document
	getResp, err := client.Doc.Get(ctx, opensearchapi.GetReq{Index: index, ID: "1"})
	if err != nil {
		return err
	}
	var updated Student
	if err := json.Unmarshal(getResp.Source, &updated); err != nil {
		return err
	}
	out, err := json.Marshal(updated)
	if err != nil {
		return err
	}
	fmt.Println("Updated document: " + string(out))

	// Delete a document
	fmt.Println("\nDeleting a student......")
	deleteResp, err := client.Doc.Delete(ctx, opensearchapi.DeleteReq{
		Index:  index,
		ID:     "3",
		Params: &opensearchapi.DeleteParams{Refresh: "true"},
	})
	if err != nil {
		return err
	}
	fmt.Println("Result:", deleteResp.Result)

	// Delete the index
	fmt.Println("\nDeleting the index......")
	deleteIndexResp, err := client.Indices.Delete(ctx, &opensearchapi.IndicesDeleteReq{Indices: []string{index}})
	if err != nil {
		return err
	}
	fmt.Println("Acknowledged:", deleteIndexResp.Acknowledged)

	return nil
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

- 如需更多使用用戶端的範例，請參閱 [`opensearch-go` 使用者指南](https://github.com/opensearch-project/opensearch-go/blob/main/USER_GUIDE.md)。
- 如需特定工作的指南，例如大量編製索引和搜尋，請參閱 [`opensearch-go` 指南](https://github.com/opensearch-project/opensearch-go/tree/main/guides)。
