set nocompatible              " be iMproved, required
filetype off                  " required

" ================ Vundle ====================
set rtp+=~/.vim/bundle/Vundle.vim
call vundle#begin()
Plugin 'VundleVim/Vundle.vim'
Plugin 'scrooloose/nerdtree'
Plugin 'jistr/vim-nerdtree-tabs'
Plugin 'vim-airline/vim-airline'
Plugin 'lornix/vim-scrollbar'
call vundle#end()
filetype plugin indent on


" ================ General Config ====================
colorscheme console-cowboy
set clipboard+=unnamedplus
set number
set backspace=indent,eol,start
set history=1000
set showcmd
set noshowmode
set visualbell
set hidden
syntax on
set scrolloff=5
set sidescrolloff=5
set sidescroll=1
set ignorecase
set smartcase
set hlsearch
set incsearch
set nowrap
set linebreak
nmap j gj
nmap k gk
set laststatus=2
set cursorline
" set autoread
autocmd VimResized * wincmd =
noremap <silent> <C-S>          :update<CR>
vnoremap <silent> <C-S>         <C-C>:update<CR>
inoremap <silent> <C-S>         <C-O>:update<CR>

" ================ Persistent Undo ==================
if has('persistent_undo')
  silent !mkdir ~/.vim/backups > /dev/null 2>&1
  set undodir=~/.vim/backups
  set undofile
endif


" ================ Indentation ======================
set autoindent
set smartindent
set smarttab
set shiftwidth=2
set softtabstop=2
set tabstop=2
set expandtab
nnoremap p p=`]<C-o>
nnoremap P P=`]<C-o>

" ================ Turn Off Swap Files ==============
set noswapfile
set nobackup
set nowb

" ================ Tabs ====================
nnoremap <C-t>     :tabnew<CR>
nnoremap <C-w>     :tabclose<CR>
nnoremap <C-Tab>   :tabnext<CR>
nnoremap <C-S-Tab> :tabprevious<CR>
inoremap <C-t>     <Esc>:tabnew<CR>
inoremap <C-w>     <Esc>:tabclose<CR>
inoremap <C-Tab>   <Esc>:tabnext<CR>i
inoremap <C-S-Tab> <Esc>:tabprevious<CR>i

" ================ scrollbar ====================
let g:scrollbar_thumb='-'
let g:scrollbar_clear='|'

" ================ airline ====================
let g:airline_left_sep=''
let g:airline_right_sep=''
let g:airline_theme='console_cowboy'
autocmd vimenter * AirlineRefresh

" ================ NERDTree ====================
autocmd vimenter * NERDTree
let g:nerdtree_tabs_open_on_console_startup=1
map <Tab> :wincmd w<CR>
map <C-n> :NERDTreeTabsToggle<CR>
" set autochdir
let NERDTreeAutoDeleteBuffer = 1
let NERDTreeMinimalUI = 1
let NERDTreeChDirMode=2
autocmd bufenter * if (winnr("$") == 1 && exists("b:NERDTree") && b:NERDTree.isTabTree()) | q | endif
autocmd VimEnter * wincmd p
autocmd StdinReadPre * let s:std_in=1
autocmd VimEnter * if argc() == 0 && !exists("s:std_in") | wincmd p | endif

