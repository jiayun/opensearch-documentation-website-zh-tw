---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "分段複製"
nav_order: 70
has_children: true
parent: Availability and recovery
datatable: true
redirect_from:
  - /opensearch/segment-replication/
  - /opensearch/segment-replication/index/
  - /tuning-your-cluster/segment-replication/
  - /tuning-your-cluster/availability-and-recovery/segment-replication/
---

# 分段複製

分段複製是在分片之間複製分段檔案，而不是在每個分片副本上將文件編製索引。這種做法可提升索引處理輸送量並降低資源使用率，但會增加網路使用率。分段複製是一系列旨在解耦讀取與寫入以降低運算成本的功能中的第一項。

當主要分片在重新整理時將檢查點傳送至副本分片，副本分片上就會觸發新的分段複製事件。這會發生在：

- 將新的副本分片新增至叢集時。
- 主要分片重新整理時有分段檔案變更時。
- 對等復原期間，例如副本分片復原與分片重新配置（使用 `move` allocation 命令的明確配置，或自動分片重新平衡）。

## 使用案例

分段複製可應用於多種情境，包括：

- 寫入負載高但搜尋需求不高，且重新整理時間較長的情境。
- 負載極高時，您想新增節點但不想立即為所有資料編製索引。
- 副本數量較低的 OpenSearch 叢集部署，例如用於記錄分析的部署。

## 遠端後端儲存空間

您可以使用兩種方式進行分段複製：

- **遠端後端儲存空間**，一種持久性儲存方案：主要分片將分段檔案傳送至遠端後端儲存空間，副本分片則從同一個儲存位置取得副本。如需使用遠端後端儲存空間的更多資訊，請參閱[遠端後端儲存空間]({{site.url}}{{site.baseurl}}/tuning-your-cluster/availability-and-recovery/remote-store/index/)。
- 節點對節點通訊：主要分片使用節點對節點通訊直接將分段檔案傳送至副本分片。

## 分段複製組態

為叢集設定預設複製類型會影響所有新建立的索引。不過，您可以在建立索引時指定不同的複製類型。索引層級的設定會覆寫叢集層級的設定。

### 建立使用分段複製的索引

若要使用分段複製作為索引的複製策略，請在建立索引時將 `replication.type` 參數設為 `SEGMENT`，如下所示：

```json
PUT /my-index1
{
  "settings": {
    "index": {
      "replication.type": "SEGMENT" 
    }
  }
}
```
{% include copy-curl.html %}

如果您使用遠端後端儲存空間，請在索引請求本文中加入 `remote_store` 屬性。

使用節點對節點複製時，主要分片會消耗較多的網路頻寬，因為它會將分段檔案推送至所有副本分片。因此，將主要分片平均分配至各節點會有所幫助。若要確保主要分片分配均衡，請將動態設定 `cluster.routing.allocation.balance.prefer_primary` 設為 `true`。如需更多資訊，請參閱[叢集設定]({{site.url}}{{site.baseurl}}/api-reference/cluster-api/cluster-settings/)。

為獲得最佳效能，建議您啟用下列設定：

1. [分段複製背壓]({{site.url}}{{site.baseurl}}/tuning-your-cluster/availability-and-recovery/segment-replication/backpressure/)
2. 使用下列命令進行均衡的主要分片配置：

```json
PUT /_cluster/settings
{
  "persistent": {
    "cluster.routing.allocation.balance.prefer_primary": true,
    "segrep.pressure.enabled": true
  }
}
```
{% include copy-curl.html %}

### 為叢集設定複製類型

您可以在 `opensearch.yml` 檔案中為新建立的叢集索引設定預設複製類型，如下所示：

```yaml
cluster.indices.replication.strategy: 'SEGMENT'
```
{% include copy.html %}


### 強制使用叢集層級的複製類型

