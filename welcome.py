import os
from os import path
from buildui import get_layouts

from pyxley.utils import create_app, default_static_path, default_template_path

# create the flask app
here = path.abspath(path.dirname(__file__))
HTML_PARAMS = {
    "page_scripts": ["bundle.js"],
    "base_scripts": [],
    "css": ["main.css"],
    "title": "BCBS"
}
app = create_app(here, default_static_path(), default_template_path(), index_params=HTML_PARAMS)

# build the layout
get_layouts(app, here+"/files/sentimentAHY.txt")

port = os.getenv('PORT', '5000')
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(port))

