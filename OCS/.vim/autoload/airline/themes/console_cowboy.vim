let g:airline#themes#console_cowboy#palette = {}

let s:N1   = [ '' , '' , 8  , 7 ]
let s:I1 = [ '' , '' , s:N1[2]  , 11  ]
let s:V1 = [ '' , '' , s:N1[2] , s:I1[3] ]
let s:IA1 = [ '' , '' , 0 , 0 , '' ]

let s:N2   = [ s:N1[1] , s:N1[1] , s:N1[3] , s:N1[3] ]
let s:I2 = [ s:I1[1] , s:I1[1] , s:I1[3] , s:I1[3]  ]
let s:V2 = [ s:V1[1] , s:V1[1] , s:V1[3] , s:V1[3] ]
let s:IA2 = [ s:IA1[0] , s:IA1[1] , s:IA1[2] , s:IA1[3] , '' ]
let s:N3   = [ s:N1[0] , s:N1[1] , s:N1[2]  , s:N1[3] ]
let s:I3 = [ s:I1[0] , s:I1[1] , s:I1[2]  , s:I1[3]  ]
let s:V3 = [ s:V1[0] , s:V1[1] , s:V1[2]  , s:V1[3]  ]
let s:IA3 = [ s:IA1[0] , s:IA1[1] , s:IA1[2] , s:IA1[3] , '' ]
let g:airline#themes#console_cowboy#palette.normal = airline#themes#generate_color_map(s:N1, s:N2, s:N3)
let g:airline#themes#console_cowboy#palette.normal_modified = { 'airline_c': [ s:N1[0] , s:N1[1] , s:N1[2]     , s:N1[3]      , ''     ] , }
let g:airline#themes#console_cowboy#palette.insert = airline#themes#generate_color_map(s:I1, s:I2, s:I3)
let g:airline#themes#console_cowboy#palette.visual = airline#themes#generate_color_map(s:V1, s:V2, s:V3)
let g:airline#themes#console_cowboy#palette.inactive = airline#themes#generate_color_map(s:IA1, s:IA2, s:IA3)
let g:airline#themes#console_cowboy#palette.insert_modified = { 'airline_c': [ s:I1[0] , s:I1[1] , s:I1[2]     , s:I1[3]      , ''     ] , }
let g:airline#themes#console_cowboy#palette.visual_modified = { 'airline_c': [ s:V1[0] , s:V1[1] , s:V1[2]     , s:V1[3]      , ''     ] , }
let g:airline#themes#console_cowboy#palette.inactive_modified = { 'airline_c': [ s:IA1[0] , s:IA1[1] , s:IA1[2] , s:IA1[3] , '' ] , }
let g:airline#themes#console_cowboy#palette.insert_paste = { 'airline_a': [ s:I1[0]   , s:I1[1] , s:I1[2] , s:I1[3]     , ''     ] , }
let g:airline#themes#console_cowboy#palette.replace = copy(g:airline#themes#console_cowboy#palette.insert)
let g:airline#themes#console_cowboy#palette.replace.airline_a = [ s:I1[0]   , s:I1[1] , s:I1[2] , s:I1[3]     , ''     ]
let g:airline#themes#console_cowboy#palette.replace_modified = g:airline#themes#console_cowboy#palette.insert_modified

let g:airline#themes#console_cowboy#palette.accents = { 'red': [ '' , '' , 1 , ''  ] }
if !get(g:, 'loaded_ctrlp', 0)
  finish
endif
let g:airline#themes#console_cowboy#palette.ctrlp = airline#extensions#ctrlp#generate_color_map(
      \ [ '#d7d7ff' , '#5f00af' , 189 , 55  , ''     ],
      \ [ '#ffffff' , '#875fd7' , 231 , 98  , ''     ],
      \ [ '#5f00af' , '#ffffff' , 55  , 231 , 'bold' ])
