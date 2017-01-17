<?php

/*
 * If you need a local copy of composer:
 * curl -sS https://getcomposer.org/installer | php
 *
 * Install the required Guzzle libraries for the demo:
 * php composer.phar install
 *
 */

require 'vendor/autoload.php';
use GuzzleHttp\Client;

$target_website = "<the URL or domain name of the website to retrieve the categories for>";

$key = "<insert your API key>";
$secret_key = "<insert your API secret key>";

// Use URL-safe base64 encoding
$base64_target_website = str_replace(array('+', '/'), array('-', '_'), base64_encode($target_website));

$api_url = sprintf("https://api.webshrinker.com/categories/v2/%s", $base64_target_website);

$client = new GuzzleHttp\Client();
$res = $client->request('GET', $api_url, [
    'auth' => [$key, $secret_key],
    'exceptions' => false
]);

$status_code = $res->getStatusCode();
$result = json_decode($res->getBody());

switch ($status_code) {
    case 200:
        // Do something with the JSON response
        $categories = implode(",", $result->data[0]->categories);
        print "'{$target_website}' belongs to the following categories: {$categories}\n";
        break;
    case 202:
        // The request is being categorized right now in real time, check again for an updated answer
        print "The categories for '{$target_website}' are being determined, check again in a few seconds\n";
        break;
    default:
        // The different status codes are covered in the documentation
        // http://docs.webshrinker.com/v2/website-category-api.html#category-lookup)
        print "An error occurred: HTTP {$status_code}\n";
        if (isset($result->error)) {
            $error = $result->error->message;
            print "{$error}\n";
        }
        break;
}
