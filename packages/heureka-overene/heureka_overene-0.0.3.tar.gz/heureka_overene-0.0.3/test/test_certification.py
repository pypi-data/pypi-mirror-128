import json
from unittest import TestCase

import httpretty
import pytest
from heureka_overene import ShopCertification, HeurekaService

INVALID_INIT_PARAMETERS = [
	('', 'test@test.sk'),
	(None, 'test@test.sk'),
	('asdlfkasdf', 'test.sk'),
	('asdfasdfa', '@@test.sk')
]


@pytest.mark.parametrize('key,email', INVALID_INIT_PARAMETERS)
def test_invalid_init_paramenters(key, email):
	with pytest.raises(ValueError) as e:
		ShopCertification(key, email)


@pytest.mark.parametrize('order_id', [ 'asdf', '23b', None, ])
def test_invalid_order_ids(order_id):
	shop_certification = ShopCertification('adsfasdfasdf', 'test@test.sk')
	with pytest.raises(TypeError) as e:
		shop_certification.order_id = order_id


@pytest.mark.parametrize('email',['info@google.com', 'info@test.local'])
def test_valid_init_email(email):
	ShopCertification('adsfasdfasdf', email)


@httpretty.activate(allow_net_connect=False)
def test_send_base():
	api_url = 'https://api.heureka.cz/shop-certification/v2/order/log'
	httpretty.register_uri(httpretty.POST, api_url, status=200, body='{"code": 200, "message": "ok"}')
	shop_certification = ShopCertification('adsfasdfasdf', 'info@info.sk', service=HeurekaService.CZ)
	assert True == shop_certification.log_order()
	last_request = httpretty.last_request()
	assert 'Content-type' in last_request.headers
	assert 'application/json' in last_request.headers['Content-type']


@httpretty.activate(allow_net_connect=False)
def test_invalid_auth():
	api_url = 'https://api.heureka.cz/shop-certification/v2/order/log'
	response_data = '{ "code": 401, "message": "unauthorized", "description": "Unknown API key" }'
	httpretty.register_uri(httpretty.POST, api_url, status=401, body=response_data)
	shop_certification = ShopCertification('adsfasdfasdf', 'info@info.sk', service=HeurekaService.CZ)
	assert False == shop_certification.log_order()


def test_invalid_product_id():
	certification = ShopCertification('alskdjfasdf', 'test@test.sk')
	with pytest.raises(ValueError):
		certification.add_product_id('')
	with pytest.raises(ValueError):
		certification.add_product_id(None)
	certification.add_product_id('PORD-12')
	with pytest.raises(ValueError):
		certification.add_product_id('PORD-12')


@httpretty.activate(allow_net_connect=False, verbose=True)
def test_send_full_data():
	httpretty.register_uri(httpretty.POST, 'https://api.heureka.sk/shop-certification/v2/order/log', responses=200, body='{"code": 200, "message": "ok"}')

	API_KEY = 'asdflaksdfasdf'
	EMIAL = 'test@test.sk'
	ORDER_ID = 2342
	PRODUCTS_IDS = ['123', '234234', 'ad23423']
	shop_certification = ShopCertification(API_KEY, EMIAL)
	for pk in PRODUCTS_IDS:
		shop_certification.add_product_id(pk)
	shop_certification.order_id = ORDER_ID
	assert True == shop_certification.log_order()
	last_request = httpretty.last_request()
	TestCase().assertDictEqual({
		"apiKey": API_KEY,
		"email": EMIAL,
		"orderId": ORDER_ID,
		"productItemIds": PRODUCTS_IDS
	}, json.loads(last_request.body))

	with pytest.raises(RuntimeError):
		shop_certification.log_order()
