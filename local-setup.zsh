# Run to setup function on localhost
functions-framework --target get_all_reviews --debug

# Example curl command to send a request
curl -m 70 https://asia-south2-durable-pulsar-388017.cloudfunctions.net/scraper-milestone2 -H 'Content-Type: application/json' -d '{ 
    "URL": "https://www.amazon.in/Baseus-Screenbar-Adjustable-Brightness-Temperature/dp/B08CXL3YQ8/ref=sr_1_2?crid=2V7F7H5YS3E5W&keywords=baseus+monitor+light&qid=1687614850&refinements=p_n_availability%3A1318485031&rnid=1318483031&sprefix=baseus+monitor+lig%2Caps%2C259&sr=8-2",
    "hdrs": {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
        "Accept-Encoding": "gzip, deflate",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "DNT": "1",
        "Connection": "close",
        "sec-ch-ua": "\"Brave\";v=\"113\", \"Chromium\";v=\"113\", \"Not-A.Brand\";v=\"24\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform-version": "\"13.2.0\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "no-cors",
        "sec-fetch-site": "same-origin",
        "sec-gpc": "1", "Accept-Language": "en-US,en;q=0.5"
    }
}'