from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Movie, MovieList, Genre
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
import re

@login_required(login_url='login')
def index(request):
    movies = Movie.objects.all()

    # Preprocess genres for modal display
    for movie in movies:
        movie.genre_list = ", ".join([g.name for g in movie.genres.all()])

    featured_movie = movies[len(movies) - 1]

    context = {
        'movies': movies,
        'featured_movie': featured_movie,
    }
    return render(request, 'index.html', context=context)


@login_required(login_url='login')
def my_list(request):
    movie_list = MovieList.objects.filter(owner_user=request.user)
    user_movie_list = []

    for movie_entry in movie_list:
        movie = movie_entry.movie
        # Preprocess genres
        movie.genre_list = ", ".join([g.name for g in movie.genres.all()])
        user_movie_list.append(movie)

    context = {
        'movies': user_movie_list
    }
    return render(request, 'my_list.html', context=context)


@login_required(login_url='login')
def genre(request, pk):
    genre_name = pk.capitalize()
    genre_obj = get_object_or_404(Genre, name__iexact=genre_name)

    movies = Movie.objects.filter(genres=genre_obj)

    # Preprocess genres
    for movie in movies:
        movie.genre_list = ", ".join([g.name for g in movie.genres.all()])

    context = {
        'movies': movies,
        'movie_genre': genre_obj.name,
    }
    return render(request, 'genre.html', context=context)


@login_required(login_url='login')
def search(request):
    if request.method == 'POST':
        search_term = request.POST['search_term']

        movies = Movie.objects.filter(
            Q(title__icontains=search_term) |
            Q(genres__name__icontains=search_term)
        ).distinct()

        # Preprocess genres
        for movie in movies:
            movie.genre_list = ", ".join([g.name for g in movie.genres.all()])

        context = {
            'movies': movies,
            'search_term': search_term,
        }
        return render(request, 'search.html', context=context)

    return redirect('/')


# API and other views remain the same
@login_required
def movies_api(request):
    movies = Movie.objects.all()
    data = [
        {
            "id": movie.id,
            "title": movie.title,
            "description": movie.description,
            "genres": [g.name for g in movie.genres.all()],
            "release_date": movie.release_date,
            "length": movie.length,
            "image_card_url": movie.image_card_url,
            "image_cover_url": movie.image_cover_url,
            "video_url": movie.video_url,
        }
        for movie in movies
    ]
    return JsonResponse(data, safe=False)


@login_required
def my_list_api(request):
    movie_list = MovieList.objects.filter(owner_user=request.user)
    uuids = [m.movie.uu_id for m in movie_list]
    return JsonResponse({"movie_uuids": uuids})


@login_required(login_url='login')
def watch(request, pk):
    movie_uuid = pk
    movie_details = Movie.objects.get(uu_id=movie_uuid)
    context = {'movie_details': movie_details}
    return render(request, 'watch.html', context)


@login_required(login_url='login')
def add_to_list(request):
    if request.method == 'POST':
        movie_url_id = request.POST.get('movie_id')
        uuid_pattern = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'
        match = re.search(uuid_pattern, movie_url_id)
        movie_id = match.group() if match else None

        movie = get_object_or_404(Movie, uu_id=movie_id)

        movie_entry = MovieList.objects.filter(owner_user=request.user, movie=movie).first()

        if movie_entry:
            movie_entry.delete()
            response_data = {'status': 'removed', 'message': 'Removed ❌'}
        else:
            MovieList.objects.create(owner_user=request.user, movie=movie)
            response_data = {'status': 'added', 'message': 'Added ✔'}

        return JsonResponse(response_data)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Invalid Credentials')
            return redirect('login')
    return render(request, 'login.html')


def signup(request):
    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Already Registered')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Already Exists')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)
                return redirect('/')
        else:
            messages.info(request, 'Incorrect Password')
            return redirect('signup')
    else:
        return render(request, 'signup.html')


@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('login')
