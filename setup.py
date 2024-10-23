from setuptools import setup, find_packages

setup(
    name="etl_cli_tool",  # Name of your package
    version="1.0",  # Version number
    description="ETL and Database Query CLI tool",  # Description of the tool
    author="Arko Bhattacharya",  # Author details
    author_email="arko.bhattacharya@duke.edu",
    packages=find_packages(),  # Automatically find all packages inside `mylib`
    install_requires=[  # Optional: Add dependencies here
        "black==24.8.0",
        "click==8.1.7",
        "pytest==8.3.3",
        "pytest-cov==5.0.0",
        "requests==2.32.2",
        "ruff==0.6.9",
        "tabulate==0.9.0",
        "python-dotenv==1.0.1",
        "databricks-sql-connector==3.4.0",  # List any external dependencies (e.g., 'pandas', 'SQLAlchemy', etc.)
    ],
    entry_points={  # Define the CLI entry point
        "console_scripts": [
            "etl_cli=mypackage.main:interactive_menu",  # Correct reference to main.py in mylib
        ],
    },
)
