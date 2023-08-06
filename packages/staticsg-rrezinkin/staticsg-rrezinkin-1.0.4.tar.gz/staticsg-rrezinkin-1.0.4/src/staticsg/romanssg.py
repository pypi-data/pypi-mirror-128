"""
Main Static Site Functionality
"""
# Import Statements
import sys
import os
import fnmatch
import argparse
from roman_ssg_util import conversion_func_file, conversion_func_folder, configFileRead

# Main Logic
def main(arguments):
    # Local Variables
    parser = argparse.ArgumentParser(description="Roman Static Site Generator")
    parser.add_argument("--input", "-i", help="Specify input file")
    parser.add_argument(
        "--version", "-v", action="version", version="1.0.2", help="Show version"
    )
    parser.add_argument("-o", "--output", help="Specify a custom output destination")
    parser.add_argument(
        "-l", "--lang", help="Specify a custom HTML language", default="en-CA"
    )
    parser.add_argument(
        "-c", "--config", help="Introduce a config file with specific configurations"
    )
    arguments = parser.parse_args(arguments)

    isCustomDirectory = False
    workingDirectoryPath = os.getcwd()
    distFolder = workingDirectoryPath + "/dist"
    arrayOfFiles = []

    if arguments.config is not None:
        input, lang = configFileRead(arguments.config)
    else:
        input = arguments.input
        lang = arguments.lang

    if arguments.output:
        outputDirectory = arguments.output
        isCustomDirectory = True
        print("Output Directory has been changed to: " + arguments.output)
        if os.path.isdir(input):
            print("Working on Directory: " + input)
            for i in os.listdir(input):
                if fnmatch.fnmatch(i, "*.txt") or fnmatch.fnmatch(i, "*.md"):
                    arrayOfFiles.append(i)
            conversion_func_folder(
                lang,
                input,
                isCustomDirectory,
                arrayOfFiles,
                outputDirectory,
                distFolder,
            )
        else:
            print("Working on a File")
            arrayOfFiles.append(input)
            conversion_func_file(
                lang, isCustomDirectory, arrayOfFiles, outputDirectory, distFolder
            )
    else:
        if os.path.isdir(input):
            print("Working on Directory: " + input)
            for i in os.listdir(input):
                if fnmatch.fnmatch(i, "*.txt") or fnmatch.fnmatch(i, "*.md"):
                    arrayOfFiles.append(i)
            conversion_func_folder(
                lang,
                input,
                isCustomDirectory,
                arrayOfFiles,
                "",
                distFolder,
            )
        else:
            print("Working on a File")
            arrayOfFiles.append(input)
            conversion_func_file(lang, isCustomDirectory, arrayOfFiles, "", distFolder)


if __name__ == "__main__":
    main(sys.argv[1:])
