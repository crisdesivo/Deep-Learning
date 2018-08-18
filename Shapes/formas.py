import pygame
from pygame.locals import *
import numpy as np
import tensorflow as tf

image = tf.placeholder(tf.float32, shape=[1, 500, 500, 1], name="image")
real_shape = tf.placeholder(tf.float32, shape=[1, 4], name='shape')

layer = tf.layers.conv2d(image, 10, 5, strides=2, padding='valid')
layer = tf.nn.relu(layer)
layer = tf.layers.average_pooling2d(layer, 3, 2)
layer = tf.layers.dropout(layer)
layer = tf.layers.conv2d(image, 20, 21, strides=10, padding='valid')
layer = tf.nn.relu(layer)
layer = tf.layers.average_pooling2d(layer, 3, 2)
layer = tf.layers.dropout(layer)
layer = tf.layers.flatten(layer)
print(layer.shape)
layer = tf.layers.dense(layer, 50)
layer = tf.nn.relu(layer)
logits = tf.layers.dense(layer, 4)
output = tf.nn.softmax(logits, name="output")

saver = tf.train.Saver()
cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(labels=real_shape, logits=logits))
optimizer = tf.train.AdamOptimizer().minimize(cost)
diff = tf.cast(tf.equal(tf.argmax(real_shape, axis=1), tf.argmax(output, axis=1)), tf.float32)
accuracy = tf.reduce_mean(diff, name="accuracy")

sess = tf.Session()
sess.run(tf.global_variables_initializer())

def ren(array):
    return range(len(array))


pygame.init()
screen=pygame.display.set_mode((500, 500),pygame.RESIZABLE|DOUBLEBUF)
screen_on = True

x=250
y=250

def square(screen, x, y, s):
    pygame.draw.rect(screen, (0,0,0), (x-s/2, y-s/2, s, s))
def circle(screen, x, y, s):
    pygame.draw.circle(screen, (0,0,0), (x, y), int(s*0.66))
def triangle(screen, x, y, s):
    p1= (x, y+s/2)
    p2= (x-s/2, y-s/2)
    p3= (x + s/2, y-s/2)
    pygame.draw.polygon(screen, (0,0,0), (p1, p2, p3))
def star(screen, x, y, s):
    n=5
    q=3
    p = [(x+s*np.sin(i*2*np.pi/n), y-s*np.cos(i*2*np.pi/n)) for i in range(n)]
    order = [p[(q*i)%n] for i in range(n)]
    pygame.draw.polygon(screen, (0,0,0), order)
shapes=[square, circle, triangle, star]
time = 0
recent_acc=0
while screen_on:
    pygame.draw.rect(screen, (255, 255, 255), (0, 0, 500, 500))
    r1=np.random.randint(0, high=len(shapes))
    r2=np.random.randint(20, high=200)
    r3=np.random.randint(r2, high=500-r2)
    r4=np.random.randint(r2, high=500-r2)
    shapes[r1](screen, r3, r4, r2)
    pygame.display.flip()
    pixeles = np.array(pygame.surfarray.array2d(screen)).reshape([-1,500,500,1])/16777215
    shape=np.array([0,0,0,0])
    shape[r1] = 1
    acc, _ = sess.run([accuracy, optimizer], feed_dict={image: pixeles, real_shape: [shape]})
    if time%100==0:
        print(recent_acc)
        recent_acc=acc*0.01
    else:
        recent_acc+=acc*0.01
    time+=1
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == K_ESCAPE:
                saver.save(sess, "/tmp_formas/model.ckpt")
                pygame.quit()
                screen_on = False