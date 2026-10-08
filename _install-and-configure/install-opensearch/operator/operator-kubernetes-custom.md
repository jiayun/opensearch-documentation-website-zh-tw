---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "Kubernetes 部署自訂"
parent: OpenSearch Kubernetes Operator
grand_parent: Installing OpenSearch
nav_order: 40
---

# Kubernetes 部署自訂

除了設定 OpenSearch 本身之外，您也可以自訂 operator 部署 OpenSearch 和 OpenSearch Dashboards Pod 的方式。

## 資料持久性

根據預設，operator 會使用預設 [Storage Class](https://kubernetes.io/docs/concepts/storage/storage-classes/) 的持久性儲存空間來建立 OpenSearch 節點集區。您可以針對每個節點集區變更此行為。您可以提供其他的 storage class 和存取模式，或設定 `hostPath` 或 `emptyDir` 儲存空間。

可用的儲存空間選項如下：

<!-- vale off -->
### Persistent Volume Claim (PVC)
<!-- vale on -->

預設選項是使用 PVC 的持久性儲存空間。如有需要，您可以明確定義 `storageClass`、`annotations` 和 `labels`：

```yaml
nodePools:
  - component: masters
    replicas: 3
    diskSize: "30Gi"
    roles:
      - "data"
      - "master"
    persistence:
      pvc:
        storageClass: mystorageclass # Set the name of the storage class to be used
        accessModes: # You can change the accessMode
          - ReadWriteOnce
        annotations: # You can add annotations
          test.io/crypt-key-id: "your-kms-key-id"
        labels: # You can add labels
          team: "backend-data"
```
{% include copy.html %}

<!-- vale off -->
### emptyDir
<!-- vale on -->

如果您不想使用持久性儲存空間，可以使用 `emptyDir` 選項。請注意，這可能導致資料遺失，因此您應僅在測試時，或針對已透過其他方式持久保存的資料使用此選項。

```yaml
nodePools:
  - component: masters
    replicas: 3
    diskSize: "30Gi"
    roles:
      - "data"
      - "master"
    persistence:
      emptyDir: {} # This configures emptyDir
```
{% include copy.html %}

如果您使用 `emptyDir`，請將 `spec.general.drainDataNodes` 設定為 `true`。這可確保在執行滾動升級或重新啟動作業之前，會先將分片從 Pod 中移出。

<!-- vale off -->
### hostPath
<!-- vale on -->

最後一個選項是使用 `hostPath`。強烈不建議使用 `hostPath`。根據預設，operator 會套用 Pod 反親和性 (anti-affinity)，以防止多個 Pod 排程到同一個節點上，這在使用 `hostPath` 時有所幫助。不過，如果您需要更嚴格的控制，請為節點集區設定明確的親和性規則，以確保多個 Pod 不會排程到同一個 Kubernetes 主機上。

```yaml
nodePools:
  - component: masters
    replicas: 3
    diskSize: "30Gi"
    roles:
      - "data"
      - "master"
    persistence:
      hostPath:
        path: "/var/opensearch" # Define the path on the host here
```
{% include copy.html %}

## Pod 與容器的安全性內容

您可以為 OpenSearch Pod 和 OpenSearch Dashboards Pod 設定安全性內容 (security context)，以定義權限與存取控制設定。若要為 Pod 指定安全性設定，請加入 `podSecurityContext` 欄位。若為容器，請加入 `securityContext` 欄位。

OpenSearch Pod（位於 `spec.general`）和 OpenSearch Dashboards Pod（位於 `spec.dashboards`）的結構相同：

```yaml
spec:
  general:
    podSecurityContext:
      runAsUser: 1000
      runAsGroup: 1000
      runAsNonRoot: true
    securityContext:
      allowPrivilegeEscalation: false
      privileged: false
  dashboards:
    podSecurityContext:
      fsGroup: 1000
      runAsNonRoot: true
    securityContext:
      capabilities:
        drop:
          - ALL
      privileged: false
```
{% include copy.html %}

根據預設，OpenSearch Pod 會啟動一個 init 容器來設定磁碟區。此容器需要以 root 權限執行，且不會使用已定義的 `securityContext`。如果您的 Kubernetes 環境不允許使用 root 使用者的容器，請[停用此 init 輔助程式](#disabling-the-init-helper)。在這種情況下，請將 `general.setVMMaxMapCount` 設定為 `false`，因為此功能同樣會以 root 啟動 init 容器。

在初始叢集設定期間啟動的 bootstrap Pod，會使用與 OpenSearch Pod 相同的 Pod `securityContext`（init 容器也有相同的限制）。
{: .note}

bootstrap Pod 會使用持久性儲存空間 (PVC)，在初始化期間的重新啟動之間保留叢集狀態。這可防止 bootstrap Pod 在安全性組態更新工作完成後重新啟動時，發生叢集形成失敗的情況。bootstrap PVC 會隨 bootstrap Pod 自動建立和刪除。

## OpenSearch 節點上的標籤或註解

您可以在節點集區組態中加入額外的標籤 (label) 或註解 (annotation)。這有助於與其他應用程式整合（例如服務網格），或用於設定 Prometheus 擷取端點。

此外，您也可以使用 `spec.general.annotations` 欄位全域設定註解。這些註解不僅會套用至節點集區，也會套用至 Kubernetes 服務。

```yaml
spec:
  nodePools:
    - component: masters
      replicas: 3
      diskSize: "5Gi"
      labels: # Add any extra labels as key-value pairs here
        someLabelKey: someLabelValue
      annotations: # Add any extra annotations as key-value pairs here
        someAnnotationKey: someAnnotationValue
      nodeSelector:
      resources:
        requests:
          memory: "2Gi"
          cpu: "500m"
        limits:
          memory: "2Gi"
          cpu: "500m"
      roles:
        - "data"
        - "master"
```
{% include copy.html %}

所定義的任何註解和標籤都會直接加入節點集區的 Pod。

## 為 OpenSearch Dashboards 部署加入標籤或註解

您可以在 OpenSearch Dashboards Pod 規格中加入標籤或註解。如果您希望 OpenSearch Dashboards 成為服務網格的一部分，或要與依賴標籤或註解的其他應用程式整合，這會很有幫助。

```yaml
spec:
  dashboards:
    enable: true
    version: 3.0.0
    replicas: 1
    labels: # Add any extra labels as key-value pairs here
      someLabelKey: someLabelValue
    annotations: # Add any extra annotations as key-value pairs here
      someAnnotationKey: someAnnotationValue
```
{% include copy.html %}

所定義的任何註解和標籤都會直接加入 OpenSearch Dashboards Pod。

## OpenSearch 節點上的優先順序類別

您可以透過指定優先順序類別名稱，將 OpenSearch 節點設定為使用 `PriorityClass`。這有助於避免 OpenSearch 節點遭到不必要的驅逐。

```yaml
spec:
  nodePools:
    - component: masters
      replicas: 3
      diskSize: "5Gi"
      priorityClassName: somePriorityClassName
      resources:
        requests:
          memory: "2Gi"
          cpu: "500m"
        limits:
          memory: "2Gi"
          cpu: "500m"
      roles:
        - "master"
```
{% include copy.html %}

## Pod 親和性

根據預設，operator 會套用 Pod 反親和性規則，以防止同一個 OpenSearch 叢集的多個 Pod 排程到同一個節點上。這可降低單一節點故障影響多個 Pod 的風險，進而提升高可用性。

預設的反親和性使用 `PreferredDuringSchedulingIgnoredDuringExecution`，這是一種軟性偏好設定：如果沒有其他可用節點，它不會阻止排程，但會優先將 Pod 分散到不同節點。

您可以在節點集區、bootstrap 或 OpenSearch Dashboards 組態中明確設定 `affinity` 欄位，以覆寫此預設行為：

```yaml
spec:
  nodePools:
    - component: masters
      replicas: 3
      diskSize: "30Gi"
      roles:
        - "master"
        - "data"
      affinity:
        podAntiAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            - labelSelector:
                matchLabels:
                  opensearch.org/opensearch-cluster: my-cluster
              topologyKey: kubernetes.io/hostname
  bootstrap:
    affinity:
      podAntiAffinity:
        preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            podAffinityTerm:
              labelSelector:
                matchLabels:
                  opensearch.org/opensearch-cluster: my-cluster
              topologyKey: kubernetes.io/hostname
  dashboards:
    enable: true
    affinity:
      podAffinity:
        preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            podAffinityTerm:
              labelSelector:
                matchLabels:
                  app: opensearch-dashboards
              topologyKey: kubernetes.io/zone
```
{% include copy.html %}

如果您設定了明確的 `affinity`，它會完全取代預設的反親和性行為。若要完全停用反親和性，請設定 `affinity: {}`。

## Sidecar 容器

您可以在同一個 Pod 中，與 OpenSearch 一起部署額外的 sidecar 容器。這適用於記錄檔傳送、監控代理程式，或其他需要與 OpenSearch 節點一起執行的輔助服務。

```yaml
spec:
  nodePools:
    - component: masters
      replicas: 3
      diskSize: "30Gi"
      resources:
        requests:
          memory: "2Gi"
          cpu: "500m"
        limits:
          memory: "2Gi"
          cpu: "500m"
      roles:
        - "master"
        - "data"
      sidecarContainers:
        - name: log-shipper
          image: fluent/fluent-bit:latest
          resources:
            requests:
              memory: "64Mi"
              cpu: "100m"
            limits:
              memory: "128Mi"
              cpu: "200m"
          volumeMounts:
            - name: varlog
              mountPath: /var/log
        - name: monitoring-agent
          image: prometheus/node-exporter:latest
          ports:
            - containerPort: 9100
              name: metrics
```
{% include copy.html %}

由於 sidecar 容器與 OpenSearch 容器在同一個 Pod 中執行，因此它們共用相同的網路命名空間與儲存磁碟區。

## 額外的磁碟區

您可以將額外的磁碟區掛載到 OpenSearch Pod 中，以提供額外的組態（例如外掛程式的組態檔案）。支援的磁碟區類型包括 `ConfigMap`、`Secret`、`emptyDir`、投射磁碟區（projected volume）以及 CSI 磁碟區。

請在 `spec.general.additionalVolumes` 或 `spec.dashboards.additionalVolumes` 中提供額外磁碟區的陣列：

```yaml
spec:
  general:
    additionalVolumes:
      - name: example-configmap
        path: /path/to/mount/volume
        #subPath: mykey # Add this to mount only a specific key of the configmap/secret
        configMap:
          name: config-map-name
        restartPods: true # Set this to true to restart the pods when the content of the configMap changes
      - name: temp
        path: /tmp
        emptyDir: {}
      - name: example-csi-volume
        path: /path/to/mount/volume
        #subPath: "subpath" # Add this to mount the CSI volume at a specific subpath
        csi:
          driver: csi-driver-name
          readOnly: true
          volumeAttributes:
            secretProviderClass: example-secret-provider-class
      - name: example-projected-volume
        path: /path/to/mount/volume
        projected:
          sources:
            - serviceAccountToken:
                path: "token"
      - name: example-persistentvolumeclaim-volume
        path: /path/to/mount/volume
        persistentVolumeClaim:
          claimName: claim-name
      - name: nfs-volume
        path: /mnt/backups/opensearch
        nfs:
          server: 192.168.1.233
          path: /export/backups/opensearch
          readOnly: false # Optional, defaults to false
  dashboards:
    additionalVolumes:
      - name: example-secret
        path: /path/to/mount/volume
        secret:
          secretName: secret-name
```
{% include copy.html %}

### NFS 磁碟區支援

NFS 磁碟區可以直接掛載到 OpenSearch Pod 中，不需要外部佈建程式或 CSI 驅動程式。這對於儲存在 NFS 共用上的快照儲存庫特別有用。若要設定 NFS 磁碟區，請指定 `nfs` 欄位，並提供必要的 `server` 與 `path` 參數：

```yaml
spec:
  general:
    additionalVolumes:
      - name: nfs-backups
        path: /mnt/backups/opensearch
        nfs:
          server: 192.168.1.233
          path: /export/backups/opensearch
          readOnly: false # Optional, defaults to false
```
{% include copy.html %}

這可以與快照儲存庫組態結合使用：

```yaml
spec:
  general:
    additionalVolumes:
      - name: nfs-backups
        path: /mnt/backups/opensearch
        nfs:
          server: 192.168.1.233
          path: /export/backups/opensearch
    snapshotRepositories:
      - name: nfs-repository
        type: fs
        settings:
          location: /mnt/backups/opensearch
```
{% include copy.html %}

Operator 會將定義的磁碟區新增至 OpenSearch 叢集的所有 Pod。目前無法針對個別節點集區（`nodePools`）定義磁碟區。

## 將環境變數新增至 Pod

您可以將自己的環境變數新增至 OpenSearch Pod 與 OpenSearch Dashboards Pod。您可以將值提供為字串常值，或從 secret 或 `ConfigMap` 掛載。

OpenSearch 與 OpenSearch Dashboards 的結構相同：

```yaml
spec:
  dashboards:
    env:
      - name: MY_ENV_VAR
        value: "myvalue"
      - name: MY_SECRET_VAR
        valueFrom:
          secretKeyRef:
            name: my-secret
            key: some_key
      - name: MY_CONFIGMAP_VAR
        valueFrom:
          configMapKeyRef:
            name: my-configmap
            key: some_key
  nodePools:
    - component: nodes
      env:
        - name: MY_ENV_VAR
          value: "myvalue"
        # The other options are supported here as well.
```
{% include copy.html %}

## 自訂叢集網域名稱

如果您的 Kubernetes 叢集設定了自訂網域名稱（預設為 `cluster.local`），請相應地設定 operator，內部路由才能正常運作。請在 Helm chart 值中設定 `manager.dnsBase`。

```yaml
manager:
  # ...
  dnsBase: custom.domain
```
{% include copy.html %}

## 自訂 init helper

在叢集初始化期間，operator 會使用 init 容器作為輔助程式。這些容器使用 `busybox` 映像檔（具體而言為 `docker.io/busybox:latest`）。如果您在離線環境中工作，且叢集無法存取登錄檔，或者您想要自訂映像檔，可以在叢集 `spec` 中指定 `initHelper` 映像檔，以覆寫所使用的映像檔：

```yaml
spec:
  initHelper:
    # You can either only specify the version
    version: "1.27.2-buildcustom"
    # Or specify a totally different image
    image: "mycustomrepo.cr/mycustombusybox:myversion"
    # Additionally you can define the imagePullPolicy
    imagePullPolicy: IfNotPresent
    # and imagePullSecrets if needed
    imagePullSecrets:
      - name: docker-pull-secret
```
{% include copy.html %}

## 編輯 init 容器資源

Init 容器在執行時沒有任何資源限制，但您可以在 YAML 定義中新增 resources 區段，以指定資源請求與限制。透過設定適當的資源限制，您可以控制配置給 init 容器的 CPU 與記憶體數量，有助於確保它不會讓其他容器資源匱乏。

```yaml
spec:
  initHelper:
    resources:
      requests:
        memory: "128Mi"
        cpu: "250m"
      limits:
        memory: "512Mi"
        cpu: "500m"
```
{% include copy.html %}

## 停用 init helper

在某些情況下，您可能想要避免使用 `chmod` init 容器（例如在 OpenShift 上，或者您的叢集會封鎖以 `root` 身分執行的容器）。
您可以在 `values.yaml` 中新增以下內容來停用它：

```yaml
manager:
  extraEnv:
    - name: SKIP_INIT_CONTAINER
      value: "true"
```
{% include copy.html %}

## PodDisruptionBudget

PDB（Pod Disruption Budget）是一種 Kubernetes 資源，透過定義維護期間或非預期事件發生時可接受的中斷程度，協助確保應用程式的高可用性。
它會指定必須維持可用的最少 Pod 數量，以維持所需的服務水準。
每個節點集區（`nodePools`）的 PDB 定義都是唯一的。
請提供 `minAvailable` 或 `maxUnavailable` 其中之一來設定 PDB，但不能同時提供兩者。

```yaml
apiVersion: opensearch.org/v1
kind: OpenSearchCluster
---
spec:
  nodePools:
    - component: masters
      replicas: 3
      diskSize: "30Gi"
      pdb:
        enable: true
        minAvailable: 3
    - component: datas
      replicas: 7
      diskSize: "100Gi"
      pdb:
        enable: true
        maxUnavailable: 2
```
{% include copy.html %}

## 公開 OpenSearch Dashboards

若要將叢集的 OpenSearch Dashboards 執行個體公開給 Kubernetes 叢集外部的使用者或服務，建議的方式是使用 Ingress。

簡單範例：

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: opensearch-dashboards
  namespace: default
spec:
  tls:
    - hosts:
        - dashboards.my.company
  rules:
    - host: dashboards.my.company
      http:
        paths:
          - backend:
              service:
                name: my-cluster-dashboards
                port:
                  number: 5601
            path: "/(.*)"
            pathType: ImplementationSpecific
```
{% include copy.html %}

如果您已為 OpenSearch Dashboards 啟用 HTTPS，請指示您的 Ingress 控制器在內部使用 HTTPS 連線。這取決於您所使用的控制器（例如 nginx-ingress 或 `traefik`）。
{: .note}

## 設定 OpenSearch Dashboards Kubernetes 服務

您可以自訂 Operator 為 OpenSearch Dashboards 部署所產生的 Kubernetes Service 物件。

支援的 Service 類型：

- ClusterIP（預設）
- NodePort
- LoadBalancer

使用 `LoadBalancer` 類型時，您可以選擇性地設定負載平衡器的來源範圍。

```yaml
apiVersion: opensearch.org/v1
kind: OpenSearchCluster
---
spec:
  dashboards:
    service:
      type: LoadBalancer # Set one of the supported types
      loadBalancerSourceRanges: "10.0.0.0/24, 192.168.0.0/24" # Optional, add source ranges for a load balancer
```
{% include copy.html %}

## 公開 OpenSearch 叢集 REST API

若要將 OpenSearch 的 REST API 公開到 Kubernetes 叢集外部，建議的方式是使用 Ingress。
在內部使用自我簽署憑證（您可以讓 Operator 產生這些憑證），然後讓 Ingress 使用由受信任 CA（例如 Let's Encrypt 或公司內部 CA）簽發的憑證。如此一來，您就不必費心為 OpenSearch 叢集提供自訂憑證，而您的使用者仍會看到有效的憑證。

## 自訂探查逾時與閾值

如果叢集節點未在達到閾值之前啟動，導致 Pod 重新啟動，您可以視需要為每個節點設定逾時與閾值。

```yaml
apiVersion: opensearch.org/v1
kind: OpenSearchCluster
---
spec:
  nodePools:
    - component: masters
      replicas: 3
      diskSize: "30Gi"
      probes:
        liveness:
          initialDelaySeconds: 10
          periodSeconds: 20
          timeoutSeconds: 5
          successThreshold: 1
          failureThreshold: 10
        startup:
          initialDelaySeconds: 10
          periodSeconds: 20
          timeoutSeconds: 5
          successThreshold: 1
          failureThreshold: 10
        readiness:
          initialDelaySeconds: 60
          periodSeconds: 30
          timeoutSeconds: 30
          successThreshold: 1
          failureThreshold: 5
```
{% include copy.html %}

## 自訂啟動與就緒探查命令

`liveness` 探查是 TCP 檢查，而啟動與就緒探查則是透過 cURL 使用 OpenSearch API。

如果您需要自訂啟動或就緒探查命令，可以如下列範例所示覆寫這些命令：

```yaml
apiVersion: opensearch.org/v1
kind: OpenSearchCluster
...
spec:
  nodePools:
    - component: masters
      ...
      probes:
        startup:
          command:
            - echo
            - "Hello, World!"
        readiness:
          command:
            - echo
            - "Hello, World!"
```
{% include copy.html %}

## 設定資源限制與請求

除了前面各節中關於如何為節點集區指定資源需求的資訊之外，您也可以針對進階使用案例，為 Operator 所建立的所有實體指定資源。

Operator 會透過 Job、StatefulSet 和 ReplicaSet 等資源產生許多 Pod，而這些資源會使用 init 容器。下列組態可讓您為所有 init 容器指定預設的資源組態。

```yaml
apiVersion: opensearch.org/v1
kind: OpenSearchCluster
---
spec:
  initHelper:
    resources:
      requests:
        memory: "50Mi"
        cpu: "50m"
      limits:
        memory: "200Mi"
        cpu: "200m"
```
{% include copy.html %}

您也可以如下列範例所示，設定安全性更新作業的資源。

```yaml
apiVersion: opensearch.org/v1
kind: OpenSearchCluster
---
spec:
  security:
    config:
      updateJob:
        resources:
          limits:
            cpu: "100m"
            memory: "100Mi"
          requests:
            cpu: "100m"
            memory: "100Mi"
```
{% include copy.html %}

此處提供的範例並未反映實際的資源需求。您可能需要進行進一步測試，才能根據您的特定需求適當調整資源。
{: .note}
