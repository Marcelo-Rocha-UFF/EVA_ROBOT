import pygame
import time

print("Initing pygame...")

pygame.init()

print("waiting for 2s...")
time.sleep(2)
print("Playing a sound!")
sound = pygame.mixer.Sound('efx-blin.wav')

playing = sound.play()

while playing.get_busy():
    pygame.time.delay(100)