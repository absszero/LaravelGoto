# Laravel Goto for Sublime Text

Goto `*.blade.php`  or `Controller@Method` by `Alt`+`Left-Click`

![example](example.gif)

## Feature 

- Open Blade Template files *(EX. hello.blade.php)*

- Open Controller with method *(EX. \Namespace\Controller.php@Method)*

- Open Static files (*EX. hello.js*)

- Default supported static file extensions

    - js
    - ts
    - jsx
    - vue
    - css
    - scss
    - sass
    - less
    - styl
    - htm
    - html
    - xhtml
    - xml
    - log
    
    

## Installation

### Package Control

1. `Ctrl+Shift+P` then select `Package Control: Install Package`
2. Type `Laravel Goto`

### Manually

-  MacOS

   ```shell
   git clone https://github.com/absszero/LaravelGoto.git ~/Library/Application\ Support/Sublime\ Text\ 3/Packages/LaravelGoto
   ```

- Linux

  ```shell
  git clone https://github.com/absszero/LaravelGoto.git ~/.config/sublime-text-3/Packages/LaravelGoto
  ```

- Windows

  ```shell
  git clone https://github.com/absszero/LaravelGoto.git %APPDATA%\Sublime Text 3\Packages\LaravelGoto
  ```



## Usage

- Move your cursor on a text, Press `Alt`+`Left-Click` or `Alt`+`;` to run the command.
- Select a text, `Right-Click` to open content menu, Press `Laravel Goto`.



## Extend static file extensions

You can add other file extensions throught `Preferences > Package Settings > LaravelGoto > Settings`, and add this option `static_extensions` 

```json
    "static_extensions": [
        "your_extension_here"
    ]
```

