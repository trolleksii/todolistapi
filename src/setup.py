from setuptools import setup, find_packages

setup(
    name="todoitemslistapi",
    version="0.0.1",
    description="Todo List API",
    packages=find_packages(),
    include_package_data=True,
    scripts=["manage.py"],
    install_requires=[
        "Django>=2.1.2",
        "django-cors-headers>=2.4.0",
        "gunicorn>=19.9.0"
    ],
    extras_require={
        "test": [
            "colorama>=0.4.0",
            "coverage>=4.5.1",
            "django-nose>=1.4.6",
            "nose>=1.3.7",
            "pinocchio>=0.4.2",
            "pytz>=2018.5"
        ]
    }
)
