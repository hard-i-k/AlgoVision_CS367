import random
import json

class SimpleMENACE:
    def __init__(self, stage_replication=None):
        # default replication as you had
        self.stage_replication = stage_replication or {1: 4, 3: 3, 5: 2, 7: 1}
        self.matchboxes = {}

    # --- Board Canonicalization (rotation + reflection) ---
    def get_canonical_state(self, board):
        # board is list of 9 entries ["X","O"," "]
        rotations = [
            board,
            self.rotate(board),
            self.rotate(self.rotate(board)),
            self.rotate(self.rotate(self.rotate(board)))
        ]
        reflections = [self.reflect(b) for b in rotations]
        all_states = rotations + reflections
        # convert each state to tuple of strings and pick lexicographically smallest
        all_tuples = [tuple(s) for s in all_states]
        return tuple(min(all_tuples))

    def rotate(self, b):
        return [b[6], b[3], b[0],
                b[7], b[4], b[1],
                b[8], b[5], b[2]]

    def reflect(self, b):
        return [b[2], b[1], b[0],
                b[5], b[4], b[3],
                b[8], b[7], b[6]]

    # --- Initialize matchbox for a canonical state ---
    def init_matchbox(self, canonical_state, stage):
        moves = [i for i, v in enumerate(canonical_state) if v == " "]
        # store bead counts as ints
        self.matchboxes[canonical_state] = {int(m): int(self.stage_replication[stage]) for m in moves}

    def compute_stage(self, d):
        if d <= 1:
            return 1
        elif d <= 3:
            return 3
        elif d <= 5:
            return 5
        return 7

    # choose_move now returns (move, canonical_state, stage)
    def choose_move(self, board, move_number, game_length_estimate):
        canonical_state = self.get_canonical_state(board)
        distance_from_end = game_length_estimate - move_number
        stage = self.compute_stage(distance_from_end)

        # ensure matchbox exists for this canonical state using the stage
        if canonical_state not in self.matchboxes:
            self.init_matchbox(canonical_state, stage)

        beads = self.matchboxes[canonical_state]
        total = sum(beads.values())
        # pick a bead uniformly at random among total beads
        r = random.randint(1, total)
        cum = 0
        for move, count in beads.items():
            cum += count
            if r <= cum:
                return move, canonical_state, stage

    def update_beads(self, game_history, result):
        # game_history: list of (canonical_state, move, stage)
        for board_state, move, stage in game_history:
            rep = self.stage_replication[stage]
            # initialize safety if missing (shouldn't happen)
            if board_state not in self.matchboxes:
                self.init_matchbox(board_state, stage)
            if result == "win":
                self.matchboxes[board_state][move] += 3 * rep
            elif result == "draw":
                self.matchboxes[board_state][move] += 1 * rep
            else:  # loss
                self.matchboxes[board_state][move] = max(1, self.matchboxes[board_state][move] - rep)

    # Save and load reliably converting tuple keys to JSON strings
    def save(self, filename="matchboxes.json"):
        serial = {}
        for k, v in self.matchboxes.items():
            # k is tuple of 9 strings -> convert to list then dump
            ks = json.dumps(list(k))
            serial[ks] = v
        with open(filename, "w") as f:
            json.dump(serial, f)

    def load(self, filename="matchboxes.json"):
        with open(filename, "r") as f:
            serial = json.load(f)
        self.matchboxes = {}
        for ks, v in serial.items():
            k = tuple(json.loads(ks))  # restore tuple of strings
            # inner dict keys might be strings due to JSON -> convert back to int
            self.matchboxes[k] = {int(m): int(c) for m, c in v.items()}
