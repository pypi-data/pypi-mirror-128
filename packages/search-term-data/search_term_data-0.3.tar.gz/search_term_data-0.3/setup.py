from distutils.core import setup

setup(
    name='search_term_data',
    packages=['search_term_data'],
    version='0.3',
    license='MIT',
    description='Python deamon that monitors a directory for new csv files.',
    author='Kabelo Davhana',
    author_email='eugene.davhana@gmail.com',
    url='https://github.com/DVHKAB00122/coding-challenge',
    download_url='https://github.com/DVHKAB00122/coding-challenge/archive/refs/tags/v_03.tar.gz',
    keywords=['Monitors', 'daemon', 'csv'],
    install_requires=[
        'python-daemon', 'PyYAML'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
