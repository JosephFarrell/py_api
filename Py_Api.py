# Sample RESTful API
# Requests made to Open Notify (http://open-notify.org)

import requests # This will send requests to the server
import json     # This will deserialize the recieved data so we can parse it more clearly

## Make a GET request to the server

try:
	# The actual request
	response = requests.get("http://api.open-notify.org/iss-now.json")
	# Check for any errors in getting the response
	response.raise_for_status()

except requests.exceptions.HTTPSError as error:
	# If there was an error, print it to console and terminate
	print(error)
	sys.exit()

## Deserialize the response

# Data will be a dictionary corresponding to the JSON response
# For example we can access the latitude of the ISS using data["iss_position"]["latitude"]
data = response.json()

# We can also make the response into an object
# Following code by user XEye of StackOverflow (https://stackoverflow.com/users/885564/xeye)
class Struct(object):
	def __init__(self, data):
		for name, value in data.items():
			setattr(self, name, self._wrap(value))

	def _wrap(self, value):
		if isinstance(value, (tuple, list, set, frozenset)): 
			return type(value)([self._wrap(v) for v in value])
		else:
			return Struct(value) if isinstance(value, dict) else value

iss_data = Struct(data)

# Now we can access the latitude through our new Struct object using iss_data.iss_position.latitude
print("Current latitude of the ISS: " + iss_data.iss_position.latitude)
print("Current longitude of the ISS: " + iss_data.iss_position.longitude)