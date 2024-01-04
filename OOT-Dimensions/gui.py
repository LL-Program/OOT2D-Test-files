import pygame 
def create_button(button, image, position, callback):
    button["image"] = image
    button["rect"] = image.get_rect(topleft=position)
    button["callback"] = callback

 
def button_on_click(button, event):
    if event.button == 1:
        if button["rect"].collidepoint(event.pos):
            button["callback"](button)
 
def push_button_goodbye(button):
    print("You push Goodbye button")
 
# Define your button
button = {}
# Create button

def nbut(x,y, gameDisplay, carImg):
    gameDisplay.blit(carImg, (x,y))