# implementation of card game - Memory

import simplegui
import random

CARD_CONTENT=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
CARD_IS_REVEALED=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
FIRST_CARD=0
SECOND_CARD=0
CURRENT_STEP=0
TURNS=0
label=None

# helper function to initialize globals
def new_game():
    global CARD_CONTENT,CARD_IS_REVEALED,FIRST_CARD,SECOND_CARD,CURRENT_STEP,TURNS
    CARD_CONTENT=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    CARD_IS_REVEALED=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    FIRST_CARD=0
    SECOND_CARD=0
    CURRENT_STEP=1
    TURNS=0
    for x in xrange(0,16):
        tmp=random.randint(1,16)
        while(tmp in CARD_CONTENT):
            tmp=random.randint(1,16)
        CARD_CONTENT[x]=tmp
    print(CARD_CONTENT)

     
# define event handlers
def mouseclick(pos):
    global CARD_CONTENT,CARD_IS_REVEALED,FIRST_CARD,SECOND_CARD,CURRENT_STEP,TURNS
    if CARD_IS_REVEALED[pos[0]/50]==1:
        pass
    else:
        if(CURRENT_STEP==1):
            if not (CARD_CONTENT[FIRST_CARD]%8)==(CARD_CONTENT[SECOND_CARD]%8):
                CARD_IS_REVEALED[FIRST_CARD]=0
                CARD_IS_REVEALED[SECOND_CARD]=0
            CARD_IS_REVEALED[pos[0]/50]=1
            CURRENT_STEP=2
            FIRST_CARD=pos[0]/50
        else:
            SECOND_CARD=pos[0]/50
            CARD_IS_REVEALED[SECOND_CARD]=1
            CURRENT_STEP=1
            TURNS = TURNS+1
    
                        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    global label,TURNS
    label.set_text("Turns="+str(TURNS))
    for i in xrange(0,16):
        if CARD_IS_REVEALED[i]==0:
            canvas.draw_image(image,(760,909),(1520,1818),(50*i+25,50),(50,100))
        else:
            canvas.draw_text(str(CARD_CONTENT[i]%8), (50*i+7,80),80, 'White')
    pass


# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")
image = simplegui.load_image('http://commondatastorage.googleapis.com/codeskulptor-assets/gutenberg.jpg')

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric
# http://www.codeskulptor.org/#user38_zNj7Xr0Cp0_11.py