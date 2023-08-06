from .consts import *


class Task:
    def __init__(self, task_type, question, callback, unique_id):
        self.task_type = task_type
        self.callback = callback
        self.question = question
        self.unique_id = unique_id

    def to_dic(self):
        dic = {
            'task-type': self.task_type,
            'callback': self.callback,
        }
        if self.unique_id:
            dic.update({'_id': self.unique_id})
        return dic

    def set_id(self, unique_id):
        self.unique_id = unique_id


class Text_Tagging(Task):

    def __init__(self, text, question, all_tags, callback=None, unique_id=None):
        super(Text_Tagging, self).__init__(TEXT_TAGGING_TYPE, question, callback, unique_id)
        self.text = text
        self.all_tags = all_tags

    def to_dic(self):
        dic = super(Text_Tagging, self).to_dic()
        dic.update(
            {
                'data': {'text': self.text},
                'meta-label': {
                    'all-tags': self.all_tags,
                    'question': self.question
                }
            })
        return dic
