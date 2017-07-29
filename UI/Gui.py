import tkinter.ttk as ttk
from tkinter import *


from DA.Da import *


class Gui(Tk):

    def __init__(self, parent):
        Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()



    def initialize(self):
        self.Frame_Appli = Frame(self.parent, borderwidth=2, relief=GROOVE)

        Frame_Menu = Frame(self.parent)
        Frame_Menu.pack(side=LEFT, padx=10,pady=10)

        Bouton_Ajout = Button(Frame_Menu,text = 'Nouvelle Entrée',command=self.Add_Input)
        Bouton_Ajout.pack(pady=5,fill=X)

        Bouton_Journal = Button(Frame_Menu, text='Voir le Journal',command=self.voir_journal)
        Bouton_Journal.pack(pady=5,fill=X)

        Bouton_Comptes = Button(Frame_Menu,text='Voir les Comptes')
        Bouton_Comptes.pack(pady=5,fill=X)

        Bouton_Resultat = Button(Frame_Menu, text='Voir le Resultat')
        Bouton_Resultat.pack(pady=5,fill=X)

        Bouton_Bilan = Button(Frame_Menu,text='Voir le Bilan')
        Bouton_Bilan.pack(pady=5,fill=X)

        self.Frame_Appli.pack(side=LEFT, padx=20, pady=20, fill=NONE, expand=TRUE)
        self.Add_Input()

    def unload_Appli(self,FrameToUnload):

        list = FrameToUnload.pack_slaves()
        for widget in list:
            widget.destroy()

    def Add_Input(self):
        self.unload_Appli(self.Frame_Appli)

        # Label nouvelle entrée
        label = Label(self.Frame_Appli, text="Nouvelle entrée")
        label.pack()

        # Frame conteneur
        # Frame1 = Frame(self.Frame_Appli, borderwidth=2, relief=GROOVE)
        # Frame1.pack(side=TOP, padx=30, pady=20)

        # Date
        label = Label(self.Frame_Appli, text="Date (jj/mm/aaaa)")
        label.pack()
        iptDate = Entry(self.Frame_Appli)
        iptDate.pack(padx=10)

        # Compte
        label = Label(self.Frame_Appli, text="Compte")
        label.pack()
        listeComptes = Listbox(self.Frame_Appli,width=60)

        maliste= sqlite.SelectAccounts()
        for i in sqlite.SelectAccounts():
            listeComptes.insert(i[0],str('  ' + i[1]))
            print (i[0],i[1])
        listeComptes.pack(pady=5)

        # Libelle
        label = Label(self.Frame_Appli, text="Libellé")
        label.pack()
        iptLib = Entry(self.Frame_Appli, width=60)
        iptLib.pack(padx=30)

        # Frame conteneur
        Frame2 = Frame(self.Frame_Appli, borderwidth=2, relief=GROOVE)
        Frame2.pack(side=TOP, pady=10)

        # entree / sortie
        value = StringVar()
        iptSens = IntVar()
        iptEntree = Radiobutton(Frame2, text="Entrée", variable=iptSens, value=1)
        iptSortie = Radiobutton(Frame2, text="Sortie", variable=iptSens, value=2)
        iptEntree.pack(pady=5)
        iptSortie.pack(pady=5)

        # Montant
        label = Label(self.Frame_Appli, text="Montant")
        label.pack()
        iptMontant = Entry(self.Frame_Appli, width=60)
        iptMontant.pack()

        # bouton valider
        bouton = Button(self.Frame_Appli,
                        text="valider",width=50,
                        command=lambda: Da.AddToDB(iptDate.get(),
                                                maliste[listeComptes.curselection()[0]],
                                                iptLib.get(), iptSens.get(), iptMontant.get()))
        bouton.pack(pady=10)

    def voir_journal(self):

        self.unload_Appli(self.Frame_Appli)

        self.Frame_Appli.pack(fill=BOTH)

        frame_dt = Frame(self.Frame_Appli)
        frame_dt.pack(side=LEFT, padx=20, pady=20)

        tree_dt = ttk.Treeview(frame_dt)

        tree_dt.pack(padx=2, pady=2)

        tree_dt.heading("#0",text="Date")
        tree_dt.column("#0", width=110)

        for dt in sqlite.MonthQuery():
            id = tree_dt.insert("",0,iid= parser.parse(dt[0]).year,text=parser.parse(dt[0]).year)
            tree_dt.insert(id, "end", text='Janvier', values=1)
            tree_dt.insert(id, "end", text='Février', values=2)
            tree_dt.insert(id, "end", text='Mars', values=3)
            tree_dt.insert(id, "end", text='Avril', values=4)
            tree_dt.insert(id, "end", text='Mai', values=5)
            tree_dt.insert(id, "end", text='Juin', values=6)
            tree_dt.insert(id, "end", text='Juillet', values=7)
            tree_dt.insert(id, "end", text='Aout', values=8)
            tree_dt.insert(id, "end", text='Septembre', values=9)
            tree_dt.insert(id, "end", text='Octobre', values=10)
            tree_dt.insert(id, "end", text='Novembre', values=11)
            tree_dt.insert(id, "end", text='Décembre', values=12)


        label = Label(self.Frame_Appli,text='Journal')
        label.pack(expand=FALSE)

        scrollbar = Scrollbar(self.Frame_Appli)
        scrollbar.pack(side=RIGHT, fill=Y)

        cols = ("CLE","Date","Compte", "Libellé", "Sens","Montant")
        dcols =("Date","Compte", "Libellé", "Sens","Montant")
        tree=ttk.Treeview(self.Frame_Appli,columns=cols, displaycolumns=dcols,yscrollcommand=scrollbar.set)
        tree['show'] = 'headings'
        tree.column("Date",width=80)
        tree.column("Sens", width=80)
        tree.column("Montant", width=80)

        for i in cols:
            tree.heading(i,text=i)

        scrollbar.config(command=tree.yview)
        tree.pack(fill=BOTH,expand=True)

        tree_dt.bind("<Double-1>", lambda _: self.JournalLoad("loadJournal",tree,tree_dt.parent(item=tree_dt.focus()),
                                                              tree_dt.item(tree_dt.focus())['values'][0]))


    def JournalLoad(self,event,tree,SelectedYear,SelectedMonth):
        for i in tree.get_children():
            tree.delete(i)
        SelectedYear=str(SelectedYear)
        if len(str(SelectedMonth))==1:
            SelectedMonth = '0' + str(SelectedMonth)
        else:
            SelectedMonth = str(SelectedMonth)

        for item in sqlite.SelectQuery(SelectedMonth, SelectedYear):
            # print(item)
            tree.insert("", 0, text="", values=item)

