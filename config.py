import os
import re
import socket
import subprocess
from libqtile import qtile
from libqtile.config import Click, Drag, Group, KeyChord, Key, Match, Screen
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from typing import List  # noqa: F401

mod = "mod4"
terminal = guess_terminal()

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "Left", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "Right", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "Down", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "Up", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "Left", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "Right", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "Down", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "Up", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "Left", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "Right", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "Down", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "Up", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    Key([mod], "m",lazy.spawn('amixer -c1 sset "Auto-Mute Mode" Enabled')),
    Key([mod], "b",lazy.spawn('chromium')),
    Key([], "XF86AudioMute", lazy.spawn("amixer -c1 sset 'Master' toggle")),
    Key([], "XF86AudioLowerVolume", lazy.spawn("amixer -c1 sset 'Master' 5%-")),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("amixer -c1 sset 'Master' 5%+")),
    Key([], "XF86MonBrightnessUp", lazy.spawn("light -A 10")),
    Key([], "XF86MonBrightnessDown", lazy.spawn("light -U 10")),
     Key([], "Print", lazy.spawn("flameshot gui")),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawn('dmenu_run')),
    Key([mod], "e", lazy.spawn('emote')),
    Key([mod,"control"], "z", lazy.spawn('zotero')),
    Key([mod, "control"], "n", lazy.spawn('notion-app')),
    Key([mod, "control"], "m", lazy.spawn('mendeley-reference-manager')),
    Key([mod, "control"], "r", lazy.spawn('qtile cmd-obj -o cmd -f reload_config')),
    Key([mod, "control"], "o", lazy.spawn('obsidian')),
]

groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod1 + shift + letter of group = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )
colors = {
            "flamingo": "#F3CDCD",
            "mauve": "#DDB6F2",
            "pink": "#f5c2e7",
            "maroon": "#DE3163",
            "red": "#fd3333",
            "orange": "#FF7F00",
            "peach": "#FFBF00",
            "yellow": "#f6e653",
            "green": "#90EE90",
            "teal": "#40E0D0", 
            "blue": "#0000FF",
            "sky": "#89dceb",
            "white": "#d9e0ee",
            "gray": "#6e6c7e",
            "black": "#000000",
          }

layouts = [
    layout.Columns(margin=8,border_focus_stack=["#d75f5f", "#8f3d3d"], border_width=3),
    layout.Max(),
]

widget_defaults = dict(
    font="MesloLGSDZ Nerd Font Mono style = Bold",
    fontsize=17,
    padding=3,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        bottom=bar.Bar(
            [ 
                widget.TextBox(
                                text="🚀",
                                padding=0,
                                fontsize=35,
                                foreground = colors["gray"]
                                ),
                widget.GroupBox(
                                
                                highlight_method = "line",
                                block_highlight_text_color = colors["black"],
                                borderwidth = 4,
                                active = colors["gray"],
                                inactive = colors["black"],
                                this_current_screen_border = colors["gray"],
                                highlight_color = colors["white"],
                            ),
                widget.TextBox(
                                text="|",
                                padding=0,
                                fontsize=35,
                                foreground = colors["gray"]                             ),
                widget.WindowName(
                                fontsize = 13,
                                foreground = colors["white"],
                            ),
                widget.Systray(),
                widget.Battery(
                                format = "{char}{percent:2.0%}",
                                foreground = colors["white"],
                                charge_char = "🔋",
                                full_char = "🔋",
                                discharge_char = "🔋",
                                unknown_char = "🔋",
                                empty_char = "🪫",
                                low_foreground = colors["red"],
                                low_percentage = 0.25,
                                update_interval=30,
                              ),
                widget.Volume(
                                fmt = " 📢{}",
                                foreground = colors["white"],
                                update_interval = 0, 
                                #get_volume_command = "amixer sget Master | grep 'Right:' | awk -F'[][]' '{ print $2 }",
                            ),
               widget.Memory (
                                format = " 💾{MemUsed:.0f}{mm}/{MemTotal:.0f}{mm}",
                                foreground = colors["white"],
                                #foreground = "#A020F0",
                              ),
                widget.Net(
                                format=" 🔺{up}🔻{down}",
                                foreground = colors["white"],
                                ),

                widget.Clock(
                                format = " 📅%a,%d %b %y",
                                foreground = colors["white"],
                                 ),
                widget.Clock(
                                format = " ⏳%H:%M",
                                foreground = colors["white"],
                                 ),
                widget.CurrentLayoutIcon(
                                scale = 0.8,
                               ),
            ],
            30,
            background = "#242222",
            ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "Qtile"
