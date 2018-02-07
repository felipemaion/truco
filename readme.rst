Truco Paulista
==============

This is my first project in Python.
It is a Game called Truco (Paulista). Very popular in Brazil.

How to use:
-----------


You will need to install the package for the Deck of cards::

    pip install pyCardDeck
    

Made and shared at Github (https://github.com/iScrE4m/pyCardDeck) by iScrE4m


After that you can run the pre-loaded game (4 players)::

python truco.py

Or just create a new one as shown at the very last lines of the truco.py file:


.. code-block:: python
    game = TrucoGame([Player("Felipe"), Player("iScreE4m")])
    game.truco()
  

