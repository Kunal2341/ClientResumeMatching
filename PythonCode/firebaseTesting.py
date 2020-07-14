from firebase import firebase
firebase = firebase.FirebaseApplication("https://resumematcher-8706e.firebaseio.com/", None)
name = input("Name: ")
email = input("Email: ")
phone = input("Phone: ")
experience = input("Experience: ")
data = {
    'name': name,
    'Email': email,
    'Phone': phone,
    'Experience': experience,
}
result = firebase.post(name, data)
print(name)
print("\nRecord Inserted")
print(result)