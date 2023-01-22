import pygame
import random

# Reference on rendering each character with different color:
# https://stackoverflow.com/questions/64966471/how-to-change-the-color-a-section-of-text-in-pygame


class TypingGame:
    def __init__(self) -> None:
        # Screen size
        self.width = 1142
        self.height = 647
        self.screen = None
        self._running = True
        # Initialize images
        self.open_img = pygame.image.load("type-speed-open.png")
        self.icon_img = pygame.image.load("icon.png")
        self.icon_img = pygame.transform.scale(self.icon_img, (150, 150))
        # Background color
        self.BACKGROUND_COLOR = (224, 177, 203)
        # The current sentence and letter that are on the screen
        self.cur_s = ""
        self.cur_letter = 0

    def get_sentences(self):
        """Getting a random sentence from the text file"""
        with open("sentences.txt", "r") as file:
            tmp = []
            for line in file:
                tmp.append(line.strip())
            self.cur_s = random.choice(tmp)
            return

    def on_init(self):
        """Initialize pygame and screen"""
        self.get_sentences()
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.HWSURFACE | pygame.DOUBLEBUF)
        pygame.display.set_caption("Typing Speed Test")
        self._running = True
        self.screen.blit(self.open_img, (0, 0))
        pygame.display.update()

    def on_loop(self, unicode):
        """Rendering the entire sentence every loop"""
        font = pygame.freetype.Font("CascadiaCode.ttf", 25)
        font.origin = True
        # Pick the next character to render or the next sentence when it reaches the end
        if unicode == self.cur_s[self.cur_letter].lower():
            self.cur_letter += 1
            if self.cur_letter >= len(self.cur_s):
                self.cur_letter = 0
                self.get_sentences()
        text_surf_rect = font.get_rect(self.cur_s)
        baseline = text_surf_rect.y
        text_surf = pygame.Surface(text_surf_rect.size)
        text_surf_rect.center = self.screen.get_rect().center
        metrics = font.get_metrics(self.cur_s)
        total = 0
        text_surf.fill(self.BACKGROUND_COLOR)
        for (idx, (letter, metric)) in enumerate(zip(self.cur_s, metrics)):
            # select the right color
            if idx == self.cur_letter:
                color = (0, 119, 182)
            elif idx < self.cur_letter:
                color = (141, 153, 174)
            else:
                color = (43, 45, 66)
            # render the single letter
            font.render_to(text_surf, (total, baseline), letter, color)
            # move the starting position up
            total += metric[4]
        self.screen.blit(text_surf, text_surf_rect)
        pygame.display.update()

    def on_reset(self):
        font = pygame.font.Font("CascadiaCode.ttf", 80)
        text = font.render("Start typing", True, (27, 38, 59))
        text_rect = text.get_rect(center=(self.width / 2, 70))
        self.screen.fill(self.BACKGROUND_COLOR)
        self.screen.blit(self.icon_img, (self.width / 2 - 75, 647 - 150))
        self.screen.blit(text, text_rect)
        self.on_loop(None)
        self.cur_letter = 0
        self.get_sentences()

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        while self._running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.on_reset()
                elif event.type == pygame.KEYDOWN:
                    self.on_loop(event.unicode)
        self.on_cleanup()


if __name__ == "__main__":
    theApp = TypingGame()
    theApp.on_init()
    theApp.on_execute()
