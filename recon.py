import socket

domain = input("Domaine : ")


try:
	ip = socket.gethostbyname(domain)
	print(f"IP : {ip}")
except:
	print("Erreur")
