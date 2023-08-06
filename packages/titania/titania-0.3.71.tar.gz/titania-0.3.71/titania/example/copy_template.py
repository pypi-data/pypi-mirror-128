from pathlib import Path
import os

realpath = Path(os.path.dirname(os.path.realpath(__file__)))
template_path = realpath / '../template'

def main_file(project_name):
    with open(template_path/'main.py', 'r') as f:
        file_content = f.read()
    return file_content

def config_file(project_name):
    with open(template_path/'config.py', 'r') as f:
        file_content = f.read()
    return file_content

def thresholds_tab_file():
    with open(template_path/'views/thresholds_gui.py', 'r') as f:
        file_content = f.read()
    return file_content

def thresholds_file():
    with open(template_path/'views/thresholds.py', 'r') as f:
        file_content = f.read()
    return file_content

def control_panel_file():
    with open(template_path/'panels/control_panel.py', 'r') as f:
        file_content = f.read()
    return file_content
