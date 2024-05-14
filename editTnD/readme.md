# Image Date Editing Tool

This project is a simple GUI application that allows you to edit the date metadata of images.

## Installation

Before running the script, you need to install the required Python libraries. You can do this by running the following command in your terminal:
'pip install -r requirements.txt'

## Features

- Edit image date to a specific date
- Rename folders
- Generate image thumbnails

## Dependencies

- PySimpleGUI
- os
- datetime
- piexif
- glob
- PIL

## How to Use

1. Run `edit_img_creation_tnd.py`.
2. In the GUI, input the path for the folder containing the images you want to edit.
3. Input the new date you want to set for the images.
4. Click 'Edit Date' to start the editing process.
5. to calculate age enter birth date (bottom ddl) and estimated age (this why you could tell what was date when for exemple you were 4 years old in a family event)
after approving, the date will be copied to the editing panel

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)