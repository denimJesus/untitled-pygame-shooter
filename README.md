# untitled-pygame-shooter
> An unfinished and unplayable game-like thing faintly resembling Vampire Survivors, made to practice Python, Pygame and basics of game development.

## Technologies Used
- Python 3.11.2
- Pygame 2.2.0

## Usage
- Run **main.py**.
- Move with WASD or arrow keys (or press M to toggle mouse movement)
- Die / get bored
- Press ESC to quit.

Automatic shooting is planned, but not implemented yet, and only one enemy type spawns. Also included are next to no graphics, no sprite animations and no level ups, so pretty much no game yet either.

Window size can be changed by editing the values of `WIDTH` and `HEIGHT` in **variables.py**. These, as well as the variable `SPRITE_SCALE` also affect non-visual things in the code, so were there any game balance, that might be affected as well.

Even though no other inputs (outside future menus) are planned, for now there are debug keys for testing. These probably will change often (and can be found in event_queue.py), but at the time of writing they are as follows:
```
Key    Action
 1    Spawn 3 bullets orbiting player
 2    Spawn 9 bullets orbiting player
 3    Spawn bullet orbiting player (with random radius and offset)
 4    Spawn bullet orbiting last bullet spawned with 3 (with random radius and offset)
 5    Despawn all bullets
 6    Fire bullet at closest enemy
 7    Fire bullet at random enemy
 8    Fire Bullet_Sine at closest enemy (a bullet traveling in a wave)
 9    Spawn Enemy_Sine from random direction (an enemy traveling through obstacles in a wave)
 0    Kill all enemies
 P    Spawn Enemy_Follow from random direction (an enemy moving towards player)
 O    Spawn Worm (unfinished enemy type)
 I    Spawn a "bombs" pickup at coordinates (100,100) (spawns an explosion on 3 random enemies)
```

## Image Generator
In the directory `./image_generator` is a simple Python file **imagegen.py** to generate a custom image for the player sprite, and demonstrate one idea on how to implement sprite animations. It blits images from files in the subdirectories `heads` and `legs` on an image in subdirectory `bodies`, and saves the resulting image.

##### Usage
If **imagegen.py** is run by itself, a window opens, where you can preview the sprite. Parts can be changed with the keys Q/E (for heads), A/D (for bodies) and Z/C (for legs). ENTER saves the current selection as a .png file, which will be imported by the game as a player image. ESC quits without saving.

The parts' names are shown under the sprite (with the first letter capitalized). These are taken from the filenames in `heads` and `bodies`, and in the case of `legs`, the subdirectory names, as legs support multiple pictures for multiple frames of animation. 

Also has a function `get_sprite_by_names()`, which can be imported. It takes the aforementioned part names (filenames without extensions) as parameters, and returns a tuple of (`sprite standing still as a pygame.Surface`, `Looping Python Generator for walk animation frames`).
