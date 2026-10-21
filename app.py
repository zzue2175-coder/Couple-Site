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
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'})
        
        url = data.get('url', '')
        if not url:
            return jsonify({'success': False, 'error': 'လင့်ခ် ထည့်ရန် လိုအပ်ပါသည်။'})
        
        api_url = "https://api.cobalt.tools/api/json"
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        payload = {"url": url}
        
        response = requests.post(api_url, json=payload, headers=headers, timeout=15)
        res_data = response.json()
        
        status = res_data.get('status')
        if status in ['stream', 'redirect']:
            return jsonify({'success': True, 'video_url': res_data.get('url'), 'title': 'Download Video'})
        elif status == 'picker':
            picker = res_data.get('picker')
            if picker and len(picker) > 0:
                return jsonify({'success': True, 'video_url': picker[0].get('url'), 'title': 'Download Video'})
        
        error_msg = res_data.get('text', 'ဗီဒီယို လင့်ခ် ထုတ်ယူ၍ မရပါ။')
        return jsonify({'success': False, 'error': error_msg})
            
    except Exception as e:
        return jsonify({'success': False, 'error': 'ဆာဗာ ချိတ်ဆက်မှု အဆင်မပြေပါ။'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
