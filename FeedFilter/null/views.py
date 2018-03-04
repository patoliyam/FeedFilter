from django.shortcuts import render_to_response, render, redirect
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
import time, os, io, threading
from google.cloud import vision
from django.views.decorators.csrf import csrf_exempt
from bs4 import BeautifulSoup
import base64
# import unicodedata
import requests
from models import *
from django.db.models import Count, Min, Sum, Avg

@csrf_exempt
def register(request):
    if request.method == 'POST':
        username = (request.POST.get('username'))
        password = (request.POST.get('password'))
        if User.objects.filter(username=username).count() > 0:
            return JsonResponse({"status": 0})
        user = User.objects.create_user(username=username, password=password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({"status": 1})
    else:
        return JsonResponse({"status": 0})


@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        username = (request.POST.get('username'))
        password = (request.POST.get('password'))
        user = authenticate(username=username, password=password)
        if user is not None and user.is_authenticated:
            login(request, user)
            return JsonResponse({"status": 1})
        else:
            return JsonResponse({"status": 0})
    else:
        return JsonResponse({"status": 0})


@csrf_exempt
def logout_view(request):
    # print(request.user)
    if request.user is not None and request.user.is_authenticated:
        logout(request)
        return JsonResponse({"status": 1})
    else:
        return JsonResponse({"status": 0})


@csrf_exempt
def checklogin(request):
    if request.user is not None and request.user.is_authenticated:
        return JsonResponse({"status": 1})
    else:
        return JsonResponse({"status": 0})


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


def image_filter(url_of_image, a, count, userquery, block_list, post_id, request,textmodvalue):
    # print "func 1"
    '''image is being analyzed'''
    if (url_of_image):
        client = vision.ImageAnnotatorClient()
        imgurl1 = urllib2.urlopen(
            url_of_image).read()
        print(url_of_image)
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

                if (fuz[1] > 70):
                    if (Tag.objects.filter(tagname=str(fuz[0])).count() == 0):
                        tmp = Tag(tagname=str(fuz[0]), no_of_post=1)
                        tmp.save()
                    else:
                        tmp = Tag.objects.filter(tagname=str(fuz[0]))[0]
                        tmp.no_of_post = tmp.no_of_post + 1
                        tmp.save()
                    if (post_id not in block_list):
                        # print "link of img blocked : " + url_of_image
                        if BlockedPost.objects.filter(user=request.user, post_id=str(post_id)).count() == 0:
                            tmp = BlockedPost(user=request.user, post_id=str(post_id), post_type='0',
                                              text_or_url=url_of_image)
                            tmp.save()
                        block_list.append(post_id)
        print("in image_filter")
        print(block_list)
        temp = []
        text_of_image = response.full_text_annotation.text
        print("text_of_image : ", text_of_image)
        sentiment_analyzer(text_of_image, '', temp, userquery, block_list, post_id, request)

        text_filter(text_of_image, '', temp, userquery, block_list, post_id, request)

        if (textmodvalue):
            print("")
            text_moderation(text_of_image, '', temp, userquery, block_list, post_id, request)

    count.append(1)


# using content_moderator api. it is content moderator ( not vision).
def adult_racy_filter(url_of_image, a, count, userquery, block_list, post_id, request):
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
    if (url_of_image):
        try:
            body = {"DataRepresentation": "URL", "Value": url_of_image}
            conn = httplib.HTTPSConnection('eastasia.api.cognitive.microsoft.com')
            conn.request("POST", "/contentmoderator/moderate/v1.0/ProcessImage/Evaluate?%s" % params, json.dumps(body),
                         headers)
            response = conn.getresponse()
            data = response.read()
            print "data from adult_Racy api:"
            data = json.loads(data)
            print(data['RacyClassificationScore'])
            print(data['AdultClassificationScore'])
            conn.close()
            if data['RacyClassificationScore'] > 0.4:
                if (post_id not in block_list):
                    block_list.append(post_id)
                    if Stats.objects.filter(sentiment_type='2',user=request.user).count() == 0:
                        tmp = Stats(user=request.user, sentiment_type='2', count=1)
                        tmp.save()
                    else:
                        tmp = Stats.objects.filter(user=request.user, sentiment_type='2')[0]
                        tmp.count = tmp.count + 1
                        tmp.save()
                    if BlockedPost.objects.filter(user=request.user, post_id=str(post_id)).count() == 0:
                        tmp = BlockedPost(user=request.user, post_id=str(post_id), post_type='0', text_or_url=url_of_image)
                        tmp.save()
            elif data['AdultClassificationScore'] > 0.4:
                if (post_id not in block_list):
                    block_list.append(post_id)
                    if Stats.objects.filter(sentiment_type='1',user=request.user).count() == 0:
                        tmp = Stats(user=request.user, sentiment_type='1', count=1)
                        tmp.save()
                    else:
                        tmp = Stats.objects.filter(user=request.user, sentiment_type='1')[0]
                        tmp.count = tmp.count + 1
                        tmp.save()
                    if BlockedPost.objects.filter(user=request.user, post_id=str(post_id)).count() == 0:
                        tmp = BlockedPost(user=request.user, post_id=str(post_id), post_type='0', text_or_url=url_of_image)
                        tmp.save()
            print("adult racy")
            print(block_list)
        except Exception as e:
            pass
        # print("error in adult racy filter",e)
    count.append(1)


# using moderation api. Gives three score for a text
def text_moderation(text_of_post, a, count, userquery, block_list, post_id, request):
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
    if text_of_post:
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
            if review:
                if post_id not in block_list:
                    block_list.append(post_id)
                    if BlockedPost.objects.filter(user=request.user, post_id=str(post_id)).count() == 0:
                        tmp = BlockedPost(user=request.user, post_id=str(post_id), post_type='1', text_or_url=text_of_post)
                        tmp.save()
            elif cat1 > 0.4 and (cat1>cat2 and cat1>cat3):
                if post_id not in block_list:
                    block_list.append(post_id)
                    if Stats.objects.filter(user=request.user,sentiment_type='1').count() == 0:
                        tmp = Stats(user=request.user, sentiment_type='1', count=0)
                        tmp.save()
                    else:
                        tmp = Stats.objects.filter(user=request.user, sentiment_type='1')[0]
                        tmp.count = tmp.count + 1
                        tmp.save()
                    if BlockedPost.objects.filter(user=request.user, post_id=str(post_id)).count() == 0:
                        tmp = BlockedPost(user=request.user, post_id=str(post_id), post_type='1', text_or_url=text_of_post)
                        tmp.save()
            elif cat2 > 0.4 and (cat2>cat1 and cat2>cat3):
                if post_id not in block_list:
                    block_list.append(post_id)
                    if Stats.objects.filter(user=request.user,sentiment_type='3').count() == 0:
                        tmp = Stats(user=request.user, sentiment_type='3', count=0)
                        tmp.save()
                    else:
                        tmp = Stats.objects.filter(user=request.user, sentiment_type='3')[0]
                        tmp.count = tmp.count + 1
                        tmp.save()
                    if BlockedPost.objects.filter(user=request.user, post_id=str(post_id)).count() == 0:
                        tmp = BlockedPost(user=request.user, post_id=str(post_id), post_type='1', text_or_url=text_of_post)
                        tmp.save()
            elif cat3 > 0.4 and (cat3>cat1 and cat3>cat2):
                if post_id not in block_list:
                    block_list.append(post_id)
                    if Stats.objects.filter(user=request.user,sentiment_type='0').count() == 0:
                        tmp = Stats(user=request.user, sentiment_type='0', count=0)
                        tmp.save()
                    else:
                        tmp = Stats.objects.filter(user=request.user, sentiment_type='0')[0]
                        tmp.count = tmp.count + 1
                        tmp.save()
                    if BlockedPost.objects.filter(user=request.user, post_id=str(post_id)).count() == 0:
                        tmp = BlockedPost(user=request.user, post_id=str(post_id), post_type='1', text_or_url=text_of_post)
                        tmp.save()

        except Exception as e:
            print("error in text moderationfilter", e)
            pass
        print("in text moderation")
        print(block_list)
    count.append(1)


# using text analytics api. Gives a single score for sentiment
def sentiment_analyzer(text_of_post, a, count, userquery, block_list, post_id, request):
    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': 'eac4641ee0cf4d9183a7114fceca02aa',
    }

    params = urllib.urlencode({
    })
    if(text_of_post):
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
            print(data)
            conn.close()
            score = data['documents'][0]['score']
            for k in userquery:
                if UserPost.objects.filter(post_id=post_id, user=request.user).count() > 0:
                    tmp = UserPost(user=request.user, post_id=post_id, sentiment_score=score,tagname=k)
                    tmp.save()
            if score < 0.5:
                if post_id not in block_list:
                    block_list.append(post_id)
                    if BlockedPost.objects.filter(user=request.user, post_id=str(post_id)).count() == 0:
                        tmp = BlockedPost(user=request.user, post_id=str(post_id), post_type='1', text_or_url=text_of_post)
                        tmp.save()
        except Exception as e:
            print("error in text sentiment filter api", e)
            pass
        print("in sentiment analysis")
        print(block_list)
    count.append(1)


