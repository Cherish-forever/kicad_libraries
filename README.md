# kicad_libraries
Kicad libraries management tool

# Prepare
`$ pip3 install west`


# Download
`$ west init -m https://github.com/Cherish-forever/kicad_libraries.git && west update`

# Generate footprint table
`$ west footprint -o ~/.config/kicad/7.0/fp-lib-table`

# Generate symbol table
`$ west symbol -o ~/.config/kicad/7.0/sym-lib-table`



# How to add repository

You can add yourself repository in west.yml, or create yml file in submanifests.
