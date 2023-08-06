"""
Utility Static Site Functionality
"""
import os
import shutil
import markdown
from json.decoder import JSONDecodeError
import json


def get_local_files(array_of_files):
    """Get local files"""
    localArr = []
    for i in array_of_files:
        if os.name == "posix":
            temp = os.getcwd() + "/" + str(i)
        else:
            temp = os.getcwd() + "\\" + str(i)
        localArr.append(temp)
    return localArr


def create_index_page(hmtl_lang, previous_filename_arr):
    """Create Index HTML Page"""
    counter = 1
    with open("index.html", "w", encoding="utf-8") as indexPage:
        indexPage.write("<!doctype html>\n")
        indexPage.write('<html lang="' + hmtl_lang + '">\n')
        indexPage.write("<head>\n")
        indexPage.write('\t<meta charset="utf-8">\n')
        indexPage.write("\t<title>" + "Index" + "</title>\n")
        indexPage.write(
            '\t<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        )
        indexPage.write("</head>\n")
        indexPage.write("<body>\n")
        for name in previous_filename_arr:
            linkString = f'<a href="./{name}.html">{counter}. {name}</a><br>'
            indexPage.write(str(linkString))
            counter += 1


def write_to_file(html_lang, a_file, file_counter, stricly_file_names):
    """Write to file Function"""
    # Read Current Existing File
    with open(a_file, "r", encoding="utf8") as originalFile:  # Read existing file
        originalFileName, end = os.path.splitext(
            stricly_file_names[file_counter]
        )  # Cut off the extension of the file
        temp = originalFile.read().splitlines()
    checkForTheme = temp

    # Create new File under html Extension, and open file.
    with open(originalFileName + ".html", "w", encoding="utf-8") as newFile:
        with open(originalFileName + ".html", "a", encoding="utf-8") as newFile:
            # Write main html section
            newFile.write("<!doctype html>\n")
            newFile.write('<html lang="' + html_lang + '">\n')
            newFile.write("<head>\n")
            newFile.write('\t<meta charset="utf-8">\n')
            newFile.write("\t<title>" + originalFileName + "</title>\n")
            newFile.write(
                '\t<meta name="viewport" content="width=device-width, initial-scale=1">\n'
            )
            for i in checkForTheme:
                if i.startswith("theme"):
                    if "dark" in i:
                        create_css_file(True)
                        newFile.write(
                            '\t<link rel="stylesheet" href="main.css" type="text/css">\n'
                        )
                        temp.pop(0)
            newFile.write("</head>\n")
            newFile.write("<body>\n")
            # Bulk of Main Logic of reading file and putting it into html file.
            for i in temp:  # Loop through the file we opened
                if i != "":  # We dont want <p> tags created for new lines
                    if end == ".txt":
                        newFile.write("\t<p>" + i + "</p>\n")
                    if end == ".md":
                        newFile.write("\t" + markdown.markdown(i) + "\n")
            newFile.write("</body>\n")
            newFile.write("</html>")


def create_css_file(has_theme_color):
    """Create CSS file"""
    if has_theme_color:
        with open("main.css", "w", encoding="utf-8") as cssFile:
            with open("main.css", "a", encoding="utf-8") as cssFile:
                cssFile.write("body{background-color: #2a2b2d}" + "\n")
                cssFile.write("p, h1, h2, h3, h4, li, ul, code{color: #fefefe}" + "\n")


def conversion_func_file(
    lang, is_custom_directory, array_of_files, custom_directory_path, dist_folder
):
    """Converting txt files"""
    # Local Variables
    localFiles = []
    striclyFileNames = array_of_files
    localFiles = get_local_files(array_of_files)
    fileCounter = 0
    print("\n~~~ SSG Compiling and Working! ~~~\n")
    # For File name convert into html and create new File.
    if is_custom_directory is False:
        try:
            if os.path.isdir(
                "dist"
            ):  # Check to see if dist exists, if it does, delete children and parent
                shutil.rmtree(dist_folder)
            os.mkdir(dist_folder)  # Try to create new dist folder
        except OSError as error:
            print("\n--- FAILURE ---")
            print(error)

        for i in localFiles:
            os.chdir(dist_folder)  # Change directories
            write_to_file(
                lang, i, fileCounter, striclyFileNames
            )  # Call the Write Function
            fileCounter += 1
        print("\n--- SUCCESS ---")
    else:
        for file in localFiles:
            os.chdir(custom_directory_path)  # Change directories
            write_to_file(
                lang, file, fileCounter, striclyFileNames
            )  # Call the Write Function
            fileCounter += 1
        print("\n--- SUCCESS ---")


def conversion_func_folder(
    lang,
    directory_name,
    is_custom_directory,
    array_of_files,
    custom_directory_path,
    dist_folder,
):
    """Converting files from within a folder"""
    # Local Variables
    localFiles = []
    striclyFileNames = array_of_files
    fileCounter = 0
    previousFileNameArr = []
    print("\n~~~ SSG Compiling and Working! ~~~\n")
    if (
        is_custom_directory is False
    ):  # Check to see if a custom output directory exists.
        try:
            if os.path.isdir(
                "dist"
            ):  # Check to see if dist exists, if it does, delete children and parent
                shutil.rmtree(dist_folder)
        except OSError as error:
            print("\n--- FAILURE ---:" + error)

        # Try to create new dist folder
        os.mkdir(dist_folder)
        # Change to specified Folder
        os.chdir(directory_name)
        directoryPath = os.getcwd()
        print(array_of_files)
        localFiles = get_local_files(array_of_files)
        # rint(localFiles)
        # Main Logic
        for file in localFiles:
            previousFileNameArr.append(
                os.path.splitext(striclyFileNames[fileCounter])[0]
            )
            os.chdir(dist_folder)
            write_to_file(lang, file, fileCounter, striclyFileNames)
            fileCounter += 1
            os.chdir(directoryPath)

        # Create Custom Index html page with links to all the created files
        os.chdir(dist_folder)
        create_index_page(lang, previousFileNameArr)
        print("\n--- SUCCESS ---")
    else:
        # Change to specified Folder
        os.chdir(directory_name)

        # Gather local files and convert them into usable paths
        localFiles = get_local_files(array_of_files)

        # Main logic
        for file in localFiles:
            directoryPath = os.getcwd()
            previousFileNameArr.append(
                os.path.splitext(striclyFileNames[fileCounter])[0]
            )
            tempCustomDirectoryPath = os.path.join("../", custom_directory_path)
            os.chdir(tempCustomDirectoryPath)
            write_to_file(lang, file, fileCounter, striclyFileNames)
            fileCounter += 1
            os.chdir(directoryPath)

        # Create Custom Index html page with links to all the created files
        os.chdir(tempCustomDirectoryPath)
        create_index_page(lang, previousFileNameArr)
        print("\n--- SUCCESS ---")


def configFileRead(config):
    """Configuration File Interpreter"""
    try:
        with open(config, "rb") as f:
            try:
                config = json.load(f)
                for i in config:
                    if i == "i" or i == "input":
                        input = config[i]
                    if i == "l" or i == "lang":
                        lang = config[i]
                    if input == "":
                        print("No input file specified!")
                        exit(1)
                return input, lang
            except JSONDecodeError:
                print("Invalid JSON")
                exit(1)
    except FileNotFoundError:
        print("Config file not found")
        exit(1)
