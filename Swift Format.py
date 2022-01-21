#!/usr/bin/env python
# coding: utf-8
#
# Swift Format.py
#
# AGPLv3 License
# Created by github.com/aerobounce on 2020/07/19.
# Copyright © 2020 to Present, aerobounce. All rights reserved.
#

import html
import os
import re
from subprocess import PIPE, Popen

import sublime
import sublime_plugin

SETTINGS_FILENAME = "Swift Format.sublime-settings"
PHANTOM_SETS = {}
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


def is_file_readable(path):
    return os.path.isfile(path) and os.access(path, os.R_OK)


def update_phantoms(view, stderr, region):
    view_id = view.id()

    view.erase_phantoms(str(view_id))
    if view_id in PHANTOM_SETS:
        PHANTOM_SETS.pop(view_id)

    if not stderr or not "Unexpected" in stderr:
        return

    if not view_id in PHANTOM_SETS:
        PHANTOM_SETS[view_id] = sublime.PhantomSet(view, str(view_id))

    # Extract line and column
    digits = re.compile(r"\d+|$").findall(stderr)
    line = int(digits[0]) - 1
    column = int(digits[1]) - 1

    if region:
        line += view.rowcol(region.begin())[0]

    # Format error message
    pattern = "Running SwiftFormat...\nerror: "
    stderr = re.compile(pattern).sub("", stderr)

    # Func to hook with `on_navigate`
    def erase_phantom(self):
        view.erase_phantoms(str(view_id))

    phantoms = []
    point = view.text_point(line, column)
    region = sublime.Region(point, view.line(point).b)
    phantoms.append(
        sublime.Phantom(
            region,
            (
                "<body id=inline-error>"
                + PHANTOM_STYLE
                + '<div class="error-arrow"></div><div class="error">'
                + '<span class="message">'
                + html.escape(stderr, quote=False)
                + "</span>"
                + "<a href=hide>"
                + chr(0x00D7)
                + "</a></div>"
                + "</body>"
            ),
            sublime.LAYOUT_BELOW,
            on_navigate=erase_phantom,
        )
    )
    PHANTOM_SETS[view_id].update(phantoms)

    # Scroll to the syntax error point
    if sublime.load_settings(SETTINGS_FILENAME).get("scroll_to_error_point"):
        view.sel().clear()
        view.sel().add(sublime.Region(point))
        view.show_at_center(point)


def swiftformat(view, edit, use_selection):
    # Load settings file
    settings = sublime.load_settings(SETTINGS_FILENAME)

    # Build command to execute
    command = ""
    settings_keys = [
        "swiftformat_bin_path",
        "use_config_file",
        "swiftversion",
        "rules",
        "disable",
        "options",
        "raw_options",
    ]

    # Parse settings
    for key in settings_keys:
        value = settings.get(key)

        if value:
            # Binary path
            if key == "swiftformat_bin_path":
                command += "{}".format(value)

            # Config file
            elif key == "use_config_file":
                # Extract Sublime window's variables
                variables = view.window().extract_variables()
                # Iterate directories to find config file
                for candidate in settings.get("config_paths"):
                    config_file = sublime.expand_variables(candidate, variables)
                    if is_file_readable(config_file):
                        command += ' --config "{}"'.format(config_file)
                        break

            # Formatting options
            elif key == "options":
                for (k, v) in settings.get(key).items():
                    if v:
                        command += ' --{0} "{1}"'.format(k, v)

            # Raw options
            elif key == "raw_options":
                for v in settings.get(key):
                    if v:
                        command += " {}".format(v)

            # CLI options
            else:
                command += ' --{0} "{1}"'.format(key, value)

    #
    # Execute Format
    #
    def format_text(target_text, selection, region):
        # If string is empty, just return
        if not target_text:
            return

        # Print command to be executed to the console of ST
        print("Swift Format executed command: {}".format(command))

        # Open subprocess with the command
        with Popen(command, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE) as popen:
            # Write selection into stdin, then ensure the descriptor is closed
            popen.stdin.write(target_text.encode("utf-8"))
            popen.stdin.close()

            # Read stdout and stderr
            stdout = popen.stdout.read().decode("utf-8")
            stderr = popen.stderr.read().decode("utf-8")

            # Catch some keywords in stderr
            command_succeeded = "successfully" in stderr
            syntax_error = "Unexpected" in stderr

            # Replace with the result only if no error has been caught
            if command_succeeded:
                view.replace(edit, selection, stdout)

            # Present alert: `swiftformat` not found
            if "not found" in stderr:
                sublime.error_message(
                    "Swift Format\n"
                    + stderr
                    + "Specify absolute path to 'swiftformat' in the settings"
                )
                return command_succeeded

            # Present alert: Unknown error
            if not command_succeeded and not syntax_error:
                sublime.error_message("Swift Format\n" + stderr)
                return command_succeeded

            # Update Phantoms
            update_phantoms(view, stderr, region)

            return command_succeeded

    # Store original viewport position
    original_viewport_position = view.viewport_position()

    # Prevent needles iteration as much as possible
    has_selection = any([not r.empty() for r in view.sel()])
    if (settings.get("format_selection_only") or use_selection) and has_selection:
        for region in view.sel():
            if region.empty():
                continue

            # Break at the first error
            if not format_text(view.substr(region), region, region):
                break

    else:
        # Don't format entire file when use_selection is true
        if use_selection:
            return

        # Use entire region/string of view
        selection = sublime.Region(0, view.size())
        target_text = view.substr(selection)
        format_text(target_text, selection, None)

    # Restore viewport position only if it's appropriate
    if PHANTOM_SETS and sublime.load_settings(SETTINGS_FILENAME).get("scroll_to_error_point"):
        return

    view.set_viewport_position((0, 0), False)
    view.set_viewport_position(original_viewport_position, False)


class SwiftFormatCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        swiftformat(self.view, edit, False)


class SwiftFormatSelectionCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        swiftformat(self.view, edit, True)


class SwiftFormatListener(sublime_plugin.ViewEventListener):
    def on_pre_save(self):
        is_syntax_swift = "Swift" in self.view.settings().get("syntax")
        is_ext_swift = (
            self.view.window().extract_variables()["file_extension"] == "swift"
        )

        if is_syntax_swift or is_ext_swift:
            if sublime.load_settings(SETTINGS_FILENAME).get("format_on_save"):
                self.view.run_command("swift_format")

    def on_close(self):
        view_id = self.view.id()
        if view_id in PHANTOM_SETS:
            PHANTOM_SETS.pop(view_id)
