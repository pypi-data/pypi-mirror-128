# Heureka 'Overené zákazníkmi' Python module


[Heureka Overené zákazníkmi](https://www.overenezakaznikmi.sk/) (ShopCertification) service API implementation for Python

Usage
-----

Import class `heureka_overene.ShopCertification` using [your API key](https://sluzby.heureka.sk/napoveda/co-je-sluzba-overene-zakaznikmi/) for login.

Basic usage of ShopCertification

```python
from heureka_overene import ShopCertification, HeurekaService

# Slovak shop initialization
shop_certification = ShopCertification(api_key='Your API key', email='Your email', service=HeurekaService.SK)
# Czech shop initialization
shop_certification = ShopCertification(api_key='Your API key', email='Your email', service=HeurekaService.CZ)

# log order
certification.log_order()
```

Set the customer order ID (only integers are allowed):

```python
certification.order_id = 12345
```

Add products id from the customer order. (Use IDs which you use in ITEM_ID field of the [Heureka XML feed](https://sluzby.heureka.sk/napoveda/xml-feed/))

```python
certification.add_product_id('PROD-124')
```
