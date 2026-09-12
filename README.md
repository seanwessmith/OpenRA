# Radar map-edge visibility comparison

Native OpenRA screenshots for OpenRA/OpenRA#22589, captured 2026-09-12.
Baseline: `f3ec7f8e1593b482f85fd101652deb740c33dee6` (bleed).
Patch: `2312e064113463d9c624d875c95d4f462ebe8cdb` — initialize the radar shroud texture to opaque `ColorShroud` before the existing projected-cell updates.

The screenshots are unedited JPEGs returned by the desktop capture tool, approximately 1224x768. They are native game captures, not generated images or a simulated renderer. Comparisons use the same map, locked spawn/faction, default camera, and graphics settings; elapsed game time, animation and resource randomness are not frame-synchronized. Review radar coverage, not unrelated animation pixels.

## Tiberian Sun: Sunstroke

This fixture preplaces a normal GDI radar and three power plants for Multi0, with the normal power-dependent `ProvidesRadar` condition. The screenshot shows 250 surplus power. The radar is not granted directly to the player in this fixture. Buildings were preplaced, not constructed through the UI.

Before any visibility command, baseline exposes terrain bands at the top and bottom of the radar; the patch covers these outside-map pixels. The same result holds after toggling `/visibility` on and off. `/clear-shroud` gives the explored-with-fog comparison.

| State | Baseline | Patched |
|---|---|---|
| Radar, never used visibility cheat | [before](ts-building-before-unexplored.jpg) | [after](ts-building-after-unexplored.jpg) |
| Visibility cheat enabled | [before](ts-building-before-visibility.jpg) | [after](ts-building-after-visibility.jpg) |
| Visibility cheat disabled again | [before](ts-building-before-cheat-off.jpg) | [after](ts-building-after-cheat-off.jpg) |
| Explored, fog enabled | [before](ts-building-before-explored.jpg) | [after](ts-building-after-explored.jpg) |

## Rectangular-map comparisons

These fixtures grant `ProvidesRadar` directly to the player to isolate the real radar renderer from construction. No visible regression in the selected radar scenes. These are scoped smoke tests, not exhaustive gameplay validation.

| Mod / map | Unexplored | Visibility on | Explored with fog |
|---|---|---|---|
| Red Alert / A Path Beyond | [before](ra-before-unexplored.jpg), [after](ra-after-unexplored.jpg) | [before](ra-before-visibility.jpg), [after](ra-after-visibility.jpg) | [before](ra-before-explored.jpg), [after](ra-after-explored.jpg) |
| Dune 2000 / Pasty Mesa | [before](d2k-before-unexplored.jpg), [after](d2k-after-unexplored.jpg) | [before](d2k-before-visibility.jpg), [after](d2k-after-visibility.jpg) | [before](d2k-before-explored.jpg), [after](d2k-after-explored.jpg) |
| Tiberian Dawn / African Gambit | [before](cnc-before-unexplored.jpg), [after](cnc-after-unexplored.jpg) | [before](cnc-before-visibility.jpg), [after](cnc-after-visibility.jpg) | [before](cnc-before-explored.jpg), [after](cnc-after-explored.jpg) |

## Reproduce

Build OpenRA normally. Install the mod content listed by its installer into a dedicated support directory. The asset packs used here matched the SHA1 values in the checkout's installer definitions. Run `python3 reproduce.py CHECKOUT SUPPORT_DIR` to create the map fixtures from the checkout's original map data and the supplied map YAML files.

Launch from the checkout, replacing the absolute support path and choosing `Game.Mod=ts Launch.Map=radar-building`, `Game.Mod=ra Launch.Map=radar-ra`, `Game.Mod=d2k Launch.Map=radar-d2k`, or `Game.Mod=cnc Launch.Map=radar-cnc`:

```
./launch-game.sh Game.Mod=ts Launch.Map=radar-building Engine.SupportDir=/absolute/support/path Graphics.Mode=PseudoFullscreen Game.ViewportEdgeScroll=false Debug.SendSystemInformation=false
```

Capture the initial radar; enter `/visibility` in chat and capture; repeat `/visibility` and capture; enter `/clear-shroud` and capture the explored/fog state. Repeat with baseline and patched builds. The fixture enables developer commands but does not start with visibility checks disabled. Original terrain, heights and map bounds are retained.

## Environment and limitations

- macOS 27.0, Apple M4 (arm64), SDL 2.32.10, OpenGL 4.1 Metal - 91.7, Modern renderer, display 1710x1107, effective game resolution reported 1710x1073, window scale 2, UI scale 1.
- .NET SDK 10.0.401, runtime 10.0.12. The repository's native apphost was compiled into a local app bundle to let the desktop capture tool find the game window.
- Native mouse control failed in the desktop tool; map launch arguments and keyboard chat commands were used. No manual construction, minimap clicking, multiplayer, Windows or Linux UI validation is claimed.
- The change does not alter projection geometry or minimap input mapping. Existing map-bound sizing TODOs remain outside its scope.
- AI disclosure: Codex generated the patch and fixtures, operated the native game and inspected these captures. No independent human playtest is claimed.

## Checks

`make` passed on baseline and patch. `make test` and `make check` passed on the patch with no reported errors. Baseline and patched `dotnet test .../OpenRA.Test.dll --test-adapter-path:.` each passed 508 tests with the same two skipped PNG tests. `git diff --check` passed.
