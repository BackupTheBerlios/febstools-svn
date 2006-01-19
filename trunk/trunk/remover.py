#!/usr/bin/env python

import sys
from flickrapi import FlickrAPI

# Autenticazione
flickrAPIKey = "ea9b8730af07cd76f6dc4fde27744b74"  # API key
flickrSecret = "45dfeeb5abec1ff9"                  # shared "secret"
gruppo='91264405@N00'

# crea una istanza di FlickrAPI 
fapi = FlickrAPI(flickrAPIKey, flickrSecret)

# ottieni un token valido
token = fapi.getToken(browser="firefox", perms="write")
rsp = fapi.auth_checkToken(api_key=flickrAPIKey, auth_token=token)
fapi.testFailure(rsp)

#grabba tutte le foto con il group id specificato
rsp = fapi.groups_pools_getPhotos(auth_token=token,api_key=flickrAPIKey,group_id=gruppo)
fapi.testFailure(rsp)

for a in rsp.photos[0].photo:
	rsp = fapi.groups_pools_remove(api_key=flickrAPIKey,photo_id=a['id'],auth_token=token,group_id=gruppo)
	fapi.testFailure(rsp,exit=0)


