# Saby Vok API Client

## Installation

```sh
pip install sabyvok
```

## Usage

```python
from sabyvok import SabyVokClient

client = SabyVokClient(
    "your_client_id",
    "your_client_secret",
    "your_secret_key",
)
data = client.req(inn='7605016030')
print(data[0]['company_name'])  # Компания "Тензор", ООО

```