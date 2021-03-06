"""
Slider
======

.. image:: images/slider.jpg

The :class:`Slider` widget looks like a scrollbar. It supports horizontal and
vertical orientations, min/max values and a default value.

To create a slider from -100 to 100 starting from 25::

    from kivy.uix.slider import Slider
    s = Slider(min=-100, max=100, value=25)

To create a vertical slider::

    from kivy.uix.slider import Slider
    s = Slider(orientation='vertical')

"""
__all__ = ('ValueAera', )

from kivy.uix.widget import Widget
from kivy.properties import (NumericProperty, AliasProperty, OptionProperty,
                             ReferenceListProperty, BoundedNumericProperty)


class ValueAera(Widget):
    """Class for creating a Slider widget.

    Check module documentation for more details.
    """

    value = NumericProperty(0.)
    x_value = NumericProperty(0.)
    y_value = NumericProperty(0.)

    '''Current value used for the slider.

    :attr:`value` is a :class:`~kivy.properties.NumericProperty` and defaults
    to 0.'''

    min = NumericProperty(0.)
    x_min= NumericProperty(0.)
    y_min= NumericProperty(0.)
    '''Minimum value allowed for :attr:`value`.

    :attr:`min` is a :class:`~kivy.properties.NumericProperty` and defaults to
    0.'''

    max = NumericProperty(100.)
    x_max = NumericProperty(100.)
    y_max = NumericProperty(100.)
    '''Maximum value allowed for :attr:`value`.

    :attr:`max` is a :class:`~kivy.properties.NumericProperty` and defaults to
    100.'''

    padding = NumericProperty(10)
    '''Padding of the slider. The padding is used for graphical representation
    and interaction. It prevents the cursor from going out of the bounds of the
    slider bounding box.

    By default, padding is 10. The range of the slider is reduced from padding
    \*2 on the screen. It allows drawing a cursor of 20px width without having
    the cursor go out of the widget.

    :attr:`padding` is a :class:`~kivy.properties.NumericProperty` and defaults
    to 10.'''

    orientation = OptionProperty('horizontal', options=(
        'vertical', 'horizontal'))
    '''Orientation of the slider.

    :attr:`orientation` is an :class:`~kivy.properties.OptionProperty` and
    defaults to 'horizontal'. Can take a value of 'vertical' or 'horizontal'.
    '''

    range = ReferenceListProperty(min, max)
    x_range = ReferenceListProperty(min, max)
    y_range = ReferenceListProperty(min, max)
    '''Range of the slider in the format (minimum value, maximum value)::

        >>> slider = Slider(min=10, max=80)
        >>> slider.range
        [10, 80]
        >>> slider.range = (20, 100)
        >>> slider.min
        20
        >>> slider.max
        100

    :attr:`range` is a :class:`~kivy.properties.ReferenceListProperty` of
    (:attr:`min`, :attr:`max`).
    '''

    step = BoundedNumericProperty(0, min=0)
    '''Step size of the slider.

    .. versionadded:: 1.4.0

    Determines the size of each interval or step the slider takes between
    min and max. If the value range can't be evenly divisible by step the
    last step will be capped by slider.max

    :attr:`step` is a :class:`~kivy.properties.NumericProperty` and defaults
    to 1.'''


    def get_x_norm_value(self):
        vmin = self.x_min
        d = self.x_max - vmin
        if d == 0:
            return 0
        return (self.x_value - vmin) / float(d)

    def get_y_norm_value(self):
        vmin = self.y_min
        d = self.y_max - vmin
        if d == 0:
            return 0
        return (self.y_value - vmin) / float(d)


    def set_x_norm_value(self, x_value):
        vmin = self.x_min
        step = self.step
        val = x_value * (self.x_max - vmin) + vmin
        if step == 0:
            self.x_value = val
        else:
            self.x_value = min(round((val - vmin) / step) * step + vmin,
                             self.x_max)

    def set_y_norm_value(self, y_value):
        vmin = self.y_min
        step = self.step
        val = y_value * (self.y_max - vmin) + vmin
        if step == 0:
            self.y_value = val
        else:
            self.y_value = min(round((val - vmin) / step) * step + vmin,
                             self.y_max)

    x_value_normalized = AliasProperty(get_x_norm_value, set_x_norm_value,
                                     bind=('x_value', 'x_min', 'x_max', 'step'))

    y_value_normalized = AliasProperty(get_y_norm_value, set_y_norm_value,
                                     bind=('y_value', 'y_min', 'y_max', 'step'))



    '''Normalized value inside the :attr:`range` (min/max) to 0-1 range::

        >>> slider = Slider(value=50, min=0, max=100)
        >>> slider.value
        50
        >>> slider.value_normalized
        0.5
        >>> slider.value = 0
        >>> slider.value_normalized
        0
        >>> slider.value = 100
        >>> slider.value_normalized
        1

    You can also use it for setting the real value without knowing the minimum
    and maximum::

        >>> slider = Slider(min=0, max=200)
        >>> slider.value_normalized = .5
        >>> slider.value
        100
        >>> slider.value_normalized = 1.
        >>> slider.value
        200

    :attr:`value_normalized` is an :class:`~kivy.properties.AliasProperty`.
    '''


    def get_x_value_pos(self):
        padding = self.padding
        x = self.x
        y = self.y
        nval = self.x_value_normalized

        return x + padding + nval * (self.width - 2 * padding), y


    def get_y_value_pos(self):
        padding = self.padding
        x = self.x
        y = self.y
        nval = self.y_value_normalized

        return x, y + padding + nval * (self.height - 2 * padding)

    def set_value_pos(self, pos):
        padding = self.padding
        x = min(self.right - padding, max(pos[0], self.x + padding))
        y = min(self.top - padding, max(pos[1], self.y + padding))
        if self.orientation == 'horizontal':
            if self.width == 0:
                self.value_normalized = 0
            else:
                self.value_normalized = (x - self.x - padding
                                         ) / float(self.width - 2 * padding)
        else:
            if self.height == 0:
                self.value_normalized = 0
            else:
                self.value_normalized = (y - self.y - padding
                                         ) / float(self.height - 2 * padding)

    def set_x_value_pos(self, pos):
        padding = self.padding

        x = min(self.right - padding, max(pos, self.x + padding))

        if self.width == 0:
            self.x_value_normalized = 0
        else:
            self.x_value_normalized = (x - self.x - padding
                                     ) / float(self.width - 2 * padding)

    def set_y_value_pos(self, pos):
        padding = self.padding
        y = min(self.top - padding, max(pos, self.y + padding))

        if self.height == 0:
            self.y_value_normalized = 0
        else:
            self.y_value_normalized = (y - self.y - padding
                                     ) / float(self.height - 2 * padding)


    x_value_pos=AliasProperty(get_x_value_pos, set_x_value_pos,
                              bind=('x', 'y', 'width', 'height', 'x_min',
                                    'x_max', 'x_value_normalized', 'orientation'))
    y_value_pos=AliasProperty(get_y_value_pos, set_y_value_pos,
                              bind=('x', 'y', 'width', 'height', 'y_min',
                                    'y_max', 'y_value_normalized', 'orientation'))

    '''Position of the internal cursor, based on the normalized value.

    :attr:`value_pos` is an :class:`~kivy.properties.AliasProperty`.
    '''

    def on_touch_down(self, touch):
        if self.disabled or not self.collide_point(*touch.pos):
            return

        else:
            touch.grab(self)
            self.x_value_pos = touch.x
            self.y_value_pos = touch.y
        return True

    def on_touch_move(self, touch):
        if touch.grab_current == self:
            self.x_value_pos = touch.x
            self.y_value_pos = touch.y
            return True

    def on_touch_up(self, touch):
        if touch.grab_current == self:
            # self.value_pos = touch.pos
            self.x_value_pos = touch.x
            self.y_value_pos = touch.y
            return True

if __name__ == '__main__':
    from kivy.app import App

    class SliderApp(App):
        def build(self):
            return ValueAera(padding=25)

    SliderApp().run()
