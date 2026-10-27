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

資料匯入處理器是[資料匯入管線]({{site.url}}{{site.baseurl}}/ingest-pipelines/index/)的核心元件。它們會在編製索引前預先處理文件。例如，您可以移除欄位、從文字中擷取值、轉換資料格式，或附加額外資訊。

OpenSearch 在您的 OpenSearch 安裝中提供一組標準的[資料匯入處理器](#supported-processors)。若要列出 OpenSearch 中可用的處理器，請使用 [Nodes Info]({{site.url}}{{site.baseurl}}/api-reference/nodes-apis/nodes-info/) API 操作：

```json
GET /_nodes/ingest?filter_path=nodes.*.ingest.processors
```
{% include copy-curl.html %}

管線中的每個處理器都必須安裝在叢集中的所有節點上。如果任何節點缺少某個處理器，Create or Update Pipeline API 請求將會失敗。如果您使用外掛程式提供的處理器，請在 [`plugin.mandatory`]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/plugin-settings/) 設定中列出該外掛程式，讓缺少該外掛程式的節點無法啟動。

若要設定與部署資料匯入處理器，請確認您具備必要的權限與存取權限。如需更多資訊，請參閱 [API 權限]({{site.url}}{{site.baseurl}}/security/access-control/api/)。
{:.note}

## 支援的處理器

處理器類型及其必要或選用參數會依您的特定使用案例而有所不同。OpenSearch 支援下列資料匯入處理器。如需在 OpenSearch 管線中使用這些處理器的教學，請前往各處理器的對應文件。

處理器類型 | 說明
:--- | :--- 
`append` | 在文件的欄位中新增一或多個值。
`bytes` | 將人類可讀的位元組值轉換為以 bytes 為單位的值。
`community_id` | 為網路流量元組產生 community ID 流量雜湊演算法。
`convert` | 變更文件中某欄位的資料類型。
`copy` | 將現有欄位中的整個物件複製到另一個欄位。
`csv` | 擷取 CSV 並將其儲存為文件中的個別欄位。
`date` | 從欄位解析日期，然後使用該日期或時間戳記作為文件的時間戳記。
`date_index_name` | 根據文件中的日期或時間戳記欄位，將文件編製索引到以時間為基礎的索引中。
`dissect` | 使用定義的模式從文字欄位擷取結構化欄位。
`dot_expander` | 將含點號的欄位展開為物件欄位。
`drop` | 捨棄文件，不編製索引也不產生任何錯誤。
`fail` | 產生例外狀況並停止管線的執行。
`fingerprint` | 為文件中指定的特定欄位或所有欄位產生雜湊值。
`foreach` | 對文件中陣列欄位的每個元素套用另一個處理器。
`geojson-feature` | 將 GeoJSON 資料編製索引到地理空間欄位中。
`grok` | 使用模式比對解析並結構化非結構化資料。
`gsub` | 取代或刪除文件字串欄位中的子字串。
`html_strip` | 從文字欄位移除 HTML 標籤並傳回純文字內容。
`ip2geo` | 新增 IPv4 或 IPv6 位址的地理位置資訊。
`join` | 使用分隔字元將陣列的每個元素串連成單一字串。
`json` | 將 JSON 字串轉換為結構化 JSON 物件。
`kv` | 自動解析欄位中的鍵值對。
`lowercase` | 將特定欄位中的文字轉換為小寫字母。
`ml_inference` | 執行在 OpenSearch 中註冊的機器學習模型，並將模型輸出新增至文件。
`pipeline` | 執行內部管線。
`remove` | 從文件中移除欄位。
`remove_by_pattern` | 依欄位模式從文件中移除欄位。
`rename` | 重新命名現有欄位。
`script` | 對傳入的文件執行內嵌或已儲存的指令碼。
`set` | 將欄位的值設定為指定的值。
`sort` | 以遞增或遞減順序排序陣列的元素。
`sparse_encoding` | 從文字欄位產生稀疏向量/詞元與權重，供使用稀疏檢索的 neural sparse 搜尋使用。
`split` | 使用分隔字元將欄位分割為陣列。
`text_chunking` | 將過長的文件分割成較小的區塊。
`text_embedding` | 從文字欄位產生向量嵌入，用於語意搜尋。
`text_image_embedding` | 從文字與影像欄位產生組合向量嵌入，用於多模態搜尋。
`trim` | 移除字串欄位開頭與結尾的空白字元。
`uppercase` | 將特定欄位中的文字轉換為大寫字母。
`urldecode` | 解碼 URL 編碼格式的字串。
`user_agent` | 從瀏覽器傳送至其網路請求的使用者代理中擷取詳細資訊。 