# using text analytics api. Gives keywords from text
def text_filter(text_of_post, a, count, userquery, block_list, post_id, request):
    start = time.time()

    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': 'eac4641ee0cf4d9183a7114fceca02aa',
    }

    params = urllib.urlencode({
        # Request parameters
        'numberOfLanguagesToDetect': '1',
    })

    # print("text", text_of_post)
    body = {'documents': [
        {'id': '1',
         'text': text_of_post},
    ]}
    if (text_of_post):
        try:
            conn = httplib.HTTPSConnection('eastasia.api.cognitive.microsoft.com')
            conn.request("POST", "/text/analytics/v2.0/keyPhrases?%s" % params, json.dumps(body), headers)
            response = conn.getresponse()
            keyword = response.read()
            # print(keyword)
            conn.close()
        except Exception as e:
            print("Errno")

        for query in userquery:
            if (query.lower() in text_of_post.lower()):
                if (Tag.objects.filter(tagname=query).count() == 0):
                    tmp = Tag(tagname=query, no_of_post=1)
                    tmp.save()
                else:
                    tmp = Tag.objects.filter(tagname=query)[0]
                    tmp.no_of_post = tmp.no_of_post + 1
                    tmp.save()
                if post_id not in block_list:
                    block_list.append(post_id)
                    if BlockedPost.objects.filter(user=request.user, post_id=str(post_id)).count() == 0:
                        tmp = BlockedPost(user=request.user, post_id=str(post_id), post_type='1',text_or_url=text_of_post)
                        tmp.save()

        keyword = json.loads(keyword)
        if 'documents' in keyword:
            keyword = keyword['documents']
            if len(keyword) != 0:
                keyword = keyword[0]
                if keyword is not None:
                    keyword = keyword['keyPhrases']
                    for query in userquery:
                        for key in keyword:
                            match = dice_coefficient(key, query)
                            if match > 0.4:
                                # print ("Key :" + str(key) + "  Query : " + str(query) + "  Match : " + str(match)+"post id " + post_id)
                                # ambiguity
                                if (Tag.objects.filter(tagname=key).count() == 0):
                                    tmp = Tag(tagname=key, no_of_post=1)
                                    tmp.save()
                                else:
                                    tmp = Tag.objects.filter(tagname=key)[0]
                                    tmp.no_of_post = tmp.no_of_post + 1
                                    tmp.save()
                                if post_id not in block_list:
                                    block_list.append(post_id)
                                    if BlockedPost.objects.filter(user=request.user, post_id=str(post_id)).count() == 0:
                                        tmp = BlockedPost(user=request.user, post_id=str(post_id), post_type='1',
                                                          text_or_url=text_of_post)
                                        tmp.save()
    print("in text filter")
    print(block_list)
    count.append(1)


