from matplotlib import rcParams
import matplotlib.pyplot as plt
import numpy as np

rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Arial']

class MTKCDPrinterBuilder:

    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.current_row = 0
        self.current_colummn = 0
        self.fig, self.axes = plt.subplots(rows, columns)

    def new_columns(self):
        self.current_colummn+=1
        return self

    def first_row(self):
        self.current_row = 0
        return self

    def get_axis(self):
        if (self.rows > 1):
            if (self.columns > 1):
                ax1 = self.axes[self.current_row, self.current_colummn]
            else:
                ax1 = self.axes[self.current_row]
        else:
            if (self.columns > 1):
                ax1 = self.axes[self.current_colummn]
            else:
                ax1 = self.axes
        return ax1

    def add_spec(self, segment, delta_j, Fs, SG, frq):

        ax = self.get_axis()

        start_sec = segment[0]
        end_sec = segment[1]

        start_spec = (start_sec*Fs) // (delta_j)
        end_spec = (end_sec*Fs) // (delta_j)

        segment = [SG[i][int(start_spec):int(end_spec)] for i in range(0, len(frq))]
        ax.imshow(segment, aspect='auto', interpolation='bicubic', cmap='jet', origin='lower',
                         extent=[start_sec, end_sec, 1, frq[len(frq) - 1]])
        ax.set_ylabel("Frequency (Hz)")

        self.current_row+=1

        return self

    def add_kc_markings(self, segment, x, Fs, kc_markings, color, min_y=-150, max_y=150):

        ax = self.get_axis()

        start_segment_sec = segment[0]
        end__segment_sec = segment[1]

        start_segment = start_segment_sec * Fs
        end_segment = end__segment_sec * Fs


        x_axis_data = np.arange(start_segment, end_segment + 1)
        x_axis_data = [x / Fs for x in x_axis_data]
        sequence= x[int(start_segment):int(end_segment + 1)]

        if (len(sequence) < len(x_axis_data)):
            x_axis_data = x_axis_data[0:len(sequence)]

        ax.plot(x_axis_data,sequence, "#686868")
        ax.invert_yaxis()

        if(min_y!=None and max_y!=None):
            ax.set_ylim(max_y, min_y)


        # ax.set_xlabel("Time (s)")
        ax.set_ylabel("Amplitude $(\mu V$)")

        for kc in kc_markings:
                    # print(trecho)
                    start_kc_sec = float(kc[0])
                    start_kc = start_kc_sec * Fs

                    end_kc_sec = float(kc[1])
                    end_kc = end_kc_sec * Fs


                    if (start_kc_sec < end__segment_sec and start_kc_sec >= start_segment_sec):
                        start_kc = int(start_kc)
                        end_kc = int(end_kc)

                        if (start_kc < start_segment):
                            start_kc = start_segment

                        if (end_kc > end_segment):
                            end_kc = end_segment

                        x_axis = np.arange(start_kc, end_kc + 1)
                        x_axis = [x / Fs for x in x_axis]
                        sequence = x[int(start_kc):int(end_kc + 1)]
                        ax.plot(x_axis, sequence, color, linewidth=3.0)

        ax.margins(0, 0)

        self.current_row += 1
        return self

    def build(self, path, width=15, height=30, hspace=0.25, format='png'):


        self.fig.subplots_adjust(top=0.92, bottom=0.08, left=0.1, right=0.95, hspace=hspace,
                            wspace=0.35)

        self.fig.set_size_inches(width, height)
        self.fig.savefig(path, dpi=300, format=format)
