---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "為編製索引速度進行調校"
nav_order: 41
has_children: false
---

# 為編製索引速度調校您的叢集

下列組態在執行僅編製索引的工作負載時，相較於預設體驗，展現出約 60% 的輸送量提升。該工作負載並未納入搜尋或其他情境。機器上僅執行 OpenSearch 伺服器處理程序，基準測試用戶端則裝載於不同的節點上。

執行環境由 AWS Cloud 中的 Intel EC2 執行個體 (r7iz.2xlarge) 組成，所使用的工作負載為 OpenSearch Benchmark 所提供的 StackOverflow 資料集。

## Java 堆積大小

較大的 Java 堆積大小對編製索引很有幫助。將 Java 最小與最大堆積大小設為 RAM 大小的 50%，在 EC2 執行個體上可展現更好的編製索引效能。

## 排清 translog 閾值

`flush_threshold_size` 的預設值為 512 MB。這表示 translog 在達到 512 MB 時會排清。編製索引負載的權重決定了 translog 的頻率。當您增加 `index.translog.flush_threshold_size` 時，節點執行 translog 作業的頻率會降低。由於排清是耗用大量資源的作業，降低 translog 的頻率可改善編製索引效能。藉由增加排清閾值大小，OpenSearch 叢集也會建立較少的大型分段，而非多個小型分段。大型分段合併的頻率較低，且會有更多執行緒用於編製索引，而非用於合併。

對於純編製索引的工作負載，請考慮將 `flush_threshold_size` 增加至 Java 堆積大小的 25%，以改善編製索引效能。

增加 `index.translog.flush_threshold_size` 也可能增加 translog 完成所需的時間。如果分片失敗，由於 translog 較大，復原會耗費更多時間。
{: .note}

在增加 `index.translog.flush_threshold_size` 之前，請呼叫下列 API 作業以取得目前的排清作業統計資料：

```json
GET /{index}/_stats/flush?pretty
```
{% include copy-curl.html %}

在輸出中，請留意排清次數與總時間。下列範例輸出顯示有 124 次排清，耗時 17,690 毫秒：

```json
{
     "flush": {
          "total": 124,
          "total_time_in_millis": 17690
     }
}
```

若要增加排清閾值大小，請呼叫下列 API 作業：

```json
PUT /{index}/_settings 
{
  "index":
  {
    "translog.flush_threshold_size" : "1024MB"
  }
}
```
{% include copy-curl.html %}

在此範例中，排清閾值大小設為 1024 MB，這對記憶體超過 32 GB 的執行個體而言最為理想。

請為您的叢集選擇適當的閾值大小。
{: .note}

再次執行 stats API 作業，以查看排清活動是否有所改變：

```json
GET /{index}/_stats/flush
```
{% include copy-curl.html %}

最佳做法是僅為目前的索引增加 `index.translog.flush_threshold_size`。確認結果之後，再將變更套用至索引範本。
{: .note}

## 索引重新整理間隔

根據預設，OpenSearch 每秒都會重新整理索引。OpenSearch 只會重新整理在過去 30 秒內收到至少一個搜尋請求的索引。

當您增加重新整理間隔時，資料節點發出的 API 呼叫會減少。為避免 [429 錯誤](https://repost.aws/knowledge-center/opensearch-resolve-429-error)，最佳做法是增加重新整理間隔。

如果您的應用程式可以容忍文件編製索引的時間與其變為可見的時間之間的時間增加，您可以將 `index.refresh_interval` 增加至較大的值，例如 `30s`，甚至在純編製索引的情境中將其停用，以改善編製索引速度。

## 索引緩衝區大小

如果節點正在執行大量編製索引，請確定索引緩衝區大小足夠大。您可以將索引緩衝區大小設為 Java 堆積大小的百分比，或設為位元組數。在大多數情況下，JVM 記憶體 10% 的預設值便已足夠。您可以嘗試將其增加至最高 25%，以進一步改善。

## 並行合併

並行合併的最大數量指定為 `max_merge_count`。concurrentMergeScheduler 會在需要時控制合併作業的執行。合併會在不同的執行緒中執行，當達到執行緒數量上限時，後續的合併會等待直到有合併執行緒可用為止。
若索引節流是問題所在，請考慮將合併執行緒數目增加至超過預設值。

## 分片分配

為確保分片平均分配於您要將資料匯入之索引的資料節點上，請使用下列公式確認分片已平均分配：

索引的分片數 = k * (資料節點數)，其中 k 是每個節點的分片數

例如，如果索引中有 24 個分片，且有 8 個資料節點，則 OpenSearch 會為每個節點分配 3 個分片。 

## 將副本計數設為零

如果您預期會有大量編製索引，請考慮將 `index.number_of_replicas` 值設為 `0`。每個副本都會複製編製索引的流程。因此，停用副本可改善您的叢集效能。大量編製索引完成後，請重新啟用已複寫的索引。

如果在停用副本時節點失敗，您可能會遺失資料。只有在您可以容忍短時間內遺失資料時，才停用副本。
{: .important }

## 實驗以找出最佳的 bulk 請求大小

請從 5 MiB 至 15 MiB 的 bulk 請求大小開始。然後慢慢增加請求大小，直到編製索引效能不再改善為止。 

## 使用具有 SSD 執行個體儲存磁碟區的執行個體類型 (例如 I3)

I3 執行個體提供快速的本機 NVMe 儲存空間。I3 執行個體提供比使用一般用途 SSD (gp2) Amazon Elastic Block Store (Amazon EBS) 磁碟區的執行個體更好的匯入效能。如需詳細資訊，請參閱 [Amazon OpenSearch Service 的 PB 級規模](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/petabyte-scale.html)。

## 縮減回應大小

若要縮減 OpenSearch 回應的大小，請使用 `filter_path` 參數來排除不必要的欄位。請務必不要篩除任何識別或重試失敗請求所需的欄位。這些欄位會因用戶端而異。

在下列範例中，`index-name`、`type-name` 和 `took` 欄位會從回應中排除：

```json
POST /_bulk?pretty&filter_path=-took,-items.index._index,-items.index._type
{ "index" : { "_index" : "test2", "_id" : "1" } }
{ "user" : "testuser" }
{ "update" : {"_id" : "1", "_index" : "test2"} }
{ "doc" : {"user" : "example"} }
```
{% include copy-curl.html %}

## 壓縮轉碼器

在 OpenSearch 2.9 及更新版本中，有兩種新的壓縮轉碼器：`zstd` 和 `zstd_no_dict`。您可以選擇在 `index.codec.compression_level` 設定中為這些轉碼器指定壓縮層級，其值範圍為 [1, 6]。[基準測試]({{site.url}}{{site.baseurl}}/im-plugin/index-codecs/#benchmarking)資料顯示，與 `default` 轉碼器相比，`zstd` 提供高出 7% 的寫入輸送量，`zstd_no_dict` 提供高出 14% 的輸送量，同時儲存空間改善 30%。如需壓縮的詳細資訊，請參閱 [索引轉碼器]({{site.url}}{{site.baseurl}}/im-plugin/index-codecs/)。
