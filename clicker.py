import pygame
import pygame.gfxdraw
import time
import sys


pygame.init()
pygame.display.set_caption('BRS CLICKER')


#set screen parametres
screen_width = 1000
screen_height = 650
screen = pygame.display.set_mode((screen_width, screen_height))
gui_font = pygame.font.Font(None,30)
gui_font_for_brs = pygame.font.Font(None, 68)



#add photos
background_img = pygame.image.load("background.jpg")
botan_img = pygame.image.load("botan.png")
symbol = pygame.image.load("phystech_symbol_.png")
book_img = pygame.image.load("book.png")




#class for buttons
class Button:
    def __init__(self,text,width,height,pos,elevation):
        self.elevation = elevation
        self.dynamic_elecation = elevation
        self.top_rect = pygame.Rect(pos,(width,height))
        self.top_color = '#475F77'
        self.bottom_rect = pygame.Rect(pos,(width,height))
        self.bottom_color = '#354B5E'
        self.text = text
        self.pos = pos
        self.text_surf = gui_font.render(text,True,'#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)

    def draw(self):
        self.top_rect.y = self.pos[1] - self.dynamic_elecation
        self.text_rect.center = self.top_rect.center
        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elecation
        pygame.draw.rect(screen,self.bottom_color, self.bottom_rect,border_radius = 12)
        pygame.draw.rect(screen,self.top_color, self.top_rect,border_radius = 12)
        screen.blit(self.text_surf, self.text_rect)

    def collidepoint(self, mouse_pos):
        return pygame.Rect((self.pos[0] - 20, self.pos[1] - 20),(self.pos[0] +
            20, self.pos[1] + 20)).collidepoint(mouse_pos)



#set background photo + autoclickers
def background():
    screen.blit(background_img, (0, 0))
    clicker_symbol.add_animation()
    botan.add_animation()
    book.add_animation()



#set status of autoclickers
def your_status():
    status_botans = "Количество людей, которые вам сейчас помогают : {amount}. Они добавляют {brs_from_botans} БРС".format(amount=botan.amount, brs_from_botans=botan.get_bonus())
    status_books = "Количество заботанных задачников={amount}. Этот опыт приносит вам {brs_from_books} БРС".format(amount=book.amount, brs_from_books=book.get_bonus())

    screen.blit(gui_font.render(status_botans, True, "#FFFFFF"), (100, 500))
    screen.blit(gui_font.render(status_books, True, '#FFFFFF'), (100, 600))





#sets the parameter of clicks = BRS
class brs_():
    def __init__(self, amount, x, y):
        self.x = x
        self.y = y
        self.amount = amount

    def len_of_amount(self):
        cnt = 0
        amount_copy = self.amount
        while amount_copy != 0:
            cnt+=1
            amount_copy //= 10
        return cnt

    def brs_status(self):

     font = pygame.font.Font(None, 72)
     text = font.render("БРС : {current_amount}".format(current_amount=self.amount), True, (41, 0,
                 255))
     place = text.get_rect(center=(self.x + self.len_of_amount() * 5, self.y ))
     screen.blit(text, place)




#class for autoclickers
class brs_helpers:
    def __init__(self, img, x, y, cost, bonus, amount, time):
        self.x = x
        self.y = y
        self.img = img
        self.cost = cost
        self.bonus = bonus
        self.amount = amount
        self.time = time

    def get_bonus(self):
        return self.bonus * self.amount

    def add_animation(self):
            changed_smbl = pygame.transform.scale(self.img, (700,
                    200))
            screen.blit(self.img, (symbol.get_rect(center = (self.x + 700 /
                2, self.y + 200 / 2))))

    def autominer(self):
        time.sleep(self.time)
        brs.amount += self.get_bonus()



#class for clicker_symbol = great phystech symbol!
class phystech_symbol:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 100
        self.height = 100
        self.animation = False

    def add_animation(self):
            changed_smbl = pygame.transform.scale(symbol, (int(0.5*self.width),
                    int(0.5*self.height)))
            screen.blit(symbol, (symbol.get_rect(center = (self.x + self.width /
                2, self.y + self.height / 2))))



#set base variables
brs = brs_(0, 150, 400)
clicker_symbol = phystech_symbol(100, 100)



#add autoclickers
botan = brs_helpers(botan_img, 400, 100, 100, 1, 0, 0.1)
book = brs_helpers(book_img, 450, 320, 2000, 10, 0, 0.1)


#add buttons
botan_button = Button('Я помогу({cost} БРС)'.format(cost = botan.cost),200,40,(780,150),5)
book_button = Button('Изучить({cost} БРС)'.format(cost=book.cost),200, 40, (780, 300),5)



#add other variablew
helpers = [botan, book]
buttons = {botan : botan_button, book : book_button}
set_of_helpers = set()
is_playing = True



#main loop
while is_playing:
    for event in pygame.event.get():
        #if user clicks
        if event.type == pygame.KEYDOWN:
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                brs.amount += 1

        #if user tries to buy autoclicker
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = event.pos
                for brs_helper in helpers:
                    if buttons[brs_helper].collidepoint(mouse_pos) and brs.amount>=brs_helper.cost:
                        brs.amount -= brs_helper.cost
                        brs_helper.amount += 1
                        set_of_helpers.add(brs_helper)

        #if user is tired and wants to quit
        if event.type == pygame.QUIT:
            is_playing = False


    #add animation
    background()

    your_status()
    #set status of clicks
    brs.brs_status()

    #add autominers
    for elem in set_of_helpers:
        elem.autominer()


    #set beautiful buttons
    botan_button.draw()
    book_button.draw()


    #update user's display
    pygame.display.update()


#bye bye
pygame.quit()
