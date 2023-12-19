import sublime
import sublime_plugin
import webbrowser


class OpenUrlUnderCursorCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        for region in self.view.sel():
            scope_region = self.view.extract_scope(region.begin())
            url = self.view.substr(scope_region)
            webbrowser.open_new_tab(url)
