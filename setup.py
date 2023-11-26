import io
import re
import ast
from setuptools import find_packages,setup

_version_re = re.compile(r'__version__\s+=\s+(.*)')

# Warn if we are installing over top of an existing installation. This can
# cause issues where files that were deleted from a more recent Django are
# still present in site-packages. See #18115.


EXCLUDE_FROM_PACKAGES = []
with io.open("src/plutonkit/__init__.py", "rt", encoding="utf8") as f:
    version = re.search(r'__version__ = "(.*?)"', f.read()).group(1)

EXCLUDE_FROM_PACKAGES = [];


setup(
    name='plutonkit',
    version=version,
    url='https://plutonkit.codehyouka.xyz/',
    author='Codehyouka',
    author_email='plants.coordinators@gmail.com',
    description=('Start kit for python, for building application'),
    license='MIT',
    packages=find_packages( "src"),
    package_dir={"": "src"},
    package_data={'': ['*.txt'],
                  'plutonkit.template':[
                      'ariadne/*',
                      'bottle/*',
                      'default_grpc/*',
                      'default_web3/*',
                      'default_websocket/*',
                      'django/*',
                      'django/testapp/*',
                      'django_graphbox/*',
                      'django_graphbox/myapp*',
                      'django_graphbox/myproject/*',
                      'django_rest/*',
                      'fastapi/*',
                      'flask/*',
                      'graphene/*',
                      'tartiflette/*'
                  ]},
    include_package_data=True,
    
    entry_points={'console_scripts': [
        'plutonkit = plutonkit.command:autoload',
    ]},
    install_requires=[
        "PyYAML>=6.0.1"
    ],
    platforms='any',
    extras_require={
            "pytest": ["pytest"],
            "pytz": ["pytz"],
            "pylint": ["pylint"],
    },
    zip_safe=False,
    classifiers=[
       
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
