extends Area2D

signal collected

func _on_body_entered(body: Node2D) -> void:
	# Check if the body is the player
	if body.is_in_group("player"):
		print("Key: Player collected the key!")
		collected.emit()
		queue_free()
