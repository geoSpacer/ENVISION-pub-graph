#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      olsenk
#
# Created:     19/06/2017
# Copyright:   (c) olsenk 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import matplotlib.pyplot as plt
from numpy.random import rand
from numpy import arange

def main():

    val = 3-6*rand(5)    # the bar lengths
    pos = arange(5)+.5    # the bar centers on the y axis
    print pos

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.barh(pos,val, align='center',height=0.1)
    ax.set_yticks(pos, ('Tom', 'Dick', 'Harry', 'Slim', 'Jim'))

    ax.axvline(0,color='k',lw=3)   # poor man's zero level

    ax.set_xlabel('Performance')
    ax.set_title('horizontal bar chart using matplotlib')
    ax.grid(True)
    plt.show()

if __name__ == '__main__':
    main()
