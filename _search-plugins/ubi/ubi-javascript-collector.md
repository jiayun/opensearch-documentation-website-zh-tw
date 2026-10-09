---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "UBI JavaScript 收集器"
parent: User Behavior Insights
grand_parent: Optimizing search quality
has_children: false
nav_order: 10
---

# 如何使用 UBI JavaScript 收集器

UBI 隨附一個非常基本的 JavaScript 用戶端，可管理特定搜尋的 `query_id` 生命週期，並能建立 UBI 事件資料結構，為特定動作儲存這些結構。

如需結構描述的詳細資訊，請參閱 [UBI 索引結構描述]({{site.url}}{{site.baseurl}}/search-plugins/ubi/schemas/)。

我們建議將此用戶端做為起點，以滿足您的特定需求。

## 安裝

此用戶端是單一檔案（[ubi.js](https://github.com/opensearch-project/user-behavior-insights/tree/main/ubi-javascript-collector/ubi.js)），且僅相依於 `axios` 程式庫。  
<!-- vale off -->
從 [https://github.com/opensearch-project/user-behavior-insights/tree/main/ubi-javascript-collector/ubi.js](https://github.com/opensearch-project/user-behavior-insights/tree/main/ubi-javascript-collector/ubi.js) 下載。
<!-- vale on -->

若要參考事件並建立用戶端，請使用下列程式碼：

```js
import { UbiEvent } from './ubi';
import { UbiEventAttributes } from './ubi'
import { UbiClient } from './ubi'

const ubiClient = new  UbiClient('http://localhost:9200');
```
{% include copy.html %}


## 建立事件 

下列程式碼會追蹤在電子商務應用程式中將商品加入購物車的動作。它使用 `UbiEvent` 和 `UbiEventAttributes` 類別來封裝事件詳細資料，之後可將這些詳細資料傳送至追蹤系統：
```js
var event = new UbiEvent(
    'add_to_cart', 
    client_id, 
    session_id, 
    getQueryId(), 
    new UbiEventAttributes('product', item.primary_ean, item.title, item), 
    item.title + ' (' + item.id + ')'
);
```
{% include copy.html %}

### 參數

1. **事件名稱**： 
   - `'add_to_cart'` -- 此字串表示所追蹤的事件類型。

2. **用戶端 ID**： 
   - `client_id` -- 一個變數，用於保存用戶端的唯一識別碼。這有助於區分不同的使用者或工作階段。

3. **工作階段 ID**： 
   - `session_id` -- 一個變數，用於保存使用者工作階段的唯一識別碼。這用於追蹤特定工作階段內的使用者互動。

4. **查詢 ID**： 
   - `getQueryId()` -- 一個函式呼叫，用於擷取目前的查詢 ID，這可能代表特定的搜尋或互動情境。

5. **UbiEventAttributes**： 
   - 這是 `UbiEventAttributes` 類別的執行個體，用於封裝事件的額外詳細資料：
     - **類型**： 
       - `'product'` -- 指定屬性類型與產品相關。
     - **主要 EAN**： 
       - `item.primary_ean` -- 這是產品以 EAN 格式表示的唯一識別碼。
     - **標題**： 
       - `item.title` -- 產品名稱或描述。
     - **商品**： 
       - `item` -- 包含所有相關詳細資料的完整產品物件。

6. **事件標籤**： 
   - `item.title + ' (' + item.id + ')'` -- 這會為事件建立描述性標籤，其中包含產品標題及其唯一識別碼（ID）。

方法 `getQueryId()` 指的是會產生唯一查詢 ID（並將其儲存在工作階段中）的輔助方法。  
以下是範例方法：

```js
function generateQueryId(){
  const query_id = generateGuid();
  sessionStorage.setItem('query_id', query_id);
  return query_id;
}

function generateGuid() {
  let id = '';
  try{
    id = crypto.randomUUID();
  }
  catch(error){
    // crypto.randomUUID only works in https, not http context, so fallback.
    id ='10000000-1000-4000-8000-100000000000'.replace(/[018]/g, c =>
      (c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16)
    );
  }
  return id;
};
```
{% include copy.html %}

## 追蹤事件 

您可以呼叫 `trackEvent` 方法，將事件傳送至後端：

```js
ubiClient.trackEvent(event);
```


## 追蹤查詢

您可以選擇使用此用戶端追蹤查詢（而非使用 OpenSearch 的 UBI 外掛程式）。

程式碼與用於追蹤事件的程式碼類似：

```js
const query = new UbiQuery(APPLICATION, client_id, query_id, value, "_id", {});
ubiClient.trackQuery(query)
```
