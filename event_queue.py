import pygame as pg
import random, math, sys
import weapons, misc, enemies, pickups
from pygame.locals import *
from variables import *

def process_event_queue(game):
    """ Check event queue for non-movement related keypresses """
    game = game
    player = game.player
    for event in pg.event.get():

        # ESC / Close button
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pg.quit()
            sys.exit()
            raise SystemExit

        # M = Toggle mouse
        if event.type == KEYDOWN and event.key == K_m:
            player.mouse_movement_enabled = not player.mouse_movement_enabled

        # Temporary debug buttons for testing
        """ 1 = Spawn 3 orbiters
            2 = Spawn 9 orbiters
            3 = Spawn bullet orbiting player (with ugly random offset)
            4 = Spawn bullet orbiting previous bullet spawned with 3
            5 = Despawn bullets
            6 = Spawn bullet towards closest enemy
            7 = Spawn bullet towards random enemy
            8 = Spawn (WIP) sine bullet
            9 = Spawn (WIP) sine enemy
            0 = Kill enemies
            P = Spawn Enemy_Follow
            O = Spawn Worm (very WIP)
            I = Spawn a bomb pickup
            
            Z, X, C = Some patterns made with weapons.spawn_orbiters()
        """
        global prev
        if event.type == KEYDOWN:
            if event.key == K_1:
                weapons.spawn_orbiters(game, 3)
            elif event.key == K_2:
                weapons.spawn_orbiters(game, 9)
            elif event.key == K_3:
                offset = (random.randrange(0,4), random.randrange(0,4), random.randrange(0,20), random.randrange(0,20))
                prev = weapons.Bullet_Orbit(game, player, random.randrange(20,150), random.randrange(10,50), -1, offset)
            elif event.key == K_4:
                try:
                    offset = (random.randrange(0,4), random.randrange(0,4), random.randrange(0,20), random.randrange(0,20))
                    weapons.Bullet_Orbit(game, prev, random.randrange(5,30), random.randrange(1,50), -1, offset)
                except:
                    pass
            elif event.key == K_5:
                for sprite in bullet_group:
                    sprite.kill()
            elif event.key == K_9:
                enemies.Enemy_Sine(game)
            elif event.key == K_0:
                for sprite in enemy_group:
                    sprite.death()
            elif event.key == K_p:
                enemies.Enemy_Follow(game)
            elif event.key == K_o:
                enemies.Enemy_Worm_Head(game)
            elif event.key == K_i:
                pickups.Item_Bombs(game, 100,100)
            elif event.key == K_z:
                weapons.spawn_orbiters(game, 2, 50)
                weapons.spawn_orbiters(game, 4, 70)
                weapons.spawn_orbiters(game, 6, 90)
                weapons.spawn_orbiters(game, 8, 110)
                weapons.spawn_orbiters(game, 10, 130)
            elif event.key == K_x:
                weapons.spawn_orbiters(game, 2, 50, -30)
                weapons.spawn_orbiters(game, 4, 70)
                weapons.spawn_orbiters(game, 6, 90, -30)
                weapons.spawn_orbiters(game, 8, 110)
            elif event.key == K_c:
                weapons.spawn_orbiters(game, 20, 50)
                weapons.spawn_orbiters(game, 20, 70, -30)
                
        if pg.key.get_pressed()[K_6]:
            weapons.Bullet_Line(game)
        if pg.key.get_pressed()[K_7]:
            weapons.Bullet_Line(game, misc.get_random_enemy())
        if pg.key.get_pressed()[K_8]:
            weapons.Bullet_Sine(game)
