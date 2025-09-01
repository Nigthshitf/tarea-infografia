extends Area2D

signal collected

func _on_body_entered(body: Node2D) -> void:
	print("Gem: Body entered: ", body.name)
	# Check if the body is the player
	if body.is_in_group("player"):
		print("Gem: Player collected gem!")
		collected.emit()
		queue_free()
