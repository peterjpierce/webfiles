import flask

from app import app
import app.controller as controller
from app.filters import *


def render_template(template_name, **kwargs):
    """Injects calls to flask.render_template() with embellishments."""
    injections = {}
    kwargs.update(injections)
    return flask.render_template(template_name, **kwargs)


@app.route('/', defaults={'subdir': ''})
@app.route('/<path:subdir>')
def index(subdir=''):
    """List files in config.FILE_ROOT or an optional subdirectory."""
    entries = controller.listdir(subdir)
    return render_template('filelist.html', entries=entries)


@app.route('/download')
def download():
    """Stream the given file if authenticated and permitted.

    The request args must include ?fp=<path_tail> which is the path to a
    file relative to config.FILE_ROOT.

    The controller takes care of trapping user input problems.
    """
    try:
        path_tail = flask.request.args.get('fp')
        return controller.stream_file(path_tail)
    except Exception as err:
        return 'invalid request: %s' % flask.request.url
