from pytwitter import Api
from config import BearerToken

api = Api(bearer_token=BearerToken)
print(api.get_users(ids=["783214", "2244994945"]))