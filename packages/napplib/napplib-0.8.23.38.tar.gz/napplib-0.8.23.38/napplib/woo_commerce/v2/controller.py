from typing import Optional, Union
import requests
from requests.auth import HTTPBasicAuth
from dataclasses import dataclass

from loguru 	import logger

from napplib.utils import AttemptRequests
from napplib.utils	import LoggerSettings

@logger.catch()
@dataclass
class WooCommerceController:
	'''This is not a static class! 
	Instantiate an object passing the authentications through the constructor

	Documentation: https://woocommerce.github.io/woocommerce-rest-api-docs/'''

	url: str
	consumer_key: str
	consumer_secret: str
	api_version: Optional[str] = 'v3'
	debug: bool = False
	
	def __post_init__(self):
		level = 'INFO' if not self.debug else 'DEBUG'
		LoggerSettings(level=level)

	@AttemptRequests(success_codes=[200, 201], waiting_time=5)
	def get_product(self, product_code: str = '', page: int = 1) -> Union[list, dict]:
		'''return all products when no product_code is informed'''
		endpoint= f'/wp-json/wc/{self.api_version}/products/' + product_code
		headers = {
			'User-Agent':'curl/7.68.0',
		}

		return requests.get(f'{self.url}{endpoint}?page={page}', headers=headers, auth=HTTPBasicAuth(self.consumer_key,self.consumer_secret))


