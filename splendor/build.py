import os
import sys
import subprocess

def buildSourceFilesList(current_folder, verbose):
    build_directory = "build"
    source_files = []

    for root, dirs, files in os.walk(current_folder):
        for file in files:
            if file.endswith("build.py") or file.endswith("__main__.py"):
                continue
            if file.endswith(".py"):
                full_path = os.path.join(root, file)
                ouput_file = "{0}/{1}.cpp".format(build_directory, file[:-3])
                source_files.append(ouput_file)

                if not os.path.exists(ouput_file) or os.path.getmtime(full_path) > os.path.getmtime(ouput_file):
                    if verbose:
                        print("building: {0} to {1}".format(full_path, ouput_file))

                    if file == "main.py":
                        subprocess.call(["cython3", "-3", "--cplus", "-o", ouput_file, full_path, "--embed"])
                    else:
                        subprocess.call(["cython3", "-3", "--cplus", "-o", ouput_file, full_path])
                else:
                    if verbose:
                        print("skipping: {1} newer than {0}".format(full_path, ouput_file))
    
    return source_files

if len(sys.argv) > 1 and sys.argv[1] == "-v":
    verbose = True
else:
    verbose = False

source_files = buildSourceFilesList(".", verbose)
compile_cmd = ["gcc"] + source_files + ["-O2", "-I/usr/include/python3.7", "-L/usr/lib/python3.7/config-3.7m-x86_64-linux-gnu/", "-lpython3.7", "-o", "exe_splendor"]

if verbose:
    print(" ".join(compile_cmd))

subprocess.call(compile_cmd)

