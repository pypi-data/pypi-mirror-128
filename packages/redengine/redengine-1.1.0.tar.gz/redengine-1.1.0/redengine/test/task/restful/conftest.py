
from threading import Thread

import pytest

from redengine import Scheduler
from redengine.conditions import ParamExists

@pytest.fixture
def scheduler(tmpdir, session):
    with tmpdir.as_cwd() as old_dir:
        #orig_cwd = os.getcwd()
        #tmpdir.chdir()

        #session.parameters["shutdown"] = False
        sched = Scheduler(shut_cond=ParamExists(shutdown=True))
        thread = Thread(target=sched)
        thread.start()
        yield sched

        session.parameters["shutdown"] = True
        thread.join()
        #os.chdir(orig_cwd)

@pytest.fixture
def api_port(tmpdir, session):
    pytest.importorskip("flask")
    return 12700

@pytest.fixture
def api_task(api_port, session):
    pytest.importorskip("flask")
    from redengine.tasks.api.http import HTTPConnection

    session.config["http_api_host"] = '127.0.0.1'
    session.config["http_api_port"] = api_port # Just a random port
    return HTTPConnection(force_run=True)

@pytest.fixture
def client(tmpdir, api_task):
    pytest.importorskip("flask")

    app = api_task.create_app()
    #db_fd, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True
    #orig_cwd = os.getcwd()
    #tmpdir.chdir()
    with tmpdir.as_cwd() as old_cwd:
        with app.test_client() as client:
            #with app.app_context():
            #    myapp.init_db()
            yield client
    #os.chdir(orig_cwd)
    #os.close(db_fd)
    #os.unlink(flaskr.app.config['DATABASE'])
