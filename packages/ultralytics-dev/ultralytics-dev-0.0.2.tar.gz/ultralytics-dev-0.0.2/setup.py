import pathlib
import setuptools

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text(encoding="utf-8")

setuptools.setup(
    name="ultralytics-dev",  # name of pypi package
    version='0.0.2',  # version of pypi package
    python_requires=">=3.6",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/ultralytics/package-framework",
    author="Ultralytics",
    author_email='kalenmike@gmail.com',
    packages=['ultralytics'],
    include_package_data=True,
    install_requires=['PyYAML>=5.3.1', 'requests', 'GitPython>=3.1.24'],
    extras_require={'tests': [
        'pytest',
        'pytest-cov',
        'coverage',
    ]},
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development", "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Image Recognition",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX", "Operating System :: Unix",
        "Operating System :: MacOS"
    ],
    keywords=
    "machine-learning, deep-learning, ml, pytorch, YOLO, object-detection, vision, YOLOv3, YOLOv4, YOLOv5"
)
