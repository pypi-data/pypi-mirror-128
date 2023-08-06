from typing import List, Union
from kivy.app import App
from kivy.lang.builder import Builder
from kivy.uix.widget import Widget
from kivy.properties import ListProperty, NumericProperty
from kwidgets.utils import intersperse, to_xy

Builder.load_string("""
<LineChart>:
    on_height: self.recompute_pixelpoints()
    on_width: self.recompute_pixelpoints()
    canvas:
        Color:
            rgba: 1,0,0,1
        Line: 
            width: self._linewidth
            points: self._pixel_points
""")

class LineChart(Widget):
    _pixel_points = ListProperty([0,0,1,1,2,2])
    _value_points = ListProperty([0,0,1,1,2,2])
    _padding = NumericProperty(10)
    _linewidth = NumericProperty(1)

    def recompute_pixelpoints(self):
        xs, ys = to_xy(self._value_points)
        xmin = min(xs)
        xmax = max(xs)
        ymin = min(ys)
        ymax = max(ys)
        ya = float((self.height-2.*(self._padding))/(ymax-ymin))
        yb = float(-ya*ymin)

        xa = float((self.width-2.*(self._padding))/(xmax-xmin))
        xb = float(-xa*ymin)

        self._pixel_points = intersperse([[self.x+self._padding+(xa * x + xb) for x in xs], [self.y+self._padding+(ya * y + yb) for y in ys]])

    def setData(self, vals: List[Union[float, int]]):
        assert len(vals) % 2 == 0, "An odd number of values were provided.  List but be [x1, y1, x2, y2, ...]"
        self._value_points = vals
        self.recomput_pixelpoints()

    def setData(self, xs: List[Union[int, float]], ys: List[Union[int, float]]):
        self.setData(intersperse([xs, ys]))

    @property
    def value_points(self):
        return self._value_points

    @value_points.setter
    def value_points(self, vals: List[Union[float, int]]):
        self._value_points=vals
        self.recompute_pixelpoints()

    @property
    def padding(self):
        return self._padding

    @padding.setter
    def padding(self, value: int):
        self._padding = value
        self.recompute_pixelpoints()

    @property
    def linewidth(self):
        return self._linewidth

    @linewidth.setter
    def linewidth(self, value: int):
        self._linewidth = value


class LineChartApp(App):
    def build(self):
        container = Builder.load_string('''
#:import np numpy
BoxLayout:
    orientation: 'vertical'
    LineChart
        value_points: 1,1,2,2,3,1.5,4,4,5,1
        padding: 20
        linewidth: 2
''')
        return container

if __name__ == "__main__":
    LineChartApp().run()