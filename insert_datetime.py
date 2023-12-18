import sublime
import sublime_plugin
import datetime

class InsertTime(sublime_plugin.TextCommand):

    def run(self, edit):
        current_time = datetime.datetime.now().strftime("%H%M")
        for region in self.view.sel():
            if region.empty():
                self.view.insert(edit, region.a, current_time)
            else:
                self.view.replace(edit, region, current_time)
