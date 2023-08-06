from typing import Tuple

import numpy as np

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.components.rectangle import rectangle
from gdsfactory.components.taper import taper


@gf.cell
def grating_coupler_rectangular(
    n_periods: int = 20,
    period: float = 0.75,
    fill_factor: float = 0.5,
    width_grating: float = 11.0,
    length_taper: float = 150.0,
    wg_width: float = 0.5,
    layer: Tuple[int, int] = gf.LAYER.WG,
    polarization: str = "te",
    wavelength: float = 1.55,
) -> Component:
    r"""Grating coupler uniform (grating with rectangular shape not elliptical).
    Therefore it needs a longer taper.
    Grating teeth are straight instead of elliptical.

    Args:
        n_periods: 20
        period: 0.75
        fill_factor: 0.5
        width_grating: 11
        length_taper: 150
        wg_width: 0.5

    .. code::

                 \  \  \  \
                  \  \  \  \
                _|-|_|-|_|-|___
               |_______________  W0

    """
    c = Component()
    taper_ref = c << taper(
        length=length_taper,
        width2=width_grating,
        width1=wg_width,
        layer=layer,
    )

    c.add_port(port=taper_ref.ports["o1"], name="o1")
    x0 = taper_ref.xmax

    for i in range(n_periods):
        xsize = gf.snap.snap_to_grid(period * fill_factor)
        cgrating = c.add_ref(
            rectangle(size=[xsize, width_grating], layer=layer, port_type=None)
        )
        cgrating.x = gf.snap.snap_to_grid(x0 + i * period)
        cgrating.y = 0

    xport = np.round((x0 + cgrating.x) / 2, 3)

    port_type = f"vertical_{polarization.lower()}"
    c.add_port(name=port_type, port_type=port_type, midpoint=(xport, 0), orientation=0)
    c.info.polarization = polarization
    c.info.wavelength = wavelength
    gf.asserts.grating_coupler(c)
    return c


if __name__ == "__main__":
    # c = grating_coupler_rectangular(name='gcu', partial_etch=True)
    c = grating_coupler_rectangular()
    print(c.ports)
    c.show()
