const fns = require('./functions/getAllReviews');


// Example usage
// const url = "https://www.amazon.in/Baseus-Screenbar-Adjustable-Brightness-Temperature/dp/B08CXL3YQ8/";
const headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41",
    "Accept-Encoding": "gzip, deflate",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "DNT": "1",
    "Origin": "https://www.amazon.in",
    "Referer": "https://www.amazon.in/",
    "Connection": "close",
    "Upgrade-Insecure-Requests": "1"
  }

async function getReviews(event, context, callback) {
    console.log(event);
    const eventParams = event["queryStringParameters"];
    // const eventBody = JSON.parse(event["body"]);
    // console.log(eventBody);
    const url = eventParams['url'];
    console.log(url);
    console.log(headers);

    const res = fns.getAllReviews(url, headers)
        .then(reviews => {
            console.log(reviews);
            return reviews;
        })
        .catch(error => {
            console.error(error);
            throw error;
        });
    
    return res;
    // return callback(null, res);
    // TODO: Read up on callback here and why it works
}

// AWS Lambda handler export
exports.handler = getReviews;
