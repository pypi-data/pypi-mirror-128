# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kodak', 'kodak.database', 'kodak.resources', 'tests']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=8.3.2,<9.0.0',
 'flask-restful>=0.3.8,<0.4.0',
 'flask>=1.1.2,<2.0.0',
 'peewee>=3.13.3,<4.0.0',
 'ruamel.yaml>=0.16.12,<0.17.0']

extras_require = \
{'deployment': ['gunicorn>=20.1.0,<21.0.0']}

entry_points = \
{'console_scripts': ['kodak = kodak.cli:main']}

setup_kwargs = {
    'name': 'kodak',
    'version': '0.1.0',
    'description': 'HTTP server for uploading images and generating thumbnails',
    'long_description': "# kodak\n\nWeb server for auto-generating banners, previews, thumbnails, and more from any directory.\nLightweight, simple, and designed for performance.\n\nDeveloped with [Poetry 1.0+](https://python-poetry.org/)\n\n## Goals\n\n- Support defining server-side manipulation specifications\n\n  ```\n  KODAK_MANIP_FOOBAR_CROP_VERTICAL=300\n  KODAK_MANIP_FOOBAR_SCALE_HORIZONTAL=1200\n  KODAK_MANIP_FOOBAR_SCALE_STRATEGY=absolute\n\n  KODAK_MANIP_FIZZBUZZ_NAME=black+white\n  KODAK_MANIP_FIZZBUZZ_BLACK_AND_WHITE=true\n  KODAK_MANIP_FIZZBUZZ_SCALE_HORIZONTAL=50\n  KODAK_MANIP_FIZZBUZZ_SCALE_STRATEGY=relative\n  ```\n\n- Support retrieving manipulated images based on server side configuration\n\n  ```\n  GET /image/<name>/foobar\n\n  GET /image/<name>/black+white\n  ```\n\n- Support optionally exposing full-resolution source images\n\n  ```\n  GET /image/<name>/original\n  ```\n\n- Support caching of generated image manipulations for reuse\n\n- Support [HTTP 410](https://httpstatuses.com/410) for indicating removed images and\n  manipulations\n\n- Support optional authentication with pre-generated access tokens\n\n- Support static file tree management for exposure via external web server (which is faster\n  than serving files with python)\n\n- Support automatic indexing of newly added image files\n\n- Support automatic indexing of removed image files\n\n- Support arbitrary source directory structure\n\n- Support Dockerized deployment\n\n- Support bare-metal deployment (via systemd)\n\n## Non-goals\n\n- Client-defined image manipulations through publicly exposed parameters\n\n  > Manipulating images is- in the grand scheme of things- pretty resource intensive. Exposing\n  > dynamic parameters that can be cycled through to generate hundreds or thousands of\n  > permutations for every known image on a server could be used to either consume the\n  > server's entire disk or server's entire CPU.\n\n- Upload functionality\n\n  > This application should be as simple as possible. Lots of people have implemented file\n  > upload systems, synchronizers, and managers way better than I have.\n\n- Robust and flexible access control\n\n  > See above. Complex authentication can be added using a reverse proxy or any one of several\n  > dozen options for 3rd party middleware. The provided authentication is supposed to be\n  > dead simple for people who absolutely need the server to be private but absolutely cannot\n  > implement something more complicated.\n\n- Pre-creation of image manipulations\n\n  > The goal of this program is just-in-time creation of the manipulated assets with\n  > aggressive caching; first load is slow, subsequent loads are fast. For this use case\n  > there's no sense creating or storing an asset until it's known to be needed.\n",
    'author': 'Ethan Paul',
    'author_email': '24588726+enpaul@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/enpaul/kodak/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
