import io
from turtle import title

from flask import render_template, session, flash, request, redirect, url_for, send_file
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db
from app.email import send_password_reset_email
from app.forms import LoginForm, EditPostForm, RegistrationForm, EditProfileForm, PostForm, ResetPasswordRequestForm, \
    EmptyForm, ResetPasswordForm
from app.models import User, Post, Tag
from datetime import datetime, timezone


@app.route('/')
def root():
    return redirect(url_for('login'))


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(timezone.utc)
        db.session.commit()


def cleanup_unused_tags():
    # Query for tags not linked to any posts
    unused_tags = Tag.query.filter(Tag.posts == None).all()

    # Delete unused tags
    for unused_tag in unused_tags:
        db.session.delete(unused_tag)

    # Commit the changes to the database
    db.session.commit()


@app.route('/index')
@login_required
def index():
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    tags = Tag.query.all()
    cleanup_unused_tags()
    return render_template('index.html', title='Home', posts=posts, tags=tags)


@app.route('/login', methods=['GET', 'POST'])
def login():
    color = session.get('color', 'red')
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid Username or Password')
            color = session.pop('color', 'default')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('auth/login.html', title='Sign In', form=form, color=color)


@app.route('/signup', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Congratulations, you are now a registered user!")
        session['color'] = 'green'
        return redirect(url_for('login'))
    return render_template('auth/register.html', title='Register', form=form)


@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        print("Reset Password Requested for User:", user)
        if user:
            send_password_reset_email(user)
        else:
            flash("Email not found")
            return redirect(url_for('reset_password_request'))

        flash('Check your email for the instructions to reset your password.')
        return redirect(url_for('login'))
    return render_template('auth/reset.html', title="Reset Password", form=form, color='red')


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your Password has been reset.')
        return redirect(url_for('login'))
    return render_template('auth/reset_password.html', form=form)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


# Create a New Post
@app.route('/new_post', methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        tag = Tag.query.filter_by(name=form.tags.data).first() or Tag(name=form.tags.data)
        post = Post(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.post.data,
            user_id=current_user.id,
            image_data=form.image.data.read() if form.image.data else None,
            image_url=form.image_url.data if form.image_url.data else None,
            tag=tag
        )
        db.session.add(post)
        db.session.commit()

        return redirect(url_for('index'))
    return render_template('post/newPost.html', title='New Post', form=form)


@app.route('/display_image/<int:post_id>')
@login_required
def display_image(post_id):
    post = Post.query.filter_by(id=post_id).first()
    return send_file(io.BytesIO(post.image_data), mimetype='image/jpeg')


@app.route('/post/<int:post_id>')
@login_required
def post(post_id):
    post = Post.query.filter_by(id=post_id).first()
    return render_template('post/post.html', title=post.title, post=post)


@app.route('/user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def profile(user_id):
    form = EmptyForm()
    user = User.query.get_or_404(user_id)
    posts = Post.query.filter_by(user_id=user_id).order_by(Post.timestamp.desc()).all()
    editform = EditProfileForm(original_username='Bruno', about_me=user.about_me)
    if editform.validate_on_submit():
        user.username = editform.username.data
        user.about_me = editform.about_me.data
        db.session.commit()
        return redirect(url_for('profile', user_id=user_id))
    return render_template('profile/user.html', title="Profile", user=user, posts=posts, form=form, form2=editform)


@app.route('/follow/<user_id>', methods=['POST'])
@login_required
def follow(user_id):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(id=user_id).first()
        if user is None:
            return redirect(url_for('index'))
        if user == current_user:
            return redirect(url_for('profile', user_id=user_id))
        current_user.follow(user)
        db.session.commit()
        return redirect(url_for('profile', user_id=user_id))
    else:
        return redirect(url_for('index'))


@app.route('/unfollow/<user_id>', methods=['POST'])
@login_required
def unfollow(user_id):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(id=user_id).first()
        if user is None:
            return redirect(url_for('index'))
        if user == current_user:
            return redirect(url_for('profile', user_id=user_id))
        current_user.unfollow(user)
        db.session.commit()
        return redirect(url_for('profile', user_id=user_id))
    else:
        return redirect(url_for('index'))


@app.route("/tags/<tag_name>")
@login_required
def post_by_tags(tag_name):
    posts = Tag.query.filter_by(name=tag_name).first().posts

    posts_counts = len(posts)
    return render_template('post/post_by_tags.html', posts_counts=posts_counts, posts=posts,
                           title=f"posts with {tag_name}", tag_name=tag_name)


@app.route('/delete/<post_id>')
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/edit/<post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    form = EditPostForm(
        title=post.title,
        subtitle=post.subtitle,
        post=post.body,
        tags=post.tag.name
    )
    if form.validate_on_submit():
        post.title = form.title.data
        post.subtitle = form.subtitle.data
        post.body = form.post.data
        post.tag = Tag.query.filter_by(name=form.tags.data).first() or Tag(name=form.tags.data)
        if form.image.data is None:
            pass
        else:
            post.image = form.image.data.read()

        if form.image_url.data is None:
            pass
        else:
            post.image_url = form.image_url.data
        db.session.commit()
        cleanup_unused_tags()
        return redirect(url_for('post', post_id=post_id))
    return render_template('post/editPost.html', title='Edit Post', form=form)
