import os.path

from flask import request, session, render_template, redirect, url_for

from webfiles import app
import webfiles.controllers as controllers
from webfiles.errors import InvalidSessionError
from webfiles.filters import *
from webfiles.forms import LoginForm

IGNORE = [
    'favicon.ico',
    ]


def render(template_name, **kwargs):
    """Injects calls to flask.render_template() with embellishments."""
    injections = {}
    kwargs.update(injections)
    return render_template(template_name, **kwargs)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    logform = LoginForm()

    if request.method == 'POST':
        logform = LoginForm(request.form)
        if logform.validate() and controllers.authenticate():
            return redirect(url_for('index'))
    # this happens if error in POST or any other request
    return render('login.html', form=logform)


@app.route('/logout/')
def logout():
    controllers.logout()
    return redirect(url_for('login'))


@app.route('/', defaults={'subdir': ''})
@app.route('/<path:subdir>/')
def index(subdir=''):
    """List files in settings.config.FILE_ROOT or an optional subdirectory."""
    if subdir in IGNORE:
        return ''

    try:
        entries = controllers.listdir(subdir)
    except InvalidSessionError as err:
        return logout()

    return render('filelist.html', entries=entries)


@app.route('/download')
def download():
    """Stream the given file if authenticated and permitted.

    The request args must include ?fp=<path_tail> which is the path to a
    file relative to settings.config.FILE_ROOT.

    The controller takes care of trapping user input problems.
    """
    try:
        path_tail = request.args.get('fp')
        return controllers.stream_file(path_tail)
    except InvalidSessionError as err:
        return logout()
    except Exception as err:
        return 'invalid request: %s' % (request.url)
