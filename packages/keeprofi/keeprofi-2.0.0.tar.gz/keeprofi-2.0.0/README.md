# KEEPROFI

Fast rofi drun menu for keepass database

## Installation

### aur: `keeprofi`

### pip: `keeprofi`

System dependencies:

* `rofi`
* `xclip` - copy password in clipboard
* system keyring(optional)

## Usage

0. Bind and press shortcut for `keeprofi`
1. Find keepass database file
2. Type the master password for your keepass database
3. Select password

	* Press `Enter` for default action(copy password in clipboard)
	* `Ctrl+Enter` - for additional action(type password in active window)
	* `Shift+Enter` - for open password attributes menu where you can select any attr with `Enter` or `Ctrl+Enter`

## Features

* Saves last opened `*.kdb` path
* Saves last `*.kdb` master password in system keyring(disabled by default)
* Desktop notifications with log and error messages
* `Ctrl+h` - switch hidden files

## Configuration

`XDG_CONFIG_HOME/keeprofi/config.json:`
```yaml
default_action: copy            # ['copy'|'type'] - default action that will done by 'Enter' pressing
save_masterpass: false          # [false|true|'1W2D3H4M5S'] - this flag controlles using keyring for `*.kdb` file password saving
keybinds:
  hidden: Control+h             # switch hidden files
  custom_action: Control+Return # custom action(typing by default)
  pass_attrs: Shift+Return      # password attributes menu open
notify_icons:
  success: keepassxc-dark
  fail: keepassxc-locked
dir_format: /{name}             # format of directories and keepass groups output
```

### save_masterpass

Can take 3 value:

* `false`(default) - `*.kdb` file password never saves in keyring
* `true` - `*.kdb` file password always saves in keyring
* `1W2D3H4M5S` - time interval format that specify how long password can be stored in keyring. Where:
	* W - weeks
	* D - days
	* H - hours
	* M - minutes
	* S - seconds

	any unit can be missed, but existing units should observe the specified order
