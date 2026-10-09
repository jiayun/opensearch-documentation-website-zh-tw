---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "索引轉換"
nav_order: 60
has_children: true
redirect_from:
  - /im-plugin/index-transforms/
has_toc: false
---

# 索引轉換

索引彙整作業可讓您將舊資料彙整至精簡的索引，以降低資料細緻度；而轉換作業則可讓您建立以特定欄位為中心、經過彙總的資料檢視，以便用不同的方式將資料視覺化或進行分析。

舉例來說，假設您有分散於多個欄位和類別的航空公司資料，而您想查看依航空公司、季度及價格整理的資料摘要。您可以使用轉換作業建立一個依這些特定類別整理的新彙總索引。

您可以透過下列任一方式建立轉換作業：

- 在 OpenSearch Dashboards 中建立，它會顯示來源索引的欄位及範例資料、在您選取欄位時預覽轉換後的欄位，並列出您已建立的作業及其狀態。請參閱[建立轉換作業](#creating-a-transform-job)。
- 使用 [Transforms API]({{site.url}}{{site.baseurl}}/im-plugin/index-transforms/transforms-apis/) 建立，這些 API 會將整份作業組態以 JSON 形式接收，因此您可以將其儲存在版本控制中，並跨叢集複製。

## 設定轉換作業

轉換作業會從來源索引讀取資料，並將彙總後的文件寫入目標索引。若只要轉換來源索引的一部分，請新增以 [query DSL]({{site.url}}{{site.baseurl}}/query-dsl/) 撰寫的篩選條件。

作業組態分為兩個部分：

- *分組*會將文件放入目標索引中的桶。每個分組會指定來源索引中的一個 `source_field`，以及要寫入的 `target_field`，因此將範例航班資料的 `DestAirportID` 欄位分組到 `DestAirportID_terms` 目標欄位，會為每個機場產生一個桶。若省略 `target_field`，則會採用來源欄位的名稱。OpenSearch Dashboards 會附加分組的名稱，例如 `DestAirportID_terms`。轉換作業支援 `histogram`、`date_histogram` 及 `terms` [桶彙總]({{site.url}}{{site.baseurl}}/aggregations/bucket/index/)。
- *彙總*會為每個桶計算一個值，例如用於加總桶內票價的 `sum_of_total_ticket_price` 欄位。支援 `sum`、`avg`、`max`、`min`、`value_count`、`percentiles` 及 `scripted_metric` [指標彙總]({{site.url}}{{site.baseurl}}/aggregations/metric/index/)。

建立作業後，您無法變更其分組或彙總。

作業會依您設定的轉換執行間隔執行。連續作業會在每個間隔執行，並轉換自上次執行後有所變更的桶，包括新增資料的桶。非連續作業則會在第一個間隔經過後執行一次。每次執行處理的頁數會在速度與記憶體之間取捨：頁數越大，每個搜尋請求處理的資料越多，且可能超出叢集的記憶體限制。

## 範例：轉換範例航班資料

本範例會依航空公司和目的地機場彙總 OpenSearch Dashboards 範例航班資料。若要新增資料，請前往 OpenSearch Dashboards 首頁，選取 **Try our sample data**，然後在 **Sample flight data** 中選取 **Add data**。

下列作業會將 `Carrier` 和 `DestAirportID` 欄位分組，並加總每個桶中的票價：

```json
PUT _plugins/_transform/sample_flight_job
{
  "transform": {
    "enabled": true,
    "schedule": {
      "interval": {
        "period": 1,
        "unit": "Minutes",
        "start_time": 1602100553
      }
    },
    "description": "Sample flight transform job",
    "source_index": "opensearch_dashboards_sample_data_flights",
    "target_index": "finished_flight_job",
    "page_size": 1000,
    "groups": [
      {
        "terms": {
          "source_field": "Carrier",
          "target_field": "Carrier_terms"
        }
      },
      {
        "terms": {
          "source_field": "DestAirportID",
          "target_field": "DestAirportID_terms"
        }
      }
    ],
    "aggregations": {
      "sum_of_total_ticket_price": {
        "sum": {
          "field": "AvgTicketPrice"
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

作業會在第一個間隔經過後執行。若要查看其進度，請使用 [Explain API]({{site.url}}{{site.baseurl}}/im-plugin/index-transforms/transforms-apis/#get-the-status-of-a-transform-job)：

```json
GET _plugins/_transform/sample_flight_job/_explain
```
{% include copy-curl.html %}

## 搜尋轉換後的索引

轉換作業完成後，請使用 `_search` API 搜尋目標索引。目標索引中的每份文件都包含分組欄位、彙總值、寫入該文件的作業 ID (位於 `transform._id`)，以及桶中的來源文件數 (同時以 `_doc_count` 和 `transform._doc_count` 回報)。

下列請求會傳回轉換後航班索引中 `DestAirportID_terms` 為 `SFO` 的桶：

```json
GET finished_flight_job/_search
{
  "query": {
    "match": {
      "DestAirportID_terms" : "SFO"
    }
  }
}
```
{% include copy-curl.html %}

<details markdown="block">
  <summary>
    回應
  </summary>
  {: .text-delta}

```json
{
  "took" : 3,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 4,
      "relation" : "eq"
    },
    "max_score" : 1.0,
    "hits" : [
      {
        "_index" : "finished_flight_job",
        "_id" : "ifSaM4kOvFxWHw84UpfMRQ",
        "_score" : 1.0,
        "_source" : {
          "transform._id" : "sample_flight_job",
          "_doc_count" : 10,
          "transform._doc_count" : 10,
          "Carrier_terms" : "BeatsWest",
          "DestAirportID_terms" : "SFO",
          "sum_of_total_ticket_price" : 7012.053009033203
        }
      },
      {
        "_index" : "finished_flight_job",
        "_id" : "uBoQr4Q393MMLHCzz1DQPQ",
        "_score" : 1.0,
        "_source" : {
          "transform._id" : "sample_flight_job",
          "_doc_count" : 14,
          "transform._doc_count" : 14,
          "Carrier_terms" : "Logstash Airways",
          "DestAirportID_terms" : "SFO",
          "sum_of_total_ticket_price" : 9678.005126953125
        }
      },
      {
        "_index" : "finished_flight_job",
        "_id" : "1pi8feMm2fDwop05MkC6qA",
        "_score" : 1.0,
        "_source" : {
          "transform._id" : "sample_flight_job",
          "_doc_count" : 14,
          "transform._doc_count" : 14,
          "Carrier_terms" : "OpenSearch Dashboards Airlines",
          "DestAirportID_terms" : "SFO",
          "sum_of_total_ticket_price" : 9238.96060180664
        }
      },
      {
        "_index" : "finished_flight_job",
        "_id" : "56d2npFptOKeHZEt6BlohA",
        "_score" : 1.0,
        "_source" : {
          "transform._id" : "sample_flight_job",
          "_doc_count" : 11,
          "transform._doc_count" : 11,
          "Carrier_terms" : "OpenSearch-Air",
          "DestAirportID_terms" : "SFO",
          "sum_of_total_ticket_price" : 6317.92561340332
        }
      }
    ]
  }
}
```
</details>

## 索引編解碼器考量事項

關於索引編解碼器考量事項，請參閱[索引編解碼器]({{site.url}}{{site.baseurl}}/im-plugin/index-codecs/#index-rollups-and-transforms)。

## OpenSearch Dashboards 中的索引轉換

若要前往 **Index Management** 頁面，請在上方功能表前往 **Management > Index Management**。選取 **Transform jobs** 以列出叢集中的轉換作業及其來源索引、目標索引和狀態。選取作業以檢視其組態和執行結果。若要對作業採取動作，請選取其旁邊的核取方塊，然後選取 **Enable**、**Disable** 或 **Actions > Delete**。

下圖顯示 **Transform jobs** 頁面。

![轉換作業頁面]({{site.url}}{{site.baseurl}}/images/admin-ui-index/transform-jobs-list.png)

如果您的叢集沒有可轉換的資料，請從 OpenSearch Dashboards 首頁新增範例航班資料並加以轉換。如需詳細資訊，請參閱[新增範例資料]({{site.url}}{{site.baseurl}}/dashboards/getting-started/data-setup/#add-sample-data)。

### 建立轉換作業

1. 在 **Index Management** 中，選取 **Transform jobs**，然後選取 **Create transform job**。
1. 輸入作業的 **Name**，並選擇性輸入說明。
1. 在 **Source index** 中，選取要轉換的索引。
1. 選擇性在 **Source index filter** 中，選取 **Edit data filter**，輸入可選取要轉換之文件的 [query DSL]({{site.url}}{{site.baseurl}}/query-dsl/) 查詢，然後選取 **Save**。例如，下列篩選條件會選取票價至少 $1,000 的航班：

   ```json
   {
     "bool": {
       "filter": [
         { "range": { "AvgTicketPrice": { "gte": "1000" }}}
       ]
     }
   }
   ```
   {% include copy.html %}

1. 在 **Target index** 中，選取現有索引，或輸入新索引的名稱。
1. 選取 **Next**。
1. 在 **Define transforms** 中，選取要彙總的欄位：

   1. 選取 **N columns hidden** 連結，並選取您要在目標索引中使用的欄位。若要從空白表格開始，請選取 **Hide all**，然後逐一新增欄位。
   1. 針對 **Original fields with sample data** 中的每個欄位，選取 {::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/icons/add-filter-icon.png" class="inline-icon" alt="plus icon"/>{:/} (加號) 圖示，然後選取分組或彙總。結果會新增至 **Transformed fields preview based on sample data**。

1. 選取 **Next**。
1. 在 **Specify schedule** 中，執行下列操作：

   1. 若要讓作業依其排程執行，而非僅在手動啟動時執行，請保持選取 **Job enabled by default**。
   1. 若要轉換每次執行後變更的桶，請在 **Continuous** 中選取 **Yes**。
   1. 在 **Transform execution interval** 中，輸入間隔並選取 **Minute(s)**、**Hour(s)** 或 **Day(s)**。
   1. 選擇性展開 **Advanced**，並輸入 **Pages per execution** 的數目。數目越大，執行越快，且使用更多記憶體。

1. 選取 **Next**，檢閱組態，然後選取 **Create transform job**。若要變更面板，請在該面板中選取 **Edit**。

## 相關文件

- [Transforms API]({{site.url}}{{site.baseurl}}/im-plugin/index-transforms/transforms-apis/)
- [索引彙整]({{site.url}}{{site.baseurl}}/im-plugin/index-rollups/index/)
- [索引狀態管理]({{site.url}}{{site.baseurl}}/im-plugin/ism/index/)
