from setuptools import setup
import setuptools

setup(name='svg_func',
      version='1.0.15',
      description='functions in svg for logo',
      author='xmn',
      author_email='2579015983@qq.com',
      url='https://www.python.org/',
      license='MIT',
      keywords='svg',
      project_urls={
            'Documentation': 'https://packaging.python.org/tutorials/distributing-packages/',
            'Funding': 'https://donate.pypi.org',
            'Source': 'https://github.com/pypa/sampleproject/',
            'Tracker': 'https://github.com/pypa/sampleproject/issues',
      },
      package_dir={"": "src"},
      packages=setuptools.find_packages(where="src"),
      install_requires=[],
      python_requires='>=3'
     )

'''
https://www.cnblogs.com/yinzhengjie/p/14124623.html
creat python project:
python setup.py sdist
twine upload dist/*
# 1.0.15 适用于arch。poly，random，在前端表现合格
'''