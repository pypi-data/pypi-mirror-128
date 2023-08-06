from distutils.core import setup
setup(
  name = 'StatistikPendidikan',
  packages = ['StatistikPendidikan'],
  version = '0.1.1.2',
  license='MIT',
  description = 'Library ini digunakan untuk memudahkan ekstraksi data dari http://statistik.data.kemdikbud.go.id/',
  author = 'Aryya Widigdha',
  author_email = 'aryya.widigdha@yahoo.com',
  url = 'https://github.com/adwisatya/StatistikPendidikan',
  download_url = 'https://github.com/adwisatya/StatistikPendidikan/archive/refs/tags/v0.1.tar.gz',
  keywords = ['kemendikbud', 'statistik pendidikan', 'KEYWORDS'],
  install_requires=[
          'requests',
	  'lxml.html',
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
