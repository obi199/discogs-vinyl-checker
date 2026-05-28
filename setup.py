
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
        'click==8.0.1',
        'discogs-client==2.3.0',
        'Flask==2.2.5',
        'Flask-SQLAlchemy==2.5.1',
        'greenlet>=3.0.0',
        'idna==3.7',
        'itsdangerous==2.0.1',
        'Jinja2==3.1.4',
        'MarkupSafe>=2.1.1',
        'oauthlib==3.2.2',
        'passlib==1.7.4',
        'psycopg2-binary>=2.9.10',
        'python-dotenv==1.2.2',
        'requests==2.31.0',
        'six==1.16.0',
        'SQLAlchemy==1.4.22',
        'urllib3==1.26.18',
        'waitress==2.1.2',
        'Werkzeug==3.0.3',
    ],
)
