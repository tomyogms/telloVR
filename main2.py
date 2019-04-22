import tello
from ui import UI


def main():

    drone = tello.Tello('192.168.10.2', 8889)  
    vplayer = UI(drone,"./img/")
    
	# start the Tkinter mainloop
    vplayer.root.mainloop() 

if __name__ == "__main__":
    main()
