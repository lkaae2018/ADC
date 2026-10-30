import matplotlib
matplotlib.use('TkAgg')

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# ===== PARAMETRE =====
f_signal_init = 5
fs_init = 20
bits_init = 8

V_rms = 230
V_peak = V_rms * np.sqrt(2)
V_range = 2 * V_peak  # fra -peak til +peak

t_cont = np.linspace(0, 1, 1000)

fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.4)

# ===== FUNKTION =====
def get_sampled(fs, f_signal):
    Ts = 1 / fs
    t_sampled = np.arange(0, 1, Ts)
    sampled_signal = np.sin(2 * np.pi * f_signal * t_sampled)
    return t_sampled, sampled_signal

def calc_lsb(bits):
    return V_range / (2 ** bits)

# ===== INITIAL =====
analog_signal = np.sin(2 * np.pi * f_signal_init * t_cont)
t_sampled, sampled_signal = get_sampled(fs_init, f_signal_init)

[line_analog] = ax.plot(t_cont, analog_signal, color='red', label="Analog signal")
stem = ax.stem(t_sampled, sampled_signal, linefmt='b-', markerfmt='bo')

text_lsb = ax.text(0.02, 0.95, "", transform=ax.transAxes)

ax.set_ylim(-1.5, 1.5)
ax.set_title("ADC Simulation med LSB")
ax.legend()
ax.grid()

# ===== SLIDERS =====
ax_freq = plt.axes([0.2, 0.25, 0.65, 0.03])
ax_fs = plt.axes([0.2, 0.18, 0.65, 0.03])
ax_bits = plt.axes([0.2, 0.11, 0.65, 0.03])

slider_freq = Slider(ax_freq, 'Signal frekvens', 1, 20, valinit=f_signal_init)
slider_fs = Slider(ax_fs, 'Sampling frekvens', 2, 100, valinit=fs_init)
slider_bits = Slider(ax_bits, 'Bits', 1, 16, valinit=bits_init, valstep=1)

# ===== UPDATE =====
def update(val):
    f_signal = slider_freq.val
    fs = slider_fs.val
    bits = int(slider_bits.val)

    # Signal
    analog_signal = np.sin(2 * np.pi * f_signal * t_cont)
    line_analog.set_ydata(analog_signal)

    t_sampled, sampled_signal = get_sampled(fs, f_signal)

    stem.markerline.set_data(t_sampled, sampled_signal)
    stem.stemlines.set_segments(
        [[[x, 0], [x, y]] for x, y in zip(t_sampled, sampled_signal)]
    )

    # LSB beregning
    lsb = calc_lsb(bits)

    text_lsb.set_text(f"LSB på 230V= {lsb:.4f} V")

    fig.canvas.draw_idle()

slider_freq.on_changed(update)
slider_fs.on_changed(update)
slider_bits.on_changed(update)

update(None)

plt.show()