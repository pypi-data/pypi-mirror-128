from SpiffWorkflow.bpmn.workflow import BpmnWorkflow
from SpiffWorkflow.camunda.parser.CamundaParser import CamundaParser
from SpiffWorkflow.camunda.specs.UserTask import EnumFormField, UserTask
import logging as log

log.basicConfig(level=log.INFO)
 


class Workflow():
    def __init__(self, *args, **kwargs):
        file, name, process, = args, kwargs
        self.workflow = BpmnWorkflow(name)
        self.parser = CamundaParser()
        self.spec = self.parser.get_spec(name)
        self.parser.add_bpmn_file(file)
        self.workflow.do_engine_steps()
        self.ready_tasks = self.workflow.get_ready_user_tasks()
        self.process = process
        self.main()

    # def show_form(self, task):

    #     form = task.task_spec.form

    #     if task.data is None:
    #         task.data = {}

    #     for field in form.fields:
    #         prompt = field.label
    #         if isinstance(field, EnumFormField):
    #             prompt += "? (Options: " + \
    #                 ', '.join([str(option.id)
    #                           for option in field.options]) + ")"
    #         prompt += "? "
    #         answer = input(prompt)
    #         if field.type == "long":
    #             answer = int(answer)
    #         task.update_data_var(field.id, answer)

    def main(self):
        while len(self.ready_tasks) > 0:
            for task in self.ready_tasks:
                if isinstance(task.task_spec, UserTask):
                    self.process(task)
                    log.info(task.data)
                else:
                    log.info("Complete Task ", task.task_spec.name)
                self.workflow.complete_task_from_id(task.id)
            self.workflow.do_engine_steps()
            self.ready_tasks = self.workflow.get_ready_user_tasks()
        log.info(self.workflow.last_task.data)
