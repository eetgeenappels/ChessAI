import pygame
import assets
import render

running = True

font = pygame.font.SysFont('arial', size=100)
local_button = font.render('Local', True, (255, 255, 255))
online_button = font.render('Online', True, (255, 255, 255))

font_small = pygame.font.SysFont('arial', size=40)
inspire_text = font.render('Inspire Text', True, (255, 255, 0))


def tick(screen):
    global running

    screen.fill((255, 255, 255))

    multiplayer_session = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                x, y = pygame.mouse.get_pos()

                if 150 < x < 400:
                    if 300 < y < 400:
                        # local
                        running = False

                        multiplayer_session = False
                    if 450 < y < 550:
                        # online
                        running = False

                        multiplayer_session = True

    pygame.draw.rect(screen, (0, 0, 0), (150, 300, 250, 100))
    pygame.draw.rect(screen, (0, 0, 0), (150, 450, 250, 100))

    screen.blit(assets.beter_nathan, (200, 550))

    screen.blit(pygame.transform.scale(assets.main_menu_logo, (250, 250)), (50, 25))

    screen.blit(local_button, (150, 300))
    screen.blit(online_button, (150, 450))

    screen.blit(pygame.transform.rotate(inspire_text, -40), (100, 100))

    pygame.display.flip()

    return running, multiplayer_session
