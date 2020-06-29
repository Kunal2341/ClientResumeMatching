import os
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from flask import send_from_directory

UPLOAD_FOLDER = '/Users/kunal/Documents/ResumeNLPVdart/flaskWebsite/uploadedFiles/'
ALLOWED_EXTENSIONS = {'pdf'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':  # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file'] # if user does not select file, browser also submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            global fileDIRECTORY
            fileDIRECTORY = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            return render_template('uploadFile.html', fileDir = fileDIRECTORY)
            #return redirect(url_for('uploaded_file',
            #                        filename=filename))
    return render_template('uploadFile.html', fileDir = "INVALID")

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

from werkzeug.middleware.shared_data import SharedDataMiddleware
app.add_url_rule('/uploads/<filename>', 'uploaded_file',
                 build_only=True)
app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
    '/uploads':  app.config['UPLOAD_FOLDER']
})
#------------------------------------------------------------
@app.route('/')
def index():
    return render_template('index.html', fileDIRECTORY="n/a")

@app.route('/home', methods = ['POST'])
def home():
    return render_template('index.html', fileDIRECTORY = fileDIRECTORY)
@app.route('/runCode', methods = ['POST'])
def runCode():
    print("x")

if __name__ == '__main__':
    app.secret_key = 'resume'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.debug = True
    app.run()
