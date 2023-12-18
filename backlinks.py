import sublime
import sublime_plugin
import os

VALID_FILETYPES = [".md", ".note"] # TODO: Have this be a setting

class BackLinksCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        name = self.view.file_name()
        if not name:
            print("Not a saved file. Cannot have backlinks.")
            return
        results = self.find_backlinks(name.replace("\\", "/"))

        file_count = len(results)
        link_count = sum([len(results[file]) for file in results])

        new_view = self.view.window().new_file()
        new_view.set_name("Backlinks")
        header = "Backlinks for " + name + "\n\n"
        footer = "%d matches" % link_count
        if file_count > 0:
            footer += " across %d files" % file_count
        new_view.run_command("insert",{"characters": header})

        for file in results:
            new_view.run_command("insert",{"characters": file+":\n"})
            for link in results[file]:
                new_view.run_command("insert",{"characters": "    "+link+"\n"})

        new_view.run_command("insert",{"characters": "\n" + footer + "\n"})
        new_view.assign_syntax("BacklinkResults.sublime-syntax")
        new_view.set_scratch(True)
        # new_view.set_read_only(True)

    def find_backlinks(self, target_filepath: str) -> dict:
        # TODO: Search through every file (use find_all command?) for a link to the filename
        #       This can be [[filename]] or [[subpath/filename]]
        #       Both can also be [[filepath#anchor]] and/or [[filepath|link text]] as well
        backlinks = {}
        roots = self.view.window().folders()
        for directory in roots:
            # TODO: Setting for ignoring hidden folders (ones beginning with '.')
            # TODO: Setting for ignoring custom folders
            # TODO: Setting for not including entire path for results (only relative to the corresponding root directory)
            for root, dirs, files in os.walk(directory):
                for file in files:
                    if not any([file.endswith(ext) for ext in VALID_FILETYPES]):
                        continue
                    path = os.path.join(root, file).replace("\\", "/")
                    file_backlinks = self.find_backlinks_in_file(target_filepath, path)
                    if file_backlinks:
                        backlinks[path] = file_backlinks
        return backlinks

    def find_backlinks_in_file(self, target_filepath: str, filepath: str) -> list:
        target_path = os.path.splitext(target_filepath)[0]
        target = os.path.basename(target_path)
        target_regex = r"\[\[[\w\/]*" + target + r"(?:#.+?)?(?:\|.+?)?\]\]"
        print("Searching " + filepath + " for " + target)
        window = self.view.window()
        view = window.find_open_file(filepath)
        is_new_view = False
        if not view:
            view = window.open_file(filepath)
            is_new_view = True

        results = view.find_all(target_regex)

        # TODO: Make sure results are the right result
        
        results = [view.substr(region) for region in results]

        if is_new_view:
            view.close()
        return results