@csrf_exempt
def i_to_a(request):
    print "came inside i to  check"
    print(request.user.username)
    textmodvalue = request.POST.get('textmodvalue')
    imagemodvalue = request.POST.get('imagemodvalue')
    count = []
    userquery = []
    i = 0
    userquery_data = UserTag.objects.filter(user=request.user)
    for i in userquery_data:
        userquery.append(i.tagname.lower())
    for i in range(0,len(userquery)):
        if Tag.objects.filter(tagname=userquery[i]).count() == 0:
            tmp = Tag(tagname=userquery[i], no_of_post=0)
            tmp.save()
    all_threads = []
    index = 0
    block_list = []
    for i in request.POST:
        soup = BeautifulSoup(request.POST.get(i), "html.parser")
        #         # print request.POST.get(i)
        src_of_imgs = soup.findAll('img', attrs={'class': 'scaledImageFitWidth'})
        # print "src_of_imgs :" , src_of_imgs
        if src_of_imgs is not None:
            for j in src_of_imgs:
                post = soup.find('div')
                if (UserPost.objects.filter(user=request.user, postid=post['id'], post_category='0').count() == 0):
                    tmp = UserPost(user=request.user, postid=post['id'], post_category='0')
                    tmp.save()
                    all_threads.append(threading.Thread(target=image_filter, args=(j['src'], index, count, userquery, block_list, post['id'], request,textmodvalue)))
                    all_threads[index].start()
                    index = index + 1
                    if imagemodvalue:
                        print("")
                        all_threads.append(threading.Thread(target=adult_racy_filter, args=(j['src'], index, count, userquery, block_list, post['id'],request)))
                        all_threads[index].start()
                        index = index + 1
    start = time.time()
    # to check all the threads have completed
    while (2*len(count) != index and time.time() - start < 100):
        pass
    print("in i to a blocklist")
    print block_list
    return JsonResponse({"status": True, "block_list": block_list})

