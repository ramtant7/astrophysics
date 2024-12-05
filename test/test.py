import imageio.v3 as iio
from pathlib import Path
filenames = sorted(list(Path('img').glob('**/*.png')))
images = [ ]

for filename in filenames:
    images.append(iio.imread(filename))

iio.imwrite('gif/team.gif', images, duration = 10, loop = 0)

