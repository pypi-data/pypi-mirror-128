import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gflight_api",
    version="0.0.1",
    author="Sujal Singh",
    author_email="email.sujalsingh@gmail.com",
    description="Fetch data from google flights",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sujaldev/gflight-api",
    project_urls={
        "Issues": "https://github.com/sujaldev/gflight-api/issues"
    },
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content"
    ],
    package_dir={"": "src"},
    py_modules=["gflight"],
    # packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=['requests']
)
