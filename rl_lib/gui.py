# Created by modifying GUI generated py PAGE version 4.10
# In conjunction with Tcl version 8.6


import sys

try:
    from Tkinter import *
except ImportError:
    from tkinter import *

try:
    import ttk
    py3 = 0
except ImportError:
    import tkinter.ttk as ttk
    py3 = 1

from rl_lib.envs.gridWorldEnv import GridWorldEnv
from rl_lib.discreteQLearning import QLearnerDiscrete
from rl_lib.utils.gridWorldRenderer import GridWorldRenderer


def _start_gui():
    '''Starting point when module is the main routine.'''
    global val, w
    learner_params_.set_gui_default_params()
    top = New_Toplevel_1 (root)
    root.mainloop()

w = None
def _create_New_Toplevel_1(root, *args, **kwargs):
    '''Starting point when module is imported by another program.'''
    global w, w_win, rt
    rt = root
    w = Toplevel (root)
    learner_params_.set_gui_default_params()
    top = New_Toplevel_1 (w)
    return (w, top)

def _destroy_New_Toplevel_1():
    global w
    w.destroy()
    w = None

def _close_gui():
    global root
    print "closing GUI"
    root.destroy()
    root = None


class New_Toplevel_1:
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85' 
        _ana2color = '#d9d9d9' # X11 color: 'gray85' 
        font9 = "-family {DejaVu Sans} -size 12 -weight normal -slant "  \
            "roman -underline 0 -overstrike 0"

        top.geometry("533x390+598+110")
        top.title("QLearning Demo")
        top.configure(highlightbackground="wheat")
        top.configure(highlightcolor="black")

        self.Startbutton = Button(top)
        self.Startbutton.place(relx=0.75, rely=0.73, height=65, width=100)
        self.Startbutton.configure(activebackground="#f4bcb2")
        self.Startbutton.configure(disabledforeground="#b8a786")
        self.Startbutton.configure(font=font9)
        self.Startbutton.configure(highlightbackground="wheat")
        self.Startbutton.configure(text='''Start''')
        self.Startbutton.bind('<Button-1>',lambda e:learner_params_.buttonSTARTpressed())
        self.Startbutton.bind('<Key-space>',lambda e:learner_params_.buttonSTARTpressed())

        self.Labelframe1 = LabelFrame(top)
        self.Labelframe1.place(relx=0.05, rely=0.05, relheight=0.2
                , relwidth=0.29)
        self.Labelframe1.configure(relief=GROOVE)
        self.Labelframe1.configure(font=font9)
        self.Labelframe1.configure(text='''Grid Size''')
        self.Labelframe1.configure(highlightbackground="#f5deb3")
        self.Labelframe1.configure(width=155)

        self.Label2 = Label(self.Labelframe1)
        self.Label2.place(relx=0.1, rely=0.12, height=18, width=36)
        self.Label2.configure(activebackground="#f9f9f9")
        self.Label2.configure(text='''Rows''')
        self.Label4 = Label(self.Labelframe1)
        self.Label4.place(relx=0.52, rely=0.12, height=18, width=56)
        self.Label4.configure(activebackground="#f9f9f9")
        self.Label4.configure(text='''Columns''')

        self.row = Entry(self.Labelframe1)
        self.row.place(relx=0.1, rely=0.48,height=20, relwidth=0.23)
        self.row.configure(background="white")
        self.row.configure(font="TkFixedFont")
        self.row.configure(selectbackground="#c4c4c4")
        self.row.configure(textvariable=learner_params_.row_num)

        self.col = Entry(self.Labelframe1)
        self.col.place(relx=0.58, rely=0.48,height=20, relwidth=0.23)
        self.col.configure(background="white")
        self.col.configure(font="TkFixedFont")
        self.col.configure(selectbackground="#c4c4c4")
        self.col.configure(textvariable=learner_params_.col_num)

        self.Labelframe2 = LabelFrame(top)
        self.Labelframe2.place(relx=0.39, rely=0.05, relheight=0.2
                , relwidth=0.25)
        self.Labelframe2.configure(relief=GROOVE)
        self.Labelframe2.configure(font=font9)
        self.Labelframe2.configure(text='''Starting Point''')
        self.Labelframe2.configure(highlightbackground="#f5deb3")
        self.Labelframe2.configure(width=135)

        self.Label5 = Label(self.Labelframe2)
        self.Label5.place(relx=0.11, rely=0.12, height=18, width=46)
        self.Label5.configure(activebackground="#f9f9f9")
        self.Label5.configure(text='''Row No.''')
        self.Label5.configure(width=46)

        self.Label7 = Label(self.Labelframe2)
        self.Label7.place(relx=0.52, rely=0.12, height=18, width=56)
        self.Label7.configure(activebackground="#f9f9f9")
        self.Label7.configure(text='''Col No.''')

        self.start_row = Entry(self.Labelframe2)
        self.start_row.place(relx=0.14, rely=0.48,height=20, relwidth=0.27)
        self.start_row.configure(background="white")
        self.start_row.configure(font="TkFixedFont")
        self.start_row.configure(textvariable=learner_params_.start_row)

        self.start_col = Entry(self.Labelframe2)
        self.start_col.place(relx=0.6, rely=0.48,height=20, relwidth=0.27)
        self.start_col.configure(background="white")
        self.start_col.configure(font="TkFixedFont")
        self.start_col.configure(selectbackground="#c4c4c4")
        self.start_col.configure(textvariable=learner_params_.start_col)

        self.Labelframe4 = LabelFrame(top)
        self.Labelframe4.place(relx=0.69, rely=0.05, relheight=0.2
                , relwidth=0.25)
        self.Labelframe4.configure(relief=GROOVE)
        self.Labelframe4.configure(font=font9)
        self.Labelframe4.configure(text='''Goal''')
        self.Labelframe4.configure(highlightbackground="#f5deb3")
        self.Labelframe4.configure(width=135)

        self.Label11 = Label(self.Labelframe4)
        self.Label11.place(relx=0.11, rely=0.12, height=18, width=46)
        self.Label11.configure(activebackground="#f9f9f9")
        self.Label11.configure(text='''Row No.''')

        self.Label13 = Label(self.Labelframe4)
        self.Label13.place(relx=0.52, rely=0.12, height=18, width=56)
        self.Label13.configure(activebackground="#f9f9f9")
        self.Label13.configure(text='''Col No.''')

        self.goal_row = Entry(self.Labelframe4)
        self.goal_row.place(relx=0.14, rely=0.48,height=20, relwidth=0.27)
        self.goal_row.configure(background="white")
        self.goal_row.configure(font="TkFixedFont")
        self.goal_row.configure(selectbackground="#c4c4c4")
        self.goal_row.configure(textvariable=learner_params_.goal_row)

        self.goal_col = Entry(self.Labelframe4)
        self.goal_col.place(relx=0.6, rely=0.48,height=20, relwidth=0.27)
        self.goal_col.configure(background="white")
        self.goal_col.configure(font="TkFixedFont")
        self.goal_col.configure(selectbackground="#c4c4c4")
        self.goal_col.configure(textvariable=learner_params_.goal_col)

        self.Labelframe6 = LabelFrame(top)
        self.Labelframe6.place(relx=0.05, rely=0.3, relheight=0.35, relwidth=0.9)

        self.Labelframe6.configure(relief=GROOVE)
        self.Labelframe6.configure(font=font9)
        self.Labelframe6.configure(text='''Learning Parameters''')
        self.Labelframe6.configure(width=480)

        self.learning_rate = Scale(self.Labelframe6)
        self.learning_rate.place(relx=0.23, rely=0, relwidth=0.22
                , relheight=0.0, height=39)
        self.learning_rate.configure(activebackground="#f4bcb2")
        self.learning_rate.configure(font="TkTextFont")
        self.learning_rate.configure(orient="horizontal")
        self.learning_rate.configure(resolution="0.01")
        self.learning_rate.configure(to="1.0")
        self.learning_rate.configure(troughcolor="#d9d9d9")
        self.learning_rate.configure(variable=learner_params_.lr)

        self.Label1 = Label(self.Labelframe6)
        self.Label1.place(relx=0.02, rely=0.16, height=18, width=86)
        self.Label1.configure(activebackground="#f9f9f9")
        self.Label1.configure(text='''Learning Rate''')

        self.Label17 = Label(self.Labelframe6)
        self.Label17.place(relx=0.01, rely=0.49, height=18, width=106)
        self.Label17.configure(activebackground="#f9f9f9")
        self.Label17.configure(text='''Discount Factor''')

        self.discount_factor = Scale(self.Labelframe6)
        self.discount_factor.place(relx=0.23, rely=0.33, relwidth=0.22
                , relheight=0.0, height=39)
        self.discount_factor.configure(activebackground="#f4bcb2")
        self.discount_factor.configure(font="TkTextFont")
        self.discount_factor.configure(orient="horizontal")
        self.discount_factor.configure(resolution="0.01")
        self.discount_factor.configure(to="1.0")
        self.discount_factor.configure(troughcolor="#d9d9d9")
        self.discount_factor.configure(variable=learner_params_.df)

        self.Label18 = Label(self.Labelframe6)
        self.Label18.place(relx=0.05, rely=0.76, height=18, width=66)
        self.Label18.configure(activebackground="#f9f9f9")
        self.Label18.configure(text='''Episodes''')
        self.Label18.configure(width=66)

        self.eps = Entry(self.Labelframe6)
        self.eps.place(relx=0.23, rely=0.75,height=20, relwidth=0.22)
        self.eps.configure(background="white")
        self.eps.configure(font="TkFixedFont")
        self.eps.configure(width=106)
        self.eps.configure(textvariable=learner_params_.eps)

        self.action_policy = ttk.Combobox(self.Labelframe6)
        self.action_policy.place(relx=0.67, rely=0.13, relheight=0.2
                , relwidth=0.31)
        self.value_list = ['epsilon (random)','epsilon-greedy',]
        self.action_policy.configure(values=self.value_list)
        self.action_policy.configure(textvariable=learner_params_.action_policy)
        self.action_policy.configure(width=147)
        self.action_policy.configure(takefocus="")

        self.Label19 = Label(self.Labelframe6)
        self.Label19.place(relx=0.47, rely=0.16, height=18, width=86)
        self.Label19.configure(activebackground="#f9f9f9")
        self.Label19.configure(text='''Action Policy''')

        self.update_policy = ttk.Combobox(self.Labelframe6)
        self.update_policy.place(relx=0.67, rely=0.46, relheight=0.2
                , relwidth=0.31)
        self.value_list = ['QL','Sarsa',]
        self.update_policy.configure(values=self.value_list)
        self.update_policy.configure(textvariable=learner_params_.update_policy)
        self.update_policy.configure(width=147)
        self.update_policy.configure(takefocus="")

        self.Label20 = Label(self.Labelframe6)
        self.Label20.place(relx=0.47, rely=0.49, height=18, width=86)
        self.Label20.configure(activebackground="#f9f9f9")
        self.Label20.configure(text='''Update Policy''')

        self.visualise_check = Checkbutton(top)
        self.visualise_check.place(relx=0.61, rely=0.57, relheight=0.05
                , relwidth=0.32)
        self.visualise_check.configure(activebackground="#f4bcb2")
        self.visualise_check.configure(justify=RIGHT)
        self.visualise_check.configure(text='''Visualise Learning Stage''')
        self.visualise_check.configure(variable=learner_params_.check_visualise)

        self.Message1 = Message(top)
        self.Message1.place(relx=0.02, rely=0.7, relheight=0.12, relwidth=0.68)
        self.Message1.configure(text='''Obstacles in the grid world is generated in random.
Click button below to place obstacles manually.''')
        self.Message1.configure(width=363)

        self.ObstaclesButton = Button(top)
        self.ObstaclesButton.place(relx=0.08, rely=0.82, height=26, width=100)
        self.ObstaclesButton.configure(activebackground="#f4bcb2")
        self.ObstaclesButton.configure(text='''Obstacles''')
        self.ObstaclesButton.bind('<Button-1>',lambda e:learner_params_.collect_obstacle_list_from_user())
        self.ObstaclesButton.bind('<Key-space>',lambda e:learner_params_.collect_obstacle_list_from_user())


