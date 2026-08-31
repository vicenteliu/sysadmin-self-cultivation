extends SceneTree

# Proves the one claim the plate makes: from the lift lobby, along circulation only,
# every room and space is reachable without crossing a desk cell.
#
#   PLATE=/abs/path/reference-office.plate.json \
#     cli-anything-godot -p tools/floor/godot script run prove_topology.gd
#
# Exit 0 and a JSON verdict on stdout when it holds; exit 1 and the list of what could
# not be reached when it does not. It asserts nothing about widths, distances or
# compliance — see docs/adr/0014-the-plate-stops-at-topology.md for why not.

func _init() -> void:
	var path := OS.get_environment("PLATE")
	if path == "":
		printerr("PLATE is not set")
		quit(2); return
	var handle := FileAccess.open(path, FileAccess.READ)
	if handle == null:
		printerr("cannot read " + path)
		quit(2); return
	var plate: Dictionary = JSON.parse_string(handle.get_as_text())
	if plate == null:
		printerr("plate is not valid JSON")
		quit(2); return

	var w: int = plate["grid"]["w"]
	var h: int = plate["grid"]["h"]
	var walkable := {}
	var blocked := {}

	# Furniture blocks. A pod is four rows deep: chair, desk, desk, chair.
	for pod in plate["desks"]["pods"]:
		var px: int = pod["at"][0]
		var py: int = pod["at"][1]
		var per_side: int = int(ceil(float(pod["seats"]) / 2.0))
		for i in range(per_side):
			for dy in range(4):
				blocked[Vector2i(px + i, py + dy)] = true

	# Circulation is walkable by definition — that is what makes it circulation.
	for leg in plate["circulation"]:
		var r: Array = leg["rect"]
		for y in range(r[1], r[1] + r[3]):
			for x in range(r[0], r[0] + r[2]):
				walkable[Vector2i(x, y)] = true

	# An enclosed space is walkable inside its walls, plus the one cell of wall its door
	# occupies. Everything else on the perimeter stays solid.
	var enclosed: Array = []
	enclosed.append_array(plate["rooms"])
	enclosed.append_array(plate["spaces"])
	enclosed.append_array(plate["booths"])
	for space in enclosed:
		var r: Array = space["rect"]
		for y in range(r[1] + 1, r[1] + r[3] - 1):
			for x in range(r[0] + 1, r[0] + r[2] - 1):
				walkable[Vector2i(x, y)] = true
		var d: Dictionary = space["door"]
		var at: int = d["at"]
		match d["side"]:
			"n": walkable[Vector2i(at, r[1])] = true
			"s": walkable[Vector2i(at, r[1] + r[3] - 1)] = true
			"w": walkable[Vector2i(r[0], at)] = true
			"e": walkable[Vector2i(r[0] + r[2] - 1, at)] = true

	# Start in the middle of the entry space and flood.
	var entry_id: String = plate["entry"]
	var start := Vector2i(-1, -1)
	for space in enclosed:
		if space["id"] == entry_id:
			var r: Array = space["rect"]
			start = Vector2i(r[0] + r[2] / 2, r[1] + r[3] / 2)
	if start.x < 0:
		printerr("entry space '" + entry_id + "' is not on the plate")
		quit(2); return

	var seen := {}
	var queue: Array[Vector2i] = [start]
	seen[start] = true
	var crossed_desk := []
	while not queue.is_empty():
		var cell: Vector2i = queue.pop_front()
		for step in [Vector2i(1, 0), Vector2i(-1, 0), Vector2i(0, 1), Vector2i(0, -1)]:
			var next: Vector2i = cell + step
			if next.x < 0 or next.y < 0 or next.x >= w or next.y >= h: continue
			if seen.has(next): continue
			if not walkable.has(next): continue
			if blocked.has(next):
				crossed_desk.append([next.x, next.y])
				continue
			seen[next] = true
			queue.append(next)

	# Every enclosed space must have been entered, not merely passed.
	var unreachable := []
	for space in enclosed:
		var r: Array = space["rect"]
		var found := false
		for y in range(r[1] + 1, r[1] + r[3] - 1):
			for x in range(r[0] + 1, r[0] + r[2] - 1):
				if seen.has(Vector2i(x, y)): found = true; break
			if found: break
		if not found:
			unreachable.append(space["id"])

	var ok: bool = unreachable.is_empty() and crossed_desk.is_empty()
	print(JSON.stringify({
		"ok": ok,
		"entry": entry_id,
		"spaces_checked": enclosed.size(),
		"cells_reached": seen.size(),
		"unreachable": unreachable,
		"desk_cells_crossed": crossed_desk.size(),
		"godot": Engine.get_version_info().string,
	}))
	quit(0 if ok else 1)
