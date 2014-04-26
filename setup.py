from distutils.core import setup

setup(
      name='nlp',
      version='.1',
      description='Personal NLP Tools',
      author='Greg Romrell',
      author_email='grromrell@gmail.com',
      packages = ['base_nlp'],
      package_dir = {'base_nlp' : 'base_nlp'}
)