若已啟用，`cluster.index.restrict.replication.type` 設定會要求新建立的索引必須在 `cluster.indices.replication.strategy` 叢集設定中指定複製類型。指定不同複製類型的請求會被拒絕。若 `cluster.index restrict.replication.type` 已停用，您可以在 `index.replication.type` 設定中指定複製類型，以每個索引為基準選擇複製類型。

您可以在 `opensearch.yml` 檔案中定義 `cluster.index.restrict.replication.type` 設定，如下所示：

```yaml
cluster.index.restrict.replication.type: true
```
{% include copy.html %}

### 建立使用文件複製的索引

即使預設複製類型已設為分段複製，您仍可透過將 `replication.type` 設為 `DOCUMENT` 來建立使用文件複製的索引，如下所示：

```json
PUT /my-index1
{
  "settings": {
    "index": {
      "replication.type": "DOCUMENT" 
    }
  }
}
```
{% include copy-curl.html %}

## 注意事項

使用分段複製時，請考量下列事項：

1. 為現有索引啟用分段複製需要[重新編製索引](https://github.com/opensearch-project/OpenSearch/issues/3685)。
1. [跨叢集複製](https://github.com/opensearch-project/OpenSearch/issues/4090)目前並未使用分段複製在叢集之間進行複製。
1. 分段複製會導致使用節點對節點複製的主要分片網路壅塞增加，因為副本分片會從主要分片取得更新。使用遠端後端儲存空間時，主要分片可以將分段上傳至遠端後端儲存空間，副本也可以從遠端後端儲存空間取得更新。這有助於將主要分片的責任轉移至遠端後端儲存空間。
1. 寫入後讀取保證：分段複製不支援將重新整理原則設為 `wait_for` 或 `true`。如果您將 `refresh` 查詢參數設為 `wait_for` 或 `true` 然後匯入文件，只有在主要節點完成重新整理並使這些文件可被搜尋之後，您才會收到回應。副本分片只有在寫入其本機 translog 之後才會回應。如果需要即時讀取，請考慮使用 [`get`]({{site.url}}{{site.baseurl}}/api-reference/document-apis/get-documents/) 或 [`mget`]({{site.url}}{{site.baseurl}}/api-reference/document-apis/multi-get/) API 操作。
1. 系統索引支援分段複製。
1. Get、MultiGet、TermVector 與 MultiTermVector 請求會將請求路由至主要分片以提供強式讀取。將較多請求路由至主要分片，相較於將請求分散至主要與副本分片，可能會降低效能。若要在讀取繁重的叢集中提升效能，建議將這些請求中的 `realtime` 參數設為 `false`。如需更多資訊，請參閱 [Issue #8700](https://github.com/opensearch-project/OpenSearch/issues/8700)。

## 效能基準測試

在初始基準測試期間，分段複製的使用者回報，在相同的叢集設定下，輸送量比使用文件複製高出 40%。

下列基準測試是使用 [OpenSearch-benchmark]({{site.url}}{{site.baseurl}}/benchmark/index/) 搭配 [`stackoverflow`](https://www.kaggle.com/datasets/stackoverflow/stackoverflow) 與 [`nyc_taxi`](https://github.com/toddwschneider/nyc-taxi-data) 資料集收集的。

這些基準測試展示了下列組態對分段複製的影響：

- [工作負載大小](#increasing-the-workload-size)
- [主要分片數量](#increasing-the-number-of-primary-shards)
- [副本數量](#increasing-the-number-of-replicas)

您的結果可能會因叢集拓撲、使用的硬體、分片數量與合併設定而有所不同。
{: .note }

### 增加工作負載大小

下表列出 `nyc_taxi` 資料集在下列組態下的基準測試結果：

- 10 個 m5.xlarge 資料節點
- 40 個主要分片，每個各 1 個副本 (總共 80 個分片)
- 每個節點 4 個主要分片和 4 個副本分片

<table>
    <th colspan="2" ></th>
    <th colspan="3" >40 GB 主要分片，總計 80 GB</th>
    <th colspan="3">240 GB 主要分片，總計 480 GB</th>
    <tr>
        <td></td>
        <td></td>
        <td>文件複製</td>
        <td>分段複製</td>
        <td>差異百分比</td>
        <td>文件複製</td>
        <td>分段複製</td>
        <td>差異百分比</td>
    </tr>
    <tr>
        <td>儲存大小</td>
        <td ></td>
        <td>85.2781</td>
        <td>91.2268</td>
        <td>N/A</td>
        <td>515.726</td>
        <td>558.039</td>
        <td>N/A</td>
    </tr>
    <tr>
        <td rowspan="3">索引輸送量 (每秒請求數)</td>
        <td>最小值</td>
        <td>148,134</td>
        <td>185,092</td>
        <td>24.95%</td>
        <td>100,140</td>
        <td>168,335</td>
        <td>68.10%</td>
    </tr>
    <tr>
        <td class="td-custom">中位數</td>
        <td>160,110</td>
        <td>189,799</td>
        <td>18.54%</td>
        <td>106,642</td>
        <td>170,573</td>
        <td>59.95%</td>
    </tr>
    <tr>
        <td class="td-custom">最大值</td>
        <td>175,196</td>
        <td>190,757</td>
        <td>8.88%</td>
        <td>108,583</td>
        <td>172,507</td>
        <td>58.87%</td>
    </tr>
    <tr>
        <td>錯誤率</td>
        <td ></td>
        <td>0.00%</td>
        <td>0.00%</td>
        <td >0.00%</td>
        <td>0.00%</td>
        <td>0.00%</td>
        <td>0.00%</td>
    </tr>
</table>

隨著工作負載大小增加，分段複製的效益會隨之放大，因為副本不需要為更大的資料集編製索引。一般而言，在所有叢集組態下，分段複製相較於文件複製能以較低的資源成本達到更高的輸送量，這還不計入複製延遲。

### 增加主要分片數量

下表列出 `nyc_taxi` 資料集在 40 個和 100 個主要分片下的基準測試結果。

{::nomarkdown}
<table>
    <th colspan="2"></th>
    <th colspan="3">40 個主要分片，1 個副本</th>
    <th colspan="3">100 個主要分片，1 個副本</th>
    <tr>
        <td></td>
        <td></td>
        <td>文件複製</td>
        <td>分段複製</td>
        <td>差異百分比</td>
        <td>文件複製</td>
        <td>分段複製</td>
        <td>差異百分比</td>
    </tr>
    <tr>
        <td rowspan="3">索引輸送量 (每秒請求數)</td>
        <td>最小值</td>
        <td>148,134</td>
        <td>185,092</td>
        <td>24.95%</td>
        <td>151,404</td>
        <td>167,391</td>
        <td>9.55%</td>
    </tr>
    <tr>
        <td class="td-custom">中位數</td>
        <td>160,110</td>
        <td>189,799</td>
        <td>18.54%</td>
        <td>154,796</td>
        <td>172,995</td>
        <td>10.52%</td>
    </tr>
    <tr>
        <td class="td-custom">最大值</td>
        <td>175,196</td>
        <td>190,757</td>
        <td>8.88%</td>
        <td>166,173</td>
        <td>174,655</td>
        <td>4.86%</td>
    </tr>
    <tr>
        <td>錯誤率</td>
        <td ></td>
        <td>0.00%</td>
        <td>0.00%</td>
        <td >0.00%</td>
        <td>0.00%</td>
        <td>0.00%</td>
        <td>0.00%</td>
    </tr>
</table>
{:/}

隨著主要分片數量增加，分段複製相較於文件複製的效益會隨之降低。雖然在主要分片數量較多時分段複製仍具效益，但效能差異會變得較不明顯，因為每個節點上有更多主要分片必須在叢集內複製分段檔案。

### 增加副本數量

下表列出 `stackoverflow` 資料集在 1 個和 9 個副本下的基準測試結果。

{::nomarkdown}
<table>
    <th colspan="2"  ></th>
    <th colspan="3"  >10 個主要分片，1 個副本</th>
    <th colspan="3">10 個主要分片，9 個副本</th>
    <tr>
        <td></td>
        <td></td>
        <td>文件複製</td>
        <td>分段複製</td>
        <td>差異百分比</td>
        <td>文件複製</td>
        <td>分段複製</td>
        <td>差異百分比</td>
    </tr>
    <tr>
        <td rowspan="2">索引輸送量 (每秒請求數)</td>
        <td >中位數</td>
        <td>72,598.10</td>
        <td>90,776.10</td>
        <td>25.04%</td>
        <td>16,537.00</td> 
        <td>14,429.80</td> 
        <td>&minus;12.74%</td>
    </tr>
    <tr>
        <td class="td-custom">最大值</td>
        <td>86,130.80</td>
        <td>96,471.00</td>
        <td>12.01%</td>
        <td>21,472.40</td>
        <td>38,235.00</td>
        <td>78.07%</td>
    </tr>
    <tr>
        <td rowspan="4">CPU 使用率 (%)</td>
        <td >p50</td>
        <td>17</td>
        <td>18.857</td>
        <td>10.92%</td>
        <td>69.857</td>
        <td>8.833</td>
        <td>&minus;87.36%</td>
    </tr>
    <tr>
        <td class="td-custom">p90</td>
        <td>76</td>
        <td>82.133</td>
        <td>8.07%</td>
        <td>99</td>
        <td>86.4</td>
        <td>&minus;12.73%</td>
    </tr>
    <tr>
        <td class="td-custom">p99</td>
        <td>100</td>
        <td>100</td>
        <td >0%</td>
        <td>100</td>
        <td>100</td>
        <td>0%</td>
    </tr>
    <tr>
        <td class="td-custom">p100</td>
        <td>100</td>
        <td>100</td>
        <td >0%</td>
        <td>100</td>
        <td>100</td>
        <td>0%</td>
    </tr>
    <tr>
        <td rowspan="4">記憶體使用率 (%)</td>
        <td >p50</td>
        <td>35</td>
        <td>23</td>
        <td>&minus;34.29%</td>
        <td>42</td>
        <td>40</td>
        <td>&minus;4.76%</td>
    </tr>
    <tr>
        <td class="td-custom">p90</td>
        <td>59</td>
        <td>57</td>
        <td>&minus;3.39%</td>
        <td>59</td>
        <td>63</td>
        <td>6.78%</td>
    </tr>
    <tr>
        <td class="td-custom">p99</td>
        <td>69</td>
        <td>61</td>
        <td>&minus;11.59%</td>
        <td>66</td>
        <td>70</td>
        <td>6.06%</td>
    </tr>
    <tr>
        <td class="td-custom">p100</td>
        <td>72</td>
        <td>62</td>
        <td>&minus;13.89%</td>
        <td>69</td>
        <td>72</td>
        <td>4.35%</td>
    </tr>
    <tr>
        <td>錯誤率</td>
        <td ></td>
        <td>0.00%</td>
        <td>0.00%</td>
        <td >0.00%</td>
        <td>0.00%</td>
        <td>2.30%</td>
        <td>2.30%</td>
    </tr>
</table>
{:/}

隨著副本數量增加，主要分片讓副本保持最新狀態所需的時間 (稱為 _複製延遲_) 也會增加。這是因為分段複製會直接將分段檔案從主要分片複製到副本。

基準測試結果顯示，隨著副本數量增加，錯誤率不為零。錯誤率表示當副本無法跟上主要分片時，會啟動[分段複製背壓]({{site.url}}{{site.baseurl}}/tuning-your-cluster/availability-and-recovery/segment-replication/backpressure/)機制。然而，分段複製所帶來的顯著 CPU 和記憶體效益可抵銷此錯誤率。

## 後續步驟

1. 追蹤[分段複製的未來增強功能](https://github.com/orgs/opensearch-project/projects/99)。
1. 閱讀[這篇關於分段複製的部落格文章](https://opensearch.org/blog/segment-replication/)。
