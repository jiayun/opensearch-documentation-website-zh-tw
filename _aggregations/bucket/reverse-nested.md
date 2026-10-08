---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "反向巢狀"
parent: Bucket aggregations
nav_order: 160
redirect_from:
  - /query-dsl/aggregations/bucket/reverse-nested/
---

# 反向巢狀彙總

`reverse_nested` 彙總可讓您在 [`nested` 彙總]({{site.url}}{{site.baseurl}}/aggregations/bucket/nested/)情境中，針對父文件欄位進行彙總。當您依巢狀欄位分組時，彙總情境會轉移至巢狀文件。`reverse_nested` 彙總會跳出該巢狀情境，並連接回父文件（或根文件），讓後續的子彙總能夠存取父文件欄位。

`reverse_nested` 彙總必須定義在 `nested` 彙總內。
{: .note}

## 參數

`reverse_nested` 彙總接受下列參數。

| 參數 | 必要／選用 | 資料類型 | 說明 |
| :--- | :--- | :--- | :--- |
| `path` | 選用 | 字串 | 要連接回的巢狀物件路徑。預設為空（連接回根文件）。若有多層巢狀結構，請指定中間層的巢狀路徑，以連接至該層，而非根文件。 |

## 範例設定

建立索引，其中的議題包含巢狀留言：

