---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "已儲存物件"
parent: Dashboards management
has_children: true
nav_order: 12
---

# 已儲存物件

_已儲存物件_是您在 OpenSearch Dashboards 中建立並重複使用的資源，包括視覺化、儀表板、已儲存的搜尋、索引模式和地圖。您可以將這些物件匯出至檔案，再將該檔案匯入另一個執行個體，藉此將儀表板從開發叢集複製到正式環境叢集、在租用戶或工作區之間移動物件，或備份您的視覺化。

物件之間彼此相依：儀表板會參照其視覺化，而視覺化會參照其索引模式。請將物件連同其參照的物件一起匯出，如此一來，即使目標執行個體中尚未包含這些物件，也能匯入該匯出檔案。

若要以程式設計方式執行這些工作（例如作為 CI/CD 管線的一部分），請參閱 [Saved Objects API]({{site.url}}{{site.baseurl}}/dashboards/management/saved-objects-api/)。

## 匯出已儲存物件

若要匯出特定物件（例如一個儀表板及其顯示的所有內容），請依照下列步驟操作：

1. 在頂端選單中，前往 **Management** > **Dashboards Management** > **Saved objects**。
1. 選取每個要匯出之物件的核取方塊。若要縮小清單範圍，請在搜尋方塊中輸入標題，或依 **Type** 篩選。
1. 選取 **Export**。
1. 保持選取 **Include related objects**，讓匯出內容也包含所選物件參照的物件。
1. 選取 **Export** 以下載檔案。

若要匯出執行個體的完整內容，請選取 **Export all objects**，選擇要包含的類型，然後選取 **Export**。

下載的檔案採用 NDJSON 格式，每行一個物件，最後一行為摘要。此格式與 [Export Saved Objects API]({{site.url}}{{site.baseurl}}/dashboards/management/saved-objects-api/#export-saved-objects) 產生的格式相同，因此從 OpenSearch Dashboards 匯出的檔案可以使用 API 匯入，而使用 API 匯出的檔案也可以從 OpenSearch Dashboards 匯入。

若要在匯出物件之前檢視該物件參照的內容，請選取該物件的 **Relationships** 動作。

啟用多租用戶時，每個租用戶都有各自的一組已儲存物件，而匯出內容只會包含您目前所使用租用戶的物件。這也適用於 **Export all objects**，因此若要擷取執行個體中的所有物件，請切換至每個租用戶並分別匯出。啟用彙總檢視時，清單可以同時顯示多個租用戶的物件，但依租用戶篩選清單並不會改變匯出所包含的內容。如需詳細資訊，請參閱 [OpenSearch Dashboards 已儲存物件的多租用戶彙總檢視]({{site.url}}{{site.baseurl}}/security/multi-tenancy/mt-agg-view/)。

啟用工作區時，從工作區內開始的匯出只會包含與該工作區相關聯的物件。從任何工作區之外的 **Saved objects** 開始的匯出則涵蓋所有工作區：清單會包含您可存取之所有工作區的物件，並在 **Workspace** 欄中標示每個物件，而 **Export all objects** 會將所有物件寫入檔案。

若要將物件複製到同一執行個體中的另一個工作區而非匯出，請選取物件，選取 **Copy to**，然後選擇目標工作區。若要複製目前工作區中的所有物件，請選取 **Copy all objects to**。若要以程式設計方式執行相同工作，請參閱[複製已儲存物件]({{site.url}}{{site.baseurl}}/dashboards/workspace/apis/#duplicate-saved-objects)。

## 匯入已儲存物件

若要匯入已儲存物件，請依照下列步驟操作：

1. 在頂端選單中，前往 **Management** > **Dashboards Management** > **Saved objects**。
1. 選取 **Import**。
1. 選取 **Select file**，然後選擇要匯入的 NDJSON 檔案。
1. 在 **Import options** 中，選擇如何處理已存在的物件：
   - **Create new objects with unique IDs** 會將物件匯入為副本，並保持現有物件不變。
   - **Check for existing objects** 會將匯入的物件與執行個體中已有的物件進行比較。將其與 **Automatically overwrite conflicts** 搭配使用可取代現有物件，或與 **Request action on conflict** 搭配使用，以針對每個衝突個別決定。
1. 選取 **Import**，然後選取 **Done**。

如果物件參照了目標執行個體中不存在的索引模式，OpenSearch Dashboards 會列出受影響的物件，並提示您選取其他索引模式或建立一個索引模式。

啟用多租用戶時，物件會匯入至您目前所使用的租用戶，因此請在匯入前切換至目標租用戶。

啟用工作區時，**Import** 只會出現在工作區內，且匯入的物件會與該工作區相關聯。請在匯入前開啟目標工作區。

## 將儀表板複製到另一個執行個體

若要在兩個為相同資料編製索引的執行個體之間移動儀表板，請依照下列步驟操作：

1. 在來源執行個體中，前往 **Management** > **Dashboards Management** > **Saved objects**，然後選取該儀表板的核取方塊。
1. 選取 **Export**，保持選取 **Include related objects**，然後選取 **Export**。該檔案包含儀表板、其視覺化和已儲存的搜尋，以及這些項目的索引模式。
1. 在目標執行個體中，前往 **Management** > **Dashboards Management** > **Saved objects**，然後選取 **Import**。
1. 選取下載的檔案，選擇匯入選項，然後選取 **Import**。

租用戶和工作區決定了每個步驟所涵蓋的物件。請在匯出前選取來源租用戶或工作區，並在匯入前選取目標租用戶或工作區。如需詳細資訊，請參閱[匯出已儲存物件](#exporting-saved-objects)和[匯入已儲存物件](#importing-saved-objects)。

## 限制

從 OpenSearch Dashboards 匯入時可接受 `.ndjson` 檔案，也可接受由早於 NDJSON 的 OpenSearch Dashboards 或 Kibana 版本所匯出的舊版 `.json` 檔案。對 `.json` 檔案的支援已淘汰，且 Saved Objects API 只接受 `.ndjson`。請先重新匯出舊版檔案，再將其用於 API。

單次匯出或匯入以 10,000 個物件及 25 MB 的請求大小為上限。如需控制這些限制的設定，以及同時適用於 OpenSearch Dashboards 和 API 的其他注意事項，請參閱[限制]({{site.url}}{{site.baseurl}}/dashboards/management/saved-objects-api/#limitations)。
