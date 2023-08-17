from st3m.reactor import Responder
from st3m.application import Application, ApplicationContext
from st3m.ui.view import BaseView
import st3m.run
import leds
import random

class GameView(Application, BaseView):
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
        ctx.rgb(250, 250, 250).rectangle(-120, -120, 240, 240).fill()
        ctx.rgb(0,0,0).text(str(self.score))
        ctx.move_to(0, 20)
        ctx.rgb(0,0,0).text(str(int((self.timelimit - self.current_time)/100)/10))
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
        if self.current_time < 10000:
            self.current_time = self.current_time + delta_ms
        if(self.current_time < self.timelimit):
            for cap_index in range(10):
                petal = ins.captouch.petals[cap_index]
                if petal.pressed and cap_index == self.petals[self.petalid]["cap"]:
                    self.score=self.score+1
                    self.petalid = random.choice([i for i in range(0,5) if i not in [self.petalid]])
        else:
            self.vm.push(ScoreView(ApplicationContext(), self.score))

    def on_enter(self, vm: Optional[ViewManager]) -> None:
        super().on_enter(vm)

class ScoreView(BaseView):
    def __init__(self, app_ctx: ApplicationContext, score) -> None:
        super().__init__()
        self.score = score
        self.last_calib = None
        self.size: int = 60
        self.font: int = 5
    
    def on_enter(self, vm: Optional[ViewManager]) -> None:
        super().on_enter(vm)

    def draw(self, ctx: Context) -> None:
        ctx.save()
        ctx.move_to(0, -20)
        ctx.text_align = ctx.CENTER
        ctx.text_baseline = ctx.MIDDLE
        ctx.font_size = self.size
        ctx.font = ctx.get_font_name(self.font)
        ctx.rgb(250, 250, 250).rectangle(-120, -120, 240, 240).fill()
        ctx.rgb(0,0,0).text('Your score')
        ctx.move_to(0, 20)
        ctx.rgb(0,0,0).text(str(self.score))
        # play again text
        ctx.move_to(0, 50)
        ctx.font_size = int = 20
        ctx.rgb(0,0,0).text('Press right to play again')

        ctx.restore()
        leds.set_all_rgb(250, 170, 0)
        leds.update()
    
    def think(self, ins: InputState, delta_ms: int) -> None:
        super().think(ins, delta_ms) # Let BaseView do its thing
        if self.input.buttons.app.right.pressed:
            self.vm.push(CountdownView(ApplicationContext()))

# Make a clock go down from 3 seconds
class CountdownView(Application, BaseView):
    def __init__(self, app_ctx: ApplicationContext) -> None:
        super().__init__(app_ctx)
        self.timer = 4000
        self.current_time = 0
        self.last_calib = None
        self.size: int = 60
        self.font: int = 5

    def on_enter(self, vm: Optional[ViewManager]) -> None:
        super().on_enter(vm)

    def draw(self, ctx: Context) -> None:
        ctx.rgb(250, 250, 250).rectangle(-120, -120, 240, 240).fill()
        ctx.save()
        ctx.move_to(0, -20)
        ctx.text_align = ctx.CENTER
        ctx.text_baseline = ctx.MIDDLE
        ctx.font_size = self.size
        ctx.font = ctx.get_font_name(self.font)
        ctx.rgb(0,0,0).text('Get ready!')
        ctx.move_to(0, 20)
        ctx.rgb(0,0,0).text(str(int((self.timer - self.current_time)/1000)%100))
        ctx.restore()
    
    def think(self, ins: InputState, delta_ms: int) -> None:
        super().think(ins, delta_ms) # Let BaseView do its thing
        self.current_time = self.current_time + delta_ms
        if self.current_time > self.timer:
            self.vm.push(GameView(ApplicationContext()))

# Make a rules screen
class RulesView(Application, BaseView):
    def __init__(self, app_ctx: ApplicationContext) -> None:
        super().__init__(app_ctx)
        self.last_calib = None
        self.size: int = 60
        self.font: int = 5

    def on_enter(self, vm: Optional[ViewManager]) -> None:
        super().on_enter(vm)

    def draw(self, ctx: Context) -> None:
        ctx.rgb(250, 250, 250).rectangle(-120, -120, 240, 240).fill()
        ctx.save()
        ctx.move_to(0, -80)
        ctx.text_align = ctx.CENTER
        ctx.text_baseline = ctx.MIDDLE
        ctx.font_size = self.size
        ctx.font = ctx.get_font_name(self.font)
        ctx.rgb(0,0,0).text('#TODO')
        ctx.move_to(0, -50)
        ctx.rgb(0,0,0).text('Press as')
        ctx.move_to(0, -20)
        ctx.rgb(0,0,0).text('many lit')
        ctx.move_to(0, 10)
        ctx.rgb(0,0,0).text('petals in ten')
        ctx.move_to(0, 40)
        ctx.rgb(0,0,0).text('seconds as')
        ctx.move_to(0, 70)
        ctx.rgb(0,0,0).text('you can')
        ctx.restore()
    
    def think(self, ins: InputState, delta_ms: int) -> None:
        super().think(ins, delta_ms) # Let BaseView do its thing
        if self.input.buttons.app.right.pressed:
            self.vm.push(CountdownView(ApplicationContext()))

class SplashView(Application, BaseView):
    def __init__(self, app_ctx: ApplicationContext) -> None:
        super().__init__(app_ctx)
        self.last_calib = None
        self.size: int = 50
        self.font: int = 5

    def on_enter(self, vm: Optional[ViewManager]) -> None:
        super().on_enter(vm)

    def draw(self, ctx: Context) -> None:
        ctx.rgb(250, 250, 250).rectangle(-120, -120, 240, 240).fill()
        ctx.save()
        ctx.move_to(0, -80)
        ctx.text_align = ctx.CENTER
        ctx.text_baseline = ctx.MIDDLE
        ctx.font_size = self.size
        ctx.font = ctx.get_font_name(self.font)
        ctx.rgb(0,0,0).text('SPEDEN')
        ctx.move_to(0, -50)
        ctx.image(
            "/flash/sys/apps/spedenspelit/spede_nelio.png",
            -75,
            -75,
            150,
            150
        )
        ctx.move_to(0, 80)
        ctx.rgb(0,0,0).text('SPELIT')
        ctx.move_to(0, 100)
        ctx.font_size: int = 20
        ctx.rgb(0,0,0).text('Press right to')
        ctx.move_to(0, 110)
        ctx.rgb(0,0,0).text('continue')
        ctx.restore()
    
    def think(self, ins: InputState, delta_ms: int) -> None:
        super().think(ins, delta_ms) # Let BaseView do its thing
        if self.input.buttons.app.right.pressed:
            self.vm.push(RulesView(ApplicationContext()))

class Spede(Application, BaseView):
    def draw(self, ctx: Context) -> None:
        # Paint the background black because I don't know how to code
        ctx.rgb(0, 0, 0).rectangle(-120, -120, 240, 240).fill()

    def think(self, ins: InputState, delta_ms: int) -> None:
        super().think(ins, delta_ms) # Let BaseView do its thing
        self.vm.push(SplashView(ApplicationContext()))


# improvements
# make the leds change colors on every push
# if wrong petal is pressed end the game
# make a way to exit the game
# add a high score file
# switch right and right around

st3m.run.run_view(Spede(ApplicationContext()))