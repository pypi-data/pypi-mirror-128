import setuptools


setuptools.setup(name="simplelayout_LyuYanfang",
      version="1.0.0",
      author="LyuYanfang",
      author_email="lvyanfang@stu.pku.edu.cn",
      description="A sample Python project",
      package_dir={"": "src"},
      packages=setuptools.find_packages(where="src"),
      install_requires=["simplelayout"],
      entry_points={
            'console_scripts':[
                  'sample=3_simplelayout_package_LyuYanfang.src.simplelayout.__main__:main',
            ]
      }
      )