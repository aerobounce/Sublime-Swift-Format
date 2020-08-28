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
    <img src="https://user-images.githubusercontent.com/10491362/87870544-01507d00-c9e4-11ea-9fa1-1f7eb4b5bb20.gif" style="display: block; width: 100%;" />
</p>


## 📜 Overview
- **[📦 Install](#-Install)**
- **[⚠️ Dependency](#%EF%B8%8F-dependency)**
- **[📝 Available Commands](#-Available-Commands)**
- **[🛠 Default Settings](#-Default-Settings)**
- **[🤝 Thank you](#-Thank-you)**


## 📦 Install

- [Available via Package Control][packagecontrol]
1. Package Control: Install Package
2. Type `Swift Format` and Install

#### Manual Install

1. Clone this repository as shown below (**Note that target directory name has to be `Swift Format`**)
2. You're ready (Restart Sublime Text if the package is not recognized)

```sh
cd "$HOME/Library/Application Support/Sublime Text 3/Packages"
git clone https://github.com/aerobounce/Sublime-Swift-Format.git "Swift Format"
```


## ⚠️ Dependency

- Swift Format does not work without <b><code>swiftformat</code></b> as this package utilizes the formatter.
    - You can install it via **Homebrew**: <b><code>brew install swiftformat</b></code>
    - For more details, visit: [nicklockwood/SwiftFormat][swiftformat]
- (macOS users) If your default shell have the <b><code>PATH</b></code> to <b><code>swiftformat</b></code> you can start using this plugin.
- If that is not the case, specify the **Absolute PATH** in the settings:

```JavaScript
{
    "swiftformat_bin_path": "PATH to swiftformat"
}
```


## 📝 Available Commands

| Caption                                   | Command                         | Default Key Bindings |
| ----------------------------------------- | ------------------------------- | -------------------- |
| <kbd>Swift Format: Format</kbd>           | `swift_format`                  | None                 |
| <kbd>Swift Format: Format Selection</kbd> | `swift_format_selection`        | None                 |

- **Command** is the name of the command you can use for **Key-Bindings**.
- Be aware that any manual modifications with `Format Selection` might be lost upon saving a file if `format_on_save` is `true`, which it is by default.


## 🛠 Default Settings

- By default, `swiftversion` is not specified. **It's recommended to specify the version.** Unless it's specified, some rules will be omitted.

```javascript
{
    /*
        Swift Format Settings
    */
    "swiftformat_bin_path": "swiftformat",
    "format_on_save": true,         // Invoke "Swift Format: Format" command on save
    "format_selection_only": false, // Entire file will be used if no selection available
    "scroll_to_error_point": true,  // Scroll to the point syntax error occured

    /*
        SwiftFormat CLI Options
            • To use only specific rules, use `rules` key.
            • To disable specific rules, use `disable` key.
            • To see up-to-date rules: `swiftformat --rules`
    */
    "swiftversion": "", // The version of Swift used in the files being formatted
    "rules": "",        // The list of rules to apply.
    "disable": "",      // A list of format rules to be disabled (comma-delimited)

    /*
        Formatting Options
            • Specify without doubled hyphens
            • To see up-to-date options: `swiftformat --options`
            • Example:
                "options": {
                    "allman": "false",
                    "ifdef": "no-indent"
                }
    */
    "options": {
    }
}
```


## 🤝 Thank you

- [nicklockwood/SwiftFormat][swiftformat] — Swift Format for Sublime Text is powerd by swiftformat, the best Swift formatter available.

[swiftformat]: https://github.com/nicklockwood/SwiftFormat
[packagecontrol]: https://packagecontrol.io/packages/Swift%20Format
