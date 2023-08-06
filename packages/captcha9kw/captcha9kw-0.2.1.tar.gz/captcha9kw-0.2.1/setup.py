# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['captcha9kw']

package_data = \
{'': ['*']}

install_requires = \
['filetype>=1.0.8,<2.0.0',
 'requests>=2.26.0,<3.0.0',
 'validators>=0.18.2,<0.19.0']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=1.0,<2.0']}

setup_kwargs = {
    'name': 'captcha9kw',
    'version': '0.2.1',
    'description': 'A simple package for interacting with the 9kw.eu anti-captcha service.',
    'long_description': '\nWelcome to captcha9kw’s documentation!\n**************************************\n\ncaptcha9kw is a smallish Python package for making use of the\n`9kw.eu`_ services, including solving of interactive captchas like\nGoogle’s reCaptcha or image-based captchas used by a lot of different\nservices out there.\n\nImportant: This package is under construction and functionality may change.\n\n\nInstallation\n============\n\nYou can install captcha9kw from PyPI using pip:\n\n.. code:: shell\n\n   $ pip install captcha9kw\n\n\nGetting started\n===============\n\nSolving a simple image-based captcha is pretty easy:\n\n   .. image:: docs/source/_static/captcha.gif\n\n   The captcha used here.\n\nimage-captcha\n\n.. code:: python\n\n   from captcha9kw import api9kw\n\n   conn = api9kw()\n   conn.api_key = "myapikeyhere"\n   print(f"Current account balance: {conn.balance} credits.")\n   captcha_id = conn.submit_image_captcha("mycaptcha.gif")\n   answer = conn.get_answer(captcha_id, wait=1)\n   if(answer == "spring water"):\n       conn.captcha_feedback_correct(captcha_id)\n   else:\n       conn.captcha_feedback_incorrect(captcha_id)\n\nSimilarly, for e.g. a reCaptcha:\n\ninteractive captcha\n\n.. code:: python\n\n   from captcha9kw import api9kw\n\n   conn = api9kw()\n   conn.api_key = "myapikeyhere"\n   print(f"Current account balance: {conn.balance} credits.")\n   website_url = "https://www.some.web.site"\n   website_key = obtain_site_key() # Supply your own code here\n   captcha_id = conn.submit_interactive_captcha(website_key, website_url)\n   answer = conn.get_answer(captcha_id, wait=1)\n   if(test_answer_on_site(answer)):\n       conn.captcha_feedback_correct(captcha_id)\n   else:\n       conn.captcha_feedback_incorrect(captcha_id)\n\nFor more information, check the `API Reference\n<api_reference.rst#api-reference>`_.\n\n\n9kw.eu\n======\n\n9kw.eu is a German captcha-solving service, providing a quick and easy\nAPI over HTTP GET/POST. Users can buy credits that will be deducted\nfrom based on the type of captcha in question and related settings. As\na nice bonus, users can also earn credits for themselves by solving\nother people’s captchas, either through the website directly or\nthrough their custom client.\n\nYou can sign up for their service at: https://www.9kw.eu/register.html\n\nOr, if you really wish to grant me a couple of free credits, sign up\nusing my referral link: https://www.9kw.eu/register.html?r=210326\n\nNote: Do not feel any pressure to use the referral link! I know a lot of\n   people feel iffy about such and I do not feel offended, if you\n   prefer to not add me as your referrer.\n\nAlso, maybe take a look at `their API <https://www.9kw.eu/api.html>`_.\n',
    'author': 'WereCatf',
    'author_email': 'werecatf@outlook.com',
    'maintainer': 'WereCatf',
    'maintainer_email': 'werecatf@outlook.com',
    'url': 'https://github.com/WereCatf/captcha9kw/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
