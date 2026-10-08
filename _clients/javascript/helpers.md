---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "輔助方法"
parent: JavaScript client
nav_order: 2
---

# JavaScript 輔助方法

JavaScript 輔助方法可簡化複雜的 API 任務。如需完整的輔助方法文件，請參閱 [`opensearch-js` 指南](https://github.com/opensearch-project/opensearch-js/tree/main/guides)。

## 批次輔助方法

批次輔助方法可簡化複雜的批次 API 請求。它會將資料來源中的文件分成多個批次，將每個批次傳送至 Bulk API，並重試失敗的操作。由於 `onDocument` 函式會傳回每份文件的操作，因此一次呼叫即可結合 `index`、`create`、`update` 和 `delete` 操作。若要傳送您自行建構的批次請求本文，請使用 `client.bulk` 方法。如需詳細資訊，請參閱[批次指南](https://github.com/opensearch-project/opensearch-js/blob/main/guides/bulk.md)。

### 使用方式

下列程式碼會建立批次輔助方法執行個體：

```javascript
const { Client } = require('@opensearch-project/opensearch')
const documents = require('./docs.json')

const client = new Client({ ... })

const result = await client.helpers.bulk({
  datasource: documents,
  onDocument (doc) {
    return {
      index: { _index: 'example-index' }
    }
  }
})

console.log(result)
```
{% include copy.html %}

批次輔助方法操作會傳回包含下列欄位的物件：

```json
{
  total: number,
  failed: number,
  retry: number,
  successful: number,
  noop: number,
  time: number,
  bytes: number,
  aborted: boolean
}
```

### 批次輔助方法組態選項

建立新的批次輔助方法執行個體時，您可以使用下列組態選項。

| 選項 | 資料類型 | 必要／預設 | 說明 
| :--- | :--- | :--- | :---
| `datasource` | 陣列、非同步產生器，或由字串或物件組成的可讀取串流 | 必要 | 代表您需要建立、刪除、編製索引或更新的文件。 
| `onDocument` | 函式 | 必要 | 針對指定 `datasource` 中的每份文件呼叫的函式。它會傳回要對此文件執行的操作。您也可以選擇將新文件作為函式結果的一部分傳回，以便在 `create` 和 `index` 操作中修改文件。
| `concurrency` | 整數 | 選用。預設為 5。 | 要平行執行的請求數量。 
| `flushBytes` | 整數 |  選用。預設為 5,000,000。 | 要傳送的批次本文大小上限，以位元組為單位。
| `flushInterval` | 整數 |  選用。預設為 30,000。 | 讀取最後一份文件後，在送出本文之前等待的時間，以毫秒為單位。
| `onDrop` | 函式 | 選用。預設為 `noop`。 | 針對達到重試次數上限後仍無法編製索引的每份文件呼叫的函式。 
| `refreshOnCompletion` | 布林值或字串 | 選用。預設為 `false`。 | 是否應在批次操作結束時執行重新整理。設為 `true` 可重新整理所有索引，或設為索引名稱以僅重新整理該索引。 
| `retries` | 整數 |  選用。預設為用戶端的  `maxRetries` 值。 | 在針對該文件呼叫 `onDrop` 之前，重試操作的次數。
| `wait` | 整數 |  選用。預設為 5,000。 | 重試操作之前等待的時間，以毫秒為單位。

### 範例

下列範例說明編製索引、建立、更新及刪除的批次輔助方法操作。如需詳細資訊及進階索引動作，請參閱 GitHub 中的 [`opensearch-js` 指南](https://github.com/opensearch-project/opensearch-js/tree/main/guides)。  

#### 編製索引

編製索引操作會在文件不存在時建立新文件，並在文件已存在時重新建立文件。

下列批次操作會將文件編製索引至 `example-index`：

```javascript
client.helpers.bulk({
  datasource: arrayOfDocuments,
  onDocument (doc) {
    return {
      index: { _index: 'example-index' }
    }
  }
})
```
{% include copy.html %}

下列批次操作會將文件編製索引至 `example-index`，並覆寫文件：

```javascript
client.helpers.bulk({
  datasource: arrayOfDocuments,
  onDocument (doc) {
    return [
      {
        index: { _index: 'example-index' }
      },
      { ...doc, createdAt: new Date().toISOString() }
    ]
  }
})
```
{% include copy.html %}

#### 建立

建立操作只會在文件尚未存在時建立新文件。

下列批次操作會在 `example-index` 中建立文件：

```javascript
client.helpers.bulk({
  datasource: arrayOfDocuments,
  onDocument (doc) {
    return {
      create: { _index: 'example-index', _id: doc.id }
    }
  }
})
```
{% include copy.html %}

下列批次操作會在 `example-index` 中建立文件，並覆寫文件：

```javascript
client.helpers.bulk({
  datasource: arrayOfDocuments,
  onDocument (doc) {
    return [
      {
        create: { _index: 'example-index', _id: doc.id }
      },
      { ...doc, createdAt: new Date().toISOString() }
    ]
  }
})
```
{% include copy.html %}

#### 更新

更新操作會使用傳送的欄位更新文件。文件必須已存在於索引中。

下列批次操作會更新 `example-index` 中的文件：

```javascript
client.helpers.bulk({
  datasource: arrayOfDocuments,
  onDocument (doc) {
    // The update operation always requires a tuple to be returned, with the
    // first element being the action and the second being the update options.
    return [
      {
        update: { _index: 'example-index', _id: doc.id }
      },
      { doc_as_upsert: true }
    ]
  }
})
```
{% include copy.html %}

下列批次操作會更新 `example-index` 中的文件，並覆寫文件：

```javascript
client.helpers.bulk({
  datasource: arrayOfDocuments,
  onDocument (doc) {
    return [
      {
        update: { _index: 'example-index', _id: doc.id }
      },
      {
        doc: { ...doc, createdAt: new Date().toISOString() },
        doc_as_upsert: true
      }
    ]
  }
})
```
{% include copy.html %}

#### 刪除

刪除操作會刪除文件。

下列批次操作會從 `example-index` 中刪除文件：

```javascript
client.helpers.bulk({
  datasource: arrayOfDocuments,
  onDocument (doc) {
    return {
      delete: { _index: 'example-index', _id: doc.id }
    }
  }
})
```
{% include copy.html %}

## 相關文件

- 如需更多輔助方法文件，例如編製索引和多重搜尋的文件，請參閱 [`opensearch-js` 指南](https://github.com/opensearch-project/opensearch-js/tree/main/guides)。
- 如需完整的範例應用程式，請參閱 [`opensearch-js` 範例](https://github.com/opensearch-project/opensearch-js/tree/main/samples)。
