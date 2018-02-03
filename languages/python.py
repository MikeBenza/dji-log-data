import os

from . import Language

class Python(Language):

    _transformations = {
        'bool': 'bool({0})',
        'degrees': 'math.degrees({0})',
        'divide_by': '{0} / {1}',
        'divide_then_modulo': '({0} / {1}) % 360',
        'equals_0': '{0} == 0',
        'neq_0': '{0} != 0',
        'utc_milliseconds': 'datetime.datetime.utcfromtimestamp({0}/1000.0)'
    }

    _struct_types = {
        'Double': 'd',
        'Single': 'f',
        'U8':     'B',
        'U16':    'H',
        'U32':    'L',
        'U64':    'Q',
        'S8':     'b',
        'S16':    'h',
        'S32':    'l',
        'S64':    'q'
    }

    def __init__(self, frames_file, keys_file, template_directory):
        filters = {
            'format_to_struct_type': self.format_to_struct_type,
            'apply_transformation': self.apply_transformation,
            'bit_mask': self.bit_mask,
            'bit_shift': self.bit_shift,
            'pascal_case': self.pascal_case,
        }
        super(Python, self).__init__(
            frames_file=frames_file,
            keys_file=keys_file,
            frames_template='frames.py',
            keys_template='keys.py',
            template_directory=os.path.join(template_directory, 'python'),
            environment_args={'lstrip_blocks': True, 'trim_blocks': True},
            additional_filters=filters)

    @staticmethod
    def format_to_struct_type(format):
        if isinstance(format, dict):
            if format['type'] == 'String':
                return "{0}s".format(format['length'])
            else:
                raise Exception("Unrecognized format: %s" % format)
        return Python._struct_types[format]

    @staticmethod
    def apply_transformation(t, transformation):
        if not isinstance(transformation, dict):
            transformation_name = transformation
            values = []
        else:
            transformation_name = transformation['name']
            values = transformation['values']
        return Python._transformations[transformation_name].format(t, *values)

    @staticmethod
    def bit_mask(bits):
        if isinstance(bits, int):
            bits = {'start': bits, 'end': bits}
        return '0x{:02X}'.format(sum([1 << b for b in range(bits['start'], bits['end'] + 1)]))

    @staticmethod
    def bit_shift(bits):
        if isinstance(bits, int):
            bits = {'start': bits, 'end': bits}
        return bits['start']

    @staticmethod
    def pascal_case(s):
        return s.replace('_', ' ').title().replace(' ', '')
