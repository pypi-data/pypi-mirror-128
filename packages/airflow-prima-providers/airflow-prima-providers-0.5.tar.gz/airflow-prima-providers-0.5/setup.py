from distutils.core import setup

setup(
  name = 'airflow-prima-providers',
  packages = ['airflow-prima-providers'],
  version = '0.5',
  license='MIT',
  description = 'Airflow utility providers developed by Prima Assicurazioni',
  author = 'Prima Assicurazioni',
  author_email = 'team-data@prima.it',
  url = 'https://github.com/albanovito/providers-prima',
  download_url = 'https://github.com/albanovito/providers-prima/archive/refs/tags/0.5.tar.gz',
  keywords = ['airflow', 'prima', 'providers'],
  install_requires=[
          'apache-airflow',
          'boto3',
          'botocore',
          'cached_property'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9'
  ],
)