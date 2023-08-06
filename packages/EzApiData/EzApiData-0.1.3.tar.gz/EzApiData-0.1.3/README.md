## EzApiData
## Get available data from api's that you can use

# Why I made this api
- It would be a pain to have to make request to a api for data so I decided why not make it easier for everyone by helping you get the data in a simple function


# When getting an api key I recommend using a .env so it will be more protected
```python
import os
import dotenv

dotenv.load_dotenv()

EXAMPLE_API(os.getenv("<VAR-SET-FOR-API-KEY>"))
```

# Example to get info from api
```python
from ezapidata.ApiList.games.game import game_API
import os
import dotenv

dotenv.load_dotenv()

#Must always have a valid API key which can be acquired from the Brawl Stars API and put it in <API-KEY>
API_CALL = game_API(os.getenv("<VAR-SET-FOR-API-KEY>"))

#returns player stats
API_CALL.get_data("<PASS-PARAMETERS>")
```

# used api links
- https://www.weatherapi.com/
- https://developer.brawlstars.com/#/
- https://developer.clashofclans.com/#/
- https://yfapi.net
