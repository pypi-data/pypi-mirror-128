from setuptools import setup

version = {}
with open('genanki/version.py') as fp:
  exec(fp.read(), version)

setup(name='genanki-noyaml',
      version=version['__version__'],
      description='Generate Anki decks programmatically',
      url='http://github.com/brumar/genanki',
      author='Bruno Martin',
      author_email='martin.bruno.mail@gmail.com',
      license='MIT',
      packages=['genanki'],
      zip_safe=False,
      include_package_data=True,
      python_requires='>=3.6',
      install_requires=[
        'cached-property',
        'frozendict',
        'chevron'
      ],
      setup_requires=[
          'pytest-runner',
      ],
      tests_require=[
          'pytest>=6.0.2',
      ],
      keywords=[
        'anki',
        'flashcards',
        'memorization',
      ])
