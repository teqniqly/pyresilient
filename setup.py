from teqniqly import version
import setuptools
import os


def main():
    cwd = os.getcwd()
    abspath = os.path.abspath(__file__)
    dir_name = os.path.dirname(abspath)
    os.chdir(dir_name)

    with open("README.md", "r") as f:
        long_description = f.read()

    setuptools.setup(
        name="teqniqly-resilient",
        version=version,
        author="Teqniqly",
        author_email="farooq@teqniqly.com",
        description="A Python resilience library.",
        license="MIT",
        long_description=long_description,
        long_description_content_type="text/markdown",
        packages=setuptools.find_namespace_packages(exclude="tests"),
        include_package_data=True,
        keywords=["retry", "resilient", "fault", "handling"],
        install_requires=[],
        test_suite="tests",
        platforms="Platform Independent",
        package_data={"teqniqly-resilient": ["LICENSE", "README.md"]},
        classifiers=[
            "Development Status :: 4 - Beta",
            "Intended Audience :: Developers",
            "Programming Language :: Python :: 3.5",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        python_requires=">=3.5",
    )

    # Pop back to the original directory.
    os.chdir(cwd)


if __name__ == "__main__":
    main()
