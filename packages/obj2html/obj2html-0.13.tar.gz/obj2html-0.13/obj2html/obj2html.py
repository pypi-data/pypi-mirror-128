import os
import json
import re
import copy

TEMPLATE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'index.html')
TEMPLATE_ELEMENTS_ONLYT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'elements.html')


def simple_mustache(input_string, value_dict):
  output_string = copy.deepcopy(input_string)
  mustache_variables = re.findall(r"{{.*?}}",output_string)

  for v_text in mustache_variables:
    v_name = v_text[2:-2].strip()
    if '.' in v_name:
      dict_name, dict_subname = v_name.split(".")
      v = value_dict[dict_name][dict_subname]
    else:
      v = value_dict[v_name]
    output_string = output_string.replace(v_text, str(v))
  return output_string

def obj2html(
  obj_path, output_html_path=None, 
  camera={
      "fov": 45,
      "aspect": 2,
      "near": 0.1,
      "far": 100,
      "pos_x": 0,
      "pos_y": 10,
      "pos_z": 20,
      "orbit_x": 0,
      "orbit_y": 5,
      "orbit_z": 0,
    },
    light={
      "color": "0xFFFFFF",
      "intensity": 1,
      "pos_x": 0,
      "pos_y": 10,
      "pos_z": 0,
      "target_x": -5,
      "target_y": 0,
      "target_z": 0,
    },
    obj_options={
      "scale_x": 30,
      "scale_y": 30,
      "scale_z": 30,
    },
    html_elements_only=False
  ):
  with  open(obj_path, "r") as f:
    content = f.readlines()
  content = '\n'.join(content)
  js_cont = {'obj': content}
  js_string = json.dumps(js_cont)

  template_path = TEMPLATE_PATH
  if html_elements_only:
    template_path  = TEMPLATE_ELEMENTS_ONLYT_PATH
  with  open(template_path, "r") as f:
    html_template = f.read()

  data_dict = {
    "obj_3d": js_string,
    "obj_options": obj_options,
    "camera": camera,
    "light": light,
  }

  html_string = simple_mustache(html_template, data_dict)

  if output_html_path != None:
    with  open(output_html_path, "w") as f:
      f.write(html_string)
  else:
    return html_string

if __name__ == '__main__':
  obj2html('model.obj', 'tmp.html', html_elements_only=True)