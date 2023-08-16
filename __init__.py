from st3m.reactor import Responder
from st3m.application import Application, ApplicationContext
import st3m.run
import leds
import random


# divide petals by leds
# light up one petal at a time at random
# when lit petal is pressed add a score
# display score at the screen
# count down from ten seconds
# when time is up, display score

class Spede(Application):
    def __init__(self, app_ctx: ApplicationContext) -> None:
        super().__init__(app_ctx)
        self.last_calib = None
        self.petals = [
            { "leds":[36, 5], "cap": 0 },
            { "leds":[4, 13], "cap": 2 },
            { "leds":[12, 21], "cap": 4 },
            { "leds":[20, 29], "cap": 6 },
            { "leds":[28, 37], "cap": 8 }
        ]
        self.petalid = 0

    def draw(self, ctx: Context) -> None:
        # Paint the background black
        ctx.rgb(0, 0, 0).rectangle(-120, -120, 240, 240).fill()
        ctx.rgb(255, 0, 0).round_rectangle(-20, -20, 40, 40, 20).fill()

        leds.set_all_rgb(0, 0, 0)
        for i, petal in enumerate(self.petals):
            if i == self.petalid:
                if i != 0:
                    for ledid in range(petal["leds"][0], petal["leds"][1]):
                        leds.set_rgb(ledid, 250, 170, 0)
                else:
                    # top petal is a speshul kid
                    for ledid in range(36, 40):
                        leds.set_rgb(ledid, 250, 170, 0)
                    for ledid in range(0, 5):
                        leds.set_rgb(ledid, 250, 170, 0)

        leds.update()
            

    def think(self, ins: InputState, delta_ms: int) -> None:
        super().think(ins, delta_ms)
        # self.petalid = random.randint(0, 3)
        # make all of the petals work
        # wait for user input
        # if user input matches the lit petal, move forward
        for cap_index in range(10):
            petal = ins.captouch.petals[cap_index]
            if petal.pressed and cap_index == self.petals[self.petalid]["cap"]:
                self.petalid = random.randint(0, 4)
                print('jee')


# improvements
# only wait input from the top petals

st3m.run.run_view(Spede(ApplicationContext()))