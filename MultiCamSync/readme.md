# Video Syncing Tool

This project is a simple GUI application that allows you to synchronize two videos either by their creation date or by their audio.

## Features

- Synchronize videos by creation date
- Synchronize videos by audio

## Dependencies

- PySimpleGUI
- Sync_by_time
- sync_by_audio
- Utilies

## How to Use

1. Run `main.py`.
2. In the GUI, input the paths for `VIDEO_1` and `VIDEO_2` by typing them in or using the file browser.
3. Choose the synchronization method by selecting either 'Sync by Creation Date' or 'Sync by Audio'.
4. Click 'Sync' to start the synchronization process.

If the synchronization is successful, a popup will appear saying 'Done!', which will auto-close after 3 seconds. If the synchronization fails, an error popup will appear.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)