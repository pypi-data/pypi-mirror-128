from setuptools import setup

setup(
    name='ecscontrol',
    version='1.0.1',
    license='MIT',
    description = 'Tool for automation of deployments to AWS ECS',
    author = 'Milos Kozak',
    author_email = 'milos.kozak@lejmr.com',
    url = 'https://github.com/lejmr/ecsctl',
    download_url = 'https://github.com/lejmr/ecsctl/archive/v_01.tar.gz',    
    packages=['ecs', 'ecs.bin'],
    install_requires=[
        'Click',
        'Jinja2',
        'python-magic',
        'python-slugify',
        'dateparser',
        'boto3',
        'PyYAML'
    ],
    entry_points={
        'console_scripts': [
            'ecsctl = ecs.bin.ecsctl:group',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',      # Define that your audience are developers
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',   # Again, pick a license
        'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)