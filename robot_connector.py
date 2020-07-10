import requests
import json

email = ""

#receives email input
def send_email(input_email):
    global email
    email = input_email


#receives action from the chatbot
def send_to_connector(action):
    #checks which action is needed for now only send email is possible
    if (action == "sendEmail"):
        token = getUserToken()
        global email
        sendEmailRobot(token,email)

#gets the Bear token with the Orchestrator API
def getUserToken():
    user_data = """{
        "grant_type": "refresh_token",
        "client_id": "8DEv1AMNXczW3y4U15LL3jYf62jK93n5",
        "refresh_token": "jKEoPjK5Tq-GYK_62GxxfGf5tp4PVl260X_ZmOPdsMYIG"
    }"""
    url = "https://account.uipath.com/oauth/token"
    headers = {'content-type': 'application/json', 'X-UIPATH-TenantName': 'CasaltieDefault', }
    data = requests.post(url, json=json.loads(user_data), headers=headers)
    authentication_data = json.loads(data.text)
    token = "Bearer " + str(authentication_data["access_token"])
    print(token)
    return token

# post request to start robot
def sendEmailRobot(token, mailadress):
    url = "https://cloud.uipath.com/casaltie/CasaltieDefkod6494944/odata/Jobs/UiPath.Server.Configuration.OData.StartJobs"
    headers = {'content-type': 'application/json', 'X-UIPATH-TenantName': 'CasaltieDefkod6494944',
               'X-UIPATH-OrganizationUnitID': '332506', "Authorization": token}
    print("hallo")
    start_job_json = r'{"startInfo": {"ReleaseKey": "7c765233-7049-4c78-a138-5a058f112d34","Strategy": "All","RobotIds": [],"NoOfRobots": 0, "InputArguments": "{\"email\":\"'+ mailadress +r'\"}"}}'
    data = requests.post(url, json=json.loads(start_job_json), headers=headers)


if __name__ == '__main__':
    send_to_connector("sendEmail")
