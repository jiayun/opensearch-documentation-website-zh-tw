---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "GPU 加速"
parent: Using ML models within OpenSearch
grand_parent: Integrating ML models
nav_order: 150
---


# GPU 加速

在 OpenSearch 叢集中使用機器學習 (ML) 節點執行自然語言處理 (NLP) 模型時，您可以透過圖形處理器 (GPU) 加速，在 ML 節點上獲得更佳的效能。GPU 可與叢集的 CPU 協同運作，加快模型上傳與訓練的速度。

## 支援的 GPU

ML 節點支援下列 GPU 執行個體：

- [搭載 CUDA 11.6 的 NVIDIA 執行個體](https://aws.amazon.com/nvidia/)
- [AWS Inferentia](https://aws.amazon.com/machine-learning/inferentia/)

如果您需要 GPU 運算能力，可以透過 [Amazon Elastic Compute Cloud (Amazon EC2)](https://aws.amazon.com/ec2/) 佈建 GPU 執行個體。如需如何佈建 GPU 執行個體的詳細資訊，請參閱[建議的 GPU 執行個體](https://docs.aws.amazon.com/dlami/latest/devguide/gpu.html)。

## 支援的映像

您可以在搭載 CUDA 11.6 的 [Docker 映像](https://gitlab.com/nvidia/container-images/cuda/blob/master/doc/supported-tags.md)以及 [Amazon Machine Images (AMI)](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/AMIs.html) 上使用 GPU 加速。

## PyTorch

GPU 加速的 ML 節點需要 [PyTorch](https://pytorch.org/docs/stable/index.html) 1.12.1 才能與 ML 模型搭配運作。

## 設定 GPU 加速的 ML 節點

視 GPU 而定，您可以手動佈建 GPU 加速的 ML 節點，或使用自動初始化指令碼。

### 準備 NVIDIA ML 節點

NVIDIA 使用 CUDA 來提升節點效能。為了善用 CUDA，您必須確認驅動程式在 `/dev` 目錄中包含 `nvidia-uvm` 核心。若要檢查核心，請輸入 `ls -al /dev | grep nvidia-uvm`。

如果 `nvidia-uvm` 核心不存在，請執行 `nvidia-uvm-init.sh`：

```bash
#!/bin/bash
## Script to initialize nvidia device nodes.
## https://docs.nvidia.com/cuda/cuda-installation-guide-linux/index.html#runfile-verifications
/sbin/modprobe nvidia
if [ "$?" -eq 0 ]; then
  # Count the number of NVIDIA controllers found.
  NVDEVS=`lspci | grep -i NVIDIA`
  N3D=`echo "$NVDEVS" | grep "3D controller" | wc -l`
  NVGA=`echo "$NVDEVS" | grep "VGA compatible controller" | wc -l`
  N=`expr $N3D + $NVGA - 1`
  for i in `seq 0 $N`; do
    mknod -m 666 /dev/nvidia$i c 195 $i
  done
  mknod -m 666 /dev/nvidiactl c 195 255
else
  exit 1
fi
/sbin/modprobe nvidia-uvm
if [ "$?" -eq 0 ]; then
  # Find out the major device number used by the nvidia-uvm driver
  D=`grep nvidia-uvm /proc/devices | awk '{print $1}'`
  mknod -m 666 /dev/nvidia-uvm c $D 0
  mknod -m 666 /dev/nvidia-uvm-tools c $D 0
else
  exit 1
fi
```

如果您使用 OpenSearch 的封裝版本以原生方式 (不使用 Docker) 執行 OpenSearch，`systemd` 可能會阻止 OpenSearch 存取您的 GPU。若要加速模型，您需要可正常運作的 [CUDA Toolkit](https://developer.nvidia.com/cuda-toolkit) 安裝，並能存取 `/dev` 下的 NVIDIA 裝置。

若要允許 OpenSearch 使用 GPU，請新增下列組態來更新 `systemd` 服務：

```ini
systemctl edit opensearch.service

[Service]
DevicePolicy=auto
``` 


確認 `/dev` 下存在 `nvidia-uvm` 之後，您就可以在叢集中啟動 OpenSearch。

### 準備 AWS Inferentia ML 節點

視 AWS Inferentia 上執行的 Linux 作業系統而定，您可以使用下列命令與指令碼來佈建 ML 節點，並在叢集中執行 OpenSearch。

首先，請在您的叢集上[下載並安裝 OpenSearch]({{site.url}}{{site.baseurl}}/install-and-configure/index/)。

接著匯出 OpenSearch 並設定您的環境變數。此範例將 OpenSearch 匯出至 `opensearch-2.5.0` 目錄，因此 `OPENSEARCH_HOME` = `opensearch-2.5.0`：

```bash
echo "export OPENSEARCH_HOME=~/opensearch-2.5.0" | tee -a ~/.bash_profile
echo "export PYTORCH_VERSION=1.12.1" | tee -a ~/.bash_profile
source ~/.bash_profile
```

接下來，建立名為 `prepare_torch_neuron.sh` 的 shell 指令碼檔案。您可以根據您的 Linux 作業系統，複製並自訂下列其中一個範例：

- [Ubuntu 20.04](#ubuntu-2004)
- [Amazon Linux 2](#amazon-linux-2)

執行指令碼後，請結束目前的終端機，並開啟新的終端機來啟動 OpenSearch。

GPU 加速僅在 Ubuntu 20.04 與 Amazon Linux 2 上測試過。不過，您可以使用其他 Linux 作業系統。
{: .note}

#### Ubuntu 20.04

```bash
. /etc/os-release
sudo tee /etc/apt/sources.list.d/neuron.list > /dev/null <<EOF
deb https://apt.repos.neuron.amazonaws.com ${VERSION_CODENAME} main
EOF
wget -qO - https://apt.repos.neuron.amazonaws.com/GPG-PUB-KEY-AMAZON-AWS-NEURON.PUB | sudo apt-key add -

# Update OS packages
sudo apt-get update -y

################################################################################################################
# To install or update to Neuron versions 1.19.1 and newer from previous releases:
# - DO NOT skip 'aws-neuron-dkms' install or upgrade step, you MUST install or upgrade to latest Neuron driver
################################################################################################################

# Install OS headers
sudo apt-get install linux-headers-$(uname -r) -y

# Install Neuron Driver
sudo apt-get install aws-neuronx-dkms -y

####################################################################################
# Warning: If Linux kernel is updated as a result of OS package update
#          Neuron driver (aws-neuron-dkms) should be re-installed after reboot
####################################################################################

# Install Neuron Tools
sudo apt-get install aws-neuronx-tools -y

######################################################
#   Only for Ubuntu 20 - Install Python3.7
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt-get install python3.7
######################################################
# Install Python venv and activate Python virtual environment to install    
# Neuron pip packages.
cd ~
sudo apt-get install -y python3.7-venv g++
python3.7 -m venv pytorch_venv
source pytorch_venv/bin/activate
pip install -U pip

# Set pip repository to point to the Neuron repository
pip config set global.extra-index-url https://pip.repos.neuron.amazonaws.com

#Install Neuron PyTorch
pip install torch-neuron torchvision
# If you need to trace the neuron model, install torch neuron with this command
# pip install torch-neuron neuron-cc[tensorflow] "protobuf==3.20.1" torchvision

# If you need to trace neuron model, install the transformers for tracing the Huggingface model.
# pip install transformers

# Copy torch neuron lib to OpenSearch
PYTORCH_NEURON_LIB_PATH=~/pytorch_venv/lib/python3.7/site-packages/torch_neuron/lib/
mkdir -p $OPENSEARCH_HOME/lib/torch_neuron; cp -r $PYTORCH_NEURON_LIB_PATH/ $OPENSEARCH_HOME/lib/torch_neuron
export PYTORCH_EXTRA_LIBRARY_PATH=$OPENSEARCH_HOME/lib/torch_neuron/lib/libtorchneuron.so
echo "export PYTORCH_EXTRA_LIBRARY_PATH=$OPENSEARCH_HOME/lib/torch_neuron/lib/libtorchneuron.so" | tee -a ~/.bash_profile

# Increase JVm stack size to >=2MB
echo "-Xss2m" | tee -a $OPENSEARCH_HOME/config/jvm.options
# Increase max file descriptors to 65535
echo "$(whoami) - nofile 65535" | sudo tee -a /etc/security/limits.conf
# max virtual memory areas vm.max_map_count to 262144
sudo sysctl -w vm.max_map_count=262144
```

#### Amazon Linux 2

```bash
# Configure Linux for Neuron repository updates
sudo tee /etc/yum.repos.d/neuron.repo > /dev/null <<EOF
[neuron]
name=Neuron YUM Repository
baseurl=https://yum.repos.neuron.amazonaws.com
enabled=1
metadata_expire=0
EOF
sudo rpm --import https://yum.repos.neuron.amazonaws.com/GPG-PUB-KEY-AMAZON-AWS-NEURON.PUB
# Update OS packages
sudo yum update -y
################################################################################################################
# To install or update to Neuron versions 1.19.1 and newer from previous releases:
# - DO NOT skip 'aws-neuron-dkms' install or upgrade step, you MUST install or upgrade to latest Neuron driver
################################################################################################################
# Install OS headers
sudo yum install kernel-devel-$(uname -r) kernel-headers-$(uname -r) -y
# Install Neuron Driver
####################################################################################
# Warning: If Linux kernel is updated as a result of OS package update
#          Neuron driver (aws-neuron-dkms) should be re-installed after reboot
####################################################################################
sudo yum install aws-neuronx-dkms -y
# Install Neuron Tools
sudo yum install aws-neuronx-tools -y

# Install Python venv and activate Python virtual environment to install    
# Neuron pip packages.
cd ~
sudo yum install -y python3.7-venv gcc-c++
python3.7 -m venv pytorch_venv
source pytorch_venv/bin/activate
pip install -U pip

# Set Pip repository  to point to the Neuron repository
pip config set global.extra-index-url https://pip.repos.neuron.amazonaws.com

# Install Neuron PyTorch
pip install torch-neuron torchvision
# If you need to trace the neuron model, install torch neuron with this command
# pip install torch-neuron neuron-cc[tensorflow] "protobuf<4" torchvision

# If you need to run the trace neuron model, install transformers for tracing Huggingface model.
# pip install transformers

# Copy torch neuron lib to OpenSearch
PYTORCH_NEURON_LIB_PATH=~/pytorch_venv/lib/python3.7/site-packages/torch_neuron/lib/
mkdir -p $OPENSEARCH_HOME/lib/torch_neuron; cp -r $PYTORCH_NEURON_LIB_PATH/ $OPENSEARCH_HOME/lib/torch_neuron
export PYTORCH_EXTRA_LIBRARY_PATH=$OPENSEARCH_HOME/lib/torch_neuron/lib/libtorchneuron.so
echo "export PYTORCH_EXTRA_LIBRARY_PATH=$OPENSEARCH_HOME/lib/torch_neuron/lib/libtorchneuron.so" | tee -a ~/.bash_profile
# Increase JVm stack size to >=2MB
echo "-Xss2m" | tee -a $OPENSEARCH_HOME/config/jvm.options
# Increase max file descriptors to 65535
echo "$(whoami) - nofile 65535" | sudo tee -a /etc/security/limits.conf
# max virtual memory areas vm.max_map_count to 262144
sudo sysctl -w vm.max_map_count=262144
```

指令碼執行完成後，請開啟新的終端機，讓設定生效。接著，啟動 OpenSearch。

OpenSearch 現在應已在您的 GPU 加速叢集中執行。但是，如果佈建期間發生任何錯誤，您可以手動安裝 GPU 加速器驅動程式。

#### 手動準備 ML 節點

如果前述兩個指令碼未能正確佈建您的 GPU 加速節點，您可以手動安裝 AWS Inferentia 的驅動程式：

1. 根據您選擇的 Linux 作業系統部署 AWS 加速器執行個體。如需操作說明，請參閱 [PyTorch Neuron 設定](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/frameworks/torch/torch-setup.html#pytorch-neuron-setup)。

2. 將 Neuron 程式庫複製到 OpenSearch 中。下列命令使用名為 `opensearch-2.5.0` 的目錄：

   ```bash
   OPENSEARCH_HOME=~/opensearch-2.5.0
   ```

3. 設定 `PYTORCH_EXTRA_LIBRARY_PATH` 路徑。在此範例中，我們會在 OPENSEARCH_HOME 資料夾中建立 `pytorch` 虛擬環境：

   ```bash
   PYTORCH_NEURON_LIB_PATH=~/pytorch_venv/lib/python3.7/site-packages/torch_neuron/lib/


   mkdir -p $OPENSEARCH_HOME/lib/torch_neuron; cp -r  $PYTORCH_NEURON_LIB_PATH/ $OPENSEARCH_HOME/lib/torch_neuron
   export PYTORCH_EXTRA_LIBRARY_PATH=$OPENSEARCH_HOME/lib/torch_neuron/lib/libtorchneuron.so
  ```

4. （選用）若要監視加速器執行個體的 GPU 使用量，請安裝 [Neuron 工具](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/tools/neuron-sys-tools/index.html)，讓模型可以在您的執行個體中使用：

   ```bash
   # Install Neuron Tools
   sudo apt-get install aws-neuronx-tools -y
   ```

   ```bash
   # Add Neuron tools your PATH
   export PATH=/opt/aws/neuron/bin:$PATH
   ```
  
   ```bash
   # Test Neuron tools
   neuron-top
   ```


5. 為確保您有足夠的記憶體可上傳模型，請將 JVM 堆疊大小增加至 `>+2MB`：

   ```bash
   echo "-Xss2m" | sudo tee -a $OPENSEARCH_HOME/config/jvm.options
   ```

6. 啟動 OpenSearch。

## 疑難排解

由於使用 ML 模型需要大量資料，因此當您嘗試在叢集中執行 OpenSearch 時，可能會遇到下列 `max file descriptors` 或 `vm.max_map_count` 錯誤：

```bash
[1]: max file descriptors [8192] for opensearch process is too low, increase to at least [65535]
[2]: max virtual memory areas vm.max_map_count [65530] is too low, increase to at least [262144]
```

若要排解最大檔案描述元錯誤，請執行下列命令：

```bash
echo "$(whoami) - nofile 65535" | sudo tee -a /etc/security/limits.conf
```

若要修正 `vm.max_map_count` 錯誤，請執行此命令將計數增加至 `262114`：

```bash
sudo sysctl -w vm.max_map_count=262144
```

## 後續步驟

如果您想試用搭配預先訓練之 Hugging Face 模型、使用 AWS Inferentia 的 GPU 加速叢集，請參閱[預先訓練 BERT 教學](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/src/examples/pytorch/bert_tutorial/tutorial_pretrained_bert.html)。

