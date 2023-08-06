from typing import List, Union, Dict, Tuple, Iterable

import matplotlib.pyplot as plt
import numpy as np
from mysutils.collections import merge_tuples


def plot_measures(measures: List[Union[float, Tuple[float, float]]],
                  xticks: Iterable[str],
                  filename: str = None,
                  color: str = 'black',
                  capsize: int = 3,
                  linestyle: str = 'None',
                  marker: str = 's',
                  markersize: int = 7,
                  mfc: str = 'black',
                  mec: str = 'black',
                  **kwargs) -> None:
    d = {name: measures[i] for i, name in enumerate(xticks)}
    plot_measure(d, xticks, filename, color, capsize, linestyle, marker, markersize, mfc, mec, **kwargs)


def plot_measure(measure: Dict[str, Union[float, Tuple[float, float]]],
                 detail: bool = True,
                 xticks: Iterable[str] = None,
                 filename: str = None,
                 color: str = 'black',
                 capsize: int = 3,
                 linestyle: str = 'None',
                 marker: str = 's',
                 markersize: int = 7,
                 mfc: str = 'black',
                 mec: str = 'black',
                 **kwargs) -> None:
    x = np.arange(1, len(measure) + 1)
    plt.figure(figsize=(8,7))
    plt.xticks(x, xticks if xticks else measure, rotation=90)
    if not detail:
        plt.ylim(ymin=0)
    if measure.values() and isinstance(list(measure.values())[0], tuple):
        y, err = merge_tuples(measure.values())
        plt.errorbar(x=x, y=y, yerr=err, color=color, capsize=capsize, linestyle=linestyle, marker=marker,
                     markersize=markersize, mfc=mfc, mec=mec, **kwargs)
    else:
        plt.bar(x=x, height=measure.values(), color=color, capsize=capsize, linestyle=linestyle, **kwargs)
    plt.tight_layout()
    if filename:
        plt.savefig(filename)
    else:
        plt.show()
    plt.close()
