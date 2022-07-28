from buildhat import Motor
from pygame import mixer

LOOP_WAV = '/home/pi/Desktop/roller-loop.mp3'
SCREAMS_WAV = '/home/pi/Desktop/roller-screams.mp3'

def go(port="A"):
    motor = Motor(port)
    motor.plimit(1)
    mixer.init()
    
    # go up
    mixer.music.load(LOOP_WAV)
    mixer.music.play(-1)  # play in loop
    motor.run_for_rotations(28, speed=10)
    mixer.music.stop()
    
    # kick and go down
    mixer.music.load(SCREAMS_WAV)
    mixer.music.play()
    motor.run_for_rotations(35.5, speed=100)
    
    motor.stop()


if __name__ == "__main__":
    go()
