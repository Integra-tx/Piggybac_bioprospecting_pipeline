from setuptools import setup, find_packages

# Function to read requirements from requirements.txt
def parse_requirements(filename):
    """Load requirements from a pip requirements file."""
    with open(filename, 'r') as req_file:
        return req_file.read().splitlines()

# Read requirements from requirements.txt
requirements = parse_requirements('requirements.txt')

# Setup configuration
setup(
    name='bioprospecting_pipeline',
    version='1.0.0',
    packages=find_packages(),
    install_requires=requirements,  # Use the parsed requirements
    entry_points={
        'console_scripts': [
            'bioprospecting=bioprospecting_pipeline.main:main'
        ]
    },
    description='A Python pipeline for recovering proteins from genomes.',
    author='Alejandro Agudelo Franco',
    author_email='alejandro.af@integra-tx.com',
    url='https://github.com/Integra-tx/Piggybac_bioprospecting',
    license='MIT',
)



