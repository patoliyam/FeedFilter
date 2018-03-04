import httplib, urllib, base64,json
headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': 'f855ce3e91d043d3953004bae7964f5e',
    }
params = urllib.urlencode({
    # Request parameters
    'CacheImage': '{false}',
})
try:
    body = {"DataRepresentation": "URL", "Value":"http://aaronallen.com/wp-content/uploads/2013/08/Middle-East-Racist-Ad-500x238.jpg"}
    conn = httplib.HTTPSConnection('eastasia.api.cognitive.microsoft.com')
    conn.request("POST", "/contentmoderator/moderate/v1.0/ProcessImage/Evaluate?%s" % params, json.dumps(body),
                 headers)
    response = conn.getresponse()
    data = response.read()
    print "data from adult_Racy api:"
    data = json.loads(data)
    print(data)
    conn.close()
except:
    print("error")