---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "編解碼器與處理器組合"
parent: Common use cases
nav_order: 10
---

# 編解碼器與處理器組合

在匯入時，[`s3` 來源]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/sources/s3/)所接收的資料可以由[編解碼器]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/sources/s3#codec)剖析。編解碼器會在資料透過 OpenSearch Data Prepper 管線[處理器]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/processors/processors/)匯入之前，以特定格式壓縮和解壓縮大型資料集。

雖然大多數編解碼器都可以搭配大多數處理器使用，但在處理下列輸入類型時，使用下列編解碼器與處理器組合可以讓您的管線更有效率。

## JSON 陣列

[JSON 陣列](https://json-schema.org/understanding-json-schema/reference/array)用於排列不同類型的元素。由於 JSON 中必須使用陣列，因此陣列中包含的資料必須是表格式資料。

JSON 陣列不需要處理器。

## NDJSON

與 JSON 陣列不同，[NDJSON](https://www.npmjs.com/package/ndjson) 允許以換行符號分隔每一列資料，也就是說，資料會逐行處理，而不是以陣列方式處理。

NDJSON 輸入類型會使用 [newline]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/sources/s3#newline-codec) 編解碼器剖析，該編解碼器會將每一行剖析為單一記錄事件。接著，[parse_json]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/processors/parse-json/) 處理器會將每一行輸出為單一事件。

## CSV

CSV 資料類型會以表格形式輸入資料。它可以不同時搭配編解碼器與處理器使用，但仍需要其中之一，例如只使用 `csv` 處理器，或只使用 `csv` 編解碼器。

搭配下列編解碼器與處理器組合使用時，CSV 輸入類型最有效率。

### `csv` 編解碼器

當 [`csv` 編解碼器]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/sources/s3#csv-codec)在不搭配處理器的情況下使用時，會自動偵測 CSV 中的標頭，並將其用於索引對應。

### `newline` 編解碼器

[`newline` 編解碼器]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/sources/s3#newline-codec)會將每一列剖析為單一記錄事件。只有在設定 `header_destination` 時，此編解碼器才會偵測標頭。接著，[`csv`]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/processors/csv/) 處理器會將事件輸出為多個欄。從 `newline` 編解碼器的 `header_destination` 中偵測到的標頭，可以在 `csv` 處理器的 `column_names_source_key.` 下使用。

## Parquet

[Apache Parquet](https://parquet.apache.org/docs/overview/) 是專為 Hadoop 打造的欄式儲存格式。設定管線時，您可以使用 Parquet 編解碼器，直接從 Amazon Simple Storage Service (Amazon S3) 物件讀取 Parquet 資料。這會從 Parquet 擷取所有資料。或者，您也可以使用 [S3 Select]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/sources/s3#using-s3_select-with-the-s3-source) 來取代編解碼器。在此情況下，[S3 Select]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/sources/s3#using-s3_select-with-the-s3-source) 會直接剖析 Parquet 檔案。如果您要篩選或載入部分資料，這種做法可能更有效率。

使用 [S3 Select]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/sources/s3#using-s3_select-with-the-s3-source) 時會產生額外的 S3 費用。
{: .note}

## Avro

[Apache Avro](https://avro.apache.org/docs) 是專為 Hadoop 打造的欄式儲存格式。不使用編解碼器時，其效率最高。搭配 [S3 Select]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/sources/s3#using-s3_select-with-the-s3-source) 使用時，Avro 可以透過選擇性擷取資料來提供優異的效能。

## `event_json`

`event_json` 輸出編解碼器會將事件資料和中繼資料轉換為 JSON 格式，以傳送至接收端 (sink)，例如 S3 接收端。`event_json` 輸入編解碼器會讀取事件及其中繼資料，以在 Data Prepper 中建立事件。
