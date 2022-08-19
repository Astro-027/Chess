import pygame

from config import *


class Piece:
    def __init__(self, pos: (int, int), turn: int, piece_name: str = None):
        self.piece_name = piece_name
        self.sprite = None
        self.image_path = None
        self.piece_moves = []
        self.disabled_moves = []
        self.piece_attacks = None
        # self.stale_mate = False # TODO: No moves left
        self.protectors = []

        self.start_pos, self.pos, self.current_pos = pos, pos, pos
        self.turn = turn
        
        self.captured = False
        self.move_count = 0
    
    def input(self, event: pygame.event):
        if event.type == pygame.VIDEORESIZE:
            self.sprite = pygame.image.load(self.image_path)
    
    def update(self, pieces=[], board_turns=False):
        pass

    def draw(self, screen, blit_size: (int, int), panel, rotate = 0):
        if self.image_path == None or self.pos == None:
            return
        self.sprite = pygame.image.load(self.image_path)
        x, y = self.pos
        x_pos = x * panel.width / 8 + (panel.x + 5)
        y_pos = y * panel.height / 8 + (panel.y + 5)
        self.sprite = pygame.transform.rotate(self.sprite, rotate)
        self.sprite = pygame.transform.smoothscale(self.sprite, blit_size)
        screen.blit(self.sprite, (x_pos, y_pos))
    
    def move_piece(self, x, y, current_turn=0, other_pieces=[]) -> (int, int):
        if self.is_valid_move(x, y, other_pieces) and self.turn == current_turn:
            self.current_pos = (x, y)
            self.pos = (x, y)
            self.move_count += 1
        else:
            self.pos = self.current_pos
        return self.current_pos
    
    def force_move(self, x, y, count_move = True, condition = True) -> (int, int):
        if condition:
            self.current_pos = (x, y)
            self.pos = (x, y)
            if count_move:
                self.move_count += 1
        return self.current_pos

    def is_valid_move(self, target_x, target_y, other_pieces=[]) -> bool:
        if target_x < 0 or target_x > 7 or target_y < 0 or target_y > 7 or (target_x, target_y) == self.current_pos:
            return False
        return (target_x, target_y) in self.get_movement(other_pieces) or (target_x, target_y) in self.get_capturables(other_pieces)
    
    def get_movement(self, other_pieces):
        blocks = []
        self.capturables = []
        piece_positions = []
        
        if other_pieces != []:
            piece_positions = [p.current_pos for p in other_pieces]
        
        if self.piece_moves == None:
            return blocks
        
        for move in list(self.piece_moves):
            if self.current_pos == None:
                continue
            pos = self.add_to_pos(move)
            
            for p in pos:
                if p not in piece_positions:
                    blocks.append(p)
                else:
                    if (self.piece_attacks == None) and other_pieces[piece_positions.index(p)].turn != self.turn:
                        self.capturables.append(p)
                    break
            else:
                blocks += pos
        
        if self.disabled_moves == []:
            return blocks
        self.capturables = [c for c in self.capturables if c not in self.disabled_moves]
        return [b for b in blocks if b not in self.disabled_moves]

    def get_capturables(self, other_pieces):
        if self.piece_attacks == None:
            self.get_movement(other_pieces)
        else:
            piece_positions = [p.current_pos for p in other_pieces]

            self.capturables = []
            for attack in list(self.piece_attacks):
                if self.current_pos == None:
                    continue
                pos = self.add_to_pos(attack)
                for p in pos:
                    if p in piece_positions and p not in self.disabled_moves:
                        piece = other_pieces[piece_positions.index(p)]
                        if piece.turn != self.turn:
                            self.capturables.append(p)
                        break
        return self.capturables

    def add_to_pos(self, move: str):
        return [
            (self.current_pos[0] + j[0], self.current_pos[1] - j[1])
            for j in self.decode_move(move) 
            if self.current_pos[0] + j[0] in range(0, 8) and self.current_pos[1] - j[1] in range(0, 8)
        ]
        
    def reflect_place(self):
        '''
            Mirrors the pieces position.
        '''
        if self.current_pos == None:
            return
        x = 7 - self.current_pos[0]
        y = 7 - self.current_pos[1]
        self.force_move(x, y, False)
        self.piece_moves = self.get_reflected_move(self.piece_moves)
        if self.piece_attacks != None:
            self.piece_attacks = self.get_reflected_move(self.piece_attacks)
        return (x, y)

    def get_reflected_move(self, old_move:[(str)]) -> [(str)]:
        '''
            Returns reflected movement of a piece!
        '''
        new_move = []
        for move in old_move:
            new_points = []
            for point in move:
                temp = point
                try:
                    temp = str(int(temp) * -1)
                except:
                    temp = str(int(temp.split('|')[0]) * -1) + '|' + str(int(temp.split('|')[1]) * -1)
                new_points.append(temp)
            new_move.append(new_points)
        return new_move

    def decode_move(self, area: list) -> [(int, int)]:
        '''
            Return all possible blocks as a list
        '''
        blocks = []
        pos_x = []
        pos_y = []
        if "|" in area[-2]:
            pos_x = self._get_n2n(n2n=area[-2], seperator="|")
        else:
            pos_x = [int(area[-2])]
        
        if "|" in area[-1]:
            pos_y = self._get_n2n(n2n=area[-1], seperator="|")
        else:
            pos_y = [int(area[-1])]
        
        for i in range(max([len(pos_x), len(pos_y)])):
            if pos_x == [] or pos_y == []:
                continue
            x = pos_x[-1] if pos_x.index(pos_x[-1]) < i else pos_x[i]
            y = pos_y[-1] if pos_y.index(pos_y[-1]) < i else pos_y[i]
            blocks.append((x, y))
        return blocks

    def destroy_piece(self):
        self.current_pos = None
        self.pos = None
        self.captured = True
    
    def _get_n2n(self, n2n: str, seperator: str):
        '''
            Returns List of numbers from n2n by seperating
            with the seperator.
            i.e: n2n = 1|5, seperator = '|' -> [1, 2, 3, 4, 5]
        '''
        nums = []
        n1, n2 = n2n.split(seperator)[0:2]
        if '-' in n2:
            n2 = str(int(n2) - 1) # for the loop, we need to add 1 to the second number
        else:
            n2 = str(int(n2) + 1)
            
        while n1 != n2:
            nums.append(int(n1))
            if int(n1) < int(n2):
                n1 = str(int(n1) + 1)
            else:
                n1 = str(int(n1) - 1)
        
        return nums

    def _set_sprite(self, turn, white_piece_name, black_piece_name):
        if turn == 0:
            self.image_path = WHITE_PIECES_PATH + white_piece_name
        else:
            self.image_path = BLACK_PIECES_PATH + black_piece_name
    
    def _change_turn(self, pieces):
        piece_turns = [p.turn for p in pieces]
        if self.turn < max(piece_turns):
            self.turn += 1
        else:
            self.turn = min(piece_turns)

    def is_protected(self, pieces) -> bool:
        self._change_turn(pieces)
        self.protectors = [p for p in pieces if p.turn == self.turn and self.current_pos in p.get_capturables(pieces)]
        self._change_turn(pieces)
        return len(self.protectors) > 0

