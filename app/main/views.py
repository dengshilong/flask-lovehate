import os

from flask import flash, app
from flask import render_template, request,\
    current_app
from flask import url_for
from flask_login import current_user
from werkzeug.utils import redirect

from app import db
from app.common import get_uuid_filename
from app.main.form import PostForm
from . import main
from ..models import Post, Category
from manage import app


@main.route('/', methods=['GET'])
def index():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.create_time.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    return render_template('index.html', posts=posts,
                           pagination=pagination)

@main.route('/add', methods=['GET', 'POST'])
def add():
    if current_user.is_anonymous:
        return redirect(url_for('auth.login'))
    form = PostForm()
    if form.validate_on_submit():
        f = form.photo.data
        filename = get_uuid_filename(f.filename)
        print(filename)
        f.save(os.path.join(app.config['STATIC_BASE_DIR'], filename))
        category = Category.query.filter_by(name=form.category.data).first()
        if not category:
            category = Category(name=form.category.data)
            db.session.add(category)
            db.session.commit()
        post = Post(photo=filename, author_id=current_user.id, category_id=category.id)
        db.session.add(post)
        flash('已记下')
        return redirect(url_for('main.index'))
    return render_template('main/add.html', form=form)
