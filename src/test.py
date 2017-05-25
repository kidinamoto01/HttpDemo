from urllib.request import urlopen
import json

# Get the dataset
url = 'http://www.quandl.com/api/v1/datasets/FRED/GDP.json'
response = urlopen(url)

# Convert bytes to string type and string type to dict
string = response.read().decode('utf-8')
json_obj = json.loads(string)

print(json_obj['source_name']) # prints the string with 'source_name' key
print(json_obj['column_names']) # prints the string with 'source_name' key