```json
PUT /issues
{
  "mappings": {
    "properties": {
      "title": { "type": "text" },
      "tags": { "type": "keyword" },
      "comments": {
        "type": "nested",
        "properties": {
          "username": { "type": "keyword" },
          "comment": { "type": "text" }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

將一些文件編製索引：

```json
POST /issues/_bulk?refresh=true
{"index":{"_id":"1"}}
{"title":"Add dark mode to settings page","tags":["ui","enhancement"],"comments":[{"username":"alice","comment":"Would love this feature"},{"username":"bob","comment":"Should support system preference detection"}]}
{"index":{"_id":"2"}}
{"title":"Export report as PDF","tags":["export","enhancement"],"comments":[{"username":"alice","comment":"CSV export would also be useful"},{"username":"carol","comment":"Added to the roadmap"}]}
{"index":{"_id":"3"}}
{"title":"Improve mobile navigation","tags":["ui","mobile"],"comments":[{"username":"bob","comment":"Hamburger menu would work well"},{"username":"carol","comment":"Agree, especially for tablets"}]}
```
{% include copy-curl.html %}

## 範例

下列範例會找出最活躍的留言者，接著使用 `reverse_nested` 判斷每位留言者最常參與哪些標籤的議題。若沒有 `reverse_nested`，便無法存取 `tags` 欄位，因為彙總情境位於巢狀 `comments` 物件內：

```json
GET /issues/_search
{
  "size": 0,
  "aggs": {
    "comments": {
      "nested": {
        "path": "comments"
      },
      "aggs": {
        "top_commenters": {
          "terms": {
            "field": "comments.username"
          },
          "aggs": {
            "back_to_issue": {
              "reverse_nested": {},
              "aggs": {
                "top_tags": {
                  "terms": {
                    "field": "tags"
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

回應顯示，Bob 的留言出現在標記為「ui」（2 個議題）、「enhancement」（1 個）及「mobile」（1 個）的議題中：

```json
{
  ...
  "aggregations": {
    "comments": {
      "doc_count": 6,
      "top_commenters": {
        "doc_count_error_upper_bound": 0,
        "sum_other_doc_count": 0,
        "buckets": [
          {
            "key": "alice",
            "doc_count": 2,
            "back_to_issue": {
              "doc_count": 2,
              "top_tags": {
                "doc_count_error_upper_bound": 0,
                "sum_other_doc_count": 0,
                "buckets": [
                  {
                    "key": "enhancement",
                    "doc_count": 2
                  },
                  {
                    "key": "export",
                    "doc_count": 1
                  },
                  {
                    "key": "ui",
                    "doc_count": 1
                  }
                ]
              }
            }
          },
          {
            "key": "bob",
            "doc_count": 2,
            "back_to_issue": {
              "doc_count": 2,
              "top_tags": {
                "doc_count_error_upper_bound": 0,
                "sum_other_doc_count": 0,
                "buckets": [
                  {
                    "key": "ui",
                    "doc_count": 2
                  },
                  {
                    "key": "enhancement",
                    "doc_count": 1
                  },
                  {
                    "key": "mobile",
                    "doc_count": 1
                  }
                ]
              }
            }
          },
          {
            "key": "carol",
            "doc_count": 2,
            "back_to_issue": {
              "doc_count": 2,
              "top_tags": {
                "doc_count_error_upper_bound": 0,
                "sum_other_doc_count": 0,
                "buckets": [
                  {
                    "key": "enhancement",
                    "doc_count": 1
                  },
                  {
                    "key": "export",
                    "doc_count": 1
                  },
                  {
                    "key": "mobile",
                    "doc_count": 1
                  },
                  {
                    "key": "ui",
                    "doc_count": 1
                  }
                ]
              }
            }
          }
        ]
      }
    }
  }
}
```

## 範例：在多層巢狀結構中使用 path 參數

當文件中的巢狀物件內含其他巢狀物件時，您可以使用 `path` 參數連接回中間層，而非根文件。下列範例使用論壇式結構，其中貼文包含巢狀留言，而每則留言包含巢狀回覆：

```json
PUT /forum_posts
{
  "mappings": {
    "properties": {
      "title": { "type": "keyword" },
      "comments": {
        "type": "nested",
        "properties": {
          "author": { "type": "keyword" },
          "replies": {
            "type": "nested",
            "properties": {
              "author": { "type": "keyword" }
            }
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

將包含留言和回覆的貼文編製索引：

```json
POST /forum_posts/_doc/1?refresh=true
{
  "title": "Post A",
  "comments": [
    { "author": "alice", "replies": [{"author": "bob"}, {"author": "carol"}] },
    { "author": "bob", "replies": [{"author": "alice"}] }
  ]
}
```
{% include copy-curl.html %}

下列彙總會依回覆作者分組，接著使用 `reverse_nested` 搭配 `"path": "comments"` 連接回留言層級（而非根文件），並找出每個人回覆了哪些留言作者：

```json
GET /forum_posts/_search
{
  "size": 0,
  "aggs": {
    "comments": {
      "nested": { "path": "comments" },
      "aggs": {
        "replies": {
          "nested": { "path": "comments.replies" },
          "aggs": {
            "reply_authors": {
              "terms": { "field": "comments.replies.author" },
              "aggs": {
                "back_to_comment": {
                  "reverse_nested": { "path": "comments" },
                  "aggs": {
                    "comment_authors": {
                      "terms": { "field": "comments.author" }
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

回應顯示，Bob 回覆了 Alice 的留言，Carol 也回覆了 Alice 的留言：

```json
{
  ...
  "aggregations": {
    "comments": {
      "doc_count": 2,
      "replies": {
        "doc_count": 3,
        "reply_authors": {
          "doc_count_error_upper_bound": 0,
          "sum_other_doc_count": 0,
          "buckets": [
            {
              "key": "alice",
              "doc_count": 1,
              "back_to_comment": {
                "doc_count": 1,
                "comment_authors": {
                  "doc_count_error_upper_bound": 0,
                  "sum_other_doc_count": 0,
                  "buckets": [
                    {
                      "key": "bob",
                      "doc_count": 1
                    }
                  ]
                }
              }
            },
            {
              "key": "bob",
              "doc_count": 1,
              "back_to_comment": {
                "doc_count": 1,
                "comment_authors": {
                  "doc_count_error_upper_bound": 0,
                  "sum_other_doc_count": 0,
                  "buckets": [
                    {
                      "key": "alice",
                      "doc_count": 1
                    }
                  ]
                }
              }
            },
            {
              "key": "carol",
              "doc_count": 1,
              "back_to_comment": {
                "doc_count": 1,
                "comment_authors": {
                  "doc_count_error_upper_bound": 0,
                  "sum_other_doc_count": 0,
                  "buckets": [
                    {
                      "key": "alice",
                      "doc_count": 1
                    }
                  ]
                }
              }
            }
          ]
        }
      }
    }
  }
}
```

## 回應本文欄位

下表列出回應本文欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `doc_count` | 整數 | 彙總連接回的父文件數量。此計數反映的是相異父文件的數量，而非巢狀文件的數量。 |
