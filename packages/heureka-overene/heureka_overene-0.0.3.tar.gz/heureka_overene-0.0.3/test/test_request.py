# -*- coding: utf-8 -*-
from heureka_overene.request import HeurekaRequest
from heureka_overene import HeurekaApiActions, HeurekaService
import httpretty
import pytest
import json


REQUEST_URL_PARAMETERS = [
	('https://api.heureka.cz/shop-certification/v2/order/log', httpretty.GET, HeurekaService.CZ, {}, {}),
	('https://api.heureka.sk/shop-certification/v2/order/log', httpretty.GET, HeurekaService.SK, {}, {}),
	('https://api.heureka.sk/shop-certification/v2/order/log?test=fast', httpretty.GET, HeurekaService.SK, {'test': 'fast'}, {}),
	('https://api.heureka.sk/shop-certification/v2/order/log?test=fast&params=val', httpretty.GET, HeurekaService.SK, {'test': 'fast', 'params': 'val'}, {}),
	('https://api.heureka.cz/shop-certification/v2/order/log', httpretty.POST, HeurekaService.CZ, {}, {'jano': 10}),
	('https://api.heureka.sk/shop-certification/v2/order/log', httpretty.POST, HeurekaService.SK, {}, {'data': 'valid'}),
	('https://api.heureka.sk/shop-certification/v2/order/log?test=fast', httpretty.POST, HeurekaService.SK, {'test': 'fast'}, {'data': 'valid'}),
	('https://api.heureka.sk/shop-certification/v2/order/log?test=fast&params=val', httpretty.POST, HeurekaService.SK, {'test': 'fast', 'params': 'val'}, {'data': 'valid'}),
]


@httpretty.activate(allow_net_connect=False, verbose=True)
@pytest.mark.parametrize('url, http_method, service, get_data, post_data', REQUEST_URL_PARAMETERS)
def test_request_url(url, http_method, service, get_data, post_data):
	request = HeurekaRequest(service)
	httpretty.register_uri(http_method, url, responses=200, body='{"code": 200, "message": "ok"}')
	success, data = request.request(HeurekaApiActions.LOG_ORDER, get_data=get_data, post_data=post_data)
	assert success
	assert data['code'] == 200
	last_request = httpretty.last_request()
	assert last_request.url == url
	assert last_request.method == http_method


@httpretty.activate(allow_net_connect=False, verbose=True)
def test_request_miss_match_codes():
	api_url = 'https://api.heureka.cz/shop-certification/v2/order/log'
	response_data = json.dumps({ "code": 401, "message": "unauthorized", "description": "Unknown API key \"xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\"." })
	request = HeurekaRequest(HeurekaService.CZ)
	httpretty.register_uri(httpretty.POST, api_url, status=301, body=response_data)
	success, data = request.request(HeurekaApiActions.LOG_ORDER, get_data={}, post_data={'key': 'val'})
	assert success == False
	assert data['code'] == 401
	last_request = httpretty.last_request()

   

@httpretty.activate(allow_net_connect=False, verbose=True)
def test_request_server_error():
	api_url = 'https://api.heureka.cz/shop-certification/v2/order/log'
	request = HeurekaRequest(HeurekaService.CZ)
	httpretty.register_uri(httpretty.POST, api_url, status=500, body='Unknown server error')
	success, data = request.request(HeurekaApiActions.LOG_ORDER, get_data={}, post_data={'key': 'val'})
	assert success == False
	assert data['code'] == 500