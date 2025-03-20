import tkinter as tk
from tkinter import filedialog
from json import load, dump

import os

with open("settings.json") as settings:
    SETTINGS = load(settings)

directory = ""

class Command:
    def __init__(self, data : dict):
        self.type = data["type"]
        if self.type in SETTINGS["command_group_types"]:
            self.subcommands = data["data"]["commands"]
            
        elif self.type == "path":
            self.path_name = data["data"]["pathName"]

def open_dir_dialog():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askdirectory(title="Open the deploy directory of your WPILib project")
    return file_path

def open_file_dialog():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfile(defaultextension=".auto",title="Open the auto you want to flip")
    return file_path

def get_commands(data:dict):
    if data["type"] in SETTINGS["command_group_types"]:
        for command in data["data"]["commands"]:
            command_ = Command(command)
            if command_.type == 'path':
                flipped_path_name = get_path(command_.path_name)
                command['data']['pathName'] = flipped_path_name
            
            else:
                command = get_commands(command)

    return data

def get_path(path_name:str):
    global directory
    path_name_lower = path_name.lower()
    if "left" in path_name_lower:
        path_data = {}
        with open(directory+"\\pathplanner\\paths\\"+path_name+".path") as file:
            data = load(file)
            path_data = data
            
        path_name.replace("left", "right")
        path_name = path_name.replace("Left", "Right")
        with open(directory+"\\pathplanner\\paths\\"+path_name+".path", "w") as file:
            for waypoint in path_data["waypoints"]:
                anchor = waypoint["anchor"]
                in_heading = waypoint.get('prevControl')
                if in_heading:
                    in_heading['y'] = SETTINGS["field_width"]-in_heading['y']

                out_heading = waypoint.get('nextControl')
                if out_heading:
                    out_heading['y'] = SETTINGS["field_width"]-out_heading['y']

                anchor["y"] = SETTINGS["field_width"]-anchor["y"]
                if waypoint["linkedName"]:
                    waypoint["linkedName"] = None

            path_data["idealStartingState"]["rotation"] = -path_data["idealStartingState"]["rotation"]
            path_data["goalEndState"]["rotation"] = -path_data["goalEndState"]["rotation"]

            print(path_data)
            dump(path_data, file)
            
        return path_name
    elif "right" in path_name_lower:
        path_data = {}
        with open(directory+"\\pathplanner\\paths\\"+path_name+".path") as file:
            data = load(file)
            path_data = data
            
        path_name = path_name.replace("right", "left")
        path_name = path_name.replace("Right", "Left")
        with open(directory+"\\pathplanner\\paths\\"+path_name+".path", "w") as file:
            for waypoint in path_data["waypoints"]:
                anchor = waypoint["anchor"]
                in_heading = waypoint.get('prevControl')
                if in_heading:
                    in_heading['y'] = SETTINGS["field_width"]-in_heading['y']

                out_heading = waypoint.get('nextControl')
                if out_heading:
                    out_heading['y'] = SETTINGS["field_width"]-out_heading['y']

                anchor["y"] = SETTINGS["field_width"]-anchor["y"]
                if waypoint["linkedName"]:
                    waypoint["linkedName"] = None

            path_data["idealStartingState"]["rotation"] = -path_data["idealStartingState"]["rotation"]
            path_data["goalEndState"]["rotation"] = -path_data["goalEndState"]["rotation"]

            print(path_data)
            dump(path_data, file)
            
        return path_name

dir_path = open_dir_dialog()

if dir_path:
    directory = dir_path
    file = open_file_dialog()
    if file:
        data = load(file)
        data["command"] = get_commands(data["command"])
        if "right" in file.name.lower():
            auto_name = file.name.replace("Right", "Left").replace("right", "left")
        elif "left" in file.name.lower():
            auto_name = file.name.replace("Left", "Right").replace("left", "right")
        print(auto_name)
        with open(auto_name, "w") as auto:
            dump(data, auto)
    