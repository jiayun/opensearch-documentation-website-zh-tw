---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "低階 .NET 用戶端"
nav_order: 30
has_children: false
parent: .NET clients
---

# 低階 .NET 用戶端 (OpenSearch.Net)

OpenSearch.Net 是一個低階 .NET 用戶端，提供與 OpenSearch 通訊的基礎層。它沒有任何相依性，可以處理輪流負載平衡、傳輸以及基本的請求/回應循環。OpenSearch.Net 將所有 OpenSearch API 端點封裝為方法。使用 OpenSearch.Net 時，您需要自行建構查詢。

本入門指南說明如何連線至 OpenSearch、將文件編製索引，以及執行查詢。用戶端原始碼請參閱 [`opensearch-net` 儲存庫](https://github.com/opensearch-project/opensearch-net)。

## 穩定版本

本文件反映 [GitHub 儲存庫](https://github.com/opensearch-project/opensearch-net) 中最新的更新，可能包含目前穩定版本尚未提供的變更。NuGet 上目前的穩定版本為 [2.2.0](https://www.nuget.org/packages/OpenSearch.Net/2.2.0)。如需支援的 OpenSearch 版本與目標架構的資訊，請參閱[相容性]({{site.url}}{{site.baseurl}}/clients/dot-net/#compatibility)。

## 安裝 OpenSearch.Net 用戶端

若要安裝 OpenSearch.Net，請下載 [OpenSearch.Net NuGet 套件](https://www.nuget.org/packages/OpenSearch.Net)，並在您選擇的 IDE 中將其加入專案。在 Microsoft Visual Studio 中，請依照下列步驟操作：
- 在 **Solution Explorer** 面板中，以滑鼠右鍵按一下您的方案或專案，然後選取 **Manage NuGet Packages for Solution**。
- 搜尋 OpenSearch.Net NuGet 套件，然後選取 **Install**。

或者，您也可以使用 .NET CLI 將 OpenSearch.Net 加入專案：

```bash
dotnet add package OpenSearch.Net --version 2.2.0
```
{% include copy.html %}

您也可以將 OpenSearch.Net 加入 .csproj 檔案：

```xml
<Project>
  ...
  <ItemGroup>
    <PackageReference Include="OpenSearch.Net" Version="2.2.0" />
  </ItemGroup>
</Project>
```
{% include copy.html %}

## 範例資料

本頁的範例使用下列 `Student` 類別來代表一位學生，相當於索引中的一份文件。`ToString` 方法會將 `Student` 格式化以供主控台輸出：

```cs
using System.Globalization;
using System.Runtime.Serialization;

public class Student
{
    [DataMember(Name = "firstName")]
    public string FirstName { get; set; } = string.Empty;

    [DataMember(Name = "lastName")]
    public string LastName { get; set; } = string.Empty;

    [DataMember(Name = "gpa")]
    public double Gpa { get; set; }

    [DataMember(Name = "gradDate")]
    public string GradDate { get; set; } = string.Empty;

    public override string ToString() =>
        string.Format(CultureInfo.InvariantCulture,
            "{% raw %}Student{{firstName='{0}', lastName='{1}', gpa={2}, gradDate={3}}}{% endraw %}",
            FirstName, LastName, Gpa, GradDate);
}
```
{% include copy.html %}

預設情況下，OpenSearch.Net 會完全依照屬性名稱的宣告方式進行序列化。`DataMember` 屬性會指定欄位名稱，因此 `Student` 會被編製索引為包含 `firstName`、`lastName`、`gpa` 和 `gradDate` 欄位的文件。
{: .note}

## 連線至 OpenSearch

建立 OpenSearchLowLevelClient 物件以連線至預設 OpenSearch 主機 (`http://localhost:9200`) 時，請使用預設建構函式。

```cs
var client  = new OpenSearchLowLevelClient();
```
{% include copy.html %}

若要透過位址已知的單一節點連線至您的 OpenSearch 叢集，請使用該位址建立 ConnectionConfiguration 物件，並將其傳遞給 OpenSearch.Net 建構函式：

```cs
var nodeAddress = new Uri("http://myserver:9200");
var config = new ConnectionConfiguration(nodeAddress);
var client = new OpenSearchLowLevelClient(config);
```
{% include copy.html %}

您也可以使用[連線集區]({{site.url}}{{site.baseurl}}/clients/dot-net-conventions#connection-pools)來管理叢集中的節點。此外，您還可以設定連線組態，讓 OpenSearch 以格式化的 JSON 傳回回應。

```cs
var uri = new Uri("http://localhost:9200");
var connectionPool = new SingleNodeConnectionPool(uri);
var settings = new ConnectionConfiguration(connectionPool).PrettyJson();
var client = new OpenSearchLowLevelClient(settings);
```
{% include copy.html %}

若要使用多個節點連線至您的 OpenSearch 叢集，請使用這些節點的位址建立連線集區。在此範例中，使用的是 [`SniffingConnectionPool`]({{site.url}}{{site.baseurl}}/clients/dot-net-conventions#connection-pools)，因為它會追蹤叢集中被移除或加入的節點，因此最適合會自動擴展的叢集。

```cs
var uris = new[]
{
    new Uri("http://localhost:9200"),
    new Uri("http://localhost:9201"),
    new Uri("http://localhost:9202")
};
var connectionPool = new SniffingConnectionPool(uris);
var settings = new ConnectionConfiguration(connectionPool).PrettyJson();
var client = new OpenSearchLowLevelClient(settings);
```
{% include copy.html %}

## 連線至 Amazon OpenSearch Service

若要使用 AWS Signature Version 4 簽署對 Amazon OpenSearch Service 的請求，請安裝 OpenSearch.Net.Auth.AwsSigV4 套件。此套件相依於 OpenSearch.Net，因此也會一併安裝 OpenSearch.Net：

```bash
dotnet add package OpenSearch.Net.Auth.AwsSigV4 --version 2.2.0
```
{% include copy.html %}

`AwsSigV4HttpConnection` 會使用預設 AWS 憑證供應商鏈中的憑證來簽署請求。您傳遞給 `AwsSigV4HttpConnection` 的 Region 必須與您的網域或集合的 Region 相符。下列範例使用 `us-east-1` Region。

在下列範例中，請將端點替換為您的網域端點，該端點列於 Amazon OpenSearch Service 主控台中網域的詳細資料頁面。

下列範例說明如何連線至 Amazon OpenSearch Service：

```cs
using Amazon;
using OpenSearch.Net;
using OpenSearch.Net.Auth.AwsSigV4;

namespace Application
{
    class Program
    {
        static void Main(string[] args)
        {
            var endpoint = new Uri("https://search-<domain-name>-<id>.us-east-1.es.amazonaws.com");
            var connection = new AwsSigV4HttpConnection(RegionEndpoint.USEast1, service: AwsSigV4HttpConnection.OpenSearchService);
            var config = new ConnectionConfiguration(endpoint, connection);
            var client = new OpenSearchLowLevelClient(config);

            Console.WriteLine(client.RootNodeInfo<StringResponse>().Body);
        }
    }
}
```
{% include copy.html %}

## 連線至 Amazon OpenSearch Serverless

下列範例說明如何連線至 Amazon OpenSearch Serverless。請將端點替換為您的集合端點，該端點列於 Amazon OpenSearch Service 主控台中集合的詳細資料頁面：

```cs
using Amazon;
using OpenSearch.Net;
using OpenSearch.Net.Auth.AwsSigV4;

namespace Application
{
    class Program
    {
        static void Main(string[] args)
        {
            var endpoint = new Uri("https://<collection-id>.us-east-1.aoss.amazonaws.com");
            var connection = new AwsSigV4HttpConnection(RegionEndpoint.USEast1, service: AwsSigV4HttpConnection.OpenSearchServerlessService);
            var config = new ConnectionConfiguration(endpoint, connection);
            var client = new OpenSearchLowLevelClient(config);

            Console.WriteLine(client.Cat.Indices<StringResponse>().Body);
        }
    }
}
```
{% include copy.html %}

Amazon OpenSearch Serverless 支援 OpenSearch API 作業的子集，且不支援本頁範例中使用的 `refresh` 參數。如需更多資訊，請參閱 [Amazon OpenSearch Serverless 中支援的作業與外掛程式](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/serverless-genref.html)。
{: .note}

## 使用 ConnectionConfiguration

使用 `ConnectionConfiguration` 將組態選項傳遞給 OpenSearch.Net 用戶端。下列範例使用 `ConnectionConfiguration` 來：

- 啟用 gzip 壓縮的請求與回應。
- 通知 OpenSearch 傳回格式化的 JSON。

```cs
var uri = new Uri("http://localhost:9200");
var connectionPool = new SingleNodeConnectionPool(uri);
var settings = new ConnectionConfiguration(connectionPool)
    .EnableHttpCompression()
    .PrettyJson();

var client = new OpenSearchLowLevelClient(settings);
```
{% include copy.html %}

## 建立索引

下列範例會建立一個具有一個主要分片和一個副本的索引。此範例明確地將 `gradDate` 欄位對應為 `yyyy-MM-dd` 格式的 `date`。當您將文件編製索引時，OpenSearch 會動態對應其他文件欄位：

```cs
var index = "students";
var createIndexResponse = client.Indices.Create<DynamicResponse>(index,
    PostData.Serializable(new
    {
        settings = new
        {
            index = new
            {
                number_of_shards = 1,
                number_of_replicas = 1
            }
        },
        mappings = new
        {
            properties = new
            {
                gradDate = new { type = "date", format = "yyyy-MM-dd" }
            }
        }
    }));
```
{% include copy.html %}

每個方法的泛型類型參數會指定回應類型。`DynamicResponse` 可讓您依路徑從回應本文讀取值，例如 `createIndexResponse.Get<string>("index")`。`StringResponse` 會以字串形式傳回回應本文。

## 將單一文件編製索引

若要將文件編製索引，請先建立 `Student` 類別的執行個體：

```cs
var student = new Student { FirstName = "John", LastName = "Doe", Gpa = 3.89, GradDate = "2022-05-15" };
```
{% include copy.html %}

或者，您也可以使用匿名型別建立學生。在此情況下，屬性名稱即為欄位名稱：

```cs
var student = new { firstName = "John", lastName = "Doe", gpa = 3.89, gradDate = "2022-05-15" };
```
{% include copy.html %}

接著，使用 `Index` 方法將此學生上傳至 `students` 索引，ID 為 `1`。將 `Refresh` 設定為 `Refresh.True` 可讓文件立即可供搜尋：

```cs
var indexResponse = client.Index<DynamicResponse>(index, "1",
    PostData.Serializable(student),
    new IndexRequestParameters { Refresh = Refresh.True });
```
{% include copy.html %}

## 使用 Bulk API 將多個文件編製索引

若要將多個文件編製索引，請使用 Bulk API 將多項操作合併為一個請求：

```cs
var bulkBody = new object[]
{
    new { index = new { _index = index, _id = "2" } },
    new Student { FirstName = "Paulo", LastName = "Santos", Gpa = 3.93, GradDate = "2021-05-20" },
    new { index = new { _index = index, _id = "3" } },
    new Student { FirstName = "Shirley", LastName = "Rodriguez", Gpa = 3.91, GradDate = "2019-05-10" }
};
var bulkResponse = client.Bulk<StringResponse>(PostData.MultiJson(bulkBody),
    new BulkRequestParameters { Refresh = Refresh.True });
```
{% include copy.html %}

在接受本文的 API 中，您可以將請求本文以匿名物件、字串、位元組陣列或資料流的形式傳送。對於接受多行 JSON 的 API，您可以將本文以位元組清單或物件清單的形式傳送，如上述範例所示。`PostData` 類別提供靜態方法，可用上述所有形式傳送本文。

## 搜尋文件

若要建構 Query DSL 查詢，請在請求本文中使用匿名型別。下列查詢會搜尋所有學生：

```cs
var searchResponse = client.Search<StringResponse>(index,
    PostData.Serializable(new { query = new { match_all = new { } } }));
Console.WriteLine(searchResponse.Body);
```
{% include copy.html %}

下列範圍查詢會搜尋於 2019 年畢業的學生：

```cs
var searchResponse = client.Search<StringResponse>(index,
    PostData.Serializable(new
    {
        query = new
        {
            range = new
            {
                gradDate = new { gte = "2019-01-01", lte = "2019-12-31" }
            }
        }
    }));
Console.WriteLine(searchResponse.Body);
```
{% include copy.html %}

或者，您也可以使用字串來建構請求。使用字串時，您必須逸出 `"` 字元：

```cs
var searchResponse = client.Search<StringResponse>(index,
    @" {
    ""query"":
        {
            ""range"":
            {
                ""gradDate"":
                {
                    ""gte"": ""2019-01-01"",
                    ""lte"": ""2019-12-31""
                }
            }
        }
    }");
Console.WriteLine(searchResponse.Body);
```
{% include copy.html %}

## 將結果分頁

若要將結果分頁，請使用 `from` 和 `size` 參數。下列範例會依畢業日期排序學生，並每次擷取兩筆結果。第一個請求會傳回第一頁結果，第二個請求則會傳回下一頁：

```cs
var firstPageResponse = client.Search<StringResponse>(index,
    PostData.Serializable(new
    {
        from = 0,
        size = 2,
        sort = new[] { new { gradDate = "asc" } },
        query = new { match_all = new { } }
    }));
Console.WriteLine(firstPageResponse.Body);

var nextPageResponse = client.Search<StringResponse>(index,
    PostData.Serializable(new
    {
        from = 2,
        size = 2,
        sort = new[] { new { gradDate = "asc" } },
        query = new { match_all = new { } }
    }));
Console.WriteLine(nextPageResponse.Body);
```
{% include copy.html %}

`from` 和 `size` 參數適用於前幾頁的結果。若要對大量結果進行分頁，請搭配 `search_after` 使用時間點 (point in time)。如需詳細資訊，請參閱[將結果分頁]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/paginate/)。

## 更新文件

在 `doc` 欄位中傳送部分文件即可更新文件。只有部分文件中的欄位會被更新：

```cs
var updateResponse = client.Update<DynamicResponse>(index, "1",
    PostData.Serializable(new { doc = new { gpa = 3.92 } }));
```
{% include copy.html %}

## 刪除文件

使用下列程式碼刪除文件：

```cs
var deleteResponse = client.Delete<DynamicResponse>(index, "3",
    new DeleteRequestParameters { Refresh = Refresh.True });
```
{% include copy.html %}

## 刪除索引

使用下列程式碼刪除索引：

```cs
var deleteIndexResponse = client.Indices.Delete<DynamicResponse>(index);
```
{% include copy.html %}

## 以非同步方式使用 OpenSearch.Net 方法

對於需要非同步程式碼的應用程式，OpenSearch.Net 中的所有方法呼叫都有對應的非同步版本：

```cs
// synchronous method
var response = client.Index<StringResponse>(index, "1",
                                PostData.Serializable(student));

// asynchronous method
var asyncResponse = await client.IndexAsync<StringResponse>(index, "1",
                                    PostData.Serializable(student));
```
{% include copy.html %}

## 處理例外狀況

根據預設，當操作失敗時，OpenSearch.Net 不會擲回例外狀況。例如，下列查詢會在不存在的索引中搜尋文件：

```cs
var searchResponse = client.Search<StringResponse>("students1",
    @" {
    ""query"":
        {
            ""match"":
            {
                ""lastName"":
                {
                    ""query"": ""Santos""
                }
            }
        }
    }");

Console.WriteLine(searchResponse.Body);
```
{% include copy.html %}

回應包含 404 錯誤狀態碼，但不會擲回例外狀況。您可以在 `status` 欄位中查看狀態碼：

```json
{
  "error" : {
    "root_cause" : [
      {
        "type" : "index_not_found_exception",
        "reason" : "no such index [students1]",
        "index" : "students1",
        "resource.id" : "students1",
        "resource.type" : "index_or_alias",
        "index_uuid" : "_na_"
      }
    ],
    "type" : "index_not_found_exception",
    "reason" : "no such index [students1]",
    "index" : "students1",
    "resource.id" : "students1",
    "resource.type" : "index_or_alias",
    "index_uuid" : "_na_"
  },
  "status" : 404
}
```

若要將 OpenSearch.Net 設定為擲回例外狀況，請在 `ConnectionConfiguration` 上開啟 `ThrowExceptions()` 設定：

```cs
var uri = new Uri("http://localhost:9200");
var connectionPool = new SingleNodeConnectionPool(uri);
var settings = new ConnectionConfiguration(connectionPool)
                        .PrettyJson().ThrowExceptions();
var client = new OpenSearchLowLevelClient(settings);
```
{% include copy.html %}

若要判斷請求是否成功，請使用回應物件的下列屬性：

```cs
Console.WriteLine("Success: " + searchResponse.Success);
Console.WriteLine("SuccessOrKnownError: " + searchResponse.SuccessOrKnownError);
Console.WriteLine("Original Exception: " + searchResponse.OriginalException);
```
{% include copy.html %}

- 如果回應碼位於 2xx 範圍內，或回應碼為此請求的預期值之一，`Success` 會傳回 true。
- 如果回應成功，或回應碼位於 400–501 或 505–599 範圍內，`SuccessOrKnownError` 會傳回 true。如果 SuccessOrKnownError 為 true，則不會重試該請求。
- `OriginalException` 會保存失敗回應的原始例外狀況。

## 範例程式

此範例程式整合了前面幾節的程式碼。它連線至已啟用 Security 外掛程式的叢集。若要連線至未啟用 Security 外掛程式的叢集，請變更標有 `// Without security` 註解的程式碼行。在執行範例程式之前，請確認您的專案中已定義 `Student` 類別。為了列印傳回的文件，範例程式使用 `System.Text.Json` 將每個文件的 `_source` 反序列化為 `Student`。

此範例程式僅供測試之用。它在程式碼中指定認證資訊並停用憑證驗證，以便連線至使用自簽憑證的叢集。在正式環境中，請從安全的位置載入認證資訊，並驗證叢集的憑證。
{: .warning}

下列範例程式會建立用戶端、建立索引、逐一及大量將文件編製索引、搜尋文件、更新文件、刪除文件，然後刪除索引：

```cs
using System.Text.Json;
using OpenSearch.Net;

namespace NetClientProgram;

internal class Program
{
    public static void Main(string[] args)
    {
        var config = new ConnectionConfiguration(new Uri("https://localhost:9200")); // Without security, use http://localhost:9200
        config.BasicAuthentication("admin", "<custom-admin-password>"); // Without security, remove this line
        config.ServerCertificateValidationCallback(CertificateValidations.AllowAll); // Without security, remove this line
        var client = new OpenSearchLowLevelClient(config);

        // Create the index
        var index = "students";
        Console.WriteLine("Creating index......");
        var createIndexResponse = client.Indices.Create<DynamicResponse>(index,
            PostData.Serializable(new
            {
                settings = new
                {
                    index = new
                    {
                        number_of_shards = 1,
                        number_of_replicas = 1
                    }
                },
                mappings = new
                {
                    properties = new
                    {
                        gradDate = new { type = "date", format = "yyyy-MM-dd" }
                    }
                }
            }));
        Console.WriteLine("Index created: " + createIndexResponse.Get<string>("index"));

        // Index a document
        Console.WriteLine("\nIndexing one student......");
        var student = new Student { FirstName = "John", LastName = "Doe", Gpa = 3.89, GradDate = "2022-05-15" };
        var indexResponse = client.Index<DynamicResponse>(index, "1",
            PostData.Serializable(student),
            new IndexRequestParameters { Refresh = Refresh.True });
        Console.WriteLine($"Result: {indexResponse.Get<string>("result")}, id: {indexResponse.Get<string>("_id")}, version: {indexResponse.Get<long>("_version")}");

        // Bulk index documents
        Console.WriteLine("\nIndexing many students......");
        var bulkBody = new object[]
        {
            new { index = new { _index = index, _id = "2" } },
            new Student { FirstName = "Paulo", LastName = "Santos", Gpa = 3.93, GradDate = "2021-05-20" },
            new { index = new { _index = index, _id = "3" } },
            new Student { FirstName = "Shirley", LastName = "Rodriguez", Gpa = 3.91, GradDate = "2019-05-10" }
        };
        var bulkResponse = client.Bulk<StringResponse>(PostData.MultiJson(bulkBody),
            new BulkRequestParameters { Refresh = Refresh.True });
        using (var bulkJson = JsonDocument.Parse(bulkResponse.Body))
        {
            Console.WriteLine("Errors: " + bulkJson.RootElement.GetProperty("errors").GetRawText());
            foreach (var item in bulkJson.RootElement.GetProperty("items").EnumerateArray())
            {
                var operation = item.GetProperty("index");
                Console.WriteLine($"  {operation.GetProperty("result")} id: {operation.GetProperty("_id")}");
            }
        }

        // Search for all students
        Console.WriteLine("\nSearching for all students......");
        var searchResponse = client.Search<StringResponse>(index,
            PostData.Serializable(new
            {
                from = 0,
                size = 2,
                sort = new[] { new { gradDate = "asc" } },
                query = new { match_all = new { } }
            }));
        PrintTotal(searchResponse);
        Console.WriteLine("Page 1:");
        PrintStudents(searchResponse);

        var nextPageResponse = client.Search<StringResponse>(index,
            PostData.Serializable(new
            {
                from = 2,
                size = 2,
                sort = new[] { new { gradDate = "asc" } },
                query = new { match_all = new { } }
            }));
        Console.WriteLine("Page 2:");
        PrintStudents(nextPageResponse);

        // Search for students who graduated in 2019
        Console.WriteLine("\nSearching for students who graduated in 2019......");
        var searchResponse2 = client.Search<StringResponse>(index,
            PostData.Serializable(new
            {
                query = new
                {
                    range = new
                    {
                        gradDate = new { gte = "2019-01-01", lte = "2019-12-31" }
                    }
                }
            }));
        PrintTotal(searchResponse2);
        PrintStudents(searchResponse2);

        // Update a document
        Console.WriteLine("\nUpdating a student's GPA......");
        var updateResponse = client.Update<DynamicResponse>(index, "1",
            PostData.Serializable(new { doc = new { gpa = 3.92 } }));
        Console.WriteLine($"Result: {updateResponse.Get<string>("result")}, version: {updateResponse.Get<long>("_version")}");

        // Get the updated document
        var getResponse = client.Get<StringResponse>(index, "1");
        using (var getJson = JsonDocument.Parse(getResponse.Body))
        {
            var updatedStudent = getJson.RootElement.GetProperty("_source").Deserialize<Student>(JsonOptions);
            Console.WriteLine("Updated document: " + updatedStudent);
        }

        // Delete a document
        Console.WriteLine("\nDeleting a student......");
        var deleteResponse = client.Delete<DynamicResponse>(index, "3",
            new DeleteRequestParameters { Refresh = Refresh.True });
        Console.WriteLine("Result: " + deleteResponse.Get<string>("result"));

        // Delete the index
        Console.WriteLine("\nDeleting the index......");
        var deleteIndexResponse = client.Indices.Delete<StringResponse>(index);
        using (var deleteIndexJson = JsonDocument.Parse(deleteIndexResponse.Body))
        {
            Console.WriteLine("Acknowledged: " + deleteIndexJson.RootElement.GetProperty("acknowledged").GetRawText());
        }
    }

    // Deserializes camelCase JSON field names into Student properties
    private static readonly JsonSerializerOptions JsonOptions = new(JsonSerializerDefaults.Web);

    // Prints the total number of hits
    private static void PrintTotal(StringResponse searchResponse)
    {
        using var json = JsonDocument.Parse(searchResponse.Body);
        var hits = json.RootElement.GetProperty("hits");
        Console.WriteLine("Total hits: " + hits.GetProperty("total").GetProperty("value"));
    }

    // Prints the student in each hit
    private static void PrintStudents(StringResponse searchResponse)
    {
        using var json = JsonDocument.Parse(searchResponse.Body);
        var hits = json.RootElement.GetProperty("hits");
        foreach (var hit in hits.GetProperty("hits").EnumerateArray())
        {
            var student = hit.GetProperty("_source").Deserialize<Student>(JsonOptions);
            Console.WriteLine("  " + student);
        }
    }
}
```
{% include copy.html %}

範例程式會產生下列輸出：

```text
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

- 如需更多使用用戶端的範例，請參閱 [`opensearch-net` 使用者指南](https://github.com/opensearch-project/opensearch-net/blob/main/USER_GUIDE.md)。
- 如需特定工作的指南，例如大量編製索引和搜尋，請參閱 [`opensearch-net` 指南](https://github.com/opensearch-project/opensearch-net/tree/main/guides)。
- 如需完整的範例應用程式，請參閱 [`opensearch-net` 範例](https://github.com/opensearch-project/opensearch-net/tree/main/samples)。
