---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "電話號碼分析器"
parent: Analyzers
nav_order: 140
---

# 電話號碼分析器

`analysis-phonenumber` 外掛程式提供用於剖析電話號碼的分析器和斷詞器。剖析電話號碼並不簡單（儘管乍看之下可能很簡單），因此需要專用的分析器。如需了解剖析電話號碼時常見的誤解，請參閱 [Falsehoods programmers believe about phone numbers](https://github.com/google/libphonenumber/blob/master/FALSEHOODS.md)。


OpenSearch 支援下列電話號碼分析器：

* [`phone`](#the-phone-analyzer)：在編製索引時使用的[索引分析器]({{site.url}}{{site.baseurl}}/analyzers/index-analyzers/)。
* [`phone-search`](#the-phone-search-analyzer)：在搜尋時使用的[搜尋分析器]({{site.url}}{{site.baseurl}}/analyzers/search-analyzers/)。

此外掛程式在內部使用 [`libphonenumber`](https://github.com/google/libphonenumber) 程式庫，並遵循其剖析規則。

電話號碼分析器並非用於在較長的文字中尋找電話號碼。您應該將其用於僅包含電話號碼的欄位。
{: .note}

## 安裝外掛程式

在使用電話號碼分析器之前，您必須執行下列命令來安裝 `analysis-phonenumber` 外掛程式：

```sh
./bin/opensearch-plugin install analysis-phonenumber
```

## 指定預設地區

您可以選擇在分析器中提供 `phone-region` 參數，以指定剖析電話號碼時使用的預設地區。有效的電話地區以 ISO 3166 國碼表示。如需更多資訊，請參閱 [ISO 3166 國碼清單](https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes)。

對包含國際撥號前綴 `+` 的電話號碼進行斷詞時，預設地區並不相關。然而，對於以國家前綴撥打國際號碼的電話號碼（例如，從大多數歐洲國家撥打北美洲時，使用 `001` 而非 `+1`），則需要提供地區。透過指定地區，您也可以為不含國際前綴的國內電話號碼正確編製索引。

## 範例

下列請求會建立一個索引，其中包含一個用於匯入瑞士（地區碼 `CH`）電話號碼的欄位：

```json
PUT /example-phone
{
  "settings": {
    "analysis": {
      "analyzer": {
        "phone-ch": {
          "type": "phone",
          "phone-region": "CH"
        },
        "phone-search-ch": {
          "type": "phone-search",
          "phone-region": "CH"
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "phone_number": {
        "type": "text",
        "analyzer": "phone-ch",
        "search_analyzer": "phone-search-ch"
      }
    }
  }
}
```
{% include copy-curl.html %}

## phone 分析器

`phone` 分析器會根據指定的電話號碼產生 n-gram。包含國際撥號前綴的（虛構）瑞士電話號碼，無論是否使用瑞士專屬的電話地區皆可剖析。因此，下列兩個請求會產生相同的結果：

```json
GET /example-phone/_analyze
{
  "analyzer" : "phone-ch",
  "text" : "+41 60 555 12 34"
}
```
{% include copy-curl.html %}

```json
GET /example-phone/_analyze
{
  "analyzer" : "phone",
  "text" : "+41 60 555 12 34"
}
```
{% include copy-curl.html %}

回應包含產生的 n-gram：

```json
["+41 60 555 12 34", "6055512", "41605551", "416055512", "6055", "41605551234", ...]
```

然而，如果您指定的電話號碼不含國際撥號前綴 `+`（使用 `0041` 或完全省略
國際撥號前綴），則只有設定了正確電話地區的分析器才能剖析該號碼：

```json
GET /example-phone/_analyze
{
  "analyzer" : "phone-ch",
  "text" : "060 555 12 34"
}
```
{% include copy-curl.html %}

## phone-search 分析器

相較之下，`phone-search` 分析器不會建立 n-gram，只會產生一些基本詞元。例如，傳送下列請求並指定 `phone-search` 分析器：

```json
GET /example-phone/_analyze
{
  "analyzer" : "phone-search",
  "text" : "+41 60 555 12 34"
}
```
{% include copy-curl.html %}

回應包含下列詞元：

```json
["+41 60 555 12 34", "41 60 555 12 34", "41605551234", "605551234", "41"]
```
