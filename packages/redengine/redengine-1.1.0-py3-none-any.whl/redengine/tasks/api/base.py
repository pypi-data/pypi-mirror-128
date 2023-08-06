
from typing import List
from redengine.core import Task

class TaskCommand:

    def __init__(self, task_name):
        self.task_name = task_name

    @classmethod
    def from_dict(cls, d:dict):
        command = d.pop('command')
        cmd = {
            "delete": DeleteTask,
            "disable": DisableTask,
            "force_run": ForceRun,
        }[command]
        return cmd(**d)


class DeleteTask(TaskCommand):

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        del self.session[self.task_name]

class DisableTask(TaskCommand):

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        self.session[self.task_name].disabled = True

class ForceRun(TaskCommand):

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        self.session[self.task_name].force_run = True


class ParamCommand:
    pass

class DeleteParam(ParamCommand):

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        del self.session.parameters[self.param_name]

class AddParam(ParamCommand):

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        self.session.parameters[self.param_name] = self.value


class ConnectorTask(Task):

    def execute(self, *args, **kwargs):
        self.setup()

        while not self.thread_terminate.is_set():
            time.sleep(self.delay)
            self.inspect()

        self.teardown()

    def setup(self):
        return

    def inspect(self):
        return

    def teardown(self):
        return

    def get_info_tasks(self) -> List[dict]:
        "Get task info to display"
        for task in self.session.tasks:
            yield self.format_task(task)

    def get_info_session(self, tasks=None):
        "Get session info to display"
        session = self.session
        data = {
            "config": session.config,
            "parameters": session.parameters,
        }
        if tasks == "full":
            for task in session.tasks.values():
                data["tasks"].append(self.format_task(task))
        elif tasks == "count":
            data["tasks"] = len(session.tasks)
        elif tasks == "names":
            data["tasks"] = list(session.tasks.keys())
        return data

    def format_task(self, task):
        return {
            "name": task.name,
            "class": type(task),
            "start_cond": str(task.start_cond),
            "end_cond": str(task.end_cond),

            "execution": task.execution,
            "parameters": task.parameters,

            "disabled": task.disabled,
            "force_run": task.force_run,

            "status": task.status,
            "last_run": task.last_run,
            "last_success": task.last_success,
            "last_fail": task.last_fail,
            "last_inaction": task.last_inaction,
        }

    def create_task(self, data:dict):
        # data should be like:
        # {"name": "mytask", "code": ""}
        CodeTask(**data)

    def update_task(self, data:dict, task_name=None):
        if task_name is None:
            task_name = data["task_name"]
        task = self.session.get_task(task_name)
        with task.lock:
            for attr, value in data.items():
                setattr(task, attr, value)
            task.save() #! TODO (should save to disk)

    def delete_task(self, task_name):
        task = self.session.tasks.pop(task_name)
        task.delete()


class FileAPI(ConnectorTask):

    def inspect(self):
        file = Path(self.file)
        if file.is_file():
            cont = read_json(file)
        for command in cont:
            self.handle_command(command)

class FlaskTask(ConnectorTask):

    def __init__(self):
        self.app.add_endpoint("/session", endpoint="session", self.route_session)
        self.app.add_endpoint("/tasks", endpoint="tasks", self.route_tasks)
        self.app.add_endpoint("/logs", endpoint="session", self.route_logs)

    def route_session(self):
        return jsonify(self.get_info_session())

    def route_tasks(self):
        if request.method == "GET":
            return jsonify(self.get_info_tasks())
        elif request.method == "PATCH":
            data = request.get_json()
            self.update_task(data)

    def route_logs(self):
        return jsonify(self.get_info_logs())