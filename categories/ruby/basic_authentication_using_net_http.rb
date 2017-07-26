require 'net/http'
require 'base64'
require 'json'

target_website = '<the URL or domain name of the website to retrieve the categories for>'

key = '<insert your API key>'
secret_key = '<insert your API secret key>'

api_uri = URI('https://api.webshrinker.com/categories/v3/' + Base64.urlsafe_encode64(target_website))

req = Net::HTTP::Get.new(api_uri)
req.basic_auth key, secret_key

res = Net::HTTP.start(api_uri.hostname, api_uri.port, :use_ssl => true) {|http|
  http.request(req)
}

status_code = res.code
data = JSON.parse(res.body)

if status_code == '200'
    # Do something with the JSON response
    category_data = data['data'][0]['categories']

    puts "'#{target_website}' belongs to the following categories:"

    # Print the category ID, the human friendly category name, score and confident values for each entry
    categories = []
    category_data.each {|entry|
        puts "(%s) %s [score=%f,confident=%s]" % [entry['id'], entry['label'], entry['score'], entry['confident']]
    }
elsif status_code == '202'
    # The request is being categorized right now in real time, check again for an updated answer
    puts "The categories for '#{target_website}' are being determined, check again in a few seconds"
else
    # The different status codes are covered in the documentation (https://docs.webshrinker.com/v3/website-category-api.html)
    puts "An error occurred: HTTP #{status_code}"
    if data.has_key? 'error'
    	puts data['error']['message']
    end
end
