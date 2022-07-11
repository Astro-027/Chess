import pygame

class Piece:
    def __init__(self, sprite: pygame.image, start_pos: (int, int), piece_name = 'pawn', turn: int = 0, piece_moves = [('0', '1'), ('F', '0', '1|2')], different_attacks = None):
      self.sprite = sprite
      self.start_pos = start_pos
      self.pos = start_pos
      self.current_pos = start_pos
      self.piece_name = piece_name
      self.turn = turn
      self.piece_moves = piece_moves
      self.different_attacks = different_attacks
      self.move_count = 0
      self.capturables = []
      
    
    def move_piece(self, x, y, other_pieces):
        if self.movable(x, y, other_pieces):
          self.current_pos = (x, y)
          self.pos = (x, y)
          self.move_count += 1
        else:
          self.pos = self.current_pos
        return self.current_pos
    
    def force_move(self, x, y, condition = True):
        if condition:
          self.current_pos = (x, y)
          self.move_count += 1
        return self.current_pos
    
    def movable(self, target_x, target_y, pieces) -> bool:
        if target_x < 0 or target_x > 7 or target_y < 0 or target_y > 7:
            return False
        return (target_x, target_y) in self.get_movement(pieces) or (target_x, target_y) in self.get_capturables(pieces)
    
    def get_movement(self, pieces):
        blocks = []
        self.capturables = []
        piece_positions = [p.current_pos for p in pieces]
  
        for i in [list(move) for move in self.piece_moves]:
          if 'F' in i and self.move_count != 0 or self.current_pos == None:
            continue
          pos = [(self.current_pos[0] + j[0], self.current_pos[1] - j[1]) for j in self.movable_blocks(i)]
          # if pieces != []:
          for p in pos:
            if p not in [piece.current_pos for piece in pieces]:
              blocks.append(p)
            else:
              if self.different_attacks == None and pieces[piece_positions.index(p)].turn != self.turn:
                self.capturables.append(p)
              break
          else:
            blocks += pos
        return blocks

    def get_capturables(self, pieces):
        piece_positions = [p.current_pos for p in pieces]
        if self.different_attacks == None:
            self.get_movement(pieces)
        else:
            self.capturables = []
            attack_list = [list(attack) for attack in self.different_attacks]
            for i in attack_list:
                if 'F' in i and self.move_count != 0 or self.current_pos == None:
                    continue
                pos = [(self.current_pos[0] + j[0], self.current_pos[1] - j[1]) for j in self.movable_blocks(i)]
                for p in pos:
                  if p in [piece.current_pos for piece in pieces]:
                    if pieces[piece_positions.index(p)].turn != self.turn:
                      self.capturables.append(p)
                    break
        return self.capturables
  
    def movable_blocks(self, area):
        blocks = []
        pos_x = []
        pos_y = []
        if '|' in area[-2]:
          while area[-2].split('|')[0] != area[-2].split('|')[1]:
            pos_x.append(int(area[-2].split('|')[0]))
            if int(area[-2].split('|')[0]) < int(area[-2].split('|')[1]):
              area[-2] = str(int(area[-2].split('|')[0]) + 1) + '|' + area[-2].split('|')[1]
            else:
              area[-2] = str(int(area[-2].split('|')[0]) - 1) + '|' + area[-2].split('|')[1]
        else:
          pos_x = [int(area[-2])]
        
        if '|' in area[-1]:
          while area[-1].split('|')[0] != area[-1].split('|')[1]:
            pos_y.append(int(area[-1].split('|')[0]))
            if int(area[-1].split('|')[0]) < int(area[-1].split('|')[1]):
              area[-1] = str(int(area[-1].split('|')[0]) + 1) + '|' + area[-1].split('|')[1]
            else:
              area[-1] = str(int(area[-1].split('|')[0]) - 1) + '|' + area[-1].split('|')[1]
        else:
          pos_y = [int(area[-1])]
        
        for i in range(max([len(pos_x), len(pos_y)])):
            x = pos_x[-1] if pos_x.index(pos_x[-1]) < i else pos_x[i]
            y = pos_y[-1] if pos_y.index(pos_y[-1]) < i else pos_y[i]
            blocks.append((x, y))
        return blocks
      
    def destroy_piece(self):
        self.current_pos = None
        self.pos = None