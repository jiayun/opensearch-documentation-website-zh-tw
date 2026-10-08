---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "Ingest-attachment 外掛程式"
parent: Additional plugins
grand_parent: Managing OpenSearch plugins
nav_order: 20

---

# Ingest-attachment 外掛程式

`ingest-attachment` 外掛程式可讓 OpenSearch 使用 Apache 文字擷取程式庫 [Tika](https://tika.apache.org/)，從檔案中擷取內容及其他資訊。
支援的文件格式包括 PPT、PDF、RTF、ODF 等等。請參閱 Tika [支援的文件格式](https://tika.apache.org/3.2.2/formats.html)。

輸入欄位必須是 Base64 編碼的二進位資料。

## 安裝外掛程式

使用下列命令安裝 `ingest-attachment` 外掛程式：

```sh
./bin/opensearch-plugin install ingest-attachment
```

## Attachment 處理器選項

| 名稱 | 必要 | 預設 | 說明 |
| :--- | :--- | :--- | :--- |
| `field` | 是 | N/A | 用來取得 Base64 編碼二進位資料的欄位。 |
| `target_field` | 否 | Attachment | 儲存附件資訊的欄位。 |
| `properties` | 否 | 所有屬性 | 應儲存的屬性陣列。可以是 `content`、`language`、`date`、`title`、`author`、`keywords`、`content_type` 或 `content_length`。 |
| `indexed_chars` | 否 | `100_000` | 擷取時使用的字元數，用以避免欄位變得過大。使用 `-1` 表示不設限制。 |
| `indexed_chars_field` | 否 | `null` | 用來覆寫擷取時使用之字元數的欄位名稱，例如 `indexed_chars`。 |
| `ignore_missing` | 否 | `false` | 若為 `true`，當指定的欄位不存在時，處理器會直接結束，而不修改文件。 |

## 範例

下列步驟說明如何開始使用 `ingest-attachment` 外掛程式。

### 步驟 1：建立用來儲存附件的索引

下列命令會建立用來儲存附件的索引：

```json
PUT /example-attachment-index
{
  "mappings": {
    "properties": {}
  }
}
```

### 步驟 2：建立管線 

下列命令會建立包含 attachment 處理器的管線：

```json
PUT _ingest/pipeline/attachment
{
  "description" : "Extract attachment information",
  "processors" : [
    {
      "attachment" : {
        "field" : "data"
      }
    }
  ]
}
```

### 步驟 3：儲存附件

將附件轉換為 Base64 字串，以便將其作為 `data` 傳遞。
在此範例中，`base64` 命令會轉換檔案 `lorem.rtf`：

```sh
base64 lorem.rtf
```

或者，您也可以使用 Node.js 將檔案讀取為 `base64`，如下列命令所示：

```typescript
import * as fs from "node:fs/promises";
import path from "node:path";

const filePath = path.join(import.meta.dirname, "lorem.rtf");
const base64File = await fs.readFile(filePath, { encoding: "base64" });

console.log(base64File);
```

`.rtf` 檔案包含下列 Base64 文字：

`Lorem ipsum dolor sit amet`：
`e1xydGYxXGFuc2kNCkxvcmVtIGlwc3VtIGRvbG9yIHNpdCBhbWV0DQpccGFyIH0=`。

```json
PUT example-attachment-index/_doc/lorem_rtf?pipeline=attachment
{
  "data": "e1xydGYxXGFuc2kNCkxvcmVtIGlwc3VtIGRvbG9yIHNpdCBhbWV0DQpccGFyIH0="
}
```

### 查詢結果

附件處理完成後，您現在可以使用搜尋查詢來搜尋資料，如下列範例所示：

```json
POST example-attachment-index/_search
{
  "query": {
    "match": {
      "attachment.content": "ipsum"
    }
  }
}
```

OpenSearch 會傳回下列回應：

```json
{
  "took": 5,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 1,
      "relation": "eq"
    },
    "max_score": 1.1724279,
    "hits": [
      {
        "_index": "example-attachment-index",
        "_id": "lorem_rtf",
        "_score": 1.1724279,
        "_source": {
          "data": "e1xydGYxXGFuc2kNCkxvcmVtIGlwc3VtIGRvbG9yIHNpdCBhbWV0DQpccGFyIH0=",
          "attachment": {
            "content_type": "application/rtf",
            "language": "pt",
            "content": "Lorem ipsum dolor sit amet",
            "content_length": 28
          }
        }
      }
    ]
  }
}
```

## 擷取的資訊

使用此外掛程式可以擷取下列欄位：

- `content`
- `language`
- `date`
- `title`
- `author`
- `keywords`
- `content_type`
- `content_length`

若只要擷取這些欄位的子集，請在管線處理器的
`properties` 中定義這些欄位，如下列範例所示：

```json
PUT _ingest/pipeline/attachment
{
  "description" : "Extract attachment information",
  "processors" : [
    {
      "attachment" : {
        "field" : "data",
        "properties": ["content", "title", "author"]
      }
    }
  ]
}
```

## 限制擷取的內容

為了避免擷取過多字元而導致節點記憶體超載，預設限制為 `100_000`。
您可以使用設定 `indexed_chars` 變更此值。例如，您可以使用 `-1` 表示不限制字元數，但您必須確保 OpenSearch 節點上有足夠的 HEAP 空間，才能擷取大型文件的內容。

您也可以使用 `indexed_chars_field` 請求欄位，針對每份文件定義此限制。
若文件包含 `indexed_chars_field`，則會覆寫 `indexed_chars` 設定，如下列範例所示：

```json
PUT _ingest/pipeline/attachment
{
  "description" : "Extract attachment information",
  "processors" : [
    {
      "attachment" : {
        "field" : "data",
        "indexed_chars" : 10,
        "indexed_chars_field" : "max_chars",
      }
    }
  ]
}
```

設定好 attachment 管線後，您無須在請求中指定 `max_chars`，即可擷取預設的 `10` 個字元，如下列範例所示：

```json
PUT example-attachment-index/_doc/lorem_rtf?pipeline=attachment
{
  "data": "e1xydGYxXGFuc2kNCkxvcmVtIGlwc3VtIGRvbG9yIHNpdCBhbWV0DQpccGFyIH0="
}
```

或者，您也可以針對每份文件變更 `max_char`，以擷取最多 `15` 個字元，如下列範例所示：

```json
PUT example-attachment-index/_doc/lorem_rtf?pipeline=attachment
{
  "data": "e1xydGYxXGFuc2kNCkxvcmVtIGlwc3VtIGRvbG9yIHNpdCBhbWV0DQpccGFyIH0=",
  "max_chars": 15
}
```
