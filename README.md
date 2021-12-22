<h1 align="center">⚡️ Swift Format</h1>

<h3 align="center">Swift Formatter / Syntax Checker for Sublime Text 3</h3>

<p align="center">
    <img src="https://img.shields.io/badge/macOS-blue.svg" />
    <img src="https://img.shields.io/badge/Linux-yellow.svg" />
    <img src="https://img.shields.io/badge/Sublime Text-3-brightgreen.svg" />
</p>

<p align="center">
    <b>⚡️Blazingly Fast Formatting</b>
    <br>
    <b>❗️User Friendly Syntax Error Indication</a></b>
    <br>
    <br>
    <img src="https://user-images.githubusercontent.com/10491362/87870544-01507d00-c9e4-11ea-9fa1-1f7eb4b5bb20.gif" style="display: block; width: 100%;" />
</p>


# Install

- [Available via Package Control][packagecontrol]

1. `Package Control: Install Package`
2. Type `Swift Format` and Install

### Manual Install

1. Clone this repository to `.../Sublime Text 3/Packages/` (Note that target directory name has to be `Swift Format`)
2. Ready (Restart Sublime Text if the package is not recognized)

### Requirements

`swiftformat`

- Available via Homebrew `brew install swiftformat` (For more details, visit: [nicklockwood/SwiftFormat][swiftformat])
- macOS users: If your shell have `PATH` to `swiftformat` you are ready.
- If above is not the case, specify the `swiftformat_bin_path` in the settings:

```JavaScript
{
    "swiftformat_bin_path": "PATH to swiftformat"
}
```


# Commands

**Command** is the name of the command you can use for **Key-Bindings**.

| Caption                                   | Command                         | Default Key Bindings |
| ----------------------------------------- | ------------------------------- | -------------------- |
| <kbd>Swift Format: Format</kbd>           | `swift_format`                  | None                 |
| <kbd>Swift Format: Format Selection</kbd> | `swift_format_selection`        | None                 |
| <kbd>Swift Format: Settings</kbd>         | N/A                             | None                 |


# Settings

By default, `swiftversion` is not specified. It's recommended to specify the version — some rules will be omitted unless it's specified.

```javascript
{
    /*** Swift Format Settings ***/
    "swiftformat_bin_path": "swiftformat",
    "format_on_save": true,         // Invoke "Swift Format: Format" command on save
    "format_selection_only": false, // Entire file will be used if no selection available
    "scroll_to_error_point": true,  // Scroll to the point syntax error occured
    "use_config_file": true,        // Find config file and use if found
    "config_paths": [               // Paths to find a config file
        "${project_path}/.swiftformat",
        "${file_path}/.swiftformat",
        "${folder}/.swiftformat"
    ],

    /*** SwiftFormat CLI Options ***/
    // • Use "rules" key to use specific rules only
    // • Use "disable" key to disable specific rules
    // • "swiftformat --rules" to see up-to-date rules
    "swiftversion": "", // The version of Swift used in the files being formatted
    "rules": "",        // The list of rules to apply.
    "disable": "",      // A list of format rules to be disabled (comma-delimited)

    /*** Formatting Options ***/
    // • Specify without hyphens
    // • "swiftformat --options" to see up-to-date options
    // • Example:
    //     "options": {
    //         "allman": "false",
    //         "ifdef": "no-indent"
    //     }
    "options": {},

    /*** Raw Options ***/
    "raw_options": []
}
```


# Acknowledgements

- [nicklockwood/SwiftFormat][swiftformat] — Swift Format for Sublime Text is powerd by `swiftformat`, the best Swift formatter available.
- [adael/SublimePhpCsFixer][phpcsfixer] — config-related logic idea is borrowed from `SublimePhpCsFixer`.


[swiftformat]: https://github.com/nicklockwood/SwiftFormat
[packagecontrol]: https://packagecontrol.io/packages/Swift%20Format
[phpcsfixer]: https://github.com/adael/SublimePhpCsFixer
