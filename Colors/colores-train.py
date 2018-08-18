import tensorflow as tf
import pandas as pd
import numpy as np

color = tf.placeholder(tf.float16, shape=[None, 3], name="color")
my_label = tf.placeholder(tf.float16, shape=[None, 12], name='my_label')

#layer = tf.layers.dense(color, 10)
#layer = tf.nn.relu(layer)
logits = tf.layers.dense(color, 12)
output = tf.nn.softmax(logits, name='output')

cost = tf.nn.softmax_cross_entropy_with_logits_v2(labels=my_label, logits=logits)
optimizer = tf.train.AdamOptimizer(name='optimizer').minimize(cost)

sess = tf.Session()
sess.run(tf.global_variables_initializer())

coloresData = pd.read_csv('coloresData.csv', header=None)


labels = coloresData.iloc[:,3]
colores = coloresData.iloc[:,:3]/255
labels = pd.get_dummies(labels)


for _ in range(10000):
    sess.run(optimizer, feed_dict={color: colores, my_label: labels})


#nombres = ['rojo', 'verde', 'azul', 'rosa', 'celeste', 'amarillo', 'marron', 'violeta', 'naranja', 'blanco', 'gris', 'negro']
#print(nombres[np.argmax(sess.run(output, feed_dict={color: [[0,1,0]]})[0])])