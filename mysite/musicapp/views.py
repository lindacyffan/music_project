from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.core.paginator import Paginator
import pandas as pd
def song_list(request):
    df = pd.read_csv("C:/Users/53125/Desktop/music_project/data/lyrics_data_all.csv",encoding='utf-8-sig')

    songs = df.to_dict('records')

    paginator = Paginator(songs, 20)
    page_number = request.GET.get('page',1) # request.GET 相当于一个字典，里面存了URL？后面的键值对
    page_obj = paginator.get_page(page_number)
    return render(request, 'musicapp/song_list.html',{'page_obj':page_obj})# 请求页，模板，以及传给模板的数据