@csrf_exempt
def t_to_a(request):
    count = []
    userquery = []
    i = 0
    print "came in t_to_a"
    textmodvalue = request.POST.get('textmodvalue')
    imagemodvalue = request.POST.get('imagemodvalue')
    i = 0
    userquery_data = UserTag.objects.filter(user=request.user)
    for i in userquery_data:
        userquery.append(i.tagname.lower())
    for i in range(0,len(userquery)):
        if Tag.objects.filter(tagname=userquery[i]).count() == 0:
            tmp = Tag(tagname=userquery[i], no_of_post=0)
            tmp.save()
    all_threads = []
    index = 0
    block_list = []
    for i in request.POST:
        soup = BeautifulSoup(request.POST.get(i), "html.parser")
        posttext = soup.findAll('div', attrs={'class': 'userContent'})
        for j in posttext:
            #             # print "this is one item : ",  j.text
            text_of_post = j.text
            post = soup.find('div')

            userquery2 = []
            for k in userquery:
                if(UserPost.objects.filter(user=request.user,postid=post['id'],post_category='1',tagname=k).count() == 0):
                    userquery2.append(k)

            for t in userquery2:
                tmp = UserPost(user=request.user,postid=post['id'],post_category='1',tagname=t)
                tmp.save()
                all_threads.append(threading.Thread(target=text_filter, args=(text_of_post, index, count, userquery2, block_list, post['id'], request)))
                all_threads[index].start()
                index = index + 1
                # all_threads.append(threading.Thread(target=sentiment_analyzer, args=(text_of_post, index, count, userquery2, block_list, post['id'], request)))
                # all_threads[index].start()
                # index = index + 1
                # if (textmodvalue):
                #     print("")
                #     all_threads.append(threading.Thread(target=text_moderation, args=(text_of_post, index, count, userquery2, block_list, post['id'], request)))
                #     all_threads[index].start()
                #     index = index + 1
    start = time.time()
    while (len(count) != index and time.time() - start < 100):
        pass
    # print("blocklist in t_to_a")
    # print(block_list)
    return JsonResponse({"status": True, "block_list": block_list})


