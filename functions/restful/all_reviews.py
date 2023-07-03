from bs4 import BeautifulSoup
import requests
import time
import json
import random

# 64 pages max for this test example (handy later)
URL = "https://www.amazon.in/Baseus-Screenbar-Adjustable-Brightness-Temperature/dp/B08CXL3YQ8/"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
    "Accept-Encoding": "gzip, deflate",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "DNT": "1",
    "Connection": "close",
    "Upgrade-Insecure-Requests": "1",
    "sec-ch-ua": '"Brave";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    # "sec-ch-ua-platform": '"macOS"',
    "sec-ch-ua-platform-version": '"13.2.0"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "no-cors",
    "sec-fetch-site": "same-origin",
    "sec-gpc": "1",
}

# used for rotation
USER_AGENTS = [
    "Mozilla/5.0 (iPhone; CPU iPhone OS 13_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
    "Mozilla/5.0 (platform; rv:geckoversion) Gecko/geckotrail Firefox/firefoxversion",
]

def get_random_user_agent():
    return USER_AGENTS[random.randint(0, len(USER_AGENTS) - 1)]


def all_reviews_req(event):
    # req_json = request.get_json()
    if event["headers"] != None:
        req_hdrs = event["headers"]
        req_hdrs["User-Agent"] = get_random_user_agent()
        return all_reviews(event["URL"], headers=req_hdrs)
    else:
        headers["User-Agent"] = get_random_user_agent()
        return all_reviews(event["URL"])


def all_reviews(URL, headers=headers):
    BASE_URL = (
        "https://www." + URL.split(".")[1] + "." + URL.split(".")[2].split("/")[0]
    )

    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")

    print(soup)
    print("")
    print("")
    print("-----------")
    print("")
    print("")

    see_all_reviews_anchor = soup.find(attrs={"data-hook": "see-all-reviews-link-foot"})

    all_reviews_URL = BASE_URL + see_all_reviews_anchor["href"]
    all_reviews_URL_clean = "/".join(all_reviews_URL.split("/")[0:-1])

    reviews_page = requests.get(all_reviews_URL_clean, headers=headers)
    reviews_soup = BeautifulSoup(reviews_page.content, "html.parser")

    all_reviews_parse_tree_list = reviews_soup.find_all(attrs={"data-hook": "review"})

    reviews_list = []

    MAX_PAGES = 2
    count = 1
    while not reviews_soup.find(class_="a-disabled a-last") and count <= MAX_PAGES:
        # single page reviews here
        for rev in all_reviews_parse_tree_list:
            rev_title = rev.find(attrs={"data-hook": "review-title"}).get_text()
            rev_text = rev.find(attrs={"data-hook": "review-body"}).get_text()
            print(rev_title)
            print(rev_text)
            reviews_list.append({"title": rev_title, "text": rev_text})

        time.sleep(1)

        next_page_URL = reviews_soup.find("li", class_="a-last")
        next_page_URL = "https://amazon.in" + next_page_URL.contents[0]["href"]

        time.sleep(1)

        reviews_soup = BeautifulSoup(
            requests.get(next_page_URL, headers=headers).content, "html.parser"
        )
        all_reviews_parse_tree_list = reviews_soup.find_all(
            attrs={"data-hook": "review"}
        )

        count += 1

    return json.dumps({"reviews": reviews_list}, indent=4)


# all_reviews(URL, headers=headers)
