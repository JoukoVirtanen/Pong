from Tkinter import *
import tkFont
import random

FRAMES_PER_SECOND=60.0
SCREEN_WIDTH=600
SCREEN_HEIGHT=400
BALL_RADIUS=20
PAD_WIDTH=8
PAD_HEIGHT=80

X=0
Y=1

LEFT=False
RIGHT=True

def keyUp(e, app):
    if e.char=='s':
        app.paddle1_vel=0
    if e.char=='w':
        app.paddle1_vel=0
    if e.keysym_num==65364:
        app.paddle2_vel=0
    if e.keysym_num==65362:
        app.paddle2_vel=0

def keyDown(e, app):
    if e.char=="s":
        app.paddle1_vel=1
    if e.char=="w":
        app.paddle1_vel=-1
    if e.keysym_num==65364:
        app.paddle2_vel=1
    if e.keysym_num==65362:
        app.paddle2_vel=-1

class MainApp(Tk):
    def __init__(self):
        Tk.__init__(self)

        self.canvas=Canvas(self, width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
        self.canvas.pack()

        self.canvas.bind("<KeyRelease>", lambda e: keyUp(e, self))
        self.canvas.bind("<KeyPress>", lambda e: keyDown(e, self))
        self.canvas.focus_set()

        self.paddle1_pos=SCREEN_HEIGHT/2-PAD_HEIGHT/2
        self.paddle2_pos=SCREEN_HEIGHT/2-PAD_HEIGHT/2

        self.paddle1_vel=0
        self.paddle2_vel=0

        self.ball_pos=[SCREEN_WIDTH/2, SCREEN_HEIGHT/2]
        self.ball_vel=[0, 0]
        self.spawnBall(RIGHT)

        self.score1=0
        self.score2=0
        

    def draw(self):
        self.canvas.delete(ALL)

        score_font=tkFont.Font(family='Helvetica', size=24, weight='bold')

        self.canvas.create_text(0.1*SCREEN_WIDTH, 0.1*SCREEN_HEIGHT, font=score_font, text=str(self.score1))
        self.canvas.create_text(0.9*SCREEN_WIDTH, 0.1*SCREEN_HEIGHT, font=score_font, text=str(self.score2))
        self.canvas.create_line(SCREEN_WIDTH/2, 0, SCREEN_WIDTH/2, SCREEN_HEIGHT, fill="white")
        self.canvas.create_line(PAD_WIDTH, 0, PAD_WIDTH, SCREEN_HEIGHT, fill="white")
        self.canvas.create_line(SCREEN_WIDTH-PAD_WIDTH, 0, SCREEN_WIDTH-PAD_WIDTH, SCREEN_HEIGHT, fill="white")
        
        #Update ball
        if self.ball_pos[Y]<BALL_RADIUS or self.ball_pos[Y]>SCREEN_HEIGHT-BALL_RADIUS:
            self.ball_vel[Y]=-self.ball_vel[Y]

        self.ball_pos[X]+=self.ball_vel[X]
        self.ball_pos[Y]+=self.ball_vel[Y]

        #Draw ball
        x1=self.ball_pos[X]-BALL_RADIUS
        y1=self.ball_pos[Y]-BALL_RADIUS
        x2=self.ball_pos[X]+BALL_RADIUS
        y2=self.ball_pos[Y]+BALL_RADIUS
        self.canvas.create_oval(x1, y1, x2, y2, fill="red")

        #Update paddle's vertical position, keep paddle on the screen  
        self.paddle1_pos+=self.paddle1_vel
        self.paddle2_pos+=self.paddle2_vel

        if self.paddle1_pos+PAD_HEIGHT/2>SCREEN_HEIGHT:
            self.paddle1_pos=SCREEN_HEIGHT-PAD_HEIGHT/2
            self.paddle1_vel=0

        if self.paddle1_pos-PAD_HEIGHT/2<0:
            self.paddle1_pos=PAD_HEIGHT/2
            self.paddle1_vel=0

        if self.paddle2_pos+PAD_HEIGHT/2>SCREEN_HEIGHT:
            self.paddle2_pos=SCREEN_HEIGHT-PAD_HEIGHT/2
            self.paddle2_vel=0

        if self.paddle2_pos-PAD_HEIGHT/2<0:
            self.paddle2_pos=PAD_HEIGHT/2
            self.paddle2_vel=0

        #Draw paddles
        x1=0
        y1=self.paddle1_pos-PAD_HEIGHT/2
        x2=PAD_WIDTH
        y2=self.paddle1_pos+PAD_HEIGHT/2
        self.canvas.create_rectangle(x1, y1, x2, y2, fill="red")

        x1=SCREEN_WIDTH-PAD_WIDTH
        y1=self.paddle2_pos-PAD_HEIGHT/2
        x2=SCREEN_WIDTH
        y2=self.paddle2_pos+PAD_HEIGHT/2
        self.canvas.create_rectangle(x1, y1, x2, y2, fill="red")

        #Determine whether paddle and ball collide
        if self.ball_pos[X]-BALL_RADIUS<PAD_WIDTH:
            if self.ball_pos[Y]>self.paddle1_pos+PAD_HEIGHT/2 or self.ball_pos[Y]<self.paddle1_pos-PAD_HEIGHT/2:
                self.spawnBall(RIGHT)
                self.score2+=1
            else:
                self.ball_vel[X]=-self.ball_vel[X]
                self.ball_pos[X]+=self.ball_vel[X]
                self.ball_vel[X]*=1.05
                self.ball_vel[Y]*=1.05

        if self.ball_pos[X]+BALL_RADIUS+PAD_WIDTH>SCREEN_WIDTH:
            if self.ball_pos[Y]>self.paddle2_pos+PAD_HEIGHT/2 or self.ball_pos[Y]<self.paddle2_pos-PAD_HEIGHT/2:
                self.spawnBall(LEFT)
                self.score1+=1
            else:
                self.ball_vel[X]=-self.ball_vel[X]
                self.ball_pos[X]+=self.ball_vel[X]
                self.ball_vel[X]*=1.05
                self.ball_vel[Y]*=1.05
        
        self.after(1, self.draw)

        

    def spawnBall(self, direction):
        self.ball_pos=[SCREEN_WIDTH/2, SCREEN_HEIGHT/2]
        self.ball_vel[X]=random.uniform(30.0/FRAMES_PER_SECOND, 60.0/FRAMES_PER_SECOND)
        self.ball_vel[Y]=random.uniform(-30.0/FRAMES_PER_SECOND, 30.0/FRAMES_PER_SECOND)
        if direction==LEFT:
            self.ball_vel[X]=-self.ball_vel[X]

    def newGame(self):
        self.score1=0
        self.score2=0
        direction=RIGHT
        self.spanBall()

if __name__=="__main__":
    app=MainApp()
    app.geometry(str(SCREEN_WIDTH)+"x"+str(SCREEN_HEIGHT))
    app.draw()
    app.mainloop()
