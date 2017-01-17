import requests
from base64 import urlsafe_b64encode

target_website = "<the URL or domain name of the website to retrieve the categories for>"

key = "<insert your API key>"
secret_key = "<insert your API secret key>"

api_url = "https://api.webshrinker.com/categories/v2/%s" % urlsafe_b64encode(target_website)

response = requests.get(api_url, auth=(key, secret_key))
status_code = response.status_code
data = response.json()

if status_code == 200:
    # Do something with the JSON response
    categories = data['data'][0]['categories']
    print "'%s' belongs to the following categories: %s" % (target_website, ",".join(categories))
elif status_code == 202:
    # The request is being categorized right now in real time, check again for an updated answer
    print "The categories for '%s' are being determined, check again in a few seconds" % target_website
else:
    # The different status codes are covered in the documentation (http://docs.webshrinker.com/v2/website-category-api.html#category-lookup)
    print "An error occurred: HTTP %d" % status_code
    if 'error' in data:
        print data['error']['message']
