let SessionLoad = 1
if &cp | set nocp | endif
let s:cpo_save=&cpo
set cpo&vim
inoremap <F5> =strftime("=== %a %b %d, %Y ===")
map  :NERDTreeToggle
nmap <silent> ,w,m <Plug>VimwikiMakeTomorrowDiaryNote
nmap <silent> ,w,y <Plug>VimwikiMakeYesterdayDiaryNote
nmap <silent> ,w,t <Plug>VimwikiTabMakeDiaryNote
nmap <silent> ,w,w <Plug>VimwikiMakeDiaryNote
nmap <silent> ,w,i <Plug>VimwikiDiaryGenerateLinks
nmap <silent> ,wi <Plug>VimwikiDiaryIndex
nmap <silent> ,ws <Plug>VimwikiUISelect
nmap <silent> ,wt <Plug>VimwikiTabIndex
nmap <silent> ,ww <Plug>VimwikiIndex
nnoremap ,a :Ack! 
nnoremap ,' viwa'hbi'lel
nnoremap ," viwa"hbi"lel
nnoremap ,sv :source $MYVIMRC
nnoremap ,ev :vsplit $MYVIMRC
nnoremap H ^
nnoremap L $
nnoremap Q <Nop>
xmap S <Plug>VSurround
nmap cS <Plug>CSurround
nmap cs <Plug>Csurround
nmap ds <Plug>Dsurround
vmap gx <Plug>NetrwBrowseXVis
nmap gx <Plug>NetrwBrowseX
xmap gS <Plug>VgSurround
nnoremap q <Nop>
nmap ySS <Plug>YSsurround
nmap ySs <Plug>YSsurround
nmap yss <Plug>Yssurround
nmap yS <Plug>YSurround
nmap ys <Plug>Ysurround
vnoremap <silent> <Plug>NetrwBrowseXVis :call netrw#BrowseXVis()
nnoremap <silent> <Plug>NetrwBrowseX :call netrw#BrowseX(expand((exists("g:netrw_gx")? g:netrw_gx : '<cfile>')),netrw#CheckIfRemote())
nnoremap <silent> <Plug>SurroundRepeat .
nnoremap <F5> "=strftime("=== %a %b %d, %Y ===")P
noremap <F11> :Invbg
nnoremap <F2> :set invpaste paste?
imap S <Plug>ISurround
imap s <Plug>Isurround
imap  <Plug>Isurround
inoremap jk 
let &cpo=s:cpo_save
unlet s:cpo_save
set paste
set background=dark
set backspace=indent,eol,start
set expandtab
set fileencodings=ucs-bom,utf-8,default,latin1
set grepprg=grep\ -nH\ $*
set helplang=en
set incsearch
set laststatus=2
set pastetoggle=<F2>
set printoptions=paper:letter
set runtimepath=~/.vim,~/.vim/bundle/Vim-Jinja2-Syntax,~/.vim/bundle/ansible-vim,~/.vim/bundle/black,~/.vim/bundle/cvim,~/.vim/bundle/nerdtree,~/.vim/bundle/python-mode,~/.vim/bundle/syntastic,~/.vim/bundle/vim-airline,~/.vim/bundle/vim-colors-solarized,~/.vim/bundle/vim-indent-object,~/.vim/bundle/vim-json,~/.vim/bundle/vim-surround,~/.vim/bundle/vim-terraform,~/.vim/bundle/vim-yaml,~/.vim/bundle/vimwiki,/var/lib/vim/addons,/usr/share/vim/vimfiles,/usr/share/vim/vim80,/usr/share/vim/vimfiles/after,/var/lib/vim/addons/after,~/.vim/bundle/vim-yaml/after,~/.vim/bundle/python-mode/after,~/.vim/after
set shell=zsh
set shellpipe=>%s\ 2>&1
set shiftround
set shiftwidth=4
set showcmd
set smartcase
set smartindent
set splitbelow
set splitright
set suffixes=.bak,~,.swp,.o,.info,.aux,.log,.dvi,.bbl,.blg,.brf,.cb,.ind,.idx,.ilg,.inx,.out,.toc
set tabstop=4
set undofile
set visualbell
set wildignore=*.pyc
set wildmenu
set wildmode=longest:full,full
let s:so_save = &so | let s:siso_save = &siso | set so=0 siso=0
let v:this_session=expand("<sfile>:p")
silent only
cd ~/cloud/ansible-infinidat-collection
if expand('%') == '' && !&modified && line('$') <= 1 && getline(1) == ''
  let s:wipebuf = bufnr('%')
