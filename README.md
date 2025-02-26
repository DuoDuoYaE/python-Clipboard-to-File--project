# python-exe-project/python-exe-project/README.md

# Clipboard to File Application

This project is a Python application that allows users to save clipboard content to a file using a graphical user interface (GUI). It includes features for managing clipboard content and configuring shortcuts for quick saving.

## Features

- Save clipboard text to a specified file.
- Configure default file paths and shortcut keys.
- Custom script execution within the application.

## Requirements

- Python 3.x
- Required libraries listed in `requirements.txt`

## Installation

1. Clone the repository or download the project files.
2. Navigate to the project directory.
3. Install the required dependencies:

```
pip install -r requirements.txt
```

## Running the Application

To run the application, execute the following command:

```
python src/Main.py
```

Or Packaging program:

```
pyinstaller --onefile --windowed --icon=src/invite.ico src/Main.py
```

## ~~[Windows]() How to start the folder path of the system boot~~

* ~~The directory where the system starts automatically：`shell:Common Startup`~~
* ~~The directory that the user starts automatically：`shell:Startup`~~

Do not add it to the boot folder, as there will be a scramble.Building the Executable

## To package the application as an executable, use the following command:

```
python setup.py build
```

This will create a standalone executable in the `dist` directory.

## Usage

1. Launch the application.
2. select any text to you, then click the shortcut they will be saved to the Specify the file.
3. Use the configured shortcut or the button in the GUI to save the clipboard content to the specified file.

## About script writing

If you write an infinite loop script, there are only two ways to stop:

1. Exit the main program
2. Or add it in the script

```
stop_event.is_set()
```

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.
