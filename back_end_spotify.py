# -*- coding: utf-8 -*-
"""
Created on Fri Nov  9 00:58:02 2018

@author: Ariclenes Silva
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi
import json
import requests

class spotify_back_end(object):
    def __init__(self, search):
        self.search = search

    def start(self):
        self.gst=self.get_spotify_token()
        self.headers = {'Authorization': 'Bearer ' + self.gst}
        self.response = requests.get('https://api.spotify.com/v1/search?query='+self.search+'&type=album&market=US&offset=0&limit=20', headers=self.headers)
        self.response_json = json.loads(self.response.content)
        self.response_items = self.response_json['albums']['items']
        
        everything=[]
        for items in self.response_items:
            for artists in items['artists']:
                art= artists['name'] # artists in the album
                break
            name_alb=items['name'] # name of the album
            rele_year=items['release_date'] # release date of the album
            total_track_alb=items['total_tracks'] # total track of the album
            album_id=items['id']
            
            everything.append([album_id,name_alb,art,rele_year,total_track_alb])
        return everything

    def get_spotify_token(self):
        self.client_id = '90813dad052f44bb96bd719a848f8ac7'
        self.client_secret = '9525c220f8784ca8a1ac4a950e805af9'
        self.grant_type = 'client_credentials'
        self.payload = {'client_id': self.client_id, 'client_secret': self.client_secret, 'grant_type': self.grant_type}
        self.headers_dict = {'content-type':'application/x-www-form-urlencoded'}
        self.response_json = requests.post("https://accounts.spotify.com/api/token/",data = self.payload, headers = self.headers_dict)
        self.response = json.loads(self.response_json.content)
        return self.response['access_token'] 