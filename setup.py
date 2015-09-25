try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'An basic but interesting distributed calendar',
    'author': 'Xiaoyan Lu',
    'url': 'http://github.com/xil12008/calendar-wuu-bernstein-algorithm',
    'download_url': 'http://github.com/xil12008/calendar-wuu-bernstein-algorithm',
    'author_email': 'My email.',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['calendar'],
    'scripts': [],
    'name': 'calendar-wuu-bernstein-algorithm'
}

setup(**config)
