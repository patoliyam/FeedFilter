from django.shortcuts import render_to_response,render,redirect
from django.template.context import RequestContext
from django.contrib.auth import logout as auth_logout
from django.http import HttpResponse
import httplib, urllib
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
from null.models import *




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

def func1(url_of_image,a,count,userquery,block_list,post_id):
    # print "func 1"
    # '''image is being analyzed'''
    client = vision.ImageAnnotatorClient()
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
        for j in fuzoutput:
#             # print j[0],j[1],all_web_entities[j[0]]
            if(j[1]>50):
                if (Tag.objects.filter(tagname=query).count() == 0):
                    tmp = Tag(tagname=query, no_of_post=1)
                    tmp.save()
                else:
                    tmp = Tag.objects.filter(tagname=query)[0]
                    tmp.no_of_post = tmp.no_of_post + 1
                    tmp.save()
                if(post_id not in block_list):
                    # print "link of img blocked : " + url_of_image
                    block_list.append(post_id)

    '''text of image is being analyzed'''
    text_of_image = response.full_text_annotation.text
#     # print text_of_image
    accessKey = 'df0d9ef87db04d2a9985a64583e7e54a'
    uri = 'westus.api.cognitive.microsoft.com'
    path = '/text/analytics/v2.0/keyPhrases'
    documents = {'documents': [
        {'id': '1',
         'text': text_of_image},
    ]}
    headers = {'Ocp-Apim-Subscription-Key': accessKey}
    conn = httplib.HTTPSConnection(uri)
    body = json.dumps(documents)
    conn.request("POST", path, body, headers)
    response = conn.getresponse()
    keyword = response.read()
    keyword = json.loads(keyword)
    keyword = keyword['documents']
    if len(keyword) != 0:
        keyword = keyword[0]
        if keyword is not None:
            keyword = keyword['keyPhrases']
            for query in userquery:
                if(query.lower() in text_of_image.lower()):

                    if post_id not in block_list:
                        block_list.append(post_id)
                        # print "link of img blocked : " + url_of_image
                        if (Tag.objects.filter(tagname=query).count() == 0):
                            tmp = Tag(tagname=query, no_of_post=1)
                            tmp.save()
                        else:
                            tmp = Tag.objects.filter(tagname=query)[0]
                            tmp.no_of_post = tmp.no_of_post + 1
                            tmp.save()

                    continue
                for key in keyword:
                    match = dice_coefficient(key, query)
#                     # print ("Key :" + str(key) + "  Query : " + str(query) + "  Match : " + str(match))
                    if match > 0.1:
#                         # print "pahucha"

                        if post_id not in block_list :
                            block_list.append(post_id)
                            # print "link of img blocked : " + url_of_image
                            if (Tag.objects.filter(tagname=query).count() == 0):
                                tmp = Tag(tagname=query, no_of_post=1)
                                tmp.save()
                            else:
                                tmp = Tag.objects.filter(tagname=query)[0]
                                tmp.no_of_post = tmp.no_of_post + 1
                                tmp.save()
#                             # print block


    '''marking a post as eveluated'''
    count.append(1)

def  func3(url_of_image,a,count,userquery,block_list,post_id):
    start = time.time()
    # print start
    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': '8a08bd9c92f646e5b5189b0edc504746',
    }
    params = urllib.urlencode({
        # Request parameters
        'CacheImage': '{boolean}',
    })
    try:
        body = {"DataRepresentation":"URL","Value":url_of_image}
        conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
        conn.request("POST", "/contentmoderator/moderate/v1.0/ProcessImage/Evaluate?%s" % params, json.dumps(body), headers)
        response = conn.getresponse()
        data = response.read()
        # print "data :"
        # print(data)
        conn.close()
        if data.IsImageAdultClassified or data.IsImageRacyClassified:
            if (post_id not in block_list):
                # print "link of img blocked : " + url_of_image
                block_list.append(post_id)

    except Exception as e:
        pass


