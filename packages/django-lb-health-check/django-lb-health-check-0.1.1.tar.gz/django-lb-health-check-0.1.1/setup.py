# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lb_health_check']

package_data = \
{'': ['*']}

install_requires = \
['Django>=2.2']

setup_kwargs = {
    'name': 'django-lb-health-check',
    'version': '0.1.1',
    'description': 'Middleware based health check for Django',
    'long_description': '# Django Load Balancer Health Check\n\nAliveness check for Django that bypasses ALLOWED_HOSTS\n\n## Purpose\n\nWhen running on app platforms (Heroku/DigitalOcean/etc), Kubernetes, AWS behind an Elastic Load Balancer, and other similar platforms it is often the case that the host header is not set appropriately for health checks. When these platforms perform an HTTP health check without the proper host header an *error 400 bad request* will be returned by Django. This is because the Django Common Middleware tests the host header and raises a DisalowedHost exception if it doesn\'t match what is in ALLOWED_HOSTS. This package provides an alternative health/aliveness check that is returned by middlware and thus bypasses the ALLOWED_HOSTS check. In order to accomplish this, django-lb-health-check middleware checks if the incoming URL is for the known health check URL and returns a response - bypassing the majority of the Django platform. It is not designed as a replacement for something like [django-health-check](https://github.com/KristianOellegaard/django-health-check), but instead as a better alternative to a TCP based aliveness check that ensures your Django project has been started and is responding to HTTP instead of just having a port open.\n\n## Usage\n\nInstall *django-lb-health-check*\n\n```shell\npip install django-lb-health-check\n```\n\nAdd *lb_health_check* to your middleware. It **must** be above *django.middleware.common.CommonMiddleware* and should be below *django.middleware.security.SecurityMiddleware*, as high in the stack as possible to prevent any queries or unneeded code from running during a health check.\n\n```python\nMIDDLEWARE = [\n    \'django.middleware.security.SecurityMiddleware\',\n    \'lb_health_check.middleware.AliveCheck\', #  <- New middleware here\n    \'django.contrib.sessions.middleware.SessionMiddleware\',\n    \'django.middleware.common.CommonMiddleware\',\n    \'django.middleware.csrf.CsrfViewMiddleware\',\n    \'django.contrib.auth.middleware.AuthenticationMiddleware\',\n    \'django.contrib.messages.middleware.MessageMiddleware\',\n    \'django.middleware.clickjacking.XFrameOptionsMiddleware\',\n]\n```\n\nSet the URL you want to use for your aliveness check. Note that a GET request to this URL **will** shadow any other route you have defined through the Django URL mapper. Aliveness URL can be a string for a single health check URL or a list of strings if you want the aliveness check to run from multiple URLs. The multiple URL strategy is helpful if you are changing the URL of the endpoint by allowing both the old and new URLs to be checked.\n\n```python\nALIVENESS_URL = "/health-check/"\n```\n\nTest your health check after starting your server:\n\n```bash\ncurl localhost:8000/health-check/\nOK\n```\n',
    'author': 'Adam Peacock',
    'author_email': 'adam@thepeacock.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Hovercross/django-lb-health-check',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
