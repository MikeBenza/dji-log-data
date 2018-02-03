{% if not base_class %}{%- set base_class = 'Frame' -%}{% endif %}
{% if not extra_args %}{%- set extra_args = [] -%}{% endif %}
{% macro unpack_value(field, subfield) -%}
(self.raw_fields['{{ field.name }}'] & {{ subfield.bits | bit_mask }}) >> {{ subfield.bits | bit_shift}}
{%- endmacro %}
{% macro optionally_apply_transformation(value, field) -%}
    {%- if field.transformation -%}
        {{ value | apply_transformation(field.transformation) }}
    {%- else -%}
        {{ value }}
    {%- endif -%}
{%- endmacro %}
{%- macro enumify(v, field) -%}
    {%- if field.type == "enum" %} \
            default_enum_value({{frame_data.type}}.{{ field.enum_name | pascal_case }}, {{ v }})
    {%- else -%}
        {{v}}
    {%- endif -%}
{%- endmacro -%}

class {{frame_data.type}}({{ base_class }}):
    frame_type = FrameType.{{frame_data.type}}

    {% if frame_data.enums %}
    {% for (name, enum) in frame_data.enums.items() %}
    class {{ name | pascal_case }}(Enum):
        {% for enum_value in enum['values'] %}
        {{ enum_value.name }} = {{ enum_value.value }}
        {% endfor %}
        {% if enum.default %}
        _default = {{ enum.default }}
        {% else %}
        UNRECOGNIZED = -1
        _default = UNRECOGNIZED
        {% endif %}

    {% endfor %}
    {% else %}

    {% endif %}
    def __init__(self, body, version{% for arg in extra_args %}, {{arg}}{% endfor %}):
        super({{frame_data.type}}, self).__init__(body, version)
        {% for arg in  extra_args %}
        self.{{arg}} = {{arg}}
        {% endfor %}

        self.raw_fields = {}
        self.fields = {}

        self.unpack_fields()
        self.load_fields()

    def unpack_fields(self):
        {% if frame_data.field_definitions %}
        {# TODO: Support different versions #}
        data = struct.unpack_from("<{% for field in frame_data.field_definitions[0].fields %}{{ field.format | format_to_struct_type }}{% endfor %}", self.body, 0)

        {% for field in frame_data.field_definitions[0].fields %}
        {% if field.unknown %}
        # Ignore field {{ loop.index0 }} because it's unknown
        {% else %}
        self.raw_fields['{{ field.name }}'] = data[{{ loop.index0 }}]
        {% endif %}
        {% endfor %}
        {% elif frame_data.string_frame %}
        self.raw_fields['message'] = struct.unpack_from("%ss" % len(self.body), self.body, 0)
        {% endif %}

    def load_fields(self):
        {% if frame_data.field_definitions %}
        {# TODO: Support different versions #}
        {% for field in frame_data.field_definitions[0].fields %}
        {% if not field.unknown-%}
        {% if field.packed %}
        self.fields['{{ field.name }}'] = {}
        {% for subfield in field.subfields %}
        self.fields['{{ field.name }}']['{{ subfield.name }}'] = {{ enumify(optionally_apply_transformation(unpack_value(field, subfield), subfield), subfield) }}
        {% endfor %}
        {% else %}
        self.fields['{{ field.name }}'] = {{ enumify(optionally_apply_transformation(("self.raw_fields['" ~ field.name ~ "']"), field), field) }}
        {% endif %}
        {% endif %}
        {% endfor %}
        {% elif frame_data.string_frame %}
        self.fields['message'] = self.raw_fields['message']
        {% endif %}
