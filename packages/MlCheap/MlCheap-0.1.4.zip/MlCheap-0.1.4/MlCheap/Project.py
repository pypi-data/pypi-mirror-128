class Project:
    def __init__(self, name, labels_per_task):
        self.name = name
        self.labels_per_task = labels_per_task

    def to_dic(self):
        return {"project_name": self.name, "labels_per_task": self.labels_per_task}
