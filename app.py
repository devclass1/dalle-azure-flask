import os
import openai
from flask import Flask, request, render_template, send_from_directory

app = Flask(__name__)

# Configure Azure AI Foundry
AZURE_ENDPOINT = os.environ.get("AZURE_ENDPOINT", "")
AZURE_KEY = os.environ.get("AZURE_KEY", "")
DEPLOYMENT_NAME = os.environ.get("DEPLOYMENT_NAME", "")
API_VERSION = os.environ.get("API_VERSION", "2023-06-01-preview")

# Configure OpenAI to use Azure
openai.api_type = "azure"
openai.api_base = AZURE_ENDPOINT
openai.api_version = API_VERSION
openai.api_key = AZURE_KEY

UPLOAD_FOLDER = 'static/images'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        prompt = request.form['prompt']
        size = request.form.get('size', '1024x1024')
        quality = request.form.get('quality', 'standard')
        style = request.form.get('style', 'vivid')
        
        try:
            response = openai.Image.create(
                prompt=prompt,
                size=size,
                quality=quality,
                style=style,
                n=1,
                deployment_id=DEPLOYMENT_NAME
            )
            image_url = response['data'][0]['url']
            return render_template('index.html', image_url=image_url, prompt=prompt)
        
        except Exception as e:
            return render_template('index.html', error=str(e))
    
    return render_template('index.html')

@app.route('/static/images/<filename>')
def serve_image(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
