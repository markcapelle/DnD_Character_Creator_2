# DnD_Character_Creator_2

GitHub Repository: https://github.com/markcapelle/DnD_Character_Creator_2
Render Deployment: https://dnd-character-creator-2.onrender.com/

Dungeons and Dragons (5th Edition) Character Creator (v2)

Project Description
This project is version 2 of the Python Project Dungeons and Dragons Character Creator. The project has been mostly rewritten and refactored to use databases instead of browser sessions to store data.
Additionally a userid system has been implemented so that multiple users can access the app and manage their own data.

Test Credentials
These test credentials contain some characters I created during testing. The system is ready for you to create new users.
User: mark@email.ie
Password: pass

Features
Character Sheet Generator
Users can explore multiple character race and class options, and based on selections see exactly which abilities their points allocation should focus on, as well as peruse the traits that will be available to them. Instead of having to spend a long time flicking back and forth through a rulebook, everything pertinent will be presented in easily digestible segments, especially for newcomers to the tabletop game.

Dice Box
For prospecting players who just want to try the game out and haven’t invested in their own dice yet, the random number generator using some simple javascript allows users to simulate multi sided dice, from the unusual d4 to the complicated d100 and the bread-and-butter Dungeons and Dragons d20. Additionally, the user will be able to roll multiples of the same dice all at once.

Spellbook
Instead of having to search through the veritable tome for that one spell a user wants to try out, the provided spellbook has some starter spells that are easily accessed through a button click and like all other aspects of the app, can easily be expanded and scaled.

Variable tracker
On their character sheet, the user will have the interactivity to tick off spell slots as they are used, hit dice as they are rolled, and even keep track of death save rolls and managed hit points with just a button click. All the data is saved in a database on a character-by-character basis, all linked to the user’s userid.

Notebook
Each of the user’s characters saves a unique notebook in which they can save and organise their custom campaign notes.

Design
Colours
The colours used were selected from the classing DnD colour palate seen on most traditional character sheets. It gives a weathered paper, scroll kind of look. Experiments were done with some texture files, but it made some of the text harder to read so a gradient was used to make the background colours less monotonous.

Fonts
A variant of Times New Roman was used. It’s a simple, readable font and gives it a slightly medieval feel in keeping with the general fantasy aesthetic.

Audio
Simple dice rolls in a wooden box were recorded as well as a few page flicks and pen scribbles. The best of each was selected and converted into mp3 files to be used in the app to invoke the classic pen and paper tabletop game feel.
A paper tearing sound effect was added for deletion of characters, notes, etc.

Development
Project Planning
Most of the project planning was to do with what the database was going to look like. A few sketches were made in simple spreadsheets just to get an idea of what data was actually needed. From there it grew into a database diagram that focused on what data would be divided into what table and what the table relationships would look like. 
From there the project aesthetic mimicked previous iteration, and the original DnD character sheet design.
Part of the data design was to minimise the amount of data each character had to store. This was achieved by simply recording the ability stats. All other modifier and numerical stats could then be calculated programmatically in the character sheet when displaying. In part, this makes the database somewhat ready for a future levelling up system where ability scores can be improved and higher-level proficiency bonuses can be pulled from variables, instead of having to update a number of columns and tables every time.

Python (app.py)
app.py is the central hub of the entire Flask application, handling the routing, database interaction, authentication, and character management logic in one place. It initializes the flask app, loads the database configuration, registers all models in models.py, and exposes every route the frontend relies on.

SQL Database 
The SQL database is hosted by Neon and entirely built in models.py.
The tables were organised into three main categories. 
The user table stores the user data.
The characters table links to the user so they only see the characters they have created. The character tables store a variety of data to do with the individual characters, while also referencing to the reference tables.
The reference tables are the static data from which the characters are built. These store the various available races, their specific features and rules, classes, etc. its from these reference tables some of the universal character data is displayed.

Scripts (*.py)
Simple single-run python scripts were created for ease of development. Scripts would easily remove tables so they could be modified and recreated on flask execution. Another was used to pre-populate the database under a test user with test data. Another script was created that quickly and easily populates the static database tables from which the app draw class, race and background data/rules.
Seed_script.py is the most useful even after the app enters production. It uses dictionaries that can be easily expanded in order to add more classes, races, backgrounds, spellbooks and even spells for character creation and customisation.

CSS
Style.css
All the general style data is used across the board in style.css, specifically written to use flex for responsive design and an aesthetic derived from DnD character sheets.
Some additional styles were added for new features such as the notebook. In particular, the spellbook style was overhauled to include an index of pips, to show the user relatively which page in the spellbook they are browsing.

Dice_animations.css
Used exclusively on the dice hub dice.html. It handles the 2d animations that display the dice results.

Javascript
Dice.js
The dice rolling javascript is kept in a separate javascript and just uses a couple of functions to generate random numbers depending on how many sided dice is selected. And the output is arrayed when multiple dice are requested.

Audio.js
This js file exclusively loads the mp3 files and has a function that plays audio from the beginning. Additional functions call the main function, feeding it the required variable for the specific sound required.

Index.js
The controller script that makes the character list page interactive. It attaches click handlers to the Load, Delete, and New Character buttons so the page can route to a character, remove one via a DELETE request, or start creating a new one.

Character_sheet.js
The javascript that powers all the interactive trackers and utility buttons on the character sheet page. It initializes the UI based on values sent from the backend; hit dice, death saves, exhaustion, and spell slots by reading each element’s data attribute and updating the visual state accordingly.
It also handles all in page actions: adjusting HP, toggling hit dice, marking death saves, changing exhaustion levels, and tracking spell slot usage. Each click directs to audio.js functions for sound effects.

Character_creation.js
This javascript is the logic layer that drives the character building workflow. It listens for every choice the user makes and updates the interface dynamically based on those selections. It controls how many skills can be selected based on class, auto-checks the skills granted based on background to prevent double-selection and updates ability values based on race bonuses.

Notebook.js
This javascript powers the character specific notebook window. Its main job is to handle switching between notes, loading their content from the database and saving edits whenever a heading tab is changed, or after 1.5 seconds after user inactivity.

Spellbook.js
This .js file controls the page flipping interface of the user’s spellbook popup. It collects all the .spell-page elements from the character, builds a row of clickable “pips” for navigation, and keeps track of which page is currently visible.



Challenges Faced
Bad habit
I picked up on a bad habit during the development of this app. I tended to set a feature that I want to add, and then fail to commit working interim iterations of the feature along the way. I usually work until that feature is completely done, then commit it all in one upload.
Technically not an issue when working on a solo project, but I can see how that could cause issues when collaborating in a team working on different features and interactions in tandem.

Performance latency
Some distinct performance latency was detected after implementation of Render. This appears to be a common thing between services such as Render and Neon and seems to be the nature of using free services. Every time a character change is made, say adjusting HP or fetching a notebook entry and making changes, there is a noticeable 2 second delay.
I think a possible solution would be to better merge design philosophies of v1 and v2 of the app. Use browser sessions to display and modify the character sheet in real time, then a second of user inactivity commits the change to the database in the background.
Testing this would require a complete refactor of the project, so it should be something worth noting in the next project.

Sources
All of the character creation algorithms, character classes, races, rules, dice designs and equipment are derived from the contents of the Dungeons and Dragons 5th Edition Player’s Handbook by Wizards of the Coast.

Deployed site
This site has been deployed to GitHub Pages at the URL below:
https://markcapelle.github.io/DnD_Character_Creator_2/

