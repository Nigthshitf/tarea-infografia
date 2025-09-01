extends Node

func _ready():
	print("=== DEBUG TEST ===")
	
	# Test if main scene has the nodes
	var main = get_node("/root/Main")
	if main:
		print("Main node found")
		
		if main.has_node("Key"):
			print("Key node found in main")
			var key = main.get_node("Key")
			print("Key script: ", key.get_script())
		else:
			print("Key node NOT found in main")
			
		if main.has_node("Player"):
			print("Player node found in main")
			var player = main.get_node("Player")
			print("Player has_key: ", player.has_key if player.has("has_key") else "No has_key property")
		else:
			print("Player node NOT found in main")
			
		if main.has_node("Door"):
			print("Door node found in main")
		else:
			print("Door node NOT found in main")
	else:
		print("Main node NOT found")
