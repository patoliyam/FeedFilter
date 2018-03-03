from django.shortcuts import render_to_response,render,redirect
from django.template.context import RequestContext
from django.contrib.auth import logout as auth_logout
from django.http import HttpResponse
import httplib, urllib
from django.contrib.auth import authenticate, login, logout
import urllib2, json
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from django.http import Http404
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.contrib.auth.models import User
import time , os, io, threading
from google.cloud import vision
from django.views.decorators.csrf import csrf_exempt
from bs4 import BeautifulSoup
import base64
import unicodedata
import requests
from models import *

@csrf_exempt
def register(request):
    if request.method == 'POST':
        username = (request.POST.get('username'))
        password = (request.POST.get('password'))
        if User.objects.filter(username=username).count() > 0:
            return JsonResponse({"status":0})
        user = User.objects.create_user(username=username,password=password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({"status":1})
    else:
        return JsonResponse({"status":0})

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        username = (request.POST.get('username'))
        password = (request.POST.get('password'))
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({"status":1})
        else:
            return JsonResponse({"status":0})
    else:
        return JsonResponse({"status":0})

@csrf_exempt
def logout_view(request):
    # print(request.user)
    if request.user is not None and request.user.is_authenticated:
        logout(request)
        return JsonResponse({"status":1})
    else:
        return JsonResponse({"status":0})

@csrf_exempt
def checklogin(request):
    if request.user is not None and request.user.is_authenticated:
        return JsonResponse({"status":1})
    else:
        return JsonResponse({"status":0})

def dice_coefficient(a, b):
    """dice coefficient 2nt/na + nb."""
    if not len(a) or not len(b): return 0.0
    if len(a) == 1:  a = a + u'.'
    if len(b) == 1:  b = b + u'.'

    a_bigram_list = []
    for i in range(len(a) - 1):
        a_bigram_list.append(a[i:i + 2])
    b_bigram_list = []
    for i in range(len(b) - 1):
        b_bigram_list.append(b[i:i + 2])

    a_bigrams = set(a_bigram_list)
    b_bigrams = set(b_bigram_list)
    overlap = len(a_bigrams & b_bigrams)
    dice_coeff = overlap * 2.0 / (len(a_bigrams) + len(b_bigrams))
    return dice_coeff

def image_filter(url_of_image,a,count,userquery,block_list,post_id,request):
    # print "func 1"
    '''image is being analyzed'''
    print("image is being analyzed")
    client = vision.ImageAnnotatorClient()
    print(url_of_image)
    imgurl1 = urllib2.urlopen(
        url_of_image).read()
    response = client.annotate_image({
        'image': {
            'content': imgurl1
        },
        'features': [
            {'type': vision.enums.Feature.Type.WEB_DETECTION}, {'type': vision.enums.Feature.Type.TEXT_DETECTION},
        ],
    })
    labels = response
    all_web_entities = {}
    web_entities = labels.web_detection.web_entities
    for i in web_entities:
        all_web_entities[i.description] = i.score
    choices = all_web_entities.keys()
    for query in userquery:
        fuzoutput = process.extract(query, choices, limit=5)
        # print(fuzoutput)
        for fuz in fuzoutput:
            # print fuz[0],fuz[1],all_web_entities[fuz[0]]
            if(fuz[1]>70):
                # ambiguity
                # if (Tag.objects.filter(tagname=query).count() == 0):
                #     tmp = Tag(tagname=query, no_of_post=1)
                #     tmp.save()
                # else:
                #     tmp = Tag.objects.filter(tagname=query)[0]
                #     tmp.no_of_post = tmp.no_of_post + 1
                #     tmp.save()
                if(post_id not in block_list):
                    # print "link of img blocked : " + url_of_image
                    if BlockedPost.objects.filter(user=request.user, post_id=str(post_id)).count() == 0:
                        tmp = BlockedPost(user=request.user, post_id=str(post_id), post_type='0',
                                          text_or_url=url_of_image)
                        tmp.save()
                    block_list.append(post_id)
    # print("ye wala")
    # print(block_list)

#     '''text of image is being analyzed'''
#     text_of_image = response.full_text_annotation.text
#     accessKey = 'b188ffaad0c34867b8804255cdea2706'
#     uri = 'eastasia.api.cognitive.microsoft.com'
#     path = '/text/analytics/v2.0/keyPhrases'
#     documents = {'documents': [
#         {'id': '1',
#          'text': text_of_image},
#     ]}
#     headers = {'Ocp-Apim-Subscription-Key': accessKey}
#     conn = httplib.HTTPSConnection(uri)
#     body = json.dumps(documents)
#     conn.request("POST", path, body, headers)
#     response = conn.getresponse()
#     keyword = response.read()
#     keyword = json.loads(keyword)
#     keyword = keyword['documents']
#     if len(keyword) != 0:
#         keyword = keyword[0]
#         if keyword is not None:
#             keyword = keyword['keyPhrases']
#             for query in userquery:
#                 if(query.lower() in text_of_image.lower()):
#                     if post_id not in block_list:
#                         block_list.append(post_id)
#                         # print "link of img blocked : " + url_of_image
#                         # if (Tag.objects.filter(tagname=query).count() == 0):
#                         #     tmp = Tag(tagname=query, no_of_post=1)
#                         #     tmp.save()
#                         # else:
#                         #     tmp = Tag.objects.filter(tagname=query)[0]
#                         #     tmp.no_of_post = tmp.no_of_post + 1
#                         #     tmp.save()
#                     continue
#                 for key in keyword:
#                     match = dice_coefficient(key, query)
# #                     # print ("Key :" + str(key) + "  Query : " + str(query) + "  Match : " + str(match))
#                     if match > 0.4:
#                         if post_id not in block_list :
#                             block_list.append(post_id)
#                             # if (Tag.objects.filter(tagname=query).count() == 0):
#                             #     tmp = Tag(tagname=query, no_of_post=1)
#                             #     tmp.save()
#                             # else:
#                             #     tmp = Tag.objects.filter(tagname=query)[0]
#                             #     tmp.no_of_post = tmp.no_of_post + 1
#                             #     tmp.save()
    # '''marking a post as eveluated'''

    temp = []
    text_of_image = response.full_text_annotation.text

    print("text_of_image : " ,text_of_image)

    text_moderation(text_of_image,'',temp,userquery,block_list,post_id)

    sentiment_analyzer(text_of_image,'',temp,userquery,block_list,post_id)

    text_filter(text_of_image,'',temp,userquery,block_list,post_id)

    count.append(1)


# using content_moderator api. it is content moderator ( not vision).
def adult_racy_filter(url_of_image,a,count,userquery,block_list,post_id,request):
    start = time.time()
    # print start
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
        body = {"DataRepresentation":"URL","Value":url_of_image}
        conn = httplib.HTTPSConnection('eastasia.api.cognitive.microsoft.com')
        conn.request("POST", "/contentmoderator/moderate/v1.0/ProcessImage/Evaluate?%s" % params, json.dumps(body), headers)
        response = conn.getresponse()
        data = response.read()
        print "data from adult_Racy api:"
        data = json.loads(data)
        # print(data)
        conn.close()
        if data['RacyClassificationScore']> 0.2 or data['AdultClassificationScore'] > 0.2:
            if (post_id not in block_list):
                if BlockedPost.objects.filter(user=request.user, post_id=str(post_id)).count() == 0:
                    tmp = BlockedPost(user=request.user, post_id=str(post_id), post_type='0', text_or_url=url_of_image)
                    tmp.save()
                block_list.append(post_id)
    except Exception as e:
        # print("error in adult racy filter",e)
        pass
    count.append(1)

# using moderation api. Gives three score for a text
def text_moderation(text_of_post,a,count,userquery,block_list, post_id,request):
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
    body = str(text_of_post)
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

        if review or cat1 > 0.2 or cat2 > 0.2 or cat3 > 0.2:
            if post_id not in block_list:
                block_list.append(post_id)
                if BlockedPost.objects.filter(user=request.user, post_id=str(post_id)).count() == 0:
                    tmp = BlockedPost(user=request.user, post_id=str(post_id), post_type='1', text_or_url=text_of_post)
                    tmp.save()

    except Exception as e:
        print("error in text moderationfilter", e)
        pass
    count.append(1)

# using text analytics api. Gives a single score for sentiment
def sentiment_analyzer(text_of_post,a,count,userquery,block_list, post_id,request):
    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': 'eac4641ee0cf4d9183a7114fceca02aa',
    }

    params = urllib.urlencode({
    })

    try:
        body = {"documents": [
                                {
                                  "language": "en",
                                  "id": "1",
                                  "text": text_of_post
                                }
                            ]
                }
        conn = httplib.HTTPSConnection('eastasia.api.cognitive.microsoft.com')
        conn.request("POST", "/text/analytics/v2.0/sentiment?%s" % params, json.dumps(body), headers)
        response = conn.getresponse()
        data = response.read()
        data = json.loads(data)
        conn.close()
        score = data['documents'][0]['score']
        if score < 0.5:
            if post_id not in block_list:
                block_list.append(post_id)
                if BlockedPost.objects.filter(user=request.user, post_id=str(post_id)).count() == 0:
                    tmp = BlockedPost(user=request.user, post_id=str(post_id), post_type='1', text_or_url=text_of_post)
                    tmp.save()
    except Exception as e:
        print("error in text sentiment filter api", e)
        pass
    count.append(1)

