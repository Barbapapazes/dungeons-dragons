# Map editor

This map editor is used to create or edit a map for the game. It uses a GUI to facilitate the process of map creation. This tool is not inside the game which is different process. But we recommended to close the game when update a map for a better experience.

## Start the map

```sh
# start the map editor
$ pipenv run map_editor
```

Please refer to [config](/config.html) for more informations.

## Shortcuts

- **CTRL + K**: show all shortcuts

### In the tileset

- **Left Click**: select a tile
- **ZQSD or Scroll Wheel**: move the tileset

### In the map

- **IJKL**: move the map in the viewport
- **Number**: select a layer
- **Left Click**: add a tile to the selected layer, drag to add many tiles
- **Right Click**: remove a tile from the selected layer, drag to remove many tiles
- **ALT + Left Click** (drag to draw): create a wall
- **ALT + Right Click** (inside a rect): remove a wall or a player
- **CTRL + R**: remove the selected tile
- **CTRL + S**: save the map

### Tools

- **Paint Pot** (red square): select a layer, a tile and then click on the paint pot
- **Rubber** (yellow square): remove all tile from the selected layer
- **Player** (green square): create a player object

## About Tiled

Because our game support the standard `.tmx` files for saving map data, you can use [Tiled](https://www.mapeditor.org/) for a better experience.
