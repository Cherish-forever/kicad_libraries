# kicad_libraries
Kicad libraries management tool

# Prepare
`$ pip3 install west`


# Download
`$ west init -m https://github.com/Cherish-forever/kicad_libraries.git && west update`

# Generate table

## Keep kicad-offical footprint and symbol compatible with kicad default libraries config(Recommend)

### footprint
`$ west footprint -o ~/.config/kicad/7.0/fp-lib-table -k True`

### symbols
`$ west symbol -o ~/.config/kicad/7.0/sym-lib-table -k True`

## kicad-offical footprint and symbol be same with other repository(No Recommend)

### footprint
`$ west footprint -o ~/.config/kicad/7.0/fp-lib-table`

### symbols
`$ west symbol -o ~/.config/kicad/7.0/sym-lib-table`

# 3D model binding

## command

`$ python3 .kicad_libraries/scripts/model3d.py <footprint_path> <3d_model_path> <model extension>`

eg:

footprint path is Cylindric3D, 3d model path is Cylindric3D, the 3d model extension is ".wrl"

`$ python3 .kicad_libraries/scripts/model3d.py Cylindric3D Cylindric3D ".wrl"`

## batch process 3d model

`$ ls | xargs -n 1 -I {} python3 .kicad_libraries/scripts/model3d.py {} {} ".wrl"`

## batch process 3d model except kicad directory

`$ ls -d */ | grep -Ev '^kicad/$' | sed 's#/$##' | xargs -n 1 -I {} python3 .kicad_libraries/scripts/model3d.py {} {} ".wrl"`

## batch process 3d model recovery

`$ west forall -c "git reset --hard HEAD"`

## signle repository recovery

`$ cd <path_have_git> && git reset --hard HEAD`

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
