import sys
import os
import enum

nytimes_com = '''
This New Liquid Is Magnetic, and Mesmerizing

Scientists have created "soft" magnets that can flow 
and change shape, and that could be a boon to medicine 
and robotics. (Source: New York Times)


Most Wikipedia Profiles Are of Men. This Scientist Is Changing That.

Jessica Wade has added nearly 700 Wikipedia biographies for
 important female and minority scientists in less than two 
 years.

'''

bloomberg_com = '''
The Space Race: From Apollo 11 to Elon Musk

It's 50 years since the world was gripped by historic images
 of Apollo 11, and Neil Armstrong -- the first man to walk 
 on the moon. It was the height of the Cold War, and the charts
 were filled with David Bowie's Space Oddity, and Creedence's 
 Bad Moon Rising. The world is a very different place than 
 it was 5 decades ago. But how has the space race changed since
 the summer of '69? (Source: Bloomberg)


Twitter CEO Jack Dorsey Gives Talk at Apple Headquarters

Twitter and Square Chief Executive Officer Jack Dorsey 
 addressed Apple Inc. employees at the iPhone maker's headquarters
 Tuesday, a signal of the strong ties between the Silicon Valley giants.
i'''

class Page():

    def __init__(self, url, text):
        self.url = url
        self.text = text

    def get_url(self):
        return self.url

    def get_text(self):
        return self.text


class Status(enum.Enum):
    ok = 1
    error = 2


class Browser():
    error_message = "Error"

    def load_page(self, str_input, directory, page):
        self.create_file(str_input, directory, page)
        return Status.ok, page.get_text()

    @staticmethod
    def create_directory(directory):
        parent_dir = os.getcwd()
        path = os.path.join(parent_dir, directory)
        if os.path.isdir(path):
            pass
        else:
            os.mkdir(path)
        return path

    @staticmethod
    def create_file(str_input, directory, page):
        path = self.create_directory(directory)
        dot = "."
        file_name = os.path.join(path, page.get_url().split(dot)[0])
       # if not os.path.isfile(file_name):
        with open(file_name, "w") as f:
            f.write(page.get_text())

    def get_error_message(self):
        return self.error_message


def main():
    urls = {"bloomberg.com": bloomberg_com, "nytimes.com": nytimes_com}
    browser = Browser()
    args = sys.argv
    directory = args[-1]
    browser.create_directory(directory)
    str_input = ""
    exit_from_program = "exit"
    while str_input != exit_from_program:
        str_input = input()
        if str_input in urls:
            page = Page(str_input, urls.get(str_input))
            status, value = browser.load_page(str_input, directory, page)
            if value is not None:
                print(value)
            if status is Status.error:
                continue
        else:
            print(browser.error_message)
            continue


main()
