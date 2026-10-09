---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "指令碼"
nav_order: 1
nav_exclude: true
has_toc: false
has_children: true
permalink: /scripting/
---

# 指令碼

_指令碼_ 是 OpenSearch 在請求時評估的自訂運算式。當固定的查詢、對應或彙總無法表達您所需的邏輯時，指令碼可擴充 API，例如在每筆搜尋結果中傳回計算欄位、依結合相關性分數與欄位值的公式為文件排名，或在更新期間修改文件。

指令碼在 OpenSearch 內執行，貼近資料，因此您不需要擷取文件、在應用程式中轉換它們，然後再次將它們編製索引。這種速度伴隨著取捨：搜尋或彙總指令碼會針對 OpenSearch 考慮的每份文件執行一次，因此大型索引上的緩慢指令碼會放大成緩慢的請求。

預設的指令碼語言是 [Painless]({{site.url}}{{site.baseurl}}/scripting/painless/)。在任何接受指令碼的地方，`lang` 欄位會選取語言，因此您可以為特定請求選擇不同的語言。

本節的範例會針對單一產品記錄索引執行，因此您可以建立它一次，並從任何頁面繼續操作。如需對應與範例文件，請參閱[測試設定]({{site.url}}{{site.baseurl}}/scripting/using-scripts/#test-setup)。

## 可用的語言

下表中的每種語言都經過沙箱處理，並可在預設的 OpenSearch 發行版中使用。Painless 是唯一可在每個指令碼情境中執行的語言；其他每種語言都只處理單一工作。

語言 | 用途
:--- | :---
[`painless`]({{site.url}}{{site.baseurl}}/scripting/painless/) | 任何情境中的一般用途指令碼。
[`expression`]({{site.url}}{{site.baseurl}}/scripting/expressions/) | 數值排名與排序。
[`mustache`]({{site.url}}{{site.baseurl}}/api-reference/search-apis/search-template/) | 搜尋範本。
`knn` | 精確 k-NN 搜尋。`knn` 語言不接受自己的任何程式碼。其 `source` 必須是常值字串 `knn_score`，而欄位與查詢向量則在 `params` 中提供。如需完整請求，請參閱[使用評分指令碼進行精確 k-NN 搜尋]({{site.url}}{{site.baseurl}}/vector-search/vector-search-techniques/knn-score-script/)。

若要檢視您的叢集支援的語言，以及每種語言可執行的情境，請使用 [Get Script Languages API]({{site.url}}{{site.baseurl}}/api-reference/script-apis/get-script-language/)。該回應可能會列出上表以外的語言，因為外掛程式可以為自己的內部用途註冊語言。如需每個情境提供的內容，請參閱[指令碼情境]({{site.url}}{{site.baseurl}}/scripting/script-contexts/)。

沙箱化語言會將指令碼限制在 Java 類別與方法的允許清單中，該清單排除檔案存取、網路存取、執行緒建立與反射。允許清單可限制惡意指令碼能造成的損害，但不會讓來自不受信任來源的指令碼變得可以安全執行。在您接受來自無法控制之來源的指令碼之前，請參閱[指令碼安全性]({{site.url}}{{site.baseurl}}/scripting/script-security/)。
{: .warning}

## 後續步驟

若要撰寫您的第一個指令碼，請依序完成下列頁面：

1. [如何使用指令碼]({{site.url}}{{site.baseurl}}/scripting/using-scripts/) 會介紹 `script` 物件、示範如何執行內嵌指令碼並儲存一個以供重複使用，以及建立本節範例所使用的索引。
2. [在指令碼中存取文件欄位]({{site.url}}{{site.baseurl}}/scripting/accessing-fields/) 說明指令碼如何讀取文件資料，以及每項工作應選擇哪個存取路徑。
3. [Painless 指令碼語言]({{site.url}}{{site.baseurl}}/scripting/painless/) 說明預設語言，並連結至完整的語法參考。
4. [指令碼安全性]({{site.url}}{{site.baseurl}}/scripting/script-security/) 說明限制叢集接受哪些指令碼的設定。在您讓用戶端提交指令碼之前，請先套用這些設定。
