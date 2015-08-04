_number = 'number'
_count = 'count'
_step = 'step'
_location = 'location'
_token_map = {'#':_number, '|':_count, '$':_step, '@':_location}

def _replace_entries(map1, map2):
    return {t:map2[t] if t in map2 else map1[t]
            for t in map1.keys()|map2.keys()}

#Some functions for evolving stuff
def _evolve_number(tokens):
    curr_val = int(tokens[_number])
    stp = 1
    if _step in tokens:
        stp = int(tokens[_step])
    return curr_val + stp
_evolution_map = {_number:_evolve_number}

#Some functions for printing stuff
def _print_number(tokens):
    if _count in tokens:
        return ''
    return '#'+tokens[_number]
def _print_count(tokens):
    if not _number in tokens:
        return ''
    return tokens[_number]+' of '+tokens[_count]
def _print_step(tokens):
    return ''
def _print_location(tokens):
    return '@'+tokens[_location]
_print_map = {_number:_print_number, _count:_print_count,
        _step:_print_step, _location:_print_location}

class special:
    tokens = { }
    token_map = _token_map
    evolution_map = _evolution_map
    print_map = _print_map

    def __init__(self, tokens,
            token_map=_token_map,
            evolution_map=_evolution_map,
            print_map=_print_map):
        self.evolution_map = _replace_entries(_evolution_map, evolution_map)
        self.token_map = _replace_entries(_token_map, token_map)
        self.print_map = _replace_entries(_print_map, print_map)
        self.tokens = {self.token_map[tk]:tokens[tk] for tk in tokens
                        if tk in self.token_map}

    def has_next(self):
        if not _count in self.tokens or not _number in self.tokens:
            return True
        if not _number in self.evolution_map:
            return True
        return self.evolution_map[_number](self.tokens) \
                <=int(self.tokens[_count])

    def evolve(self):
        self.tokens = {tk:self.evolution_map[tk](self.tokens)
                if tk in self.evolution_map else self.tokens[tk]
                for tk in self.tokens}

    def print(self):
        tmp = [self.print_map[tk](self.tokens) for tk in self.tokens]
        return [st for st in tmp if st != '']
