import os

def generate_manim_video(code):
    # save script in a temp file
    with open('temp.py', 'w') as f:
        f.write(code)

    # generate the video with manim
    os.system("manim -qh temp.py output")

    # delete temp file
    os.system("rm temp.py")

    return True


