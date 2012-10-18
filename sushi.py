import ImageGrab
import time
from autopy import mouse
from autopy.bitmap import capture_screen
from autopy.bitmap import Bitmap
from threading import Timer
import sys


#autodetects where's the game window:
def autodetect(): #HACK HACK HACK HACK HACK
    '''Returns a tuple with the (x,y) value of the top-left corner
    of the game's frame. To be fed to globals x_pad and y_pad.'''
    cords = capture_screen().find_bitmap(Bitmap.from_string('b2,2,eNpjYICC8pYJAAMJAYz='))
    
    if cords == None:
        cords = capture_screen().find_bitmap(Bitmap.from_string('b4,4,eNr7/x8FMMAAhI0sDmEAADweIOA='))
        return cords
    else:
        cords = map(lambda x: x-1, cords) #fix offset
        return cords

try:
    x_pad, y_pad = autodetect()
except TypeError:
    raise SystemExit("Game window not found")

#globals
tables = {0: [0,   106], #lazy division
          1: [107, 212], #TODO: get more accurate coordinates
          2: [213, 318],
          3: [319, 424],
          4: [425, 530],
          5: [530, 640]}

order = {'gunkanmaki' : '\x7f\x00;;hh;;;;\x94\x94\x94\x94\x94;;;;;;;;\x00\x7f',
         'california' : '\x7f\x00\xde\xde\xbb\xbb\xde\xde\xff\xff;;;;;\xff\xff\xde\xde\xbb\xbb\xde\xde\x00\x7f',
         'onigiri'    : '\xe7\xe7\xe7\xe7\xff\xff\xe7\xe7\xe7\xe7\xe7\xe7\xe7\xe7\xe7\xe7\xe7\xbb\xbb\xe7\xe7',
         'salmonroll' : '\xff\xff\xff\xff\xde\xde\xde\xde\xde\xde\xde\xde\xab\xab\xab\xab\xab\xde\xde\xab\xab\xab\xab\xde\xde\xff',
         'shrimpsushi': '\x00\x00\x00\x00\x00\x00\x8b\x8b\xd8\xd8\xab\xab\xd8\xd8\xff\xff\x00\x00;;;;;;;\x00\x00\x00\x00\xd8\xd8',
         'unagiroll'  : '\x7f\x00GGtt\x8c\x8ctttt\x00\x00;;;;;;;\x00\x00\x00\x00tttttt\x8c\x8cGG\x00\x7f',
        }

recipe = {'onigiri':     ['rice', 'rice', 'nori'],
          'california':  ['rice', 'nori', 'roe'],
          'gunkanmaki':  ['rice', 'nori', 'roe', 'roe'],
          'salmonroll':  ['rice', 'nori', 'salmon', 'salmon'],
          'shrimpsushi': ['rice', 'nori', 'shrimp', 'shrimp'],
          'unagiroll':   ['rice', 'nori', 'unagi', 'unagi']
          }

class Client:
    served = {0:False, 1:False, 2:False, 3:False, 4:False, 5:False}

def doneeating(client, c):
    client.served[c] = False
    print "customer number %d has finished eating\n" % int(c)
    cleartables()

def mainloop(): #TODO
    client = Client()
    i = Inventory()
    GameOver = False
    LevelOver = False
    while not LevelOver:
        for c in range(6):
            wish = getcustomer(c)
            if client.served[c] == False and wish != None:
                i.make(wish)
                client.served[c] = wish
                print "Served client number %d" % c
                Timer(5+(c*3), doneeating, [client, c]).start()

        #LevelOver = True

#temp for testing
gunkanmaki  = 'gunkanmaki'
onigiri     = 'onigiri'
california  = 'california'
salmonroll  = 'salmonroll'
shrimpsushi = 'shrimpsushi'
unagiroll   = 'unagiroll'
shrimp      = 'shrimp'
rice        = 'rice'
nori        = 'nori'
roe         = 'roe'
salmon      = 'salmon'
unagi       = 'unagi'

class Ingred:
    shrimp = (35, 333)
    rice   = (91, 333)
    nori   = (35, 390)
    roe    = (91, 390)
    salmon = (35, 443)
    unagi  = (91, 443)

