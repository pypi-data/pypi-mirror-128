import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="cookdir",
    version="0.0.1",
    author="yjdai",
    author_email="136271877@qq.com",
    description="create directories by template",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Blockhead-yj/cookdir",
    include_package_data=True,
    package_data={
        'cookdir':['recipe/*.yml']
    },
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9' # actually i don't know it, but i write this in 3.9
)
