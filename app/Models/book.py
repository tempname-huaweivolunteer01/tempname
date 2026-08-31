class Book:
    id: int
    name:str
    author:str
    genre:str
    launch_date:str

    def __init__(self,
                 id:int,
                 name:str,
                 author:str,
                 genre:str,
                 launch_date:str) -> None:
        self.id = id
        self.name = name
        self.author = author
        self.genre = genre
        self.launch_date = launch_date
