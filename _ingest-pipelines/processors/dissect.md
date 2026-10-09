---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Dissect
parent: Ingest processors
nav_order: 60
---

本文件說明如何在 OpenSearch 資料匯入管線中使用 `dissect` 處理器。如果您的使用情境涉及大型或複雜的資料集，請考慮使用在 OpenSearch 叢集上執行的 [Data Prepper `dissect` 處理器]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/processors/dissect/)。
{: .note}

# Dissect

`dissect` 處理器會從文件文字欄位中擷取值，並根據 dissect 模式將它們對應到個別欄位。此處理器非常適合從具有已知結構的記錄訊息中擷取欄位。與 `grok` 處理器不同，`dissect` 不使用正規表示式，且語法更簡單。

## 語法

以下是 `dissect` 處理器的語法：

```json
{
  "dissect": {
    "field": "source_field",
    "pattern": "%{dissect_pattern}"
  }
}
```
{% include copy.html %}


## 組態參數

下表列出 `dissect` 處理器的必要與選用參數。

參數 | 必要／選用 | 說明 |
|-----------|-----------|-----------|
`field`  | 必要  | 包含要剖析之資料的欄位名稱。 |
`pattern` | 必要 | 用於從指定欄位擷取資料的 dissect 模式。 |
`append_separator` | 選用 | 分隔附加欄位的分隔字元或字串。預設為 `""`（空字串）。
`description`  | 選用  | 處理器的簡要描述。  |
`if` | 選用 | 執行處理器的條件。 |
`ignore_failure` | 選用 | 指定處理器即使遇到錯誤也繼續執行。若設為 `true`，則會忽略處理器失敗。預設為 `false`。 |
`ignore_missing`  | 選用  | 指定處理器是否應忽略不含指定欄位的文件。若設為 `true`，當欄位不存在或為 `null` 時，處理器不會修改文件。預設為 `false`。 |
`on_failure` | 選用 | 處理器失敗時要執行的處理器清單。 |
`tag` | 選用 | 處理器的識別標籤。在除錯時有助於區分相同類型的處理器。 |

## 使用處理器

依照下列步驟在管線中使用處理器。

**步驟 1：建立管線**

下列查詢會建立名為 `dissect-test` 的管線，使用 `dissect` 處理器來剖析記錄行：

```json
PUT /_ingest/pipeline/dissect-test
{
  "description": "Pipeline that dissects web server logs",
  "processors": [
    {
      "dissect": {
        "field": "message",
        "pattern": "%{client_ip} - - [%{timestamp}] \"%{http_method} %{url} %{http_version}\" %{response_code} %{response_size}" 
      }
    }
  ]
}
```
{% include copy-curl.html %}

**步驟 2 (選用)：測試管線**

建議您在匯入文件之前先測試管線。
{: .tip}

若要測試管線，請執行下列查詢：

```json
POST _ingest/pipeline/dissect-test/_simulate
{
  "docs": [
    {
      "_index": "testindex1",
      "_id": "1",
      "_source": {
        "message": "192.168.1.10 - - [03/Nov/2023:15:20:45 +0000] \"POST /login HTTP/1.1\" 200 3456"
      }
    }
  ]
}
```
{% include copy-curl.html %}

**回應**

下列範例回應確認管線如預期運作：

```json
{
  "docs": [
    {
      "doc": {
        "_index": "testindex1",
        "_id": "1",
        "_source": {
          "response_code": "200",
          "http_method": "POST",
          "http_version": "HTTP/1.1",
          "client_ip": "192.168.1.10",
          "message": """192.168.1.10 - - [03/Nov/2023:15:20:45 +0000] "POST /login HTTP/1.1" 200 3456""",
          "url": "/login",
          "response_size": "3456",
          "timestamp": "03/Nov/2023:15:20:45 +0000"
        },
        "_ingest": {
          "timestamp": "2023-11-03T22:28:32.830244044Z"
        }
      }
    }
  ]
}
```

**步驟 3：匯入文件**

下列查詢會將文件匯入名為 `testindex1` 的索引：

```json
PUT testindex1/_doc/1?pipeline=dissect-test
{
   "message": "192.168.1.10 - - [03/Nov/2023:15:20:45 +0000] \"POST /login HTTP/1.1\" 200 3456"
}
```
{% include copy-curl.html %}

**步驟 4 (選用)：擷取文件**

