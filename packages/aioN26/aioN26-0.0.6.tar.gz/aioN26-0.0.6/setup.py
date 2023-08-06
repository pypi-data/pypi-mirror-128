from setuptools import setup

setup(name='aioN26',
      version='0.0.6',
      license='MIT',
      author='Marcelo Troitino',
      author_email='marcelo@cygnuskraft.es',
      description='Unofficial asynchronous API interface to the N26 bank',
      long_description=open('README.rst').read(),  #'file: README.rst',
      url='https://www.cygnuskraft.es/contact-us/',
      keywords='N26 asyncio aioN26 API',
      include_package_data=True,
      classifiers = [
          'Development Status :: 4 - Beta',
          'Framework :: AsyncIO',
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 3.10',
          'Topic :: Utilities',
          'License :: OSI Approved :: MIT License'],
      install_requires=['aiohttp==3.8.1',
                        'certifi==2021.10.8',
                        'click==8.0.3',
                        'pycryptodome==3.11.0',
                        'python-dotenv==0.19.2',
                        'aiofiles==0.7.0']
      )