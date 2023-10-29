from django.shortcuts import render
from .form import ImageForm
from .models import Images
import pickle
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import requests
from bs4 import BeautifulSoup
import re

# Create your views here.

# Load the list from the file
with open("class_names.pkl", "rb") as file:
    class_names = pickle.load(file)
# Load the model
model = load_model("food_model2.h5")

def home(request):
    a = class_names
    return render(request,"homepage.html", {'list':a})

def main(request):
    if request.method == "POST":
        form=ImageForm(data=request.POST,files=request.FILES)
        if form.is_valid():
            form.save()
            obj=form.instance
            imgg = image.load_img("."+obj.image.url, target_size=(224, 224))
            x = image.img_to_array(imgg)
            x = np.expand_dims(x, axis=0)
            images = np.vstack([x])
            pred = model.predict(images, batch_size=32)
            prediction = class_names[np.argmax(pred)]
            try:
                url = 'https://www.google.com/search?&q=' + prediction + ' calories'
                req = requests.get(url).text
                scrap = BeautifulSoup(req, 'html.parser')
                calories_table = scrap.find("table")
                
                if calories_table:
                    calories = calories_table.text
                    a = calories.replace('%', '')
                    info = ''
                else:
                    a = ""
                    info = "Information is not available right now"

            except Exception as e:
                a = ""
                info = "Information is not available right now"

            # Define regular expressions to extract different information
            calories_regex = re.compile(r"১০০ gCalories \(kcal\) (\d+\.\d+)")
            lipid_regex = re.compile(r"মান\*লিপিড (\d+\.\d+)")
            carbohydrate_regex = re.compile(r"শর্করা (\d+)")
            protein_regex = re.compile(r"প্রোটিন (\d+\.\d+)")
            vitamin_c_regex = re.compile(r"ভিটামিন সি(\d+)")
            calcium_regex = re.compile(r"ক্যালসিয়াম(\d+)")
            iron_regex = re.compile(r"লোহা(\d+)")
            vitamin_d_regex = re.compile(r"ভিটামিন ডি(\d+)")
            magnesium_regex = re.compile(r"ম্যাগনেসিয়াম(\d+)")
            sodium_regex = re.compile(r"সোডিয়াম (\d+)")

            calories_match = calories_regex.search(a)
            lipid_match = lipid_regex.search(a)
            carbohydrate_match = carbohydrate_regex.search(a)
            protein_match = protein_regex.search(a)
            vitamin_c_match = vitamin_c_regex.search(a)
            calcium_match = calcium_regex.search(a)
            iron_match = iron_regex.search(a)
            vitamin_d_match = vitamin_d_regex.search(a) 
            magnesium_match = magnesium_regex.search(a)
            sodium_match = sodium_regex.search(a)

            calories = calories_match.group(1) if calories_match else "N/A"
            lipid = lipid_match.group(1) if lipid_match else "N/A"
            carbohydrate = carbohydrate_match.group(1) if carbohydrate_match else "N/A"
            protein = protein_match.group(1) if protein_match else "N/A"
            vitamin_c = vitamin_c_match.group(1) if vitamin_c_match else "N/A"
            calcium = calcium_match.group(1) if calcium_match else "N/A"
            iron = iron_match.group(1) if iron_match else "N/A"
            vitamin_d = vitamin_d_match.group(1) if vitamin_d_match else "N/A"
            magnesium = magnesium_match.group(1) if magnesium_match else "N/A"
            sodium = sodium_match.group(1) if sodium_match else "N/A"

            def bn2en_number(number):
                search_array = ["১", "২", "৩", "৪", "৫", "৬", "৭", "৮", "৯", "০"]
                replace_array = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
                en_number = number
                for i in range(len(search_array)):
                    en_number = en_number.replace(search_array[i], replace_array[i])

                return en_number

            context = {
                "info" : info,
                "obj":obj,
                "pred": class_names[np.argmax(pred)],
                "Calories": bn2en_number(calories),
                "Lipid" : bn2en_number(lipid),
                "carbohydrate" : bn2en_number(carbohydrate),
                "protein" : bn2en_number(protein),
                "vitamin_c": bn2en_number(vitamin_c),
                "calcium" : bn2en_number(calcium),
                "iron": bn2en_number(iron),
                "vitamin_d": bn2en_number(vitamin_d),
                "magnesium": bn2en_number(magnesium),
                "Sodium": bn2en_number(sodium),
            }
            return render(request,"main.html",context)
    else:
        form=ImageForm()
        img=Images.objects.all()
    return render(request,"main.html",{"img":img,"form":form})