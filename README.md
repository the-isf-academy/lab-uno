# UNO - Card game lab
The goal of this lab is to teach classes and objects through the implementation of a text-based game.

This implementation of Uno is documented [here](https://cs.fablearn.org/docs/uno/).

## Setup
After cloning the repository, run the following command in your Terminal:

    pip install -r requirements.txt

This will automatically install all of the packages required to run this lab.

## Play!
Run `python game.py` to play!

#### Note: setup from command line
The game can be setup from the command line to avoid going through the manual setup:

    python game.py -h human_name-human_name-... -c computer_strategy-computer_strategy-... -f deck_file.csv

### Cards
Cards are can be read into the game from a csv file organized as such:
| color | number | special        |
|-------|--------|----------------|
| red   | 2      |                |
| red   |        | skip           |
|       |        | wild-draw-four |

The following sets of cards are included in this repo:

* standard deck (`uno_cards.csv`)
* standard deck without special cards (`uno_cards_basic.csv`)
* standard deck without draw two cards or wild draw four cards (`uno_cards_no_draw.csv`)

### Rules

The rules of this implementation of uno are based on the ones found here: [http://play-k.kaserver5.org/Uno.html](http://play-k.kaserver5.org/Uno.html)

Some exceptions:

* If a player draws a card because they cannot play during their turn, they cannot immediately play that card (they must wait until their next turn).
* If a player plays an invalid card, they must return the card to their hand, draw two cards and end their turn.
* The game always starts the same way, even if a special card is drawn as the first top card. A random color is chosen if the first card is a wild card.
* No scoring or stats are maintained over multiple games. [But this could make a great extension!]

## Lab
You can find the lab documenting this assignment [here](https://cs.fablearn.org/labs/2-2-uno%20lab.html).
