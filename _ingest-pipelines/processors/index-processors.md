---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "資料匯入處理器"
nav_order: 80
has_children: true
has_toc: false
redirect_from:
   - /api-reference/ingest-apis/ingest-processors/
---

# 資料匯入處理器

資料匯入處理器是[資料匯入管線]({{site.url}}{{site.baseurl}}/ingest-pipelines/index/)的核心元件。它們會在編製索引之前先對文件進行前置處理。例如，您可以移除欄位、從文字中擷取值、轉換資料格式，或附加額外資訊。

OpenSearch 在您的 OpenSearch 安裝中提供一組標準的[資料匯入處理器](#supported-processors)。若要取得 OpenSearch 中可用處理器的清單，請使用 [Nodes Info]({{site.url}}{{site.baseurl}}/api-reference/nodes-apis/nodes-info/) API 操作：

```json
GET /_nodes/ingest?filter_path=nodes.*.ingest.processors
```
{% include copy-curl.html %}

若要設定與部署資料匯入處理器，請確認您具備必要的權限與存取權限。如需更多資訊，請參閱 [API 權限]({{site.url}}{{site.baseurl}}/security/access-control/api/)。
{:.note}

## 支援的處理器

處理器類型及其必要或選用參數會依您的特定使用情境而有所不同。OpenSearch 支援下列資料匯入處理器。若要取得在 OpenSearch 管線中使用這些處理器的教學，請前往各處理器的對應文件。

處理器類型 | 說明
:--- | :--- 
`append` | 在文件的欄位中新增一或多個值。
`bytes` | 將人類可讀的位元組值轉換為以位元組為單位的數值。
`community_id` | 為網路流量元組產生 community ID 流量雜湊演算法。
`convert` | 變更文件中欄位的資料類型。
`copy` | 將現有欄位中的整個物件複製到另一個欄位。
`csv` | 擷取 CSV 並將其儲存為文件中的個別欄位。
`date` | 從欄位解析日期，然後使用該日期或時間戳記作為文件的時間戳記。
`date_index_name` | 根據文件中的日期或時間戳記欄位，將文件編製索引至以時間為基礎的索引。
`dissect` | 使用定義的模式從文字欄位中擷取結構化欄位。
`dot_expander` | 將含點號的欄位展開為物件欄位。
`drop` | 捨棄文件，不編製索引也不引發任何錯誤。
`fail` | 引發例外狀況並停止管線的執行。
`fingerprint` | 為文件中指定的特定欄位或所有欄位產生雜湊值。
`foreach` | 允許對文件中陣列或物件欄位的每個元素套用另一個處理器。
`geoip` | 新增 IP 地址的地理位置資訊。
`geojson-feature` | 將 GeoJSON 資料編製索引至地理空間欄位。
`grok` | 使用模式比對來解析並結構化非結構化資料。
`gsub` | 取代或刪除文件字串欄位中的子字串。
`html_strip` | 從文字欄位移除 HTML 標籤並傳回純文字內容。
`ip2geo` | 新增 IPv4 或 IPv6 地址的地理位置資訊。
`join` | 使用分隔字元將陣列的每個元素串接成單一字串。
`json` | 將 JSON 字串轉換為結構化的 JSON 物件。
`kv` | 自動解析欄位中的鍵值對。
`lowercase` | 將特定欄位中的文字轉換為小寫字母。
`pipeline` | 執行內部管線。
`remove` | 從文件中移除欄位。
`remove_by_pattern` | 依欄位模式從文件中移除欄位。
`rename` | 重新命名現有欄位。
`script` | 對傳入的文件執行內嵌或已儲存的指令碼。
`set` | 將欄位的值設定為指定的值。
`sort` | 以遞增或遞減順序排序陣列的元素。
`sparse_encoding` | 使用稀疏檢索為神經稀疏搜尋從文字欄位產生稀疏向量/詞元及其權重。
`split` | 使用分隔字元將欄位分割為陣列。
`text_chunking` | 將長文件分割為較小的區塊。
`text_embedding` | 從文字欄位產生向量嵌入以進行語意搜尋。
`text_image_embedding` | 從文字與影像欄位產生組合向量嵌入，以進行多模態神經搜尋。
`trim` | 移除字串欄位的開頭與結尾空白。
`uppercase` | 將特定欄位中的文字轉換為大寫字母。
`urldecode` | 解碼 URL 編碼格式的字串。
`user_agent` | 從瀏覽器隨網路請求傳送的使用者代理程式資訊中擷取詳細資料。

## 處理器數量限制設定

您可以使用叢集設定 `cluster.ingest.max_number_processors` 來限制資料匯入處理器的數量。處理器總數包含處理器的數量以及 [`on_failure`]({{site.url}}{{site.baseurl}}/ingest-pipelines/pipeline-failures/) 處理器的數量。

`cluster.ingest.max_number_processors` 的預設值為 `Integer.MAX_VALUE`。若新增的處理器數量超過 `cluster.ingest.max_number_processors` 中設定的值，將會擲回 `IllegalStateException`。

## 支援批次處理的處理器

某些處理器支援批次匯入——它們可以批次方式同時處理多份文件。這些支援批次處理的處理器在使用批次處理時通常能提供更好的效能。若要進行批次處理，請使用 [Bulk API]({{site.url}}{{site.baseurl}}/api-reference/document-apis/bulk/) 並提供 `batch_size` 參數。所有支援批次處理的處理器都具有批次模式與單一文件模式。當您使用 `PUT` 方法匯入文件時，處理器會以單一文件模式運作，並依序處理文件。只有 `text_embedding` 與 `sparse_encoding` 處理器支援批次處理。所有其他處理器一次只處理一份文件。

## 選擇性啟用處理器

由 [ingest-common 模組](https://github.com/opensearch-project/OpenSearch/blob/2.x/modules/ingest-common/src/main/java/org/opensearch/ingest/common/IngestCommonPlugin.java)定義的處理器，可以透過提供 `ingest-common.processors.allowed` 叢集設定來選擇性啟用。若未提供，則預設會啟用所有處理器。指定空清單會停用所有處理器。若變更設定以移除先前啟用的處理器，則任何使用已停用處理器的管線，在節點重新啟動且新設定生效後將會失敗。
