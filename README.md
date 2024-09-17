# Detector de Cáncer de Piel con TensorFlow

Este proyecto utiliza TensorFlow para construir un modelo de aprendizaje profundo que detecta el cáncer de piel a partir de imágenes. El modelo está entrenado para clasificar imágenes de lesiones cutáneas como benignas o malignas.

## Características del Proyecto

- **Preprocesamiento de Datos**: Utiliza `ImageDataGenerator` para la augmentación de datos y la normalización.
- **Arquitectura del Modelo**: Una red neuronal convolucional (CNN) con múltiples capas de convolución y pooling.
- **Entrenamiento del Modelo**: Entrenado con un conjunto de datos de imágenes de lesiones cutáneas, utilizando técnicas de ajuste de pesos de clase para manejar el desbalance de clases.
- **Evaluación del Modelo**: Evaluado en un conjunto de datos de validación para medir su precisión y pérdida.
- **Guardado del Modelo**: El modelo entrenado se guarda en un archivo `.h5` para su uso futuro.

## Requisitos

- Python 3.x
- TensorFlow 2.x
- Un conjunto de datos de imágenes de lesiones cutáneas

## Instalación

1. Clona este repositorio:
    ```bash
    git clone https://github.com/TFTomasFernandez/AI-Detected-Cancer.git
    cd tu_repositorio
    ```

2. Instala las dependencias:
    ```bash
    pip install tensorflow
    ```

3. Coloca tu conjunto de datos en la carpeta `train` con la siguiente estructura:
    ```
    train/
    ├── benign/
    │   ├── imagen1.jpg
    │   ├── imagen2.jpg
    │   └── ...
    └── malignant/
        ├── imagen1.jpg
        ├── imagen2.jpg
        └── ...
    ```

## Uso

1. Ejecuta el script de entrenamiento:
    ```bash
    jupyter notebook MVP.ipynb
    ```

2. El modelo entrenado se guardará como [`modelo_cancer_piel.h5`](command:_github.copilot.openRelativePath?%5B%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fc%3A%2FUsers%2Ftomif%2FDesktop%2FAI%20Detectora%20de%20Cancer%20de%20Piel%2Fmodelo_cancer_piel.h5%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22755ed039-28e4-498b-88bc-152f29c42a5e%22%5D "c:\Users\tomif\Desktop\AI Detectora de Cancer de Piel\modelo_cancer_piel.h5").


## Pruebas

1. Ejecuta el script de Test:
    ```bash
    jupyter notebook Test_Model.ipynb
    ```
2. Cambia las rutas de imagenes y ejecuta
   ```bash
    image_path = r'tu/ruta/de/pruba'
    ```
3. Imagenes de prueba:

![Imagen 1](https://github.com/TFTomasFernandez/AI-Detected-Cancer/blob/Repositorio/train/Benigno/15.jpg) ![](https://github.com/TFTomasFernandez/AI-Detected-Cancer/blob/Repositorio/Image/Probabilidad%20benigna.png)

![Imagen 2](https://github.com/TFTomasFernandez/AI-Detected-Cancer/blob/Repositorio/train/Maligno/50.jpg) ![](https://github.com/TFTomasFernandez/AI-Detected-Cancer/blob/Repositorio/Image/Probabilidad%20maligna.png)
   

