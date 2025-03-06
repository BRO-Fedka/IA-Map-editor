import pygame
import sys
import pickle
from PIL import ImageColor
from shapely.geometry import Polygon
WH = 32
postWH = 32*32/WH
def main():
    MAP = pickle.load(open('MAPEXPS0', 'rb'))
    MAPB = []
    MAPZ = []
    MAPS = []
    MAPG = []
    MAPQ = []
    for _ in MAP['B']:
        try:
            k = list(_.exterior.coords)
            for l in range(0,len(k)):
                k[l] = (k[l][0]*postWH,k[l][1]*postWH)
            MAPB.append(k)
        except:pass
    for _ in MAP['S']:
        try:
            k = list(_.exterior.coords)
            for l in range(0,len(k)):
                k[l] = (k[l][0]*postWH,k[l][1]*postWH)
            MAPS.append(k)
        except:pass
    for _ in MAP['Z']:
        k = list(_.exterior.coords)
        for l in range(0,len(k)):
            k[l] = (k[l][0]*postWH,k[l][1]*postWH)
        MAPZ.append(k)
    for _ in MAP['G']:
        k = list(_.exterior.coords)
        for l in range(0,len(k)):
            k[l] = (k[l][0]*postWH,k[l][1]*postWH)
        MAPG.append(k)
    for x in range(0,WH):
        for y in range(0,WH):
            if len(MAP['Q'][(x,y)]['B'])>0:MAPQ.append((x*4,y*4,4,4))
    TPS = 60
    pygame.init()
    Form = pygame.display.set_mode((1024, 1024))
    clock = pygame.time.Clock()
    pygame.display.update()
    while True:
        TPS = clock.tick(TPS)
        pygame.display.set_caption(str(clock.get_fps()))
        for _ in MAPZ:
            pygame.draw.polygon(Form, ImageColor.getcolor("#2879ADFF", "RGBA"), _)
        for _ in MAPB:
            pygame.draw.polygon(Form, ImageColor.getcolor("#FFC45FFF", "RGBA"), _)
        for _ in MAPG:
            pygame.draw.polygon(Form, ImageColor.getcolor("#569f4fff", "RGBA"), _)
        for _ in MAPS:
            pygame.draw.polygon(Form, ImageColor.getcolor("#454545ff", "RGBA"), _)
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                pygame.image.save(Form, 'MAP.png')
                sys.exit()
        pygame.display.update()
        Form.fill(ImageColor.getcolor("#004F88FF", "RGBA"))

if __name__ == '__main__':
    main()
