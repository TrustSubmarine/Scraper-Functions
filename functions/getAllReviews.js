const chromium = require('chrome-aws-lambda');


// Function to get a random user agent
function getRandomUserAgent() {
  const userAgents = [
    // "Mozilla/5.0 (iPhone; CPU iPhone OS 13_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
    // "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
    "Mozilla/5.0 (platform; rv:geckoversion) Gecko/geckotrail Firefox/firefoxversion"
  ];

  const randomIndex = Math.floor(Math.random() * (userAgents.length - 1));
  return userAgents[randomIndex];
}

async function getAllReviews(url, headers) {
  console.log(url);
  console.log(headers);

  const browser = await chromium.puppeteer.launch({
    args: chromium.args,
    defaultViewport: chromium.defaultViewport,
    executablePath: await chromium.executablePath,
    headless: chromium.headless,
    ignoreHTTPSErrors: true,
  });

  const page = await browser.newPage();
  
  // Set the user agent
  const userAgent = getRandomUserAgent();
  await page.setUserAgent(userAgent);
  console.log(userAgent);
  
  // Set the headers
  await page.setExtraHTTPHeaders(headers);
  
  // Go to the main product page
  await page.goto(url);

  page.title().then(title => console.log(title));
  
  // TODO: why does this line break everything?
  // const html = await page.content();
  
  
  // Extract the link for all reviews
  // TODO: why does this line sometimes work, and then other times just not?
  // const seeAllReviewsAnchor = await page.$eval('[data-hook="see-all-reviews-link-foot"]', anchor => anchor.href);
  const seeAllReviewsAnchor = await page.$eval('.a-link-emphasis.a-text-bold', anchor => anchor.href);
  // seeAllReviewsAnchor.then(i => console.log(i));
  console.log(seeAllReviewsAnchor);

//   const baseUrl = `https://www.${url.split("/")[2]}`;
//   const allReviewsUrl = baseUrl + seeAllReviewsAnchor;
  const allReviewsUrl = seeAllReviewsAnchor;
  console.log(allReviewsUrl);
  console.log("after all reviews url print")
  
  // Go to the all reviews page
  await page.goto(allReviewsUrl);
  
  let reviewsList = [];
  const maxPages = 2;
  let count = 1;
  
  while (count <= maxPages) {
    // Get the reviews on the current page
    const reviews = await page.$$eval('[data-hook="review"]', elements => {
      return elements.map(element => {
        const title = element.querySelector('[data-hook="review-title"]').innerText;
        const text = element.querySelector('[data-hook="review-body"]').innerText;
        console.log({title, text});
        return { title, text };
      });
    });
    
    reviewsList = reviewsList.concat(reviews);
    
    // console.log("here");

    const nextPageUrl = await page.$eval('.a-last > a', link => link.href);
    // const nextPageUrlEval = await page.eval(link => link.href, nextPageUrl);
    await page.goto(nextPageUrl);
    console.log(`here with ${count}`);
    // console.log(await page.content());
    
    count++;
  }
  
  await browser.close();
  
  const result = JSON.stringify({ reviews: reviewsList }, null, 4);

  console.log(result);

  return result;
}

module.exports = { getAllReviews };