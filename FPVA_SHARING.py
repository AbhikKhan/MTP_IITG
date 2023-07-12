Coordinates = {}
nextMixPosition = [-1,-1,1,1,-1,0,0,1,0,-1]
levelWiseSharing = []

class Coordinate:
    def __init__(self, x: int, y: int):
        self._x = x
        self._y = y

    def __str__(self) -> str:
        return f'{self.x} {self.y} {self.interFluid}'
    
    # Getter and setter for x
    @property
    def x(self) -> int:
        return self._x

    @x.setter
    def x(self, x: int):
        self._x = x

    # Getter and setter for y
    @property
    def y(self) -> int:
        return self._y

    @y.setter
    def y(self, y: int):
        self._y = y

    # Getter and setter for intermediate fluid
    @property
    def interFluid(self) -> int:
        return self._interFluid

    @interFluid.setter
    def interFluid(self, interFluid: int):
        self._interFluid = interFluid
        

class Mixture:
    global Coordinates
    def __init__(self, x: int, y: int, mixingNode: int):
        if f'{x} {y}' not in Coordinates:
            Coordinates[f'{x} {y}'] = Coordinate(x, y)
        self._top_left = Coordinates[f'{x} {y}']
        self._top_left._interFluid = mixingNode

        if f'{x} {y+1}' not in Coordinates:
            Coordinates[f'{x} {y+1}'] = Coordinate(x, y+1)
        self._top_right = Coordinates[f'{x} {y+1}']
        self._top_right._interFluid = mixingNode

        if f'{x+1} {y}' not in Coordinates:
            Coordinates[f'{x+1} {y}'] = Coordinate(x+1, y)
        self._bottom_left = Coordinates[f'{x+1} {y}']
        self._bottom_left._interFluid = mixingNode

        if f'{x+1} {y+1}' not in Coordinates:
            Coordinates[f'{x+1} {y+1}'] = Coordinate(x+1, y+1)
        self._bottom_right = Coordinates[f'{x+1} {y+1}']
        self._bottom_right._interFluid = mixingNode

    def __str__(self) -> str:
        return f"[{self._top_left}] [{self._top_right}]\n[{self._bottom_left}] [{self._bottom_right}]"


def nextStep(x, y, level):
    if level == 0:
        return
    '''
        see the four coordinates
        If any coordinate is present in the coordinates then
            make w_coordinate["x y"]_level = 1
    '''
    for key in Coordinates:
        print(key, '->', Coordinates[key])
    fluidsInCells = {}
    if f'{x, y}' in Coordinates:
        fluidsInCells[Coordinates[f'{x, y}']] += 1

    if f'{x+1, y}' in Coordinates:
        fluidsInCells[Coordinates[f'{x+1, y}']] += 1

    if f'{x, y+1}' in Coordinates:
        fluidsInCells[Coordinates[f'{x, y+1}']] += 1

    if f'{x+1, y+1}' in Coordinates:
        fluidsInCells[Coordinates[f'{x+1, y+1}']] += 1

    print(fluidsInCells)


    mix = Mixture(x, y, level)
    for i in range(len(nextMixPosition)-1):
        nextStep(x + nextMixPosition[i], y + nextMixPosition[i+1], level-1)

def main():
    nextStep(0, 0, 2)


if __name__ == "__main__":
    main()