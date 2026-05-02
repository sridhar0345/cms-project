import uuid
import logging
from flask import render_template, session, request, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user, login_required
from urllib.parse import urlparse as url_parse
from FlaskWebProject import app, db
from FlaskWebProject.forms import PostForm as EditForm, LoginForm
from FlaskWebProject.models import User, Post
import msal

logger = logging.getLogger(__name__)

@app.route('/')
@app.route('/home')
@login_required
def index():
    post_list = Post.query.all()
    return render_template('index.html', title='Home', posts=post_list)

@app.route('/new_post', methods=['GET', 'POST'])
@login_required
def new_post():
    form = EditForm()
    if form.validate_on_submit():
        post = Post()
        file = request.files.get('image_path')
        post.save_changes(form, file, current_user.id, new=True)
        return redirect(url_for('index'))
    return render_template('edit.html', title='Create Post', form=form, post=None)

@app.route('/post/<int:id>', methods=['GET', 'POST'])
@login_required
def post(id):
    post = Post.query.get(id)
    form = EditForm()
    if form.validate_on_submit():
        file = request.files.get('image_path')
        post.save_changes(form, file, current_user.id)
        return redirect(url_for('post', id=post.id))
    return render_template('edit.html', title='Edit Post', form=form, post=post)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            logger.warning('Invalid login attempt for user: %s', form.username.data)
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        logger.info('User %s logged in successfully', user.username)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    session["state"] = str(uuid.uuid4())
    auth_url = _build_auth_url(scopes=[], state=session["state"])
    return render_template('login.html', title='Sign In', form=form, auth_url=auth_url)

@app.route('/getAToken')
def authorized():
    if request.args.get('state') != session.get("state"):
        return redirect(url_for("index"))
    if "error" in request.args:
        return render_template("auth_error.html", result=request.args)
    if request.args.get('code'):
        cache = _load_cache()
        result = _build_msal_app(cache=cache).acquire_token_by_authorization_code(
            request.args['code'],
            scopes=[],
            redirect_uri=url_for('authorized', _external=True)
        )
        if "error" in result:
            return render_template("auth_error.html", result=result)
        session["user"] = result.get("id_token_claims")
        _save_cache(cache)
        user = User.query.filter_by(username='admin').first()
        login_user(user)
        logger.info('Admin logged in successfully via Microsoft')
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('login'))

def _load_cache():
    cache = msal.SerializableTokenCache()
    if session.get("token_cache"):
        cache.deserialize(session["token_cache"])
    return cache

def _save_cache(cache):
    if cache.has_state_changed:
        session["token_cache"] = cache.serialize()

def _build_msal_app(cache=None):
    return msal.ConfidentialClientApplication(
        app.config['CLIENT_ID'],
        authority="https://login.microsoftonline.com/common",
        client_credential=app.config['CLIENT_SECRET'],
        token_cache=cache
    )

def _build_auth_url(scopes=None, state=None):
    return _build_msal_app().initiate_auth_code_flow(
        scopes or [],
        redirect_uri=url_for('authorized', _external=True),
        state=state
    )['auth_uri']