from setuptools import setup

setup(name='pixel_sorting',
      version='0.1',
      description='Pixel sorting with python',
      url='http://github.com/henne90gen/pixel_sorting',
      author='Henne',
      author_email='henne90gen@gmail.com',
      license='GPL',
      packages=['pixel_sorting'],
      zip_safe=False,
      test_suite="pixel_sorting.tests",
      install_requires=['Pillow'])