class QLearnerParameters:
    def __init__(self):
        # These are Tk variables used passed to Tkinter and must be
        # defined before the widgets using them are created.
        # global row_num, col_num # Grid row and col
        self.row_num = IntVar()
        self.col_num = IntVar()
        self.start_row = IntVar()
        self.start_col = IntVar()
        self.goal_row = IntVar()
        self.goal_col = IntVar()
        self.check_visualise = StringVar()

        # learning rate and discount factor
        self.lr = DoubleVar()
        self.df = DoubleVar()
        self.eps = IntVar()

        self.action_policy = StringVar()
        self.update_policy = StringVar()

    def set_gui_default_params(self):

        self.check_visualise.set("1")
        self.row_num.set(5)
        self.col_num.set(5)
        self.start_row.set(1)
        self.start_col.set(1)
        self.goal_row.set(5)
        self.goal_col.set(5)

        self.lr.set(0.8)
        self.df.set(0.95)
        self.eps.set(2000)

        self.action_policy.set('epsilon (random)')
        self.update_policy.set('QL')


    def collect_obstacle_list_from_user(self):

        self.grid_gui = GridWorldRenderer(rows = self.row_num.get(), cols = self.col_num.get(), 
                                          start = (self.start_row.get() - 1, self.start_col.get() - 1),
                                          goal = (self.goal_row.get()- 1, self.goal_col.get()- 1),
                                          caption = 'Grid World - Set Obstacles')

        self.grid_gui.execute_collect_mouse_response()


    def buttonSTARTpressed(self):

        self.row_out = self.row_num.get()
        self.col_out = self.col_num.get()
        self.start_row_out = self.start_row.get() - 1  # indexed from 0 in qlearner code
        self.start_col_out = self.start_col.get() - 1  #
        self.goal_row_out = self.goal_row.get()- 1 #
        self.goal_col_out = self.goal_col.get() - 1 #
        self.check_vis_out = bool(int(self.check_visualise.get()))

        self.lr_out = self.lr.get()
        self.df_out = self.df.get()
        self.eps_out = self.eps.get()

        action_pol = self.action_policy.get()
        if action_pol == 'epsilon (random)':
            self.act_pol = 'epsilon'
        elif action_pol == 'epsilon-greedy':
            self.act_pol = 'epsilon_greedy'

        update_pol = self.update_policy.get()
        if update_pol == 'QL':
            self.val_update_pol = 'q'
        elif update_pol == 'Sarsa':
            self.val_update_pol = 'sarsa'

        print self.row_out, self.col_out,self.start_row_out,self.start_col_out,self.goal_row_out,self.goal_col_out, self.check_vis_out, self.lr_out, self.df_out, self.eps_out, self.act_pol
        _close_gui()



if __name__ == '__main__':

    root = Tk()


    learner_params_ = QLearnerParameters()
    _start_gui()

    if root is None:
        env = GridWorldEnv(grid_row = learner_params_.row_out, grid_col = learner_params_.col_out, 
                           start_pos = (learner_params_.start_row_out,learner_params_.start_col_out), 
                           target = (learner_params_.goal_row_out,learner_params_.goal_col_out), 
                           render = learner_params_.check_vis_out)

        learner = QLearnerDiscrete(env, lr = learner_params_.lr_out, y = learner_params_.df_out, eps = learner_params_.eps_out, action_policy = learner_params_.act_pol)


        qtable = learner.find_best_q_table()

        print "Final Q-Table Values: "
        print qtable

        # act_path =  learner.find_best_actions_at_each_state()

        env.visualise_optimal_path(qtable)

