from django.shortcuts import render
from django.http import JsonResponse

from django.core import serializers
from django.views.decorators.http import require_http_methods
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from tensorflow import keras
import numpy as np


from base64 import decodestring
from PIL import Image
import io
# Create your views here.

list_all=["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"," ","",""]
model = keras.models.load_model('model/my_model.h5')

@require_http_methods(["POST"])
def submitImage(request):
    response = {}
    try:
        image_data = request.FILES.get('img')
        if image_data != None:
            img_base64 = b""

            for chunks in image_data.chunks():
                img_base64 += chunks

            image = decodestring(img_base64)
            img = Image.open(io.BytesIO(image))
            res = predict_img(img)
            response['data'] = res
            response['sucess'] = True
        else:
            response['data'] = '0'
            response['sucess'] = True
    except Exception as inst:
        response['data'] = inst.args
        response['sucess'] = False
    
    return JsonResponse(response)

def predict_img(img : Image):
    img = img.crop((0,0,128,128))
    img = img.convert("L")
    img = img.resize((64, 64), Image.ANTIALIAS)
    img.save("./test.jpg")
    data = np.asarray(img)
    data = np.reshape(data,(64,64,1))
    data = data/255.0
    data = np.array([data])

    res = model.predict(data)
    return list_all[np.argmax(res)]