class Coord:
    phone         = (593, 369)  #phonea
    menu_toppings = (528, 276)  #topping menu
    t_shrimp      = (463, 207)  #shrimp
    t_unagi       = (545, 211)  #unagia
    t_nori        = (463, 265)  #nori
    t_roe         = (545, 275)  #roe
    t_salmon      = (461, 326)  #salmon
    t_rice        = (545, 283)  #ricebuy
    delivery_norm = (499, 298)  #normal delivery
    menu_rice     = (504, 293)  #rice

    closemenu     = (591, 336)  #close buy menu

    mat = (196, 437)

    plates = ((80, 204),
             (181, 207),
             (282, 209),
             (383, 208),
             (485, 209),
             (585, 204))

class Inventory:
    def __init__(self):
        pass

    def screengrab(self):
        box = (x_pad, y_pad, x_pad+640, y_pad+480)
        im = ImageGrab.grab(box)
        return im

    toppings = {'shrimp':5,
                'unagi':5,
                'salmon':5,
                'nori':10,
                'roe':10,
                'rice':10}

    def make(self, food, amount = 1):
        if food == None:
            return
        for times in range(amount):
            for ingredient in recipe[food]:
                if self.toppings[ingredient] <= 3:
                    print 'Not enough ingredients'
                    self.check()
                    return
            #print 'Ingredients on mat:',
            for item in recipe[food]:
                self.toppings[item] -= 1
                click(getattr(Ingred, item))
                #print 'Put ingredient %s on mat' % item
                #print item,
                time.sleep(0.1)
            click(Coord.mat)
            cleartables()
            time.sleep(0.3)
            print 'Finished making', food
            self.check()

    def check(self):
        for food, amount in self.toppings.items():
            if amount <= 4:
                print 'Amount of %s is low' % food
                self.buy(food)

    def buy(self, name):
        click(Coord.phone)
        if name == 'rice':
            click(Coord.menu_rice)
            click(Coord.t_rice)
        else:
            click(Coord.menu_toppings)                               #normalgray       ricegray
        if self.screengrab().getpixel(getattr(Coord, 't_'+name)) in ((109, 123, 127), (127, 127, 127)):
            click(Coord.closemenu)
            print 'Not enough money to buy', name
        else:
            click(getattr(Coord, 't_'+name))
            if name in ('shrimp', 'salmon', 'unagi'):
                self.toppings[name] += 5
                print 'Bought 5 more', name
            else:
                self.toppings[name] += 10
                print 'Bought 10 more', name
            click(Coord.delivery_norm)
            time.sleep(1)
        cleartables()


def getline(fn):
    ordersline = (x_pad, y_pad+64, x_pad+640, y_pad+65)
    ImageGrab.grab(ordersline).save(fn)

def getbox(fn):
    ImageGrab.grab((x_pad, y_pad, x_pad+640, y_pad+480)).save(fn)

def encode(fn):
    import Image
    return Image.open(fn).convert('L').tostring()

def click(cord):
    mouse.move(x_pad+cord[0], y_pad+cord[1])
    mouse.click()
    time.sleep(0.1)

def startgame():
    menus = ((309, 205), (318, 391), (584, 453), (319, 378))
    map(click, menus)
    print 'Starting game!'

def cleartables():
    map(click, Coord.plates)
    #print 'plates cleared'

def opengame():
    import webbrowser
    webbrowser.open('http://www.miniclip.com/games/sushi-go-round/en/')

def getcustomer(n):
    counter = ImageGrab.grab((x_pad+tables[n][0], y_pad+64, \
              x_pad+tables[n][1], y_pad+65)).convert('L').tostring()
    for food, wish in order.iteritems():
        if wish in counter:
            return food
    return None

i = Inventory()

def main():
    if len(sys.argv) > 2:
        eval(sys.argv[1]+'('+sys.argv[2]+')')
    elif len(sys.argv) >1:
        eval(sys.argv[1]+'()')
    else:
        i = Inventory()
        print 'Initialized!'
        print 'Available recipes:'
        for k, v in recipe.iteritems():
            print k
        startgame()
        mainloop()

if __name__ == '__main__':
    main()