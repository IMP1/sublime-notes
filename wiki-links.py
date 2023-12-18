import sublime
import sublime_plugin
import re
import os


LINK_REGEX = re.compile(r'\[\[.+?\]\]')
HEADER_PATTERN = r'^\s*#+\s%s\s*$'
VALID_FILETYPES = [".md", ".note"]  # TODO: Have this be a setting

class SeekToAnchor(sublime_plugin.EventListener):

    ignore_events = False
    anchor_string = None

    def on_load(self, view):
        if SeekToAnchor.ignore_events:
            return
        if not SeekToAnchor.anchor_string:
            return

        SeekToAnchor.ignore_events = True
        SeekToAnchor.seek(view, SeekToAnchor.anchor_string)
        SeekToAnchor.anchor_string = None
        SeekToAnchor.ignore_events = False

    @staticmethod
    def seek(view, anchor_string):
        anchor = HEADER_PATTERN % anchor_string.replace("_", r"\s")
        anchor_region = view.find(anchor, 0)
        if anchor_region:
            view.show_at_center(anchor_region)

class OpenFileCallable:

    def __init__(self, view, entries):
        self.view = view
        self.entries = entries

    def __call__(self, index) -> None:
        if index < 0:
            return
        entry = self.entries[index]
        link = entry.split("#")
        filepath = link[0]
        anchor = link[1] if len(link) > 1 else None
        if anchor:
            SeekToAnchor.anchor_string = anchor
        new_view = self.view.window().open_file(filepath)
        if anchor:
            SeekToAnchor.seek(new_view, SeekToAnchor.anchor_string)


class WikiLinksCommand(sublime_plugin.TextCommand):

    def is_visible(self, event=None) -> bool:
        if event:
            click_point = self.view.window_to_text((event["x"], event["y"]))
        else:
            click_point = self.view.sel()[0].begin()
        scope_text = self.view.substr(self.view.extract_scope(click_point))
        return bool(LINK_REGEX.match(scope_text))

    def run(self, edit, event=None) -> None:
        if event:
            click_point = self.view.window_to_text((event["x"], event["y"]))
            self.navigate_to_entry(self.get_entry_name(click_point))
        else:
            for region in self.view.sel():
                self.navigate_to_entry(self.get_entry_name(region.begin()))

    def get_entry_name(self, point) -> str:
        scope_region = self.view.extract_scope(point)
        return self.view.substr(scope_region)[2:-2]

    def navigate_to_entry(self, link_string) -> None:
        entries = self.find_entries(link_string)
        if not entries:
            new_view = self.view.window().new_file()
            new_view.set_name(link_string.split("|")[0].split("#")[0])
            return

        open_entry = OpenFileCallable(self.view, entries)
        if len(entries) > 1:
            self.view.window().show_quick_panel(entries, open_entry)
        else:
            open_entry(0)

    def find_entries(self, link_string) -> list:
        roots = self.view.window().folders()
        if len(roots) == 0:
            print("No folders are open to search wiki links in.")
            return []
        link = link_string.split("|")[0].split("#")
        filename = link[0]
        anchor = link[1] if len(link) > 1 else None
        entries = []
        for directory in roots:
            # TODO: Setting for ignoring hidden folders (ones beginning with '.')
            # TODO: Setting for ignoring custom folders
            for root, dirs, files in os.walk(directory):
                for file in files:
                    path = os.path.join(root, file).replace("\\", "/")
                    if any([path.endswith(filename + extension) for extension in VALID_FILETYPES]):
                        entries.append(path)
        if anchor:
            entries = [f + "#" + anchor for f in entries]
        return entries