def func4(text_of_post,a,count,userquery,block, post_id):
    accessKey = 'df0d9ef87db04d2a9985a64583e7e54a'
    uri = 'westus.api.cognitive.microsoft.com'
    path = '/text/analytics/v2.0/sentiment'
    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': '{df0d9ef87db04d2a9985a64583e7e54a}',
    }
    params = urllib.urlencode({
    })

    try:
        conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
        documents = {'documents': [
            {"language": "en",
             'id': '1',
             'text': text_of_post },
        ]}
        headers = {'Ocp-Apim-Subscription-Key': accessKey}
        conn = httplib.HTTPSConnection(uri)
        body = json.dumps(documents)
        conn.request("POST", path, body, headers)
        response = conn.getresponse()
        data = response.read()
        data = json.loads(data)
        if(len(data["errors"])==0):
            if Post.objects.filter(post_id=post_id).count()==0:
                tmp = Post(post_id = post_id,sentiments = data["documents"][0]["score"])
                tmp.save()
        conn.close()

    except Exception as e:
        print(e)

def func2(text_of_post,a,count,userquery,block, post_id):
    start = time.time()
    accessKey = 'df0d9ef87db04d2a9985a64583e7e54a'
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
                        if(Tag.objects.filter(tagname=query).count()==0):
                            tmp = Tag(tagname=query,no_of_post=1)
                            tmp.save()
                        else:
                            tmp = Tag.objects.filter(tagname=query)[0]
                            tmp.no_of_post = tmp.no_of_post + 1
                            tmp.save()
                        if post_id not in block:
                            block.append(post_id)
                            # print "post blocked : " + text_of_post
                        continue
                    for key in keyword:

                        match = dice_coefficient(key,query)
                        # print ("Key :" + str(key) + "  Query : " + str(query) + "  Match : " + str(match))
                        if match > 0.1:
                            if (Tag.objects.filter(tagname=query).count() == 0):
                                tmp = Tag(tagname=query, no_of_post=1)
                                tmp.save()
                            else:
                                tmp = Tag.objects.filter(tagname=query)[0]
                                tmp.no_of_post = tmp.no_of_post + 1
                                tmp.save()
#                             # print "pahucha"
                            if post_id not in block :
                                block.append(post_id)
#                                 # print block
        count.append(1)

@csrf_exempt
def i_to_a(request):
    # print "inside i to a"
    count = []
    userquery = []
    i = 0
    while(request.POST.get('userquery[' + str(i) + ']')):
        userquery.append(request.POST.get('userquery['+ str(i)+']'))
        if Tag.objects.filter(tagname=request.POST.get('userquery[' + str(i) + ']')).count()==0:
            tmp = Tag(tagname=request.POST.get('userquery[' + str(i) + ']'),no_of_post=0)
            tmp.save()
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
                all_threads.append(threading.Thread(target=func1,args=(j['src'],index,count,userquery,block_list,post['id'])))
                all_threads[index].start()
                index = index + 1
                all_threads.append(threading.Thread(target=func3, args=(j['src'], index, count, userquery, block_list, post['id'])))
                all_threads[index].start()
                index = index + 1
#             # print "post end"

    start = time.time()
    while(2*len(count)!=index and time.time()-start<100):
        pass
    # print block_list
    for i in block_list:
        if BlockedPost.objects.filter(post_id=block_list[i]).count()==0:
            tmp  = BlockedPost(post_id=block_list[i])
            tmp.save()
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
        if Tag.objects.filter(tagname=request.POST.get('userquery[' + str(i) + ']')).count()==0:
            tmp = Tag(tagname=request.POST.get('userquery[' + str(i) + ']'),no_of_post=0)
            tmp.save()
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
            all_threads.append(threading.Thread(target=func2, args=(text_of_post, index, count, userquery, block_list, post['id'])))
            all_threads[index].start()
            index = index + 1
            all_threads.append(threading.Thread(target=func4, args=(text_of_post, index, count, userquery, block_list, post['id'])))
            all_threads[index].start()
            index = index + 1
#         # print "post end"
    start = time.time()
    while (2*len(count) != index and time.time() - start < 100):
        pass
    # print "block_list : " , block_list
    for i in block_list:
        if BlockedPost.objects.filter(post_id=i).count()==0:
            tmp  = BlockedPost(post_id=i)
            tmp.save()
    return JsonResponse({"status": True, "block_list": block_list})


