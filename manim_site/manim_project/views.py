from django.shortcuts import render
from django.http import HttpResponse

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
