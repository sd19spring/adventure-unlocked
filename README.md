![](https://i.imgur.com/YydO3Xo.jpg)

<iframe width="560" height="315" src="https://www.youtube.com/embed/94OChRZpU3c" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

Adventure unlocked is a generative parser based text game. It has new music and different interactions for every play through. The user interacts with the game in a terminal-like window where they can type in any command that they would like to explore the world.

<iframe width="560" height="315" src="https://www.youtube.com/embed/yEMsvp5hBEY" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

## Looks cool, right?

The game is a thrilling murder mystery, where you solve a murder. Will there be twists and turns you may ask? Well of course, though depending on how you play the game, things may change. The game will immerse you with its charming music and riveting story, and allow you to escape into another world. _Come on! Give it a try! The story is all about you!_

## Playing the Game
### Installation

Adventured unlocked is built with the following dependencies: pygame, and sonic-pi.
To install pygame:

    pip install pygame

To install sonic-pi:

    sudo add-apt-repository ppa:sonic-pi/ppa
    sudo apt-get update
    sudo apt-get install sonic-pi

### Running
To run the game simply execute the following command:

    python adventure_unlocked.py

## Want to know how the game works?
There are four main aspects of the code: a game engine, world generation, music generation, and visualization. These are them combined to create a playable, generative game.
### Game Engine
The game engine is effectively the core that ties together the other componenets of the game. The engine handles json interpretation, User input interpretation and maintainence of game state. The first two features are two are exercises in string parsing and responding to the users commands. The game state is mainly run through pygame. However, over many games, the users data can be saved through json and text files.

### World Generation
The world is composed of rooms to traverse and items to interact with. To generate these two, we decided to perform bottom up generation, having items by composed of different attributes that describe properties and reactions, and have rooms be filled with such items to interact with. The rooms are generated in order with breadth-first-search to ensure that the player is able to traverse in either direction from and to rooms back and forth.

### Music Generation

![](https://i.imgur.com/8sIZx5q.jpg)

In order to generate new music with each playthrough and room, a set of musical phrases is created then played.

A list was made for holding different weights for beat lengths - eighth, quarter, etc. - and another was created to hold different weights for intervals. Then, given a time signature and number of measures, beat lengths are randomly selected based on their weights. Afterwards, notes are selected for each beat length. The music is then played in sonic-pi as the game runs.

### Text Visualization

In order to create the visuals for our text game we used pygame to replicate a terminal style window. This was done to create easy text input and also animate text outputted from the game. This animation is done to simulate the game speaking to the player rather than the player just reading the game output. The terminal is the primary method of interacting with the game as you traverse the generated landscape of Adventure Unlocked.

![](https://i.imgur.com/GNzzocS.png)

## Our Inspiration

Throughout the process of developing Adventure Unlocked we focused primarily on the interesting prospect of making a game generate and run on its own. We sought to create a unique experience for each player so no one playthrough was the exact same as the last. Our original intentions involved a bare bones framework for a ordinary text adventure game that could then be adapted to a generative method of creating items and rooms for the game.
This broad goal was guided by the advice of our peers and mentors as we balanced the scale of the generative portions of the game. In the first architectural review we were able to decide on the theme of Murder Mystery to guide the plot and objective of the game. Also, we  sure to priortize the entertainment and ease of play for the game as we do not want our generation to impede our player's experience. In the second architectural review we focused on some of nuances related to game interactions by asking about if previous games should affect a player's current game. While this goal seemed to be interesting to us we dtermined the best path for us was to focus on the integration of different sections of code in order to create a cohesive game. Our priority from then on was creating a working version of the game to sort the issues that may come up along the way.
In the end, our game is different from the initial idea, but still interesting. It is a generative text based adventure, where you are trying to solve a murder mystery. How the story goes is up to you. As a result, any player can feel connected to the game because they are the main character in the game.

## Authors
* [Manu Patil](https://github.com/mpatil99) - Game engine
* [Richard Gao](https://github.com/hardlyrichie) - World generation
* [Chris Lee](https://github.com/clee4) - Music generation
* [Colin Takeda](https://github.com/cstakeda) - Frontend visuals

## Attribution

[Pygame](https://www.pygame.org/docs/): Pygame is a set of modules used for video game development in Python. We have used it to create our custom terminal window.

[SonicPi](https://sonic-pi.net/): SonicPi is a music creation software, which allowed us to generate and play music as our game ran.

[TextWorld](https://www.microsoft.com/en-us/research/project/textworld/): an open-source, extensible engine that both generates and simulates text games. Built to train reinforcement learning (RL) agents to learn skills such as language understanding and grounding, combined with sequential decision making, we took inspiraton from their game generation idea.

The mansion image was downloaded from [stickpng.com](http://www.stickpng.com/img/miscellaneous/buildings/haunted-house) 

## License
This project is licensed under the MIT License - see the LICENSE.md file for details
