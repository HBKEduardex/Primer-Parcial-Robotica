# Proyecto Final – Cinemática Directa e Inversa (ROS2)

Este repositorio contiene el trabajo final realizado en ROS2 Humble, donde se implementaron las cinemáticas directa e inversa de una mano robótica compuesta por el dedo índice y el pulgar, además de los nodos publisher y subscriber del ejercicio 1.

---

## Integrantes
- Adrián Eduardo Vargas Llanquipacha  
- Israel Silva Bernal

---

## Estructura del proyecto

**1. robot_description**  
Contiene los modelos URDF de los dedos y los archivos launch para visualizarlos en RViz.  
Aquí se encuentran las cinemáticas directas e inversas del índice, del pulgar y de ambos como una mano (seis launch en total).  
Cada modelo se lanza con su propio `robot_state_publisher` y se une al frame común `world`.  
Los archivos `.launch.py` permiten activar o desactivar el `joint_state_publisher_gui`.

**2. visual_pubsub**  
Incluye los códigos de cinemática inversa:  
- `inverse_kinematics_indice.py`  
- `inverse_kinematics_pulgar.py`  
- `inverse_kinematics_hand.py`  

Se usan las matrices Jacobianas y el método Damped Least Squares (DLS).  
Cada clase tiene su función `update_joints()` para calcular la posición actual, el error y actualizar las articulaciones hasta alcanzar el target.  
Los resultados se visualizan en RViz mientras se muestran los valores en consola.

**3. ej1**  
Contiene los cinco nodos publisher y subscriber del primer ejercicio.  
Los nodos 1, 2 y 3 simulan sensores, el nodo 4 promedia los datos y el nodo 5 muestra el resultado final.  
Se utiliza el mensaje `examen_msg` (similar al `filter_sensor` del ejemplo visto en clase).

---

## Ejecución básica

```bash
# Compilar
colcon build
source install/setup.bash

# Visualizar los dedos (sin GUI)
ros2 launch robot_description cinematica_inversa_hand.launch.py gui:=false

# Ejecutar la cinemática inversa completa
ros2 run visual_pubsub inverse_kinematics_hand
