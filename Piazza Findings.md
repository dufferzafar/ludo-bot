
# Meta

_(?) indicates doubts_

* The game goes on till a player wins
    - No limit (?)

* The time limit is not fixed to be 120sec
    - It will be varied during gameplay somehow (?)
    - How will this affect things (?)

* There will be multiple matches between bots

* Demo 1
    - Die rolls are always 1

* Demo 2
    - P1 gets die roll of 2
    - P2 gets 1

# Gameplay

<!-- * There should be _some AI_ involved -->

* **Die Rolls**
    - Is a list: `[6, 6, 5]`

    - Is not ordered (?)
        + So we can move `5` before `6` on some coin

    - 3 sixes result in a duck: `[0]`
        + There will never be a `[6, 6, 6]`

* **Moves**
    
    - Multiple moves are separated by `<next>`

* **Opening**

    - Opening moves should be sent before all others (?)

    - `_6` if opening by 6 & `_1` if opening by 1
        + as it should be

* **Skipping**
    - Send `NA\n` to pass a move

    - Only when there really is no valid move possible

    - If one move is possible, then just send it 
        + Even if it doesn't use all die rolls

* **Stacking**
    - Not allowed on `White` boxes only!

    - No concept of `Blocks`

    - On locations that can be stacked 
        + there can be any number of coins
            * of any color

* **Disable GUI**
    - Pass `--noBoard`


