import pygame
import string

from classes import Config, Rect, Player, Territory, Unit

type GameObject = Player | Territory | Unit

class Drawer:

  def __init__(self, config:Config) -> None:
    # Create our initial screens, the first is normal, the second has the ability to create opaque objects
    self.screen = pygame.display.set_mode(config.screen)

    # The surface is used as a way to print opaque objects
    self.surface = pygame.Surface(config.screen, pygame.SRCALPHA)

    # Color used to fill in the bakcground
    self.fill = config.colors[config.fill]

    self.images = config.images
    self.colors = config.colors
    self.fonts = config.fonts
    self.rects = config.rects

  # Draws the background for the game (1 time draw)
  def drawBackground(self) -> None:
    # Caption the game
    pygame.display.set_caption('Fishing For Bass')

    # Fill the screen
    self.screen.fill(self.fill)

    background = ['map', 'gamebar', 'turn', 'color', 'yields', 'shop', 'info']

    for feature in background:
      self.drawRect(feature)

    pygame.display.flip()

  # Draws a rectangle given rectangle, its color, and the width of the border
  def drawRect(self, name:str) -> None:
    rect = self.rects[name]

    pygame.draw.rect(self.screen, self.colors['black'], rect.border)
    pygame.draw.rect(self.screen, rect.color, rect.rect)
  
  # Draws text in the given spot
  def drawText(self, text:str, size:str, coordinates:tuple[int, int], alignment:str='left') -> None:
    # Format the text
    text = string.capwords(text.replace('_', ' '))

    # Render the text
    format_text = self.fonts[size].render(text, 0, self.colors['black'])

    # Frame the text
    rect = format_text.get_rect()

    # Align the rendered text
    match alignment:
      case 'left':
        rect.midleft = coordinates
      case 'middle':
        rect.center = coordinates
      case 'right':
        rect.midright = coordinates

    # Draw the text on the screen
    self.screen.blit(format_text, rect)
  
  # Draws a line of resources
  def drawResources(self, values:list[int], rect:pygame.Rect):
    rect = pygame.Rect(rect.move(10,10).topleft, (rect.h - 20, rect.h - 20))

    yields = [self.config.image(x) for x in ['food', 'wood', 'metal', 'oil', 'power']]
    
    for stat, value in zip(yields, values):
      # The image for the stat
      self.screen.blit(stat, rect)

      rect = rect.move(15, 0)

      # The text for the stat
      self.drawText(str(value), 'med', rect.center, 'left')

      rect = rect.move(57.5, 0)

  # Draws the player icons
  def draw(self, players:list[Player], units:list[Unit], pc:Player, hov:GameObject|None, turn:int) -> None:        
    info:dict = self.background['info']
    inforect:pygame.Rect = info['rect']
    iconrect:pygame.Rect = info['iconrect']
    turnrect:pygame.Rect = self.background['turn']['rect']
    resourcerect:pygame.Rect = self.background['resource']['rect']

    # Draw the turn
    self.drawText('Turn ' + str(turn), 'lrg', turnrect.center, 'middle')

    # Draw the player resources
    self.drawResources(pc.stats(), resourcerect)

    match type(hov):
      case Player.__class__:
        # Draw the icon
        self.drawRect(iconrect, hov.color, 5)

        # Draw the name
        self.drawText(hov.name, 'med', iconrect.move(50,0).midleft, 'left')

        # Draws the divider line
        pygame.draw.line(self.screen, self.colors['black'], inforect.move(10,0).midleft, inforect.move(-10,0).midright, 5)

        # Highlight each territory the player owns
        for ter in hov.territories:
          pygame.draw.polygon(self.surface, ter.color, ter.border)
        
        # Draw the surface atop the screen
        self.screen.blit(self.surface, (0,0))

      case Territory.__class__:
        # Draw the icon
        self.drawRect(iconrect, hov.color, 5)

        # Draw the name
        self.drawText(hov.name, 'med', iconrect.move(50,0).midleft, 'left')

        # Draws the divider line
        pygame.draw.line(self.screen, self.colors['black'], inforect.move(10,0).midleft, inforect.move(-10,0).midright, 5)

        # Highlight the selected territory
        pygame.draw.polygon(self.surface, hov.color, hov.border)
    
        # Draw the surface atop the screen
        self.screen.blit(self.surface, (0,0))

      case Unit.__class__:
        # Draw the icon
        self.drawRect(iconrect, hov.color, 5)
        self.screen.blit(pygame.transform.scale(hov.image, (iconrect.w, iconrect.h)), iconrect)

        # Draws the divider line
        pygame.draw.line(self.screen, self.colors['black'], inforect.move(10,0).midleft, inforect.move(-10,0).midright, 5)

      case _:
        # Clears the surface for the next frame
        self.surface.fill([0,0,0,0])

        # Redraws the map of the game
        self.screen.blit(self.images['map'], self.rects['map'])

        # Redraw the player boxes
        for plyr in players:
          self.drawRect(plyr.rect, plyr.color, plyr.border)
    
        # Redraws the units in the shop
        for un in units:
          self.drawRect(un.rect, un.color, un.border)
          self.screen.blit(un.image, un.rect)

        # Redraw the info box to clear the slate
        self.drawRect(inforect, info['color'], info['border'])

    pygame.display.flip()