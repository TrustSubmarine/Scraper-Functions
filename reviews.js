const fns = require('./functions/getAllReviews');

// Example usage
const url = "https://www.amazon.in/Baseus-Screenbar-Adjustable-Brightness-Temperature/dp/B08CXL3YQ8/";
const headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
    "Accept-Encoding": "gzip, deflate",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "DNT": "1",
    "Connection": "close",
    "Upgrade-Insecure-Requests": "1",
    "sec-ch-ua": '"Brave";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform-version": '"13.2.0"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "no-cors",
    "sec-fetch-site": "same-origin",
    "sec-gpc": "1"
};

fns.getAllReviews(url, headers)
    .then(reviews => {
        console.log(reviews);
        // console.log(headers);
        // console.log(url);
    })
    .catch(error => {
        console.error(error);
    });