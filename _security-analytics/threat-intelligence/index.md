---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "威脅情報"
nav_order: 40
has_children: true
redirect_from:
  - /security-analytics/threat-intelligence/
---

# 威脅情報

Security Analytics 中的威脅情報提供整合威脅情報摘要的功能。摘要包含入侵指標 (IOC)，其會透過設定威脅情報監視器，在您的資料中搜尋惡意指標。當威脅情報摘要中的惡意 IP、網域或雜湊值與您的資料相符時，這些監視器會產生發現項目，並可傳送通知。


您可以透過下列方式使用威脅情報：

- 威脅情報 API：若要使用 API 操作設定威脅情報，請參閱[威脅情報 API]({{site.url}}{{site.baseurl}}/security-analytics/threat-intelligence/api/threat-intel-api/)。
- OpenSearch Dashboards：若要透過 OpenSearch Dashboards 介面設定及使用威脅情報，請參閱[入門]({{site.url}}{{site.baseurl}}/security-analytics/threat-intelligence/getting-started/)。