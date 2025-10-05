import numpy as np
import matplotlib.pyplot as plt
import cv2
import random
import math
import copy
import time
import psutil
from collections import deque

class JigsawSolver:
    """
    A class to solve a 4x4 jigsaw puzzle using a hybrid greedy and
    simulated annealing approach.
    """
    def __init__(self, image_matrix, patch_size=128):
        """
        Initializes the solver with the image data.
        
        Args:
            image_matrix (np.array): The 512x512 image data.
            patch_size (int): The size of each square patch.
        """
        self.image = image_matrix.T  # Transpose to match original orientation
        self.patch_size = patch_size
        self.grid_size = self.image.shape[0] // patch_size
        self.patches = self._create_patches()
        self.num_patches = len(self.patches)

    def _create_patches(self):
        """Splits the image into a dictionary of patches."""
        patches = {}
        patch_id = 0
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                patch = self.image[
                    i * self.patch_size : (i + 1) * self.patch_size,
                    j * self.patch_size : (j + 1) * self.patch_size,
                ]
                patches[patch_id] = patch
                patch_id += 1
        return patches

    def get_dissimilarity_score(self, grid):
        """
        Calculates the total dissimilarity score for a given grid configuration.
        The score is the sum of absolute differences of pixels on adjacent edges.
        """
        score = 0
        # Horizontal dissimilarity
        for r in range(self.grid_size):
            for c in range(self.grid_size - 1):
                patch_left_id = grid[r][c]
                patch_right_id = grid[r][c + 1]
                
                edge_left = self.patches[patch_left_id][:, -1]
                edge_right = self.patches[patch_right_id][:, 0]
                score += np.sum(np.abs(edge_left - edge_right))

        # Vertical dissimilarity
        for r in range(self.grid_size - 1):
            for c in range(self.grid_size):
                patch_top_id = grid[r][c]
                patch_bottom_id = grid[r + 1][c]

                edge_top = self.patches[patch_top_id][-1, :]
                edge_bottom = self.patches[patch_bottom_id][0, :]
                score += np.sum(np.abs(edge_top - edge_bottom))

        return score

    def solve_greedy_construction(self):
        """
        Builds a solution using a greedy best-fit heuristic.
        Tries starting with each patch in the corner to find the best initial guess.
        """
        best_grid = None
        min_score = float('inf')

        print("Phase 1: Running Greedy Construction Heuristic...")
        for start_patch_id in range(self.num_patches):
            grid = [[-1 for _ in range(self.grid_size)] for _ in range(self.grid_size)]
            
            # Anchor the starting patch
            grid[0][0] = start_patch_id
            
            placed_patches = {start_patch_id}
            queue = deque([(0, 0)])
            visited_cells = {(0, 0)}

            while queue:
                r, c = queue.popleft()
                
                # Check neighbors (Down, Right, Up, Left)
                for dr, dc in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                    nr, nc = r + dr, c + dc
                    
                    if 0 <= nr < self.grid_size and 0 <= nc < self.grid_size and (nr, nc) not in visited_cells:
                        visited_cells.add((nr, nc))
                        
                        # Find the best fitting patch for this empty neighbor cell
                        best_fit_patch_id = -1
                        lowest_dissimilarity = float('inf')

                        unused_patches = set(range(self.num_patches)) - placed_patches
                        
                        for patch_id in unused_patches:
                            # Temporarily place patch to calculate score
                            grid[nr][nc] = patch_id
                            
                            current_dissimilarity = self.get_dissimilarity_score_for_cell(grid, nr, nc)
                            
                            if current_dissimilarity < lowest_dissimilarity:
                                lowest_dissimilarity = current_dissimilarity
                                best_fit_patch_id = patch_id

                        # Permanently place the best patch
                        grid[nr][nc] = best_fit_patch_id
                        placed_patches.add(best_fit_patch_id)
                        queue.append((nr, nc))
            
            # After building a full grid, check its total score
            current_score = self.get_dissimilarity_score(grid)
            if current_score < min_score:
                min_score = current_score
                best_grid = copy.deepcopy(grid)

        print(f"Greedy Construction complete. Best initial score: {min_score}")
        return best_grid, min_score

    def get_dissimilarity_score_for_cell(self, grid, r, c):
        """Helper to calculate score contribution from a single cell's neighbors."""
        score = 0
        # Check Up
        if r > 0 and grid[r-1][c] != -1:
            score += np.sum(np.abs(self.patches[grid[r-1][c]][-1, :] - self.patches[grid[r][c]][0, :]))
        # Check Down
        if r < self.grid_size - 1 and grid[r+1][c] != -1:
            score += np.sum(np.abs(self.patches[grid[r][c]][-1, :] - self.patches[grid[r+1][c]][0, :]))
        # Check Left
        if c > 0 and grid[r][c-1] != -1:
            score += np.sum(np.abs(self.patches[grid[r][c-1]][:, -1] - self.patches[grid[r][c]][:, 0]))
        # Check Right
        if c < self.grid_size - 1 and grid[r][c+1] != -1:
            score += np.sum(np.abs(self.patches[grid[r][c]][:, -1] - self.patches[grid[r][c+1]][:, 0]))
        return score


    def solve_simulated_annealing(self, initial_grid):
        """
        Refines a solution using Simulated Annealing.
        """
        current_grid = copy.deepcopy(initial_grid)
        best_grid = copy.deepcopy(initial_grid)
        current_score = self.get_dissimilarity_score(current_grid)
        best_score = current_score

        initial_temp = 20000.0   # <-- Increase this significantly
        final_temp = 0.1
        alpha = 0.998  # Cooling rate
        temp = initial_temp
        
        iteration = 0
        
        print("\nPhase 2: Refining with Simulated Annealing...")
        while temp > final_temp:
            iteration += 1
            # Generate a neighbor by swapping two random patches
            r1, c1 = random.randint(0, self.grid_size-1), random.randint(0, self.grid_size-1)
            r2, c2 = random.randint(0, self.grid_size-1), random.randint(0, self.grid_size-1)
            
            neighbor_grid = copy.deepcopy(current_grid)
            neighbor_grid[r1][c1], neighbor_grid[r2][c2] = neighbor_grid[r2][c2], neighbor_grid[r1][c1]
            
            neighbor_score = self.get_dissimilarity_score(neighbor_grid)
            
            delta_e = neighbor_score - current_score
            
            # Acceptance criteria
            if delta_e < 0 or random.uniform(0, 1) < math.exp(-delta_e / temp):
                current_grid = copy.deepcopy(neighbor_grid)
                current_score = neighbor_score
                
                if current_score < best_score:
                    best_score = current_score
                    best_grid = copy.deepcopy(current_grid)
            
            temp *= alpha
            
            if iteration % 100 == 0:
                print(f"Iter: {iteration}, Temp: {temp:.2f}, Best Score: {best_score}")

        print(f"Simulated Annealing complete after {iteration} iterations.")
        return best_grid, best_score

    def reconstruct_image(self, grid):
        """Reconstructs the full image from a grid of patch IDs."""
        full_image = np.zeros(self.image.shape, dtype=np.uint8)
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                patch_id = grid[r][c]
                full_image[
                    r * self.patch_size : (r + 1) * self.patch_size,
                    c * self.patch_size : (c + 1) * self.patch_size,
                ] = self.patches[patch_id]
        return full_image

    @staticmethod
    def display_image(image, title=""):
        """Displays an image using matplotlib."""
        plt.imshow(image, cmap="gray")
        plt.title(title)
        plt.show()

