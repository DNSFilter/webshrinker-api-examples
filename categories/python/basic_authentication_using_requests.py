import requests
from base64 import urlsafe_b64encode

target_website = "<the URL or domain name of the website to retrieve the categories for>"

key = "<insert your API key>"
secret_key = "<insert your API secret key>"

api_url = "https://api.webshrinker.com/categories/v3/%s" % urlsafe_b64encode(target_website)

response = requests.get(api_url, auth=(key, secret_key))
status_code = response.status_code
data = response.json()

if status_code == 200:
    # Do something with the JSON response
    category_data = data['data'][0]['categories']

    # Build a string array containing the category ID, the human friendly category name, score and confident values for each entry
    categories = []
    for entry in category_data:
        categories.append('({}) {} [score={},confident={}]'.format(entry['id'], entry['label'], entry['score'], entry['confident']))

    print "'%s' belongs to the following categories:\n%s" % (target_website, "\n".join(categories))
elif status_code == 202:
    # The request is being categorized right now in real time, check again for an updated answer
    print "The categories for '%s' are being determined, check again in a few seconds" % target_website
else:
    # The different status codes are covered in the documentation (https://docs.webshrinker.com/v3/website-category-api.html)
    print "An error occurred: HTTP %d" % status_code
    if 'error' in data:
        print data['error']['message']
