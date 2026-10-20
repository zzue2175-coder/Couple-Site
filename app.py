from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import yt_dlp
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
    url = data.get('url')
    
    try:
           ydl_opts = {
            'format': 'best', 
            'quiet': True,
            'extractor_args': {
                'youtube': {
                    'player_client': ['ios', 'web']
                }
            }
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            video_url = info.get('url')
            title = info.get('title', 'Video')
        return jsonify({'success': True, 'video_url': video_url, 'title': title})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
