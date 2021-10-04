from flask import Flask, render_template, request, send_file, url_for, redirect
import base64
import os.path
import image_classification
from datetime import datetime
import json 

app = Flask(__name__)


classifier = image_classification.Classifier("./ai_models/model.h5")
classifier.load()

with open("./plant_data.json","r") as file:
    s = file.read()
    
plant_data = json.loads(s) 
 
@app.route("/")
def index():
    return render_template('index.html')


@app.route("/upload", methods=['GET', 'POST'])
def upload():
    with open("ip.log", "a") as f:
        f.write(request.remote_addr + "\n")
    if request.method == 'POST':
        base64image = request.form.get("imgBase64").split("data:image/webp;base64,")[1]
        base64bytes = base64image.encode("ascii")
        image = base64.b64decode(base64bytes)
        
        for i in range(0,1000):
            ip = str(request.remote_addr).replace(".", "-")
            if not os.path.isfile(f"uploads/{ip}_{i}.jpg"):
                with open(f"uploads/{ip}_{i}.jpg", "wb") as file:
                    file.write(image)

                p = classifier.predict(f"{ip}_{i}", f"/root/bwki/uploads/{ip}_{i}.jpg")
                
                return p
                
        return "max pics reached"    



@app.route("/pics/<index>")
def download(index):
    ip = str(request.remote_addr).replace(".", "-")
    image_name = f"{ip}_{index}"
    if index == 'x':
        for i in range(0,1000):
            image_name = f"{ip}_{i}"
            if not os.path.isfile(f"uploads/{image_name}.jpg"):
                image_name = f"{ip}_{i-1}"
                break
            
    p = classifier.predict(image_name, f"/root/bwki/uploads/{image_name}.jpg")
    print(p)
    return send_file(f"uploads/{image_name}.jpg")





def get_matching_plants(plant):
    lst = []
    if plant_data["data"].get(plant) == None:
        return lst
    for p in plant_data["data"].get(plant):
        if p[0] != '-':
            lst.append(p)
    print(lst)
    return lst
    
def get_bad_plants(plant):
    lst = []
    if plant_data["data"].get(plant) == None:
        return lst
    for p in plant_data["data"].get(plant):
        if p[0] == '-':
            lst.append(p.replace("-", ""))
    print(lst)
    return lst

@app.route("/gurke")
def gurke():
    bad_plants = get_bad_plants("gurke")
    good_plants = get_matching_plants("gurke")
    return render_template("gurke.html", good_plants=good_plants,bad_plants=bad_plants)

@app.route("/zucchini")
def zucchini():
    bad_plants = get_bad_plants("zucchini")
    good_plants = get_matching_plants("zucchini")
    return render_template("zucchini.html", good_plants=good_plants,bad_plants=bad_plants)

@app.route("/zuckererbse")
def zuckererbse():
    bad_plants = get_bad_plants("zuckererbse")
    good_plants = get_matching_plants("zuckererbse")
    return render_template("zuckererbse.html", good_plants=good_plants,bad_plants=bad_plants)

@app.route("/tomate")
def tomate():
    bad_plants = get_bad_plants("tomate")
    good_plants = get_matching_plants("tomate")
    return render_template("tomate.html", good_plants=good_plants,bad_plants=bad_plants)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=443, debug=False, ssl_context='adhoc')
