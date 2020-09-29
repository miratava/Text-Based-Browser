import sys
import os
import enum
import requests


class Status(enum.Enum):
    ok = 1
    error = 2
    exit = 3


class Browser:
    error_message = "Error"

    def __init__(self):
        self.pages = []

    def load_page(self, directory, page):
        file_name = self.create_file(directory, page)
        self.pages.append(file_name)
        return Status.ok, page.text

    @staticmethod
    def create_directory(directory):
        parent_dir = os.getcwd()
        path = os.path.join(parent_dir, directory)
        if os.path.isdir(path):
            pass
        else:
            os.mkdir(path)
        return path

    def create_file(self, directory, page):
        path = self.create_directory(directory)
        dot = "."
        file_name = os.path.join(path, dot.join(page.url.split(dot)[:-1]))
        if not os.path.isfile(file_name):
            with open(file_name, "w") as f:
                f.write(page.text)
        return file_name

    def process_input_data(self, directory, str_input):
        command_exit = "exit"
        command_back = "back"
        if str_input == command_exit:
            return Status.exit, None
        if str_input == command_back:
            return self.go_back()
        page = requests.get(str_input)
        if page.status_code == requests.codes.ok:
            return self.load_page(directory, page)
        return Status.error, page.status_code

    def go_back(self):
        page_in_stack = -2
        if len(self.pages) <= 1:
            return Status.ok, None
        else:
            with open(self.pages.pop(page_in_stack)) as f:
                return Status.ok, f.read()


def main():
    browser = Browser()
    args = sys.argv
    directory = args[-1]
    str_input = ""
    exit_from_program = "exit"
    while str_input != exit_from_program:
        str_input = input()
        http = "http://"
        if not str_input.startswith(http):
            str_input = http + str_input
        status, value = browser.process_input_data(directory, str_input)
        if value is not None:
            print(value)
        elif status is Status.error:
            continue
        elif status is Status.exit:
            break


main()
