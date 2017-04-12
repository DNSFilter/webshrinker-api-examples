##########################################################################################
# NOTE: If you are using Python 2.7.6 you might run into an issue
# with making API calls using the requests library.
# For a workaround, see:
# http://stackoverflow.com/questions/31649390/python-requests-ssl-handshake-failure
##########################################################################################

import requests
from base64 import urlsafe_b64encode

target_website = "<the domain name/IP address of the site to retrieve the information about>"

key = "<insert your API key>"
secret_key = "<insert your API secret key>"

api_url = "https://api.webshrinker.com/hosts/v2/%s" % urlsafe_b64encode(target_website)

response = requests.get(api_url, auth=(key, secret_key))
status_code = response.status_code
data = response.json()

if status_code == 200:
    # Do something with the JSON response
    print data
elif status_code == 400:
    # Bad or malformed HTTP request
    print "Bad or malformed HTTP request"
    print data
elif status_code == 401:
    # Unauthorized
    print "Unauthorized - check your access and secret key permissions"
    print data
elif status_code == 402:
    # Request limit reached
    print "Account request limit reached"
    print data
else:
    # General error occurred
    print "A general error occurred, try the request again"
