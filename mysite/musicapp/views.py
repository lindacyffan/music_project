from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.shortcuts import redirect
import pandas as pd
import time
import json
import os
df = pd.read_csv("C:/Users/53125/Desktop/music_project/data/lyrics_data_all.csv",encoding='utf-8-sig')

songs = df.to_dict('records')
def song_list(request):
    paginator = Paginator(songs, 20)
    page_number = request.GET.get('page',1) # request.GET 相当于一个字典，里面存了URL？后面的键值对
    page_obj = paginator.get_page(page_number)
    return render(request, 'musicapp/song_list.html',{'page_obj':page_obj})# 请求页，模板，以及传给模板的数据
def song_detail(request,song_id):
    song_at_id = None
    for song in songs:
        if(song['id']==song_id):
            song_at_id = song
            break
    data = load_comments()
    return render(request, 'musicapp/song_detail.html',{'song':song_at_id,'comments':data.get(str(song_id),[])})
df2 = pd.read_csv("C:/Users/53125/Desktop/music_project/data/artists_unique.csv",encoding='utf-8-sig')

artists = df2.to_dict('records')
def artist_list(request):
    
    paginator = Paginator(artists, 20)
    page_number = request.GET.get('page',1) # request.GET 相当于一个字典，里面存了URL？后面的键值对
    page_obj = paginator.get_page(page_number)
    return render(request, 'musicapp/artist_list.html',{'page_obj':page_obj})# 请求页，模板，以及传给模板的数据

def artist_detail(request,artistid):
    artist_at_id = None
    for artist in artists:
        if(artist['artist_id']==artistid):
            artist_at_id = artist
            break

    songs_by_artist = []
    for song in songs:
        if song['artist_id']==artistid:
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
        playlist_song[source]=[]
    playlist_song[source].append(song)

def playlist_list(request):
    
    return render(request, 'musicapp/playlist_list.html',{'playlist':playlist_song})



def playlist_detail(request,source):
    return render(request, 'musicapp/playlist_detail.html',{'playlist_source':playlist_song[source],'source':source})


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
        for song in songs:
            if keyword in str(song['name']) or keyword in str(song['artist_name']) or keyword in str(song['lyrics']):
                results_list.append(song)
    if search_type == 'artist':
        for artist in artists:
            if keyword in str(artist['artist_name']) or keyword in str(artist['artist_intro']):
                results_list.append(artist)
    elapsed = round((time.time()-start_time)*1000 , 2)
    paginator = Paginator(results_list, 10)
    page_number = request.GET.get('page',1) # request.GET 相当于一个字典，里面存了URL？后面的键值对
    page_obj = paginator.get_page(page_number)
    return render(request, 'musicapp/search_results.html',{
        'page_obj':page_obj,
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