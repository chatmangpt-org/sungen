import yaml
import xml.etree.ElementTree as ET
import typer
from workflow_engine import WorkflowEngine  # Assuming this is the correct import for the workflow engine

app = typer.Typer()

def convert_yaml_to_xml(yaml_file: str, xml_file: str):
    with open(yaml_file, 'r') as yf:
        data = yaml.safe_load(yf)

    definitions = ET.Element('definitions', {
        'xmlns': "http://www.omg.org/spec/BPMN/20100524/MODEL",
        'xmlns:xsi': "http://www.w3.org/2001/XMLSchema-instance",
        'id': "Definitions_1",
        'targetNamespace': "http://www.bpmn.org/schema/bpmn"
    })

    process = ET.SubElement(definitions, 'process', {
        'id': data['morning_routine']['start_event']['id'],
        'isExecutable': "false"
    })

    start_event = ET.SubElement(process, 'startEvent', {
        'id': data['morning_routine']['start_event']['id'],
        'name': data['morning_routine']['start_event']['name']
    })

    previous_task_id = start_event.attrib['id']
    
    for task in data['morning_routine']['tasks']:
        task_element = ET.SubElement(process, 'task', {
            'id': task['id'],
            'name': task['name']
        })
        ET.SubElement(process, 'sequenceFlow', {
            'id': f"Flow_{len(process)}",
            'sourceRef': previous_task_id,
            'targetRef': task['id']
        })
        previous_task_id = task['id']

    end_event = ET.SubElement(process, 'endEvent', {
        'id': data['morning_routine']['end_event']['id'],
        'name': data['morning_routine']['end_event']['name']
    })
    
    ET.SubElement(process, 'sequenceFlow', {
        'id': f"Flow_{len(process)}",
        'sourceRef': previous_task_id,
        'targetRef': end_event.attrib['id']
    })

    tree = ET.ElementTree(definitions)
    tree.write(xml_file, encoding='utf-8', xml_declaration=True)

@app.command()
def main(yaml_file: str, xml_file: str):
    """Convert YAML to XML for the workflow engine."""
    convert_yaml_to_xml(yaml_file, xml_file)
    typer.echo(f"Converted {yaml_file} to {xml_file}")

if __name__ == "__main__":
    app()
