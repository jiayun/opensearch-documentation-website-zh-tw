---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "索引轉碼器"
parent: Tuning indexes
nav_order: 30
---

# 索引轉碼器

索引轉碼器決定索引的已儲存欄位在磁碟上如何壓縮與儲存。索引轉碼器由指定壓縮演算法的靜態 `index.codec` 設定控制。此設定會影響索引分片大小與索引操作效能。  

## 支援的轉碼器

OpenSearch 支援四種可用於壓縮已儲存欄位的轉碼器。每種轉碼器在壓縮率（儲存空間大小）與索引效能（速度）之間提供不同的取捨： 

* `default` -- 此轉碼器採用搭配預設字典的 [`LZ4` 演算法](https://en.wikipedia.org/wiki/LZ4_(compression_algorithm))，優先考量效能而非壓縮率。與 `best_compression` 相比，它提供更快的索引與搜尋作業，但可能導致較大的索引／分片大小。若索引設定中未提供任何轉碼器，則使用 `LZ4` 作為預設壓縮演算法。
* `best_compression` -- 此轉碼器使用 [`zlib`](https://en.wikipedia.org/wiki/Zlib) 作為基礎壓縮演算法。它可達到高壓縮率，進而產生較小的索引大小。然而，這可能會在索引作業期間產生額外的 CPU 使用量，並可能因此導致較高的索引與搜尋延遲。 

OpenSearch 也提供兩種以 [Zstandard 壓縮演算法](https://github.com/facebook/zstd) 為基礎的轉碼器。此演算法在壓縮率與速度之間提供良好的平衡。

變更現有索引的轉碼器設定可能相當困難（請參閱[變更索引轉碼器](#changing-an-index-codec)），因此在使用新的轉碼器設定之前，請務必在非正式環境中測試具代表性的工作負載。
{: .important}

* `zstd` -- 此轉碼器提供與 `best_compression` 轉碼器相當的顯著壓縮，且 CPU 使用量合理，並相較於 `default` 轉碼器改善了索引與搜尋效能。
* `zstd_no_dict` -- 此轉碼器與 `zstd` 類似，但不包含字典壓縮功能。相較於 `zstd`，它提供更快的索引與搜尋作業，但代價是索引大小略大。

`zstd` 與 `zstd_no_dict` 壓縮轉碼器無法用於 [k-NN]({{site.url}}{{site.baseurl}}/search-plugins/knn/index/) 或 [Security Analytics]({{site.url}}{{site.baseurl}}/security-analytics/index/) 索引。
{: .warning}

對於 `zstd` 與 `zstd_no_dict` 轉碼器，您可以選擇在 `index.codec.compression_level` 設定中指定壓縮層級。此設定接受 [1, 6] 範圍內的整數。較高的壓縮層級會產生較高的壓縮率（較小的儲存空間），但速度會有所取捨（較慢的壓縮與解壓縮速度會導致較大的索引與搜尋延遲）。 

建立索引分段時，會使用目前的索引轉碼器進行壓縮。若您更新索引轉碼器，更新後建立的任何分段都會使用新的壓縮演算法。關於特定作業的考量，請參閱[索引作業的索引轉碼器考量](#index-codec-considerations-for-index-operations)。
{: .note}

`DEFLATE` 與 `LZ4` 壓縮演算法提供硬體加速的壓縮轉碼器。這些硬體加速轉碼器可在執行 Linux 核心 3.10 及更新版本的最新第 4 代與第 5 代 Intel®️ Xeon®️ 處理器上使用。對於所有其他系統與平台，轉碼器會使用該平台對應的軟體實作。 

您可以設定下列其中一個 `index.codec` 值來使用硬體加速轉碼器：
* `qat_lz4`：硬體加速的 `LZ4`
* `qat_deflate`：硬體加速的 `DEFLATE`
* `qat_zstd`：硬體加速的 `ZSTD`

`qat_deflate` 轉碼器提供的壓縮率遠優於 `qat_lz4`，且壓縮與解壓縮速度僅略微下降。`qat_zstd` 轉碼器使用硬體加速進行壓縮，但依賴軟體解壓縮。
{: .note}

`index.codec.compression_level` 設定可用於指定 `qat_lz4`、`qat_deflate` 與 `qat_zstd` 的壓縮層級。 

`index.codec.qatmode` 設定控制硬體加速器的行為，並使用下列其中一個值：

* `auto`：若硬體加速失敗，演算法會切換為軟體加速。
* `hardware`：保證僅使用硬體壓縮。若硬體無法使用，則會發生例外狀況，直到硬體可用為止。

關於 `index.codec.qatmode` 設定對快照的影響，請參閱[快照](#snapshots)一節。

關於 Intel 上硬體加速的詳細資訊，請參閱 [Intel (R) QAT 加速器概覽](https://www.intel.com/content/www/us/en/developer/topic-technology/open/quick-assist-technology/overview.html)。

## 選擇轉碼器 

索引轉碼器的選擇會影響儲存索引資料所需的磁碟空間量。`best_compression`、`zstd` 與 `zstd_no_dict` 等轉碼器可達到較高的壓縮率，進而產生較小的索引大小。相反地，`default` 轉碼器不優先考量壓縮率，導致索引大小較大，但搜尋作業比 `best_compression` 更快。

## 索引作業的索引轉碼器考量

下列索引轉碼器考量適用於各種索引作業。

### 寫入

每個索引都由分片組成，而每個分片又進一步劃分為 Lucene 分段。在索引寫入期間，會根據索引設定中指定的轉碼器建立新的分段。若您更新索引的轉碼器，新的分段將使用新的轉碼器演算法。 

### 合併

在分段合併期間，OpenSearch 會將較小的索引分段合併為較大的分段，以提供最佳的資源使用率並改善效能。索引轉碼器設定會影響合併作業的速度與效率。索引上發生的合併次數取決於分段大小，而較小的分段大小會直接轉換為較小的合併大小。若您更新 `index.codec` 設定，新的合併作業在建立合併後的分段時將使用新的轉碼器。合併後的分段將具有新轉碼器的壓縮特性。

### 分割與縮減

[Split API]({{site.url}}{{site.baseurl}}/api-reference/index-apis/split/) 會將原始索引分割為新索引，其中每個原始主要分片會分割為兩個或多個主要分片。[Shrink API]({{site.url}}{{site.baseurl}}/api-reference/index-apis/shrink-index/) 會將現有索引縮減為具有較少主要分片數的新索引。在分割或縮減作業過程中，任何新建立的分段都會使用最新的轉碼器設定。

### 快照

建立[快照]({{site.url}}{{site.baseurl}}/tuning-your-cluster/availability-and-recovery/snapshots/index/)時，索引轉碼器設定會影響快照的大小及其建立所需的時間。若更新索引的轉碼器，新建立的快照將使用最新的轉碼器設定。產生的快照大小將反映最新轉碼器設定的壓縮特性。快照中包含的現有分段將保留其原始壓縮特性。 

當您將索引從某個叢集的快照還原至另一個叢集時，請務必確認目標叢集支援來源快照中分段的轉碼器。例如，若來源快照包含 `zstd` 或 `zstd_no_dict` 轉碼器的分段（於 OpenSearch 2.9 中推出），您將無法將該快照還原至執行較舊 OpenSearch 版本的叢集，因為該版本不支援這些轉碼器。 

對於 OpenSearch 2.15 及更新版本中提供的硬體加速壓縮轉碼器，`index.codec.qatmode` 的值會影響快照與還原的執行方式。若該值為 `auto`（預設值），則快照與還原可正常運作。然而，若該值為 `hardware`，則必須將其重設為 `auto`，還原程序才能在缺少硬體加速器的系統上成功。

您可以在還原程序期間修改 `index.codec.qatmode` 的值，方法如下：`"index_settings": {"index.codec.qatmode": "auto"}`。
{: .note}

### 重新編製索引

當您從來源索引執行[重新編製索引]({{site.url}}{{site.baseurl}}/im-plugin/reindex-data/)作業時，在目標索引中建立的新分段將具有目標索引轉碼器設定的屬性。 

### 索引彙總與轉換

當索引[彙總]({{site.url}}{{site.baseurl}}/im-plugin/index-rollups/)或[轉換]({{site.url}}{{site.baseurl}}/im-plugin/index-transforms/)作業完成時，在目標索引中建立的分段將具有目標索引建立期間所指定之索引轉碼器的屬性，與來源索引轉碼器無關。若目標索引是透過彙總作業動態建立，則目標索引的分段會使用預設轉碼器。

## 變更索引轉碼器

無法變更已開啟索引的轉碼器設定。您可以關閉索引、套用新的索引轉碼器設定，然後重新開啟索引，此時只有新的分段會以新的轉碼器寫入。這需要短暫停止對索引的所有讀取與寫入，以進行轉碼器變更，並可能導致分段大小與壓縮率不一致。或者，您可以將所有資料從來源索引重新編製索引至具有不同轉碼器設定的新索引，不過這是相當耗費資源的作業。

## 效能調校與基準測試

視您的特定使用案例而定，您可能需要嘗試不同的索引轉碼器設定，以微調 OpenSearch 叢集的效能。使用不同的轉碼器進行基準測試，並測量其對索引速度、搜尋效能與資源使用率的影響，可協助您找出適合您工作負載的最佳索引轉碼器設定。使用 `zstd` 與 `zstd_no_dict` 轉碼器時，您也可以微調壓縮層級，以找出適合您叢集的最佳組態。

### 基準測試

下表提供 `best_compression`、`zstd` 與 `zstd_no_dict` 轉碼器相較於 `default` 轉碼器的效能比較。測試是使用 [`nyc_taxi`](https://github.com/toddwschneider/nyc-taxi-data) 資料集執行。結果以百分比變化列出，粗體結果表示效能改善。

| | `best_compression` | `zstd` | `zstd_no_dict` |
|:---	|:---	|:---	|:--- |
|**寫入** | | | 
|中位數延遲	|0%	|0%	|&minus;1%	|
|p90 延遲	|3%	|2%	|**&minus;5%**	|
|輸送量	|&minus;2%	|**7%**	|**14%**	|
|**讀取**	| | | 
|中位數延遲	|0%	|1%	|0%	|
|p90 延遲	|1%	|1%	|**&minus;2%**	|
|**磁碟**	| | | 
| 壓縮率	|**&minus;34%**	|**&minus;35%**	|**&minus;30%**	|

