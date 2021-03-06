from flask import Flask, request, render_template, send_file, jsonify
import os
import cv2
import base64
import torch
from preproce import Preprocessing

template_dir = '../html/templates'
static_dir = '../html/static'
app = Flask(__name__, template_folder=template_dir, static_url_path='/static', static_folder=static_dir)
uploads_dir = './uploads/'
os.makedirs(uploads_dir, exist_ok=True)

model = torch.hub.load('ultralytics/yolov5', 'custom', path='./weights/final.pt')  # load weight model
@app.route('/edah_api', methods=['POST'])
def run_edah_api():
    json_list = []
    if request.method == 'POST':
        if 'filename' not in request.files:
            json_list = [{'image': 'there is no filename in form!'}]
        image_file = request.files['filename']
        predict_img = Preprocessing(image_file,image_file.filename) # Preprocessing      
        results = model(predict_img, size=1280) # inference with size = 1280
        # res = results.pandas().xyxy[0].to_json(orient="records")
        # print('JSON result---',res)
        image_path = os.path.join(uploads_dir,'detect/')
        results.save(image_path)  # save result IMG to image_path
        pre_img = open('./uploads/detect/image0.jpg', 'rb') 
        img_string = base64.b64encode(pre_img.read())
    json_list = [{'image': img_string.decode('utf-8')}] # to base64 
    return jsonify(json_list)

@app.route('/', methods=['GET'])
def run_app():
    return render_template('index.html')

if __name__ == "__main__":
    #app.run(debug=True, host='0.0.0.0', port=5555, ssl_context='adhoc')
    app.run(debug=True)
