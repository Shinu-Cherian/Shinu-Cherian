from scripts.profile_builder import Profile
from scripts.render.theme import Theme
from scripts.render.core import SectionResult, Element

def render(profile: Profile, theme: Theme) -> SectionResult:
    ascii_lines = [
        r"WWWWWW&WM?                       =SMMMMM###",
        r"&&&&&WM?*. :,.                    .MWMWMMMM",
        r"&&888&?+, .:                       .=*SWWMM",
        r"8888&&?:                              :+MWM",
        r"8BBB8#?;     ,~%S%%SS?+.              .#WWW",
        r"BB$W=  ,   *B$$$$$$$$W?+?+             M&WW",
        r"$$$?      ?$$$$$$$&MS?%#S*;,:;.       :8&&&",
        r"$$$$,    .B$$$$$$$$$$$$88MS%*+~       ?8&&&",
        r"$$$$8    ?$$$$$$$$B$$$$8#?~=;:=~      8888&",
        r"$$$$$B   ~;:.     .?S:.              S$8888",
        r"$$$$$$*             ~                W$8888",
        r"$$$$$B#*.:.        B$#           :; ,,$BB88",
        r"$$$$$BM8**M#?=... %$$W=         :+= .~$BB88",
        r"$$$$$$$S?888&S*+~%$$$8+=: ,::;;=~*  .&$BBB8",
        r"$$$$$$$$+S$$$$$8B$S+~,  .,=??+~=:  =M$$$BBB",
        r"$$$$$$$$W *&$$$$W~          =~;   W$$$B$$BB",
        r"$$$$$$$$$W:~%$M    ==~,      ,     =M$$$B$B",
        r"$$$$$$$$$~ ..=%,;S8BM%?~;.            ?$$$B",
        r"$$$$$$$*    ~..=SWS;                    *B$",
        r"$$$$$M       =   ;~~,:,                   +",
        r"$$$B:                                      ",
        r"$$*                                        ",
        r"S                                          ",
        r"S                                          ",
        r"S                                          ",
        r"S                                          ",
        r"?                                          ",
        r"+"                                          "
    ]
    
    char_width = theme.get_char_width()
    max_chars = max(len(line) for line in ascii_lines)
    section_width = max_chars * char_width
    
    elements = []
    current_y = 0
    for line in ascii_lines:
        elements.append(Element(x=0, y=current_y, raw_text=line, css_class="text ascii"))
        current_y += theme.line_height
        
    return SectionResult(width=section_width, height=current_y, elements=elements)
