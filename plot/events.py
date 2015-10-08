class MousePlotEvents:
    def __init__(self):
        self.press = False
        self.cur_xlim = None
        self.cur_ylim = None
        self.xpress = None
        self.ypress = None

        self.start_xlim = None
        self.start_ylim = None

    def zoom(self, ax, zoom_scale=1.1):
        def zoom(event):
            if event.inaxes != ax:
                return

            cur_xlim = ax.get_xlim()
            cur_ylim = ax.get_ylim()

            xdata = event.xdata
            ydata = event.ydata

            if event.button == 'down':
                scale_factor = 1 / zoom_scale
            elif event.button == 'up':
                scale_factor = zoom_scale
            else:
                scale_factor = 1
                print event.button

            new_width = (cur_xlim[1] - cur_xlim[0]) * scale_factor
            new_height = (cur_ylim[1] - cur_ylim[0]) * scale_factor

            relx = (cur_xlim[1] - xdata)/(cur_xlim[1] - cur_xlim[0])
            rely = (cur_ylim[1] - ydata)/(cur_ylim[1] - cur_ylim[0])

            ax.set_xlim([xdata - new_width * (1-relx), xdata + new_width * (relx)])
            ax.set_ylim([ydata - new_height * (1-rely), ydata + new_height * (rely)])
            ax.figure.canvas.draw()

        fig = ax.get_figure() # get the figure of interest
        fig.canvas.mpl_connect('scroll_event', zoom)

        return zoom

    def move(self, ax):
        def on_press(event):
            if event.inaxes != ax:
                return

            if event.button == 1:
                self.cur_xlim = ax.get_xlim()
                self.cur_ylim = ax.get_ylim()
                self.press = True
                self.xpress = event.xdata
                self.ypress = event.ydata

        def on_release(event):
            if event.button == 1:
                self.press = False
                ax.figure.canvas.draw()

        def on_motion(event):
            if not self.press:
                return
            if event.inaxes != ax:
                return
            dx = event.xdata - self.xpress
            dy = event.ydata - self.ypress
            self.cur_xlim -= dx
            self.cur_ylim -= dy
            ax.set_xlim(self.cur_xlim)
            ax.set_ylim(self.cur_ylim)

            ax.figure.canvas.draw()

        # get the figure of interest
        fig = ax.get_figure()

        # attach the call back
        fig.canvas.mpl_connect('button_press_event', on_press)
        fig.canvas.mpl_connect('button_release_event', on_release)
        fig.canvas.mpl_connect('motion_notify_event', on_motion)

    def reset(self, ax):
        # TODO: Add third dimensional to reset
        def right_button_pressed(event):
            if event.inaxes != ax:
                return

            elif event.button == 3:
                ax.set_xlim(self.start_xlim)
                ax.set_ylim(self.start_ylim)
                ax.figure.canvas.draw()

        # get the figure of interest
        fig = ax.get_figure()

        self.start_xlim = ax.get_xlim()
        self.start_ylim = ax.get_ylim()

        fig.canvas.mpl_connect('button_press_event', right_button_pressed)