from setuptools import setup

setup(name='django-charged',
      version='0.0.1',
      description='lightningd REST/ws API for django Lapps',
      url='http://github.com/FeedTheWeb/django-charged',
      author='Alex',
      author_email='dsoftware@protonmail.com',
      license='MIT',
      install_requires=['pylightning','channels','base58'],
      packages=['lightning'],
zip_safe=True)