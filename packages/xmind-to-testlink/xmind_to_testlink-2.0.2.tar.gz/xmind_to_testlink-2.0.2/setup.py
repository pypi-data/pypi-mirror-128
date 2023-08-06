"""
Documentation
-------------
XmindToTestlink is a tool to help you convert xmindzen file to testlink recognized xml files,
then you can import it into testlink as test suite , test cases and requirement.

For more detail, please go to: https://github.com/DancePerth/XmindToTestlink

"""

from setuptools import setup, find_packages

long_description = __doc__

def main():
    setup(
        name="xmind_to_testlink",
        description="Convert xmindzen to TestLink xml",
        keywords="xmind testlink import converter testing testcase requirement",
        long_description=long_description,
        version="2.0.2",
        author="zhaobk",
        author_email="zhaobk@nationalchip.com",
        packages=find_packages(),
        package_data={},
        entry_points={
            'console_scripts':[
                'xmindtotestlink=xmind_to_testlink.main:main',
                ]
            }
    )


if __name__ == "__main__":
    main()
