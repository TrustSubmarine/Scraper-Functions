from functions.restful.all_reviews import all_reviews_req

def get_all_reviews(event, context):
    URL = event['URL']
    headers = event['headers']
    print(URL)
    print(headers)
    return all_reviews_req(event)