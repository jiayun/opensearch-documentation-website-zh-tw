---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: corpora
parent: Anatomy of a workload
nav_order: 20
redirect_from:
  - /benchmark/workloads/corpora/
---

<!-- vale off -->
# corpora 元素
<!-- vale on -->

`corpora` 元素包含工作負載使用的所有文件語料庫。您可以複製並貼上任何語料庫定義，以便在不同工作負載之間使用文件語料庫。

## 範例

以下範例定義一個名為 `movies` 的語料庫，其中包含 `11658903` 份文件，未壓縮大小為 `1544799789` 位元組：

```json
  "corpora": [
    {
      "name": "movies",
      "documents": [
        {
          "source-file": "movies-documents.json",
          "document-count": 11658903, # Fetch document count from command line
          "uncompressed-bytes": 1544799789 # Fetch uncompressed bytes from command line
        }
      ]
    }
  ]
```

## 組態選項

請搭配 `corpora` 使用下列選項。

參數 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`name` | 是 | 字串 | 文件語料庫的名稱。由於 OpenSearch Benchmark 會在其目錄中使用此名稱，因此請僅使用不含空白字元的小寫名稱。
`documents` | 是 | JSON 陣列 | 文件檔案的陣列。
`meta` | 否 | 字串 | 由鍵值對組成的對應，包含語料庫的額外中繼資料。


`documents` 陣列中的每個項目包含下列選項。

參數 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`source-file` | 是 | 字串 | 包含工作負載對應文件的檔案名稱。在本機使用 OpenSearch Benchmark 時，文件包含在 JSON 檔案中。提供 `base_url` 時，請使用壓縮檔案格式：`.zip`、`.bz2`、`.gz`、`.tar`、`.tar.gz`、`.tgz` 或 `.tar.bz2`。壓縮檔案中必須有一個包含該名稱的 JSON 檔案。
`document-count` | 是 | 整數 | `source-file` 中的文件數量，用於決定哪些用戶端索引對應到文件語料庫的哪些部分。N 個用戶端中的每一個各接收文件語料庫的 N 分之一。使用包含父子關係文件的來源時，請指定父文件的數量。
`base-url` | 否 | 字串 | 指向根路徑的 http(s)、Amazon Simple Storage Service (Amazon S3) 或 Google Cloud Storage URL，OpenSearch Benchmark 可從該路徑取得對應的來源檔案。
`source-format` | 否 | 字串 | 定義 OpenSearch Benchmark 用來解譯 `source-file` 中所指定資料檔案的格式。僅支援 `bulk`。
`compressed-bytes` | 否 | 整數 | 壓縮來源檔案的大小（以位元組為單位），表示 OpenSearch Benchmark 要下載的資料量。
`uncompressed-bytes` | 否 | 整數 | 來源檔案解壓縮後的大小（以位元組為單位），表示解壓縮後的來源檔案所需的磁碟空間。
`target-index` | 否 | 字串 | 定義 `bulk` 操作應作為目標的索引名稱。當 `indices` 元素中只定義一個索引時，OpenSearch Benchmark 會自動推導此值。當 `includes-action-and-meta-data` 設定為 `true` 時，會忽略 `target-index` 的值。
`target-type` | 否 | 字串 | 定義大量操作中目標索引的文件類型。當 `indices` 元素中只定義一個索引，且該索引只有一個類型時，OpenSearch Benchmark 會自動推導此值。當 `includes-action-and-meta-data` 設定為 `true` 時，會忽略 `target-type` 的值。
`includes-action-and-meta-data` | 否 | 布林值 | 設為 `true` 時，表示文件的檔案已包含 `action` 行和 `meta-data` 行。設為 `false` 時，表示文件的檔案僅包含文件。預設為 `false`。
`meta` | 否 | 字串 | 由鍵值對組成的對應，包含語料庫的額外中繼資料。 

