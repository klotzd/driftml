#%%
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from scipy import ndimage
import matplotlib.cbook as cbook

filename = "BAnumpy1.npy"
dfall = np.load(filename)
# x/y grid center points
x_cords = np.linspace(0.1, 5.9, 30)
y_cords = np.linspace(0.1, 1.9, 10)
xv, yv = np.meshgrid(x_cords, y_cords, sparse=False, indexing="ij")
# one timestep only
sz = np.shape(dfall)[2]
count = 0
#%%
count = 0
# source coords
x_s = 0.5
y_s = 1
zmax = 0
while count < sz:
    df = dfall[:, :, count]

    # populate z set
    z = np.zeros((30, 10))
    for x in range(30):
        for y in range(10):
            z[x, y] = df[x, y] / 0.095 * 100
    zmax1 = np.amax(z)
    if zmax1 > zmax:
        zmax = zmax1
    count = count+1
#%%
# source coords
x_s = 0.5
y_s = 1

count = 0
while count < sz:
    df = dfall[:, :, count]

    # populate z set
    z = np.zeros((30, 10))
    for x in range(30):
        for y in range(10):
            z[x, y] = (df[x, y] / 0.095 * 100)/zmax
    # contour plotprint(
    fig1, ax1 = plt.subplots(figsize=(12, 6))
    
    bounds = np.linspace(0, 1, 41)
    
    norm = colors.BoundaryNorm(boundaries=bounds, ncolors=256)
    #conm = ax1.contourf(xv, yv, z, norm = norm, cmap=plt.cm.hot, levels = bounds)
    conm = ax1.pcolormesh(xv, yv, z, norm = norm, cmap=plt.cm.hot)
    
    orig = ax1.plot(x_s, y_s, "xr", markersize=12)

    cbar = fig1.colorbar(conm, ax=ax1, extend='both', orientation='vertical')

    cbar.set_label('norm. deposition density')
    timestep = count*0.25+ 0.25
    ax1.set_title(('Timestep = ' + str(timestep)) + 's')
    ax1.set_xlabel("x distance / m")
    ax1.set_ylabel("y distance / m")
    #ax1.annotate(filename, xy=(4, -0.15), xycoords='data', annotation_clip=False)

    #fig1 = plt.gcf()
    
    fig1.savefig(('/home/sam/Documents/openfoam-spray-runs/visualisation/figs/time' + str(count) + '.png'), bbox_inches = 'tight',
    pad_inches = 0)
    count = count+1

#%%
# grid plot
plt.figure(figsize=(12, 6))
plt.pcolormesh(xv, yv, z, cmap=plt.cm.hot)
#plt.show()
plt.plot(x_s, y_s, "xr", markersize=12)
plt.xlabel("x distance / m")
plt.ylabel("y distance / m")
#plt.colorbar(ax=ax)
plt.show()
# %%
import pylab as plb
from scipy.optimize import curve_fit
from scipy import asarray as ar,exp

x = y_cords
y = z
n = len(y)                          #the number of data
mean = sum(x*y)/n                   #note this correction
sigma = np.sqrt(sum(y*(x-mean)**2)/n)       #note this correction
#%%
import imageio
images = []
count = 0
while count < sz:
     filename = ('/home/sam/Documents/openfoam-spray-runs/visualisation/figs/time' + str(count) + '.png')

     images.append(imageio.imread(filename))
     imageio.mimsave('/home/sam/Documents/openfoam-spray-runs/visualisation/figs/plotmovie.gif', images, format='GIF', fps=4)
     count = count+1

# %%
import java.awt.Color;
import java.awt.Graphics2D;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import javax.imageio.ImageIO;
/**
 * This code try to join two BufferedImage
 * @author wangdq
 * 2013-12-29
 */
public class JoinImage {
    public static void main(String args[])
    {   
        String filename = System.getProperty("user.home")+File.separator;
        try {
            BufferedImage img1 = ImageIO.read(new File(filename+"1.png"));
            BufferedImage img2=ImageIO.read(new File(filename+"2.png"));
            BufferedImage joinedImg = joinBufferedImage(img1,img2);
            boolean success = ImageIO.write(joinedImg, "png", new File(filename+"joined.png"));
            System.out.println("saved success? "+success);
        } catch (IOException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
    }
    /**
     * join two BufferedImage
     * you can add a orientation parameter to control direction
     * you can use a array to join more BufferedImage
     */

    public static BufferedImage joinBufferedImage(BufferedImage img1,BufferedImage img2) {

        //do some calculate first
        int offset  = 5;
        int wid = img1.getWidth()+img2.getWidth()+offset;
        int height = Math.max(img1.getHeight(),img2.getHeight())+offset;
        //create a new buffer and draw two image into the new image
        BufferedImage newImage = new BufferedImage(wid,height, BufferedImage.TYPE_INT_ARGB);
        Graphics2D g2 = newImage.createGraphics();
        Color oldColor = g2.getColor();
        //fill background
        g2.setPaint(Color.WHITE);
        g2.fillRect(0, 0, wid, height);
        //draw image
        g2.setColor(oldColor);
        g2.drawImage(img1, null, 0, 0);
        g2.drawImage(img2, null, img1.getWidth()+offset, 0);
        g2.dispose();
        return newImage;
    }
}