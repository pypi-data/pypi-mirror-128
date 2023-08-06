# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['blenderless']

package_data = \
{'': ['*']}

install_requires = \
['bpy==2.91a0',
 'click>=8.0.1,<9.0.0',
 'hydra-core>=1.0.7,<2.0.0',
 'imageio',
 'pillow',
 'tqdm>=4.61.2,<5.0.0',
 'trimesh>=3.9.24,<4.0.0',
 'xvfbwrapper>=0.2.9,<0.3.0']

entry_points = \
{'console_scripts': ['blenderless = blenderless.cli:cli']}

setup_kwargs = {
    'name': 'blenderless',
    'version': '0.1.8',
    'description': 'Blenderless is the python package for easy headless rendering using blender.',
    'long_description': "# Blenderless\n\nBlenderless is the Python package for easy headless rendering using Blender.\n\nWhile Blender is a fantastic open-source 3D modeling software which can be run from the command line, there are still some inconveniences when rendering from a headless server:\n\n - the blender python interface `bpy` can only be imported a single time,\n - and, there is no framebuffer for blender to write to.\n\nFurthermore, the `bpy` interface has a steep learning curve.\n\n This package is meant to overcome these issues in a easy-to-use manner. It does so by first defining the entire scene and only interacting with the `bpy` at render time in a separate thread using a virtual framebuffer.\n\n Example use cases:\n  - Generating thumbnails or previews from 3D files.\n  - Batch generation of views from 3D files.\n  - Automatic generation of compositions of a set of meshes into a single scene\n  - Converting meshes and labels into .blend files\n  - Export GIF animations of a camera looping around an object.\n\n\n## How to use this\n\n### Resources:\n - You can find basic examples in the [unit tests](https://github.com/oqton/blenderless/tree/master/tests/test_data).\n - [Notebook examples](https://github.com/oqton/blenderless/tree/master/notebooks) (point clouds, mesh face colors, ...)\n\n\n### Python module\n\nThe blenderless package can be loaded as a module. The main functionality is exposed using the Blenderless class. There is support for Jupyter Notebooks as the images/gifs will be shown as IPython Image objects automatically.\n\n\n```python\nfrom blenderless import Blenderless\n\n# Set the following property if you want to export the generated blender workspace.\nBlenderless.export_blend_path = 'export.blend'\n\n# Render single STL file\npath_to_foo_png = Blenderless.render('meshpath.stl', dest_path=None, azimuth=45, elevation=30, theta=0)\n\n# Render from config, note that objects and cameras are defined within the YAML config.\npath_to_foo_png = Blenderless.render_from_config('config.yml', dest_path=None)\n\n# Render GIF animation, note that azimuth is defined by number of frames.\npath_to_foo_gif = Blenderless.gif(cls, mesh_path, dest_path=None, elevation=30, theta=0, frames=60, duration=2)\n```\n\n### Command-line interface\n\nRender geometry file to image\n\n```sh\n$ blenderless image foo.stl output.png\n$ blenderless --export-blend-path export.blend image foo.stl output.png # If .blend needs to be exported\n```\n\nRender geometry to gif with a camera looping around an object.\n\n```sh\n$ blenderless gif foo.stl output.gif\n```\n\nThe following command rendera a YAML config to an image\n\n```sh\n$ blenderless config scene.yml output.png\n```\n\n### YAML configuration files\n\nMore advanced scenes can be defined using a YAML configuration file. In this file objects, cameras, labels, materials and presets can be defined.\n\nExample:\n```yaml\nscene: # See options in blenderless.scene.Scene\n  preset_path: ../../preset.blend\n\ncameras: # See options in blenderless.camera\n  - _target_: blenderless.camera.SphericalCoordinateCamera # Instantiate one camera with following arguments\n    azimuth: 45\n    elevation: 30\n    theta: 0\n    distance: 1\n\nobjects: # See blenderless.geometry and blenderless.material\n  - _target_: blenderless.geometry.Mesh # Refers to classes within the blenderless package\n    mesh_path: ../../mesh/3DBenchy.stl # Constructor argument\n    material: # Constructor argument pointing towards another class within the blenderless package\n      _target_: blenderless.material.MaterialFromName\n      material_name: test_material # Link to material name known in present.blend\n\n  - _target_: blenderless.geometry.BlenderLabel\n    label_value: '42'\n```\n\n\n### Export blender file\n\n## Install\n\n```buildoutcfg\nsudo apt-get install xvfb\npipx install poetry==1.1.5\nmake .venv\n```\n\n### Testing\n\n```sh\nmake test\n```\n",
    'author': 'Axel Vlaminck',
    'author_email': 'axel.vlaminck@oqton.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/oqton/blenderless',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<3.8',
}


setup(**setup_kwargs)
