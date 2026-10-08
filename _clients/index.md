---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "語言用戶端"
nav_order: 1
has_children: false
nav_exclude: true
permalink: /clients/
redirect_from:
  - /clients/index/
---

# ![用戶端圖示]({{site.url}}{{site.baseurl}}/images/icons/OpenSearch-Clients-Icon.avif){: .heading-icon} OpenSearch 語言用戶端

OpenSearch 用戶端可讓您從應用程式的程式碼中使用 OpenSearch。用戶端會連線至您的叢集、傳送請求，並以您所用程式語言的物件形式傳回回應，因此您無須自行建構 HTTP 請求及剖析 JSON，即可建立索引、新增文件及進行搜尋。

## OpenSearch 用戶端

OpenSearch 為下列程式語言與平台提供用戶端：

* **Python**
  * [OpenSearch Python 用戶端]({{site.url}}{{site.baseurl}}/clients/python-low-level/)
  * [OpenSearch Python ML 用戶端]({{site.url}}{{site.baseurl}}/clients/opensearch-py-ml/)：使用 DataFrame 分析 OpenSearch 索引中的資料，並將機器學習 (ML) 模型上傳至 OpenSearch。
* **Java**
  * [OpenSearch Java 用戶端]({{site.url}}{{site.baseurl}}/clients/java/)
* **JavaScript**
  * [OpenSearch JavaScript (Node.js) 用戶端]({{site.url}}{{site.baseurl}}/clients/javascript/index/)
* **Go**
  * [OpenSearch Go 用戶端]({{site.url}}{{site.baseurl}}/clients/go/)
* **Ruby**
  * [OpenSearch Ruby 用戶端]({{site.url}}{{site.baseurl}}/clients/ruby/)
* **PHP**
  * [OpenSearch PHP 用戶端]({{site.url}}{{site.baseurl}}/clients/php/)
* **.NET**
  * [OpenSearch .NET 用戶端]({{site.url}}{{site.baseurl}}/clients/dot-net/)
* **Rust**
  * [OpenSearch Rust 用戶端]({{site.url}}{{site.baseurl}}/clients/rust/)
* **Hadoop**
  * [Hadoop 連接器 (Apache Spark、Apache Hive 及 Hadoop MapReduce)]({{site.url}}{{site.baseurl}}/clients/hadoop/)

## 已淘汰的用戶端

下列用戶端已淘汰：

* [OpenSearch 高階 Python 用戶端]({{site.url}}{{site.baseurl}}/clients/python-high-level/)：請改用 [OpenSearch Python 用戶端]({{site.url}}{{site.baseurl}}/clients/python-low-level/)。
* [OpenSearch Java 高階 REST 用戶端]({{site.url}}{{site.baseurl}}/clients/java-rest-high-level/)：請改用 [OpenSearch Java 用戶端]({{site.url}}{{site.baseurl}}/clients/java/)。


## 舊版用戶端

可搭配 Elasticsearch OSS 7.10.2 使用的用戶端，應該也能搭配 OpenSearch 1.x 使用。不過，這些用戶端的最新版本可能包含授權或版本檢查，因而刻意破壞相容性。下表提供建議使用的用戶端版本，以便與 OpenSearch 1.x 達到最佳相容性。對於 OpenSearch 2.0 及更新版本，沒有任何 Elasticsearch 用戶端能與 OpenSearch 完全相容。

雖然 OpenSearch 與 Elasticsearch 共有數項核心功能，但混用兩者的用戶端與伺服器極有可能導致錯誤及非預期的結果。隨著 OpenSearch 與 Elasticsearch 持續分歧，此類風險可能會增加。儘管您的 Elasticsearch 用戶端或許仍可繼續搭配您的 OpenSearch 叢集使用，但建議您針對 OpenSearch 叢集使用 OpenSearch 用戶端。
{: .warning}

若要檢視特定用戶端的相容性對照表，請參閱該用戶端儲存庫中的 `COMPATIBILITY.md` 檔案。

用戶端 | 建議版本
:--- | :---
[Elasticsearch Java 低階 REST 用戶端](https://central.sonatype.com/artifact/org.elasticsearch.client/elasticsearch-rest-client/7.13.4) | 7.13.4
[Elasticsearch Java 高階 REST 用戶端](https://central.sonatype.com/artifact/org.elasticsearch.client/elasticsearch-rest-high-level-client/7.13.4) | 7.13.4
[Elasticsearch Python 用戶端](https://pypi.org/project/elasticsearch/7.13.4/) | 7.13.4
[Elasticsearch Node.js 用戶端](https://www.npmjs.com/package/@elastic/elasticsearch/v/7.13.0) | 7.13.0
[Elasticsearch Ruby 用戶端](https://rubygems.org/gems/elasticsearch/versions/7.13.0) | 7.13.0

若您測試某個舊版用戶端並確認其可正常運作，請[提交 PR](https://github.com/opensearch-project/documentation-website/pulls) 並將其新增至此表。
