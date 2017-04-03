"""
Utility to populate a Git repo with the basic requritments to start working
on a project

Author: Matthew Feickert <feickert@cern.ch>
Date: 2017-03-31
"""
import os
import subprocess
import sys
import glob
import argparse
# TODO: Use GitPython https://github.com/gitpython-developers/GitPython
# import git


def check_for(file_name):
    """
    Checks the dir path for if the file exists

    Args:
        file_name (str): the name of the file to look for

    Returns:
        bool:
            True: if the file exists
            False: if the file doesn't exist
    """
    # TODO: Make this only go one level deep
    yes = subprocess.check_output(
        "find -iname " + file_name, shell=True).splitlines()[0]
    if subprocess.check_output("find -iname " + file_name, shell=True):
        return True
    else:
        return False


def check_if_git_repo(args):
    # Add Python 2.7 support (begrudgingly)
    if sys.version_info < (3, 0):
        if not glob.glob(os.path.dirname(args.project_dir) + ".git"):
            print("This is not a git repo.\n")
            response = raw_input(
                "Would you like to make it one? [Y/n] ").lower()
            if response == 'yes' or response == 'y':
                print("git init")
                subprocess.call("git init", shell=True)
            elif response == 'no' or response == 'n':
                response = raw_input(
                    "Do you want to proceed anyway? [Y/n] ").lower()
                if response == 'yes' or response == 'y':
                    return
                else:
                    exit()
            else:
                subprocess.call("clear", shell=True)
                check_if_git_repo(args)
    # Python 3 (standard)
    else:
        if not glob.glob(os.path.dirname(args.project_dir) + ".git"):
            print("This is not a git repo.\n")
            response = input("Would you like to make it one? [Y/n] ").lower()
            if response == 'yes' or response == 'y':
                print("git init")
                subprocess.call("git init", shell=True)
            elif response == 'no' or response == 'n':
                response = input(
                    "Do you want to proceed anyway? [Y/n] ").lower()
                if response == 'yes' or response == 'y':
                    return
                else:
                    exit()
            else:
                subprocess.call("clear", shell=True)
                check_if_git_repo(args)


def set_readme(args):
    project_name = os.path.split(args.project_dir.rstrip('/'))[1]
    if not glob.glob(os.path.dirname(args.project_dir) + "README.*"):
        file_name = os.path.join(os.path.dirname(args.project_dir),
                                 "README." + args.readme_extension)
        with open(file_name, "w+") as README:
            README.write("# " + project_name + "\n\n")
            README.write("Hello " +
                         subprocess.check_output(
                             "git config user.name", shell=True).splitlines()[0].decode("utf-8")
                         + "! Remember to write the README for project "
                         + project_name + ".\n")


def set_license(args):
    if not glob.glob(os.path.dirname(args.project_dir) + "LICENSE"):
        with open(os.path.join(os.path.dirname(args.project_dir), "LICENSE"), "w") as LICENSE:
            LICENSE.write("\n")


def make_src_dir(args):
    project_name = os.path.split(args.project_dir.rstrip('/'))[1]
    language = args.language.lower()
    if language == 'python':
        if not glob.glob(os.path.dirname(args.project_dir) + project_name):
            subprocess.call(
                "mkdir " + os.path.dirname(args.project_dir) + project_name, shell=True)
            return True
    elif language == 'cpp' or language == 'c++':
        if not glob.glob(os.path.dirname(args.project_dir) + "src"):
            subprocess.call(
                "mkdir " + os.path.dirname(args.project_dir) + "src", shell=True)
            return True
    return False


def setup_src(args):
    project_name = os.path.split(args.project_dir.rstrip('/'))[1]
    language = args.language.lower()
    if language == 'python':
        language_extension = '.py'
        subprocess.call(
            "touch " + os.path.dirname(args.project_dir) + project_name +
            "/__init__.py", shell=True)
        subprocess.call(
            "touch " + os.path.dirname(args.project_dir) + project_name +
            "/" + project_name + ".py", shell=True)
    elif language == 'cpp' or language == 'c++':
        subprocess.call(
            "touch " + os.path.dirname(args.project_dir) + "src/" + project_name + ".h", shell=True)
        subprocess.call(
            "touch " + os.path.dirname(args.project_dir) + "src/" + project_name + ".cpp", shell=True)
        subprocess.call(
            "touch " + os.path.dirname(args.project_dir) + "src/main.cpp", shell=True)


def make_tests_dir(args):
    if not glob.glob(os.path.dirname(args.project_dir) + "tests"):
        subprocess.call(
            "mkdir " + os.path.dirname(args.project_dir) + "tests", shell=True)
        return True
    else:
        return False


def setup_tests(args):
    project_name = os.path.split(args.project_dir.rstrip('/'))[1]
    language = args.language.lower()
    language_extension = '.py'  # default
    if language == 'cpp' or language == 'c++':
        language_extension = '.cpp'  # default
    subprocess.call(
        "touch " + os.path.dirname(args.project_dir) + "tests/test_"
        + project_name + language_extension, shell=True)


def make_build_dir(args):
    if not glob.glob(os.path.dirname(args.project_dir) + "build"):
        subprocess.call(
            "mkdir " + os.path.dirname(args.project_dir) + "build", shell=True)
        return True
    else:
        return False


def setup_build(args):
    # TODO: Fix cmake commands
    subprocess.call("cp " + os.path.dirname(args.project_dir) +
                    "files/CMakeLists.txt src/", shell=True)
    #subprocess.call("cd " + os.path.dirname(args.project_dir) + "build", shell=True)
    subprocess.call(
        "cd " + os.path.dirname(args.project_dir) + "build" + ";"
        + "cmake -G \"Unix Makefiles\" ../src/", shell=True)
    #subprocess.call("cmake -G \"Unix Makefiles\" ..", shell=True)


def make_git_commit(args):
    # TODO: Have this print to screen
    project_name = os.path.split(args.project_dir.rstrip('/'))[1]
    subprocess.check_output(["git", "status"])
    subprocess.check_output(["git", "add", "-A"])
    commit_message = "Setup Git project repo " + \
        project_name + " with setupRepo utility"
    subprocess.check_output(["git", "commit", "-m", commit_message])


def main():
    parser = argparse.ArgumentParser(
        description='Get input for setting up the repo')
    parser.add_argument('--readme', metavar='readme_extension', type=str,
                        dest="readme_extension", default="md",
                        help='the file extension for the README: {md, rtf}')
    parser.add_argument('--language', metavar='language', type=str,
                        dest="language", default="python",
                        help='the language the code will be written in: {C++, Python}')
    parser.add_argument('--project',  type=str,
                        dest="project_dir", default=os.path.split(os.getcwd())[1],
                        help='the project directory name that is being setup')
    args = parser.parse_args()

    check_if_git_repo(args)
    set_readme(args)
    set_license(args)

    if make_src_dir(args):
        setup_src(args)

    if make_tests_dir(args):
        setup_tests(args)

    if args.language != 'python':
        if make_build_dir(args):
            # setup_build(args)
            pass

    make_git_commit(args)


if __name__ == '__main__':
    main()
