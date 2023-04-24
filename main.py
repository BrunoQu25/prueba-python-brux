# main() will be run when you invoke this action
#
# @param Cloud Functions actions accept a single parameter, which must be a JSON object.
#
# @return The output of this action, which must be a JSON object.
#


import json
import requests
from decouple import config

def main(dic):
    #NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.

    API_KEY = config('APIKEY') # Paste the account APIKEY where the Watson Machine Learning service is
    token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
    mltoken = token_response.json()["access_token"]
    
    header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}
    
    dic['creditCardAvg'] = dic['creditCardAvg']/1000 #Do not forget to do this. 

    # NOTE: manually define and pass the array(s) of values to be scored in the next line. You can appreciate that dic.age will be
    #       the age you ask to the customer in Watson Assistant.
    
    payload_scoring = {
        "input_data": [
            {
                "fields": [
                    "Age",
                    "Experience",
                    "Income",
                    "ZIP Code",
                    "Family",
                    "CCAvg",
                    "Education",
                    "Mortgage",
                    "Securities Account",
                    "CD Account",
                    "Online",
                    "CreditCard"
                    ],
                    "values": [
                        [
                            dic['age'],
                            dic['experience'],
                            dic['income'],
                            dic['ZIP'],
                            dic['family'],
                            dic['creditCardAvg'],
                            dic['education'],
                            dic['mortgage'],
                            dic['security'],
                            dic['CD'],
                            dic['online'],
                            dic['creditCard']
                        ]
                    ]
            }
        ]
    
    }
    response_scoring = requests.post(config('URL'), json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
    # REPLACE THE URL WITH YOUR DEPLOY URL.
      
    result = response_scoring.text
    result_json = json.loads(result)
    
    result_keys = result_json['predictions'][0]['fields']
    result_vals = result_json['predictions'][0]['values']
    
    result_dict = dict(zip(result_keys, result_vals[0]))
      
    x = zip(result_keys, result_vals[0])
    
    predict = result_dict["prediction"]
    
    
    
    final = f'Your application is presenting a {predict}'
      
    print("final: ", final)
    return { 'message': final }