---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "其他外掛程式"
parent: Managing OpenSearch plugins
nav_order: 10
has_children: true
has_toc: false
redirect_from:
  - /install-and-configure/additional-plugins/
---

# 其他外掛程式

除了 OpenSearch 標準發行版本所提供的外掛程式之外，還有許多其他外掛程式可供使用。這些其他外掛程式由 OpenSearch 開發人員或 OpenSearch 社群成員所建置。其中大多數都維護於 GitHub 上的 [OpenSearch/plugins](https://github.com/opensearch-project/OpenSearch/tree/main/plugins) 目錄中，並且可以依名稱安裝，例如執行 `bin/opensearch-plugin install <plugin-name>`。若要列出所有可依名稱安裝的外掛程式，請執行 `bin/opensearch-plugin install --help`。維護於獨立儲存庫中的外掛程式（例如 `opensearch-jvector`）必須從下載的套件安裝。

下表列出常用的其他外掛程式，以及每個外掛程式最早可用的 OpenSearch 版本。

| 外掛程式名稱                                                                                                           | 最早可用版本               |
|:---|:---|
| `analysis-icu`                                                                                                           | 1.0.0                      |
| `analysis-kuromoji`                                                                                                      | 1.0.0                      |
| `analysis-nori`                                                                                                          | 1.0.0                      |
| [`analysis-phonenumber`]({{site.url}}{{site.baseurl}}/analyzers/supported-analyzers/phone-analyzers/)                  | 2.18.0                     |
| `analysis-phonetic`                                                                                                      | 1.0.0                      |
| `analysis-smartcn`                                                                                                       | 1.0.0                      |
| [`analysis-stempel`]({{site.url}}{{site.baseurl}}/analyzers/language-analyzers/polish/)                                                                                                       | 1.0.0                      |
| [`analysis-ukrainian`]({{site.url}}{{site.baseurl}}/analyzers/language-analyzers/ukrainian/)                                                                                                     | 1.0.0                      |
| `discovery-azure-classic`                                                                                                | 1.0.0                      |
| `discovery-ec2`                                                                                                          | 1.0.0                      |
| `discovery-gce`                                                                                                          | 1.0.0                      |
| [`ingest-attachment`]({{site.url}}{{site.baseurl}}/install-and-configure/additional-plugins/ingest-attachment-plugin/) | 1.0.0                      |
| `ingestion-kafka`                                                                                                         | 3.0.0                      |
| `ingestion-kinesis`                                                                                                       | 3.0.0                      |
| `mapper-annotated-text`                                                                                                  | 1.0.0                      |
| `mapper-murmur3`                                                                                                         | 1.0.0                      |
| [`mapper-size`]({{site.url}}{{site.baseurl}}/install-and-configure/additional-plugins/mapper-size-plugin/)             | 1.0.0                      |
| [`opensearch-jvector`]({{site.url}}{{site.baseurl}}/install-and-configure/additional-plugins/opensearch-jvector/)       | 3.5.0                      |
| `repository-azure`                                                                                                       | 1.0.0                      |
| `repository-gcs`                                                                                                         | 1.0.0                      |
| `repository-hdfs`                                                                                                        | 1.0.0                      |
| `repository-s3`                                                                                                          | 1.0.0                      |
| `store-smb`                                                                                                              | 1.0.0                      |
| `transport-grpc`                                                                                                         | 3.0.0                      |
| `workload-management` | 2.18.0 |

## 相關文件

- [管理 OpenSearch 外掛程式]({{site.url}}{{site.baseurl}}/install-and-configure/plugins/)
- [`ingest-attachment` 外掛程式]({{site.url}}{{site.baseurl}}/install-and-configure/additional-plugins/ingest-attachment-plugin/)
- [`mapper-size` 外掛程式]({{site.url}}{{site.baseurl}}/install-and-configure/additional-plugins/mapper-size-plugin/)
- [`opensearch-jvector` 外掛程式]({{site.url}}{{site.baseurl}}/install-and-configure/additional-plugins/opensearch-jvector/)
