import re
import sublime
import sublime_plugin

class IncrementCommand(sublime_plugin.TextCommand):

    MONTHS = [
        "January", "February", "March", "April", "May", "June", 
        "July", "August", "September", "October", "November", "December"
    ]

    WEEKDAYS = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]

    def wrap(self, table, value, delta):
        current_index = table.index(value)
        new_index = (current_index + delta) % len(table)
        return table[new_index]

    def run(self, edit, delta):
        selection = self.view.sel()
        for region in selection:
            region_text = self.view.substr(region)
            result = region_text
            if region_text in IncrementCommand.MONTHS:
                result = self.wrap(IncrementCommand.MONTHS, region_text, delta)
            elif region_text in IncrementCommand.WEEKDAYS:
                result = self.wrap(IncrementCommand.WEEKDAYS, region_text, delta)
            else:
                try:
                    result = str(int(region_text) + delta)
                except Exception as e:
                    print(e)
            self.view.replace(edit, region, result)


class InsertRegionNumberCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        selection = self.view.sel()
        for i, region in enumerate(selection):
            region_number = str(i + 1)
            if region.empty():
                self.view.insert(edit, region.a, region_number)
            else:
                self.view.replace(edit, region, region_number)