def load_octave_matrix(file_path):
    """Loads image data from the specified .mat file."""
    matrix_data = []
    with open(file_path, 'r') as f:
        lines = f.readlines()[5:] # Skip header
        for line in lines:
            line = line.strip()
            if line:
                try:
                    matrix_data.append(int(line))
                except ValueError:
                    continue
    
    expected_size = 512 * 512
    if len(matrix_data) != expected_size:
        raise ValueError(f"Data size mismatch: expected {expected_size}, got {len(matrix_data)}")
        
    return np.array(matrix_data).reshape((512, 512))

if __name__ == "__main__":
    # --- Main Execution ---
    process = psutil.Process()
    start_time = time.time()
    
    # 1. Load data and initialize solver
    try:
        image_data = load_octave_matrix("scrambled_lena.mat")
        solver = JigsawSolver(image_data)
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")
        exit()

    # 2. Phase 1: Greedy Construction
    greedy_grid, greedy_score = solver.solve_greedy_construction()
    greedy_image = solver.reconstruct_image(greedy_grid)
    solver.display_image(greedy_image, f"Result after Greedy Heuristic (Score: {greedy_score})")
    
    # 3. Phase 2: Simulated Annealing
    final_grid, final_score = solver.solve_simulated_annealing(greedy_grid)
    final_image = solver.reconstruct_image(final_grid)
    solver.display_image(final_image, f"Final Result after Simulated Annealing (Score: {final_score})")

    # 4. Report Performance
    total_time = time.time() - start_time
    memory_usage_mb = process.memory_info().rss / (1024 * 1024)
    
    print("\n--- Performance Summary ---")
    print(f"Total execution time: {total_time:.2f} seconds")
    print(f"Peak memory usage: {memory_usage_mb:.2f} MB")
    print(f"Initial greedy score: {greedy_score}")
    print(f"Final SA score: {final_score}")