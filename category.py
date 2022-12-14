class Category:
    categories: list = []

    def __init__(self) -> None:
        with open(file="categories.txt") as file:
            for line in file:
                x = line[:-1]
                self.categories.append(x)

        file.close()

    def add_category(self, category: str) -> None:
        category = category.lower()
        
        for item in self.categories:
            if item == category:
                raise Exception(ValueError("Alredy excist category"))
        
        self.categories.append(category)
        with open(file="categories.txt", mode='w') as file:
            for item in self.categories:
                file.write("%s\n" %item)

        file.close()
