class Workflow:
    def __init__(self, project_module, update, context):
        self.project_module = project_module
        self.update = update
        self.context = context
        self.project_name = self.context.args[:1][0]
        self.project_arguments = self.context.args[1:]
        self.starter = self.update.effective_user.name

    def run(self):
        return self.project_module.ci_build(self.update, self.context)

    def get_info(self):
        return (f"{self.project_name}\n"
                f"Arguments: {' '.join(self.project_arguments)}\n"
			    f"Started by: {self.starter}\n")
