import functools
import logging
import sys
import uuid
from datetime import datetime
from enum import Enum
from typing import Any, NamedTuple, Optional, Tuple

from ...basic.error import utils as common_err
from ...basic.data.datatuple import DataTuple
from ...basic.validation import input

import celery
from celery import Celery


class CeleryConfig(NamedTuple):
    MAIN: str
    RESULT_BACKEND: str
    BROKER_URL: str
    IMPORTS: Tuple[str, ...]


class RobertCeleryProgressType:
    percent = 'percent'
    count = 'count'
    text = 'text'


class TaskStatus(Enum):
    PENDING = 'PENDING'
    RUNNING = 'RUNNING'
    SUCCESS = 'SUCCESS'
    FAILURE = 'FAILURE'
    CANCELLED = 'CANCELLED'
    INITIAL = 'INITIAL'
    ARCHIVED = 'ARCHIVED'


class RobertCeleryState(NamedTuple):
    status: TaskStatus
    error: Optional[Exception] = None
    progress: Any = None
    progress_type: Optional[str] = None
    result: Any = None


class Task(DataTuple):
    task_id: str
    progress: Optional[float]
    task_module: str
    status: TaskStatus
    args: Optional[dict]
    result: Optional[dict]
    error: Optional[str]
    operator_id: Optional[int]
    start_time: Optional[datetime]
    end_time: Optional[datetime]


class Colls:
    Task = 'Task'


class TaskLog:
    def __init__(self, mg_cfg: MongoAccessor):
        self.mg_cfg = mg_cfg

    def upsert_task(self, task: Task):
        doc = task.to_bson()
        self.mg_cfg.update_many(Colls.Task, {'task_id': task.task_id},
                                {'$set': doc},
                                upsert=True)
        return

    def create_task(self, task_id: str, module_name: str, operator_id: int,
                    params: dict):
        self.upsert_task(
            Task(task_id=task_id,
                 progress=0,
                 task_module=module_name,
                 status=TaskStatus.PENDING,
                 operator_id=operator_id,
                 args=params,
                 start_time=datetime.utcnow()))
        return

    def query_task(self,
                   task: Task,
                   page_num: Optional[int] = None,
                   page_size: Optional[int] = None):
        query = task.to_bson()
        if page_num and page_size:
            skip = (page_num - 1) * page_size
            limit = page_size
        else:
            skip = None
            limit = None
        rv = list(
            self.mg_cfg.find(Colls.Task,
                             query,
                             skip=skip,
                             limit=limit,
                             sort=[('_id', -1)]))
        return rv

    def init_task_class(self):
        task_log = self

        class RobertTask(celery.Task):
            def __init__(self, *args, **kwargs):
                self.task_log = task_log
                super().__init__(*args, **kwargs)

            def on_success(self, retval, task_id, args, kwargs):
                self.task_log.upsert_task(
                    Task(task_id=task_id,
                         status=TaskStatus.SUCCESS,
                         progress=1,
                         result=retval,
                         end_time=datetime.utcnow()))

            def on_failure(self, exc, task_id, args, kwargs, einfo):
                self.task_log.upsert_task(
                    Task(task_id=task_id,
                         status=TaskStatus.FAILURE,
                         progress=1,
                         error=einfo,
                         end_time=datetime.utcnow()))

        return RobertTask


class RobertCelery:
    def __init__(self, cfg: CeleryConfig, task_log: Optional[TaskLog] = None):
        cfg = input.assert_not_none_of('cfg', cfg, CeleryConfig)
        self.instance = Celery(main=cfg.MAIN,
                               backend=cfg.RESULT_BACKEND,
                               broker=cfg.BROKER_URL,
                               imports=cfg.IMPORTS)
        self.task_log = task_log

    def launch_by_name(self, module_name: str, task_name: str,
                       **kwargs) -> str:
        module_name = input.ensure_not_none_str('module_name', module_name)
        task_name = input.ensure_not_none_str('task_name', task_name)

        try:
            module = sys.modules.get(module_name)
            if module is None:
                raise common_err.InternalDataError(f'Invalid module name:{module_name}')
            task_func = getattr(module, task_name)
        except AttributeError:
            raise common_err.InternalDataError(
                f'No task named {task_name} in {module_name}')
        if not task_func:
            raise common_err.InternalDataError(
                f'No task named {task_name} in {module_name}')
        uid = str(uuid.uuid4()).replace('-', '')
        task_id = f"{module_name}-{task_name}-{uid}"
        if self.task_log:
            operator_id = kwargs.get('operator_id')
            full_module_name = f'{module_name}.{task_name}'
            self.task_log.create_task(task_id=task_id,
                                    module_name=full_module_name,
                                    operator_id=operator_id,
                                    params=kwargs)
        logging.info(f"Launching task {task_id}...")
        task_func.apply_async(kwargs=kwargs, task_id=task_id)
        return task_id

    def get_task_state(self, task_id: str) -> RobertCeleryState:
        ar = self.instance.AsyncResult(task_id)
        rv = None

        max_retry = 10
        for i in range(max_retry):
            state = ar.state
            try:
                state = TaskStatus(state)
            except ValueError:
                raise NotImplementedError(f"Invalid state: {state}")
            if state == TaskStatus.RUNNING:
                try:
                    rv = RobertCeleryState(
                        status=TaskStatus.RUNNING,
                        progress=ar.result.get('progress'),
                        progress_type=ar.result.get('progress_type'))
                except AttributeError:
                    # In extreme cases, ar.state changes from "RUNNING" to "SUCCESS" just after we check ar.state.
                    # Then ar.result will raise an error because ar.result is updated to the task result
                    # instead of the task progress object at this time.
                    logging.warning(
                        f"Inconsistent celery AsyncResult: {state}:{ar.state}:{ar.result}"
                    )
            elif state == TaskStatus.SUCCESS:
                rv = RobertCeleryState(status=state, result=ar.result)
            elif state == TaskStatus.FAILURE:
                rv = RobertCeleryState(status=state, error=ar.info)
            elif state in {
                    TaskStatus.PENDING, TaskStatus.CANCELLED,
                    TaskStatus.INITIAL
            }:
                rv = RobertCeleryState(status=state)
            else:
                raise RuntimeError()
            if rv is not None:
                break
            if i < max_retry - 1:
                logging.warning(f"Failed to get the task state. Retry!")

        if rv is None:
            raise common_err.InternalError(
                f"Failed to get the task state after all retries!")

        return rv

    def update_progress(self, progress_type: RobertCeleryProgressType,
                        progress: Any):
        task = self.instance.current_worker_task
        task.update_state(state=TaskStatus.RUNNING.value,
                          meta=dict(progress=progress,
                                    progress_type=progress_type))

    @staticmethod
    def task_wrapper(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            code = '1'
            msg = ''
            success = True
            try:
                data = func(*args, **kwargs)
            except common_err.RobertError as e:
                success = False
                details = e.args[0]
                code = details.get('code', common_err.E_INTERNAL)
                msg = details.get('msg', '')
                data = details.get('data', None)
                logging.error(
                    f'raise RobertError with code={code}, msg={msg}, data={data}'
                )
            except Exception as e:
                success = False
                code = common_err.E_INTERNAL
                msg = str(e)
                data = None
                logging.error(str(e), exc_info=True)
            if isinstance(data, common_err.RobertResponse):
                return {
                    'success': True,
                    'code': data.code,
                    'msg': data.msg,
                    'data': data.data
                }
            else:
                return {
                    'code': code,
                    'msg': msg,
                    'data': data,
                    'success': success
                }

        return wrapper
