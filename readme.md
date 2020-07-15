# Laravel Goto for Sublime Text

Goto various Laravel files

![example](example.gif)

## Feature

- Go to Blade Template files *(EX. hello.blade.php)*

- Go to Controller and highlight method *(EX. \Namespace\Controller.php@Method)*

- Go to Static files (*EX. hello.js*)

- Go to Config files and highlight option (EX. config/app.php)

- Go to Language files and highlight option (EX. resources/lang/en/messages.php )

- Go to .env and highlight option

- Go to paths by path helpers, EX:
  - app_path('User.php');
  - base_path('vendor');
  - config_path('app.php');
  - database_path('UserFactory.php');
  - public_path('css/app.css');
  - resource_path('sass/app.scss');
  - storage_path('logs/laravel.log');

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

- Select a text, `Right-Click` to open content menu, Press `Laravel Goto` or use `Alt + ;`.


## Extend static file extensions

You can add other file extensions throught `Preferences > Package Settings > LaravelGoto > Settings`, and add this option `static_extensions`

```json
    "static_extensions": [
        "your_extension_here"
    ]
```

