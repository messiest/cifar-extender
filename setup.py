from distutils.core import setup

setup(name='cifar-extender',
      version='1.0',
      description='extending the cifar datasets',
      long_description=open('README.md').read(),
      author='Chris Messier',
      license='BSD 3-Clause',
      author_email='messier.development@gmail.com',
      url='https://github.com/messiest/cifar-extender',
      packages=['cifar_extender'],
      classifiers=['Development Status :: 1 - Planning',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: BSD License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Programming Language :: Python :: 3',
                   'Topic :: Artificial Intelligence :: Scientific/Engineering'],
      entry_points={
          'console_scripts': [
              'cifar-download = cifar_extender.download:main'
          ]
      },
      )
