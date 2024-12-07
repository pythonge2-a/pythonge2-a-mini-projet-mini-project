from django.shortcuts import render, redirect
from django.http import HttpResponse
from manim_project.utils.generate_video import generate_manim_video 
from os.path import join
from django.conf import settings


script_path = join("", "manim_script_1.py")


# Home
def home(request):
    return render(request, 'manim_project/home.html')


# Script edition
def edit_code(request):
    if request.method == 'POST':
        code = request.POST.get('code', '')
        # TODO: Ajouter la logique pour traiter et générer une vidéo avec Manim

        return HttpResponse("Le code a été soumis avec succès !")
    return render(request, 'manim_project/edit.html')


# Pre-coded script 
def generate_pre_coded_video(request):
    if request.method == 'POST':
        try:
            # Get the script name from the form
            script_name = request.POST.get('script_name')
            
            if not script_name:
                raise ValueError("Le nom du script n'est pas spécifié.")

            # Construct the path to the script
            script_path = join(settings.MEDIA_ROOT, "pre_coded", script_name)
            
            with open(script_path, 'r') as file:
                script_content = file.read()

            generate_manim_video(script_content)
            return redirect('result')
        except Exception as e:
            print(f"Erreur : {e}")
            return render(request, 'manim_project/pre_coded.html', {'error': str(e)})
    return render(request, 'manim_project/pre_coded.html')


# Video generation
def generate_video_view(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        generate_manim_video(code)
        return redirect('result')  # Redirige vers une page de succès ou une autre page
    return render(request, 'manim_project/edit.html')


# Result 
def result(request):
    return render(request, 'manim_project/result.html')