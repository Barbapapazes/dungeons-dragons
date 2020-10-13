import pygame
import sys
import random
from settings import *
from Items import *
from Person import *


class Game():
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.myfont = pygame.font.SysFont('Calibri', 25)
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()


    def New(self):
        # Items
        sword_steel = Weapon('img/sword.png', "a", 20,5)
        #sword_wood = Weapon('img/swordWood.png', "pas ouf", 10, 'sword')
        #hp_potion = Consumable('img/potionRed.png', 2, 30)
        #helmet_armor = Armor('img/helmet.png', 10, 20, 'head')
        #chest_armor = Armor('img/chest.png', 10, 40, 'chest')
        #upg_helmet_armor = Armor('img/upg_helmet.png', 10, 40, 'head')
        #upg_chest_armor = Armor('img/upg_chest.png', 10, 80, 'chest')

        self.all_sprites = pygame.sprite.Group()
        self.all_coins = pygame.sprite.Group()
        self.player = Person(self)
        #self.coin = Coin(self, random.randrange(0, GRIDWIDTH), random.randrange(0, GRIDHEIGHT))
        self.inventory = Inventory(self.player, 20, 5, 4)

        #self.inventory.addItemInv(helmet_armor)
        #self.inventory.addItemInv(hp_potion)
        self.inventory.addItemInv(sword_steel)
        #self.inventory.addItemInv(sword_wood)
        #self.inventory.addItemInv(chest_armor)
        #self.inventory.addItemInv(upg_helmet_armor)
        #self.inventory.addItemInv(upg_chest_armor)
        g.run()


    def run(self):
        # game loop
        while True:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pygame.quit()
        sys.exit()

    def update(self):
        # game loop update
        self.all_sprites.update()
        self.player.update()
        self.all_coins.update()

    def events(self):
            # game loop events
        for event in pygame.event.get():
        # check for closing window
            if event.type == pygame.QUIT:
                self.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.player.move(0, -1)
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.player.move(0, 1)
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.player.move(-1)
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.player.move(1)
                if event.key == pygame.K_b:
                    self.inventory.toggleInventory()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                if self.inventory.display_inventory:
                    mouse_pos = pygame.mouse.get_pos()
                    self.inventory.checkSlot(self.screen, mouse_pos)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.inventory.display_inventory:
                    self.inventory.moveItem(self.screen)
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if self.inventory.display_inventory:
                    self.inventory.placeItem(self.screen)

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pygame.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pygame.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw_player_stats(self):
        self.PV = self.myfont.render(f"{self.player.PV}" , False, RED)
        #self.prot = self.myfont.render(f"{self.player.prot}" , False, WHITE)
        #self.atk = self.myfont.render(f"{self.player.atk}" , False, WHITE)
        #self.coins = self.myfont.render(f"{self.player.p_coins}" , False, GOLD)
        #self.hpimg = pygame.image.load('img/heart.png').convert_alpha()
        #self.protimg = pygame.image.load('img/upg_shieldSmall.png').convert_alpha()
        #self.atkimg = pygame.image.load('img/upg_dagger.png').convert_alpha()
        #self.coinimg = pygame.image.load('img/coin1.png').convert_alpha()
        #self.screen.blit(self.hp,(STATPOSX,25))
        #self.screen.blit(self.prot,(STATPOSX,75))
        #self.screen.blit(self.atk,(STATPOSX,125))
        #self.screen.blit(self.coins,(STATPOSX,175))
        #self.screen.blit(self.hpimg,(STATPOSX-50,5))
        #self.screen.blit(self.protimg,(STATPOSX-50,55))
        #self.screen.blit(self.atkimg,(STATPOSX-50,105))
        #self.screen.blit(self.coinimg,(STATPOSX-55,155))


    def draw(self):
        # game loop draw
        self.screen.fill(BGCOLOR)
        self.draw_grid()
        self.all_sprites.draw(self.screen)
        self.inventory.draw(self.screen)
        self.draw_player_stats()
        # flipping display after drawing
        pygame.display.flip()

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass


g = Game()
while True:
    g.New()

pygame.quit()
sys.exit()