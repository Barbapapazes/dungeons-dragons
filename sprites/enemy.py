"""Define a enemy"""

from random import choice, choices, randint, random, uniform

from config.colors import GREEN, RED, YELLOW
from config.sprites import ARMOR, ASSETS_SPRITES, ITEMS, WAIT_TIME, TYPES_HEROS
from config.window import TILESIZE
from inventory.inventory import Armor
from utils.cell import Cell

from sprites.character import *

vec = pg.math.Vector2

# npc settings
MOB_HIT_RECT = pg.Rect(0, 0, 30, 30)
SIZE = 8
SEEK_FORCE = 0.25
APPROACH_RADIUS = TILESIZE
WANDER_RING_DISTANCE = 5 * TILESIZE
WANDER_RING_RADIUS = TILESIZE * 1
CLASSES = ["fighter", "rogue", "wizard", "boss"]
TYPE = {
    "skeleton": {"health": 10, "STR": 45, "DEX": 20, "CON": 15, "INT": 50, "WIS": 30, "CHA": 30},
    "goblin":   {"health": 15, "STR": 55, "DEX": 50, "CON": 10, "INT": 20, "WIS": 15, "CHA": 10},
    "phantom":   {"health": 20, "STR": 25, "DEX": 35, "CON": 20, "INT": 40, "WIS": 30, "CHA": 10},
    "boss": {"health": 50, "STR": 70, "DEX": 25, "CON": 40, "INT": 20, "WIS": 10, "CHA": 40}
}


