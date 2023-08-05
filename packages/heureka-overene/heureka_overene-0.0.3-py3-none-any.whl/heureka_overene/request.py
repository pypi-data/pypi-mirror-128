import json
from urllib.parse import urlencode, urljoin

import requests

from .const import HeurekaApiActions, HeurekaService


class HeurekaRequest:
	__slots__ = ('_service')

	def __init__(self, service: HeurekaService):
		self._service = service

	def request(self, action: HeurekaApiActions, get_data: dict = None, post_data: dict = None):
		url = urljoin(self._service.get_url(), './' + action.value)
		if get_data:
			url = url + '?' + urlencode(get_data)

		if post_data:
			headers = {'Content-type': 'application/json;charset=utf-8'}
			response = requests.post(url=url, headers=headers, data=json.dumps(post_data))
		else:
			response = requests.get(url=url)
		try:
			data = response.json()
			return data['code'] == 200, response.json()
		except json.decoder.JSONDecodeError:
			status_code = response.status_code
			if status_code == 200:
				status_code = 501
			return False, {'message': response.text, 'code': status_code}
