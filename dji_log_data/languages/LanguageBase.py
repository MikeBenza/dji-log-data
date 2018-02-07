from jinja2 import Environment, PackageLoader

from pkg_resources import resource_stream
import json


class Language(object):
    def __init__(self, frames_template, keys_template, environment_args, additional_filters):
        self._frames_template = frames_template
        self._keys_template = keys_template
        self._env = Environment(loader=PackageLoader('dji_log_data'), **environment_args)
        self._env.filters.update(additional_filters)

    def generate_frames(self, output_file):
        data = json.load(resource_stream('dji_log_data', 'data/frames.json'))
        template = self._env.get_template(self._frames_template)
        output_file.write(template.render(data=data))

    def generate_keys(self, output_file):
        data = json.load(resource_stream('dji_log_data', 'data/keys.json'))
        template = self._env.get_template(self._keys_template)
        output_file.write(template.render(keys=data))
