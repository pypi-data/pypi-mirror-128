## Config File Location
Config files for RadiSpawn can be referenced in three ways:
- Absolute paths, then, in this order:
- Paths relative to the current working directory
- Paths relative to ~/.config/radispawn/

## Config File Format
The config files are JSON files:
- Main object
    - "wedges": list (Lists the wedges in the menu, starting from the top and going clockwise)
        - Object
            - "name": string (Label on the wedge)
            - "call": string (This is the executable that is run when a wedge is selected)
            - "color": list of integers (0-255 for red, green, and blue)
