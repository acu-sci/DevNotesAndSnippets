## **VIM Basic navigation**

* **Opening a file:**
>vim filename.txt


* **Switching between modes:**
   - To enter insert mode: Press `i`
   - To return to command mode: Press `Esc`

* **Moving the cursor:**
   - **$** - go to the end of the line
   - **0** - go to the start of the line
   - **h** - Move the cursor left.
   - **j** - Move the cursor down.
   - **k** - Move the cursor up.
   - **l** - Move the cursor right.

* **Multicursor:**
   - v to enter visual mode  
   - make a selection  
   - I to enter insert mode in all lines of selecttion  

* **Fancy moving cursor:**
   - **f** - find and move to a character in current line
   - **w** - go to the start of the next word
   - **b** - go backwards in words
   - **}** - move to next paragraph
* **Moving to specific line numbers:**
   - To jump to a specific line number: `G` followed by the line number. For example, `10G` to go to line 10.

* **Scrolling through the file:**
   - **Ctrl + f** - Scroll forward one page.
   - **Ctrl + b** - Scroll backward one page.
   - **Ctrl + u** - Scroll half a page up.
   - **Ctrl + d** - Scroll half a page down.

* **Searching for text:**
   - To search for text: `/` followed by the text. Press `Enter` to perform the search.
   - To search for the next occurrence: Press `n`.
   - To search for the previous occurrence: Press `N`.

* **Saving and quitting:**
   - To save and exit: `:wq`
   - To quit without saving: `:q!`

* To remove a whole line in Vim, you can use the `dd` command