## 常見處理器參數

每個處理器都有各自的參數。此外，所有處理器都支援下列選用參數。

參數 | 類型 | 說明
:--- | :--- | :---
`description` | 字串 | 處理器的說明。
`if` | 字串或物件 | Painless 指令碼條件，可指定為字串，或指定為包含 `source`、`lang` 與 `params` 的指令碼物件。唯有當條件評估為 `true` 時，處理器才會執行。如需詳細資訊，請參閱[條件式執行]({{site.url}}{{site.baseurl}}/ingest-pipelines/conditional-execution/)。
`ignore_failure` | 布林值 | 若為 `true`，則處理器失敗時管線仍會繼續執行。預設值為 `false`。如需詳細資訊，請參閱[處理管線失敗]({{site.url}}{{site.baseurl}}/ingest-pipelines/pipeline-failures/)。
`on_failure` | 處理器物件陣列 | 處理器失敗時要執行的處理器。如需詳細資訊，請參閱[處理管線失敗]({{site.url}}{{site.baseurl}}/ingest-pipelines/pipeline-failures/)。
`tag` | 字串 | 處理器的識別碼。此標籤會出現在錯誤中繼資料，以及 [Nodes Stats API]({{site.url}}{{site.baseurl}}/api-reference/nodes-apis/nodes-stats/) 傳回的匯入統計資料中，可協助您在管線中識別特定處理器。如需詳細資訊，請參閱[使用處理器標籤進行監控與偵錯]({{site.url}}{{site.baseurl}}/ingest-pipelines/create-ingest/#using-processor-tags-for-monitoring-and-debugging)。

下列 `lowercase` 處理器會將 `coupon_code` 欄位正規化。它只會對優惠券程式碼長度超過四個字元的文件執行；若執行失敗，會將錯誤訊息記錄在 `coupon_error` 欄位中，讓管線得以繼續執行：

```json
{
  "lowercase": {
    "description": "Normalizes coupon codes",
    "tag": "normalize-coupon",
    "if": "ctx.coupon_code instanceof String && ctx.coupon_code.length() > 4",
    "field": "coupon_code",
    "on_failure": [
      {
        "set": {
          "field": "coupon_error",
          "value": "{% raw %}{{ _ingest.on_failure_message }}{% endraw %}"
        }
      }
    ]
  }
}
```
{% include copy.html %}

## 處理器數量限制設定

您可以使用叢集設定 `cluster.ingest.max_number_processors` 來限制資料匯入處理器的數量。處理器總數包含處理器的數量以及 [`on_failure`]({{site.url}}{{site.baseurl}}/ingest-pipelines/pipeline-failures/) 處理器的數量。

`cluster.ingest.max_number_processors` 的預設值為 `Integer.MAX_VALUE`。若新增的處理器數量超過 `cluster.ingest.max_number_processors` 中設定的值，將會擲回 `IllegalStateException`。

## 支援批次處理的處理器

某些處理器支援批次匯入——它們可以批次方式同時處理多份文件。這些支援批次處理的處理器在使用批次處理時通常能提供更好的效能。若要進行批次處理，請使用 [Bulk API]({{site.url}}{{site.baseurl}}/api-reference/document-apis/bulk/) 並提供 `batch_size` 參數。所有支援批次處理的處理器都具有批次模式與單一文件模式。當您使用 `PUT` 方法匯入文件時，處理器會以單一文件模式運作，並依序處理文件。只有 `text_embedding` 與 `sparse_encoding` 處理器支援批次處理。所有其他處理器一次只處理一份文件。

## 選擇性啟用處理器

[ingest-common 模組](https://github.com/opensearch-project/OpenSearch/blob/main/modules/ingest-common/src/main/java/org/opensearch/ingest/common/IngestCommonModulePlugin.java)所定義的處理器，可以透過在 `opensearch.yml` 中提供 `ingest.common.processors.allowed` 靜態設定來選擇性啟用。若未提供，則預設啟用所有處理器。指定空清單會停用所有處理器。如果將該設定變更為移除先前已啟用的處理器，則任何使用已停用處理器的管線，在節點重新啟動且新設定生效後將會失敗。
