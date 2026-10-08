---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "高階 .NET 用戶端的更多進階功能"
nav_order: 12
has_children: false
parent: .NET clients
---

# 高階 .NET 用戶端 (OpenSearch.Client) 的更多進階功能

下列範例說明 OpenSearch.Client 的更多進階功能。簡單範例請參閱[入門指南]({{site.url}}{{site.baseurl}}/clients/OSC-dot-net/)。此範例使用下列 `Student` 類別，與[入門指南]({{site.url}}{{site.baseurl}}/clients/OSC-dot-net/)中使用的類別相同。OpenSearch.Client 會將其屬性名稱轉換為 `firstName`、`lastName`、`gpa` 和 `gradDate` 欄位名稱。`ToString` 方法會將 `Student` 格式化為主控台輸出：

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

## 對應

OpenSearch 使用動態對應來推斷已編製索引文件的欄位類型。不過，若要更充分控制文件的結構描述，您可以將明確對應傳遞給 OpenSearch。您可以在這個對應中為文件的部分或所有欄位定義資料類型。

同樣地，OpenSearch.Client 使用自動對應，根據類別屬性的類型來推斷欄位資料類型。若要使用自動對應，請使用 AutoMap 的預設建構函式建立 `students` 索引：

```cs
var createResponse = await osClient.Indices.CreateAsync("students",
    c => c.Map(m => m.AutoMap<Student>()));
```
{% include copy.html %}

如果您使用自動對應，`Gpa` 會對應為 double，而 `FirstName`、`LastName` 和 `GradDate` 是字串屬性，因此會對應為帶有 keyword 子欄位的 text。若要在 `GradDate` 上搜尋日期範圍，請將它對應為 `yyyy-MM-dd` 格式的 `date`。如果您想搜尋 `FirstName` 和 `LastName`，並且只允許區分大小寫的完整符合，可以將這些欄位僅對應為 keyword 來停用分析。在 Query DSL 中，您可以使用下列查詢來完成：

```json
PUT students
{
  "mappings" : {
    "properties" : {
      "firstName" : {
        "type" : "keyword"
      },
      "lastName" : {
        "type" : "keyword"
      },
      "gradDate" : {
        "type" : "date",
        "format" : "yyyy-MM-dd"
      }
    }
  }
}
```

在 OpenSearch.Client 中，您可以使用流暢的 lambda 語法來對應這些欄位：

```cs
var createResponse = await osClient.Indices.CreateAsync(index,
                c => c.Map(m => m.AutoMap<Student>()
                .Properties<Student>(p => p
                .Keyword(k => k.Name(f => f.FirstName))
                .Keyword(k => k.Name(f => f.LastName))
                .Date(d => d.Name(f => f.GradDate).Format("yyyy-MM-dd")))));
```
{% include copy.html %}

## 設定

除了對應之外，您還可以在建立索引時指定設定，例如主要分片和副本分片的數量。下列查詢將主要分片數量設為 1，副本分片數量設為 2：

```json
PUT students
{
  "mappings" : {
    "properties" : {
      "firstName" : {
        "type" : "keyword"
      },
      "lastName" : {
        "type" : "keyword"
      },
      "gradDate" : {
        "type" : "date",
        "format" : "yyyy-MM-dd"
      }
    }
  }, 
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 2
  }
}
```

在 OpenSearch.Client 中，與前述查詢等效的寫法如下：

```cs
var createResponse = await osClient.Indices.CreateAsync(index,
                            c => c.Map(m => m.AutoMap<Student>()
                            .Properties<Student>(p => p
                            .Keyword(k => k.Name(f => f.FirstName))
                            .Keyword(k => k.Name(f => f.LastName))
                            .Date(d => d.Name(f => f.GradDate).Format("yyyy-MM-dd"))))
                            .Settings(s => s.NumberOfShards(1).NumberOfReplicas(2)));
```
{% include copy.html %}

## 使用 Bulk API 編製多份文件的索引

除了使用 `Index` 和 `IndexDocument` 為單一文件編製索引，以及使用 `IndexMany` 為多份文件編製索引之外，您還可以使用 `Bulk` 或 `BulkAll` 來取得更充分的文件索引控制。逐一為文件編製索引效率不佳，因為每份送出的文件都會建立一個 HTTP 請求。BulkAll 協助程式讓您不必自行處理重試、分塊或退避請求功能。它會在請求失敗時自動重試、在伺服器停機時退避，並控制一個 HTTP 請求中送出多少份文件。

