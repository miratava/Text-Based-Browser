import sys
import os
import enum

nytimes_com = '''
This New Liquid Is Magnetic, and Mesmerizing

Scientists have created “soft” magnets that can flow 
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
 addressed Apple Inc. employees at the iPhone maker’s headquarters
 Tuesday, a signal of the strong ties between the Silicon Valley giants.
i'''

class Page():

    def __init__(self, url, text):
        self.url = url
        self.text = text

    def get_url(self):
        return self.url

    def get_text(self):
        return  self.text


class Status(enum.Enum):
    ok = 1
    error = 2


class Browser():
    error_message = "Error"

    def is_validate_input(self, str_input):
        dot = "."
        if dot in str_input:
            return True
        return False

    def is_page_exist(self, str_input, page: Page):
        if str_input == page.get_url():
            return True
        return False

    def load_page(self, str_input, directory, page: Page):
        if self.is_validate_input(str_input):
            self.create_file(str_input, directory, page)
            if self.is_page_exist(str_input, page):
                return Status.ok, page.get_text()
        return Status.error, self.error_message

    @staticmethod
    def create_file(str_input, directory, page: Page):
        dot = "."
        try:
            os.mkdir(directory)
        except FileExistsError:
            pass
        file_name = page.get_url().split(dot)[0]
        if not os.path.exists(directory + "\\" + file_name):
            with open(file_name, "w") as f:
                f.write(page.get_text())


def main():
    urls = {"bloomberg.com": bloomberg_com, "nytimes.com": nytimes_com}
    browser = Browser()
    args = sys.argv
    directory = args[-1]
    input_str = ""
    exit_from_program = "exit"
    while input_str != exit_from_program:
        input_str = input()
        for item in urls.items():
            page = lambda x, y : Page(item[0], item[1])
            status, value = browser.load_page(url, directory, page)
            if value is not None:
                print(value)
            if status is Status.error:
                continue


main()
>>>>>>> Added classes
