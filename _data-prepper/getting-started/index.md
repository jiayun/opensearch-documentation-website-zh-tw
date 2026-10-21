---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "入門"
nav_order: 5
has_children: true
has_toc: false
redirect_from:
  - /clients/data-prepper/get-started/
  - /data-prepper/getting-started/
steps:
- heading: 安裝並設定 Data Prepper
  description: 使用 Docker 映像檔或 Linux 壓縮檔安裝 Data Prepper，並了解其設定方式。
  link: /data-prepper/getting-started/installing/
- heading: 設定管線
  description: 了解管線結構，以及伺服器與記錄組態檔。
  link: /data-prepper/getting-started/configuring-pipelines/
- heading: 執行 Data Prepper
  description: 使用最小管線啟動 Data Prepper、傳送測試事件，然後停止 Data Prepper。
  link: /data-prepper/getting-started/running/
- heading: 將記錄資料匯入 OpenSearch
  description: 建立管線，剖析原始 Apache 存取記錄、將其寫入 OpenSearch 索引，並讓您搜尋剖析後的欄位。
  link: /data-prepper/getting-started/ingesting-log-data/
---

# OpenSearch Data Prepper 入門

OpenSearch Data Prepper 是伺服器端的資料收集器，可接收來自應用程式的資料、轉換資料，並傳送至 OpenSearch。Data Prepper 與 OpenSearch 分開執行，且未包含在 OpenSearch 安裝套件中。

## 管線與事件

Data Prepper 會執行_管線_。每條管線會從_來源_讀取資料，使用一或多個_處理器_轉換或捨棄事件，並將結果寫入一或多個_接收端_。在來源與處理器之間，事件會先在_緩衝區_中等待。例如，管線可以透過 HTTP 接收記錄行、將每一行剖析為欄位，並將結果寫入 OpenSearch 索引。單一 Data Prepper 執行個體可以執行多條管線。

_事件_是通過管線的單一資料項目，例如一行記錄。每個事件由稱為_欄位_的鍵值對組成，類似 JSON 物件。當管線寫入 OpenSearch 時，每個事件會成為一份文件。其他接收端（例如 Amazon S3）會將事件序列化為檔案。處理器會在事件抵達接收端之前，讀取並修改每個事件的欄位。

## 組態檔

Data Prepper 使用下列組態檔。

| 檔案 | 必要 | 說明 |
| :--- | :--- | :--- |
| 管線組態 | 是 | 一或多個 YAML 檔案，用於定義要執行的管線，包括其來源、處理器與接收端。Data Prepper 不提供預設管線，且若沒有管線組態檔就不會啟動。如需詳細資訊，請參閱[設定管線]({{site.url}}{{site.baseurl}}/data-prepper/getting-started/configuring-pipelines/)。 |
| `data-prepper-config.yaml` | 否 | Data Prepper 伺服器的設定，例如連接埠、TLS，以及[核心 API]({{site.url}}{{site.baseurl}}/data-prepper/managing-data-prepper/core-apis/) 的驗證。Data Prepper 包含預設的伺服器組態檔。 |
| `log4j2-rolling.properties` | 否 | [Log4j 2](https://logging.apache.org/log4j/2.x/) 記錄組態。Data Prepper 包含預設的記錄組態檔。 |

由於必須有管線，因此您必須在啟動 Data Prepper 之前至少定義一條管線。

## 後續步驟

若要開始使用 Data Prepper，請依序執行下列步驟：

{% include list.html list_items=page.steps %}
