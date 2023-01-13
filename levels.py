from small_enemy import normal

leveldata = data = eval('\t'.join([line.strip() for line in open('levels.txt').readlines()]))

class Levels():
    def __init__(self) -> None:
        self.level = 0
        self.iteration = 0
        self.wait = 0
        self.end = False
        self.game_end = False
    
    def apply_spawn(self):
        if self.wait > 0:
            self.wait -= 50
        else :
            try:
                for key, value in leveldata[self.level][self.iteration].items():
                    match key:
                        case 'normal':
                            normal(value[0], value[1])
                            self.iteration += 1
                        case 'wait':
                            self.wait = value
                            self.iteration += 1
            except IndexError:
                if self.level >= len(leveldata):
                    self.game_end = True
                self.end = True