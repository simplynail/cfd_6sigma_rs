# -*- coding: utf-8 -*-
'''
ttk_multicolumn_listbox2.py
Python31 includes the Tkinter Tile extension ttk.
Ttk comes with 17 widgets, 11 of which already exist in Tkinter:
Button, Checkbutton, Entry, Frame, Label, LabelFrame, Menubutton,
PanedWindow, Radiobutton, Scale and Scrollbar
The 6 new widget classes are:
Combobox, Notebook, Progressbar, Separator, Sizegrip and Treeview
For additional info see the Python31 manual:
http://gpolo.ath.cx:81/pydoc/library/ttk.html
Here the TreeView widget is configured as a multi-column listbox
with adjustable column width and column-header-click sorting.
Tested with Python 3.1.1 and Tkinter 8.5
'''
import tkinter as tk
import tkinter.font as tkFont
import tkinter.ttk as ttk

class McListBox(object):
    """use a ttk.TreeView as a multicolumn ListBox"""
    def __init__(self,headers,rows):
        self.items_header = headers
        self.items_list = rows
        self.container = None
        self.tree = None
        self.build()
        
    def build(self):
        self._setup_widgets()
        self._build_tree()
        
    def _setup_widgets(self):
        self.container = ttk.Frame()
        self.container.grid()
        # create a treeview with dual scrollbars
        self.tree = ttk.Treeview(self.container,columns=self.items_header, show="headings")
        for item in self.items_header:
            self.tree.column(item,anchor='center')
        vsb = ttk.Scrollbar(orient="vertical",
            command=self.tree.yview)
        hsb = ttk.Scrollbar(orient="horizontal",
            command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set,
            xscrollcommand=hsb.set)
        self.tree.grid(column=0, row=0, sticky='nsew', in_=self.container)
        vsb.grid(column=1, row=0, sticky='ns', in_=self.container)
        hsb.grid(column=0, row=1, sticky='ew', in_=self.container)
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_rowconfigure(0, weight=1)
        
    def _build_tree(self):
        for col in self.items_header:
            self.tree.heading(col, text=col,
                command=lambda c=col: self.sortby(self.tree, c, 0))
            # adjust the column's width to the header string
            self.tree.column(col,
                width=tkFont.Font().measure(col.title()))
        for item in self.items_list:
            self.tree.insert('', 'end', values=item)
            # adjust column's width if necessary to fit each value
            for ix, val in enumerate(item):
                col_w = tkFont.Font().measure(val)
                if self.tree.column(self.items_header[ix],width=None)<col_w:
                    self.tree.column(self.items_header[ix], width=col_w)
                    
    def sortby(self, tree, col, descending):
        """sort tree contents when a column header is clicked on"""
        # grab values to sort
        data = [(tree.set(child, col), child) \
            for child in tree.get_children('')]
        # if the data to be sorted is numeric change to float
        #data =  change_numeric(data):
        for no,item in enumerate(data):
            try:
                temp = (float(item[0]),item[1])
                data[no] = temp
            except:
                pass
            
            try:
                temp = (int(item[0]),item[1])
                data[no] = temp
            except:
                pass
        # now sort the data in place
        data.sort(reverse=descending)
        for ix, item in enumerate(data):
            tree.move(item[1], '', ix)
        # switch the heading so it will sort in the opposite direction
        tree.heading(col, command=lambda col=col: self.sortby(tree, col, \
            int(not descending)))
    
if __name__ == "__main__":
    
    # the test data ...
    car_header = ['car', 'repair']
    car_list = [
    ('Hyundai', 'brakes') ,
    ('Honda', 'light') ,
    ('Lexus', 'battery') ,
    ('Benz', 'wiper') ,
    ('Ford', 'tire') ,
    ('Chevy', 'air') ,
    ('Chrysler', 'piston') ,
    ('Toyota', 'brake pedal') ,
    ('BMW', 'seat')
    ]
    
    val_types = ['txt','int','float']
    vals = [
    ('aaa', '10', '52.3') ,
    ('ccc', '2', '521.3') ,
    ('b', '110', '2.3')
    ]
    
    root = tk.Tk()
    root.wm_title("multicolumn ListBox")
    
    #mc_listbox = McListBox(car_header,car_list)
    mc_listbox = McListBox(val_types,vals)
    
    mc_listbox.intro_string = 'costam costam costam costam costam \n costam costam costam costam '
    root.mainloop()