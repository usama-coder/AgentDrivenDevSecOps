import subprocess

def list_directory(directory):

    command = f"ls {directory}"
    subprocess.run(command, shell=True)


from jinja2 import Template

def render_template(template_string, context):

    template = Template(template_string)
    return template.render(context)


class MyClass:
    def method_a(self):
        print("Method A")

    def method_b(self):
        print("Method B")

def call_method(obj, method_name):

    method = getattr(obj, method_name)
    method()
