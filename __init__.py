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

class Pew(Application):
    def __init__(self, app_ctx: ApplicationContext) -> None:
        super().__init__(app_ctx)
        self.last_calib = None
        self.petals = [
            # [37, 5],
            [5, 13],
            [13, 21],
            [21, 29],
            [29, 37]
        ]

    def draw(self, ctx: Context) -> None:
        # Paint the background black
        ctx.rgb(0, 0, 0).rectangle(-120, -120, 240, 240).fill()
        ctx.rgb(255, 0, 0).round_rectangle(-20, -20, 40, 40, 20).fill()

        for i in range(*self.petals[random.randint(0, 3)]):
            leds.set_rgb(i, 250, 170, 0)
            leds.update()
            

    def think(self, ins: InputState, delta_ms: int) -> None:
        super().think(ins, delta_ms)
        for i in range(10):
            petal = ins.captouch.petals[i]
            if petal.pressed:
                print(i)


st3m.run.run_view(Pew(ApplicationContext()))