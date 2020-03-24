from flask import Flask, render_template, redirect, request, url_for, flash
from forms import CardDataForm
import os
import pathlib
import sys
import uuid
from generate_card import runAlg

app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['UPLOAD_FOLDER'] = str(pathlib.Path(__file__).parent.absolute() / "upload")
app.config['RESULTS_FOLDER'] = str(pathlib.Path(__file__).parent.absolute() / "static" / "images" / "results")


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/admin/')
def admin():
    return render_template('admin.html')

#---------------------MAIN SITE-----------------------
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signin/')
def signin():
    return render_template('signin.html')

@app.route('/signup/')
def signup():
    return render_template('signup.html')

@app.route('/prices/')
def prices():
    return render_template('prices.html')

@app.route('/about/')
def about():
    return render_template('about.html')

@app.route('/contacts/')
def contacts():
    return render_template('contacts.html')

@app.route('/basket/')
def basket():
    return render_template('basket.html')

#-----------------------CATEGORIES--------------------
@app.route('/categories/auto/')
def category_auto():
    return render_template('auto.html')

@app.route('/categories/estate/')
def category_estate():
    return render_template('estate.html')

@app.route('/categories/education/')
def category_education():
    return render_template('education.html')

@app.route('/categories/art/')
def category_art():
    return render_template('art.html')

@app.route('/categories/sport/')
def category_sport():
    return render_template('sport.html')

@app.route('/categories/shopping/')
def category_shopping():
    return render_template('shopping.html')

#-----------------------DASHBOARD---------------------
@app.route('/dashboard/')
@app.route('/dashboard/info/')
def dashboard_info():
    return render_template('dashboard_info.html')

@app.route('/dashboard/editor/', methods=['GET', 'POST'])
def dashboard_editor():
    # Создать форму для ввода данных
    form = CardDataForm()
    if form.validate_on_submit():
        # Сохранить загруженный файл с уникальным идентификатором
        if 'logoFile' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = form.logoFile.data
        logoPath = os.path.join(app.config['UPLOAD_FOLDER'], uuid.uuid4().hex + '.png')
        file.save(logoPath)
        # Передать данные алгоритму
        resultName = uuid.uuid4().hex + '.png'
        resultPath = os.path.join(app.config['RESULTS_FOLDER'], resultName)
        mainText = form.personName.data
        tagline = form.companyName.data
        siteAddress = form.url.data
        phone = form.phone.data
        mail = form.email.data
        runAlg(mainText, tagline, siteAddress, phone, mail, logoPath, resultPath)
        # Результат алгоритма передать для отображения
        return redirect(url_for('.dashboard_result', image=resultName))
    return render_template('dashboard_editor.html', form=form)

@app.route('/dashboard/editor/results/<image>/')
def dashboard_result(image):
    imageSrc = "/static/images/results/" + image
    return render_template('dashboard_result.html', image=imageSrc)


