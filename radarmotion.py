from graphicsItems import *
import time
from PyQt5.QtCore import pyqtSlot, QObject

PLOT_Z_VALUE = 1 # display moving items OVER trajectory items

class ItemsMotionManager():
    """Collection of moving items and their motion management"""
    def __init__(self, radar):
        self.rad = radar
        self.sim = self.rad.simulation
        self.aircraft = AircraftItem()
        #self.aircraft.update_position(0,0)
        self.aircraft.setZValue(PLOT_Z_VALUE)
        radar.scene.addItem(self.aircraft)
        self.sim.update_signal.connect(self.update_items) # listen update signal on simulation

    def update_items(self):
        """Update moving items"""
        if not(self.sim.USE_IVY): # if Ivy Bus isn't used
            pos = self.sim.listeACpositions[int(self.sim.time/self.sim.SIMU_DELAY)]
            self.aircraft.update_position(pos.x, pos.y)
            time.sleep(self.sim.SIMU_DELAY)
        else:
            self.aircraft.update_position(self.sim.AC_Y, self.sim.AC_X)
        #self.rad.scene.setSceneRect(self.sim.AC_X-self.rad.width/2, self.sim.AC_Y-self.rad.height/2, self.rad.width, self.rad.height)
