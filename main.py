import functions_framework
from functions.restful.all_reviews import all_reviews_req


@functions_framework.http
def get_all_reviews(request):
    return all_reviews_req(request)
