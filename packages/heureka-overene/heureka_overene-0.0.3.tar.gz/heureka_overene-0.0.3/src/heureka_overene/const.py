import enum


class HeurekaService(enum.Enum):
	SK = 'https://api.heureka.sk/shop-certification/v2/'
	CZ = 'https://api.heureka.cz/shop-certification/v2/'

	def get_url(self):
		return self.value


class HeurekaApiActions(enum.Enum):
	LOG_ORDER = 'order/log'
