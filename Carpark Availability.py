import pandas as pd
from pandas.io.json import json_normalize
import requests

import json
import csv

# Define parameters. If unsure, use Postman as guideline
params = {"service": "CarPark_Availability", "format": "json"}

# Define header. Header typically contains Accesskey and Token(re-generate every 24 hours)
header = {"AccessKey": "bbdbccd7-842d-4442-9485-e001137d4935",
          "Token": "cg2dzmb45B8jhfjsueqy2@+47Nh3Ucfw4vG3kdt9qcDZusDPnKUn82b144cxdn499c20x2YR4Z8Z38Bm91xSTEfNqbT2bH64az25"}

# Indicate the desired URL to call API
url = "https://www.ura.gov.sg/uraDataService/invokeUraDS?service=Car_Park_Availability"

# Using request module, compile params, header into URL query and output it's json response
response = requests.get(url, params=params, headers=header)
data = response.json()

# Only print this line if you want to see it's json output in the console, else comment
print json.dumps(data, sort_keys=True, indent=4)

# json_normalize helps structure data into table format, but still in json format
df = json_normalize(data, "Result")
# Converts json into CSV and output
df.to_csv("output.csv")

# Print csv to console
print df
