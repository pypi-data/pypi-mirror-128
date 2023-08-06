from setuptools import setup


setup(
    name='sabyvok',
    version='1.0.1',
    description='Saby Vok API client',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=['sabyvok'],
    install_requires=['requests'],
    author='Igor Veselov',
    author_email='mail@veseloff.net',
    zip_safe=False,
    url='https://github.com/saby/vok/tree/main/client-py',
)
