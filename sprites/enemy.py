"""Define a enemy"""

from sprites.character import *
from inventory.inventory import Armor
from config.colors import GREEN, YELLOW, RED
from config.window import TILESIZE
from utils.cell import Cell
from random import choices, random, uniform, randint
from config.sprites import ASSETS_SPRITES, ARMOR, ITEMS, WAIT_TIME
vec = pg.math.Vector2

# npc settings
MOB_HIT_RECT = pg.Rect(0, 0, 30, 30)
SIZE = 8
SEEK_FORCE = 0.1
APPROACH_RADIUS = 50
WANDER_RING_DISTANCE = 500
WANDER_RING_RADIUS = 150
CLASSES = ["fighter", "rogue", "wizard", "boss"]
TYPE = {
    "skeleton": {"health": 50, "STR": 35, "DEX": 20, "CON": 20, "INT": 50, "WIS": 30, "CHA": 30},
    "goblin":   {"health": 60, "STR": 45, "DEX": 50, "CON": 25, "INT": 20, "WIS": 15, "CHA": 10},
    "phantom":   {"health": 70, "STR": 30, "DEX": 35, "CON": 30, "INT": 40, "WIS": 30, "CHA": 10},
    "boss": {"health": 250, "STR": 70, "DEX": 25, "CON": 50, "INT": 20, "WIS": 10, "CHA": 40}
}


