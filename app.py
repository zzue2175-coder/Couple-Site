from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import requests
import os

app = Flask(__name__)
app.secret_key = 'couple_secret_key_123'
PASSWORD = '169023'

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form.get('password') == PASSWORD:
            session['authenticated'] = True
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='စကားဝှက် မှားယွင်းနေပါတယ်!')
    return render_template('login.html')

@app.route('/home')
def index():
    if not session.get('authenticated'):
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/extract', methods=['POST'])
def extract():
    if not session.get('authenticated'):
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.get_json()
    url = data.get('url', '')
    
    try:
        # Cobalt API ကို အသုံးပြု၍ Video Link ရယူခြင်း
        api_url = "https://api.cobalt.tools/api/json"
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        payload = {"url": url}
        
        response = requests.post(api_url, json=payload, headers=headers)
        res_data = response.json()
        
        if res_data.get('status') == 'stream' or res_data.get('status') == 'redirect':
            video_url = res_data.get('url')
            return jsonify({'success': True, 'video_url': video_url, 'title': 'Download Video'})
        elif res_data.get('status') == 'picker':
            video_url = res_data['picker'][0]['url']
            return jsonify({'success': True, 'video_url': video_url, 'title': 'Download Video'})
        else:
            error_msg = res_data.get('text', 'Video မတွေ့ရှိပါ သို့မဟုတ် Download ဆွဲ၍ မရပါ')
            return jsonify({'success': False, 'error': error_msg})
            
    except Exception as e:
        return jsonify({'success': False, 'error': 'လိုင်းမကောင်းပါ သို့မဟုတ် ခေတ္တ အဆင်မပြေပါ'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
