from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.shortcuts import redirect
import pandas as pd
import time
import json
import os
import jieba
from collections import defaultdict

inverted_index = defaultdict(set)
artist_inverted_index = defaultdict(set) # 键不存在的时候可以自动创建
songs = []
artists = []

df = pd.read_csv("C:/Users/53125/Desktop/music_project/data/lyrics_data_all.csv",encoding='utf-8-sig')
songs = df.to_dict('records')

def build_inverted_index():
    global inverted_index
    inverted_index.clear()
    for song in songs:
        text = f"{song['name']} {song['artist_name']} {song.get('lyrics', '')}"
        words = jieba.lcut(text)
        for word in set(words):
            if len(word) >= 1:
                inverted_index[word].add(song['id'])
build_inverted_index()



def song_list(request):
    paginator = Paginator(songs, 15)
    page_number = request.GET.get('page',1) # request.GET 相当于一个字典，里面存了URL？后面的键值对
    page_obj = paginator.get_page(page_number)
    current = page_obj.number
    total = page_obj.paginator.num_pages
    start = max(current - 3, 1)
    end = min(current + 3, total)
    page_range = range(start, end + 1)
    return render(request, 'musicapp/song_list.html',{'page_obj':page_obj,'page_range':page_range})# 请求页，模板，以及传给模板的数据

def song_detail(request,song_id):
    song_at_id = None
    for song in songs:
        if(song['id']==song_id):
            song_at_id = song
            break
    data = load_comments()
    return render(request, 'musicapp/song_detail.html',{'song':song_at_id,'comments':data.get(str(song_id),[])})

df2 = pd.read_csv("C:/Users/53125/Desktop/music_project/data/artists_unique_clean.csv",encoding='utf-8-sig')
artists = df2.to_dict('records')
def build_artist_inverted_index():
    global artist_inverted_index
    artist_inverted_index.clear()
    for artist in artists:
        text = f"{artist['artist_name']} {artist.get('artist_intro', '')}"
        words = jieba.lcut(text)
        for word in set(words):
            if len(word) >= 1:
                artist_inverted_index[word].add(artist['artist_id'])
build_artist_inverted_index()

def artist_list(request):
    
    paginator = Paginator(artists, 15)
    page_number = request.GET.get('page',1) # request.GET 相当于一个字典，里面存了URL？后面的键值对
    page_obj = paginator.get_page(page_number)
    current = page_obj.number
    total = page_obj.paginator.num_pages
    start = max(current - 3, 1)
    end = min(current + 3, total)
    page_range = range(start, end + 1)
    return render(request, 'musicapp/artist_list.html',{'page_obj':page_obj,'page_range':page_range})# 请求页，模板，以及传给模板的数据

def artist_detail(request,artist_id):
    artist_at_id = None
    for artist in artists:
        if(artist['artist_id']==artist_id):
            artist_at_id = artist
            break

    songs_by_artist = []
    for song in songs:
        if song['artist_id']==artist_id:
            songs_by_artist.append(song)
    return render(request, 'musicapp/artist_detail.html',{
        'artist':artist_at_id,
        'songs':songs_by_artist})# 请求页，模板，以及传给模板的数据

df3 = pd.read_csv("C:/Users/53125/Desktop/music_project/data/raw_data_all.csv",encoding='utf-8-sig')
songs_raw = df3.to_dict('records')
playlist_song = {}
for song in songs_raw:
    source = song.get('source','未知歌单')
    if source not in playlist_song:
        playlist_song[source] = []
    playlist_song[source].append(song)

def playlist_list(request):
    return render(request, 'musicapp/playlist_list.html',{'playlist':playlist_song})

def playlist_detail(request,source):
    paginator = Paginator(playlist_song[source],15)
    page_number = request.GET.get('page',1)
    page_obj = paginator.get_page(page_number)
    current = page_obj.number
    total = page_obj.paginator.num_pages
    start = max(current - 3, 1)
    end = min(current + 3, total)
    page_range = range(start, end + 1)
    return render(request, 'musicapp/playlist_detail.html',{'source':source,'page_range':page_range,'page_obj':page_obj})


def search(request):
    keyword = request.GET.get('q','').strip()
    search_type = request.GET.get('type','song')
    results_list = []
    start_time = time.time()
    if not keyword:
        elapsed = round((time.time()-start_time)*1000 , 2)
        empty_paginator = Paginator([],10)
        empty_page_obj = empty_paginator.get_page(1)
        return render(request, 'musicapp/search_results.html',{
            'page_obj':empty_page_obj,
            'keyword':keyword,
            'search_type':search_type,
            'count':0,
            'elapsed':elapsed,
            'message':'请输入内容'})
    if search_type == 'song':
        song_ids = inverted_index.get(keyword,set())
        results_list = [song for song in songs if song['id'] in song_ids]
    if search_type == 'artist':
        artist_ids = artist_inverted_index.get(keyword, set())
        results_list = [artist for artist in artists if artist['artist_id'] in artist_ids]
    elapsed = round((time.time()-start_time)*1000 , 2)
    paginator = Paginator(results_list, 12)
    page_number = request.GET.get('page',1) # request.GET 相当于一个字典，里面存了URL？后面的键值对
    page_obj = paginator.get_page(page_number)
    current = page_obj.number
    total = page_obj.paginator.num_pages
    start = max(current - 3, 1)
    end = min(current + 3, total)
    page_range = range(start, end + 1)
    return render(request, 'musicapp/search_results.html',{
        'page_obj':page_obj,
        'page_range':page_range,
        'keyword':keyword,
        'search_type':search_type,
        'count':len(results_list),
        'elapsed':elapsed})

def load_comments():
    with open('C:/Users/53125/Desktop/music_project/mysite/comments.json','r',encoding='utf-8') as file:
        data = json.load(file)
        return data
    

def save_comments(comments_updated):
    with open('C:/Users/53125/Desktop/music_project/mysite/comments.json','w',encoding='utf-8') as file:
        updated_data = json.dump(comments_updated,file,ensure_ascii=False,indent=2)
        return True

def add_comment(request,song_id):
    text = request.POST.get('comment_text','').strip()
    if text:
        data = load_comments()
        song_id=str(song_id)
        if song_id not in data:
            data[song_id]=[]
        comment_id = int(time.time() * 1000)
        data[song_id].append({
            'id':comment_id,
            '内容':text,
            '时间':time.strftime('%Y-%m-%d %H:%M:%S'),
            'likes':0,
        })
        save_comments(data)
    return redirect('musicapp:song_detail',song_id=song_id)
def delete_comment(request,song_id,comment_id):
    data = load_comments()
    song_id = str(song_id)
    for item in data[song_id]:
        if item['id']==comment_id:
            data[song_id].remove(item)
            break
    save_comments(data)
    return redirect('musicapp:song_detail',song_id=song_id)