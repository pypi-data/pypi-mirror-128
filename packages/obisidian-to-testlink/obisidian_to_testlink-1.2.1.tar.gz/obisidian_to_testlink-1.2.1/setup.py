"""
Documentation
-------------
v1.1.1: 不需要需求，也可以生成用例
v1.2.1: 支持gxtest格式

"""

from setuptools import setup, find_packages

long_description = __doc__

def main():
    setup(
        name="obisidian_to_testlink",
        description="Convert obisidian to TestLink xml",
        keywords="obisidian testlink testcase requirement",
        long_description=long_description,
        version="1.2.1",
        author="zhaobk",
        author_email="zhaobk@nationalchip.com",
        packages=find_packages(),
        package_data={},
        entry_points={
            'console_scripts':[
                'obstotestlink=obisidian_to_testlink.main:main',
                ]
            }
    )


if __name__ == "__main__":
    main()
