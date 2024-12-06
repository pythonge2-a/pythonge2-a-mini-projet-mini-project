from django.shortcuts import render, redirect
from django.http import HttpResponse
from manim_project.utils.generate_video import generate_manim_video  

# Page d'accueil
def home(request):
    return render(request, 'manim_project/home.html')

# Page d'édition
def edit_code(request):
    if request.method == 'POST':
        code = request.POST.get('code', '')
        # TODO: Ajouter la logique pour traiter et générer une vidéo avec Manim


        return HttpResponse("Le code a été soumis avec succès !")
    return render(request, 'manim_project/edit.html')


def generate_video_view(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        generate_manim_video(code)
        return redirect('result')  # Redirige vers une page de succès ou une autre page
    return render(request, 'manim_project/edit.html')


def result(request):
    return render(request, 'manim_project/result.html')