若要擷取文件，請執行下列查詢：

```json
GET testindex1/_doc/1
```
{% include copy-curl.html %}

## Dissect 模式

Dissect 模式是一種告訴 `dissect` 處理器如何將字串剖析為結構化格式的方法。此模式由您想要捨棄的字串部分定義。例如，`%{client_ip} - - [%{timestamp}]` dissect 模式會將字串 `"192.168.1.10 - - [03/Nov/2023:15:20:45 +0000] \"POST /login HTTP/1.1\" 200 3456"` 剖析為下列欄位：

```json
client_ip: "192.168.1.1"
@timestamp: "03/Nov/2023:15:20:45 +0000"
```

Dissect 模式的運作方式是將字串與一組規則進行比對。例如，第一條規則會捨棄單一空格。`dissect` 處理器會找到這個空格，然後將 `client_ip` 的值指派給該空格之前的所有字元。下一條規則會比對 `[` 與 `]` 字元，然後將 `@timestamp` 的值指派給兩者之間的所有內容。

### 建構成功的 dissect 模式

在建構 dissect 模式時，請務必注意您想要捨棄的字串部分。如果您捨棄的字串過多，`dissect` 處理器可能無法成功剖析剩餘的資料。反之，如果您捨棄的字串不足，處理器可能會建立不必要的欄位。

如果模式中定義的任何 `%{keyname}` 沒有值，則會擲回例外狀況。您可以透過在 `on_failure` 參數中提供錯誤處理步驟來處理此例外狀況。

### 空鍵與具名略過鍵

