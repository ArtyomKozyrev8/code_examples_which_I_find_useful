from collections import namedtuple

Card = namedtuple("Card", ["color", "name", "points"])


class CardDesk:
    color_price = {"rd": 1, "bl": 1, "gr": 1, "wh": 1}
    name_price = {"6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "11": 11, "Q": 4, "J": 3, "K": 5}
    colors = ["rd", "bl", "gr", "wh"]
    names = [str(i) for i in range(6, 12)] + list("QJK")

    def __init__(self):
        self.desk = [Card(_color, _name, CardDesk.color_price[_color] + CardDesk.name_price[_name])
                     for _color in CardDesk.colors for _name in CardDesk.names]

    def __getitem__(self, item):
        return self.desk[item]

    def __len__(self):
        return len(self.desk)


if __name__ == '__main__':
    desk = CardDesk()
    f = lambda x: x.points
    for i in sorted(desk, key=f):
        print(i)
