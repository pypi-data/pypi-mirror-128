from typing import IO
# Dict, Generator, Generic, List, TypeVar, Union
from .Api import Api
import secrets
from .env import *
from .Task import Task


class Client:
    def __init__(self,
                 api_key):
        self.api = Api(api_key=api_key, api_instance_url=LABELER_BASE_URL)

    def create_project(self, project):
        return self.api.post_request('create-project', body=project.to_dic())

    def get_all_projects(self):
        return self.api.get_request('all-projects')

    def get_project(self, project_name):
        return self.api.get_request('project', headers={'project_name': project_name})

    def cancel_task(self, project_name, task_id):
        return self.api.delete_request('task',
                                       headers={'project_name': project_name},
                                       params={'task_id': task_id})

    def get_task(self, project_name, task_id):
        return self.api.get_request('task',
                                    headers={'project_name': project_name},
                                    params={'task_id': task_id})

    def get_all_tasks(self, project_name, status):
        return self.api.get_request('tasks',
                                    headers={'project_name': project_name},
                                    params={'status': status})

    def get_tasks_count(self, project_name, status):
        return self.api.get_request('tasks-count',
                                    headers={'project_name': project_name},
                                    params={'status': status})

    def create_task(self,
                    project_name: str,
                    task: Task):
        if task.unique_id is None:
            task.set_id(secrets.token_hex(8))
        return self.api.post_request('create-task',
                                     headers={'project_name': project_name},
                                     body=task.to_dic())

    def all_labelers(self, project_name):
        return self.api.get_request('all-labelers', headers={'project_name': project_name})

    def add_labelers(self, project_name, emails):
        return self.api.post_request('add-labelers', headers={'project_name': project_name},
                                     body={"emails": emails})

    def cancel_labeler(self, project_name, email):
        return self.api.delete_request('cancel-labeler', headers={'project_name': project_name},
                                       params={"email": email})

    def import_file(self,
                    project_name: str,
                    file_url: str):
        body = {
            'file_url': file_url
        }
        return self.api.post_request('import-file',
                                     headers={'project_name': project_name}, body=body)

    def upload_file(self, project_name: str, file: IO):
        files = {"file": file}
        return self.api.post_request('upload-file',
                                     files=files,
                                     headers={'project_name': project_name})
