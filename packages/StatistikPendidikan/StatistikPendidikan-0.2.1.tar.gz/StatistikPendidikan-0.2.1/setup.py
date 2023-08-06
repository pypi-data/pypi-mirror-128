from distutils.core import setup, Extension

with open("README", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
  name = 'StatistikPendidikan',
  packages = ['StatistikPendidikan'],
  version = '0.2.1',
  license='MIT',
  description = 'Library ini digunakan untuk memudahkan ekstraksi data dari http://statistik.data.kemdikbud.go.id/',
  long_description=long_description,
  author = 'Aryya Widigdha',
  author_email = 'aryya.widigdha@yahoo.com',
  url = 'https://github.com/adwisatya/StatistikPendidikan',
  download_url = 'https://github.com/adwisatya/StatistikPendidikan/archive/refs/tags/v0.2.tar.gz',
  keywords = ['kemendikbud', 'statistik pendidikan', 'statistik.data.kemdikbud.go.id'],
  install_requires=[
          'requests',
	  'lxml',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
)
