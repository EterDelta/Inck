from setuptools import setup

with open('README.md', 'r', encoding='utf-8') as readme:
    long_description = readme.read()

setup(
    name='inck',
    version='1.0.0',
    description="Simple spatial domain Steganography, made a CLI tool. Because... Why not?",
    long_description_content_type="text/markdown",
    long_description=long_description,
    author='EterDelta',
    license='MIT',
    package_dir={'': 'src'},
    packages=[
        'inck'
    ],
    install_requires=[
        'Pillow'
    ],
    entry_points={
        'console_scripts': [
            "inck = inck.cli:entry",
        ],
    },
    classifiers=[
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Education",
        "Topic :: Scientific/Engineering :: Image Processing"
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ],
    python_requires='>=3.6'
)
