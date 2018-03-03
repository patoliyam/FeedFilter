import httplib, urllib, base64,json
headers = {
        # Request headers
        'Content-Type': 'text/plain',
        'Ocp-Apim-Subscription-Key': 'f855ce3e91d043d3953004bae7964f5e',
    }

params = urllib.urlencode({
    # Request parameters
    'autocorrect': 'false',
    # 'PII': '{boolean}',
    # 'listId': '{string}',
    'classify': 'True',
    # 'language': '{string}',
})
body = str("text_of_post")
try:
    conn = httplib.HTTPSConnection('eastasia.api.cognitive.microsoft.com')
    conn.request("POST", "/contentmoderator/moderate/v1.0/ProcessText/Screen?%s" % params, body, headers)
    response = conn.getresponse()
    data = response.read()
    print(data)
    data = json.loads(data)
    conn.close()
    cat1 = data['Classification']['Category1']['Score']
    cat2 = data['Classification']['Category2']['Score']
    cat3 = data['Classification']['Category3']['Score']
    review = data['Classification']['ReviewRecommended']
    print(cat1,cat2,cat3,type(review))


except Exception as e:
    print("error in text moderationfilter", e)
    pass