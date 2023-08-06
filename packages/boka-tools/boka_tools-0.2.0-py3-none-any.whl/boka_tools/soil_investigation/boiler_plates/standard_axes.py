
def cone_resistance(qc, Rf):

    plot_qc = dict(
        ax='ax1',
        name='qc',
        type='plot',
        x_data=qc,
        kwargs=dict(color='black', ls='-', lw=1.5, label='qc')
        )

    plot_Rf = dict(
        ax='ax1_2',
        name='Rf',
        type='plot',
        x_data=Rf,
        kwargs=dict(color='red', lw=1, label='Rf')
        )

    ax1 = ax1=dict(xlim=[0, 10], xlabel='Cone Resistance [MPa]', ylabel='Elevation [m+CD]')
    ax1_2 = dict(
                    twin='ax1',
                    kwargs=dict(
                        xticks=[x for x in range(0, 6, 1)],
                        xticklabels=['' if x == 0 else str(x) for x in range(0, 6, 1)],
                        xlim=[25, 0],
                        xlabel='Rf [%]'
                        )
        )

    return [plot_qc, plot_Rf, ax1, ax1_2]