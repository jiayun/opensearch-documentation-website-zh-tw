---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "使用自訂邏輯產生資料"
nav_order: 35
parent: Synthetic data generation
grand_parent: Additional features
---

# 使用自訂邏輯產生資料

您可以使用定義於 Python 模組中的自訂邏輯來產生合成資料。這種方法可讓您對 OpenSearch Benchmark 產生合成資料的方式進行最細微的控制。如果您了解資料的分布以及不同欄位之間的關係，這種方法尤其實用。

## generate_synthetic_document 函式

提供給 OpenSearch Benchmark 的每個自訂模組都必須定義 `generate_synthetic_document(providers, **custom_lists)` 函式。此函式會定義 OpenSearch Benchmark 如何產生每份合成文件。

### 函式參數

| 參數 | 必要/選用 | 說明 |
|---|---|---|
| `providers` | 必要 | 包含資料產生工具的字典。可用的提供者有 `generic` (Mimesis [通用提供者](https://mimesis.name/master/api.html#generic-providers)) 和 `random` (Mimesis [Random 類別](https://mimesis.name/master/random_and_seed.html))。若要新增自訂提供者，請參閱[進階組態](#advanced-configuration)。 |
| `custom_lists` | 選用 | 關鍵字引數，包含預先定義的值清單，您可以在資料產生邏輯中使用這些值。這些值定義於 YAML 組態檔中的 `custom_lists` 之下，可讓您將資料值與 Python 程式碼分開。例如，如果您在 YAML 中定義 `dog_names: [Buddy, Max, Luna]`，您可以在函式中以 `custom_lists['dog_names']` 存取它。這讓您不必變更 Python 程式碼就能輕鬆修改資料值。 |

### 基本函式範本

```python
def generate_synthetic_document(providers, **custom_lists):
    # Access the available providers
    generic = providers['generic']
    random_provider = providers['random']

    # Generate a document using the providers
    document = {
        'name': generic.person.full_name(),
        'age': random_provider.randint(18, 80),
        'email': generic.person.email(),
        'timestamp': generic.datetime.datetime()
    }

    # Optionally, use custom lists if provided
    if 'categories' in custom_lists:
        document['category'] = random_provider.choice(custom_lists['categories'])

    return document
```
{% include copy.html %}

如需更多資訊，請參閱 [Mimesis 文件](https://mimesis.name/master/api.html)。

## Python 模組範例

下列 Python 模組範例示範如何為一家虛構的共乘公司 *Pawber* 產生關於狗狗駕駛的文件，該公司使用 OpenSearch 來儲存及搜尋大量的共乘資料。

此範例展示了幾項進階概念：
- **[自訂提供者類別](#advanced-configuration)** (`NumericString`、`MultipleChoices`)，可擴充 Mimesis 功能
- **[自訂清單](#advanced-configuration)**，用於狗狗名字、品種和零食等資料值 (以 `custom_lists['dog_names']` 參照)
- **地理叢集**邏輯，用於產生逼真的位置資料
- **複雜的文件結構**，包含巢狀物件與關聯性

將此程式碼儲存到您所需目錄中的 `pawber.py` 檔案 (例如 `~/pawber.py`)：

```python
from mimesis.providers.base import BaseProvider
from mimesis.enums import TimestampFormat

import random

GEOGRAPHIC_CLUSTERS = {
    'Manhattan': {
        'center': {'lat': 40.7831, 'lon': -73.9712},
        'radius': 0.05  # degrees
    },
    'Brooklyn': {
        'center': {'lat': 40.6782, 'lon': -73.9442},
        'radius': 0.05
    },
    'Austin': {
        'center': {'lat': 30.2672, 'lon': -97.7431},
        'radius': 0.1  # Increased radius to cover more of Austin
    }
}

def generate_location(cluster):
    """Generate a random location within a cluster"""
    center = GEOGRAPHIC_CLUSTERS[cluster]['center']
    radius = GEOGRAPHIC_CLUSTERS[cluster]['radius']
    lat = center['lat'] + random.uniform(-radius, radius)
    lon = center['lon'] + random.uniform(-radius, radius)
    return {'lat': lat, 'lon': lon}

class NumericString(BaseProvider):
    class Meta:
        name = "numeric_string"

    @staticmethod
    def generate(length=5) -> str:
        return ''.join([str(random.randint(0, 9)) for _ in range(length)])

class MultipleChoices(BaseProvider):
    class Meta:
        name = "multiple_choices"

    @staticmethod
    def generate(choices, num_of_choices=5) -> str:
        import logging
        logger = logging.getLogger(__name__)
        logger.info("Choices: %s", choices)
        logger.info("Length: %s", num_of_choices)
        total_choices_available = len(choices) - 1

        return [choices[random.randint(0, total_choices_available)] for _ in range(num_of_choices)]

def generate_synthetic_document(providers, **custom_lists):
    generic = providers['generic']
    random_mimesis = providers['random']

    first_name = generic.person.first_name()
    last_name = generic.person.last_name()
    city = random.choice(list(GEOGRAPHIC_CLUSTERS.keys()))

    # Driver Document
    document = {
        "dog_driver_id": f"DD{generic.numeric_string.generate(length=4)}",
        "dog_name": random_mimesis.choice(custom_lists['dog_names']),
        "dog_breed": random_mimesis.choice(custom_lists['dog_breeds']),
        "license_number": f"{random_mimesis.choice(custom_lists['license_plates'])}{generic.numeric_string.generate(length=4)}",
        "favorite_treats": random_mimesis.choice(custom_lists['treats']),
        "preferred_tip": random_mimesis.choice(custom_lists['tips']),
        "vehicle_type": random_mimesis.choice(custom_lists['vehicle_types']),
        "vehicle_make": random_mimesis.choice(custom_lists['vehicle_makes']),
        "vehicle_model": random_mimesis.choice(custom_lists['vehicle_models']),
        "vehicle_year": random_mimesis.choice(custom_lists['vehicle_years']),
        "vehicle_color": random_mimesis.choice(custom_lists['vehicle_colors']),
        "license_plate": random_mimesis.choice(custom_lists['license_plates']),
        "current_location": generate_location(city),
        "status": random.choice(['available', 'busy', 'offline']),
        "current_ride": f"R{generic.numeric_string.generate(length=6)}",
        "account_status": random_mimesis.choice(custom_lists['account_status']),
        "join_date": generic.datetime.formatted_date(),
        "total_rides": generic.numeric.integer_number(start=1, end=200),
        "rating": generic.numeric.float_number(start=1.0, end=5.0, precision=2),
        "earnings": {
            "today": {
                "amount": generic.numeric.float_number(start=1.0, end=5.0, precision=2),
                "currency": "USD"
            },
            "this_week": {
                "amount": generic.numeric.float_number(start=1.0, end=5.0, precision=2),
                "currency": "USD"
            },
            "this_month": {
                "amount": generic.numeric.float_number(start=1.0, end=5.0, precision=2),
                "currency": "USD"
            }
        },
        "last_grooming_check": "2023-12-01",
        "owner": {
            "first_name": first_name,
            "last_name": last_name,
            "email": f"{first_name}{last_name}@gmail.com"
        },
        "special_skills": generic.multiple_choices.generate(custom_lists['skills'], num_of_choices=3),
        "bark_volume": generic.numeric.float_number(start=1.0, end=10.0, precision=2),
        "tail_wag_speed": generic.numeric.float_number(start=1.0, end=10.0, precision=1)
    }

    return document
```
{% include copy.html %}

## 產生資料

若要使用自訂邏輯產生合成資料，請使用 `generate-data` 子命令，並提供所需的自訂 Python 模組、索引名稱、輸出路徑，以及要產生的資料總量：

```shell
osb generate-data --custom-module ~/pawber.py --index-name pawber-data --output-path ~/Desktop/sdg_outputs/ --total-size 2
```
{% include copy.html %}

如需可用參數的完整清單及其說明，請參閱 [`generate-data` 命令參考]({{site.url}}{{site.baseurl}}/benchmark/reference/commands/generate-data/)。

## 範例輸出

以下是產生 100 GB 資料時的範例輸出：

```
   ____                  _____                      __       ____                  __                         __
  / __ \____  ___  ____ / ___/___  ____ ___________/ /_     / __ )___  ____  _____/ /_  ____ ___  ____ ______/ /__
 / / / / __ \/ _ \/ __ \\__ \/ _ \/ __ `/ ___/ ___/ __ \   / __  / _ \/ __ \/ ___/ __ \/ __ `__ \/ __ `/ ___/ //_/
/ /_/ / /_/ /  __/ / / /__/ /  __/ /_/ / /  / /__/ / / /  / /_/ /  __/ / / / /__/ / / / / / / / / /_/ / /  / ,<
\____/ .___/\___/_/ /_/____/\___/\__,_/_/   \___/_/ /_/  /_____/\___/_/ /_/\___/_/ /_/_/ /_/ /_/\__,_/_/  /_/|_|
    /_/


[NOTE] ✨ Dashboard link to monitor processes and task streams: [http://127.0.0.1:8787/status]
[NOTE] ✨ For users who are running generation on a virtual machine, consider SSH port forwarding (tunneling) to localhost to view dashboard.
[NOTE] Example of localhost command for SSH port forwarding (tunneling) from an AWS EC2 instance:
ssh -i <PEM_FILEPATH> -N -L localhost:8787:localhost:8787 ec2-user@<DNS>

Total GB to generate: [1]
Average document size in bytes: [412]
Max file size in GB: [40]

100%|███████████████████████████████████████████████████████████████████| 100.07G/100.07G [3:35:29<00:00, 3.98MB/s]

Generated 24271844660 docs in 12000 seconds. Total dataset size is 100.21GB.
✅ Visit the following path to view synthetically generated data: /home/ec2-user/

-----------------------------------
[INFO] ✅ SUCCESS (took 272 seconds)
-----------------------------------
```

## 進階組態

您可以選擇性地建立 YAML 組態檔來儲存自訂資料與提供者。組態檔必須定義 `CustomGenerationValues` 參數。

`CustomGenerationValues` 中提供下列參數。這兩個參數皆為選用。

| 參數 | 必要/選用 | 說明 |
|---|---|---|
| `custom_lists` | 選用 | 預先定義的值陣列，您可以在 Python 模組中使用 `custom_lists['list_name']` 來參照。這可讓您將資料值與程式碼邏輯分離，方便在不修改 Python 檔案的情況下變更資料值。例如，`dog_names: [Buddy, Max, Luna]` 會以 `custom_lists['dog_names']` 的形式存取。 |
| `custom_providers` | 選用 | 擴充 Mimesis 功能的自訂資料產生類別。這些類別應定義在您的 Python 模組中（例如[範例](#python-module-example)中的 `NumericString` 或 `MultipleChoices`），然後在此參數中依名稱列出。這可讓您建立超出 Mimesis 預設功能的專門資料產生器。 |

### 範例組態檔

將您的組態儲存在 YAML 檔案中：

```yml
CustomGenerationValues:
  # Generate data using a custom Python module
  custom_lists:
  # Custom lists to consolidate all values in this YAML file
    dog_names: [Hana, Youpie, Charlie, Lucy, Cooper, Luna, Rocky, Daisy, Buddy, Molly]
    dog_breeds: [Jindo, Labrador, German Shepherd, Golden Retriever, Bulldog, Poodle, Beagle, Rottweiler, Boxer, Dachshund, Chihuahua]
    treats: [cookies, pup_cup, jerky]
  custom_providers:
  # OSB's synthetic data generator uses Mimesis; custom providers are essentially custom Python classes that adds more functionality to Mimesis
    - NumericString
    - MultipleChoices
```
{% include copy.html %}


### 使用組態

若要使用您的組態檔，請在 `generate-data` 命令中加入 `--custom-config` 參數：

```shell
osb generate-data --custom-module ~/pawber.py --index-name pawber-data --output-path ~/Desktop/sdg_outputs/ --total-size 2 --custom-config ~/Desktop/sdg-config.yml
```
{% include copy.html %}

## 相關文件

- [`generate-data` 命令參考]({{site.url}}{{site.baseurl}}/benchmark/reference/commands/generate-data/)
- [使用索引對應產生資料]({{site.url}}{{site.baseurl}}/benchmark/features/synthetic-data-generation/mapping-sdg/)
