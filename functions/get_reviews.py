"""AMAZON Cloud Function that gets all reviews for a dealership

Returns:
    List: List of reviews for the given dealership
"""
from ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_cloud_sdk_core import ApiException
import os
import json

def lambda_handler(event, context):
    """Main Function

    Args:
        param_dict (Dict): input paramater

    Returns:
        _type_: _description_ TODO
    """

    try:

        authenticator = IAMAuthenticator(os.environ["IAM_API_KEY"])

        service = CloudantV1(authenticator=authenticator)

        service.set_service_url(os.environ["COUCH_URL"])
        if event.get('requestContext').get('http').get('method') == 'GET':
            reviews = service.post_all_docs(
                  db='reviews',
                  include_docs= True,
                  inclusive_end= False
                ).get_result()['rows']
            reviews = list(map(lambda result: result['doc'], reviews))
            query = event.get('queryStringParameters')
            if query and query['dealerId']:
                reviews = list(filter(lambda review: int(review['dealership']) == int(query['dealerId']), reviews))
            if len(reviews):
                return {"Reviews": reviews}
            else:
                return {'statusCode': 404, 'error': 'Not found'}
        else:
            keys = ["id", "name", "dealership", "review", "purchase", "another", "purchase_date", "car_make", "car_model", "car_year"]
            body = json.loads(event.get('body'))
            for key in keys:
                if body.get(key) == None:
                    return {'statusCode': 404, 'error': 'Not enough data'}
            return {"Review": {
                        "id": body['id'],
                        "name": body['name'],
                        "dealership": body['dealership'],
                        "review": body['review'],
                        "purchase": body['purchase'],
                        "another": body['another'],
                        "purchase_date": body['purchase_date'],
                        "car_make": body['car_make'],
                        "car_model": body['car_model'],
                        "car_year": body['car_year']
                    }}
    except ApiException as ae:
        print("Method failed")
        print(" - status code: " + str(ae.code))
        print(" - error message: " + ae.message)
        if ("reason" in ae.http_response.json()):
            print(" - reason: " + ae.http_response.json()["reason"])
