from setuptools import setup

setup(name='xls_report',
      version='0.0.8',
      packages=['xls_report'],
      url='https://github.com/oleglpts/xls_report',
      license='MIT',
      platforms='any',
      author='Oleg Lupats',
      author_email='oleglupats@gmail.com',
      description='Database report generation in .xls format according to the xml description',
      long_description=open('README.md').read(),
      long_description_content_type='text/markdown',
      zip_safe=False,
      classifiers=[
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.5'
      ],
      python_requires='>=3',
      install_requires=['lxml>=4.3.4', 'xlwt>=1.3.0', 'pycurl>=7.43.0.3'])
