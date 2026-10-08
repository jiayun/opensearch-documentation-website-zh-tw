---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "在 Dev Tools 主控台中執行查詢"
parent: Getting started
nav_order: 50
---

# 在 Dev Tools 主控台中執行查詢

Dev Tools 主控台讓您能將 [Query DSL]({{site.url}}{{site.baseurl}}/query-dsl/) 查詢傳送至 OpenSearch，而無需在終端機中使用 cURL。

## 試試看：撰寫並執行查詢

1. 若要開啟 Dev Tools 主控台，請在 OpenSearch Dashboards 主頁面上選取 **Dev Tools**，或從左側導覽選單選取 **Management** > **Dev Tools**。在已啟用工作區的安裝環境中，請選取導覽面板左下角的程式碼圖示 ({::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/icons/code-icon.png" class="inline-icon" alt="code icon"/>{:/})。

2. 在主控台左側的編輯器窗格中撰寫查詢。例如，輸入下列查詢以將一些文件編製索引：

   ```json
   POST _bulk
   { "create": { "_index": "students", "_id": "2" } }
   { "name": "Jonathan Powers", "gpa": 3.85, "grad_year": 2025 }
   { "create": { "_index": "students", "_id": "3" } }
   { "name": "Jane Doe", "gpa": 3.52, "grad_year": 2024 }
   ```
   {% include copy.html %}

3. 若要傳送查詢，請將游標放在查詢文字中的任意位置，然後選取請求右上方的播放圖示 ({::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/dev-tools/play-icon.png" class="inline-icon" alt="play icon"/>{:/})，或按下 `Ctrl/Cmd+Enter`。

   OpenSearch 會在主控台右側的窗格中顯示回應。

    ![查詢範例]({{site.url}}{{site.baseurl}}/images/dashboards/dev-tools-example.png)

4. 試試搜尋查詢。輸入下列請求，以從 `students` 索引擷取所有文件：

   ```json
   GET students/_search
   {
     "query": {
       "match_all": {}
     }
   }
   ```
   {% include copy.html %}

5. 選取播放圖示以傳送請求並查看結果。

## 後續步驟

- 如需完整的 Dev Tools 參考指南，請參閱 [Dev Tools]({{site.url}}{{site.baseurl}}/dashboards/dev-tools/index/)。
- 如需完整的查詢語言參考指南，請參閱 [Query DSL]({{site.url}}{{site.baseurl}}/query-dsl/)。