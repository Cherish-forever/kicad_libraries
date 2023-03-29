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

# Update repository

update all repository

`$ west update`

update and rebase all repository

`$ west update --rebase`

only update kicad/symbols

`$ west update kicad/symbols`

only update kicad/symbols and rebase

`$ west update kicad/symbols --rebase`

# How update kicad enverioment
exp:

```$ west env -c ~/.config/kicad/7.0/kicad_common.json -e "KICAD7_3DMODULE_DIR:`west topdir`/kicad/packages3D" "KICAD7_FOOTPRINT_DIR:`west topdir`/kicad/footprints" "KICAD7_SYMBOL_DIR:`west topdir`/kicad/symbols" "KICAD_USER_TEMPLATE_DIR:`west topdir`/kicad/templates"```

`-c:` /path/to/kicad_common.json

`-e:` "the enverioment you want set"

# part or full repositories import

## part

```manifest:
  defaults:
    remote: origin

  remotes:
    - name: origin
      url-base: https://github.com

  self:
    path: .kicad_libraries
    west-commands: scripts/west-commands.yml
    import:
      - submanifests/kicad-official.yml
```

## full

```manifest:
  defaults:
    remote: origin

  remotes:
    - name: origin
      url-base: https://github.com

  self:
    path: .kicad_libraries
    west-commands: scripts/west-commands.yml
    import: submanifests
```
