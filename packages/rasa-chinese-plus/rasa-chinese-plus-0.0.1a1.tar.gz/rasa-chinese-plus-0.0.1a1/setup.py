import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rasa-chinese-plus",
    version="0.0.1a1",
    author="yizheng dai",
    author_email="387942239@qq.com",
    description="A Chinese extension package for Rasa",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/daiyizheng/rasa-chinese-plus",
    packages=setuptools.find_packages(),
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development",
    ],
    install_requires=[
        # "rasa>=2.0"
    ],
    python_requires='>=3.5',
    package_data={
        "rasa_chinese_plus": [
            "*.py",
            "*.so",
        ]
    },
)