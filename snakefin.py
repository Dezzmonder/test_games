import random
import time
import tkinter


class Snake:

    def __init__(self):
        self.cv = tkinter.Canvas(width=502, height=502, background='gray')
        self.cv.pack()
        self.points = 0
        self.speed = 0.2
        self.label = tkinter.Label(text=f"Очки: {self.points}. Скорость: {1 / self.speed} клеток в секунду")
        self.label.pack()
        self.delta = [1, 0]
        self.headpos = [random.randint(10, 40), random.randint(0, 49)]
        self.tail = [(self.headpos[0] - 1, self.headpos[1]), (self.headpos[0] - 2, self.headpos[1])]
        self.tail_len = 2
        self.applepos = (random.randint(0, 49), random.randint(0, 49))
        while self.headpos == self.applepos:
            self.applepos = (random.randint(0, 49), random.randint(0, 49))
        self.head = self.cv.create_oval(self.headpos[0] * 10 + 2,
                                        self.headpos[1] * 10 + 2, self.headpos[0] * 10 + 12, self.headpos[1] * 10 + 12,
                                        fill='navy')
        self.apple = self.cv.create_oval(self.applepos[0] * 10 + 2, self.applepos[1] * 10 + 2,
                                         self.applepos[0] * 10 + 12, self.applepos[1] * 10 + 12, fill='red')
        self.tailcv = [(self.cv.create_oval(self.tail[0][0] * 10 + 2,
                                            self.tail[0][1] * 10 + 2, self.tail[0][0] * 10 + 12,
                                            self.tail[0][1] * 10 + 12, fill='blue')),
                       (self.cv.create_oval(self.tail[1][0] * 10 + 2,
                                            self.tail[1][1] * 10 + 2, self.tail[1][0] * 10 + 12,
                                            self.tail[1][1] * 10 + 12, fill='blue'))]
        self.cv.update()

    def left(self, x):
        self.delta = [-1, 0]

    def right(self, x):
        self.delta = [1, 0]

    def up(self, x):
        self.delta = [0, -1]

    def down(self, x):
        self.delta = [0, 1]

    def spawn_apple(self):
        self.applepos = (random.randint(0, 49), random.randint(0, 49))
        while self.headpos == self.applepos or self.applepos in self.tail:
            self.applepos = (random.randint(0, 49), random.randint(0, 49))
        self.cv.coords(self.apple, self.applepos[0] * 10 + 2,
                       self.applepos[1] * 10 + 2, self.applepos[0] * 10 + 12, self.applepos[1] * 10 + 12)
        self.cv.update()

    def move(self):
        self.tail.insert(0, (self.headpos[0], self.headpos[1]))
        while self.tail_len + 1 < len(self.tail):
            self.tail.pop()
        self.headpos[0] += self.delta[0]
        self.headpos[1] += self.delta[1]
        self.cv.move(self.head, self.delta[0] * 10, self.delta[1] * 10)
        c = 0
        for i in self.tailcv:
            self.cv.coords(i, self.tail[c][0] * 10 + 2,
                           self.tail[c][1] * 10 + 2, self.tail[c][0] * 10 + 12, self.tail[c][1] * 10 + 12)
            c += 1
        self.check_pos()
        time.sleep(self.speed)
        self.cv.update()

    def loose(self):
        self.delta = 0
        self.cv.delete('all')
        self.cv.create_text(152, 242, text=f'Snake, are you okay? Points:{self.points}', font=25)
        self.cv.update()

    def lvlup(self):
        self.points += 1
        self.tail_len += 1
        if self.speed > 0.05:
            self.speed -= 0.01
        self.tailcv.append((self.cv.create_oval(self.tail[-1][0] * 10 + 2,
                                                self.tail[-1][1] * 10 + 2, self.tail[-1][0] * 10 + 12,
                                                self.tail[-1][1] * 10 + 12, fill='blue')))
        self.label.configure(text=f"Очки: {self.points}. Скорость: {1 / self.speed} клеток в секунду")
        self.label.update()
        self.spawn_apple()

    def check_pos(self):
        if self.headpos[0] == self.applepos[0] and self.headpos[1] == self.applepos[1]:
            self.lvlup()
        elif (self.headpos[0], self.headpos[1]) in self.tail:
            self.loose()
        elif self.headpos[0] < 0 or self.headpos[0] > 49:
            self.loose()
        elif self.headpos[1] < 0 or self.headpos[1] > 49:
            self.loose()


win = tkinter.Tk()
snake = Snake()
win.bind('<a>', snake.left)
win.bind('<d>', snake.right)
win.bind('<w>', snake.up)
win.bind('<s>', snake.down)
while snake.delta != 0:
    snake.move()
win.mainloop()
