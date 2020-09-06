from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint, jsonify)
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Post, User
from flaskblog.posts.forms import PostForm
from random import randint

posts = Blueprint('posts', __name__)


@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post')


@posts.route("/post/<int:post_id>")
@login_required
def post(post_id):
    post = Post.query.get_or_404(post_id)
    if current_user.username not in post.usernames.split(','):
        post.total_views += 1
        post.usernames += current_user.username + ','
    #post.current_views += 1
    current_user.current_url = "/post/" + str(post_id)
    db.session.commit()
    current_view = 100
    return render_template('post.html', title=post.title, post=post, total_views = post.total_views, current_views= current_view)


@posts.route("/update_views/<int:post_id>", methods=['POST'])
def update_views(post_id):
    current_views = db.session.query(User).filter(User.current_url=="/post/" + str(post_id)).count()
    return jsonify({'status': 'success', 'current_views': current_views})


@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))
