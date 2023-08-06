import argparse
from .property import Property
from .type_utils import str2bool
import sys
from .dataset import Dataset
from .model import Model
from .translation_dictionary import translation
import json
import copy
from .generator import generate_meta_model
import re


class ArgumentParser():
    def __init__(self, name, description, docker_image=None):
        self.parser = argparse.ArgumentParser()
        self.properties = []
        self.input_datasets = []
        self.output_datasets = []
        self.input_models = []
        self.output_models = []
        self.description = description
        self.name = name.lower().replace(" ", "-")

        if docker_image is not None:
            self.docker_image = self.set_docker_image(docker_image)
        else:
            self.docker_image = docker_image


    def add_argument(self, argument, 
                        help="Please fill argument description and upload again your service", 
                        type=str, 
                        default=None,
                        required=False, 
                        action=None):


        if action is not None:
            if action == 'store_true':
                type = str2bool
                default = False
            elif action == 'store_false':
                type = str2bool
                default = True
            else:
                print("The action: " + action + " is not currently supported")

        self.properties.append(Property(argument, type=type, help=help, default=default, required=required))
        self.parser.add_argument(argument, help=help, type=type, default=None, required=required)


    def add_input_dataset(self, help=None, columns_type=None):
        self.parser.add_argument("--input_dataset", help=help, required=True, type=str)
        self.input_datasets.append(Dataset(description=help, columns_type=columns_type))

    def add_output_dataset(self, help=None):
        self.parser.add_argument("--output_dataset", help=help, required=True, type=str)
        self.output_datasets.append(Dataset(description=help))

    def add_input_model(self, help=None):
        self.parser.add_argument("--input_model", help=help, required=True, type=str)
        self.input_models.append(Model(description=help))
    
    def add_output_model(self, help=None):
        self.parser.add_argument("--output_model", help=help, required=True, type=str)
        self.output_models.append(Model(description=help))



    def parse_known_args(self):
        args = sys.argv[1:]

        # Standard python boolean args do not work as in Alida. 
        # Hence, we need to convert boolean args properly.

        alida_compliant_args = []

        # Whenever a --arg_name is found, it is replace with --arg_name=<its-default-value>
        for arg in args:
            if len(arg.split("="))>1:
                alida_compliant_args.append(arg)
            else:
                default_value = self.get_property_default_value(arg.replace("-", ""))
                if default_value is True:
                    alida_compliant_args.append(arg + "=" + "false")
                else:
                    alida_compliant_args.append(arg + "=" + "true")
        
        # If a boolean is not prensent at all in args, add it with its default value
        missing_bool_args = self.find_missing_bool_args(alida_compliant_args)
        for arg in missing_bool_args:
            alida_compliant_args.append(arg + "=" + str(self.get_property_default_value(arg.replace("-", ""))))

        return self.parser.parse_known_args(args=alida_compliant_args)


    def get_property_default_value(self, property_name):
        for property in self.properties:
            if property.name == property_name:
                return property.default


    # Find missing boolean arguments
    def find_missing_bool_args(self, args):
        missing_args = []
        for property in self.properties:
            if property.type is str2bool:
                if "--" + property.name + "=false" not in args and "--" + property.name + "=true" not in args and "--" + property.name + "=False" not in args and "--" + property.name + "=True" not in args :
                    missing_args.append("--" + property.name)
        return missing_args


    def generate_json(self, path):
        
        json_data = generate_meta_model(name = self.name, description=self.description, 
                                        properties = self.properties, 
                                        input_datasets=self.input_datasets,
                                        output_datasets = self.output_datasets,
                                        input_models = self.input_models,
                                        output_models = self.output_models,
                                        docker_image=self.docker_image
                                        )

        with open(path, "w") as outputFile:
            json.dump(json.loads(clean_json(json_data)), outputFile, indent=4)    #, sort_keys=True)


    def set_docker_image(self, docker_image):
        self.docker_image = "docker://" + docker_image

def clean_json(string):
    string = re.sub(",[ \t\r\n]+}", "}", string)
    string = re.sub(",[ \t\r\n]+\]", "]", string)

    return string