#
# Swift Format.py
#
# AGPLv3 License
# Created by github.com/aerobounce on 2020/07/19.
# Copyright © 2020-2022, aerobounce. All rights reserved.
#

from fnmatch import fnmatch
from html import escape
from os import R_OK, access, path
from re import IGNORECASE, compile, sub
from subprocess import PIPE, Popen

from sublime import LAYOUT_BELOW, Edit, Phantom, PhantomSet, Region, View
from sublime import error_message as alert
from sublime import expand_variables, load_settings
from sublime_plugin import TextCommand, ViewEventListener

SETTINGS_FILENAME = "Swift Format.sublime-settings"
ON_CHANGE_TAG = "reload_settings"
UTF_8 = "utf-8"
PHANTOM_STYLE = """
<style>
    div.error-arrow {
        border-top: 0.4rem solid transparent;
        border-left: 0.5rem solid color(var(--redish) blend(var(--background) 30%));
        width: 0;
        height: 0;
    }
    div.error {
        padding: 0.4rem 0 0.4rem 0.7rem;
        margin: 0 0 0.2rem;
        border-radius: 0 0.2rem 0.2rem 0.2rem;
    }
    div.error span.message {
        padding-right: 0.7rem;
    }
    div.error a {
        text-decoration: inherit;
        padding: 0.35rem 0.7rem 0.45rem 0.8rem;
        position: relative;
        bottom: 0.05rem;
        border-radius: 0 0.2rem 0.2rem 0;
        font-weight: bold;
    }
    html.dark div.error a {
        background-color: #00000018;
    }
    html.light div.error a {
        background-color: #ffffff18;
    }
</style>
"""


def plugin_loaded():
    SwiftFormat.settings = load_settings(SETTINGS_FILENAME)
    SwiftFormat.reload_settings()
    SwiftFormat.settings.add_on_change(ON_CHANGE_TAG, SwiftFormat.reload_settings)


def plugin_unloaded():
    SwiftFormat.settings.clear_on_change(ON_CHANGE_TAG)


