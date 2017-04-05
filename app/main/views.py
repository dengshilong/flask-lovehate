import os

from flask import flash, abort
from flask import render_template, request,\
    current_app
from flask import url_for
from flask_login import current_user
from flask_login import login_required
from werkzeug.utils import redirect

from app import db
from app.common import get_uuid_filename, get_default_category, generate_thumbnail
from app.main.form import PostForm, EditProfileForm, CommentForm
from manage import APP
from . import main
from ..models import Post, Category, User, Comment


@main.route('/', methods=['GET'])
def index():
    APP.logger.info("index")
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
        f.save(os.path.join(current_app.config[
               'STATIC_BASE_DIR'], current_app.config['UPLOAD_DIR'], filename))
        generate_thumbnail(filename)
        if form.category.data:
            category = Category.query.filter_by(
                name=form.category.data).first()
            if not category:
                category = Category(name=form.category.data.strip())
                db.session.add(category)
                db.session.commit()
        else:
            category = get_default_category()
        post = Post(photo=filename, author_id=current_user.id,
                    category_id=category.id)
        db.session.add(post)
        flash('已记下')
        return redirect(url_for('main.index'))
    return render_template('main/add.html', form=form)


@main.route('/category/<category>', methods=['GET', ])
def category(category):
    page = request.args.get('page', 1, type=int)
    category = Category.query.filter_by(name=category).first_or_404()
    pagination = Post.query.filter_by(category_id=category.id).order_by(Post.create_time.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    return render_template('index.html', posts=posts,
                           pagination=pagination)


@main.route('/item/<int:id>', methods=['GET', 'POST'])  # pylint: disable=redefined-builtin
def post(id):  # pylint: disable=redefined-builtin
    post = Post.query.get_or_404(id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(body=form.body.data, post=post,
                          author=current_user._get_current_object())  # pylint: disable=protected-access
        db.session.add(comment)
        flash('评论已提交')
        return redirect(url_for('.post', id=post.id, page=-1))
    page = request.args.get('page', 1, type=int)
    if page == -1:
        page = (post.comments.count() - 1) / \
            current_app.config['FLASKY_COMMENTS_PER_PAGE'] + 1
    pagination = post.comments.filter_by(disabled=False).order_by(Comment.create_time.asc()).paginate(
        page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],
        error_out=False)
    comments = pagination.items
    return render_template('post.html', posts=[post], form=form,
                           comments=comments, pagination=pagination)


@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.filter_by(author_id=user.id).order_by(Post.create_time.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    return render_template('user.html', user=user, posts=posts, pagination=pagination)


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        flash('个人资料已更新')
        return redirect(url_for('.user', username=current_user.username))
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)


@main.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('无效的用户')
        return redirect(url_for('.index'))
    if current_user.is_following(user):
        flash('你已经关注该用户')
        return redirect(url_for('.user', username=username))
    current_user.follow(user)
    flash('你现在关注了 %s.' % username)
    return redirect(url_for('.user', username=username))


@main.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('无效的用户')
        return redirect(url_for('.index'))
    if not current_user.is_following(user):
        flash('你未关注该用户')
        return redirect(url_for('.user', username=username))
    current_user.unfollow(user)
    flash('你取消关注 %s.' % username)
    return redirect(url_for('.user', username=username))


@main.route('/followers/<username>')
def followers(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('无效的用户')
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followers.paginate(
        page, per_page=current_app.config['FLASKY_FOLLOWERS_PER_PAGE'],
        error_out=False)
    follows = [{'user': item.follower, 'create_time': item.create_time}
               for item in pagination.items]
    return render_template('followers.html', user=user, title="关注我的人",
                           endpoint='.followers', pagination=pagination,
                           follows=follows)


@main.route('/followed_by/<username>')
def followed_by(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('无效的用户')
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followed.paginate(
        page, per_page=current_app.config['FLASKY_FOLLOWERS_PER_PAGE'],
        error_out=False)
    follows = [{'user': item.followed, 'create_time': item.create_time}
               for item in pagination.items]
    return render_template('followers.html', user=user, title="我关注的人",
                           endpoint='.followed_by', pagination=pagination,
                           follows=follows)


@main.route('/modify_photo')
def modify_photo():
    """add thumbnail to post"""
    posts = Post.query.all()
    for post in posts:
        filename = post.photo
        print(filename)
        if post.photo.startswith(current_app.config['UPLOAD_DIR']):
            filename = '/'.join(post.photo.split('/')[1:])
            post.photo = filename
            db.session.add(post)
            db.session.commit()
        print(filename)
        generate_thumbnail(filename)
    abort(404)


@main.route('/comments')
def comments():
    page = request.args.get('page', 1, type=int)
    if current_user.is_administrator:
        comments = Comment.query.order_by(Comment.create_time.desc())
    else:
        comments = Comment.query.filter_by(
            disabled=False).order_by(Comment.create_time.desc())
    pagination = comments.paginate(page,
                                   per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'], error_out=False)
    comments = pagination.items
    return render_template('comments.html', comments=comments, pagination=pagination, page=page,
                           is_administrator=current_user.is_administrator)


@main.route('/moderate/enable/<int:id>')
@login_required
def moderate_enable(id):  # pylint: disable=redefined-builtin
    comment = Comment.query.get_or_404(id)
    comment.disabled = False
    db.session.add(comment)
    return redirect(url_for('.comments', page=request.args.get('page', 1, type=int)))


@main.route('/moderate/disable/<int:id>')
@login_required
def moderate_disable(id):  # pylint: disable=redefined-builtin
    comment = Comment.query.get_or_404(id)
    comment.disabled = True
    db.session.add(comment)
    return redirect(url_for('.comments', page=request.args.get('page', 1, type=int)))
