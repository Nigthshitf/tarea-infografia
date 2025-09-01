extends Area2D

@export var closed_texture: Texture2D
@export var open_texture: Texture2D
var is_open: bool = false

func _ready() -> void:
	close()
	print("Door initialized. Current state: closed")

func open():
	if not is_open:
		is_open = true
		$CollisionShape2D.disabled = false  # Keep collision enabled for detection
		$Sprite2D.texture = open_texture
		print("Door opened!")
	
func close():
	is_open = false
	$CollisionShape2D.disabled = false  # Keep collision enabled for detection
	$Sprite2D.texture = closed_texture
	print("Door closed!")

func _on_body_entered(body: Node2D) -> void:
	print("Door: Body entered: ", body.name)
	if body.is_in_group("player"):
		print("Door: Player detected!")
		if body.has_method("can_open_doors"):
			print("Door: Player has can_open_doors method")
			if body.can_open_doors():
				print("Door: Player has key, opening door!")
				open()
			else:
				print("Door: Player does not have key")
		else:
			print("Door: Player does not have can_open_doors method")

func _on_body_exited(body: Node2D) -> void:
	print("Door: Body exited: ", body.name)
	# Door stays open once opened with key
	# if body.is_in_group("player"):
	#     print("Door: Player left, closing door!")
	#     close()