class Pawn(Piece):
    def __init__(self, pos, turn):
        super().__init__(pos, turn, "pawn")
        self.piece_moves = [('0', '1|2')] if turn == 0 else [('0', '-1|-2')]
        self.piece_attacks = [('-1', '1'), ('1', '1')] if turn == 0 else [('-1', '-1'), ('1', '-1')]
        self._set_sprite(turn, "pawn_top.png", "pawn_top.png")
        self.en_passant = None
    
    def update(self, pieces=[], board_turns=False):
        self.board_turns = board_turns
        if self.move_count > 0:
            if board_turns:
                self.piece_moves = [('0', '1')]
            else:
                self.piece_moves = [('0', '1')] if self.turn == 0 else [('0', '-1')]
    
    def check_enpassant(self, pieces):
        # if self.en_passant != None:
        #     self.en_passant = []
        #     return False
        self.en_passant = None
        opponent_pawns = [p for p in pieces if not p.captured and p.turn != self.turn and p.move_count == 1 and p.piece_name == self.piece_name and p.current_pos[1] in [3, 4]]
        opponents_positions = [p.current_pos for p in opponent_pawns]
        if (self.current_pos[0] - 1, self.current_pos[1]) in opponents_positions: # Checks the left side of our pawn
            opponent_pawns_index = opponents_positions.index((self.current_pos[0] - 1, self.current_pos[1]))
            self.en_passant = opponent_pawns[opponent_pawns_index]
        if (self.current_pos[0] + 1, self.current_pos[1]) in opponents_positions: # Checks the right side of our pawn
            opponent_pawns_index = opponents_positions.index((self.current_pos[0] + 1, self.current_pos[1]))
            self.en_passant = opponent_pawns[opponent_pawns_index]
        return self.en_passant != None

    def do_enpassant(self):
        if self.en_passant == None: return False
        if (not self.board_turns and self.turn == 0) or not self.board_turns:
            self.force_move(self.en_passant.current_pos[0], self.current_pos[1] + 1)
        else:
            self.force_move(self.en_passant.current_pos[0], self.current_pos[1] - 1)
        self.en_passant.destroy_piece()
    
    
class Bishop(Piece):
    def __init__(self, pos, turn):
        super().__init__(pos, turn, "bishop")
        self.piece_moves = [("1|8", "1|8"), ("-1|-8", "-1|-8"), ("-1|-8", "1|8"), ("1|8", "-1|-8")]
        self._set_sprite(turn, "bishop_top.png", "bishop_top.png")

class Knight(Piece):
    def __init__(self, pos, turn):
        super().__init__(pos, turn, "knight")
        self.piece_moves = [("1", "2"), ("1", "-2"), ("-1", "2"), ("-1", "-2"), ("2", "1"), ("2", "-1"), ("-2", "-1"), ("-2", "1")]
        self._set_sprite(turn, "knight_top.png", "knight_top.png")