endif
set shortmess=aoO
badd +1 Makefile
badd +89 playbooks/test_create_snapshots.yml
badd +65 Makefile-help
badd +9 playbooks/test_remove_snapshots.yml
badd +1 tests/sanity/ignore-2.10.txt
badd +1 .
badd +342 playbooks/test_create_resources.yml
badd +21 playbooks/test_remove_resources.yml
badd +591 plugins/modules/infini_map.py
badd +41 playbooks/test_create_map_cluster.yml
badd +7 playbooks/test_remove_map_cluster.yml
badd +210 plugins/module_utils/infinibox.py
badd +1 README.md
badd +13 galaxy.yml
badd +1 docs/DEV_README.md
badd +1 requirements.txt
badd +7 .gitlab-ci.yml
argglobal
silent! argdel *
$argadd Makefile
$argadd playbooks/test_create_snapshots.yml
set stal=2
edit Makefile
set splitbelow splitright
wincmd t
set winminheight=1 winheight=1 winminwidth=1 winwidth=1
argglobal
let s:cpo_save=&cpo
set cpo&vim
imap <buffer> <silent> <C-F9> :call C_Make()
map <buffer> <silent> \rma :call C_MakeArguments()
map <buffer> <silent> \rme :call C_MakeExeToRun()
map <buffer> <silent> \rmc :call C_MakeClean()
map <buffer> <silent> \rcm :call C_ChooseMakefile()
map <buffer> <silent> \rm :call C_Make()
map <buffer> <silent> <C-F9> :call C_Make()
imap <buffer> <silent> \rma :call C_MakeArguments()
imap <buffer> <silent> \rme :call C_MakeExeToRun()
imap <buffer> <silent> \rmc :call C_MakeClean()
imap <buffer> <silent> \rcm :call C_ChooseMakefile()
imap <buffer> <silent> \rm :call C_Make()
let &cpo=s:cpo_save
unlet s:cpo_save
setlocal keymap=
setlocal noarabic
setlocal noautoindent
setlocal backupcopy=
setlocal balloonexpr=
setlocal nobinary
setlocal nobreakindent
setlocal breakindentopt=
setlocal bufhidden=
setlocal buflisted
setlocal buftype=
setlocal nocindent
setlocal cinkeys=0{,0},0),:,0#,!^F,o,O,e
setlocal cinoptions=
setlocal cinwords=if,else,while,do,for,switch
setlocal colorcolumn=
setlocal comments=sO:#\ -,mO:#\ \ ,b:#
setlocal commentstring=#\ %s
setlocal complete=.,w,b,u,t,i
setlocal concealcursor=
setlocal conceallevel=0
setlocal completefunc=
setlocal nocopyindent
setlocal cryptmethod=
setlocal nocursorbind
setlocal nocursorcolumn
setlocal nocursorline
setlocal define=
setlocal dictionary=
setlocal nodiff
setlocal equalprg=
setlocal errorformat=
setlocal noexpandtab
if &filetype != 'make'
setlocal filetype=make
endif
setlocal fixendofline
set foldcolumn=5
setlocal foldcolumn=5
setlocal foldenable
setlocal foldexpr=0
setlocal foldignore=#
setlocal foldlevel=0
setlocal foldmarker={{{,}}}
set foldmethod=syntax
setlocal foldmethod=syntax
setlocal foldminlines=1
setlocal foldnestmax=20
setlocal foldtext=foldtext()
setlocal formatexpr=
setlocal formatoptions=croql
setlocal formatlistpat=^\\s*\\d\\+[\\]:.)}\\t\ ]\\s*
setlocal formatprg=
setlocal grepprg=
setlocal iminsert=0
setlocal imsearch=-1
setlocal include=^\\s*include
setlocal includeexpr=
setlocal indentexpr=GetMakeIndent()
setlocal indentkeys=!^F,o,O,<:>,=else,=endif
setlocal noinfercase
setlocal iskeyword=@,48-57,_,192-255
setlocal keywordprg=
setlocal nolinebreak
setlocal nolisp
setlocal lispwords=
setlocal nolist
setlocal makeencoding=
setlocal makeprg=
setlocal matchpairs=(:),{:},[:]
setlocal modeline
setlocal modifiable
setlocal nrformats=bin,octal,hex
set number
setlocal number
setlocal numberwidth=4
setlocal omnifunc=
setlocal path=
setlocal nopreserveindent
setlocal nopreviewwindow
setlocal quoteescape=\\
setlocal noreadonly
setlocal norelativenumber
setlocal norightleft
setlocal rightleftcmd=search
setlocal noscrollbind
setlocal shiftwidth=4
setlocal noshortname
setlocal signcolumn=auto
setlocal nosmartindent
setlocal softtabstop=0
setlocal nospell
setlocal spellcapcheck=[.?!]\\_[\\])'\"\	\ ]\\+
setlocal spellfile=
setlocal spelllang=en
setlocal statusline=%!airline#statusline(1)
setlocal suffixesadd=
setlocal swapfile
setlocal synmaxcol=3000
if &syntax != 'make'
setlocal syntax=make
endif
setlocal tabstop=4
setlocal tagcase=
setlocal tags=
setlocal termkey=
setlocal termsize=
setlocal textwidth=0
setlocal thesaurus=
setlocal undofile
setlocal undolevels=-123456
setlocal nowinfixheight
setlocal nowinfixwidth
setlocal wrap
setlocal wrapmargin=0
let s:l = 178 - ((34 * winheight(0) + 17) / 35)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
178
normal! 0
tabedit README.md
set splitbelow splitright
wincmd t
set winminheight=1 winheight=1 winminwidth=1 winwidth=1
argglobal
if bufexists('README.md') | buffer README.md | else | edit README.md | endif
setlocal keymap=
setlocal noarabic
setlocal noautoindent
setlocal backupcopy=
setlocal balloonexpr=
setlocal nobinary
setlocal nobreakindent
setlocal breakindentopt=
setlocal bufhidden=
setlocal buflisted
setlocal buftype=
setlocal nocindent
setlocal cinkeys=0{,0},0),:,0#,!^F,o,O,e
setlocal cinoptions=
setlocal cinwords=if,else,while,do,for,switch
setlocal colorcolumn=
setlocal comments=fb:*,fb:-,fb:+,n:>
setlocal commentstring=>\ %s
setlocal complete=.,w,b,u,t,i
setlocal concealcursor=
setlocal conceallevel=0
setlocal completefunc=
setlocal nocopyindent
setlocal cryptmethod=
setlocal nocursorbind
setlocal nocursorcolumn
setlocal nocursorline
setlocal define=
setlocal dictionary=
setlocal nodiff
setlocal equalprg=
setlocal errorformat=
setlocal expandtab
if &filetype != 'markdown'
setlocal filetype=markdown
endif
setlocal fixendofline
set foldcolumn=5
setlocal foldcolumn=5
setlocal foldenable
setlocal foldexpr=0
setlocal foldignore=#
setlocal foldlevel=0
setlocal foldmarker={{{,}}}
set foldmethod=syntax
setlocal foldmethod=syntax
setlocal foldminlines=1
setlocal foldnestmax=20
setlocal foldtext=foldtext()
setlocal formatexpr=
setlocal formatoptions=tcqln
setlocal formatlistpat=^\\s*\\d\\+\\.\\s\\+\\|^[-*+]\\s\\+\\|^\\[^\\ze[^\\]]\\+\\]:
setlocal formatprg=
setlocal grepprg=
setlocal iminsert=0
setlocal imsearch=-1
setlocal include=
setlocal includeexpr=
setlocal indentexpr=
setlocal indentkeys=0{,0},:,0#,!^F,o,O,e
setlocal noinfercase
setlocal iskeyword=@,48-57,_,192-255
setlocal keywordprg=
setlocal nolinebreak
setlocal nolisp
setlocal lispwords=
setlocal nolist
setlocal makeencoding=
setlocal makeprg=
setlocal matchpairs=(:),{:},[:],<:>
setlocal modeline
setlocal modifiable
setlocal nrformats=bin,octal,hex
set number
setlocal number
setlocal numberwidth=4
setlocal omnifunc=htmlcomplete#CompleteTags
setlocal path=
setlocal nopreserveindent
setlocal nopreviewwindow
setlocal quoteescape=\\
setlocal noreadonly
setlocal norelativenumber
setlocal norightleft
setlocal rightleftcmd=search
setlocal noscrollbind
setlocal shiftwidth=4
setlocal noshortname
setlocal signcolumn=auto
setlocal smartindent
setlocal softtabstop=0
setlocal nospell
setlocal spellcapcheck=[.?!]\\_[\\])'\"\	\ ]\\+
setlocal spellfile=
setlocal spelllang=en
setlocal statusline=%!airline#statusline(1)
setlocal suffixesadd=
setlocal swapfile
setlocal synmaxcol=3000
if &syntax != 'markdown'
setlocal syntax=markdown
endif
setlocal tabstop=4
setlocal tagcase=
setlocal tags=
setlocal termkey=
setlocal termsize=
setlocal textwidth=0
setlocal thesaurus=
setlocal undofile
setlocal undolevels=-123456
setlocal nowinfixheight
setlocal nowinfixwidth
setlocal wrap
setlocal wrapmargin=0
let s:l = 37 - ((26 * winheight(0) + 17) / 35)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
37
normal! 0
tabedit docs/DEV_README.md
set splitbelow splitright
wincmd t
set winminheight=1 winheight=1 winminwidth=1 winwidth=1
argglobal
if bufexists('docs/DEV_README.md') | buffer docs/DEV_README.md | else | edit docs/DEV_README.md | endif
setlocal keymap=
setlocal noarabic
setlocal noautoindent
setlocal backupcopy=
setlocal balloonexpr=
setlocal nobinary
setlocal nobreakindent
setlocal breakindentopt=
setlocal bufhidden=
setlocal buflisted
setlocal buftype=
setlocal nocindent
setlocal cinkeys=0{,0},0),:,0#,!^F,o,O,e
setlocal cinoptions=
setlocal cinwords=if,else,while,do,for,switch
setlocal colorcolumn=
setlocal comments=fb:*,fb:-,fb:+,n:>
setlocal commentstring=>\ %s
setlocal complete=.,w,b,u,t,i
setlocal concealcursor=
setlocal conceallevel=0
setlocal completefunc=
setlocal nocopyindent
setlocal cryptmethod=
setlocal nocursorbind
setlocal nocursorcolumn
setlocal nocursorline
setlocal define=
setlocal dictionary=
setlocal nodiff
setlocal equalprg=
setlocal errorformat=
setlocal expandtab
if &filetype != 'markdown'
setlocal filetype=markdown
endif
setlocal fixendofline
set foldcolumn=5
setlocal foldcolumn=0
setlocal foldenable
setlocal foldexpr=0
setlocal foldignore=#
setlocal foldlevel=0
setlocal foldmarker={{{,}}}
set foldmethod=syntax
setlocal foldmethod=syntax
setlocal foldminlines=1
setlocal foldnestmax=20
setlocal foldtext=foldtext()
setlocal formatexpr=
setlocal formatoptions=tcqln
setlocal formatlistpat=^\\s*\\d\\+\\.\\s\\+\\|^[-*+]\\s\\+\\|^\\[^\\ze[^\\]]\\+\\]:
setlocal formatprg=
setlocal grepprg=
setlocal iminsert=0
setlocal imsearch=-1
setlocal include=
setlocal includeexpr=
setlocal indentexpr=
setlocal indentkeys=0{,0},:,0#,!^F,o,O,e
setlocal noinfercase
setlocal iskeyword=@,48-57,_,192-255
setlocal keywordprg=
setlocal nolinebreak
setlocal nolisp
setlocal lispwords=
setlocal nolist
setlocal makeencoding=
setlocal makeprg=
setlocal matchpairs=(:),{:},[:],<:>
setlocal modeline
setlocal modifiable
setlocal nrformats=bin,octal,hex
set number
setlocal nonumber
setlocal numberwidth=4
setlocal omnifunc=htmlcomplete#CompleteTags
setlocal path=
setlocal nopreserveindent
setlocal nopreviewwindow
setlocal quoteescape=\\
setlocal noreadonly
setlocal norelativenumber
setlocal norightleft
setlocal rightleftcmd=search
setlocal noscrollbind
setlocal shiftwidth=4
setlocal noshortname
setlocal signcolumn=auto
setlocal smartindent
setlocal softtabstop=0
setlocal nospell
setlocal spellcapcheck=[.?!]\\_[\\])'\"\	\ ]\\+
setlocal spellfile=
setlocal spelllang=en
setlocal statusline=%!airline#statusline(1)
setlocal suffixesadd=
setlocal swapfile
setlocal synmaxcol=3000
if &syntax != 'markdown'
setlocal syntax=markdown
endif
setlocal tabstop=4
setlocal tagcase=
setlocal tags=
setlocal termkey=
setlocal termsize=
setlocal textwidth=0
setlocal thesaurus=
setlocal undofile
setlocal undolevels=-123456
setlocal nowinfixheight
setlocal nowinfixwidth
setlocal wrap
setlocal wrapmargin=0
let s:l = 71 - ((0 * winheight(0) + 17) / 35)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
71
normal! 0
tabedit galaxy.yml
set splitbelow splitright
wincmd t
set winminheight=1 winheight=1 winminwidth=1 winwidth=1
argglobal
if bufexists('galaxy.yml') | buffer galaxy.yml | else | edit galaxy.yml | endif
setlocal keymap=
setlocal noarabic
setlocal autoindent
setlocal backupcopy=
setlocal balloonexpr=
setlocal nobinary
setlocal nobreakindent
setlocal breakindentopt=
setlocal bufhidden=
setlocal buflisted
setlocal buftype=
setlocal nocindent
setlocal cinkeys=0{,0},0),:,0#,!^F,o,O,e
setlocal cinoptions=
setlocal cinwords=if,else,while,do,for,switch
setlocal colorcolumn=
setlocal comments=:#
setlocal commentstring=#\ %s
setlocal complete=.,w,b,u,t,i
setlocal concealcursor=
setlocal conceallevel=0
setlocal completefunc=
setlocal nocopyindent
setlocal cryptmethod=
setlocal nocursorbind
setlocal nocursorcolumn
setlocal nocursorline
setlocal define=
setlocal dictionary=
setlocal nodiff
setlocal equalprg=
setlocal errorformat=
setlocal expandtab
if &filetype != 'yaml'
setlocal filetype=yaml
endif
setlocal fixendofline
set foldcolumn=5
setlocal foldcolumn=5
setlocal foldenable
setlocal foldexpr=0
setlocal foldignore=#
setlocal foldlevel=0
setlocal foldmarker={{{,}}}
set foldmethod=syntax
setlocal foldmethod=syntax
setlocal foldminlines=1
setlocal foldnestmax=20
setlocal foldtext=foldtext()
setlocal formatexpr=
setlocal formatoptions=croql
setlocal formatlistpat=^\\s*\\d\\+[\\]:.)}\\t\ ]\\s*
setlocal formatprg=
setlocal grepprg=
setlocal iminsert=0
setlocal imsearch=-1
setlocal include=
setlocal includeexpr=
setlocal indentexpr=GetYAMLIndent(v:lnum)
setlocal indentkeys=!^F,o,O,0#,0},0],<:>,0-
setlocal noinfercase
setlocal iskeyword=@,48-57,_,192-255
setlocal keywordprg=
setlocal nolinebreak
setlocal nolisp
setlocal lispwords=
setlocal nolist
setlocal makeencoding=
setlocal makeprg=
setlocal matchpairs=(:),{:},[:]
setlocal modeline
setlocal modifiable
setlocal nrformats=bin,octal,hex
set number
setlocal number
setlocal numberwidth=4
setlocal omnifunc=
setlocal path=
setlocal nopreserveindent
setlocal nopreviewwindow
setlocal quoteescape=\\
setlocal noreadonly
setlocal norelativenumber
setlocal norightleft
setlocal rightleftcmd=search
setlocal noscrollbind
setlocal shiftwidth=2
setlocal noshortname
setlocal signcolumn=auto
setlocal nosmartindent
setlocal softtabstop=0
setlocal nospell
setlocal spellcapcheck=[.?!]\\_[\\])'\"\	\ ]\\+
setlocal spellfile=
setlocal spelllang=en
setlocal statusline=%!airline#statusline(1)
setlocal suffixesadd=
setlocal swapfile
setlocal synmaxcol=3000
if &syntax != 'yaml'
setlocal syntax=yaml
endif
setlocal tabstop=2
setlocal tagcase=
setlocal tags=
setlocal termkey=
setlocal termsize=
setlocal textwidth=0
setlocal thesaurus=
setlocal undofile
setlocal undolevels=-123456
setlocal nowinfixheight
setlocal nowinfixwidth
setlocal wrap
setlocal wrapmargin=0
let s:l = 15 - ((11 * winheight(0) + 17) / 35)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
15
normal! 09|
tabedit plugins/modules/infini_map.py
set splitbelow splitright
wincmd _ | wincmd |
split
1wincmd k
wincmd w
wincmd t
set winminheight=1 winheight=1 winminwidth=1 winwidth=1
exe '1resize ' . ((&lines * 15 + 19) / 38)
exe '2resize ' . ((&lines * 19 + 19) / 38)
argglobal
if bufexists('plugins/modules/infini_map.py') | buffer plugins/modules/infini_map.py | else | edit plugins/modules/infini_map.py | endif
let s:cpo_save=&cpo
set cpo&vim
inoremap <buffer> <silent> <Nul> =pymode#rope#complete(0)
inoremap <buffer> <silent> <C-Space> =pymode#rope#complete(0)
noremap <buffer> <silent> ra :PymodeRopeAutoImport
noremap <buffer> <silent> r1p :call pymode#rope#module_to_package()
noremap <buffer> <silent> rnc :call pymode#rope#generate_class()
noremap <buffer> <silent> rnp :call pymode#rope#generate_package()
noremap <buffer> <silent> rnf :call pymode#rope#generate_function()
noremap <buffer> <silent> ru :call pymode#rope#use_function()
noremap <buffer> <silent> rs :call pymode#rope#signature()
noremap <buffer> <silent> rv :call pymode#rope#move()
noremap <buffer> <silent> ri :call pymode#rope#inline()
vnoremap <buffer> <silent> rl :call pymode#rope#extract_variable()
vnoremap <buffer> <silent> rm :call pymode#rope#extract_method()
noremap <buffer> <silent> r1r :call pymode#rope#rename_module()
noremap <buffer> <silent> rr :call pymode#rope#rename()
noremap <buffer> <silent> ro :call pymode#rope#organize_imports()
noremap <buffer> <silent> f :call pymode#rope#find_it()
noremap <buffer> <silent> d :call pymode#rope#show_doc()
noremap <buffer> <silent> g :call pymode#rope#goto_definition()
nnoremap <buffer> <silent> ,b :call pymode#breakpoint#operate(line('.'))
vnoremap <buffer> <silent> ,r :PymodeRun
nnoremap <buffer> <silent> ,r :PymodeRun
onoremap <buffer> C :call pymode#motion#select_c('^\s*class\s', 0)
vnoremap <buffer> <silent> K :call pymode#doc#show(@*)
nnoremap <buffer> <silent> K :call pymode#doc#find()
onoremap <buffer> M :call pymode#motion#select('^\s*\(async\s\+\)\=@', '^\s*\(async\s\+\)\=def\s', 0)
onoremap <buffer> [C :call pymode#motion#move('^\(class\|\%(async\s\+\)\=def\)\s', 'b')
nnoremap <buffer> [C :call pymode#motion#move('^\(class\|\%(async\s\+\)\=def\)\s', 'b')
vnoremap <buffer> [M :call pymode#motion#vmove('^\s*\(async\s\+\)\=def\s', 'b')
vnoremap <buffer> [[ :call pymode#motion#vmove('^\(class\|\%(async\s\+\)\=def\)\s', 'b')
onoremap <buffer> [M :call pymode#motion#move('^\s*\(async\s\+\)\=def\s', 'b')
onoremap <buffer> [[ :call pymode#motion#move('^\(class\|\%(async\s\+\)\=def\)\s', 'b')
nnoremap <buffer> [M :call pymode#motion#move('^\s*\(async\s\+\)\=def\s', 'b')
nnoremap <buffer> [[ :call pymode#motion#move('^\(class\|\%(async\s\+\)\=def\)\s', 'b')
onoremap <buffer> ]C :call pymode#motion#move('^\(class\|\%(async\s\+\)\=def\)\s', '')
nnoremap <buffer> ]C :call pymode#motion#move('^\(class\|\%(async\s\+\)\=def\)\s', '')
vnoremap <buffer> ]M :call pymode#motion#vmove('^\s*\(async\s\+\)\=def\s', '')
vnoremap <buffer> ]] :call pymode#motion#vmove('^\(class\|\%(async\s\+\)\=def\)\s', '')
onoremap <buffer> ]M :call pymode#motion#move('^\s*\(async\s\+\)\=def\s', '')
onoremap <buffer> ]] :call pymode#motion#move('^\(class\|\%(async\s\+\)\=def\)\s', '')
nnoremap <buffer> ]M :call pymode#motion#move('^\s*\(async\s\+\)\=def\s', '')
nnoremap <buffer> ]] :call pymode#motion#move('^\(class\|\%(async\s\+\)\=def\)\s', '')
vnoremap <buffer> aM :call pymode#motion#select('^\s*\(async\s\+\)\=@', '^\s*\(async\s\+\)\=def\s', 0)
onoremap <buffer> aM :call pymode#motion#select('^\s*\(async\s\+\)\=@', '^\s*\(async\s\+\)\=def\s', 0)
vnoremap <buffer> aC :call pymode#motion#select_c('^\s*class\s', 0)
onoremap <buffer> aC :call pymode#motion#select_c('^\s*class\s', 0)
vnoremap <buffer> iM :call pymode#motion#select('^\s*\(async\s\+\)\=@', '^\s*\(async\s\+\)\=def\s', 1)
onoremap <buffer> iM :call pymode#motion#select('^\s*\(async\s\+\)\=@', '^\s*\(async\s\+\)\=def\s', 1)
vnoremap <buffer> iC :call pymode#motion#select_c('^\s*class\s', 1)
onoremap <buffer> iC :call pymode#motion#select_c('^\s*class\s', 1)
inoremap <buffer> <silent> . .=pymode#rope#complete_on_dot()
let &cpo=s:cpo_save
unlet s:cpo_save
setlocal keymap=
setlocal noarabic
setlocal noautoindent
setlocal backupcopy=
setlocal balloonexpr=
setlocal nobinary
setlocal nobreakindent
setlocal breakindentopt=
setlocal bufhidden=
setlocal buflisted
setlocal buftype=
setlocal nocindent
setlocal cinkeys=0{,0},0),:,!^F,o,O,e
setlocal cinoptions=
setlocal cinwords=if,else,while,do,for,switch
setlocal colorcolumn=+1
setlocal comments=b:#,fb:-
setlocal commentstring=#\ %s
setlocal complete=.,w,b,u,t,i
setlocal concealcursor=
setlocal conceallevel=0
setlocal completefunc=
setlocal nocopyindent
setlocal cryptmethod=
setlocal nocursorbind
setlocal nocursorcolumn
setlocal nocursorline
setlocal define=^s*\\(def\\|class\\)
setlocal dictionary=
setlocal nodiff
setlocal equalprg=
setlocal errorformat=%+P[%f],%t:\ %#%l:%m,%Z,%+IYour\ code%m,%Z,%-G%.%#
setlocal expandtab
if &filetype != 'python'
setlocal filetype=python
endif
setlocal fixendofline
set foldcolumn=5
setlocal foldcolumn=5
setlocal foldenable
setlocal foldexpr=GetPythonFold(v:lnum)
setlocal foldignore=#
setlocal foldlevel=0
setlocal foldmarker={{{,}}}
set foldmethod=syntax
setlocal foldmethod=expr
setlocal foldminlines=1
setlocal foldnestmax=20
setlocal foldtext=PythonFoldText()
setlocal formatexpr=
setlocal formatoptions=cq
setlocal formatlistpat=^\\s*\\d\\+[\\]:.)}\\t\ ]\\s*
setlocal formatprg=
setlocal grepprg=
setlocal iminsert=0
setlocal imsearch=-1
setlocal include=^\\s*\\(from\\|import\\)
setlocal includeexpr=substitute(v:fname,'\\.','/','g')
setlocal indentexpr=pymode#indent#get_indent(v:lnum)
setlocal indentkeys=!^F,o,O,<:>,0),0],0},=elif,=except
setlocal noinfercase
setlocal iskeyword=@,48-57,_,192-255
setlocal keywordprg=pydoc
setlocal nolinebreak
setlocal nolisp
setlocal lispwords=
setlocal nolist
setlocal makeencoding=
setlocal makeprg=(echo\ '[%]';\ pylint\ -r\ y\ %)
setlocal matchpairs=(:),{:},[:]
setlocal modeline
setlocal modifiable
setlocal nrformats=bin,octal,hex
set number
setlocal number
setlocal numberwidth=4
setlocal omnifunc=pymode#rope#completions
setlocal path=
setlocal nopreserveindent
setlocal nopreviewwindow
setlocal quoteescape=\\
setlocal noreadonly
setlocal norelativenumber
setlocal norightleft
setlocal rightleftcmd=search
setlocal noscrollbind
setlocal shiftwidth=4
setlocal noshortname
setlocal signcolumn=auto
setlocal smartindent
setlocal softtabstop=0
setlocal nospell
setlocal spellcapcheck=[.?!]\\_[\\])'\"\	\ ]\\+
setlocal spellfile=
setlocal spelllang=en
setlocal statusline=%!airline#statusline(1)
setlocal suffixesadd=.py
setlocal swapfile
setlocal synmaxcol=3000
if &syntax != 'python'
setlocal syntax=python
endif
setlocal tabstop=4
setlocal tagcase=
setlocal tags=
setlocal termkey=
setlocal termsize=
setlocal textwidth=0
setlocal thesaurus=
setlocal undofile
setlocal undolevels=-123456
setlocal nowinfixheight
setlocal nowinfixwidth
setlocal nowrap
setlocal wrapmargin=0
172
normal! zo
261
normal! zo
442
normal! zo
453
normal! zo
506
normal! zo
559
normal! zo
571
normal! zo
let s:l = 277 - ((9 * winheight(0) + 7) / 15)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
277
normal! 0
wincmd w
argglobal
if bufexists('plugins/modules/infini_map.py') | buffer plugins/modules/infini_map.py | else | edit plugins/modules/infini_map.py | endif
let s:cpo_save=&cpo
set cpo&vim
inoremap <buffer> <silent> <Nul> =pymode#rope#complete(0)
inoremap <buffer> <silent> <C-Space> =pymode#rope#complete(0)
noremap <buffer> <silent> ra :PymodeRopeAutoImport
noremap <buffer> <silent> r1p :call pymode#rope#module_to_package()
noremap <buffer> <silent> rnc :call pymode#rope#generate_class()
noremap <buffer> <silent> rnp :call pymode#rope#generate_package()
noremap <buffer> <silent> rnf :call pymode#rope#generate_function()
noremap <buffer> <silent> ru :call pymode#rope#use_function()
noremap <buffer> <silent> rs :call pymode#rope#signature()
noremap <buffer> <silent> rv :call pymode#rope#move()
noremap <buffer> <silent> ri :call pymode#rope#inline()
vnoremap <buffer> <silent> rl :call pymode#rope#extract_variable()
vnoremap <buffer> <silent> rm :call pymode#rope#extract_method()
noremap <buffer> <silent> r1r :call pymode#rope#rename_module()
noremap <buffer> <silent> rr :call pymode#rope#rename()
noremap <buffer> <silent> ro :call pymode#rope#organize_imports()
noremap <buffer> <silent> f :call pymode#rope#find_it()
noremap <buffer> <silent> d :call pymode#rope#show_doc()
noremap <buffer> <silent> g :call pymode#rope#goto_definition()
nnoremap <buffer> <silent> ,b :call pymode#breakpoint#operate(line('.'))
vnoremap <buffer> <silent> ,r :PymodeRun
nnoremap <buffer> <silent> ,r :PymodeRun
onoremap <buffer> C :call pymode#motion#select_c('^\s*class\s', 0)
vnoremap <buffer> <silent> K :call pymode#doc#show(@*)
nnoremap <buffer> <silent> K :call pymode#doc#find()
onoremap <buffer> M :call pymode#motion#select('^\s*\(async\s\+\)\=@', '^\s*\(async\s\+\)\=def\s', 0)
onoremap <buffer> [C :call pymode#motion#move('^\(class\|\%(async\s\+\)\=def\)\s', 'b')
nnoremap <buffer> [C :call pymode#motion#move('^\(class\|\%(async\s\+\)\=def\)\s', 'b')
vnoremap <buffer> [M :call pymode#motion#vmove('^\s*\(async\s\+\)\=def\s', 'b')
vnoremap <buffer> [[ :call pymode#motion#vmove('^\(class\|\%(async\s\+\)\=def\)\s', 'b')
onoremap <buffer> [M :call pymode#motion#move('^\s*\(async\s\+\)\=def\s', 'b')
onoremap <buffer> [[ :call pymode#motion#move('^\(class\|\%(async\s\+\)\=def\)\s', 'b')
nnoremap <buffer> [M :call pymode#motion#move('^\s*\(async\s\+\)\=def\s', 'b')
nnoremap <buffer> [[ :call pymode#motion#move('^\(class\|\%(async\s\+\)\=def\)\s', 'b')
onoremap <buffer> ]C :call pymode#motion#move('^\(class\|\%(async\s\+\)\=def\)\s', '')
nnoremap <buffer> ]C :call pymode#motion#move('^\(class\|\%(async\s\+\)\=def\)\s', '')
vnoremap <buffer> ]M :call pymode#motion#vmove('^\s*\(async\s\+\)\=def\s', '')
vnoremap <buffer> ]] :call pymode#motion#vmove('^\(class\|\%(async\s\+\)\=def\)\s', '')
onoremap <buffer> ]M :call pymode#motion#move('^\s*\(async\s\+\)\=def\s', '')
onoremap <buffer> ]] :call pymode#motion#move('^\(class\|\%(async\s\+\)\=def\)\s', '')
nnoremap <buffer> ]M :call pymode#motion#move('^\s*\(async\s\+\)\=def\s', '')
nnoremap <buffer> ]] :call pymode#motion#move('^\(class\|\%(async\s\+\)\=def\)\s', '')
vnoremap <buffer> aM :call pymode#motion#select('^\s*\(async\s\+\)\=@', '^\s*\(async\s\+\)\=def\s', 0)
onoremap <buffer> aM :call pymode#motion#select('^\s*\(async\s\+\)\=@', '^\s*\(async\s\+\)\=def\s', 0)
vnoremap <buffer> aC :call pymode#motion#select_c('^\s*class\s', 0)
onoremap <buffer> aC :call pymode#motion#select_c('^\s*class\s', 0)
vnoremap <buffer> iM :call pymode#motion#select('^\s*\(async\s\+\)\=@', '^\s*\(async\s\+\)\=def\s', 1)
onoremap <buffer> iM :call pymode#motion#select('^\s*\(async\s\+\)\=@', '^\s*\(async\s\+\)\=def\s', 1)
vnoremap <buffer> iC :call pymode#motion#select_c('^\s*class\s', 1)
onoremap <buffer> iC :call pymode#motion#select_c('^\s*class\s', 1)
inoremap <buffer> <silent> . .=pymode#rope#complete_on_dot()
let &cpo=s:cpo_save
unlet s:cpo_save
setlocal keymap=
setlocal noarabic
setlocal noautoindent
setlocal backupcopy=
setlocal balloonexpr=
setlocal nobinary
setlocal nobreakindent
setlocal breakindentopt=
setlocal bufhidden=
setlocal buflisted
setlocal buftype=
setlocal nocindent
setlocal cinkeys=0{,0},0),:,!^F,o,O,e
setlocal cinoptions=
setlocal cinwords=if,else,while,do,for,switch
setlocal colorcolumn=+1
setlocal comments=b:#,fb:-
setlocal commentstring=#\ %s
setlocal complete=.,w,b,u,t,i
setlocal concealcursor=
setlocal conceallevel=0
setlocal completefunc=
setlocal nocopyindent
setlocal cryptmethod=
setlocal nocursorbind
setlocal nocursorcolumn
setlocal nocursorline
setlocal define=^s*\\(def\\|class\\)
setlocal dictionary=
setlocal nodiff
setlocal equalprg=
setlocal errorformat=%+P[%f],%t:\ %#%l:%m,%Z,%+IYour\ code%m,%Z,%-G%.%#
setlocal expandtab
if &filetype != 'python'
setlocal filetype=python
endif
setlocal fixendofline
set foldcolumn=5
setlocal foldcolumn=5
setlocal foldenable
setlocal foldexpr=GetPythonFold(v:lnum)
setlocal foldignore=#
setlocal foldlevel=0
setlocal foldmarker={{{,}}}
set foldmethod=syntax
setlocal foldmethod=expr
setlocal foldminlines=1
setlocal foldnestmax=20
setlocal foldtext=PythonFoldText()
setlocal formatexpr=
setlocal formatoptions=cq
setlocal formatlistpat=^\\s*\\d\\+[\\]:.)}\\t\ ]\\s*
setlocal formatprg=
setlocal grepprg=
setlocal iminsert=0
setlocal imsearch=-1
setlocal include=^\\s*\\(from\\|import\\)
setlocal includeexpr=substitute(v:fname,'\\.','/','g')
setlocal indentexpr=pymode#indent#get_indent(v:lnum)
setlocal indentkeys=!^F,o,O,<:>,0),0],0},=elif,=except
setlocal noinfercase
setlocal iskeyword=@,48-57,_,192-255
setlocal keywordprg=pydoc
setlocal nolinebreak
setlocal nolisp
setlocal lispwords=
setlocal nolist
setlocal makeencoding=
setlocal makeprg=(echo\ '[%]';\ pylint\ -r\ y\ %)
setlocal matchpairs=(:),{:},[:]
setlocal modeline
setlocal modifiable
setlocal nrformats=bin,octal,hex
set number
setlocal number
setlocal numberwidth=4
setlocal omnifunc=pymode#rope#completions
setlocal path=
setlocal nopreserveindent
setlocal nopreviewwindow
setlocal quoteescape=\\
setlocal noreadonly
setlocal norelativenumber
setlocal norightleft
setlocal rightleftcmd=search
setlocal noscrollbind
setlocal shiftwidth=4
setlocal noshortname
setlocal signcolumn=auto
setlocal smartindent
setlocal softtabstop=0
setlocal nospell
setlocal spellcapcheck=[.?!]\\_[\\])'\"\	\ ]\\+
setlocal spellfile=
setlocal spelllang=en
setlocal statusline=%!airline#statusline(2)
setlocal suffixesadd=.py
setlocal swapfile
setlocal synmaxcol=3000
if &syntax != 'python'
setlocal syntax=python
endif
setlocal tabstop=4
setlocal tagcase=
setlocal tags=
setlocal termkey=
setlocal termsize=
setlocal textwidth=0
setlocal thesaurus=
setlocal undofile
setlocal undolevels=-123456
setlocal nowinfixheight
setlocal nowinfixwidth
setlocal nowrap
setlocal wrapmargin=0
172
normal! zo
298
normal! zo
320
normal! zo
334
normal! zo
381
normal! zo
453
normal! zo
let s:l = 179 - ((6 * winheight(0) + 9) / 19)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
179
normal! 05|
wincmd w
exe '1resize ' . ((&lines * 15 + 19) / 38)
exe '2resize ' . ((&lines * 19 + 19) / 38)
tabnext 5
set stal=1
if exists('s:wipebuf')
  silent exe 'bwipe ' . s:wipebuf
endif
unlet! s:wipebuf
set winheight=1 winwidth=20 shortmess=filnxtToO
set winminheight=1 winminwidth=1
let s:sx = expand("<sfile>:p:r")."x.vim"
if file_readable(s:sx)
  exe "source " . fnameescape(s:sx)
endif
let &so = s:so_save | let &siso = s:siso_save
doautoall SessionLoadPost
unlet SessionLoad
" vim: set ft=vim :
