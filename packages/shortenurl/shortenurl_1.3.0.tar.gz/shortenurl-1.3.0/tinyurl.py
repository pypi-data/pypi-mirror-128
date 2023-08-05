import requests

print("TinyURL has loaded!")

#Test stuff
def test():
    print("TinyURL is working.")

def create(apiToken, urlToShorten, alias, domain):
    if str(domain) == "":
        domain = "tinyurl.com"
    if str(alias) == "":
        return "Alias was not provided"

    reqData = {
        "api_token": str(apiToken),
        "url": str(urlToShorten),
        "domain": str(domain),
        "alias": str(alias)
    }

    r = requests.post('https://api.tinyurl.com/create', data = reqData)
    
    if r.status_code == 200:
        print("Successful operation")
        print("Response:")
        return r.text
    elif r.status_code == 401:
        print("You are not authorized to use to access this API endpoint or resource. Please check your API token")
        print("Response:")
        return r.text
    elif r.status_code == 405:
        print("You do not have permission to access this resource 405")
        print("Response:")
        return r.text
    elif r.status_code == 422:
        print("Alias field is too long or is already a alias")
        print("Response:")
        return r.text
    else:
        print("There was an unexpected error processing your request")
        print("Response:")
        return r.text

def update(apiToken, alias, domain, newAlias, newDomain):
    if str(domain) == "":
        return "Domain was not provided"
    if str(alias) == "":
        return "Alias was not provided"
    if str(newDomain) == "":
        newDomain = "tinyurl.com"

    reqData = {
        "api_token": str(apiToken),
        "domain": str(domain),
        "alias": str(alias),
        "new_domain": str(newDomain),
        "new_alias": str(newAlias),
    }

    r = requests.post('https://api.tinyurl.com/update', data = reqData)
    
    if r.status_code == 200:
        print("Successful operation")
        print("Response:")
        return r.text
    elif r.status_code == 401:
        print("You are not authorized to use to access this API endpoint or resource. Please check your API token")
        print("Response:")
        return r.text
    elif r.status_code == 405:
        print("You do not have permission to access this resource 405")
        print("Response:")
        return r.text
    elif r.status_code == 422:
        print("Alias field is too long or is already a alias")
        print("Response:")
        return r.text
    else:
        print("There was an unexpected error processing your request")
        print("Response:")
        return r.text

def change(apiToken, alias, domain, newAlias, newUrl):
    if str(domain) == "":
        return "Domain was not provided"
    if str(alias) == "":
        return "Alias was not provided"
    if str(newUrl) == "":
        return "New URL was not provided"

    reqData = {
        "api_token": str(apiToken),
        "domain": str(domain),
        "alias": str(alias),
        "url": str(newUrl),
    }

    r = requests.post('https://api.tinyurl.com/change', data = reqData)
    
    if r.status_code == 200:
        print("Successful operation")
        print("Response:")
        return r.text
    elif r.status_code == 401:
        print ("You are not authorized to use to access this API endpoint or resource. Please check your API token")
        print ("Response:")
        return r.text
    elif r.status_code == 405:
        print("You do not have permission to access this resource 405")
        print("Response:")
        return r.text
    elif r.status_code == 422:
        print("Alias field is too long or is already a alias")
        print("Response:")
        return r.text
    else:
        print("There was an unexpected error processing your request")
        print("Response:")
        return r.text

def bulk():
    return "Not supported, yet."