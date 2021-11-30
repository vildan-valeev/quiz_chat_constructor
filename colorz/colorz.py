from colorsys import rgb_to_hsv, hsv_to_rgb

from PIL import Image
from numpy import array
from scipy.cluster.vq import kmeans

DEFAULT_NUM_COLORS = 6
DEFAULT_MINV = 170
DEFAULT_MAXV = 200
DEFAULT_BOLD_ADD = 50

THUMB_SIZE = (200, 200)
SCALE = 256.0


def hexify(rgb):
    return '#%s' % ''.join('%02x' % p for p in rgb)


def get_colors(img):
    """
    Returns a list of all the image's colors.
    """
    w, h = img.size
    return [color[:3] for count, color in img.convert('RGB').getcolors(w * h)]


def order_by_hue(colors):
    """
    Orders colors by hue.
    """
    hsvs = [rgb_to_hsv(*map(down_scale, color)) for color in colors]
    hsvs.sort(key=lambda t: t[0])
    return [tuple(map(up_scale, hsv_to_rgb(*hsv))) for hsv in hsvs]


def down_scale(x):
    return x / SCALE


def up_scale(x):
    return int(x * SCALE)


def clamp(color, min_v, max_v):
    """
    Clamps a color such that the value is between min_v and max_v.
    """
    h, s, v = rgb_to_hsv(*map(down_scale, color))
    min_v, max_v = map(down_scale, (min_v, max_v))
    v = min(max(min_v, v), max_v)
    return tuple(map(up_scale, hsv_to_rgb(h, s, v)))


def brighten(color, brightness):
    """
    Adds or subtracts value to a color.
    """
    h, s, v = rgb_to_hsv(*map(down_scale, color))
    return tuple(map(up_scale, hsv_to_rgb(h, s, v + down_scale(brightness))))


def colorz(fd, n=DEFAULT_NUM_COLORS, min_v=DEFAULT_MINV, max_v=DEFAULT_MAXV,
           bold_add=DEFAULT_BOLD_ADD, order_colors=True):
    """
    Get the n most dominant colors of an image.
    Clamps value to between min_v and max_v.
    Creates bold colors using bold_add.
    Total number of colors returned is 2*n, optionally ordered by hue.
    Returns as a list of pairs of RGB triples.
    For terminal colors, the hue order is:
    red, yellow, green, cyan, blue, magenta
    """
    img = Image.open(fd)
    img.thumbnail(THUMB_SIZE)

    obs = get_colors(img)
    clamped = [clamp(color, min_v, max_v) for color in obs]
    clusters, _ = kmeans(array(clamped).astype(float), n)
    colors = order_by_hue(clusters) if order_colors else clusters
    return list(zip(colors, [brighten(c, bold_add) for c in colors]))


def get_color(photo):
    colors = colorz(photo, )
    # print(colors, tuple(map(hexify, pair)))
    ans = ()
    for pair in colors:
        ans += tuple(map(hexify, pair))
    return ans


if __name__ == '__main__':
    img_fd = open('photo.jpg', 'rb')
    print(get_color(img_fd))
