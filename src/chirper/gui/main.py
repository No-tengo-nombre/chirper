import PySimpleGUI as sg

top_menu = [
    [
        "File",
        [
            "New",
            "Open",
            "Save",
            "Save As",
            "---",
            "Exit",
        ],
    ],
    [
        "Edit",
        [
            "Undo",
            "Redo",
        ]
    ],
    [
        "View",
        [
            "Zoom",
            "Fit",
        ]
    ],
    [
        "Help",
        [
            "About"
        ]
    ]
]


settings_column = [
    [
        sg.Text("asd"),
        sg.Text("asd"),
    ],
    [
        sg.Text("uwu"),
        sg.Text("uwu"),
    ]
]


screen_column = [
    [
        sg.Button("1"),
        sg.Button("2"),
    ],
    [
        sg.Button("3"),
    ],
    [
        sg.Button("4")
    ],
]


layout = [
    [
        sg.Menu(top_menu),
    ],
    [
        sg.Column(settings_column),
        sg.Column(screen_column),
    ]
]

# Create the window
window = sg.Window('Window Title', layout)

event, values = window.read()

# Finish up by removing from the screen
window.close()
