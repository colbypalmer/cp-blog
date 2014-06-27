import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-cp-blog',
    version='0.1.3',
    packages=['blog',],
    include_package_data=True,
    license='MIT License',  # example license
    description='A basic blog app for Django.',
    long_description=README,
    url='http://github.com/colbypalmer/cp-blog/',
    author='Colby Palmer',
    author_email='colby@colbypalmer.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires=[
        'Markdown==2.4',
        'django-recaptcha==0.0.9',
        'Pillow==2.3.0',
        'pygments==1.6',
        'South==0.8.4',
        'django-grappelli==2.5.3',
        'django-epiceditor==0.2.2',
    ],
)