class SwiftFormat:
    settings = load_settings(SETTINGS_FILENAME)
    phantom_sets = {}
    shell_command = ""
    last_valid_config_path = ""
    format_on_save = True
    ignored_filenames = []
    show_error_inline = True
    scroll_to_error_point = True
    config_paths = []

    @classmethod
    def reload_settings(cls):
        cls.shell_command = cls.settings.get("swiftformat_bin_path")
        cls.last_valid_config_path = ""
        cls.format_on_save = cls.settings.get("format_on_save")
        cls.ignored_filenames = cls.settings.get("ignored_filenames")
        cls.show_error_inline = cls.settings.get("show_error_inline")
        cls.scroll_to_error_point = cls.settings.get("scroll_to_error_point")
        cls.config_paths = cls.settings.get("config_paths")

    @classmethod
    def update_phantoms(cls, view: View, stderr: str, error_point: int):
        view_id = view.id()

        if view_id not in cls.phantom_sets:
            cls.phantom_sets[view_id] = PhantomSet(view, str(view_id))

        # Create Phantom
        def phantom_content():
            # Remove unneeded text from stderr
            error_message = stderr.replace("error: ", "")
            return (
                "<body id=inline-error>"
                + PHANTOM_STYLE
                + '<div class="error-arrow"></div><div class="error">'
                + '<span class="message">'
                + escape(error_message, quote=False)
                + "</span>"
                + "<a href=hide>"
                + chr(0x00D7)
                + "</a></div>"
                + "</body>"
            )

        new_phantom = Phantom(
            Region(error_point, view.line(error_point).b),
            phantom_content(),
            LAYOUT_BELOW,
            lambda _: view.erase_phantoms(str(view_id)),
        )
        # Store Phantom
        cls.phantom_sets[view_id].update([new_phantom])

    @staticmethod
    def parse_error_point(view: View, stderr: str):
        digits = compile(r"\d+|$").findall(stderr)
        if not stderr or not digits[0]:
            return
        line = int(digits[0]) - 1
        column = int(digits[1] or 1) - 1
        return view.text_point(line, column)

    @staticmethod
    def is_readable_file(filepath: str):
        if path.isfile(filepath):
            return access(filepath, R_OK)
        return False

    @staticmethod
    def shell(command: str, stdin: str):
        with Popen(command, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE) as shell:
            # Print command executed to the console of ST
            print("[Swift Format] Popen:", command)
            # Nil check to suppress linter
            if not shell.stdin or not shell.stdout or not shell.stderr:
                return ("", "")
            # Write target_text into stdin and ensure the descriptor is closed
            shell.stdin.write(stdin.encode(UTF_8))
            shell.stdin.close()
            # Read stdout and stderr
            return (shell.stdout.read().decode(UTF_8), shell.stderr.read().decode(UTF_8))

    @classmethod
    def execute_format(cls, view: View, edit: Edit):
        # Get entire string
        entire_region = Region(0, view.size())
        entire_text = view.substr(entire_region)

        # Early return
        if not entire_text:
            return

        # Base command
        shell_command = cls.shell_command

        # Use cached path
        if cls.config_paths and cls.is_readable_file(cls.last_valid_config_path):
            shell_command += ' --config "{}"'.format(cls.last_valid_config_path)

        # Find and use config file
        elif cls.config_paths:
            cls.last_valid_config_path = ""
            active_window = view.window()

            if active_window:
                variables = active_window.extract_variables()

                # Iterate directories to find config file
                for path_candidate in cls.config_paths:
                    config_file = expand_variables(path_candidate, variables)

                    if cls.is_readable_file(config_file):
                        shell_command += ' --config "{}"'.format(config_file)
                        cls.last_valid_config_path = config_file
                        break

        # Config file is not in use anymore
        else:
            cls.last_valid_config_path = ""

        # Execute shell and get output
        output = cls.shell(shell_command, entire_text)
        stdout = output[0]
        stderr = output[1].replace("Running SwiftFormat...\n", "")
        stderr = sub("SwiftFormat completed successfully.\n", "", stderr, flags=IGNORECASE)
        stderr = stderr.replace("\n", "")

        # Present alert for 'command not found'
        if "command not found" in stderr:
            alert("Swift Format\n" + stderr)
            return

        # Parse possible error point
        error_point = cls.parse_error_point(view, stderr)

        # Present alert for other errors
        if stderr and not error_point:
            alert("Swift Format\n" + stderr)
            return

        # Print parsing error
        if error_point:
            print("[Swift Format]", stderr)

        # Store original viewport position
        original_viewport_position = view.viewport_position()

        # Replace with the result only if no error has been caught
        if stdout and not stderr:
            view.replace(edit, entire_region, stdout)

        # Update Phantoms
        view.erase_phantoms(str(view.id()))
        if cls.show_error_inline and error_point:
            cls.update_phantoms(view, stderr, error_point)

        # Scroll to the syntax error point
        if cls.scroll_to_error_point and error_point:
            view.sel().clear()
            view.sel().add(Region(error_point))
            view.show_at_center(error_point)
        else:
            # Restore viewport position
            view.set_viewport_position((0, 0), False)
            view.set_viewport_position(original_viewport_position, False)


class GenerateConfigCommand(TextCommand):
    def run(self, edit, cwd: str):
        active_window = self.view.window()

        if not active_window:
            return

        cwd = active_window.extract_variables()[cwd]
        command = SwiftFormat.shell_command + ' --inferoptions "{}"'.format(cwd)
        output = SwiftFormat.shell(command, "")
        stdout = output[0]
        stderr = output[1]

        if "Failed to to infer options" in stderr:
            alert("Swift Format\nFailed to to infer options.")
            return

        if "Options inferred from" in stderr:
            stdout = stdout.replace(" --", "\n--")
            new_view = active_window.new_file()
            new_view.set_name(".swiftformat")
            try:
                new_view.assign_syntax("scope:source.genconfig")
            except:
                pass
            new_view.insert(edit, 0, stdout)
            new_view.insert(edit, 0, "# Inferred from {}\n".format(cwd))


class SwiftFormatCommand(TextCommand):
    def run(self, edit):
        SwiftFormat.execute_format(self.view, edit)


class SwiftFormatListener(ViewEventListener):
    def on_pre_save(self):
        active_window = self.view.window()

        if not active_window:
            return

        is_syntax_swift = "Swift" in self.view.settings().get("syntax")
        is_extension_swift = active_window.extract_variables()["file_extension"] == "swift"
        filename = active_window.extract_variables()["file_name"]

        if not (SwiftFormat.format_on_save and (is_syntax_swift or is_extension_swift)):
            return

        for ignored_filename in SwiftFormat.ignored_filenames:
            if fnmatch(filename, ignored_filename):
                return

        self.view.run_command("swift_format")

    def on_close(self):
        view_id = self.view.id()

        if view_id in SwiftFormat.phantom_sets:
            SwiftFormat.phantom_sets.pop(view_id)
