#! /usr/bin/env python3

import asyncio
import monome

class GridStudies(monome.GridApp):

    global gridConnected
    global firstConnection

    def __init__(self):
        super().__init__()
    
    # track connection status:
    def connectGrid(state, self):
        GridStudies.gridConnected = state
        try:
            GridStudies.firstConnection
            GridStudies.firstConnection = False
        except:
            GridStudies.firstConnection = True
            playTask = asyncio.create_task(self.play())

    # when grid is plugged in via USB:
    def on_grid_ready(self):
        global width
        width = self.grid.width
        global height
        height = self.grid.height
        global canvasFloor
        canvasFloor = height-2
        
        GridStudies.connectGrid(True, self)
        if GridStudies.firstConnection:
            self.step = [[0 for col in range(width)] for row in range(canvasFloor)]
            self.play_position = -1

    # when grid is physically disconnected:
    def on_grid_disconnect(self,*args):
        GridStudies.connectGrid(False, self)

    async def play(self):
        while True:
            await asyncio.sleep(0.1)
            if self.play_position == width - 1:
                self.play_position = 0
            else:
                self.play_position += 1

            # TRIGGER SOMETHING
            for y in range(canvasFloor):
                if self.step[y][self.play_position] == 1:
                    self.trigger(y)

            if GridStudies.gridConnected:
                self.draw()

    def trigger(self, i):
        print("triggered", i)

    def draw(self):
        buffer = monome.GridBuffer(width, height)

        # display steps
        for x in range(width):
            # highlight the play position
            if x == self.play_position:
                highlight = 4
            else:
                highlight = 0

            for y in range(canvasFloor):
                buffer.led_level_set(x, y, self.step[y][x] * 11 + highlight)

        # draw trigger bar and on-states
        for x in range(width):
            buffer.led_level_set(x, canvasFloor, 4)

        for y in range(canvasFloor):
            if self.step[y][self.play_position] == 1:
                buffer.led_level_set(self.play_position, canvasFloor, 15)

        # update grid
        buffer.render(self.grid)

    def on_grid_key(self, x, y, s):
        # toggle steps
        if s == 1 and y < canvasFloor:
            self.step[y][x] ^= 1
            self.draw()

async def main():
    loop = asyncio.get_event_loop()
    grid_studies = GridStudies()

    def serialosc_device_added(id, type, port):
        print('connecting to {} ({})'.format(id, type))
        asyncio.ensure_future(grid_studies.grid.connect('127.0.0.1', port))

    serialosc = monome.SerialOsc()
    serialosc.device_added_event.add_handler(serialosc_device_added)

    await serialosc.connect()
    await loop.create_future()

if __name__ == '__main__':
    asyncio.run(main())
