from setuptools import setup


setup(name='cifar-extender',
      version='1.0',
      description='extending the cifar datasets with imagenet images',
      long_description=open('README.md').read(),
      author='Chris Messier',
      license='BSD 3-Clause',
      author_email='messier.development@gmail.com',
      url='https://github.com/messiest/cifar-extender',
      packages=['cifar_extender'],
      scripts=[
          'cifar_extender/cifar_download.py',
          'cifar_extender/cifar_parser.py'
      ],
      install_requires=open('requirements.txt', 'r').readlines(),
      classifiers=[
          'Development Status :: 1 - Planning',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: BSD License',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 3.6',
          'Topic :: Scientific/Engineering :: Artificial Intelligence',
      ],
)
