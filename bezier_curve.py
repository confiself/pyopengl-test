from matplotlib import pyplot as plt
import numpy as np
NUM_STEPS = 30 #越大，曲线越密，越逼近

def circle(x,y,r,count=1000):
    xarr=[]
    yarr=[]
    for i in range(count):
        j = float(i)/count * 2 * np.pi
        xarr.append(x+r*np.cos(j))
        yarr.append(y+r*np.sin(j))
    return xarr, yarr

def curve4(x1, y1, x2,y2, x3, y3, x4, y4):
    # Anchor1 Control1 Control2 Anchor2
    p = []
    p.append((x1, y1))
    dx1 = x2 - x1
    dy1 = y2 - y1
    dx2 = x3 - x2
    dy2 = y3 - y2
    dx3 = x4 - x3
    dy3 = y4 - y3

    subdiv_step  = 1.0 / (NUM_STEPS + 1)
    subdiv_step2 = subdiv_step*subdiv_step
    subdiv_step3 = subdiv_step*subdiv_step*subdiv_step

    pre1 = 3.0 * subdiv_step
    pre2 = 3.0 * subdiv_step2
    pre4 = 6.0 * subdiv_step2
    pre5 = 6.0 * subdiv_step3

    tmp1x = x1 - x2 * 2.0 + x3
    tmp1y = y1 - y2 * 2.0 + y3

    tmp2x = (x2 - x3)*3.0 - x1 + x4
    tmp2y = (y2 - y3)*3.0 - y1 + y4

    fx = x1
    fy = y1

    dfx = (x2 - x1)*pre1 + tmp1x*pre2 + tmp2x*subdiv_step3
    dfy = (y2 - y1)*pre1 + tmp1y*pre2 + tmp2y*subdiv_step3

    ddfx = tmp1x*pre4 + tmp2x*pre5
    ddfy = tmp1y*pre4 + tmp2y*pre5

    dddfx = tmp2x*pre5
    dddfy = tmp2y*pre5

    step = NUM_STEPS

    while step > 0:
        fx  += dfx
        fy   += dfy
        dfx  += ddfx
        dfy  += ddfy
        ddfx += dddfx
        ddfy += dddfy
        p.append((fx, fy))
        step -= 1
    p.append((x4,y4))
    return p
def test_curve4():
    points = curve4(375, 435, 529, 569, 701, 450, 539, 312)
    print(points)
    x_data = [x[0] for x in points]
    y_data = [x[1] for x in points]
    plt.plot(x_data, y_data)
    plt.show()
    print(x_data)

def test_circle():
    x, y = circle(544, 443, r=144)
    plt.plot(x, y)
    plt.show()

def test_circle_1():
    x = [-0.14, 0.01, 0.18, 0.02, 0.03]
    y = [0.03, 0.19, 0.00, -0.12, 0.04]
    plt.plot(x, y)
    plt.show()


if __name__ == '__main__':
    test_circle_1()