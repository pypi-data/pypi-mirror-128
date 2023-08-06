from re import template
from jinja2 import Template, defaults
import jinja2
import json
from .translation_dictionary import translation
import os

# Load jinja template
def get_template(path):
    templateLoader = jinja2.FileSystemLoader(searchpath=os.path.dirname(os.path.realpath(__file__)))
    templateEnv = jinja2.Environment(loader=templateLoader)
    return templateEnv.get_template(path)



def generate_meta_model(name, description, properties, input_datasets, output_datasets, input_models, output_models, docker_image, json=json):
    
    template = get_template("template.py")

    outputText = template.render(name=name, description=description, properties=properties, json=json, translation=translation, 
                                input_datasets=input_datasets, output_datasets=output_datasets,
                                input_models=input_models, output_models=output_models,
                                docker_image=docker_image
                                )

    return outputText

