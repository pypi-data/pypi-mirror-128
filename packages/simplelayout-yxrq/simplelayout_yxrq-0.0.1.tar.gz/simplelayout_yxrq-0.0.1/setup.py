import setuptools

setuptools.setup(
    name="simplelayout_yxrq",
    version="0.0.1",
    author="Wang Wenhui",
    author_email="whwang@stu.pku.edu.cn",
    description="A small example package",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="scr"),
    install_requires=["simplelayout"],
    entry_points={
        'console_scripts': [
            'sample=3_simplelayout_package_yxrq.src.simplelayout.__main__:main',
        ]
    }
    )