在下列範例中，`BulkAll` 設定了索引名稱、退避重試次數和退避時間。此外，最大平行度設定會控制包含資料的平行 HTTP 請求數量。最後，size 參數指定一個 HTTP 請求中送出多少份文件。

我們建議在正式環境中將 size 設為 100–1000 份文件。
{: .tip}

`BulkAll` 接受一個資料串流，並回傳一個 Observable，您可以用它來觀察背景作業。

```cs
var bulkAll = osClient.BulkAll(ReadData(), r => r
            .Index(index)
            .BackOffRetries(2)
            .BackOffTime("30s")
            .MaxDegreeOfParallelism(4)
            .Size(100));
```
{% include copy.html %}

## 使用布林值查詢搜尋

OpenSearch.Client 公開完整的 OpenSearch 查詢功能。除了使用 match 查詢的簡單搜尋之外，您還可以建立更複雜的布林值查詢，依 `gradDate` 範圍篩選，搜尋 2022 年畢業的學生，並依姓氏排序。在下列範例中，搜尋限制為 10 份文件，並使用 scroll API 控制結果的分頁。

```cs
var gradResponse = await osClient.SearchAsync<Student>(s => s
                        .Index(index)
                        .From(0)
                        .Size(10)
                        .Scroll("1m")
                        .Query(q => q
                        .Bool(b => b
                        .Filter(f => f
                        .DateRange(r => r
                            .Field(fld => fld.GradDate)
                            .GreaterThanOrEquals("2022-01-01")
                            .LessThanOrEquals("2022-12-31")))))
                        .Sort(srt => srt.Ascending(f => f.LastName)));
```
{% include copy.html %}

回應包含 Documents 屬性，其中含有來自 OpenSearch 的符合文件。資料是以 Student 類型的已還原序列化 JSON 物件形式呈現，因此您可以以強型別方式存取其屬性。所有序列化與還原序列化都由 OpenSearch.Client 處理。

## 彙總

OpenSearch.Client 包含完整的 OpenSearch 查詢功能，包括彙總。除了將搜尋結果分組到桶 (bucket) 中（例如依 GPA 範圍將學生分組）之外，您還可以計算總和或平均值等指標。下列查詢計算索引中所有學生的平均 GPA。

將 Size 設為 0 表示 OpenSearch 只會回傳彙總結果，而不會回傳實際文件。
{: .tip}

```cs
var aggResponse = await osClient.SearchAsync<Student>(s => s
                                .Index(index)
                                .Size(0)
                                .Aggregations(a => a
                                .Average("average gpa", 
                                            avg => avg.Field(fld => fld.Gpa))));
```
{% include copy.html %}

## 建立索引與將資料編製索引的範例程式

本節的範例程式會從您執行該程式所在目錄中的 `students.csv` 檔案讀取學生記錄。請以每行一筆學生記錄的方式建立該檔案，格式為 `FirstName,LastName,Gpa,GradDate`，並以 `yyyy-MM-dd` 格式指定畢業日期。請勿包含標題列。例如：

```text
John,Doe,3.89,2022-05-15
Wei,Zhang,3.65,2022-05-15
Zhang,Li,3.72,2022-06-10
```
{% include copy.html %}

下列程式會刪除 `students` 索引 (若存在)、建立該索引、從檔案讀取學生記錄，並將其編製索引至 OpenSearch：

```cs
using System.Globalization;
using OpenSearch.Client;

namespace NetClientProgram;

internal class Program
{
    private const string index = "students";

    public static IOpenSearchClient osClient = new OpenSearchClient();

    public static async Task Main(string[] args)
    {
        // Delete the "students" index if it exists so that the index is created with the following mappings
        var existResponse = await osClient.Indices.ExistsAsync(index);

        if (existResponse.Exists)
        {
            await osClient.Indices.DeleteAsync(index);
        }

        // Create an index "students"
        // Map FirstName and LastName as keyword and GradDate as date
        var createResponse = await osClient.Indices.CreateAsync(index,
            c => c.Map(m => m.AutoMap<Student>()
            .Properties<Student>(p => p
            .Keyword(k => k.Name(f => f.FirstName))
            .Keyword(k => k.Name(f => f.LastName))
            .Date(d => d.Name(f => f.GradDate).Format("yyyy-MM-dd"))))
            .Settings(s => s.NumberOfShards(1).NumberOfReplicas(1)));

        if (!createResponse.IsValid || !createResponse.Acknowledged)
        {
            throw new Exception("Create response is invalid.");
        }

        // Take a stream of data and send it to OpenSearch
        var bulkAll = osClient.BulkAll(ReadData(), r => r
        .Index(index)
        .BackOffRetries(2)
        .BackOffTime("20s")
        .MaxDegreeOfParallelism(4)
        .Size(10)
        .RefreshOnCompleted());

        // Wait until the data upload is complete.
        // FromMinutes specifies a timeout.
        // r is a response object that is returned as the data is indexed.
        bulkAll.Wait(TimeSpan.FromMinutes(10), r =>
            Console.WriteLine("Data chunk indexed"));
    }

    // Reads student data in the form "FirstName,LastName,Gpa,GradDate"
    public static IEnumerable<Student> ReadData()
    {
        foreach (var line in File.ReadLines("students.csv"))
        {
            var fields = line.Split(',');
            yield return new Student
            {
                FirstName = fields[0],
                LastName = fields[1],
                Gpa = double.Parse(fields[2], CultureInfo.InvariantCulture),
                GradDate = fields[3]
            };
        }
    }
}
```
{% include copy.html %}

