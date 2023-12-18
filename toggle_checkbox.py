import sublime
import sublime_plugin
import re

CHECKBOXES = ["[ ]", "[X]", "[-]"]

class ToggleCheckboxCommand(sublime_plugin.TextCommand):

    def run(self, edit, target):
        if target == "cancel":
            target_char = "-"
        else:
            target_char = "X"
        selection = self.view.sel()

        # This is a hack to avoid multiple selections on the same line from cancelling each other out.
        lines = {}
        for region in selection:
            line_region = self.view.line(region)
            line = self.view.substr(line_region)
            lines[line] = line_region
        # End Hack

        for line in lines:
            line_region = lines[line]
            if not any(True for x in CHECKBOXES if x in line):
                return
            index = -1
            found = False
            while not found:
                index = line.find("[", index+1)
                if line[index+1] in ["-", "X", " "] and line[index+2] == "]":
                    found = True
            checkbox_region = sublime.Region(line_region.a + index, line_region.a + index+3)
            if line[index+1] == target_char:
                self.view.replace(edit, checkbox_region, "[ ]")
            else:
                self.view.replace(edit, checkbox_region, "[%s]" % target_char)
            # TODO: propogate the checkbox status if necessary
            # TODO: continue propogation.
            # TODO: maybe future work can support multiline checkbox tasks