# using text analytics api. Gives keywords from text
def text_filter(text_of_post,a,count,userquery,block_list, post_id,request):
    start = time.time()
    accessKey = 'b188ffaad0c34867b8804255cdea2706'
    uri = 'westus.api.cognitive.microsoft.com'
    path = '/text/analytics/v2.0/keyPhrases'
    documents = {'documents': [
        {'id': '1',
         'text': text_of_post},
    ]}
    headers = {'Ocp-Apim-Subscription-Key': accessKey}
    conn = httplib.HTTPSConnection(uri)
    body = json.dumps(documents)
    conn.request("POST", path, body, headers)
    response = conn.getresponse()
#     # print  (response.read())
    keyword = response.read()
    keyword = json.loads(keyword)
#     # print keyword
#     # print type(keyword['documents'])
    if 'documents' in keyword:
        keyword = keyword['documents']
        if len(keyword) != 0:
            keyword = keyword[0]
            if keyword is not None:
                keyword = keyword['keyPhrases']
                for query in userquery:
                    if (query.lower() in text_of_post.lower()):
                        # ambiguity
                        # if(Tag.objects.filter(tagname=query).count()==0):
                        #     tmp = Tag(tagname=query,no_of_post=1)
                        #     tmp.save()
                        # else:
                        #     tmp = Tag.objects.filter(tagname=query)[0]
                        #     tmp.no_of_post = tmp.no_of_post + 1
                        #     tmp.save()
                        if post_id not in block_list:
                            block_list.append(post_id)
                            if BlockedPost.objects.filter(user=request.user, post_id=str(post_id)).count() == 0:
                                tmp = BlockedPost(user=request.user, post_id=str(post_id), post_type='1',
                                                  text_or_url=text_of_post)
                                tmp.save()
                        continue
                    for key in keyword:
                        match = dice_coefficient(key,query)
                        # print ("Key :" + str(key) + "  Query : " + str(query) + "  Match : " + str(match))
                        if match > 0.1:
                            # ambiguity
                            # if (Tag.objects.filter(tagname=query).count() == 0):
                            #     tmp = Tag(tagname=query, no_of_post=1)
                            #     tmp.save()
                            # else:
                            #     tmp = Tag.objects.filter(tagname=query)[0]
                            #     tmp.no_of_post = tmp.no_of_post + 1
                            #     tmp.save()
                            if post_id not in block_list :
                                block_list.append(post_id)
                                if BlockedPost.objects.filter(user=request.user, post_id=str(post_id)).count() == 0:
                                    tmp = BlockedPost(user=request.user, post_id=str(post_id), post_type='1',
                                                      text_or_url=text_of_post)
                                    tmp.save()
        count.append(1)

