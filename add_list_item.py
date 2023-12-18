import sublime
import sublime_plugin
import re

class AddListItem(sublime_plugin.TextCommand):

    def run(self, edit):
        for region in self.view.sel():
            line_region = self.view.line(region)
            line_text = self.view.substr(line_region)
            match = re.search(r'^\s+?\S', line_text)
            if not match:
                self.view.window().run_command("insert", {"characters": "\n"})
                return
            i = match.end()
            line_indentation = line_text[0:i-1]
            line_symbol = line_text[i-1:i]
            checkbox = re.match(r'(\s*)\[.\]', line_text[i:])
            if checkbox:
                padding = " " * checkbox.end(1)
                line_symbol += padding + "[ ]"
            line_symbol += " "

            rest_of_line = sublime.Region(region.begin(), line_region.end())
            rest_of_string = self.view.substr(rest_of_line).rstrip()

            if rest_of_string:
                line_symbol = " " * len(line_symbol) # change to be inline but without symbol
            self.view.insert(edit, region.end(), "\n" + line_indentation + line_symbol)

class AddNumberedListItem(sublime_plugin.TextCommand):

    def run(self, edit):
        for region in self.view.sel():
            line_region = self.view.line(region)
            line_text = self.view.substr(line_region)
            match = re.match(r'^(\s*)(\d+)\.', line_text)
            if not match:
                self.view.window().run_command("insert", {"characters": "\n"})
                return
            line_indentation = match.group(1)
            line_number = int(match.group(2))
            line_symbol = str(line_number + 1) + ". "

            if line_number % 9 == 0:
                line_indentation = line_indentation[0:-2]

            rest_of_line = sublime.Region(region.begin(), line_region.end())
            rest_of_string = self.view.substr(rest_of_line).rstrip()

            if rest_of_string:
                line_symbol = " " * len(line_symbol) # change to be inline but without symbol
            self.view.insert(edit, region.end(), "\n" + line_indentation + line_symbol)
            self.cascade(edit, line_region)

    def cascade(self, edit, starting_region):
        print(starting_region)
        current_line_region = starting_region
        while False:
            pass

class MakeCurrentLineATask(sublime_plugin.TextCommand):

    def run(self, edit):
        print("doing it!")
        for region in self.view.sel():
            line_region = self.view.line(region)
            # TODO: Use current indentation
            #       Find the first non-space character and insert there instead.
            self.view.insert(edit, line_region.start(), "  - [ ] ")