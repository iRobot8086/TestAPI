from config import MOVIES

movies_list = []

for movie in MOVIES:
    if movie.get("language", '') == "Spanish":
        movies_list.append(movie)

print("*"*100,sep="|")
print(movies_list)
print("*"*100,sep="|")