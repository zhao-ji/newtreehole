#!/usr/bin/env python
# -*- coding=utf-8 -*-

import urllib2

import oauth.oauth as oauth
from requests import get, post

consumer_key = "9eab891a46e90644738442f4c03d461b"
consumer_secret = "acce8a65db9d239e8ba5d9865ac6a1d6"
oauth_token_key = "1436156-3139ae61a2a46f72254ea00f1fbcfda1"
oauth_token_secret = "706fcb982ed0e5e21de71cf62c176006"
token = ("oauth_token_secret=706fcb982ed0e5e21de71cf62c176006&"
         "oauth_token=1436156-3139ae61a2a46f72254ea00f1fbcfda1")

signature_method = oauth.OAuthSignatureMethod_HMAC_SHA1()
consumer = oauth.OAuthConsumer(consumer_key, consumer_secret)
oauth_token = oauth.OAuthToken(oauth_token_key, oauth_token_secret)


def request_to_header(request, realm=''):
    """Serialize as a header for an HTTPAuth request."""
    auth_header = 'OAuth realm="%s"' % realm
    if request.parameters:
        for k, v in request.parameters.iteritems():
            if k.startswith('oauth_') or k.startswith('x_auth_'):
                auth_header += ', %s="%s"' % (k, oauth.escape(str(v)))
    return {'Authorization': auth_header}


def fanfou_get(url="statuses/user_timeline", **kwargs):
    url = 'http://api.fanfou.com/{}.json'.format(url)

    request = oauth.OAuthRequest.from_consumer_and_token(
        consumer,
        token=oauth_token,
        http_method='GET',
        http_url=url,
        parameters=kwargs,
    )
    request.sign_request(signature_method, consumer, oauth_token)

    headers = request_to_header(request)
    ret = get(url, params=kwargs, headers=headers)
    try:
        assert ret.ok
        return ret.json()
    except Exception, e:
        print e


def fanfou_post(url="statuses/update", **kwargs):
    url = 'http://api.fanfou.com/{}.json'.format(url)

    request = oauth.OAuthRequest.from_consumer_and_token(
        consumer,
        token=oauth_token,
        http_method='POST',
        http_url=url,
        parameters=kwargs,
    )
    request.sign_request(signature_method, consumer, oauth_token)
    headers = request_to_header(request)

    ret = post(url, data=kwargs, headers=headers)
    try:
        assert ret.ok
        return ret.json()
    except Exception, e:
        print e

from poster.encode import multipart_encode
from poster.streaminghttp import register_openers


def post_photo(file_string):
    register_openers()
    url = 'http://api.fanfou.com/photos/upload.xml'
    values = {'photo': file_string, 'status': '秘密图片', 'source': '发自微信'}
    data, headers = multipart_encode(values)
    request = oauth.OAuthRequest.from_consumer_and_token(
        consumer,
        token=oauth_token,
        http_method='POST',
        http_url=url,
        parameters={},
    )
    request.sign_request(signature_method, consumer, oauth_token)
    headers.update(request_to_header(request))
    req = urllib2.Request(url, data, headers=headers)
    req.unverifiable = True
    try:
        result = urllib2.urlopen(req)
        if result.getcode() == 200:
            return 1
    except Exception, e:
        return e.read()
