# Primer Parcial ROS2 
---

## Integrantes
- Adrián Eduardo Vargas Llanquipacha  
- Israel Silva Bernal

---

## Estructura del proyecto

**1. robot_description**  
Contiene los modelos URDF de los dedos y los archivos launch para visualizarlos en RViz.  
Aquí se encuentran las cinemáticas directas e inversas del índice, del pulgar y de ambos como una mano (seis launch en total).  
Lo que se averiguó para hacer los dos dedos en una misma visualización fue añadir un fixed frame world donde se podrá visualizar y
aplicar la cinemática inversa. Además, se puso nombres individuales a cada link, joint para diferenciar entre pulgar e índice.

**2. visual_pubsub**  
Incluye los códigos de cinemática inversa:  
- `inverse_kinematics_indice.py`  
- `inverse_kinematics_pulgar.py`  
- `inverse_kinematics_hand.py`  


**3. ej1**  
Contiene los cinco nodos del primer ejercicio.  
Los nodos 1, 2 y 3 simulan sensores, el nodo 4 promedia los datos y el nodo 5 muestra el resultado final.  
Se utiliza el mensaje `examen_msg` en reemplazo del nombre filtered sensor, igual se usa lo de float y String.

---

## Ejecución básica

```bash
# Compilar
colcon build
source install/setup.bash

# Visualizar los dedos (sin GUI)
ros2 launch robot_description cinematica_inversa_hand.launch.py

# Ejecutar la cinemática inversa completa
ros2 run visual_pubsub inverse_kinematics_hand

#Ejecucion de los nodos 1, 2, 3 y 4
ros2 launch ejer1 all_nodes.launch.py
#Ejecucion del nodo 5, indicando en consola el promedio y el nombre de los topicos
ros2 run ejer1 nodo5_sub
