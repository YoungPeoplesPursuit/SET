# SET

A set clone I made because I love playing SET, but my friends aren't always on SETwithfriends to play with me :(. In fact, a lot of my friends don't like playing SET. I don't have a set of SET cards, so I decided to make my own digital SET.



## Features

- UI with clickable cards  
- Automatic scoring (3 points per SET)
- Reset cards if you can't find a SET



## Rules

The main objective of the game is to get SETs. A SET is a set of 3 cards with the condition that **every attribute of every card in the set is either all same or all different**.

Each card has 4 attributes:

- **Number:** the number of shapes on the card, from 1 to 3
- **Color:** the color of shapes on the card, which are red, green, and purple in my game
- **Shape:** the shape on the card, which are oval, diamond, and squiggle (angular S) 
- **Shading:** each card has a distinct shading, which are no fill (a white shape with a colored outline), light, or dark. 

In other words, you don't want any attributes to be 2 of a kind in the cards you choose. 


## Installation
```bash
git clone https://github.com/youngpeoplespursuit/SET.git
cd yourproject
pip install -r requirements.txt
python main.py
