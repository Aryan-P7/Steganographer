from flask import Flask, request, jsonify
import base64
from steg import ImageSteg
from ImageStegano import Steganography
import Emoji
import os
from flask_cors import CORS
import mimetypes
from PIL import Image
import io

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads' 
img = ImageSteg()
CORS(app)


if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/encode', methods=['POST'])
def encode():
    if 'image' not in request.files:
        return jsonify({'status': 'error', 'message': 'No image file part'})
    file = request.files['image']
    if file.filename == '':
        return jsonify({'status': 'error', 'message': 'No selected file'})
    if file:
        imgname = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(imgname)
        msg = request.form['msg']
        
        strbytes = msg.encode("ascii")
        base64_bytes = base64.b64encode(strbytes)
        base64_str = base64_bytes.decode("ascii")
        
        try:
            encrypted_image_path = img.encrypt_text_in_image(imgname, base64_str)
            
            mime_type, _ = mimetypes.guess_type(encrypted_image_path)
            if not mime_type:
                mime_type = 'application/octet-stream' 

            with open(encrypted_image_path, "rb") as image_file:
                encoded_bytes = base64.b64encode(image_file.read())
                encoded_string = encoded_bytes.decode('ascii')
            
            data_uri = f"data:{mime_type};base64,{encoded_string}"
            
            return jsonify({'status': 'success', 'encrypted_image': data_uri})
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)})


@app.route('/decode', methods=['POST'])
def decode():
    if 'image' not in request.files:
        return jsonify({'status': 'error', 'message': 'No image file part'})
    file = request.files['image']
    if file.filename == '':
        return jsonify({'status': 'error', 'message': 'No selected file'})
    if file:
        dimg = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(dimg)
        
        try:
            res = img.decrypt_text_in_image(dimg)
            base64_bytes = res.encode("ascii")
            base64_dec = base64.b64decode(base64_bytes)
            dec_text = base64_dec.decode("ascii")
            return jsonify({'status': 'success', 'message': dec_text})
        except Exception as e:
            return jsonify({'status': 'error', 'message': 'ERROR: No message found in uploaded file'})



@app.route('/merge', methods=['POST'])
def merge():
    if 'image1' not in request.files or 'image2' not in request.files:
        return jsonify({'status': 'error', 'message': 'Both images must be provided'})

    image1_file = request.files['image1']
    image2_file = request.files['image2']

    image1 = Image.open(image1_file)
    image2 = Image.open(image2_file)

    try:
        merged_image = Steganography().merge(image1, image2)
        
        img_byte_arr = io.BytesIO()
        merged_image.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        encoded_image = base64.b64encode(img_byte_arr).decode('ascii')
        
        return jsonify({'status': 'success', 'encrypted_image': f"data:image/png;base64,{encoded_image}"})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})


@app.route('/unmerge', methods=['POST'])
def unmerge():
    if 'image' not in request.files:
        return jsonify({'status': 'error', 'message': 'Image file must be provided'})

    image_file = request.files['image']
    image = Image.open(image_file)

    try:
        unmerged_image = Steganography().unmerge(image)
        
        img_byte_arr = io.BytesIO()
        unmerged_image.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        encoded_image = base64.b64encode(img_byte_arr).decode('ascii')
        
        return jsonify({'status': 'success', 'unmerged_image': f"data:image/png;base64,{encoded_image}"})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/emoji-encode', methods=['POST'])
def emoji_encode():
    msg = request.form['msg']
    encoded_text = Emoji.encode_text(msg)
    return jsonify({'status': 'success', 'encoded_text':encoded_text })

@app.route('/emoji-decode', methods=['POST'])
def emoji_decode():
    msg = request.form['msg']
    decoded_text = Emoji.decode_text(msg)
    return jsonify({'status': 'success', 'decoded_text':decoded_text })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
