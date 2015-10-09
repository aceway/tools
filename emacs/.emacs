(setq user-full-name "aceway")
(setq user-mail-address "aceway@qq.com")

(setq visible-bell t)
(setq sentence-end "\\([。！？]\\|……\\|[.?!][]\"')}]*\\($\\|[ \t]\\)\\)[ \t\n]*")
(setq sentence-end-double-space nil)
(setq scroll-margin 3
      croll-conservatively 10000)
(mouse-avoidance-mode 'animate)
(global-linum-mode t)

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; 指针颜色设置为白色
(set-cursor-color "green")
;; 鼠标颜色设置为白色
(set-mouse-color "white")
(setq color-theme-is-global t)
;; 一打开就起用 text 模式。 
(setq default-major-mode 'text-mode)
;; 语法高亮
(global-font-lock-mode t)
;; 以 y/n代表 yes/no
(fset 'yes-or-no-p 'y-or-n-p) 
;; 显示括号匹配 
(show-paren-mode t)
(setq show-paren-style 'parentheses)
;; 显示时间，格式如下
(display-time-mode 1) 
(setq display-time-24hr-format t) 
(setq display-time-day-and-date t) 
;; 支持emacs和外部程序的粘贴
(setq x-select-enable-clipboard t) 
;; 在标题栏提示你目前在什么位置
(setq frame-title-format "aceway%b") 
;; 默认显示 80列就换行 
(setq default-fill-column 80) 
;; 去掉工具栏
;(tool-bar-mode nil)
;;去掉菜单栏
(menu-bar-mode nil)
;; 显示列号
(setq column-number-mode t)
(setq line-number-mode t)

(setq inferior-lisp-program "/usr/local/bin/sbcl")  

(require 'ido)
(ido-mode t)
(add-to-list 'load-path "~/workspace/software/slime-2.15/")
(require 'slime)
(require 'slime-autoloads)
(slime-setup '(slime-fancy))
(slime-setup '(slime-repl))

(require 'package)
(package-initialize)
(add-to-list 'package-archives'
    ("elpa" . "http://tromey.com/elpa/") t)
(add-to-list 'package-archives'
    ("marmalade" . "http://marmalade-repo.org/packages/") t)
(add-to-list 'package-archives'
    ("melpa" . "http://melpa.milkbox.net/packages/") t)
(package-initialize)

(add-to-list 'load-path "~/.emacs.d/popup")    ; This may not be appeared if you have already added.
(require 'popup)

(add-to-list 'load-path "~/.emacs.d/auto-complete")    ; This may not be appeared if you have already added.
(require 'auto-complete-config)
(add-to-list 'ac-dictionary-directories "~/.emacs.d/auto-complete/ac-dict")
(ac-config-default)

(add-to-list 'load-path "~/.emacs.d/plugins/yasnippet")
(require 'yasnippet)
(yas-global-mode 1)

(add-to-list 'load-path "~/.emacs.d/markdown")
(autoload 'markdown-mode "markdown-mode"
  "Major mode for editing Markdown files" t)
(add-to-list 'auto-mode-alist '("\\.text\\'" . markdown-mode))
(add-to-list 'auto-mode-alist '("\\.markdown\\'" . markdown-mode))
(add-to-list 'auto-mode-alist '("\\.md\\'" . markdown-mode))

;(add-to-list 'exec-path "/usr/local/bin/w3m")
;(add-to-list 'load-path "~/.emacs.d/emacs-w3m-1.4.4/")
;(add-to-list 'load-path "~/.emacs.d/emacs-w3m/")
;(require 'w3m-load)
;(require 'w3m-lnum)
;(require 'w3m-util)
;(setq w3m-home-page "http://www.lispworks.com/documentation/HyperSpec/Front/Contents.htm")

;; color theme
(add-to-list 'load-path "~/.emacs.d/color-theme-6.6.0")
(require 'color-theme)
(eval-after-load "color-theme"
  '(progn
       (color-theme-initialize)))

(add-to-list 'load-path "~/.emacs.d/el-get/el-get")
(unless (require 'el-get nil 'noerror)
  (with-current-buffer
      (url-retrieve-synchronously
       "https://raw.githubusercontent.com/dimitri/el-get/master/el-get-install.el")
    (goto-char (point-max))
    (eval-print-last-sexp)))
(add-to-list 'el-get-recipe-path "~/.emacs.d/el-get-user/recipes")
(el-get 'sync)
