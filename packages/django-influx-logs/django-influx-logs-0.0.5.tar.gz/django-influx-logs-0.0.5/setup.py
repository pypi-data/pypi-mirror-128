from setuptools import setup, find_packages
import os
import influx_logs


README = os.path.join(os.path.dirname(__file__), 'README.md')

# When running tests using tox, README.md is not found
try:
    with open(README) as file:
        long_description = file.read()
except Exception:
    long_description = ''

setup(
    name='django-influx-logs',
    version=influx_logs.__version__,
    description=influx_logs.__doc__,
    packages=find_packages(),
    url='https://github.com/lazybird/django-influx-logs/',
    author='lazybird',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    include_package_data=True,
    zip_safe=False,
    license='MIT License',
    install_requires=[
        'influxdb',
      ],
)
