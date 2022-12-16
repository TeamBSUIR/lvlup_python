STORAGE_CATEGORIES_FILENAME = "categories.txt"


class Category:
    def get_category(self) -> list[str]:
        self.categories = []
        with open(file=STORAGE_CATEGORIES_FILENAME) as file:
            for line in file:
                x = line[:-1]
                self.categories.append(x)

        return self.categories

    def parse_to_int(self, category: str) -> int:
        return Category().get_category().index(category)

    def add_category(self, category: str) -> None:
        category = category.lower()

        self.categories = self.get_category()
        for item in self.categories:
            if item == category:
                raise Exception(ValueError("Alredy excist category"))

        self.categories.append(category)
        with open(file=STORAGE_CATEGORIES_FILENAME, mode="w") as file:
            for item in self.categories:
                file.write("%s\n" % item)
