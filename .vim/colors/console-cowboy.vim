hi clear
set background=dark
if exists("syntax_on")
  syntax reset
endif
let g:colors_name = "console-cowboy"
hi SpecialKey	  cterm=bold  ctermfg=darkred
hi NonText		  cterm=bold  ctermfg=darkred
hi Directory	  ctermfg=cyan
hi ErrorMsg		  ctermfg=black ctermbg=red
hi Search		  ctermfg=black  ctermbg=darkyellow
hi MoreMsg		  cterm=bold  ctermfg=darkgreen
hi ModeMsg		  cterm=bold
hi LineNr		  ctermfg=green	ctermbg=black
hi CursorLineNr	  ctermfg=green	ctermbg=black
hi Question		  cterm=bold  ctermfg=darkgreen
hi WildMenu       ctermfg=black ctermbg=blue cterm=none
hi StatusLine	  cterm=none ctermfg=black ctermbg=white
hi StatusLineNC   ctermfg=white ctermbg=lightblue
hi Title		  ctermfg=cyan
hi Visual		  cterm=reverse
hi WarningMsg	  cterm=none ctermfg=darkred
hi Comment		  cterm=none ctermfg=cyan 
hi Constant		  cterm=none ctermfg=blue
hi Special		  cterm=bold ctermfg=red
hi Identifier	  cterm=none ctermfg=red
hi Statement	  cterm=none ctermfg=yellow
hi PreProc		  ctermfg=yellow
hi Type			  cterm=none ctermfg=green
hi Error		  ctermfg=magenta  ctermbg=black
hi Todo			  ctermfg=black	ctermbg=darkcyan
hi CursorLine	  ctermbg=black cterm=none
hi CursorColumn	  cterm=none
hi MatchParen	  ctermfg=blue
hi TabLine		  cterm=none ctermfg=black ctermbg=white
hi TabLineFill	  cterm=none ctermfg=black ctermbg=black
hi TabLineSel	  ctermfg=black ctermbg=blue
hi Underlined	  cterm=bold,underline ctermfg=lightblue
hi Ignore		  ctermfg=black ctermbg=black
hi link IncSearch		Visual
hi link String			Constant
hi link Character		Constant
hi link Number			Constant
hi link Boolean			Constant
hi link Float			Number
hi link Function		Identifier
hi link Conditional		Statement
hi link Repeat			Statement
hi link Label			Statement
hi link Operator		Statement
hi link Keyword			Statement
hi link Exception		Statement
hi link Include			PreProc
hi link Define			PreProc
hi link Macro			PreProc
hi link PreCondit		PreProc
hi link StorageClass	Type
hi link Structure		Type
hi link Typedef			Type
hi link Tag				Special
hi link SpecialChar		Special
hi link Delimiter		Special
hi link SpecialComment	Special
hi link Debug			Special
