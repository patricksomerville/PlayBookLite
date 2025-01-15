"""ASCII art for key Moby Dick moments"""

TITLE = '''
╔════════════════════════════════════════╗
║             P L A Y B O O K            ║
║                                        ║
║          M O B Y   D I C K            ║
║        An Interactive Journey          ║
║                                        ║
║    Based on the novel by H. Melville   ║
╚════════════════════════════════════════╝
'''

WHALE_BREACH = '''
                       _.--._
                    .'       '.
                   /           \\
                  /             \\
                 |               |
                 |               |
                  \    \___/    /
                   \    ___    /
                    \  (   )  /
                     '.___.'
                       |_|
'''

PEQUOD = '''
                    |    |    |
                   )_)  )_)  )_)
                  )___))___))___)\\
                 )____)____)_____)\\\\
               _____|____|____|____\\\\\\__
      ---------\                   /---------
        ^^^^^ ^^^^^^^^^^^^^^^^^^^^^
          ^^^^      ^^^^     ^^^    ^^
               ^^^^      ^^^
'''

HARPOON = '''
      />
 -----0====>
      \\>
'''

COFFIN_BUOY = '''
     ______________
    |\ ___________ /|
    | |  R I P   | |
    | |         | |
    | |         | |
    | |         | |
    | |         | |
    | |_________| |
    |/___________|\\|
'''

LIGHTHOUSE = '''
    _____
   [     ]
   |     |
   |     |
   |  |  |
  /|  |  |\\
 //|  |  |\\\\
'''

def get_art(key: str) -> str:
    """Get ASCII art for a specific scene or object"""
    art = {
        "title": TITLE,
        "whale_breach": WHALE_BREACH,
        "pequod": PEQUOD,
        "harpoon": HARPOON,
        "coffin_buoy": COFFIN_BUOY,
        "lighthouse": LIGHTHOUSE
    }
    return art.get(key, "")
