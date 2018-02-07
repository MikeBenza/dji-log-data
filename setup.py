from setuptools import setup, find_packages

setup(name='dji_log_data',
      version='0.0.1',
      description='Data files for code generation for DJI log files (TXT flight records)',
      url='http://github.com/MikeBenza/dji-log-data',
      author='Mike Benza',
      author_email='mb.github.code@gmail.com',
      license='MIT',
      packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
      include_package_data=True,
      install_requires=['jinja2'],
      entry_points={
          'console_scripts': [
              'generate_code = dji_log_data.__main__:main'
          ]
      },
      classifiers=[
          'Development Status :: 2 - Pre-Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 3',
      ],
      zip_safe=False)