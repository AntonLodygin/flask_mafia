from requests import get, post, delete

print(get("http://localhost:1234/api/users").json())
print(get("http://localhost:1234/api/users/11").json())
print(post("http://localhost:1234/api/users", json={"login": "qwe", "password": "qwe"}).json())
# print(delete("http://localhost:1234/api/users/13", json={"login": "qwe", "password": "qwe"}).json())