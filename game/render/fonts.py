from pygame.freetype import Font
from pygame.rect import Rect
from pygame.surface import Surface


def word_wrap(surf: Surface, rect: Rect, text: str, font: Font, color=(0, 0, 0)):
    font.origin = True
    words = text.split(' ')
    width, height = rect.width, rect.height
    line_spacing = font.get_sized_height() + 2
    x, y = rect.left, rect.top + 20
    space = font.get_rect(' ')
    for word in words:
        bounds = font.get_rect(word)
        if x + bounds.width + bounds.x >= width:
            x, y = rect.left, y + line_spacing
        if x + bounds.width + bounds.x >= width:
            raise ValueError("word too wide for the surface")
        if y + bounds.height - bounds.y >= height + y:
            raise ValueError("text to long for the surface")
        font.render_to(surf, (x, y), None, color)
        x += bounds.width + space.width
    return x, y