@csrf_exempt
def i_to_a(request):
    print "came inside i to a"
    count = []
    userquery = []
    i = 0
    while(request.POST.get('userquery[' + str(i) + ']')):
        # print(i)
        # print(request.POST.get('userquery['+ str(i)+']'))
        userquery.append(request.POST.get('userquery['+ str(i)+']'))
        # if Tag.objects.filter(tagname=request.POST.get('userquery[' + str(i) + ']')).count()==0:
        #     tmp = Tag(tagname=request.POST.get('userquery[' + str(i) + ']'),no_of_post=0)
        #     tmp.save()
        i = i+1

    all_threads = []
    index = 0
    block_list = []
    for i in request.POST:
        soup = BeautifulSoup(request.POST.get(i), "html.parser")
#         # print request.POST.get(i)
        src_of_imgs = soup.findAll('img' , attrs={'class':'scaledImageFitWidth'})
        # print "src_of_imgs :" , src_of_imgs
        if src_of_imgs is  not None:
            for j in src_of_imgs:
                # # print j['src']
                # print "this is index : "+str(index)
                post = soup.find('div')
                # print post['id']
                all_threads.append(threading.Thread(target=image_filter,args=(j['src'],index,count,userquery,block_list,post['id'],request)))
                all_threads[index].start()
                index = index + 1
                all_threads.append(threading.Thread(target=adult_racy_filter, args=(j['src'], index, count, userquery, block_list, post['id'],request)))
                all_threads[index].start()
                index = index + 1