空鍵 `%{}` 或[具名略過鍵](#named-skip-key-modifier)可用於比對值，但將該值從最終文件中排除。如果您想要剖析字串但不需要儲存其所有部分，這會很有用。

### 將比對到的值轉換為非字串資料類型

預設情況下，所有比對到的值都以字串資料類型表示。如果您需要將值轉換為不同的資料類型，可以使用 [`convert` 處理器]({{site.url}}{{site.baseurl}}/ingest-pipelines/processors/convert/)。

### 鍵修飾詞 

`dissect` 處理器支援可變更處理器預設行為的鍵修飾詞。這些修飾詞一律位於 `%{keyname}` 的左側或右側，且一律以 `%{}` 括住。例如，`%{+keyname->}` 修飾詞包含附加與右側填補修飾詞。鍵修飾詞可用於將多個欄位合併為單行輸出、建立格式化的資料項目清單，或彙總來自多個來源的值。  

下表列出 `dissect` 處理器的主要修飾詞。

修飾詞 | 名稱 | 位置 | 範例 | 說明 |
|-----------|-----------|-----------|
`->` | 略過右側填補 | （最）右側 | `%{keyname->}` | 告訴 `dissect` 處理器略過右側任何重複的字元。例如，`%{timestamp->}` 可用來告訴處理器略過 `timestamp` 之後的任何填補字元，例如兩個連續空格或任何變動的字元填補。 |
`+` | 附加 | 左側 | `%{keyname} %{+keyname}` | 附加兩個或多個欄位。 | 
`+` 與 `/n` | 依指定順序附加 | 左側與右側 | `%{+keyname}/2 %{+keyname/1}` | 以指定順序附加兩個或多個欄位。 |
`?` | 具名略過鍵 | 左側 | `%{?skipme}` | 在輸出中略過比對到的值。行為與 `%{}` 相同。 |
`*` 與 `&` | 參考鍵 | 左側 | `%{*r1} %{&r1}` | 將 `*` 擷取的值用作輸出鍵，並將 `&` 擷取的值用作輸出值。 |

各鍵修飾詞的詳細說明與使用範例將於下列章節提供。

### 右側填補修飾詞 (`->`)

分割演算法相當精確，要求模式中的每個字元都必須與來源字串完全相符。舉例來說，模式 `%{hellokey} %{worldkey}` (1 個空格) 會符合字串 `Hello world` (1 個空格)，但不會符合字串 <code>Hello&nbsp;&nbsp;world</code> (2 個空格)，因為模式中只有 1 個空格，而來源字串有 2 個。

_右側填補修飾詞_ 可用來解決這個問題。將右側填補修飾詞加入模式 `%{helloworldkey->} %{worldkey}` 後，它會符合 <code>Hello&nbsp;world</code> (1 個空格)、<code>Hello&nbsp;&nbsp;world</code> (2 個空格)，甚至 <code>Hello&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;world</code> (10 個空格)。

右側填補修飾詞可用來允許 `%{keyname->}` 之後的字元重複。右側填補修飾詞可套用至任何鍵，並可搭配任何其他修飾詞。它一律應放在最右側，例如 `%{+keyname/1->}` 或 `%{}`。

#### 使用範例

以下範例說明如何使用右側填補修飾詞：

`%{city->}, %{state} %{zip}`

在此模式中，右側填補修飾詞 `->` 會套用至 `%{city}` 鍵。這兩個地址包含相同的資訊，但第二筆項目的 `city` 欄位中多了一個字 `City`。右側填補修飾詞可讓模式同時符合這兩筆地址項目，即使它們的格式略有不同：

```bash
New York, NY 10017
New York City, NY 10017
```

以下範例管線使用右側填補修飾詞搭配空鍵 `%{->}`：

```json
PUT /_ingest/pipeline/dissect-test
{
  "description": "Pipeline that dissects web server logs",
  "processors": [
    {
      "dissect": {
        "field": "message",
        "pattern": "[%{client_ip}]%{->}[%{timestamp}]" 
      }
    }
  ]
}
```
{% include copy-curl.html %}

您可以使用以下範例管線來測試此管線：

```json
POST _ingest/pipeline/dissect-test/_simulate
{
  "docs": [
    {
      "_index": "testindex1",
      "_id": "1",
      "_source": {
        "message": "[192.168.1.10]   [03/Nov/2023:15:20:45 +0000]"
      }
    }
  ]
}
```
{% include copy-curl.html %}

您的回應應類似於以下內容：

```json
{
  "docs": [
    {
      "doc": {
        "_index": "testindex1",
        "_id": "1",
        "_source": {
          "client_ip": "192.168.1.10",
          "message": "[192.168.1.10]   [03/Nov/2023:15:20:45 +0000]",
          "timestamp": "03/Nov/2023:15:20:45 +0000"
        },
        "_ingest": {
          "timestamp": "2024-01-22T22:55:42.090569297Z"
        }
      }
    }
  ]
}
```
{% include copy-curl.html %}

### 附加修飾詞 (`+`)

_附加修飾詞_ 會將兩個或多個值合併為單一輸出值。這些值會由左至右附加。您也可以指定選用的分隔符號，插入於這些值之間。

#### 使用範例

以下範例管線使用附加修飾詞：

```json
PUT /_ingest/pipeline/dissect-test
{
  "description": "Pipeline that dissects web server logs",
  "processors": [
    {
      "dissect": {
        "field": "message",
        "pattern": "%{+address}, %{+address} %{+address}",
        "append_separator": "|"
      }
    }
  ]
}
```
{% include copy-curl.html %}

您可以使用以下範例管線來測試此管線：

```json
POST _ingest/pipeline/dissect-test/_simulate
{
  "docs": [
    {
      "_index": "testindex1",
      "_id": "1",
      "_source": {
        "message": "New York, NY 10017"
      }
    }
  ]
}
```
{% include copy-curl.html %}

這些子字串會附加至 `address` 欄位，如下列回應所示：

```json
{
  "docs": [
    {
      "doc": {
        "_index": "testindex1",
        "_id": "1",
        "_source": {
          "address": "New York|NY|10017",
          "message": "New York, NY 10017"
        },
        "_ingest": {
          "timestamp": "2024-01-22T22:30:54.516284637Z"
        }
      }
    }
  ]
}
```
{% include copy-curl.html %}

### 附加並指定順序修飾詞 (`+` 和 `/n`)

_附加並指定順序修飾詞_ 會依據 `/` 之後指定的順序，將兩個或多個鍵的值合併為單一輸出值。您可以靈活自訂分隔附加值的分隔符號。附加修飾詞適合用來將多個欄位彙整為單一格式化輸出行、建構結構化的資料項目清單，以及合併來自各種來源的值。

#### 使用範例

以下範例管線使用附加並指定順序修飾詞，將前一個管線中定義的模式順序反轉。此管線指定了要插入於附加欄位之間的分隔符號。如果您未指定分隔符號，所有值將會在沒有分隔符號的情況下附加。

```json
PUT /_ingest/pipeline/dissect-test
{
  "description": "Pipeline that dissects web server logs",
  "processors": [
    {
      "dissect": {
        "field": "message",
        "pattern": "%{+address/3}, %{+address/2} %{+address/1}",
        "append_separator": "|"
      }
    }
  ]
}
```
{% include copy-curl.html %}

您可以使用以下範例管線來測試此管線：

```json
POST _ingest/pipeline/dissect-test/_simulate
{
  "docs": [
    {
      "_index": "testindex1",
      "_id": "1",
      "_source": {
        "message": "New York, NY 10017"
      }
    }
  ]
}
```
{% include copy-curl.html %}

這些子字串會以反向順序附加至 `address` 欄位，如下列回應所示：

```json
{
  "docs": [
    {
      "doc": {
        "_index": "testindex1",
        "_id": "1",
        "_source": {
          "address": "10017|NY|New York",
          "message": "New York, NY 10017"
        },
        "_ingest": {
          "timestamp": "2024-01-22T22:38:24.305974178Z"
        }
      }
    }
  ]
}
```
{% include copy-curl.html %}

### 具名略過鍵修飾詞

_具名略過鍵修飾詞_ 會使用模式中的空鍵 `{}` 或 `?` 修飾詞，將特定相符項目排除於最終輸出之外。舉例來說，下列模式是等效的：`%{firstName} %{lastName} %{?ignore}` 和 `%{firstName} %{lastName} %{}`。具名略過鍵修飾詞適合用來將不相關或不必要的欄位排除於輸出之外。

#### 使用範例

下列模式使用具名略過鍵，將某個欄位 (在此例中為 `ignore`) 排除於輸出之外。您可以為空鍵指派描述性名稱，例如 `%{?ignore}`，以清楚表示對應的值應排除於最終輸出之外：

```json
PUT /_ingest/pipeline/dissect-test
{
  "description": "Pipeline that dissects web server logs",
  "processors": [
    {
      "dissect": {
        "field": "message",
        "pattern": "%{firstName} %{lastName} %{?ignore}"
      }
    }
  ]
}
```
{% include copy-curl.html %}

您可以使用以下範例管線來測試此管線：

```json
POST _ingest/pipeline/dissect-test/_simulate
{
  "docs": [
    {
      "_index": "testindex1",
      "_id": "1",
      "_source": {
        "message": "John Doe M.D."
      }
    }
  ]
}
```
{% include copy-curl.html %}

您的回應應類似於以下內容：

```json
{
  "docs": [
    {
      "doc": {
        "_index": "testindex1",
        "_id": "1",
        "_source": {
          "firstName": "John",
          "lastName": "Doe",
          "message": "John Doe M.D."
        },
        "_ingest": {
          "timestamp": "2024-01-22T22:41:58.161475555Z"
        }
      }
    }
  ]
}
```
{% include copy-curl.html %}

### 參考鍵 (`*` 與 `&`)

參考鍵將剖析後的值用作結構化內容的鍵值配對。當處理以鍵值對形式部分記錄資料的系統時，這會很有用。透過使用參考鍵，您可以保留鍵值關係並維持所擷取資訊的完整性。

#### 使用範例

下列模式使用參考鍵將資料擷取為結構化格式。在此範例中，模式會擷取 `client_ip`，並從後續內容擷取兩組鍵值對：

```json
PUT /_ingest/pipeline/dissect-test
{
  "description": "Pipeline that dissects web server logs",
  "processors": [
    {
      "dissect": {
        "field": "message",
        "pattern": "%{client_ip} %{*a}:%{&a} %{*b}:%{&b}"
      }
    }
  ]
}
```
{% include copy-curl.html %}

您可以使用下列範例管線來測試此管線：

```json
POST _ingest/pipeline/dissect-test/_simulate
{
  "docs": [
    {
      "_index": "testindex1",
      "_id": "1",
      "_source": {
        "message": "192.168.1.10 response_code:200 response_size:3456"
      }
    }
  ]
}
```
{% include copy-curl.html %}

兩個鍵值對已被擷取至欄位中，如下列回應所示：

```json
{
  "docs": [
    {
      "doc": {
        "_index": "testindex1",
        "_id": "1",
        "_source": {
          "client_ip": "192.168.1.10",
          "response_code": "200",
          "message": "192.168.1.10 response_code:200 response_size:3456",
          "response_size": "3456"
        },
        "_ingest": {
          "timestamp": "2024-01-22T22:48:51.475535635Z"
        }
      }
    }
  ]
}
```
{% include copy-curl.html %}
