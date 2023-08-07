from flask import Flask, render_template, url_for, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:a4131619k@localhost/flask'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flask.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

migrate = Migrate(app, db)


# app.config['DATABASE'] = {
#     'dbname': 'flask',
#     'user': 'admin',
#     'password': 'a4131619k',
#     'host': 'localhost',
#     'port': '5432'
# }
#
#
# def connect_db():
#     return psycopg2.connect(
#         dbname=app.config['DATABASE']['dbname'],
#         user=app.config['DATABASE']['user'],
#         password=app.config['DATABASE']['password'],
#         host=app.config['DATABASE']['host'],
#         port=app.config['DATABASE']['port']
#     )


class Article(db.Model):
    __tablename__='article'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    time = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Article %r' % self.id


class AdditionalArticle(db.Model):
    __tablename__='addarticle'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    article = db.Column(db.Integer, db.ForeignKey('article.id'))


@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/posts')
def posts():
    articles = Article.query.order_by(Article.time.desc()).all()
    return render_template('posts.html', articles=articles)


@app.route('/posts/<int:id>')
def posts_detail(id):
    article = Article.query.get(id)
    return render_template('post_detail.html', article=article)


@app.route('/posts/<int:id>/del')
def posts_delete(id):
    article = Article.query.get_or_404(id)

    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/posts')
    except:
        return 'При удалении статьи произошла ошибка'


@app.route('/posts/<int:id>/update', methods=['POST', 'GET'])
def posts_update(id):
    article = Article.query.get(id)
    if request.method == 'POST':
        article.title = request.form['title']
        article.intro = request.form['intro']
        article.text = request.form['text']

        try:
            db.session.commit()
            return redirect('/posts')
        except:
            return 'При редактировании статьи произошла ошибка'
    else:
        return render_template('post_update.html', article=article)


@app.route('/create-article', methods=['POST', 'GET'])
def create_article():
    if request.method == 'POST':
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        article = Article(title=title, intro=intro, text=text)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/posts')
        except:
            return 'При добавлении статьи произошла ошибка'
    else:
        return render_template('create_article.html')


if __name__ == '__main__':
    app.run(debug=True)

