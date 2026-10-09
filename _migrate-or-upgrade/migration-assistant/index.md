---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Migration Assistant
nav_order: 70
has_children: false
has_toc: true
permalink: /migrate-or-upgrade/migration-assistant/
---

# Migration Assistant

OpenSearch 的 Migration Assistant 可協助您將 Elasticsearch 和 OpenSearch 工作負載遷移或升級至 OpenSearch 受管叢集。此解決方案以低風險且規範明確的遷移路徑，為現有資料與即時資料自動化手動工作。它也包含進階功能，例如中繼資料遷移工具 (Metadata Migration Tool) 以及擷取與重播比較工具 (Capture and Replay comparison tooling)，協助您更早找出可能的遷移與升級問題。遷移流程經過簡化，可根據真實客戶工作負載進行效能與行為比較，並加速遷移前、遷移及驗證階段。

此解決方案提供一套系統化的遷移工作流程，用於升級、遷移、復原及修改 OpenSearch 叢集。此工作流程包含用於管理的 Migration Console CLI、用於現有資料回填的專用擴展群組，以及用於同步來源與目標叢集之間即時流量的 Traffic Replayer。使用者可以暫停或停止遷移，而不影響生產流量，藉此降低風險。此外，回填功能會從快照擷取資料，讓來源叢集不受影響，並支援多段跳躍遷移，進而減少所需的遷移總次數，將進一步的風險降到最低。

Migration Assistant 可為您的遷移與升級需求提供幾項主要優勢。

## 優勢

Migration Assistant 提供下列優勢。

### 簡化的管理體驗

將資料從來源叢集 (source cluster) 傳輸到指定的目標 (OpenSearch 叢集)。

### 可調整且低風險的遷移

安全地擷取並重播來源與目標叢集上的流量，以找出最佳效能，同時透過停止功能、比較工具、來源保留及多段跳躍支援來降低遷移風險。

### 集中式的資料分析位置

記錄來源與目的地叢集之間的請求和回應以進行比較，然後將延遲指標和回應碼轉送至分析中樞。您可以分析將流量從舊系統轉換至新 OpenSearch 目的地所需的資料。

## 入門

若要進一步了解，請參閱 [Migration Assistant 文件]({{site.url}}{{site.baseurl}}/migration-assistant/)。
