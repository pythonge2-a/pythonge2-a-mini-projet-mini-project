import os

def generate_manim_video(code):
    # sauvegarder le code dans un fichier temporaire
    with open('temp.py', 'w') as f:
        f.write(code)
    
    # générer la vidéo avec Manim
    os.system("manim -pqh temp.py output")

    # supprimer le fichier temporaire
    os.system("rm temp.py")

    return True


