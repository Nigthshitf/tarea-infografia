extends Area2D

@export var direction: Vector2 = Vector2.ZERO
@export var speed: float = 0
@export var damage: int = 15

func _physics_process(delta: float) -> void:
	position += direction * speed * delta


func _on_area_entered(area: Area2D) -> void:
	queue_free()


func _on_body_entered(body: Node2D) -> void:
	print("Fireball hit: ", body.name)
	if body.is_in_group("player") and body.has_method("take_damage"):
		print("Fireball dealing damage to player: ", damage)
		body.take_damage(damage)
	queue_free()
