"""Define a enemy"""

from sprites.character import *
from inventory.inventory import Inventory
from config.colors import GREEN, YELLOW, RED
from config.window import TILESIZE
from utils.cell import Cell
from random import uniform
from random import randint
vec = pg.math.Vector2

# npc settings
MOB_HIT_RECT = pg.Rect(0, 0, TILESIZE-16, TILESIZE-16)
SIZE = 8
SEEK_FORCE = 0.1
APPROACH_RADIUS = 50
WANDER_RING_DISTANCE = 500
WANDER_RING_RADIUS = 150
CLASSES = ["Fighter","Mage","Rogue"]
TYPE = {
    "Skeleton" : {"health":80, "STR":10, "DEX":5, "CON":5, "INT":5, "WIS":5, "CHA":5},
    "Goblin" :   {"health":80, "STR":10, "DEX":5, "CON":5, "INT":5, "WIS":5, "CHA":5}
}

class Enemy(Character):
    def __init__(self, game, x, y, _type, health, images):

        self.groups = enemies
        pg.sprite.Sprite.__init__(self, self.groups)
        super(Enemy, self).__init__(game, x, y, _type, images, MOB_HIT_RECT)
        
        self.pos = vec(x, y)
        self.vel = vec(1, 1).rotate(uniform(0, 360))
        self.acc = vec(0, 0)

        self.last_timestamp = 0
        self.last_timestamp2 = None
        self.now = 0

        self.numberOfAction = 0

        self.inventory = Inventory(self, 5, 8)

        self.attack_range = TILESIZE * 2

        logger.error("il y a un souci d'update avec la camera")

        self.speed = 2
        
        self.target = self.pos
        self.player_spotted = None
        self.goto = []
        self.view_range = TILESIZE * 6
        self.moving = False

        self.health = TYPE.get(self.type).get("health")
        self.STR = TYPE.get(self.type).get("STR")
        self.DEX = TYPE.get(self.type).get("DEX")
        self.CON = TYPE.get(self.type).get("CON")
        self.INT = TYPE.get(self.type).get("INT")
        self.WIS = TYPE.get(self.type).get("WIS")
        self.CHA = TYPE.get(self.type).get("CHA")
        
    def __repr__(self):
        """default displayed text whenever printing the enemy
        """
        return self.type
        
    def save(self):
        """saves the enemy's characteristic into game_data

        """
        return {
            "class": self.type,
            "pos": {
                "x": self.pos.x,
                "y": self.pos.y
            },
            "health": self.health,
            "inventory": self.inventory.save()
        }

    
    def draw_health(self):
        """draw healthbar onto the screen
        """
        if self.health > 60:
            col = GREEN
        elif self.health > 30:
            col = YELLOW
        else:
            col = RED
        width = int(self.rect.width * self.health / TYPE.get(self.type).get("health"))
        self.health_bar = pg.Rect(0, 0, width, 7)
        if self.health < TYPE.get(self.type).get("health"):
            pg.draw.rect(self.image, col, self.health_bar)

    def throw_inventory(self):
        """drop every item stored inside the enemy's inventory
        """
        for slot in self.inventory.slots:
            if slot.item:
                self.inventory.throw_item(slot.item)

    def update(self):
        if self.health <= 0:
            self.throw_inventory()
            self.kill()
            self.game.turn_manager.enemies.remove(self)

        #if trap nearby: flee(trap)

        """ reset player spotted every 10 seconds
        """
        self.now = pg.time.get_ticks()
        if self.last_timestamp2 is None:
            self.last_timestamp2 = self.now
        if self.now - self.last_timestamp > 10000:
            self.last_timestamp = self.now
            self.player_spotted = None

        if self.game.versus_manager.active:
            """ If a player is in sight, evaluate whether he is worth attacking or not
            """
            if self.player_detection():
                if self.evaluation():
                    self.flee(self.player_spotted.pos)
                    #need to skip turn after some time
                else:
                    """ if player out of reach, "pathfind" him
                    """
                    
                    if self.move_or_attack():
                        if self.now - self.last_timestamp2 > 1500 and self.vel == vec(0,0): # skip if stuck on a wall
                            logger.info(self.last_timestamp2)
                            self.last_timestamp = self.now
                            self.moving = False
                            self.end_turn()
                        #bug à la ligne juste dessous si l'ennemi est juste à côté du joueur
                        if not self.goto and not self.player_spotted.pos.x - TILESIZE/2 <= self.pos.x <= self.player_spotted.pos.x + TILESIZE/2 and not self.player_spotted.pos.y - TILESIZE/2 <= self.pos.y <= self.player_spotted.pos.y + TILESIZE/2:
                            self.goto = self.path_finding(self.player_spotted.pos)
                            if self.goto:
                                del self.goto[0]
                        # logger.debug(self.goto)
                        if self.goto:
                            for i in self.goto:
                                rect = pg.Rect(i.coor, (SIZE, SIZE))
                                pg.draw.rect(self.game.map_img, (255, 255, 255), rect)
                            self.acc = self.seek(self.goto[0].coor)
                            if self.goto[0].coor.x - 32 <= self.pos.x <= self.goto[0].coor.x + 32 and self.goto[0].coor.y - 32 <= self.pos.y <= self.goto[0].coor.y + 32:
                                del self.goto[0]
                            # logger.debug("enemy proche, utilisation du A* et avancement que de X case")
                        else:
                            self.vel = vec(0,0)
                            self.moving = False
                            self.end_turn()
                    else:
                        self.attack()
                """if there is no player in range, just move around
                """
            else:
                self.end_turn()

                # temp = self.avoidnpc()
                # if temp is False:
                #     self.acc = self.wander()
                # else:
                #     self.acc = temp

            
        """actual movement update
        """
        self.vel += self.acc
        if self.vel.length() > self.speed:
            self.vel.scale_to_length(self.speed)
        self.get_direction()
        self.update_image()
        self.pos += self.vel
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

        self.update_collisions()

        # self.vel += self.acc
        # if self.vel.length() > self.speed:
        #     self.vel.scale_to_length(self.speed)
        # super().update()

    def get_direction(self):
        """get the direction which the sprite is currently facing
        """
        angle = self.vel.angle_to(vec(0, 1))
        self.direction = "down"
        if 180 - 45 <= angle < 180 + 45:
            self.direction = "up"
        if 90 - 45 <= angle < 90 + 45:
            self.direction = "right"
        if 270 - 45 <= angle < 270 + 45:
            self.direction = "left"

    def seek(self, target):
        """moves self toward a given target following a curve trajectory from its position

        Args:
            target (vec(x,y)): position vector of the target

        Returns:
            vec(x,y): acceleration vector that self should use to reach the target
        """
        desired = (target - self.pos)*2
        distance = desired.length()
        desired.normalize_ip()
        if distance < APPROACH_RADIUS:
            desired *= distance / APPROACH_RADIUS * self.speed
        else:
            desired *= self.speed
        steer = (desired - self.vel)
        if steer.length() > SEEK_FORCE:
            steer.scale_to_length(SEEK_FORCE)
        return steer

    def wander(self):
        """advanced wandering occuring every 5 to 10 seconds

        Returns:
            vec(x,y): acceleration vector that self should use to reach the target
        """
        # now = pg.time.get_ticks()
        # if now - self.last_timestamp > randint(1000,5000):
        #     self.last_timestamp = now
        circle_pos = self.pos + self.vel.normalize() * WANDER_RING_DISTANCE
        target = circle_pos + vec(WANDER_RING_RADIUS, 0).rotate(uniform(0, 360))
        return self.seek(target)

    def flee(self, target, FLEE_DISTANCE=200):
        """makes the npc run away from the target

        Args:
            target (vec(x,y)): position of the target

        Returns:
            vec(x,y): acceleration vector that self should use to reach the target
        """
        steer = vec(0, 0)
        distance = self.pos - target
        if distance.length() < FLEE_DISTANCE:
            desired = distance.normalize() * self.speed
        else:
            desired = self.vel.normalize() * self.speed
        steer = desired - self.vel
        if steer.length() > SEEK_FORCE:
            steer.scale_to_length(SEEK_FORCE)
        return steer

    def path_finding(self, goalvec=vec(0, 0)):
        """implementation of the A* pathfinfind algorithm

        Args:
            xgoal (int): x coordinate of the objective
            ygoal (int): y coordinate of the objective
        Returns:
            list : calls the function reconstruct_path to create the list of cells
        """
        start = Cell(coor=self.pos)

        open_set = [start]
        closed_set = []

        start.f = start.g + (self.pos - goalvec).length()

        # test = open(r'C:\Users\valen\Desktop\projet python\dungeons-dragons-dev\dungeons-dragons\sprites\wx.txt', 'w')
        # test.write(f'{start.coor//TILESIZE} is the start and my f is {start.f}, my g is {start.g}\n')
        # test.write(f'{goal.coor//TILESIZE} is the objective and my f is {goal.f}, my g is {goal.g}\n')

        """boucle de recherche de chemin
        """
        while open_set:
            """pitié faites que personne ne voit ça, ça sélectionne la case la plus proche de l'arrivée
            """
            mini = 10000
            for mincell in open_set:
                if mincell.f <= mini:
                    mini = mincell.f
                    current = mincell
            """si cette case est l'arrivée, on retourne le chemin pour y parvenir
            """
            if goalvec.x-TILESIZE <= current.coor.x <= goalvec.x+TILESIZE and goalvec.y-TILESIZE <= current.coor.y <= goalvec.y+TILESIZE:
                path = []
                return current.reconstruct_path(path)

            # for u in open_set:
            #     test.write(f'{u.coor//TILESIZE} is in open and my f is {u.f}, my g is {u.g}\n')
            # for y in closed_set:
            #     test.write(f'{y.coor//TILESIZE} is in closed and my f is {y.f}, my g is {y.g}\n')
            # test.write(f'{current.coor//TILESIZE} is the current cell and my f is {current.f}, i shoulf have a large {current.g} value\n')

            open_set.remove(current)
            closed_set.append(current)

            """exploration des voisins
            """
            for neigh in current.neighbor():
                """skip murs
                """
                for wall in self.game.walls.sprites():
                    skip = False
                    if wall.rect.collidepoint(neigh.coor):
                        skip = True
                        break
                if skip:
                    continue
                """skip out of bounds
                """
                if neigh.coor.x < 0 or neigh.coor.y < 0:
                    continue
                """skip noeuds explorés
                """
                skip3 = False
                if closed_set:
                    for noeudexplored in closed_set:
                        if neigh.coor//TILESIZE == noeudexplored.coor//TILESIZE:
                            skip3 = True
                            # test.write(f"{neigh.coor//TILESIZE} vire moi ça de là\n")
                            break
                if skip3:
                    continue
                """le voisin est une case valide à explorer, il est ajouté aux cases à explorer
                """
                gtry = current.g + (current.coor - neigh.coor).length()
                if neigh.g == 0 or gtry < neigh.g:
                    # test.write(f'{neigh.coor//TILESIZE} is a neighbor :D\n')
                    neigh.came_from = current
                    neigh.g = gtry
                    neigh.f = neigh.g + (neigh.coor - goalvec).length()
                    if not open_set:
                        open_set.append(neigh)
                    else:
                        """"skip already set to be explored
                        """
                        skip2 = False
                        for noeudnonexplored in open_set:
                            if neigh.coor//TILESIZE == noeudnonexplored.coor//TILESIZE:
                                skip2 = True
                                # test.write(f'{neigh.coor//TILESIZE} hopla ça dégage\n')
                                break
                        if not skip2:
                            open_set.append(neigh)

            # if current.came_from is not None:
            #     assert current.came_from.g < current.g
            # assert closed_set.count(current) == 1, current
            # assert not (current in open_set and current in closed_set)
        return []

    def player_detection(self):
        """detects whether a player is whithin the line of sight of the NPC

        Returns:
            boolean: True or False
        """
        if self.player_spotted is None:
            for player in players:
                if (player.pos - self.pos).length() < self.view_range:
                    self.player_spotted = player
                    logger.info("player spotted")
                    return True
            return False
        return True

    def avoidnpc(self):
        """make every npc avoid one another

        Returns:
            vector: if there are ennemies colliding return an acceleration vector to avoid it
        """
        collision = pg.sprite.spritecollide(self, enemies, False)
        if collision is not []:
            for sprite in collision:
                if sprite != self:        
                    return Enemy.flee(self, sprite.pos)
        return False

    def health_percentage(self):
        """returns the percentage of health left
        """
        return self.health / TYPE.get(self.type).get("health") * 100

    def evaluation(self):
        """evaluates whether the ennemi should rush or flee the player.

        Returns:
            vec(x,y): acceleration vector following [the shortest path to the player / the optimal fleeing curve]
        """
        # linear : lambda x : x/25 - 2
        return self.health_percentage()/25 - 2 < (self.groupCount(enemies.sprites()) - Character.groupCount(self.player_spotted, players.sprites()))
        #     return npc.flee(self, self.player_spotted.pos)
        # else: return npc.moveto(self, npc.pathfinding2(self, self.player_spotted.pos))

    def move_or_attack(self):
        """decide whether to attack or move this turn
        """
        if self.moving is True:
            return True
        elif (self.player_spotted.pos - self.pos).length() > self.attack_range:
            self.moving = True
            return True
        else:
            return False

    def attack(self):
        """attack instructions
        """
        self.player_spotted.health -= self.STR
        self.game.versus_manager.logs.add_log(f'{self} attacked {self.player_spotted} dealing {self.STR} damages !')
        self.end_turn()
        
    def end_turn(self):
        self.last_timestamp2 = None
        self.goto = []
        self.game.versus_manager.check_characters_actions()