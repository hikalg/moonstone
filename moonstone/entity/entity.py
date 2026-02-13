class Entity:
    e_name: str = ""
    e_alias: list[str] = []
    e_playscore: float = 1.0
    e_rating: float = 1200

    def __init__(self, name: str) -> None:
        self.e_name = name
        self.print_entity()

    def print_entity(self) -> None:
        print(
            f"----------\n{self.e_name}\n----------\nA: {self.e_alias}\nR: {self.e_rating}\nP: {self.e_playscore}"
        )

    def add_alias(self, name: str | list = "") -> list[str]:
        alias = []
        if isinstance(name, str):
            alias.append(name)
        if isinstance(name, list):
            for x in name:
                alias.append(str(x))

        for x in alias:
            self.e_alias.append(x)

        return self.e_alias

    def set_rating(self, rating: float = 0):
        self.e_rating = rating if rating != 0 else self.e_rating
        return self.e_rating