class Enemy(Character):
    """Character subclass for all enemies in the game
    """

    def __init__(self, game, x, y, _type, images, equipments=False):
        self.goto = []
        self.groups = enemies
        pg.sprite.Sprite.__init__(self, self.groups)
        super(Enemy, self).__init__(game, x, y, _type, images, MOB_HIT_RECT)
        self.type_class = images
        self.images = ASSETS_SPRITES[images]
        self.image = next(self.images[self.direction])
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.hit_rect = MOB_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        # self.hit_rect = self.rect

        self.end = False
        self.end_time = 0

        self.pos = vec(x, y)
        self.vel = vec(1, 1).rotate(uniform(0, 360))
        self.acc = vec(0, 0)

        self.last_timestamp = 0
        self.last_timestamp2 = None
        self.now = 0
        self.cooldown = 1.1
        self.spawned = False
        self.cooldown = randint(10, 20)
        self.fleeing = False
        self.skip = False

        self.attack_range = TILESIZE * 2

        self.speed = 1

        self.target = self.pos
        self.player_spotted = None

        self.view_range = TILESIZE * 6
        self.moving = False

        if images[-1] == 'F':
            self.classe = "fighter"
            self.xp = 50
        elif images[-1] == 'R':
            self.classe = "rogue"
            self.xp = 50
        elif images[-1] == 'W':
            self.classe = "wizard"
            self.xp = 50
        else:
            self.classe = "boss"
            self.xp = 150

        self.health = TYPE.get(self.type).get("health")
        self.characteristics = {
            "str": TYPE.get(self.type).get("STR"),
            "dex": TYPE.get(self.type).get("DEX"),
            "con": TYPE.get(self.type).get("CON"),
            "int": TYPE.get(self.type).get("INT"),
            "wis": TYPE.get(self.type).get("WIS"),
            "cha": TYPE.get(self.type).get("CHA")
        }
        self.set_characteristics()

        if not equipments:
            self.difficulty_tweeking()

    def __str__(self):
        """default displayed text whenever printing the enemy
        """
        return f'{self.type} {self.classe}'

    def set_characteristics(self):
        """adjust characteristics according to the difficulty
        """
        self.characteristics['str'] += 3 * self.game.difficulty
        self.characteristics['dex'] += 2 * self.game.difficulty
        self.characteristics['con'] += 2 * self.game.difficulty
        self.characteristics['int'] += 2 * self.game.difficulty
        self.characteristics['wis'] += 1 * self.game.difficulty
        self.characteristics['cha'] += 1 * self.game.difficulty

    def difficulty_tweeking(self):
        """tweeks ennemy's statistics to match game difficulty"""

        for bodypart in choices(
            ['head', 'chest', 'legs', 'feet'],
            weights=[15, 5 + self.game.difficulty * 5, 5, 10],
                k=self.game.difficulty):

            def filterPart(item):
                return item[1]["slot"] == bodypart

            filtered = filter(filterPart, ARMOR.items())
            filtered_list = [i for i in filtered]

            if len(filtered_list):
                key, value = choice(filtered_list)
                self.equip_armor(Armor(
                    key,
                    ITEMS[value['image_name']],
                    value['image_name'],
                    value['price'],
                    value['weight'],
                    value['shield'],
                    value['slot']))

    def save(self):
        """saves the enemy's characteristic into game_data

        """
        return {
            "class": self.type_class,
            "type": self.type,
            "pos": {
                "x": self.pos.x,
                "y": self.pos.y
            },
            "health": self.health,
            "equipments": self.save_equipments(),
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

    def update(self):
        self.now = pg.time.get_ticks()
        if self.now - self.last_timestamp > 5000:
            self.last_timestamp = self.now
            self.player_spotted = None
            self.goto = []

        if self.skip:
            self.end = False
            self.skip = False
            self.last_timestamp2 = None
            self.game.versus_manager.check_characters_actions(show=False)
        elif self.end:
            if self.spawned:
                self.number_actions = 0
            self.end_time += self.game.dt
            if self.end_time > (WAIT_TIME / 1000):
                self.end_time = 0
                self.end = False
                self.fleeing = False
                self.last_timestamp2 = None
                self.game.versus_manager.check_characters_actions()
        else:
            """ reset player spotted every 10 seconds
            """

            if self.game.versus_manager.active:
                """ If a player is in sight, evaluate whether he is worth attacking or not
                """
                if self.last_timestamp2 is None:
                    self.last_timestamp2 = self.now
                if self.now - self.last_timestamp2 > 3500:
                    self.end_move()
                elif self.player_detection():
                    if self.evaluation() or self.fleeing:
                        self.acc = self.flee(self.player_spotted.pos)
                        self.fleeing = True
                    else:
                        """ if player out of reach, "pathfind" him
                        """
                        self.game.turn_manager.selected_enemy = self.player_spotted
                        if self.move_or_attack():
                            if not self.goto:
                                self.goto = self.path_finding(self.player_spotted.pos)
                                if self.goto:
                                    del self.goto[0]
                            if self.goto:
                                self.acc = self.seek(self.goto[0].coor)
                                if self.goto[0].coor.x - 32 <= self.pos.x <= self.goto[0].coor.x + 32 and self.goto[0].coor.y - 32 <= self.pos.y <= self.goto[0].coor.y + 32:
                                    del self.goto[0]
                            else:
                                self.vel = vec(0, 0)
                                self.moving = False
                                self.game.logs.add_log(f'The {self} moved.')
                                self.end_move()
                        else:
                            self.attack()
                else:
                    self.skip_turn()

            elif self.player_detection():
                if self.evaluation() or self.fleeing:
                    self.acc = self.flee(self.player_spotted.pos)
                    self.fleeing = True
                else:
                    if not self.goto:
                        self.goto = self.path_finding(self.player_spotted.pos)
                        if self.goto:
                            del self.goto[0]
                    if self.goto:

                        self.acc = self.seek(self.goto[0].coor)
                        if self.goto[0].coor.x - 32 <= self.pos.x <= self.goto[0].coor.x + 32 and self.goto[0].coor.y - 32 <= self.pos.y <= self.goto[0].coor.y + 32:
                            del self.goto[0]
                """if there is no player in range, just move around
                """
            else:
                if self.vel == vec(0, 0):
                    self.vel = vec(-random(), -random())
                temp = self.avoidnpc()
                if temp is True:
                    self.acc = temp
                else:
                    temp = self.avoidtraps()
                    if temp is True:
                        self.acc = temp
                    else:
                        self.acc = self.wander()

            """actual movement update
            """
            self.vel += self.acc
            if self.vel.length() > self.speed:
                self.vel.scale_to_length(self.speed)
            self.get_direction()
            self.update_image()
            self.pos += self.vel * (self.game.dt * 100)
            self.rect = self.image.get_rect()
            self.rect.center = self.pos
            self.update_collisions()
            # self.hit_rect.center = self.rect.center
            if self.game.debug and pg.time.get_ticks() % 2000 < 100:
                self.draw_vectors()

    def draw_vectors(self):
        """draws vectors and path details when debug is True
        """
        scale = 100
        # vel
        pg.draw.line(self.game.map_img, GREEN, self.pos, (self.pos + self.vel * scale), 5)
        # desired
        pg.draw.line(self.game.map_img, RED, self.pos, (self.pos + self.desired * scale), 5)
        # target
        if not self.game.versus_manager.active and not self.goto:
            normalized = self.vel.normalize() if self.vel.length() != 0 else vec(0)
            center = self.pos + normalized * WANDER_RING_DISTANCE
            pg.draw.circle(self.game.map_img, (255, 255, 255), (int(center.x), int(center.y)), WANDER_RING_RADIUS, 1)
            pg.draw.line(self.game.map_img, YELLOW, center, self.displacement, 5)
        for i in self.goto:
            rect = pg.Rect(i.coor, (SIZE, SIZE))
            pg.draw.rect(self.game.map_img, (255, 255, 255), rect)

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
        self.desired = (target - self.pos)*2
        distance = self.desired.length()
        self.desired.normalize_ip()
        if distance < APPROACH_RADIUS:
            self.desired *= distance / APPROACH_RADIUS * self.speed
        else:
            self.desired *= self.speed
        steer = (self.desired - self.vel)
        if steer.length() > SEEK_FORCE:
            steer.scale_to_length(SEEK_FORCE)
        return steer

    def wander(self):
        """advanced wandering occuring every 5 to 10 seconds

        Returns:
            vec(x,y): acceleration vector that self should use to reach the target
        """
        circle_pos = self.pos + self.vel.normalize() * WANDER_RING_DISTANCE
        target = circle_pos + vec(WANDER_RING_RADIUS, 0).rotate(uniform(0, 360))
        self.displacement = target
        return self.seek(target)

    def flee(self, target, FLEE_DISTANCE=10*TILESIZE):
        """makes the npc run away from the target

        Args:
            target (vec(x,y)): position of the target

        Returns:
            vec(x,y): acceleration vector that self should use to reach the target
        """
        steer = vec(0, 0)
        dist = self.pos - target
        if dist.length() < FLEE_DISTANCE and dist.length() != 0:
            self.desired = dist.normalize() * self.speed
        else:
            if self.vel == vec(0, 0):
                self.vel = vec(random(), random())
            self.desired = self.vel.normalize() * self.speed
        steer = (self.desired - self.vel)
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
        i = 0
        open_set = [start]
        closed_set = []

        start.f = start.g + (self.pos - goalvec).length()

        """boucle de recherche de chemin
        """
        while open_set and i < 50:
            i += 1
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

            open_set.remove(current)
            closed_set.append(current)

            """exploration des voisins
            """
            for neigh in current.neighbor():
                """skip murs
                """
                rect = pg.Rect(neigh.coor, (10, 10))
                for wall in self.game.walls.sprites():
                    skip = False
                    if wall.rect.colliderect(rect):
                        skip = True
                        if self.game.debug:
                            pg.draw.rect(self.game.map_img, (0, 0, 0), rect)
                        break
                if skip:
                    continue
                """skip murs
                """
                for trap in self.game.traps.sprites():
                    skip = False
                    if trap.rect.colliderect(rect):
                        skip = True
                        if self.game.debug:
                            pg.draw.rect(self.game.map_img, (0, 0, 0), rect)
                        break
                if skip:
                    continue
                """skip portes
                """
                for door in self.game.doors.sprites():
                    skip = False
                    if door.rect.colliderect(rect):
                        skip = True
                        if self.game.debug:
                            pg.draw.rect(self.game.map_img, (0, 0, 0), rect)
                        break
                if skip:
                    continue
                """skip coffres
                """
                for chest in self.game.chests.sprites():
                    skip = False
                    if chest.rect.colliderect(rect):
                        skip = True
                        if self.game.debug:
                            pg.draw.rect(self.game.map_img, (0, 0, 0), rect)
                        break
                if skip:
                    continue

                """skip personnages
                """
                for enemy in enemies:
                    skip = False
                    if enemy.rect.colliderect(rect):
                        skip = True
                        if self.game.debug:
                            pg.draw.rect(self.game.map_img, (0, 0, 0), rect)
                        break
                if skip:
                    continue

                for merchant in self.game.merchants.sprites():
                    skip = False
                    if merchant.rect.colliderect(rect):
                        skip = True
                        if self.game.debug:
                            pg.draw.rect(self.game.map_img, (0, 0, 0), rect)
                        break
                if skip:
                    continue

                """skip out of bounds
                """
                if neigh.coor.x < 0 or neigh.coor.y < 0:
                    continue
                """skip noeuds explorés
                """
                skip = False
                if closed_set:
                    for noeudexplored in closed_set:
                        if neigh.coor//TILESIZE == noeudexplored.coor//TILESIZE:
                            skip = True
                            break
                if skip:
                    continue
                """le voisin est une case valide à explorer, il est ajouté aux cases à explorer
                """
                gtry = current.g + (current.coor - neigh.coor).length()
                if neigh.g == 0 or gtry < neigh.g:
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
                                break
                        if not skip2:
                            open_set.append(neigh)
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
                    if self.game.debug:
                        logger.info(f'{self} avoids {sprite} at positions {self.pos} and {sprite.pos}')
                    return Enemy.flee(self, sprite.pos)
        return False

    def avoidtraps(self):
        """make every npc avoid one another

        Returns:
            vector: if there are ennemies colliding return an acceleration vector to avoid it
        """
        collision = pg.sprite.spritecollide(self, self.game.traps, False)
        if collision:
            return self.flee(vec(collision[0].x, collision[0].y))
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
        # logger.info(self.health_percentage()//25 - 5 + self.game.difficulty > (Character.groupCount(self.player_spotted, players.sprites()) - self.groupCount(enemies.sprites())))
        return self.health_percentage() // 25 - 5 + self.game.difficulty < (Character.groupCount(
            self.player_spotted, players.sprites()) - self.groupCount(enemies.sprites()))

    def move_or_attack(self):
        """decides whether to attack or move this turn
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
        if self.classe == "wizard" and self.cooldown - self.game.turn_manager.turn < 0:
            spawn = Enemy(self.game, self.pos.x + randint(-1*TILESIZE, 1*TILESIZE),
                          self.pos.y + randint(-1*TILESIZE, 1*TILESIZE), self.type, f'{self.type}_F')
            self.game.turn_manager.add_character(spawn)
            self.game.versus_manager.logs.add_log(f"The {self} used magic to invoke a {spawn} !")
            self.cooldown += 20
            self.spawned = True
        else:
            self.game.versus_manager.selected_enemy = self.player_spotted
            if self.game.versus_manager.check_dice():
                damage = self.game.versus_manager.calc_damage()
                self.game.turn_manager.remove_health(damage, self.player_spotted)
                # if self.player_spotted.health <= 0:
                #     self.game.versus_manager.kill_enemy(self.player_spotted)
            else:
                self.game.versus_manager.calc_damage()
                self.game.versus_manager.logs.add_log(f'The {self} missed his attack...')
        self.end_move()

    def end_move(self):
        """ends enemy's turn
        """
        self.fleeing = False
        self.goto = []
        self.moving = False
        self.end = True

    def skip_turn(self):
        """skip enemy's turn
        """
        self.skip = True
        self.number_actions = 0
        self.end_move()


class Boss(Enemy):
    """boss class that is basically a non moving enemy
    """

    def __init__(self, game, x, y, _type, images):
        super(Boss, self).__init__(game, x, y, _type, images)

        self.vel = vec(0, 0)

        self.attack_range = TILESIZE * 3

    def update(self):
        if self.end:
            if self.spawned:
                self.number_actions = 0
            self.end_time += self.game.dt
            if self.end_time > (WAIT_TIME / 1000):
                self.end = False
                self.game.versus_manager.check_characters_actions()
        elif self.game.versus_manager.active:
            if self.player_detection():
                if (self.player_spotted.pos - self.pos).length() < self.attack_range:
                    self.attack()
                else:
                    self.end_move()
            else:
                self.skip_turn()
        else:
            self.update_image()
            self.update_collisions()
