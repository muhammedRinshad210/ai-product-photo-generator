from django.shortcuts import render
from PIL import Image, ImageEnhance
import os

# Create your views here.

def index(request):
    image_url = None

    if request.method == "POST":
        file = request.FILES.get('image')
        filter_type = request.POST.get('filter')

        # ✅ CREATE FOLDER IF NOT EXISTS
        os.makedirs("media", exist_ok=True)

        # if new image uploaded
        if file:
            path = "media/original.jpg"
            image = Image.open(file)
            image.save(path)
        else:
            path = "media/original.jpg"
            if not os.path.exists(path):
                return render(request, "index.html")
            image = Image.open(path)

        # apply filter
        if filter_type == "bw":
            image = image.convert('L')

        elif filter_type == "enhance":
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(2)

        elif filter_type == "warm":
            r, g, b = image.split()
            r = r.point(lambda i: i * 1.2)
            image = Image.merge('RGB', (r, g, b))

        # save output
        output_path = "media/output.jpg"
        image.save(output_path)

        image_url = "/media/output.jpg"


        # # save original image
        # image = Image.open(file)

        # # convert to balck and white
        # bw_image = image.convert('L')   #👉 🔥 MAIN LINE #👉 Converts image → Black & White

        # # ✅ CREATE FOLDER IF NOT EXISTS
        # os.makedirs("media", exist_ok=True)

        # # save new image
        # path = "media/output.jpg"
        # bw_image.save(path)

        # image_url = path
        

    return render(request, "index.html" , {'image_url' : image_url})