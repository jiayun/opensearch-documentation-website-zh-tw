---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "關鍵元件"
nav_order: 20
permalink: /classic/migration-assistant/key-components/
---

# 關鍵元件

以下是 Migration Assistant 的關鍵元件。

## Elasticsearch/OpenSearch 來源

在此解決方案中，您的來源叢集執行於 Elasticsearch 或 OpenSearch，並託管於 Amazon Elastic Compute Cloud (Amazon EC2) 執行個體或類似的運算環境中。來源叢集也可能由 AWS、其他雲端供應商管理，或託管於內部部署環境。流量會從來源叢集重新導向至 Traffic Capture Proxy，並重播至目標，通常是較新版本的 OpenSearch。

## Migration Console

Migration Console 提供專為遷移設計的 CLI，並提供多種工具來簡化遷移流程。除了清理遷移資源和管理應用程式變更之外，您可以透過此主控台執行完成遷移所需的一切作業。

## Traffic Capture Proxy

此元件專為 HTTP RESTful 流量而設計。它會將流量轉送至來源叢集，同時將此流量分割並導向至串流處理服務，以供後續重播。

## Traffic Replayer

[Traffic Replayer]({{site.url}}{{site.baseurl}}/classic/migration-assistant/migration-phases/replay-captured-traffic/) 做為流量模擬工具，會將錄製的請求流量重播至目標叢集，以模擬來源流量模式。它會將原始請求及其回應與導向目標叢集的請求及其回應建立關聯，以便進行比較分析。

## Metadata Migration Tool

整合至 Migration CLI 的 Metadata Migration Tool 可獨立使用，以遷移叢集中繼資料，包括索引對應、索引組態設定、範本、元件範本和別名。

## Reindex-from-Snapshot

`Reindex-from-Snapshot` (RFS) 會從現有快照重新編製索引資料。Amazon Elastic Container Service (Amazon ECS) 工作者會協調從現有快照遷移文件，將文件平行重新編製索引至目標叢集。

## 目標叢集

目標叢集是升級或遷移的目的地叢集。它也可能是已重新設定以符合不斷變化的應用程式需求的同版本叢集。
