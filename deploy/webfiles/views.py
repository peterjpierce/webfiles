import os.path

from flask import request, session, render_template

from webfiles import app
import webfiles.controller as controller
from webfiles.filters import *

IGNORE = [
    'favicon.ico',
    ]


def render(template_name, **kwargs):
    """Injects calls to flask.render_template() with embellishments."""
    injections = {}
    kwargs.update(injections)
    return render_template(template_name, **kwargs)


@app.route('/', defaults={'subdir': ''})
@app.route('/<path:subdir>')
def index(subdir=''):
    """List files in settings.config.FILE_ROOT or an optional subdirectory."""
    if subdir in IGNORE:
        return ''
    # TODO implement authentication
    session['catalog'] = 'group1'

    entries = controller.listdir(subdir)
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
        return controller.stream_file(path_tail)
    except Exception as err:
        return 'invalid request: %s' % (request.url)
