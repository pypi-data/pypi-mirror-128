import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="kiosk_bot",
    version="1.0",
    license='MIT',
    author="momozzing",
    author_email="ahdbsgh2@naver.com",
    description="kogpt2 based kiosk chatbot",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/momozzing/kiosk_bot",
    packages=setuptools.find_packages(),
    classifiers=[
        # 패키지에 대한 태그
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3.6'
)