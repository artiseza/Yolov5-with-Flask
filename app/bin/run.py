from flask import Flask, request, render_template, send_file, jsonify
from werkzeug.utils import secure_filename, send_from_directory
import os
import subprocess
import numpy as np
from PIL import Image
import io
import cv2
import base64
import torch

template_dir = '../html/templates'
static_dir = '../html/static'
app = Flask(__name__, template_folder=template_dir, static_url_path='/static', static_folder=static_dir)
uploads_dir = './uploads/'
os.makedirs(uploads_dir, exist_ok=True)

# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/edah_api', methods=['POST'])
def run_edah_api():
    json_list = []
    if request.method == 'POST':
        if 'filename' not in request.files:
            json_list = [{'image': 'there is no filename in form!'}]
        image_file = request.files['filename']
        
        
        # img.save(image_path)

        image_bytes = image_file.read()
        img = Image.open(io.BytesIO(image_bytes))
        results = model(img, size=1280)  # reduce size=320 for faster inference
        res = results.pandas().xyxy[0].to_json(orient="records")
        print('JSON result---',res)

        image_path = os.path.join(uploads_dir,'detect/')
        # print('image_path: ',image_path)
        results.save(image_path)  # save to image_path

        pre_img = open('./uploads/detect/image0.jpg', 'rb') 
        img_string = base64.b64encode(pre_img.read())
        # base64 傳結果
    json_list = [{'image': img_string.decode('utf-8')}]
    return jsonify(json_list)

@app.route('/', methods=['GET'])
def run_app():
    return render_template('index.html')

if __name__ == "__main__":
    #app.run(debug=True, host='0.0.0.0', port=5555, ssl_context='adhoc')
    model = torch.hub.load('ultralytics/yolov5', 'custom', path='./weights/final.pt')  # default
    # model = torch.hub.load('./', 'custom', path='./weights/final.pt', source='local')  # local repo
    app.run(debug=True)
    # app.run(debug=True, host='0.0.0.0', port=15588, ssl_context=('/app/html/ssl/openaifab.com/fullchain3.pem', '/app/html/ssl/openaifab.com/privkey3.pem'))
