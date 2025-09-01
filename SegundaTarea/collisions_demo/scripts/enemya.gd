extends Node2D

var rn = RandomNumberGenerator.new()
const FireballScene = preload("res://scenes/fireball.tscn")

@onready var animation_player: AnimationPlayer = $AnimationPlayer
@onready var timer: Timer = $Timer
@export var attack_damage: int = 10
var player_in_range: bool = false
var can_be_stomped: bool = true

func _ready() -> void:
	print("Enemy A initialized")
	timer.one_shot = true
	timer.wait_time = rn.randi_range(1, 3)
	timer.stop()
	animation_player.play("Idle")

func shoot_fireball():
	var fireball_instance = FireballScene.instantiate()
	get_parent().add_child(fireball_instance)
	fireball_instance.global_position = global_position
	fireball_instance.direction = Vector2(rn.randf_range(-1, 1), rn.randf_range(-1, 1))
	fireball_instance.speed = rn.randi_range(30, 200)

func _on_timer_timeout() -> void:
	shoot_fireball()
	timer.wait_time = rn.randi_range(1, 3)
	timer.start()

func _on_activate_zone_body_entered(body: Node2D) -> void:
	print("Enemy A: Body entered activation zone: ", body.name)
	if body.is_in_group("player"):
		print("Enemy A: Player detected, activating")
		player_in_range = true
		animation_player.play("Active")
		timer.start()

func _on_activate_zone_body_exited(body: Node2D) -> void:
	print("Enemy A: Body exited activation zone: ", body.name)
	if body.is_in_group("player"):
		print("Enemy A: Player left, deactivating")
		player_in_range = false
		animation_player.play("Idle")
		timer.stop()

func _on_hurtbox_body_entered(body: Node2D) -> void:
	print("Enemy A: Hurtbox collision with: ", body.name)
	if body.is_in_group("player"):
		# If player has gem power, enemy dies on any contact
		if body.has_method("can_stomp_enemies") and body.can_stomp_enemies():
			print("Enemy A: Player has gem power, enemy destroyed by touch!")
			take_damage(999)  # Instant kill
		elif body.has_method("take_damage"):
			print("Enemy A: Player has no gem power, dealing damage")
			body.take_damage(attack_damage)

func take_damage(amount: int):
	print("Enemy A: Taking damage: ", amount, " - DESTROYED!")
	queue_free()