#             # print "post end"

    start = time.time()
    # to check all the threads have completed
    while(2*len(count)!=index and time.time()-start<100):
        pass
    print("in i to a blocklist")
    print block_list

    # error was unicode can't be key of dictionary
    # for i in block_list:
    #     if BlockedPost.objects.filter(post_id=str(block_list[i])).count()==0:
    #         tmp  = BlockedPost(post_id=block_list[i])
    #         tmp.save()
    return JsonResponse({"status":True,"block_list": block_list})

@csrf_exempt
def t_to_a(request):
    count = []
    userquery = []
    i = 0
    # print "t_to_a"
    # print request.POST.keys()
    while (request.POST.get('userquery[' + str(i) + ']')):
        userquery.append(request.POST.get('userquery[' + str(i) + ']'))
        # if Tag.objects.filter(tagname=request.POST.get('userquery[' + str(i) + ']')).count()==0:
        #     tmp = Tag(tagname=request.POST.get('userquery[' + str(i) + ']'),no_of_post=0)
        #     tmp.save()
#         # print userquery[i]
        i = i + 1
    all_threads = []
    index = 0
    block_list = []
    for i in request.POST:
#         # print request.POST.get(i)
        soup = BeautifulSoup(request.POST.get(i), "html.parser")
        posttext = soup.findAll('div', attrs={'class': 'userContent'})
        for j in posttext:
#             # print "this is one item : ",  j.text
            text_of_post = j.text
            post = soup.find('div')
#             # print post['id']
            all_threads.append(threading.Thread(target=text_filter, args=(text_of_post, index, count, userquery, block_list, post['id'],request)))
            all_threads[index].start()
            index = index + 1
            # all_threads.append(threading.Thread(target=sentiment_analyzer, args=(text_of_post, index, count, userquery, block_list, post['id'],request)))
            # all_threads[index].start()
            # index = index + 1
            # all_threads.append(threading.Thread(target=text_moderation, args=(text_of_post, index, count, userquery, block_list, post['id'],request)))
            # all_threads[index].start()
            # index = index + 1
#         # print "post end"
    start = time.time()
    while (len(count) != index and time.time() - start < 100):
        pass
    # print "block_list : " , block_list
    # for i in block_list:
    #     if BlockedPost.objects.filter(post_id=i).count()==0:
    #         tmp  = BlockedPost(post_id=i)
    #         tmp.save()
    return JsonResponse({"status": True, "block_list": block_list})