def dashboard(request):
    if request.method == "GET":

        username = request.GET.get('username')
        password = request.GET.get('password')
        if request.user is None or not request.user.is_authenticated():
            user = authenticate(username=username,password=password)
            login(request,user)
        all_tags= Tag.objects.order_by('no_of_post')
        tags_to_suggest = []
        cur = 0
        for i in all_tags:
            if(cur==5):
                break
            if(UserTag.objects.filter(user=request.user,tag_type='0',tagname=i.tagname).count() == 0):
                tags_to_suggest.append(i)
                cur = cur+1
        stats0 = 0
        stats1 = 0
        stats2 = 0
        stats3 = 0
        stats4 = 0
        label0 = 0
        label1 = 0
        label2 = 0
        label3 = 0
        label4 = 0
        if Stats.objects.filter(user=request.user, sentiment_type='0').count() > 0 :
            stats0 = Stats.objects.filter(user=request.user, sentiment_type='0')[0].count
        if Stats.objects.filter(user=request.user, sentiment_type='1').count() > 0 :
            stats1 = Stats.objects.filter(user=request.user, sentiment_type='1')[0].count
        if Stats.objects.filter(user=request.user, sentiment_type='2').count() > 0 :
            stats2 = Stats.objects.filter(user=request.user, sentiment_type='2')[0].count
        if Stats.objects.filter(user=request.user, sentiment_type='3').count() > 0 :
            stats3 = Stats.objects.filter(user=request.user, sentiment_type='3')[0].count
        total = UserPost.objects.filter(user=request.user).distinct('postid').count()
        print(total,stats0,stats1,stats2,stats3)
        stats4 = total - (stats0+stats1+stats2+stats3)
        if total > 0 :
            label0 = str(stats0*100/total)
            label1 = str(stats1*100/total)
            label2 = str(stats2*100/total)
            label3 = str(stats3*100/total)
            label4 = str(stats4*100/total)
        # print "stats 1 : " , stats1
        generic_tags = UserTag.objects.filter(user=request.user, tag_type='0')
        account_tags = UserTag.objects.filter(user=request.user, tag_type='1')
        # print "tags_to_suggest : " , tags_to_suggest
        # print "generic tags : " , generic_tags
        # # # print "stats : ", stats
        # print "account tags : ", account_tags
        myset = UserPost.objects.filter(user=request.user).distinct('postid')
        total = 0
        count = myset.count()
        for i in myset:
            total = total+i.sentiment_score
        if count>0:
            happy_value = total*100
        else:
            happy_value = 0
        print(happy_value)
        sad_value = 100.0-happy_value
        return render(request,'null/dashboard.html', {'tags_to_suggest' : tags_to_suggest,
                                                      'stats0' : stats0,
                                                      'stats1' : stats1,
                                                      'stats2' : stats2,
                                                      'stats3' : stats3,
                                                      'stats4': stats4,
                                                      'label0': label0,
                                                      'label1': label1,
                                                      'label2': label2,
                                                      'label3': label3,
                                                      'label4': label4,
                                                      'generic_tags':generic_tags,
                                                      'account_tags':account_tags,
                                                      'happy_value': happy_value,
                                                      'sad_value':sad_value})

def blocked_content(request):
    if request.method=="GET":
        blocked_posts = BlockedPost.objects.filter(user=request.user)
        # print blocked_posts
        return render(request,'null/blocked_content.html',{'blocked_posts':blocked_posts})


def addtag(request):
    tagname = request.GET.get('tagname')
    tagtype = request.GET.get('tagtype')
    print(tagtype)
    if(UserTag.objects.filter(user=request.user,tagname=tagname,tag_type=tagtype).count()==0):
        tmp = UserTag(user=request.user,tagname=tagname,tag_type=tagtype)
        tmp.save()
        return JsonResponse({"status":1})
    else:
        return JsonResponse({"status":0})

def removetag(request):
    tagname = request.GET.get('tagname')
    tagtype = request.GET.get('tagtype')
    # print(tagname,tagtype,request.user.username)
    # print(UserTag.objects.filter(user=request.user, tagname=tagname, tag_type=int(tagtype)).count())
    if (UserTag.objects.filter(user=request.user, tagname=tagname, tag_type=int(tagtype)).count() > 0):
        UserTag.objects.get(user=request.user, tagname=str(tagname), tag_type=int(tagtype)).delete()
        return JsonResponse({"status": 1})
    else:
        return JsonResponse({"status": 0})

def fetchtag(request):
    type = request.GET.get('type')
    print type
    if type:
        usertag = UserTag.objects.filter(user=request.user,tag_type=type)
    else:
        usertag = UserTag.objects.filter(user=request.user)
    tags = []
    tagtype = []
    for t in usertag:
        tags.append(t.tagname)
        tagtype.append(t.tag_type)
    return JsonResponse({"status":1,"usertag":tags,"usertagtype":tagtype})
