extends Node2D

@onready var door: Area2D = $Door
@onready var player: CharacterBody2D = $Player
@onready var health_label: Label = $UI/HealthLabel
@onready var power_label: Label = $UI/PowerLabel

func _ready() -> void:
	$Key.collected.connect(on_key_collected)
	# Connect gem if it exists in the scene
	if has_node("Gem"):
		$Gem.collected.connect(on_gem_collected)
	
	# Connect player health signal
	player.health_changed.connect(on_player_health_changed)
	
	# Connect player power signals
	player.power_activated.connect(on_player_power_activated)
	player.power_deactivated.connect(on_player_power_deactivated)
	player.power_time_updated.connect(on_player_power_time_updated)
	
	# Update initial health display
	on_player_health_changed(player.health)
	
func on_key_collected():
	print("Key collected in main!")
	player.collect_key()

func on_gem_collected():
	player.collect_gem()

func on_player_health_changed(new_health: int):
	health_label.text = "HP: " + str(new_health)

func on_player_power_activated():
	power_label.show()

func on_player_power_deactivated():
	power_label.hide()

func on_player_power_time_updated(time_left: float):
	power_label.text = "Poder: " + str(int(ceil(time_left)))
