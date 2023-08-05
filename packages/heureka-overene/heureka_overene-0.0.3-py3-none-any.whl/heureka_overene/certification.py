# -*- coding: utf-8 -*-
from .utils import is_valid_email
from .const import HeurekaService, HeurekaApiActions
from .request import HeurekaRequest

class ShopCertification:
	__slots__ = ('_api_key', '_service', '_sent', '_products_ids', '_email', '_order_id', 'response')

	def __init__(self, api_key: str, email: str, service: HeurekaService = HeurekaService.SK):
		if not is_valid_email(email):
			raise ValueError("Not valid email")
		if api_key is None or len(api_key) == 0:
			raise ValueError("Api key can't be empty")
		self._products_ids = list()
		self._email = email
		self._order_id = None
		self._sent = False
		self._api_key = api_key
		self._service = service
		self.response = None

	def add_product_id(self, product_id: str) -> None:
		if not product_id:
			raise ValueError("Product id can't be empty")
		if product_id in self._products_ids:
			raise ValueError(f"Duplicate product ids {product_id}")
		self._products_ids.append(product_id)

	@property
	def email(self) -> str:
		return self._email

	@property
	def order_id(self) -> int:
		return self._order_id

	@order_id.setter
	def order_id(self, order_id: int):
		if not str(order_id).isnumeric():
			raise TypeError("Order ID has to be integer")
		self._order_id = int(order_id)

	def log_order(self) -> bool:
		if self._sent:
			raise RuntimeError('Order can be sent just one time')
		self._sent = True
		order_data = {
			"apiKey": self._api_key,
			"email": self.email,
		}
		if self._products_ids:
			order_data['productItemIds'] = [str(i) for i in self._products_ids if i]

		if self.order_id:
			order_data['orderId'] = self.order_id

		request = HeurekaRequest(self._service)
		success, self.response = request.request(HeurekaApiActions.LOG_ORDER, get_data=None, post_data=order_data)

		if success:
			return True
		return False