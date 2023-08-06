# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['jupyter_to_medium']

package_data = \
{'': ['*'], 'jupyter_to_medium': ['static/*']}

install_requires = \
['beautifulsoup4>=4.10.0,<5.0.0',
 'jupyter-contrib-nbextensions>=0.5.1,<0.6.0',
 'jupyter>=1.0.0,<2.0.0',
 'matplotlib>=3.5.0,<4.0.0',
 'nbconvert==5.6.1',
 'numpy>=1.21.4,<2.0.0',
 'requests>=2.26.0,<3.0.0']

entry_points = \
{'console_scripts': ['jupyter_to_medium = '
                     'jupyter_to_medium._command_line:main']}

setup_kwargs = {
    'name': 'jupyter-to-medium',
    'version': '0.2.9',
    'description': 'Publish a Jupyter Notebook as a Medium blogpost',
    'long_description': '# Jupyter to Medium\n\n[![](https://img.shields.io/pypi/v/jupyter_to_medium)](https://pypi.org/project/jupyter_to_medium)\n[![PyPI - License](https://img.shields.io/pypi/l/jupyter_to_medium)](LICENSE)\n\nPublish Jupyter Notebooks as Medium blog posts directly from your notebook with the help of jupyter_to_medium.\n\n![](docs/images/social_share_small.png)\n\n## Target User\n\nDo you ....\n\n* Publish blog posts on Medium?\n* Use Jupyter Notebooks to write your posts?\n* Dislike the time and effort it takes to transfer your posts from Jupyter to Medium?\n* Get lost/bored when switching between the medium editor, gist etc to create well linted code?\n* Want to integrate LaTeX into your posts without manually screenshot-ing all your equation cells?\n\nIf so, jupyter_to_medium will automate the process of taking your Jupyter Notebook, as is, and publishing it as a Medium post in almost no time at all saving huge amounts of time.\n\n## Motivation\n\nI\'ve [published dozens of blog posts on Medium][0] myself with all of them beginning as Jupyter Notebooks. Manually converting them to Medium posts was a fairly lengthy, painstaking process. One particularly painful process was inserting tables, which Medium does not support, into my posts. Nearly all of my posts contain numerous pandas DataFrames ([such as this one][1], which has 40! DataFrames) which are represented as HTML tables within a notebook. I\'d take screenshots of each one to insert them into my Medium posts.\n\n[0]: http://medium.com/dunder-data\n[1]: https://medium.com/dunder-data/selecting-subsets-of-data-in-pandas-6fcd0170be9c\n\n## Installation\n\n`pip install jupyter_to_medium`\n\n### Automatically activated\n\nYou should be able to skip the next step, but if the extension is not showing up in your notebook, run the following command:\n\n`jupyter bundlerextension enable --py jupyter_to_medium._bundler --sys-prefix`\n\n## Get an Integration Token from Medium\n\nBefore using this package, you must request an integration token from Medium by emailing them at <a href="mailto:yourfriends@medium.com">yourfriends@medium.com</a> allowing you to create a token in <a href="https://medium.com/me/settings">your Medium settings.</a> You can read the [entire instructions on how to get your integration token](https://github.com/Medium/medium-api-docs#21-self-issued-access-tokens).\n\n### Creating the integration token\n\nOnce your request to create integration tokens is accepted, navigate to <a href="https://medium.com/me/settings">your Medium settings.</a> Towards the bottom of the page exists the section on Integration Tokens. Enter a description for the token (`jupyter_to_medium` is a good choice) and then create the token.\n\n![png](docs/images/integration_token.png)\n\n### Save your integration token\n\nOnce you have your integration token, create the folder and file `.jupyter_to_medium/integration_token` in your home directory and save the token there. If you don\'t save it, you\'ll need to access it every time you wish to make a new post.\n\n### Create / save your github PAT (only required for gist integration)\n\nWhen publishing, jtm can take unformatted code snippets and replace them with [linted gists](https://gist.github.com/mjam03/761d017e821b62c3adf2d4cf1b7477d3). In order to do this, it needs to create the gists which requires github access as well as a Personal Access Token (PAT). To create a github account, sign up [here](https://github.com/) and then follow [these instructions](https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token) to create a PAT - __ensure to select the option for creating gists__.\n\nOnce you have your Github PAT, similar to the integration token, create the folder and file `.jupyter_to_medium/github_token` in your home directory and save the token there. If you don\'t save it, you\'ll need to access it every time you wish to make a new post.\n\n## Usage\n\nThere are three ways to publish notebooks:\n\n* Within an active notebook\n* From the command line\n* Using a Python script\n\n### Publishing to Medium within a Notebook\n\nAfter installation, open the notebook you wish to publish and select the option `File -> Deploy as -> Medium Post`\n\n![png](docs/images/menu_option.png)\n\nA new browser tab will open with a short form that needs to be completed.\n\n![png](docs/images/form.png)\n\nAfter clicking publish, the notebook and all images will be uploaded to Medium. Any HTML tables (such as pandas DataFrames) will be converted to images (via chrome), as Medium has no ability to represent tables. This is a time consuming process, so be prepared to wait. Check your terminal for updates. If successful, you\'ll get the following response with a link to view the post.\n\n![png](docs/images/success.png)\n\nClick the link to view the post.\n\n![png](docs/images/post.png)\n\n### Finalize and publish on Medium\n\nCurrently, your post will be published as a draft. Review and publish the post on Medium.\n\n### Publishing to Medium from the Command Line\n\nUpon installation, you\'ll have access to the command line program `jupyter_to_medium` with the same options as the below function.\n\n```bash\njupyter_to_medium --pub-name="Dunder Data" --tags="python, data science" "My Awesome Blog Post.ipynb"\n```\n\n### Publishing to Medium with a Python Script\n\nIn a separate script/notebook, import `juptyer_to_medium` as a module. Pass the `publish` function the location of the Jupyter Notebook you would like to publish as a Medium blog post.\n\n```python\nimport jupyter_to_medium as jtm\njtm.publish(\'My Awesome Jupyter Notebook.ipynb\',\n            integration_token=None,\n            pub_name=None,\n            title=None,\n            tags=None,\n            publish_status=\'draft\',\n            notify_followers=False,\n            license=\'all-rights-reserved\',\n            canonical_url=None,\n            chrome_path=None,\n            save_markdown=False,\n            table_conversion=\'chrome\',\n            gistify=False,\n            gist_threshold=5\n            )\n```\n\nIf successful, a message will be printed with the URL to your post.  Additionally, JSON data will be returned as a dictionary containing the returned request from Medium.\n\n## Works for Classic Notebook not Jupyter Lab\n\nCurrently, this package only works for the "classic" Jupyter Notebook and is not available in Jupyter Lab. If you have experience making Jupyter Lab extensions, please let me know.\n\n## Troubleshooting\n\nIf your post is unsuccessful, a message with the error will be printed to the screen with information that might help you solve the issue.\n\n### Table conversion with Chrome or Matplotlib\n\nBy default, tables will be converted via Chrome web browser by taking screenshots of them. If you don\'t have Chrome installed or cannot \nget chrome to work, select \'matplotlib\' for the table conversion.',
    'author': 'dexplo',
    'author_email': 'petrou.theodore@gmail.com',
    'maintainer': 'mjam03',
    'maintainer_email': 'markjamison03@gmail.com',
    'url': 'https://github.com/dexplo/jupyter_to_medium',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)