class Rook(Piece):
    def __init__(self, pos, turn):
        super().__init__(pos, turn, "rook")
        self.piece_moves = [("1|8", "0"), ("0", "1|8"), ("-1|-8", "0"), ("0", "-1|-8")]
        self._set_sprite(turn, "rook_top.png", "rook_top.png")

class Queen(Piece):
    def __init__(self, pos, turn):
        super().__init__(pos, turn, "queen")
        self.piece_moves = [("1|8", "0"), ("0", "1|8"), ("-1|-8", "0"), ("0", "-1|-8"), ("1|8", "1|8"), ("-1|-8", "-1|-8"), ("-1|-8", "1|8"), ("1|8", "-1|-8")]
        self._set_sprite(turn, "queen_top.png", "queen_top.png")
        
class King(Piece):
    def __init__(self, pos, turn):
        super().__init__(pos, turn, "king")
        self.piece_moves = [("1", "1"), ("1", "-1"), ("-1", "1"), ("-1", "-1"), ("1", "0"), ("0", "1"), ("-1", "0"), ("0", "-1")]
        self._set_sprite(turn, "king_top.png", "king_top.png")
        self.threats = []
        self.capturables = []
        self.castling_blocks = []
        self.check_count = 0
    
    def update(self, pieces=[], board_turns=False):
        self.board_turns = board_turns
    
    def move_piece(self, x, y, current_turn=0, other_pieces=[]) -> (int, int):
        if self.is_valid_move(x, y, other_pieces) and self.turn == current_turn:
            self.current_pos = (x, y)
            self.pos = (x, y)
            self.move_count += 1
            self.threads = []
        else:
            self.pos = self.current_pos
        return self.current_pos
    
    def set_disabled_moves(self, pieces):
        openents = [p for p in pieces if p.turn != self.turn]
        opponents_positions = [p.current_pos for p in openents]
        for piece in pieces:
            piece.disabled_moves = []
            hold_pos = piece.current_pos
            destroyed_piece = None
            if piece.turn != self.turn:
                continue
            for move in (piece.get_movement(pieces) + piece.get_capturables(pieces)):
                piece.force_move(move[0], move[1], False)
                if piece.current_pos in opponents_positions:
                    destroyed_piece = openents[opponents_positions.index(move)]
                    pieces.remove(destroyed_piece)
                if self.is_check(pieces, self.current_pos):
                    piece.disabled_moves.append(move)
                if destroyed_piece != None:
                    pieces.append(destroyed_piece)
                    destroyed_piece = None
                piece.force_move(hold_pos[0], hold_pos[1], False)
    
    def is_check(self, pieces: Piece, pos) -> bool:
        self.threats = [piece for piece in pieces if piece.turn != self.turn and pos in piece.get_capturables(pieces)]
        check = len(self.threats) > 0
        if check: self.check_count += 1
        return check
    
    def check_castling(self, pieces):
        self.castling_blocks = []
        self.rooks_can_castle = []
        self.piece_moves = [("1", "1"), ("1", "-1"), ("-1", "1"), ("-1", "-1"), ("1", "0"), ("0", "1"), ("-1", "0"), ("0", "-1")]
        if self.move_count > 0 or self.check_count > 0:
            return False
        rooks = [piece for piece in pieces if piece.turn == self.turn and piece.piece_name == 'rook']
        if all(rook.move_count > 0 for rook in rooks):
            return False
        change_x = (2, 6)
        point_y = 7 
        if not self.board_turns:
            if self.turn != 0: point_y = 0
        elif self.turn != 0:
            change_x = (1, 5)
        for rook in rooks:
            if rook.move_count == 0:
                if rook.current_pos == (0, point_y):
                    self.piece_moves += [('-1|-3', '0')]
                    if rook.is_valid_move(change_x[0] + 1, point_y, pieces) and self.is_valid_move(change_x[0], point_y, pieces):
                        self.castling_blocks += [(change_x[0], point_y)]
                        self.rooks_can_castle.append(rook)
                    self.piece_moves.remove(('-1|-3', '0'))
                elif rook.current_pos == (7, point_y):
                    self.piece_moves += [('1|3', '0')]
                    if rook.is_valid_move(change_x[1] - 1, point_y, pieces) and self.is_valid_move(change_x[1], point_y, pieces):
                        self.castling_blocks += [(change_x[1], point_y)]
                        self.rooks_can_castle.append(rook)
                    self.piece_moves.remove(('1|3', '0'))
        return len(self.castling_blocks) > 0

    def do_castling(self, block):
        if block not in self.castling_blocks:
            return
        self.force_move(block[0], block[1])
        for rook in self.rooks_can_castle:
            print(rook.current_pos)
            if block[0] + 1 == rook.current_pos[0] or block[0] + 2 == rook.current_pos[0]:
                rook.force_move(block[0] - 1, block[1], False)
                break
            elif block[0] - 2 == rook.current_pos[0] or block[0] - 1 == rook.current_pos[0]:
                rook.force_move(block[0] + 1, block[1], False)
                break
        return
                