class Enemy(Character):
    def __init__(self, game, x, y, _type, images):
        self.goto = []
        self.groups = enemies
        pg.sprite.Sprite.__init__(self, self.groups)
        super(Enemy, self).__init__(game, x, y, _type, images, MOB_HIT_RECT)
        self.type_class = images
        self.images = ASSETS_SPRITES[images]
        self.image = next(self.images[self.direction])
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.hit_rect = MOB_HIT_RECT
        self.hit_rect.center = self.rect.center

        self.end = False
        self.end_time = 0

        self.pos = vec(x, y)
        self.vel = vec(1, 1).rotate(uniform(0, 360))
        self.acc = vec(0, 0)

        self.last_timestamp = 0
        self.last_timestamp2 = None
        self.now = 0
        self.cooldown = 1
        self.spawned = False
        self.cooldown = randint(15, 25)

        self.attack_range = TILESIZE * 2

        self.speed = 1.5

        self.target = self.pos
        self.player_spotted = None

        self.view_range = TILESIZE * 6
        self.moving = False

        if images[-1] == 'F':
            self.classe = CLASSES[0]
            self.xp = 10
        elif images[-1] == 'R':
            self.classe = CLASSES[1]
            self.xp = 10
        elif images[-1] == 'W':
            self.classe = CLASSES[2]
            self.xp = 20
        else:
            self.classe = CLASSES[3]
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
        self.difficulty_tweeking()

    def throw_inventory(self):
        """drop every item stored inside the enemy's inventory
        """
        for slot in self.inventory.slots:
            if slot.item:
                self.inventory.throw_item(slot.item)

    def __str__(self):
        """default displayed text whenever printing the enemy
        """
        return f'{self.type} {self.classe}'

    def difficulty_tweeking(self):
        """tweeks ennemy's statistics to match game difficulty
        """
        self.characteristics['str'] += 5 * self.game.difficulty
        self.characteristics['dex'] += 3 * self.game.difficulty
        self.characteristics['con'] += 4 * self.game.difficulty
        self.characteristics['int'] += 2 * self.game.difficulty
        self.characteristics['wis'] += 1 * self.game.difficulty
        self.characteristics['cha'] += 2 * self.game.difficulty
        for bodypart in choices(
            ['head', 'chest', 'legs', 'feet'],
            weights=[15, 5 + self.game.difficulty * 5, 5, 10],
                k=self.game.difficulty):
            armor_list = []
            for part in ARMOR.items():
                # logger.info(part)
                if part[1]['slot'] == bodypart:
                    #             armor_list.append(part)
                    #     self.equip_armor(Armor(choice(armor_list), )
                    armor_list.append(part)
            for key, value in armor_list:
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
        # if trap nearby: flee(trap)
        if self.end:
            if self.spawned:
                self.number_actions = 0
            self.end_time += self.game.dt
            if self.end_time > (WAIT_TIME / 1000):
                self.end = False
                self.game.versus_manager.check_characters_actions()
        else:
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
                if self.now - self.last_timestamp2 > 3000:
                    self.end_turn()
                elif self.player_detection():
                    if self.evaluation():
                        self.flee(self.player_spotted.pos)
                    else:
                        """ if player out of reach, "pathfind" him
                        """
                        self.game.turn_manager.selected_enemy = self.player_spotted
                        if self.move_or_attack():
                            if self.now - self.last_timestamp2 > 1500 and self.vel == vec(
                                    0, 0):  # skip if stuck on a wall
                                self.player_spotted = None
                                self.moving = False
                                self.end_turn()
                            elif not self.goto:  # and not self.player_spotted.pos.x - TILESIZE/2 <= self.pos.x <= self.player_spotted.pos.x + TILESIZE/2 and not self.player_spotted.pos.y - TILESIZE/2 <= self.pos.y <= self.player_spotted.pos.y + TILESIZE/2:
                                self.goto = self.path_finding(self.player_spotted.pos)
                                if self.goto:
                                    del self.goto[0]
                            if self.goto:
                                if self.game.debug:
                                    for i in self.goto:
                                        rect = pg.Rect(i.coor, (SIZE, SIZE))
                                        pg.draw.rect(self.game.screen, (255, 255, 255), rect)
                                self.acc = self.seek(self.goto[0].coor)
                                if self.goto[0].coor.x - 32 <= self.pos.x <= self.goto[0].coor.x + 32 and self.goto[0].coor.y - 32 <= self.pos.y <= self.goto[0].coor.y + 32:
                                    del self.goto[0]
                            else:
                                self.vel = vec(0, 0)
                                self.moving = False
                                self.game.logs.add_log(f'The {self} moved.')
                                self.end_turn()
                        else:
                            self.attack()
                else:
                    self.skip_turn()

            elif self.player_detection():
                if self.evaluation():
                    self.flee(self.player_spotted.pos)
                else:
                    if not self.goto:
                        self.goto = self.path_finding(self.player_spotted.pos)
                        if self.goto:
                            if self.game.debug:
                                for i in self.goto:
                                    rect = pg.Rect(i.coor, (SIZE, SIZE))
                                    pg.draw.rect(self.game.screen, (255, 255, 255), rect)
                            self.acc = self.seek(self.goto[0].coor)
                            if self.goto[0].coor.x - 32 <= self.pos.x <= self.goto[0].coor.x + 32 and self.goto[0].coor.y - 32 <= self.pos.y <= self.goto[0].coor.y + 32:
                                del self.goto[0]
                """if there is no player in range, just move around
                """
            else:
                if self.vel == vec(0, 0):
                    self.vel = vec(-random(), -random())
                temp = self.avoidnpc()
                if temp is False:
                    self.acc = self.wander()
                else:
                    self.acc = temp

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
        logger.info(f'{self} flees {target}')
        if self.vel == vec(0, 0):
            self.vel = vec(-random(), -random())
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
                for wall in self.game.walls.sprites():
                    skip = False
                    if wall.rect.collidepoint(neigh.coor):
                        skip = True
                        break
                if skip:
                    continue
                """skip murs
                """
                for trap in self.game.traps.sprites():
                    skip = False
                    if trap.rect.collidepoint(neigh.coor):
                        skip = True
                        break
                if skip:
                    continue
                """skip portes
                """
                for door in self.game.doors.sprites():
                    skip = False
                    if door.rect.collidepoint(neigh.coor):
                        skip = True
                        break
                if skip:
                    continue
                """skip coffres
                """
                for chest in self.game.chests.sprites():
                    skip = False
                    if chest.rect.collidepoint(neigh.coor):
                        skip = True
                        break
                if skip:
                    continue

                """skip personnages
                """
                for enemy in enemies:
                    skip = False
                    if enemy.rect.collidepoint(neigh.coor):
                        skip = True
                        break
                if skip:
                    continue

                for merchant in self.game.merchants.sprites():
                    skip = False
                    if merchant.rect.collidepoint(neigh.coor):
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

            for player in self.game.turn_manager.players:
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
                    logger.info(f'{self} avoids {sprite} at positions {self.pos} and {sprite.pos}')
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
        if self.classe == "wizard" and self.cooldown - self.game.turn_manager.turn < 0:
            spawn = Enemy(self.game, self.pos.x + randint(-2*TILESIZE, 2*TILESIZE),
                          self.pos.y + randint(-2*TILESIZE, 2*TILESIZE), self.type, f'{self.type}_F')
            self.game.turn_manager.add_character(spawn)
            self.game.versus_manager.logs.add_log(f"The {self} used magic to invoke a {spawn} !")
            self.cooldown += 20
            self.spawned = True
        else:
            self.game.versus_manager.selected_enemy = self.player_spotted
            if self.game.versus_manager.check_dice():
                damage = self.game.versus_manager.calc_damage()
                self.game.turn_manager.remove_health(damage, self.player_spotted)
            else:
                self.game.versus_manager.calc_damage()
                self.game.versus_manager.logs.add_log(f'The {self} missed his attack...')
        self.end_turn()

    def end_turn(self):
        self.last_timestamp2 = None
        self.goto = []
        self.moving = False
        self.end = True

    def skip_turn(self):
        self.end_turn()
        self.number_actions = 0


class Boss(Enemy):
    def __init__(self, game, x, y, _type, images):
        super(Boss, self).__init__(game, x, y, _type, images)

        self.vel = vec(0, 0)

        self.attack_range = TILESIZE * 3

    def update(self):
        if self.game.versus_manager.active:
            if self.player_detection():
                if (self.player_spotted.pos - self.pos).length() < self.attack_range:
                    self.attack()
                else:
                    self.end_turn()
            else:
                self.skip_turn()
        else:
            self.update_image()
            self.update_collisions()
