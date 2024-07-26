import pycamunda.processdef
import pycamunda.externaltask
import requests.auth
import requests.sessions
import logging

class WorkflowEngine:
    def __init__(self, base_url: str, username: str = None, password: str = None):
        self.base_url = base_url
        self.session = requests.sessions.Session()
        if username and password:
            self.session.auth = requests.auth.HTTPBasicAuth(username, password)
        self.logger = self.setup_logger()

    def setup_logger(self):
        logger = logging.getLogger("WorkflowEngine")
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def deploy_bpmn(self, bpmn_file: str) -> bool:
        self.logger.info(f"Deploying BPMN file: {bpmn_file}")
        try:
            deploy = pycamunda.processdef.Deploy(url=self.base_url, file=bpmn_file)
            deploy.session = self.session
            deploy()
            self.logger.info("BPMN file deployed successfully.")
            return True
        except Exception as e:
            self.logger.error(f"Failed to deploy BPMN file: {e}")
            return False

    def start_process(self, process_key: str, variables: dict = None) -> bool:
        self.logger.info(f"Starting process with key: {process_key}")
        try:
            start_instance = pycamunda.processdef.StartInstance(url=self.base_url, key=process_key)
            if variables:
                for name, value in variables.items():
                    start_instance.add_variable(name=name, value=value)
            start_instance.session = self.session
            start_instance()
            self.logger.info("Process started successfully.")
            return True
        except Exception as e:
            self.logger.error(f"Failed to start process: {e}")
            return False

    def complete_task(self, task_id: str, variables: dict = None) -> bool:
        self.logger.info(f"Completing task with ID: {task_id}")
        try:
            complete = pycamunda.externaltask.Complete(url=self.base_url, id_=task_id)
            if variables:
                for name, value in variables.items():
                    complete.add_variable(name=name, value=value)
            complete.session = self.session
            complete()
            self.logger.info("Task completed successfully.")
            return True
        except Exception as e:
            self.logger.error(f"Failed to complete task: {e}")
            return False

    def get_process_instance_status(self):
        self.logger.info("Fetching process instance status.")
        try:
            get_instances = pycamunda.processinst.GetList(url=self.base_url)
            get_instances.session = self.session
            instances = get_instances()
            self.logger.info("Process instance status retrieved successfully.")
            return instances
        except Exception as e:
            self.logger.error(f"Failed to fetch process instance status: {e}")
            return None