## 搜尋的範例程式

下列程式會依姓名與畢業日期搜尋學生、計算平均 GPA，然後刪除該索引。

```cs
using OpenSearch.Client;

namespace NetClientProgram;

internal class Program
{
    private const string index = "students";

    public static IOpenSearchClient osClient = new OpenSearchClient();

    public static async Task Main(string[] args)
    {
        await SearchByName();

        await SearchByGradDate();

        await CalculateAverageGpa();

        // Delete the index
        Console.WriteLine("Deleting the index......");
        var deleteIndexResponse = await osClient.Indices.DeleteAsync(index);
        Console.WriteLine("Acknowledged: " + deleteIndexResponse.Acknowledged.ToString().ToLowerInvariant());
    }

    private static async Task SearchByName()
    {
        Console.WriteLine("Searching for name......");

        var nameResponse = await osClient.SearchAsync<Student>(s => s
                                .Index(index)
                                .Query(q => q
                                .Match(m => m
                                .Field(fld => fld.FirstName)
                                .Query("Zhang"))));

        if (!nameResponse.IsValid)
        {
            throw new Exception("Name query response is not valid.");
        }

        foreach (var s in nameResponse.Documents)
        {
            Console.WriteLine("  " + s);
        }
    }

    private static async Task SearchByGradDate()
    {
        Console.WriteLine("Searching for grad date......");

        // Search for all students who graduated in 2022
        var gradResponse = await osClient.SearchAsync<Student>(s => s
                                .Index(index)
                                .From(0)
                                .Size(10)
                                .Scroll("1m")
                                .Query(q => q
                                .Bool(b => b
                                .Filter(f => f
                                .DateRange(r => r
                                    .Field(fld => fld.GradDate)
                                    .GreaterThanOrEquals("2022-01-01")
                                    .LessThanOrEquals("2022-12-31")))))
                                .Sort(srt => srt.Ascending(f => f.LastName)));


        if (!gradResponse.IsValid)
        {
            throw new Exception("Grad date query response is not valid.");
        }

        while (gradResponse.Documents.Any())
        {
            foreach (var data in gradResponse.Documents)
            {
                Console.WriteLine("  " + data);
            }
            gradResponse = await osClient.ScrollAsync<Student>("1m", gradResponse.ScrollId);
        }

        // Release the resources held by the scroll context
        await osClient.ClearScrollAsync(c => c.ScrollId(gradResponse.ScrollId));
    }

    public static async Task CalculateAverageGpa()
    {
        Console.WriteLine("Calculating average GPA......");

        // Search and aggregate
        // Size 0 means documents are not returned, only aggregation is returned
        var aggResponse = await osClient.SearchAsync<Student>(s => s
                                .Index(index)
                                .Size(0)
                                .Aggregations(a => a
                                .Average("average gpa",
                                            avg => avg.Field(fld => fld.Gpa))));

        if (!aggResponse.IsValid) throw new Exception("Aggregation response not valid");

        var avg = aggResponse.Aggregations.Average("average gpa").Value;
        Console.WriteLine($"Average GPA is {avg}");
    }
}
```
{% include copy.html %}

## 相關文件

- 如需更多使用該用戶端的範例，請參閱 [`opensearch-net` 使用者指南](https://github.com/opensearch-project/opensearch-net/blob/main/USER_GUIDE.md)。
- 如需特定工作的指南，例如大量編製索引與搜尋，請參閱 [`opensearch-net` 指南](https://github.com/opensearch-project/opensearch-net/tree/main/guides)。
- 如需完整的範例應用程式，請參閱 [`opensearch-net` 範例](https://github.com/opensearch-project/opensearch-net/tree/main/samples)。
