---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "語音"
parent: Token filters
nav_order: 330
---

# 語音詞元篩選器

`phonetic` 詞元篩選器會將詞元轉換為其語音表示法，讓發音相似但拼寫不同的單字能夠更彈性地相符。這在搜尋名稱、品牌或其他實體時特別實用，因為使用者可能會以不同方式拼寫，但發音相似。

OpenSearch 發行版本預設不包含 `phonetic` 詞元篩選器。若要使用此詞元篩選器，您必須先依下列方式安裝 `analysis-phonetic` 外掛程式，然後重新啟動 OpenSearch：

```bash
./bin/opensearch-plugin install analysis-phonetic
```
{% include copy.html %}

如需有關安裝外掛程式的詳細資訊，請參閱[管理 OpenSearch 外掛程式]({{site.url}}{{site.baseurl}}/install-and-configure/plugins/)。
{: .note}

## 參數

您可以使用下列參數設定 `phonetic` 詞元篩選器。

參數 | 必要/選用 | 資料類型 | 說明
:--- | :--- | :--- | :--- 
`encoder` | 選用 | 字串 | 指定要使用的語音演算法。<br><br>有效值為：<br>- `metaphone`（預設）<br>- `double_metaphone`<br>- `soundex`<br>- `refined_soundex`<br>- `caverphone1`<br>- `caverphone2`<br>- `cologne`<br>- `nysiis`<br>- `koelnerphonetik`<br>- `haasephonetik`<br>- `beider_morse`<br>- `daitch_mokotoff ` 
`replace` | 選用 | 布林值 | 是否取代原始詞元。若為 `false`，原始詞元會與語音編碼一起包含在輸出中。預設值為 `true`。


## 範例

下列範例請求會建立名為 `names_index` 的新索引，並設定具有 `phonetic` 篩選器的分析器：

```json
PUT /names_index
{
  "settings": {
    "analysis": {
      "filter": {
        "my_phonetic_filter": {
          "type": "phonetic",
          "encoder": "double_metaphone",
          "replace": true
        }
      },
      "analyzer": {
        "phonetic_analyzer": {
          "tokenizer": "standard",
          "filter": [
            "my_phonetic_filter"
          ]
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

## 產生的詞元

使用下列請求，檢查使用此分析器為名稱 `Stephen` 和 `Steven` 所產生的詞元：

```json
POST /names_index/_analyze
{
  "text": "Stephen",
  "analyzer": "phonetic_analyzer"
}
```
{% include copy-curl.html %}

```json
POST /names_index/_analyze
{
  "text": "Steven",
  "analyzer": "phonetic_analyzer"
}
```
{% include copy-curl.html %}

在這兩種情況下，回應都包含相同的產生詞元：

```json
{
  "tokens": [
    {
      "token": "STFN",
      "start_offset": 0,
      "end_offset": 6,
      "type": "<ALPHANUM>",
      "position": 0
    }
  ]
}
```
