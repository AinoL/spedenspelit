from st3m.reactor import Responder
from st3m.application import Application, ApplicationContext
from st3m.ui.view import BaseView
import st3m.run
import leds
import random


# divide petals by leds
# light up one petal at a time at random
# when lit petal is pressed add a score
# display score at the screen
# count down from ten seconds
# when time is up, display score

class ScoreView(BaseView):
    def __init__(self, app_ctx: ApplicationContext, score) -> None:
        super().__init__()
        self.score = score
        # self.last_calib = None
        self.size: int = 60
        self.font: int = 5
    
    def on_enter(self, vm: Optional[ViewManager]) -> None:
        super().on_enter(vm)

    def draw(self, ctx: Context) -> None:
        ctx.save()
        ctx.move_to(0, -20)
        ctx.text_align = ctx.CENTER
        ctx.text_baseline = ctx.MIDDLE
        ctx.font_size: self.size
        ctx.font: self.font
        # Paint the background white
        ctx.rgb(250, 250, 250).rectangle(-120, -120, 240, 240).fill()
        ctx.rgb(0,0,0).text(str(self.score))


class Spede(Application, BaseView):
    def __init__(self, app_ctx: ApplicationContext) -> None:
        super().__init__(app_ctx)
        self.last_calib = None
        self.score = 0
        self.size: int = 60
        self.font: int = 5
        self.timelimit = 10000
        self.current_time = 0
        self.petals = [
            { "leds":[36, 5], "cap": 0 },
            { "leds":[4, 13], "cap": 2 },
            { "leds":[12, 21], "cap": 4 },
            { "leds":[20, 29], "cap": 6 },
            { "leds":[28, 37], "cap": 8 }
        ]
        self.petalid = 0

    def draw(self, ctx: Context) -> None:
        ctx.save()
        ctx.move_to(0, -20)
        ctx.text_align = ctx.CENTER
        ctx.text_baseline = ctx.MIDDLE
        ctx.font_size = self.size
        ctx.font = ctx.get_font_name(self.font)
        # Paint the background white
        ctx.rgb(250, 250, 250).rectangle(-120, -120, 240, 240).fill()
        ctx.rgb(0,0,0).text(str(self.score))
        ctx.move_to(0, 20)
        ctx.rgb(0,0,0).text(str((self.timelimit - self.current_time)/1000))
        ctx.restore()
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
        # input seems to sometimes take multiple presses at once, fix that
        if self.current_time < 10000:
            self.current_time = self.current_time + delta_ms
        if(self.current_time < self.timelimit):
            for cap_index in range(10):
                petal = ins.captouch.petals[cap_index]
                if petal.pressed and cap_index == self.petals[self.petalid]["cap"]:
                    # self.petalid = random.randint(0, 4)
                    self.petalid = random.choice([i for i in range(0,5) if i not in [self.petalid]])
                    self.score=self.score+1
        else:
            self.vm.push(ScoreView(ApplicationContext(), self.score))


# improvements
# only wait input from the top petals
# make the leds change colors on every push

st3m.run.run_view(Spede(ApplicationContext()))