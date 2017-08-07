from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from .models import Album,Song
from .forms import AlbumForm,SongForm

AUDIO_FILE_TYPES=['wav','mp3','ogg','flac']
IMAGE_FILE_TYPES=['png','jpg','jpeg']

@login_required
def index(request):
    template='index.html'   
    albums=Album.objects.filter(user=request.user)
    songs=Song.objects.all()
    context={'albums':albums}
    query=request.GET.get("q")
    if query:
        albums=albums.filter(Q(album_title__icontains=query)| Q(artist__icontains=query)).distinct()
        songs=songs.filter(Q(song_title__icontains=query)).distinct()
        context={'albums':albums,'songs':songs}
        return render(request,template,context)
    else:
        return render(request,template,context)
        

@login_required
def create_album(request):
    form=AlbumForm(request.POST or None,request.FILES or None)
    if form.is_valid():
        album=form.save(commit=False)
        album.user=request.user
        album.album_logo=request.FILES['album_logo']
        file_type=album.album_logo.url.split('.')[-1]
        file_type=file_type.lower()
        if file_type not in IMAGE_FILE_TYPES:
            context={'album':album,'form':form,'error_message':'Image file must be .PNG,.JPG or .JPEG',}
            return render(request,'create_album.html',context)
        album.save()
        return render(request,'detail.html',{'album':album})
    context={'form':form}
    return render(request,'create_album.html',context)

@login_required
def detail(request,album_id):
    user=request.user
    album=get_object_or_404(Album,pk=album_id)
    return render(request,'detail.html',{'album':album,'user':user})

@login_required
def songs(request, filter_by):
    try:
        song_ids=[]
        for album in Album.objects.filter(user=request.user):
            for song in album.song_set.all():
                song_ids.append(song.pk)
            user_songs=Song.objects.filter(pk__in=song_ids)
            if filter_by == 'favorites':
                user_songs=user_songs.filter(is_favorite=True)
    except Album.DoesNotExist:
        user_songs=[]
    return render(request,'songs.html',{'song_list':user_songs,'filter_by':filter_by})

def add_song(request,album_id):
    form=SongForm(request.POST or None, request.FILES or None)
    album=get_object_or_404(Album,pk=album_id)
    if request.method=='POST' and form.is_valid():
        album_songs=album.song_set.all()
        for s in album_songs:
            if s.song_title==form.cleaned_data.get("song_title"):
                context={'album':album,'form':form,'error_message':'You already added that song'}
                return render(request,'add_song.html',context)
        song=form.save(commit=False)
        song.album=album
        song.audio_file=request.FILES['audio_file']   
        file_type=song.audio_file.url.split('.')[-1]
        file_type=file_type.lower()
        if file_type not in AUDIO_FILE_TYPES:
            context={'album':album,'form':form,'error_message':'Audio file must be supported file type(.WAV,.MP3,.OGG,.FLAC)'}
            return render(request,'add_song.html',context)
        song.save()
        return render(request,'detail.html',{'album':album})
    if request.method=='GET':
        context={'form':form,'album':album}
        return render(request,'add_song.html',context)

def delete_song(request,album_id,song_id):
    album=get_object_or_404(Album,pk=album_id)
    song=Song.objects.get(pk=song_id)
    song.delete()
    return render(request,'detail.html',{'album':album})

def favorite_song(request,song_id):
    song=get_object_or_404(Song,pk=song_id)
    try:
        if song.is_favorite:
            song.is_favorite=False
        else:
            song.is_favorite=True
        song.save()
    except (KeyError,Song.DoesNotExist):
        return JsonResponse({'success':False})
    else:
        return JsonResponse({'success':True})
    

def favorite_album(request,album_id):
#    albums=Album.objects.filter(user=request.user)
    album=get_object_or_404(Album,pk=album_id)
    try:
        if album.is_favorite:
            album.is_favorite=False
        else:
            album.is_favorite=True
        album.save()
    except (KeyError,Album.DoesNotExist):
        return JsonResponse({'success':False})
    else:
        return JsonResponse({'success':True})
    return render(request,'index.html',{'albums':albums})
    

def delete_album(request,album_id):
    album=Album.objects.get(pk=album_id)
    album.delete()
    albums=Album.objects.filter(user=request.user)
    return render(request,'index.html',{'albums':albums})