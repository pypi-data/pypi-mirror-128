#!/user/bin/env python3
# -*- coding: utf-8 -*-
"""
--------------------------------------
    Author:     JiChao_Song
    Date  :     2021/11/10 21:14
    Desc  :
--------------------------------------
"""
"""A setuptools based setup module.
See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
"""
import setuptools
import os

CUR_DIR = os.path.abspath(os.path.dirname(__file__))
README = os.path.join(CUR_DIR, "README.md")
with open("README.md", "r", encoding = 'utf-8') as fd:
    long_description = fd.read()

# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

"""
name - 项目的名称
version - 项目的版本。需要注意的是，PyPI上只允许一个版本存在，如果后续代码有了任何更改，再次上传需要增加版本号
author和author_email - 项目作者的名字和邮件
description - 项目的简短描述
long_description - 项目的详细描述，会显示在PyPI的项目描述页面。上面的例子里直接用了README.md中的内容做详细描述
long_description_content_type - 用于指定long_description的markup类型，上面的例子是markdown
url - 项目主页的URL，一般给出代码仓库的链接
packages - 指定最终发布的包中要包含的packages。上面的例子中find_packages() 会自动发现项目根目录下所有的packages，当然也可以手动指定package的名字
install_requires - 项目依赖哪些库，这些库会在pip install的时候自动安装
entry_points - 上面的例子中entry_points用来自动创建脚本，上面的例子在pip install安装成功后会创建tobe这个命令，直接可以在命令行运行，即执行 tobe:main
classifiers - 其他信息，一般包括项目支持的Python版本，License，支持的操作系统。上面的例子中，我们指定项目只能在Python 3上运行，使用MIT License，不依赖操作系统。关于classifiers的完整列表，可参考 https://pypi.org/classifiers/。
"""
setuptools.setup(
    # This is the name of your project. The first time you publish this
    # package, this name will be registered for you. It will determine how
    # users can install this project, e.g.:
    #
    # $ pip install sampleproject
    #
    # And where it will live on PyPI: https://pypi.org/project/sampleproject/
    #
    # There are some restrictions on what makes a valid project name
    # specification here:
    # https://packaging.python.org/specifications/core-metadata/#name
    # Required
    name = "platformTool",

    # Versions should comply with PEP 440:
    # https://www.python.org/dev/peps/pep-0440/
    #
    # For a discussion on single-sourcing the version across setup.py and the
    # project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    # Required
    version = "0.0.3",

    # This is a one-line description or tagline of what your project does. This
    # corresponds to the "Summary" metadata field:
    # https://packaging.python.org/specifications/core-metadata/#summary
    # Optional
    description="一个简单的工具集",

    # This is an optional longer description of your project that represents
    # the body of text which users will see when they visit PyPI.
    #
    # Often, this is the same as your README, so you can just read it in from
    # that file directly (as we have already done above)
    #
    # This field corresponds to the "Description" metadata field:
    # https://packaging.python.org/specifications/core-metadata/#description-optional
    # Optional
    long_description=long_description,

    # Denotes that our long_description is in Markdown; valid values are
    # text/plain, text/x-rst, and text/markdown
    #
    # Optional if long_description is written in reStructuredText (rst) but
    # required for plain-text or Markdown; if unspecified, "applications should
    # attempt to render [the long_description] as text/x-rst; charset=UTF-8 and
    # fall back to text/plain if it is not valid rst" (see link below)
    #
    # This field corresponds to the "Description-Content-Type" metadata field:
    # https://packaging.python.org/specifications/core-metadata/#description-content-type-optional
    # Optional
    long_description_content_type="text/markdown",

    # This should be a valid link to your project's main homepage.
    #
    # This field corresponds to the "Home-Page" metadata field:
    # https://packaging.python.org/specifications/core-metadata/#home-page-optional
    # Optional
    url="https://gitee.com/zhsjch/platform_tool.git",

    # This should be your name or the name of the organization which owns the
    # project.
    # Optional
    author="JiChaoSong",

    # This should be a valid email address corresponding to the author listed
    # above.
    # Optional
    author_email="jichaosong@outlook.com",

    # You can just specify package directories manually here if your project is
    # simple. Or you can use find_packages().
    #
    # Alternatively, if you just want to distribute a single Python file, use
    # the `py_modules` argument instead as follows, which will expect a file
    # called `my_module.py` to exist:
    #
    #   py_modules=["my_module"],
    #
    # Required
    # packages = ["platform_tool"],
    packages=setuptools.find_packages(),

    # This field lists other packages that your project depends on to run.
    # Any package you put here will be installed by pip when your project is
    # installed, so they must be valid existing projects.
    #
    # For an analysis of "install_requires" vs pip's requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    # Optional
    install_requires = [
        "PyYAML>=6.0",
        "loguru>=0.5.3",
        "httpx>=0.21.1",
    ],

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # `pip` to create the appropriate form of executable for the target
    # platform.
    #
    # For example, the following would provide a command called `sample` which
    # executes the function `main` from this package when invoked:
    # Optional
    entry_points={

    },

    # Specify which Python versions you support. In contrast to the
    # 'Programming Language' classifiers above, 'pip install' will check this
    # and refuse to install the project if the version does not match. If you
    # do not support Python 2, you can simplify this to '>=3.5' or similar, see
    # https://packaging.python.org/guides/distributing-packages-using-setuptools/#python-requires
    # Optional
    #python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, <4',

    # If there are data files included in your packages that need to be
    # installed, specify them here.
    #
    # If using Python 2.6 or earlier, then these have to be included in
    # MANIFEST.in as well.
    #package_data={  # Optional
    #    'sample': ['package_data.dat'],
    #},

    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages. See:
    # http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files
    #
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    # Optional
    #data_files=[('my_data', ['data/data_file'])],

    # Classifiers help users find your project by categorizing it.
    #
    # For a list of valid classifiers, see https://pypi.org/classifiers/
    # Optional
    classifiers=(
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        # These classifiers are *not* checked by 'pip install'. See instead
        # 'python_requires' below.
        'Programming Language :: Python :: 3.8',
    ),
)