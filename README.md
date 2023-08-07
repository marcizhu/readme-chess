# GitHub README Chess Tournament

This template repository contains the source code for a Python Chess bot, together with GitHub Workflows in order to allow ANYONE to play chess from a README file. Want to see this in action? Go to my [profile page](https://github.com/marcizhu) and feel free to try it out by yourself!


## Steps to make your own repo

1. Create a new repository based on this template.

2. (Optional) Tweak the bot settings to your linking. These settings are located in the file `data/settings.yaml`. You can leave them as they are if you don't want to change anything.

3. Rename the folder `.github/_workflows` to `.github/workflows` in order to enable the GitHub Actions workflow that does all the magic.

4. Delete this README file and make your own `README.md`. I recommend using `README.template` as a starting point. Keep in mind that the text between the HTML comments like `<!-- BEGIN CHESS BOARD -->` and `<!-- END CHESS BOARD -->` will be recreated after each move, so don't waste your time changing anything in there ;)

5. Commit and push all the settings and create a new issue with title `Chess: Start new game` (case insensitive). If all goes well, after a few seconds a new response should appear telling you that a new game was successfully started and the issue should be automatically closed. After that, refresh your repository in order to see the changes done by the bot and your repository is ready to go! Just click on any of the links on the table of available moves, click on "Submit new issue" and after a few seconds, the move will be played!

Don't forget to share, have fun and enjoy your games!


## Some extra information

All games are automatically archived into the `games/` folder in PGN format. The current game is always called `games/current.pgn`, and the archived games always follow the pattern `games/game-yyyymmdd-HHMMSS.pgn`. You can download the archived games and review them using an external application. Each move in the PGN file has a comment specifying who performed each move so you can see which moves you played!

Finally, if you find any problem, feel free to submit an issue or open a PR and I will be more than happy to take a look at it!


## Credits

Thanks to [@timburgan](https://github.com/timburgan) for the initial idea. This project is heavily inspired on his. Also, big thanks to the authors and contributors of [python-chess](https://python-chess.readthedocs.io/en/latest/) and [PyGithub](https://pygithub.readthedocs.io/en/latest/). Without their libraries, this project would have been impossible :heart:


## License

This template and the code in it is licensed under the [MIT License](https://github.com/marcizhu/readme-chess/LICENSE).  
If you use this on your own repositories, please add a link back to this repo :D
