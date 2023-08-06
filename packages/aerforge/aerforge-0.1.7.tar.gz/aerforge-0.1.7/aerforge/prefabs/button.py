from aerforge import *

class Button(Entity):
    def __init__(self, window, shape = shape.Rect, width = 300, height = 100, x = 0, y = 0, color = color.Color(100, 100, 100), highlight_color = color.Color(240, 240, 240), press_color = color.Color(40, 40, 40)):
        super().__init__(
            window = window, 
            shape = shape, 
            width = width, 
            height = height,  
            x = x, 
            y = y,
            color = color,
        )

        self.normal_color = color
        self.highlight_color = highlight_color
        self.press_color = press_color

        self.state = False
        self.pressed = False

    def update(self):
        if self.pressed:
            self.pressed = False

        if self.hit(self.window.input.mouse_pos()):
            self.color = self.highlight_color

            if self.window.input.mouse_pressed(self.window.buttons["LEFT"]):
                if self.state:
                    self.color = self.press_color
                    self.state = False
                    self.pressed = True
            else:
                self.state = True
        else:
            self.color = self.normal_color
            self.state = True

    def is_pressed(self):
        if self.pressed:
            return True

        return False

if __name__ == "__main__":
    forge = Forge()

    button = Button(forge)
    button.center()

    while True:
        if button.is_pressed():
            print("Pressed!")

        button.draw()
        button.update()
        forge.update()