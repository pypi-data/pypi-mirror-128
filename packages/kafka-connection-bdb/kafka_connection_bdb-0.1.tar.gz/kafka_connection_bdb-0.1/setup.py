from distutils.core import setup

setup(name='kafka_connection_bdb',
      version='0.1',
      description='kafka connection',
      url='https://github.com/anjana-bijilesh/kafka_connection',
      download_url='https://github.com/anjana-bijilesh/kafka_connection/archive/refs/tags/v1.0.0.tar.gz',
      author='Anjana',
      author_email='anjana.v@bdb.ai',
      keywords=['kafka'],
      license='MIT',
      install_requires=['requests', 'confluent_kafka', 'logger', 'util', 'concurrent', ],

      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'Topic :: Software Development :: Build Tools',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.4',
      ],
      )
