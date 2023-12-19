import sublime
import sublime_plugin


class OpenUrlUnderCursorCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        for region in self.view.sel():
            scope_region = self.view.extract_scope(region.begin())
            url = self.view.substr(scope_region)
            self.view.window().run_command ("open_url", {"url": url})
