from time import sleep
from random import randint
import os
import subprocess
import keyboard

events = [
    "a",  # Move left
    "d",  # Move right
    "w",  # Move up
    "s",  # Move down
    "space",  # Fire
    "esc"  # Exit game
    
]
width = 20
height = 25

def get_event():
    for event in events:
        if keyboard.is_pressed(event):
            return event
    return None

def clear_screen():
    command = 'cls' if os.name == 'nt' else 'clear'
    subprocess.run(command, shell=True)

class GameMap:
    def __init__(self, width, height, tickspeed=0.2, mapHolder="_"):
        self.width = width
        self.height = height
        self.objects = []
        self.tickspeed = tickspeed
        self.mapHolder = mapHolder
        self.map = [[mapHolder]*width for _ in range(height)]

    def _print(self):
        for row in self.map:
            print(" ".join(row))

    def _clear(self):
        self.map = [[self.mapHolder]*self.width for _ in range(self.height)]
        
    def _update(self):
    
        
        for obj in self.objects:
            if keyboard.is_pressed('esc'):
                print("Exiting game...")
                exit()

            event = get_event()
            if event:
                obj.event(event)
            obj.update()
            self.map[obj.y][obj.x] = obj.symbol
            
    def removeObjectByPos(self, x, y):
        self.objects = [obj for obj in self.objects if not (obj.x == x and obj.y == y)]
        
    def getObjectByPos(self, x, y):
        for obj in self.objects:
            if obj.x == x and obj.y == y:
                return obj
        return None
            
    def addObject(self, obj):
        obj.game_map = self
        self.objects.append(obj)
        
    def draw(self):
        self._clear()
        self._update()
        self._print()
        
    def gui(self):
        print("Press 'A' to move left, 'D' to move right. Avoid the falling blocks!")
        print("-" * (self.width * 2 - 1))
        print("Press 'esc' to exit.")

    def gameLoop(self):
        while True:
            self.draw()
            sleep(self.tickspeed)
            print("\n" * 5)
            clear_screen()
        


class GameObject:
    def __init__(self, x, y, symbol):
        self.x = x
        self.y = y
        self.vy = 0
        self.symbol = symbol
        self.game_map = None
        
    def move(self, dx=0, dy=0):
        if self.colide(dx, dy):
            self.vy = 0
            return
        self.x += dx
        self.y += dy
        
    def event(self, event: str):
        pass   
        
    def update(self):
        pass
    
    def colide(self, dx=0, dy=0):
        if self.game_map is None:
            return False
        if not (0 <= self.x + dx < self.game_map.width) or not (0 <= self.y + dy < self.game_map.height):
            return True
        return any(obj.x == self.x + dx and obj.y == self.y + dy for obj in self.game_map.objects if obj != self)

class Block(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, "#")

def meteorStrike(game_map, x):
    falling_block = FallingBlock(x, 0)
    game_map.addObject(falling_block)


class FallingBlock(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, "O")
        self.vy = 1

    def update(self):
        self.move(0, self.vy)
        
        
        
class Player(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, "A")
        
    def event(self, event):
        if event == "a":
            self.move(dx=-1)
        elif event == "d":
            self.move(dx=1)
        elif event == "w":
            self.move(dy=-1)
        elif event == "s":
            self.move(dy=1)
        if event == "space":
            fire = Fire(self.x, self.y - 1)
            self.game_map.addObject(fire)

class Fire(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, "*")
        self.vy = -1

    def update(self):
        if self.colide(0, self.vy):
            self.game_map.removeObjectByPos(self.x, self.y)
            obj = self.game_map.getObjectByPos(self.x, self.y + self.vy)
            if isinstance(obj, FallingBlock):
                self.game_map.removeObjectByPos(self.x, self.y + self.vy)
            return
        self.move(0, self.vy)
            
        
        


if __name__ == "__main__":
    game_map = GameMap(width, height, tickspeed=0.05, mapHolder="   ")
    player = Player(width // 2, height - 2)
    game_map.addObject(player)
    meteorStrike(game_map, randint(0, width - 1))
    game_map.gameLoop()