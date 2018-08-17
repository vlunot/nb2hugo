from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='nb2hugo',
      python_requires='>=3.6',
      version='0.1',
      description='A Jupyter notebook to Hugo markdown converter',
      long_description=readme(),
      keywords='jupyter notebook hugo converter',
      url='http://github.com/vlunot/nb2hugo',
      author='Vincent Lunot',
      author_email='vlunot@gmail.com',
      license='MIT',
      packages=['nb2hugo'],
      install_requires=[
          'nbconvert',
          'nbformat',
          'traitlets',
          'argparse',
          'pytest',
      ],
      scripts=['bin/nb2hugo'],
      include_package_data=True,
      zip_safe=False)
