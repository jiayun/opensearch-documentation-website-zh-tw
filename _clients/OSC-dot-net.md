---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "高階 .NET 用戶端入門"
nav_order: 10
has_children: false
parent: .NET clients
---

# 高階 .NET 用戶端（OpenSearch.Client）入門

OpenSearch.Client 是高階 .NET 用戶端。它提供強型別的請求與回應，以及 Query DSL。它提供可自動剖析及序列化／反序列化請求與回應的模型，讓您無須建構原始 JSON 請求或剖析原始 JSON 回應。OpenSearch.Client 也提供 OpenSearch.Net 低階用戶端，供您在需要時使用。如需此用戶端的完整 API 文件，請參閱 [OpenSearch.Client API 文件](https://opensearch-project.github.io/opensearch-net/api/OpenSearch.Client.html)。


本入門指南說明如何連線至 OpenSearch、將文件編製索引及執行查詢。如需用戶端的原始碼，請參閱 [`opensearch-net` 儲存庫](https://github.com/opensearch-project/opensearch-net)。

## 安裝 OpenSearch.Client

若要安裝 OpenSearch.Client，請下載 [OpenSearch.Client NuGet 套件](https://www.nuget.org/packages/OpenSearch.Client/)，並在您選擇的 IDE 中將其新增至專案。在 Microsoft Visual Studio 中，請依照下列步驟操作： 
- 在 **Solution Explorer** 面板中，以滑鼠右鍵按一下您的方案或專案，然後選取 **Manage NuGet Packages for Solution**。
- 搜尋 OpenSearch.Client NuGet 套件，然後選取 **Install**。

或者，使用 .NET CLI 將 OpenSearch.Client 新增至您的專案：

```bash
dotnet add package OpenSearch.Client --version 2.2.0
```
{% include copy.html %}

您也可以將 OpenSearch.Client 新增至您的 .csproj 檔案：

```xml
<Project>
  ...
  <ItemGroup>
    <PackageReference Include="OpenSearch.Client" Version="2.2.0" />
  </ItemGroup>
</Project>
```
{% include copy.html %}

OpenSearch.Client 相依於 OpenSearch.Net，因此安裝 OpenSearch.Client 時也會安裝低階用戶端。如需支援的 OpenSearch 版本與目標架構的相關資訊，請參閱[相容性]({{site.url}}{{site.baseurl}}/clients/dot-net/#compatibility)。

## 範例資料

本頁的範例使用下列 `Student` 類別代表一名學生，相當於索引中的一份文件。`ToString` 方法會將 `Student` 格式化，以便輸出至主控台：

```cs
using System.Globalization;

public class Student
{
    public string FirstName { get; set; } = string.Empty;
    public string LastName { get; set; } = string.Empty;
    public double Gpa { get; set; }
    public string GradDate { get; set; } = string.Empty;

    public override string ToString() =>
        string.Format(CultureInfo.InvariantCulture,
            "{% raw %}Student{{firstName='{0}', lastName='{1}', gpa={2}, gradDate={3}}}{% endraw %}",
            FirstName, LastName, Gpa, GradDate);
}
```
{% include copy.html %}

依預設，OpenSearch.Client 使用駝峰式大小寫將屬性名稱轉換為欄位名稱，因此 `Student` 會被編製索引為包含 `firstName`、`lastName`、`gpa` 和 `gradDate` 欄位的文件。
{: .note}

## 連線至 OpenSearch

建立 OpenSearchClient 物件時，使用預設建構函式即可連線至預設的 OpenSearch 主機（`http://localhost:9200`）。 

```cs
var client  = new OpenSearchClient();
```
{% include copy.html %}

若要透過位址已知的單一節點連線至您的 OpenSearch 叢集，請在建立 OpenSearch.Client 執行個體時指定此位址：

```cs
var nodeAddress = new Uri("http://myserver:9200");
var client = new OpenSearchClient(nodeAddress);
```
{% include copy.html %}

您也可以透過多個節點連線至 OpenSearch。使用節點集區連線至您的 OpenSearch 叢集，可提供負載平衡及叢集容錯移轉支援等優點。若要使用多個節點連線至您的 OpenSearch 叢集，請指定這些節點的位址，並為 OpenSearch.Client 執行個體建立 `ConnectionSettings` 物件：

```cs
var nodes = new Uri[]
{
    new Uri("http://myserver1:9200"),
    new Uri("http://myserver2:9200"),
    new Uri("http://myserver3:9200")
};

var pool = new StaticConnectionPool(nodes);
var settings = new ConnectionSettings(pool);
var client = new OpenSearchClient(settings);
```
{% include copy.html %}

### 使用 ConnectionSettings

`ConnectionConfiguration` 用於將組態選項傳遞至低階 OpenSearch.Net 用戶端。`ConnectionSettings` 繼承自 `ConnectionConfiguration`，並為高階用戶端提供額外的組態選項，例如請求的預設索引名稱，以及屬性名稱與欄位名稱之間的對應。`ConnectionSettings` 是 OpenSearch.Client 套件的一部分。

若要設定節點位址，以及未指定索引名稱之請求的預設索引名稱，請建立 `ConnectionSettings` 物件：

```cs
var node = new Uri("http://myserver:9200");
var config = new ConnectionSettings(node).DefaultIndex("students");
var client = new OpenSearchClient(config);
```
{% include copy.html %}

## 建立索引

下列範例會建立具有一個主要分片和一個副本的索引。它會明確將 `gradDate` 欄位對應為採用 `yyyy-MM-dd` 格式的 `date`。當您將文件編製索引時，OpenSearch 會動態對應其他文件欄位：

```cs
var index = "students";
var createIndexResponse = client.Indices.Create(index, c => c
    .Settings(s => s
        .NumberOfShards(1)
        .NumberOfReplicas(1))
    .Map<Student>(m => m
        .Properties(p => p
            .Date(d => d.Name(f => f.GradDate).Format("yyyy-MM-dd")))));
```
{% include copy.html %}

## 將單一文件編製索引

建立一個 `Student` 執行個體：

```cs
var student = new Student { FirstName = "John", LastName = "Doe", Gpa = 3.89, GradDate = "2022-05-15" };
```
{% include copy.html %}

若要將單一文件編製索引，您可以使用流暢式 Lambda 語法或物件初始設定式語法。下列範例會將 `Refresh` 設定為 `Refresh.True`，讓文件可立即供搜尋使用。

使用流暢式 Lambda 語法，將此 `Student` 以 ID `1` 編製索引至 `students` 索引：

```cs
var indexResponse = client.Index(student, i => i
    .Index(index)
    .Id("1")
    .Refresh(Refresh.True));
```
{% include copy.html %}

使用物件初始設定式語法，將此 `Student` 以 ID `1` 編製索引至 `students` 索引：

```cs
var indexResponse = client.Index(new IndexRequest<Student>(student, index, "1")
{
    Refresh = Refresh.True
});
```
{% include copy.html %}

## 將多份文件編製索引

使用 Bulk API，在單一請求中將多份文件編製索引：

```cs
var bulkResponse = client.Bulk(b => b
    .Index(index)
    .Refresh(Refresh.True)
    .Index<Student>(op => op
        .Id("2")
        .Document(new Student { FirstName = "Paulo", LastName = "Santos", Gpa = 3.93, GradDate = "2021-05-20" }))
    .Index<Student>(op => op
        .Id("3")
        .Document(new Student { FirstName = "Shirley", LastName = "Rodriguez", Gpa = 3.91, GradDate = "2019-05-10" })));
```
{% include copy.html %}

## 搜尋文件

使用下列程式碼搜尋索引中的所有文件：

```cs
var searchResponse = client.Search<Student>(s => s
    .Index(index)
    .Query(q => q.MatchAll()));
foreach (var doc in searchResponse.Documents)
{
    Console.WriteLine(doc);
}
```
{% include copy.html %}

`searchResponse.Documents` 中的每個項目都是 `Student` 物件，其欄位可透過屬性存取。若還要取得每份文件的 ID，請逐一走訪 `searchResponse.Hits`。每筆命中結果的 `Id` 屬性包含文件 ID，而 `Source` 屬性包含 `Student` 物件：

```cs
foreach (var hit in searchResponse.Hits)
{
    Console.WriteLine($"ID: {hit.Id}, name: {hit.Source.FirstName} {hit.Source.LastName}, GPA: {hit.Source.Gpa}, graduation date: {hit.Source.GradDate}");
}
```
{% include copy.html %}

若要搜尋在 2019 年畢業的學生，請使用範圍查詢。下列 Query DSL 範圍查詢會搜尋 `gradDate` 落在 2019 年內的文件：

```json
GET students/_search
{
  "query": {
    "range": {
      "gradDate": {
        "gte": "2019-01-01",
        "lte": "2019-12-31"
      }
    }
  }
}
```

在 OpenSearch.Client 中，此查詢如下所示：

```cs
var searchResponse = client.Search<Student>(s => s
    .Index(index)
    .Query(q => q
        .DateRange(r => r
            .Field(f => f.GradDate)
            .GreaterThanOrEquals("2019-01-01")
            .LessThanOrEquals("2019-12-31"))));
```
{% include copy.html %}

回應包含一份文件，對應至正確的學生：

```text
Student{firstName='Shirley', lastName='Rodriguez', gpa=3.91, gradDate=2019-05-10}
```

## 將結果分頁

若要將結果分頁，請使用 `from` 和 `size` 參數。下列範例依畢業日期排序學生，並每次擷取兩筆結果。第一個請求傳回第一頁結果，第二個請求傳回下一頁：

```cs
var firstPageResponse = client.Search<Student>(s => s
    .Index(index)
    .Sort(so => so.Ascending(f => f.GradDate))
    .From(0)
    .Size(2));
foreach (var doc in firstPageResponse.Documents)
{
    Console.WriteLine(doc);
}

var nextPageResponse = client.Search<Student>(s => s
    .Index(index)
    .Sort(so => so.Ascending(f => f.GradDate))
    .From(2)
    .Size(2));
foreach (var doc in nextPageResponse.Documents)
{
    Console.WriteLine(doc);
}
```
{% include copy.html %}

`from` 和 `size` 參數適合用於前幾頁結果。若要對大量結果進行分頁，請搭配 `search_after` 使用時間點。詳細資訊請參閱[將結果分頁]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/paginate/)。

## 更新文件

使用部分文件來更新文件。只有部分文件中的欄位會更新：

```cs
var updateResponse = client.Update<Student, object>("1", u => u
    .Index(index)
    .Doc(new { gpa = 3.92 }));
```
{% include copy.html %}

## 刪除文件

使用下列程式碼刪除文件：

```cs
var deleteResponse = client.Delete<Student>("3", d => d
    .Index(index)
    .Refresh(Refresh.True));
```
{% include copy.html %}

## 刪除索引

使用下列程式碼刪除索引：

```cs
var deleteIndexResponse = client.Indices.Delete(index);
```
{% include copy.html %}

## 以非同步方式使用 OpenSearch.Client 方法

對於需要非同步程式碼的應用程式，OpenSearch.Client 中的所有方法呼叫都有對應的非同步版本：

```cs
// synchronous method
var response = client.Index(student, i => i.Index(index).Id("1"));

// asynchronous method
var asyncResponse = await client.IndexAsync(student, i => i.Index(index).Id("1"));
```
{% include copy.html %}

## 改用低階 OpenSearch.Net 用戶端

OpenSearch.Client 透過 `LowLevel` 屬性提供低階 OpenSearch.Net 用戶端的存取。您可以使用低階用戶端呼叫 OpenSearch.Client 未提供對應方法的 API，或自行建構請求本文，而不使用 OpenSearch.Client 查詢方法。下列範例將範圍查詢以匿名物件的形式傳送，並將回應反序列化為 `SearchResponse<Student>`：

```cs
var lowLevelClient = client.LowLevel;

var searchResponseLow = lowLevelClient.Search<SearchResponse<Student>>(index,
    PostData.Serializable(
        new
        {
            query = new
            {
                range = new
                {
                    gradDate = new
                    {
                        gte = "2019-01-01",
                        lte = "2019-12-31"
                    }
                }
            }
        }));

if (searchResponseLow.IsValid)
{
    foreach (var doc in searchResponseLow.Documents)
    {
        Console.WriteLine(doc);
    }
}
```
{% include copy.html %}

## 範例程式

此範例程式整合了前述各節的程式碼。它會連線至已啟用 Security 外掛程式的叢集。若要連線至未使用 Security 外掛程式的叢集，請變更以 `// Without security` 註解標示的程式碼行。執行範例程式之前，請確認您已在專案中定義 `Student` 類別。

此範例程式僅供測試使用。它在程式碼中指定認證資訊，並停用憑證驗證，以便連線至使用自我簽署憑證的叢集。在正式環境中，請從安全的位置載入認證資訊，並驗證叢集的憑證。
{: .warning}

下列範例程式會建立用戶端、建立索引、逐一及大量將文件編製索引、搜尋文件、更新文件、刪除文件，最後刪除索引：

```cs
using OpenSearch.Client;
using OpenSearch.Net;

namespace NetClientProgram;

internal class Program
{
    public static void Main(string[] args)
    {
        var settings = new ConnectionSettings(new Uri("https://localhost:9200")); // Without security, use http://localhost:9200
        settings.BasicAuthentication("admin", "<custom-admin-password>"); // Without security, remove this line
        settings.ServerCertificateValidationCallback(CertificateValidations.AllowAll); // Without security, remove this line
        var client = new OpenSearchClient(settings);

        // Create the index
        var index = "students";
        Console.WriteLine("Creating index......");
        var createIndexResponse = client.Indices.Create(index, c => c
            .Settings(s => s
                .NumberOfShards(1)
                .NumberOfReplicas(1))
            .Map<Student>(m => m
                .Properties(p => p
                    .Date(d => d.Name(f => f.GradDate).Format("yyyy-MM-dd")))));
        Console.WriteLine("Index created: " + createIndexResponse.Index);

        // Index a document
        Console.WriteLine("\nIndexing one student......");
        var student = new Student { FirstName = "John", LastName = "Doe", Gpa = 3.89, GradDate = "2022-05-15" };
        var indexResponse = client.Index(student, i => i
            .Index(index)
            .Id("1")
            .Refresh(Refresh.True));
        Console.WriteLine($"Result: {indexResponse.Result.ToString().ToLowerInvariant()}, id: {indexResponse.Id}, version: {indexResponse.Version}");

        // Bulk index documents
        Console.WriteLine("\nIndexing many students......");
        var bulkResponse = client.Bulk(b => b
            .Index(index)
            .Refresh(Refresh.True)
            .Index<Student>(op => op
                .Id("2")
                .Document(new Student { FirstName = "Paulo", LastName = "Santos", Gpa = 3.93, GradDate = "2021-05-20" }))
            .Index<Student>(op => op
                .Id("3")
                .Document(new Student { FirstName = "Shirley", LastName = "Rodriguez", Gpa = 3.91, GradDate = "2019-05-10" })));
        Console.WriteLine("Errors: " + bulkResponse.Errors.ToString().ToLowerInvariant());
        foreach (var item in bulkResponse.Items)
        {
            Console.WriteLine($"  {item.Result} id: {item.Id}");
        }

        // Search for all students
        Console.WriteLine("\nSearching for all students......");
        var searchResponse = client.Search<Student>(s => s
            .Index(index)
            .Sort(so => so.Ascending(f => f.GradDate))
            .From(0)
            .Size(2));
        Console.WriteLine("Total hits: " + searchResponse.Total);
        Console.WriteLine("Page 1:");
        foreach (var doc in searchResponse.Documents)
        {
            Console.WriteLine("  " + doc);
        }

        var nextPageResponse = client.Search<Student>(s => s
            .Index(index)
            .Sort(so => so.Ascending(f => f.GradDate))
            .From(2)
            .Size(2));
        Console.WriteLine("Page 2:");
        foreach (var doc in nextPageResponse.Documents)
        {
            Console.WriteLine("  " + doc);
        }

        // Search for students who graduated in 2019
        Console.WriteLine("\nSearching for students who graduated in 2019......");
        var searchResponse2 = client.Search<Student>(s => s
            .Index(index)
            .Query(q => q
                .DateRange(r => r
                    .Field(f => f.GradDate)
                    .GreaterThanOrEquals("2019-01-01")
                    .LessThanOrEquals("2019-12-31"))));
        Console.WriteLine("Total hits: " + searchResponse2.Total);
        foreach (var doc in searchResponse2.Documents)
        {
            Console.WriteLine("  " + doc);
        }

        // Update a document
        Console.WriteLine("\nUpdating a student's GPA......");
        var updateResponse = client.Update<Student, object>("1", u => u
            .Index(index)
            .Doc(new { gpa = 3.92 }));
        Console.WriteLine($"Result: {updateResponse.Result.ToString().ToLowerInvariant()}, version: {updateResponse.Version}");

        // Get the updated document
        var getResponse = client.Get<Student>("1", g => g.Index(index));
        Console.WriteLine("Updated document: " + getResponse.Source);

        // Delete a document
        Console.WriteLine("\nDeleting a student......");
        var deleteResponse = client.Delete<Student>("3", d => d
            .Index(index)
            .Refresh(Refresh.True));
        Console.WriteLine("Result: " + deleteResponse.Result.ToString().ToLowerInvariant());

        // Delete the index
        Console.WriteLine("\nDeleting the index......");
        var deleteIndexResponse = client.Indices.Delete(index);
        Console.WriteLine("Acknowledged: " + deleteIndexResponse.Acknowledged.ToString().ToLowerInvariant());
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
- 如需特定工作的指南，例如大量編製索引與搜尋，請參閱 [`opensearch-net` 指南](https://github.com/opensearch-project/opensearch-net/tree/main/guides)。
- 如需完整的範例應用程式，請參閱 [`opensearch-net` 範例](https://github.com/opensearch-project/opensearch-net/tree/main/samples)。
