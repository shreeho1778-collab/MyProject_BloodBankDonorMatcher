import pygame
from game.maze import CELL

SPEED = 3


class Player:
    def __init__(self, r, c):
        self.r = r
        self.c = c
        x = c * CELL + CELL // 2
        y = r * CELL + CELL // 2
        self.rect = pygame.Rect(x - 10, y - 10, 20, 20)
        self.color = (60, 120, 220)

    def move(self, keys, walls, rows, cols):
        dx = 0
        dy = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = SPEED
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy = -SPEED
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy = SPEED

        # Resolve each axis independently, but never cross a closed cell wall.
        if dx:
            candidate = self.rect.move(dx, 0)
            if not self._hits_wall(candidate, walls, rows, cols):
                self.rect = candidate
        if dy:
            candidate = self.rect.move(0, dy)
            if not self._hits_wall(candidate, walls, rows, cols):
                self.rect = candidate

        self.r = max(0, min(rows - 1, self.rect.centery // CELL))
        self.c = max(0, min(cols - 1, self.rect.centerx // CELL))

    def _hits_wall(self, rect, walls, rows, cols):
        # Check each edge crossed by the player's bounding box against the
        # wall flags of every cell overlapped by the candidate rectangle.
        if rect.left < 0 or rect.top < 0 or rect.right > cols * CELL or rect.bottom > rows * CELL:
            return True

        left_col = rect.left // CELL
        right_col = (rect.right - 1) // CELL
        top_row = rect.top // CELL
        bottom_row = (rect.bottom - 1) // CELL

        # If the rectangle overlaps two columns, it crossed a vertical boundary.
        if left_col != right_col:
            boundary_col = right_col
            for row in range(top_row, bottom_row + 1):
                if walls[row][left_col][2] or walls[row][right_col][3]:
                    return True

        # If the rectangle overlaps two rows, it crossed a horizontal boundary.
        if top_row != bottom_row:
            boundary_row = bottom_row
            for col in range(left_col, right_col + 1):
                if walls[top_row][col][1] or walls[bottom_row][col][0]:
                    return True

        return False

    def draw(self, screen):
        pygame.draw.ellipse(screen, self.color, self.rect)
