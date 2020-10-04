import sys
import os
import enum
import requests
from bs4 import BeautifulSoup
from colorama import init, Fore, Style


class Status(enum.Enum):
    ok = 1
    error = 2
    exit = 3


class Browser:
    error_message = "Error"

    def __init__(self):
        self.pages = []
        self.directory_path = ""

    @staticmethod
    def is_valid_input(str_input):
        dot = "."
        if dot in str_input:
            return True
        return False

    def load_page(self, page, results):
        file_name = self.create_file(page, results)
        self.pages.append(file_name)
        os.chdir(os.path.dirname(self.directory_path))
        page_text = []
        for result in results:
            page_text.append(self.make_blue_href(result))
        return Status.ok, " ".join(page_text)

    def create_directory(self, directory):
        self.directory_path = os.path.join(os.getcwd(), directory)
        if os.path.isdir(self.directory_path):
            pass
        else:
            os.mkdir(self.directory_path)
        return Status.ok

    def create_file(self, page, results):
        os.chdir(self.directory_path)
        dot = "."
        slash = "/"
        third = 2
        www = "www"
        general_page_url = page.url.split(slash)[third]
        if www in general_page_url:
            general_page_url = general_page_url[len(www) + 1:]
        file_name = dot.join(general_page_url.split(dot)[:-1])
        with open(file_name, "w") as f:
            for result in results:
                f.write(result.text + "\n")
        return file_name

    def process_input_data(self, directory, str_input):
        command_exit = "exit"
        command_back = "back"
        self.create_directory(directory)
        if str_input == command_exit:
            return Status.exit, None
        if str_input == command_back:
            return self.go_back()
        if self.is_valid_input(str_input):
            http = "http://"
            if not str_input.startswith(http):
                str_input = http + str_input
            page = requests.get(str_input)
            if page.status_code == requests.codes.ok:
                results = self.do_parse_request(page)
                return self.load_page(page, results)
        return Status.error, self.error_message

    @staticmethod
    def do_parse_request(page):
        soup = BeautifulSoup(page.content, 'html.parser')
        return soup.find_all(['p', 'header' 'a', 'ul', 'ol', 'li'], recursive=True)

    @staticmethod
    def make_blue_href(tag):
        #a = tag.find('a')
        #if a != None:
        #    return tag.text + Fore.BLUE + a.text + Style.RESET_ALL
        if tag.find('a') != None:
            return  Fore.BLUE + tag.text + Style.RESET_ALL
        return tag.text

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
        status, value = browser.process_input_data(directory, str_input)
        if value is not None:
            print(value)
        elif status is Status.error:
            continue
        elif status is Status.exit:
            break


main()
