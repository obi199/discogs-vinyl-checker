
from setuptools import find_packages, setup

setup(
    name='discogs_checker',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'certifi==2024.7.4',
        'charset-normalizer==2.0.4',
        'click==8.4.1',
        'discogs-client==2.3.0',
        'Flask==3.1.3',
        'Flask-SQLAlchemy==3.1.1',
        'greenlet==3.5.1',
        'idna==3.17',
        'itsdangerous==2.2.0',
        'Jinja2==3.1.6',
        'MarkupSafe==3.0.3',
        'oauthlib==3.2.2',
        'passlib==1.7.4',
        'psycopg2-binary==2.9.12',
        'python-dotenv==1.2.2',
        'requests==2.34.2',
        'six==1.16.0',
        'SQLAlchemy==2.0.50',
        'urllib3==2.7.0',
        'waitress==3.0.2',
        'Werkzeug==3.1.8',
    ],
)
