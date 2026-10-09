---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "筆記本"
nav_order: 90
redirect_from:
  - /dashboards/notebooks/
  - /observability-plugin/notebooks/
has_children: false
---

# 筆記本

OpenSearch Dashboards 筆記本是一種介面，可讓您輕鬆地在單一筆記本介面中結合程式碼片段、即時視覺化與敘述文字。

筆記本可讓您以互動方式探索資料，方法是執行不同的視覺化，並可與團隊成員分享，以便在專案上協作。

筆記本是由兩種元素組成的文件：程式碼區塊 (Markdown/SQL/Piped Processing Language (PPL)) 與視覺化。您可以選擇多個時間軸來比較與對照視覺化。

您也可以直接從筆記本產生[報告]({{site.url}}{{site.baseurl}}/dashboards/reporting/)。

常見的使用案例包括建立事後檢討報告、設計執行手冊、建置即時基礎架構報告，以及撰寫文件。

OpenSearch Dashboards 中的租用戶是儲存筆記本與其他 OpenSearch Dashboards 物件的空間。如需詳細資訊，請參閱 [OpenSearch Dashboards 多租用戶]({{site.url}}{{site.baseurl}}/security/multi-tenancy/tenant-index/)。
{: .note }


## 筆記本入門

若要開始使用，請在 OpenSearch Dashboards 中選擇 **Notebooks**。


### 步驟 1：建立筆記本

筆記本是用於建立報告的介面。

1. 選擇 **Create notebook** 並輸入具描述性的名稱。
1. 選擇 **Create**。

選擇 **Actions** 可重新命名、複製或刪除筆記本。

![建立筆記本]({{site.url}}{{site.baseurl}}/images/create_notebook.gif)

### 步驟 2：新增段落

段落結合程式碼區塊與視覺化，用來描述資料。

#### 新增程式碼區塊

程式碼區塊支援 Markdown、SQL 與 PPL 語言。

請使用 `%[language type]` 語法，在第一行指定輸入語言。
例如，Markdown 請輸入 `%md`，SQL 請輸入 `%sql`，PPL 請輸入 `%ppl`。

##### Markdown 區塊範例

```
%md
Add in text formatted in Markdown.
```

![Markdown 段落]({{site.url}}{{site.baseurl}}/images/markdown_notebooks.gif)

##### SQL 區塊範例

```sql
%sql
Select * from opensearch_dashboards_sample_data_flights limit 20;
```

![SQL 段落]({{site.url}}{{site.baseurl}}/images/sql_notebooks.gif)

##### PPL 區塊範例

```
%ppl
source=opensearch_dashboards_sample_data_logs | head 20
```

![PPL 段落]({{site.url}}{{site.baseurl}}/images/ppl_notebooks.gif)


#### 新增視覺化

1. 若要新增視覺化，請選擇 **Add paragraph** 並選取 **Visualization**。
1. 在 **Title** 中，選取您的視覺化並選擇日期範圍。您可以選擇多個時間軸來比較與對照視覺化。
1. 若要執行並儲存段落，請選擇 **Run**。

![視覺化段落]({{site.url}}{{site.baseurl}}/images/visualization_notebooks.gif)

## 段落動作

您可以對段落執行下列動作：

- 在報告頂端新增段落。
- 在報告底部新增段落。
- 同時執行所有段落。
- 清除所有段落的輸出。
- 刪除所有段落。

![範例筆記本]({{site.url}}{{site.baseurl}}/images/paragraphs_notebooks.gif)

## 範例筆記本

我們準備了下列範例筆記本，展示各種使用案例：

- 使用 SQL 查詢 OpenSearch Dashboards 的範例航班資料。
- 使用 PPL 查詢 OpenSearch Dashboards 的範例網頁記錄資料。
- 使用 PPL 與視覺化，對 OpenSearch Dashboards 的範例網頁記錄資料執行範例根本原因事件分析。

若要新增範例筆記本，請選擇 **Actions** 並選取 **Add sample notebooks**。

![範例筆記本]({{site.url}}{{site.baseurl}}/images/sample_notebooks.gif)

## 建立報告

您可以使用筆記本建立 PNG 與 PDF 報告：

1. 從頂端功能表列，選擇 **Reporting actions**。
1. 您可以選擇 **Download PDF** 或 **Download PNG**。

   報告會在背景以非同步方式產生，視報告大小而定，可能需要幾分鐘。報告可供下載時會出現通知。

1. 若要建立以排程為基礎的報告，請選擇 **Create report definition**。如需建立報告定義的步驟，請參閱[使用定義建立報告]({{site.url}}{{site.baseurl}}/dashboards/reporting#creating-reports-using-a-definition)。
1. 若要查看您的所有報告，請選擇 **View all reports**。

![報告筆記本]({{site.url}}{{site.baseurl}}/images/report_notebooks.gif)
