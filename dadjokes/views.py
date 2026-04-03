# views.py 

from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Joke, Picture
from .serializers import JokeSerializer, PictureSerializer


def get_random_joke():
    return Joke.objects.order_by('?').first()


def get_random_picture():
    return Picture.objects.order_by('?').first()


# ---------- HTML views ----------

def home(request):
    joke = get_random_joke()
    picture = get_random_picture()
    return render(request, 'dadjokes/random.html', {
        'joke': joke,
        'picture': picture,
    })


def random_page(request):
    joke = get_random_joke()
    picture = get_random_picture()
    return render(request, 'dadjokes/random.html', {
        'joke': joke,
        'picture': picture,
    })


def jokes_list(request):
    jokes = Joke.objects.all().order_by('-timestamp')
    return render(request, 'dadjokes/jokes_list.html', {
        'jokes': jokes,
    })


def joke_detail(request, pk):
    joke = get_object_or_404(Joke, pk=pk)
    return render(request, 'dadjokes/joke_detail.html', {
        'joke': joke,
    })


def pictures_list(request):
    pictures = Picture.objects.all().order_by('-timestamp')
    return render(request, 'dadjokes/pictures_list.html', {
        'pictures': pictures,
    })


def picture_detail(request, pk):
    picture = get_object_or_404(Picture, pk=pk)
    return render(request, 'dadjokes/picture_detail.html', {
        'picture': picture,
    })


# ---------- API views ----------

@api_view(['GET'])
def api_root(request):
    joke = get_random_joke()
    if joke is None:
        return Response({'error': 'No jokes found'}, status=404)

    serializer = JokeSerializer(joke)
    return Response(serializer.data)


@api_view(['GET'])
def api_random(request):
    joke = get_random_joke()
    if joke is None:
        return Response({'error': 'No jokes found'}, status=404)

    serializer = JokeSerializer(joke)
    return Response(serializer.data)


@api_view(['GET', 'POST'])
def api_jokes(request):
    if request.method == 'GET':
        jokes = Joke.objects.all().order_by('-timestamp')
        serializer = JokeSerializer(jokes, many=True)
        return Response(serializer.data)

    serializer = JokeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def api_joke_detail(request, pk):
    joke = get_object_or_404(Joke, pk=pk)
    serializer = JokeSerializer(joke)
    return Response(serializer.data)


@api_view(['GET'])
def api_pictures(request):
    pictures = Picture.objects.all().order_by('-timestamp')
    serializer = PictureSerializer(pictures, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def api_picture_detail(request, pk):
    picture = get_object_or_404(Picture, pk=pk)
    serializer = PictureSerializer(picture)
    return Response(serializer.data)


@api_view(['GET'])
def api_random_picture(request):
    picture = get_random_picture()
    if picture is None:
        return Response({'error': 'No pictures found'}, status=404)

    serializer = PictureSerializer(picture)
    return Response(serializer.data)