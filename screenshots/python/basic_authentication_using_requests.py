import requests
import shutil
from base64 import urlsafe_b64encode

target_website = b"<the URL or domain name of the website to retrieve the categories for>"

key = "<insert your API key>"
secret_key = "<insert your API secret key>"

# For additional image parameters and possible image sizes
# see: http://docs.webshrinker.com/v2/website-screenshot-api.html#image-requests
parameters = {
    'size': '3xlarge',
    'fullpage': True
}

api_url = "https://api.webshrinker.com/thumbnails/v2/%s" % urlsafe_b64encode(target_website).decode('utf-8')

response = requests.get(api_url, auth=(key, secret_key), stream=True, params=parameters)
status_code = response.status_code

if status_code == 200:
    # Do something with the image response
    print("Saving the screenshot for '%s' to 'screenshot_demo.png'" % target_website.decode('utf-8'))
    with open('screenshot_demo.png', 'wb') as image_file:
        shutil.copyfileobj(response.raw, image_file)
elif status_code == 202:
    print("The screenshot image for '%s' is being generated, check again in a few seconds" % target_website.decode('utf-8'))
else:
    # The different status codes are covered in the documentation 
    # http://docs.webshrinker.com/v2/website-category-api.html#category-lookup
    #
    # 401 : Unauthorized - Verify that your access key and secret key are correct
    print("An error occurred: HTTP %d" % status_code)
