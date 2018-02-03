from jinja2 import Environment, FileSystemLoader

import json


class Language(object):
    def __init__(self, frames_file, keys_file, frames_template, keys_template, template_directory, environment_args, additional_filters):
        self._frames_file = frames_file
        self._keys_file = keys_file
        self._frames_template = frames_template
        self._keys_template = keys_template
        self._env = Environment(loader=FileSystemLoader(template_directory), **environment_args)
        self._env.filters.update(additional_filters)

    def generate_frames(self, output_file):
        data = json.load(open(self._frames_file))
        template = self._env.get_template(self._frames_template)
        output_file.write(template.render(data=data))

    def generate_keys(self, output_file):
        data = json.load(open(self._keys_file))
        template = self._env.get_template(self._keys_template)
        output_file.write(template.render(keys=data))
