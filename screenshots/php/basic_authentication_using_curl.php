<?php

$target_website = "<the URL or domain name of the website to retrieve the categories for>";

$key = "<insert your API key>";
$secret_key = "<insert your API secret key>";

// Use URL-safe base64 encoding
$base64_target_website = str_replace(array('+', '/'), array('-', '_'), base64_encode($target_website));

// For additional image parameters and possible image sizes
// see: http://docs.webshrinker.com/v2/website-screenshot-api.html#image-requests
$parameters = array(
    'size' => '3xlarge',
    'fullpage' => true
);

$api_url = sprintf("https://api.webshrinker.com/thumbnails/v2/%s?%s", $base64_target_website, http_build_query($parameters));

// This demo will write the screenshot to the 'screenshot_demo.png' file in the current directory
$fp = fopen('screenshot_demo.png', 'wb');
if (!$fp) {
    print "Unable to open the output file for writing the screenshot, aborting";
    exit(1);
}

$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, $api_url);
curl_setopt($ch, CURLOPT_USERPWD, "{$key}:{$secret_key}");
curl_setopt($ch, CURLOPT_FILE, $fp);
curl_setopt($ch, CURLOPT_HEADER, 0);

$result = curl_exec($ch);
$status_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);

switch ($status_code) {
    case 200:
        // Do something with the image response
        print "The screenshot for '{$target_website}' was saved to 'screenshot_demo.png'\n";
        break;
    case 202:
        // The request is being categorized right now in real time, check again for an updated answer
        print "The screenshot image for '{$target_website}' is being generated, check again in a few seconds\n";
        break;
    default:
        // The different status codes are covered in the documentation 
        // http://docs.webshrinker.com/v2/website-category-api.html#category-lookup
        // 401 : Unauthorized - Verify that your access key and secret key are correct
        print "An error occurred: HTTP {$status_code}\n";
        break;
}

fclose($fp);